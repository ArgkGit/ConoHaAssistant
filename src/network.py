#!/usr/bin/env python3

import requests
import json
import argparse
import datetime
import identitiy

endpoint_dict = json.load(open('json/endpoint.json', 'r'))
tokens_dict = json.load(open('json/tokens.json', 'r'))

# トークンが有効期限内か確認
dt_now = datetime.datetime.now()
dt_expires = datetime.datetime.fromisoformat(tokens_dict['access']['token']['expires'].replace('Z', '+00:00') )
if dt_expires.astimezone() < dt_now.astimezone() :
  tokens_dict = identitiy.post_tokens()

headers = {
  "X-Auth-Token": tokens_dict['access']['token']['id']
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