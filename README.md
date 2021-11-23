# ConoHaAssistant

GMOのConoHa APIを用いた操作を簡単なコマンドで実現します。   
使用していない時間帯は自動的にサーバーを削除し、利用料金を節約することを目的に開発しました。  

## API情報の登録

https://manage.conoha.jp/API/ に表示されるAPI情報を登録します。  
登録した情報は `json/auth.json` `json/endpoint.json` に保存されます。  
セキュリティの観点から、保存されたファイルの管理にはご注意ください。

```
$ git clone https://github.com/Bioliss/ConoHaAssistant.git
$ cd ConoHaAssistant/src
$ python3 setup.py
```

## ドキュメント

* [Identity API 関連](doc/identity.md)
* [Compute API 関連](doc/compute.md)
* [Network API 関連](doc/network.md)