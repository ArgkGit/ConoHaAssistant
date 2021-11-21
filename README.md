# ConoHaAssistant

GMOのConoHa APIを用いた操作をコマンドで実現します。   
使用していない時間帯は自動的にサーバーを削除し、利用料金を節約することを目的に開発しました。  
サーバー追加の際は https://manage.conoha.jp/ServiceImage/ のイメージリストに表示されるイメージを利用します。

## 初期設定

https://manage.conoha.jp/API/ に表示されるAPI情報を登録します。  
登録した情報は `json/auth.json` `json/endpoint.json` に保存されます。  
セキュリティの観点から、保存されたファイルの管理にはご注意ください。

```
$ git clone https://github.com/Bioliss/ConoHaAssistant.git
$ cd ConoHaAssistant/src
$ python3 setup.py
```

## トークン取得

> 参考  
> https://support.conoha.jp/v/apitokens/  
> https://www.conoha.jp/docs/identity-post_tokens.php  

APIを使用するためにトークンを取得します。(24時間の有効期限あり)  
取得した情報は `json/tokens.json` に保存されます。  

```
$ python3 identitiy.py post_tokens
```

## サーバー追加

> 参考  
> https://www.conoha.jp/docs/compute-create_vm.php  

`post_tokens`コマンド実行中に指定した値の情報は `json/create_vm_conf.json` に保存され、次回実行時に使用されます。  
追加されたサーバーの情報は `json/created_server.json` に保存され、以降のコマンドで使用されます。  
`json/created_server.json` はサーバー追加の度に上書きされるため、コマンド操作できるのは最後に追加されたサーバーのみです。  

```
$ python3 compute.py create_vm
```

## サーバーシャットダウン

> 参考  
> https://www.conoha.jp/docs/compute-stop_cleanly_vm.php  

`create_vm`コマンドで追加したサーバーをシャットダウンします。
```
$ python3 compute.py stop_cleanly_vm
```
  
## イメージ保存

> 参考  
> https://www.conoha.jp/docs/compute-create_image.php  
> https://support.conoha.jp/v/saveimages/    

`create_vm`コマンドで追加したサーバーのイメージを保存します。  
イメージを保存するにはサーバーをシャットダウンする必要があります。  
保存したイメージが90日間利用されなかった場合はConoHaの仕様により削除されます。(有料オプション契約時は除く)  

```
$ python3 compute.py create_image
```

事前にイメージ名を`-name`オプションでで指定することもできます。  
```
$ python3 compute.py create_image -name YuiAragaki
```

## サーバー削除

> 参考  
> https://www.conoha.jp/docs/compute-delete_vm.php

`create_vm`コマンドで追加したサーバーを削除します。

```
python compute.py delete_vm
```
