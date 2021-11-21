#!/usr/bin/env python3

import requests
import json
import argparse
import datetime
import identitiy

endpoint_dict = json.load(open('json/endpoint.json', 'r'))
headers = {
  "X-Auth-Token": identitiy.get_token_id('json/tokens.json')
}

def get_secgroups_list(args):
  secgroups_dict = requests.get(endpoint_dict['NetworkService'] + '/v2.0/security-groups', headers=headers).json()
  for security_group in secgroups_dict['security_groups']:
    print("name: " + security_group['name'])

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='ConoHa Network API を用いた操作を行うスクリプトです')
    subparsers = parser.add_subparsers()

    parser_get_secgroups_list = subparsers.add_parser('get_secgroups_list', help='セキュリティグループ一覧取得')
    parser_get_secgroups_list.set_defaults(handler=get_secgroups_list)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
      args.handler(args)
    else:
      parser.print_help()