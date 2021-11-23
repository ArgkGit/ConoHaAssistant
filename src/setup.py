#!/usr/bin/env python3

import json
import os

if __name__ == '__main__':
  print('https://manage.conoha.jp/API/ に表示されるAPI情報を入力してください。')
  tenantId = input('テナント情報/テナントID : ')
  AccountService = input('エンドポイント/Account Service : ')
  ComputeService = input('エンドポイント/Compute Service : ')
  VolumeService = input('エンドポイント/Volume Service : ')
  DatabaseService = input('エンドポイント/Database Service : ')
  ImageService  = input('エンドポイント/Image Service  : ')
  DNSService = input('エンドポイント/DNS Service : ')
  ObjectStorageService = input('エンドポイント/Object Storage Service : ')
  MailService = input('エンドポイント/Mail Service : ')
  IdentityService = input('エンドポイント/Identity Service : ')
  NetworkService = input('エンドポイント/Network Service : ')
  username = input('APIユーザー/ユーザー名 : ')
  password = input('APIユーザー/パスワード : ')

  auth_dict = {
    "auth": {
      "passwordCredentials": {
          "username": username,
          "password": password
      },
      "tenantId": tenantId
    }
  }
  endpoint_dict = {
    'AccountService':AccountService,
    'ComputeService':ComputeService,
    'VolumeService':VolumeService,
    'DatabaseService':DatabaseService,
    'ImageService':ImageService,
    'DNSService':DNSService,
    'ObjectStorageService':ObjectStorageService,
    'MailService':MailService,
    'IdentityService':IdentityService,
    'NetworkService':NetworkService
  }

  os.makedirs(json, exist_ok=True)
  with open('json/auth.json', 'w') as f:
    json.dump(auth_dict, f, indent=4)
  with open('json/endpoint.json', 'w') as f:
    json.dump(endpoint_dict, f, indent=4)
