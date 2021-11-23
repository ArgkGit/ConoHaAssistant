# Compute API 関連

Compute API を用いた操作は`compute.py`にて実現します。  
APIを使用するためには、[identityモジュール](identity.md)の`post_tokens`で、トークンを取得しておく必要があります。

## `create_vm`

> https://www.conoha.jp/docs/compute-create_vm.php  

サーバーを追加するコマンドです。  

* 指定するイメージについて
  * ユーザーが保存したイメージを利用するため、 ConoHaコントロールパネルよりイメージを保存しておく必要があります。
  * `create_vm`コマンドで作成したサーバの場合は、`create_image`コマンドでもイメージを保存可能です。
* 指定するセキュリティグループについて
  * 指定できるセキュリティーグループは1種類です。
  * 各セキュリティーグループの情報は、セキュリティグループ一覧が表示された後に出力される`json/security_groups.json`を確認してください。
  * [networkモジュール](network.md)の`create_secgroup`で、セキュリティーグループを作成できます。

`create_vm`コマンド実行中に入力した値の情報は `json/create_vm_conf.json` に保存され、次回実行時に使用されます。  
追加されたサーバーの情報は `json/created_server.json` に保存され、他のコマンドで使用されます。  
`json/created_server.json` はサーバー追加の度に上書きされるため、コマンド操作できるのは最後に追加されたサーバーのみです。  

```
$ python3 compute.py create_vm
```

## `stop_cleanly_vm`


> https://www.conoha.jp/docs/compute-stop_cleanly_vm.php  

`create_vm`コマンドで追加したサーバーをシャットダウンするコマンドです。
```
$ python3 compute.py stop_cleanly_vm
```
  
## `create_image`

> https://www.conoha.jp/docs/compute-create_image.php  
> https://support.conoha.jp/v/saveimages/    

`create_vm`コマンドで追加したサーバーのイメージを保存するコマンドです。  
イメージを保存する前に、`stop_cleanly_vm`コマンドを実行してください。  
保存したイメージが90日間利用されなかった場合はConoHaの仕様により削除されます。(有料オプション契約時は除く)  

```
$ python3 compute.py create_image
```

事前にイメージ名を`-name`オプションで指定することもできます。  
```
$ python3 compute.py create_image -name YuiAragaki
```

## `delete_vm`

> https://www.conoha.jp/docs/compute-delete_vm.php

`create_vm`コマンドで追加したサーバーを削除するコマンドです。

```
python compute.py delete_vm
```
