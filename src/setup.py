#!/usr/bin/env python3

import requests
import json

if __name__ == '__main__':
  print('https://manage.conoha.jp/API/ に表示されるAPI情報を入力してください。')
  tenantId = input('テナント情報/テナントID : ')
  ComputeService = input('エンドポイント/Compute Service : ')
  IdentityService = input('エンドポイント/Identity Service : ')
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
  endpoint_dict = {'ComputeService':ComputeService, 'IdentityService':IdentityService}

  with open('json/auth.json', 'w') as f:
    json.dump(auth_dict, f, indent=4)
  with open('json/endpoint.json', 'w') as f:
    json.dump(endpoint_dict, f, indent=4)
