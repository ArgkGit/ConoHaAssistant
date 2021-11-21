# ConoHaAssistant

ConoHa APIを用いたサーバの作成や削除などをコマンド操作で実現します。   
https://manage.conoha.jp/ServiceImage/ のイメージリストに表示されるイメージを使用します。

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

APIを使用するためにトークンを取得します。  
取得した情報は `json/tokens.json` に保存されます。  
トークンには24時間の有効期限があります。

```
$ python3 identitiy.py post_tokens
```

## サーバー作成

> 参考  
> https://www.conoha.jp/docs/compute-create_vm.php  

作成されたサーバの情報は `json/created_server.json` に保存されます。  
作成される度に上書きされるため、コマンドライン操作できるのは最後に作成されたサーバのみです。  

```
$ python3 compute.py create_vm
```

## サーバシャットダウン

> 参考  
> https://www.conoha.jp/docs/compute-stop_cleanly_vm.php  

`create_vm`コマンドで作成したサーバをシャットダウンします。
```
$ python3 compute.py stop_cleanly_vm
```
  
## イメージ保存

> 参考  
> https://www.conoha.jp/docs/compute-create_image.php  
> https://support.conoha.jp/v/saveimages/    

`create_vm`コマンドで作成したサーバのイメージを保存します。  
イメージを保存するにはサーバをシャットダウンする必要があります。  
保存したイメージが90日間利用されなかった場合は削除対象となります。(有料オプション契約時は除く)  

```
$ python3 compute.py create_image
```

## サーバ削除

> 参考  
> https://www.conoha.jp/docs/compute-delete_vm.php

`create_vm`コマンドで作成したサーバを削除します。

```
python compute.py delete_vm
```
