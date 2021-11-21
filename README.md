# ConoHaAssistant

## リクエスト実施時に必要な情報

* https://www.conoha.jp/login/ からログイン > `API`

## トークン取得

> 参考 : https://support.conoha.jp/v/apitokens/


* リクエスト
  ```
   # curl -i -X POST -H "Accept: application/json" \
  -d '{ "auth": { "passwordCredentials": { "username": "APIユーザーのユーザー名", "password": "APIユーザーのパスワード" }, "tenantId": "テナント情報のテナントID" } }' \
  ${Identity ServiceのURL}/tokens > tokens.json
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
  ${Compute ServiceのURL}/flavors/detail > flavors_detail.json
  ```
  
* レスポンス
  ```json
  {
      "flavors": [
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
          }
      ]
  }
  ```
  `name`の末尾に`d30`または`d100`とついているプランが現プラン。(2021/11/21時点)

## サーバー追加

> 参考 : https://www.conoha.jp/docs/compute-create_vm.php

* リクエスト
  ```
  curl -i -X POST \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -d '{"server": {"adminPass": "rootパスワード","imageRef": "${イメージID}","flavorRef": "${VPSのプランに紐づくID"}' \
  ${Compute ServiceのURL}/servers
  ```

## サーバID取得

> 参考 : https://www.conoha.jp/docs/compute-get_vms_list.php

* リクエスト
  ```
  curl -i -X GET \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  ${Compute ServiceのURL}/servers > servers.json
  ```

* レスポンス
  ```json
  {
      "servers": [
          {
              "id": "${サーバID}",
              "links": [
                  {
                      "href": "https://compute.tyo1.conoha.io/v2/${テナントID}/servers/${サーバID}",
                      "rel": "self"
                  },
                  {
                      "href": "https://compute.tyo1.conoha.io/${テナントID}/servers/${サーバID}",
                      "rel": "bookmark"
                  }
              ],
              "name": "${IPアドレス(ハイフン区切り)}"
          }
      ]
  }
  ```

## サーバシャットダウン

> 参考 : https://www.conoha.jp/docs/compute-stop_cleanly_vm.php

* リクエスト
  ```
  curl -i -X POST \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -d '{"os-stop": null}' \
  ${Compute ServiceのURL}/servers/${サーバID}/action
  ```
  
## イメージ保存

> 参考 : https://www.conoha.jp/docs/compute-create_image.php

* リクエスト
```
curl -i -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
-d '{"createImage": {"name": "${イメージ名}"}}' \
${Compute ServiceのURL}/servers/${サーバID}/action
```

## イメージIDの取得

> 参考 : https://www.conoha.jp/docs/compute-get_images_list.php

* リクエスト
  ```
  curl -i -X GET \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  ${Compute ServiceのURL}/images
  ```

* レスポンス
  ```json
  {
      "images": [
          {
              "id": "${イメージID}",
              "links": [
              ],
              "name": "Temporary"
          },
          {
              "id": "${イメージID}",
              "links": [
              ],
              "name": "vmi-lamp-latest-ubuntu-20.04-amd64-100gb"
          },
          {
              "id": "${イメージID}",
              "links": [
              ],
              "name": "vmi-lamp-latest-ubuntu-20.04-amd64"
          },
          {
              "id": "${イメージID}",
              "links": [
              ],
              "name": "vmi-lamp-latest-ubuntu-20.04-amd64-30gb"
          },
          {
              "id": "${イメージID}",
              "links": [
              ],
              "name": "vmi-lamp-latest-ubuntu-20.04-amd64-20gb"
          }
      ]
  }
  ```

## イメージ保存のステータス取得

> 参考 : https://www.conoha.jp/docs/compute-get_images_detail_specified.php

* リクエスト
  ```
  curl -i -X GET \
  -H "Accept: application/json" \
  -H "X-Auth-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  ${Compute ServiceのURL}/images/${イメージID} > image_detail.json
  ```
  
* レスポンス
```json
  {
      "image": {
          "status": "ACTIVE",
          "updated": "2021-11-21T00:19:29Z",
          "links": [
          ],
          "id": "${イメージID}",
          "OS-EXT-IMG-SIZE:size": 20026818560,
          "name": "Temporary",
          "created": "2021-11-21T00:16:15Z",
          "minDisk": 30,
          "server": {
              "id": "${サーバID}",
              "links": [
              ]
          },
          "progress": 100,
          "minRam": 0,
          "metadata": {
              "instance_uuid": "${サーバID}",
              "dst": "Ubuntu-20.04-64bit",
              "hw_qemu_guest_agent": "yes",
              "display_order": "165",
              "os_type": "lin"
          }
      }
  }
```
`status`が`ACTIVE`であれば利用可能。
