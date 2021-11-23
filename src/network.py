#!/usr/bin/env python3

import requests
import json
import argparse
import datetime
import identity

endpoint_dict = json.load(open('json/endpoint.json', 'r'))
headers = {
  "X-Auth-Token": identity.get_token_id('json/tokens.json')
}

def get_secgroups_list():
  return requests.get(endpoint_dict['NetworkService'] + '/v2.0/security-groups', headers=headers).json()

def get_rules_on_secgroup():
  return requests.get(endpoint_dict['NetworkService'] + '/v2.0/security-group-rules', headers=headers).json()

def create_secgroup(args):
  name = input('セキュリティグループ名: ')
  description = input('セキュリティグループの説明: ')

  secgroup_dict ={
      "security_group": {
          "name": name,
          "description": description
      }
  }

  url = endpoint_dict['NetworkService'] + '/v2.0/security-groups'

  # アウトバウンド接続許可ポートは初期値で「全て許可」が設定される
  created_secgroup_dict = requests.post(url, data = json.dumps(secgroup_dict), headers=headers).json()
  with open('json/created_secgroup.json', 'w') as f:
    json.dump(created_secgroup_dict, f, indent=4)

def delete_secgroup(args):
  created_secgroup_dict = json.load(open('json/created_secgroup.json', 'r'))

  url = endpoint_dict['NetworkService'] + '/v2.0/security-groups/' + created_secgroup_dict['security_group']['id']
  print(requests.delete(url, headers=headers))

def create_rule_on_secgroup(args):
  created_secgroup_dict = json.load(open('json/created_secgroup.json', 'r'))

  port = input('許可するポート番号: ')

  secgroup_rule_dict = {
    "security_group_rule": {
        "direction": "ingress",
        "ethertype": "IPv4",
        "security_group_id": created_secgroup_dict['security_group']['id'],
        "port_range_min": port,
        "port_range_max": port,
        "protocol": "tcp"
    }
  }
  url = endpoint_dict['NetworkService'] + '/v2.0/security-group-rules'
  print(requests.post(url, data = json.dumps(secgroup_rule_dict), headers=headers).json())

def delete_rule_on_secgroup(args):
  secgroup_rules_dict = get_rules_on_secgroup()
  created_secgroup_dict = json.load(open('json/created_secgroup.json', 'r'))
  for secgroup_rule_dict in secgroup_rules_dict['security_group_rules']:
    if created_secgroup_dict['security_group']['id'] != secgroup_rule_dict['security_group_id']: continue
    print("セキュリティグループルールID: " + secgroup_rule_dict['id'])
    print("許可ポート番号: " + str(secgroup_rule_dict['port_range_min']))
    print("----------")

  secgroup_rule_id = input('削除したいセキュリティグループルールID: ')
  url = endpoint_dict['NetworkService'] + '/v2.0/security-group-rules/' + secgroup_rule_id
  print(requests.delete(url, headers=headers))

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='ConoHa Network API を用いた操作を行うスクリプトです')
    subparsers = parser.add_subparsers()

    parser_create_secgroup = subparsers.add_parser('create_secgroup', help='セキュリティグループ作成')
    parser_delete_secgroup = subparsers.add_parser('delete_secgroup', help='セキュリティグループ削除')
    parser_create_rule_on_secgroup = subparsers.add_parser('create_rule_on_secgroup', help='セキュリティグループ ルール作成')
    parser_delete_rule_on_secgroup = subparsers.add_parser('delete_rule_on_secgroup', help='セキュリティグループ ルール削除')

    parser_create_secgroup.set_defaults(handler=create_secgroup)
    parser_delete_secgroup.set_defaults(handler=delete_secgroup)
    parser_create_rule_on_secgroup.set_defaults(handler=create_rule_on_secgroup)
    parser_delete_rule_on_secgroup.set_defaults(handler=delete_rule_on_secgroup)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
      args.handler(args)
    else:
      parser.print_help()