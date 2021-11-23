#!/usr/bin/env python3

import requests
import json
import argparse

import time
import os

import identity
import network

endpoint_dict = json.load(open('json/endpoint.json', 'r'))
headers = {
  "X-Auth-Token": identity.get_token_id('json/tokens.json')
}

def get_flavors_detail():
  return requests.get(endpoint_dict['ComputeService'] + '/flavors/detail', headers=headers).json()

def get_images():
  return requests.get(endpoint_dict['ComputeService'] + '/images', headers=headers).json()

def get_image_id(image_name):
  images_dict = get_images()
  for image_dict in images_dict['images']:
    if image_name == image_dict['name']:
      return image_dict['id']

def get_images_detail_specified(image_id):
  return requests.get(endpoint_dict['ComputeService'] + '/images/' + image_id, headers=headers).json()

def get_vms_detail_specified():
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  return requests.get(endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id'], headers=headers).json()

def create_vm(args):
  conf_path = 'json/create_vm_conf.json'
  if os.path.isfile(conf_path):
    create_vm_conf_dict = json.load(open(conf_path, 'r'))
  else:
    images_dict = get_images()
    for image_dict in images_dict['images']:
      # デフォルトで用意されているイメージは除く
      if "vmi-" in image_dict['name']: continue

      print("イメージID: " + image_dict['id'])
      print("イメージ名: " + image_dict['name'])
      print("----------")

    image_id = input('使用したいイメージID: ')

    flavors_detail_dict = get_flavors_detail()
    for flavor_dict in flavors_detail_dict['flavors']:
      # 旧プランはスキップ
      if flavor_dict['disk'] == 20: continue
      if flavor_dict['disk'] == 50: continue
      print("プランID: " + flavor_dict['id'])
      print("メモリ: " + str(flavor_dict['ram']) + "MB, CPU: " + str(flavor_dict['vcpus']) + "コア, ディスク容量: " +  str(flavor_dict['disk']) + "GB")
      print("----------")

    plan_id = input('使用したいプランID: ')

    security_groups_dict = network.get_secgroups_list()

    with open('json/security_groups.json', 'w') as f:
      json.dump(security_groups_dict, f, indent=4)

    print('セキュリティグループ一覧')
    print("----------")
    for security_group_dict in security_groups_dict['security_groups']:
      print(security_group_dict['name'])
    print("----------")

    secgroup_name = input('使用したいセキュリティグループ名: ')

    create_vm_conf_dict = {
      'image_id':image_id,
      'plan_id':plan_id,
      'secgroup_name':secgroup_name
    }

    with open(conf_path, 'w') as f:
      json.dump(create_vm_conf_dict, f, indent=4)

  server_dict = {
    "server": {
        "imageRef": create_vm_conf_dict['image_id'],
        "flavorRef": create_vm_conf_dict['plan_id'],
        "security_groups": [
            {
                "name": create_vm_conf_dict['secgroup_name']
            }
        ]
    }
  }

  url = endpoint_dict['ComputeService'] + '/servers'

  created_server_dict = requests.post(url, data = json.dumps(server_dict), headers=headers).json()
  with open('json/created_server.json', 'w') as f:
    json.dump(created_server_dict, f, indent=4)

  # ステータスがACTIVE(起動中)になるまでポーリング(最大5分)
  print('構築中', end='', flush=True)
  for index in range(30):
    vms_detail_dict = get_vms_detail_specified()
    if vms_detail_dict['server']['status'] == 'ACTIVE':
      break
    print('.', end='', flush=True)
    time.sleep(10)
  print('起動しました', end='')

def stop_cleanly_vm(args):
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  url = endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id'] +'/action'
  res = requests.post(url, data = '{"os-stop": null}', headers=headers)
  if res.status_code != 202: 
    print(res.reason)
    return

  # ステータスがSHUTOFF(停止)になるまでポーリング(最大5分)
  print('停止処理中', end='', flush=True)
  for index in range(30):
    vms_detail_dict = get_vms_detail_specified()
    if vms_detail_dict['server']['status'] == 'SHUTOFF':
      break
    print('.', end='', flush=True)
    time.sleep(10)
  print('停止しました', end='')

def create_image(args):
  if args.name is not None:
    image_name = args.name
  else:
    image_name = input('イメージ名: ')
  created_server_dict = json.load(open('json/created_server.json', 'r'))
  url = endpoint_dict['ComputeService'] + '/servers/' + created_server_dict['server']['id'] +'/action'

  res = requests.post(url, data = '{"createImage": {"name": "' + image_name +'"}}', headers=headers)
  if res.status_code != 202: 
    print(res.reason)
    return

  image_id = get_image_id(image_name)
  # ステータスがACTIVE(利用可能)になるまでポーリング(最大5分)
  print('保存中', end='', flush=True)
  for index in range(30):
    image_detail_dict = get_images_detail_specified(image_id)
    if image_detail_dict['image']['status'] == 'ACTIVE':
      break
    print('.', end='', flush=True)
    time.sleep(10)
  print('イメージが利用可能になりました')

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
    parser_create_image.add_argument('-name', type=str, metavar='Temporary', help='イメージ名')
    parser_delete_vm.set_defaults(handler=delete_vm)
    
    args = parser.parse_args()

    if hasattr(args, 'handler'):
      args.handler(args)
    else:
      parser.print_help()