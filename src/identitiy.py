#!/usr/bin/env python3

import requests
import json
import argparse

auth_dict = json.load(open('json/auth.json', 'r'))
endpoint_dict = json.load(open('json/endpoint.json', 'r'))
tokens_dict = json.load(open('json/tokens.json', 'r'))
headers = {
  "X-Auth-Token": tokens_dict['access']['token']['id']
}

def post_tokens():
  url = endpoint_dict['IdentityService'] + '/tokens'
  tokens_dict = requests.post(url, data = json.dumps(auth_dict)).json()
  with open('json/tokens.json', 'w') as f:
    json.dump(tokens_dict, f, indent=4)
  return tokens_dict

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='ConoHa Identitiy API を用いた操作を行うスクリプトです')
    subparsers = parser.add_subparsers()

    parser_post_tokens = subparsers.add_parser('post_tokens', help='有効なトークン情報を取得する ')
    parser_post_tokens.set_defaults(handler=post_tokens)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
      args.handler(args)
    else:
      parser.print_help()