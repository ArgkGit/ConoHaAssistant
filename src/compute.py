#!/usr/bin/env python3

import requests
import json
import argparse

endpoint_dict = json.load(open('json/endpoint.json', 'r'))
tokens_dict = json.load(open('json/tokens.json', 'r'))
headers = {
  "X-Auth-Token": tokens_dict['access']['token']['id']
}

def get_flavors_detail():
  return requests.get(endpoint_dict['ComputeService'] + '/flavors/detail', headers=headers).json()

def get_images():
  return requests.get(endpoint_dict['ComputeService'] + '/images', headers=headers).json()

def create_vm(args):
  images_dict = get_images()
  for image_dict in images_dict['images']:
    # デフォルトで用意されているイメージは除く
    if "vmi-" in image_dict['name']: continue

    print("----------")
    print("イメージID: " + image_dict['id'])
    print("イメージ名: " + image_dict['name'])

  image_id = input('使用したいイメージID: ')

  flavors_detail_dict = get_flavors_detail()
  for flavor_dict in flavors_detail_dict['flavors']:
    # 旧プランはスキップ
    if flavor_dict['disk'] == 20: continue
    if flavor_dict['disk'] == 50: continue
    print("----------")
    print("プランID: " + flavor_dict['id'])
    print("メモリ: " + str(flavor_dict['ram']) + "MB, CPU: " + str(flavor_dict['vcpus']) + "コア, ディスク容量: " +  str(flavor_dict['disk']) + "GB")

  plan_id = input('使用したいプランID: ')
  admin_pass = input("rootパスワード: ")

  server_dict = {
    "server": {
        "imageRef": image_id,
        "flavorRef": plan_id,
        "adminPass":admin_pass
    }
  }

  url = endpoint_dict['ComputeService'] + '/servers'

  created_server_dict = requests.post(url, data = json.dumps(server_dict), headers=headers).json()
  with open('json/created_server.json', 'w') as f:
    json.dump(created_server_dict, f, indent=4)

def stop_cleanly_vm(args):
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  url = endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id'] +'/action'
  print(requests.post(url, data = '{"os-stop": null}', headers=headers))

def create_image(args):
  name = input('イメージ名: ')
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  url = endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id'] +'/action'

  # 409のときはシャットダウンされていない可能性あり
  print(requests.post(url, data = '{"createImage": {"name": name}}', headers=headers))

def delete_vm(args):
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  url = endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id']
  print(requests.delete(url, headers=headers))

if __name__ == '__main__':
 
    parser = argparse.ArgumentParser(description='ConoHa Compute API を用いた操作を行うスクリプトです')
    subparsers = parser.add_subparsers()

    parser_create_vm = subparsers.add_parser('create_vm', help='サーバー追加')
    parser_stop_cleanly_vm = subparsers.add_parser('stop_cleanly_vm', help='サーバーシャットダウン')
    parser_create_image = subparsers.add_parser('create_image', help='イメージ保存')
    parser_delete_vm = subparsers.add_parser('delete_vm', help='サーバー削除')

    parser_create_vm.set_defaults(handler=create_vm)
    parser_stop_cleanly_vm.set_defaults(handler=stop_cleanly_vm)
    parser_create_image.set_defaults(handler=create_image)
    parser_delete_vm.set_defaults(handler=delete_vm)
    
    args = parser.parse_args()

    if hasattr(args, 'handler'):
      args.handler(args)
    else:
      parser.print_help()