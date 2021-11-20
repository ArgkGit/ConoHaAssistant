# ConoHaAssistant

## リクエスト実施時に必要な情報

* https://www.conoha.jp/login/ からログイン > `API`

## トークン取得

> 参考 : https://support.conoha.jp/v/apitokens/


* リクエスト
  ```
   # curl -i -X POST -H "Accept: application/json" \
  -d '{ "auth": { "passwordCredentials": { "username": "APIユーザーのユーザー名", "password": "APIユーザーのパスワード" }, "tenantId": "テナント情報のテナントID" } }' \
  "Identity ServiceのURLの後ろに/tokensを繋げる" > tokens.json
  ```
* レスポンス
  ```json
  {
      "access": {
          "token": {
              "issued_at": "2021-11-20T14:54:41.643491",
              "expires": "2021-11-21T14:54:41Z",
              "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
              "tenant": {
              },
              "audit_ids": [
              ]
          },
          "serviceCatalog": [
          ],
          "user": {
          },
          "metadata": {
          }
      }
  }
  ```
  
## VPSのプラン一覧取得

> 参考 : https://www.conoha.jp/docs/compute-get_flavors_detail.php

* リクエスト
  ```
  curl -i -X GET \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  "Compute ServiceのURLの後ろに/flavors/detailを繋げる" > flavors_detail.json
  ```
  
* レスポンス
  ```json
  {
      "flavors": [
          {
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
              "name": "g-c1m512d30",
              "links": [
              ],
              "ram": 512,
              "OS-FLV-DISABLED:disabled": false,
              "vcpus": 1,
              "swap": "",
              "os-flavor-access:is_public": true,
              "rxtx_factor": 1,
              "OS-FLV-EXT-DATA:ephemeral": 0,
              "disk": 30,
              "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
          },
          {
              "name": "g-512mb",
              "links": [
              ],
              "ram": 512,
              "OS-FLV-DISABLED:disabled": false,
              "vcpus": 1,
              "swap": "",
              "os-flavor-access:is_public": true,
              "rxtx_factor": 1,
              "OS-FLV-EXT-DATA:ephemeral": 0,
              "disk": 20,
              "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          },
          {
          }
      ]
  }
  ```
  `name`の末尾に`d30`または`d100`とついているプランが現プラン。(2021/11/21時点)

TODO: imageRef 設定値の取得方法

## サーバー追加

> 参考 : https://www.conoha.jp/docs/compute-create_vm.php

* リクエスト
  ```
  curl -i -X POST \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -d '{"server": {"adminPass": "rootパスワード","imageRef": "","flavorRef": "VPSのプランに紐づくID"}}' \
  https://compute.tyo1.conoha.io/v2/1864e71d2deb46f6b47526b69c65a45d/servers
  ```
