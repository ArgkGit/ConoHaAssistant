# Network API 関連

Network API を用いた操作は [network.py](../src/network.py) にて実現します。  
APIを使用するためには、[identityモジュール](identity.md)の`post_tokens`で、トークンを取得しておく必要があります。

## `create_secgroup`

> https://www.conoha.jp/docs/neutron-create_secgroup.php

セキュリティグループを作成するコマンドです。  
作成したセキュリティグループには、`create_rule_on_secgroup`コマンドでルールを追加できます。  

* 初期値について
  * アウトバウンド接続許可ポートは初期値で「全て許可」が設定されます。
  * インバウンド接続許可ポートは未設定 = すべてのポートが禁止の状態です。


作成したセキュリティグループの情報は `json/created_secgroup.json` に保存され、他のコマンドで使用されます。  
`json/created_secgroup.json` はセキュリティグループ作成の度に上書きされるため、コマンド操作できるのは最後に作成したセキュリティグループのみです。  

```
python3 network.py create_secgroup
```

## `delete_secgroup`

> https://www.conoha.jp/docs/neutron-delete_secgroup.php

`create_secgroup`コマンドで作成したセキュリティグループを削除するコマンドです。

```
python3 network.py delete_secgroup
```

## `create_rule_on_secgroup`

> https://www.conoha.jp/docs/neutron-create_rule_on_secgroup.php

`create_secgroup`コマンドで作成したセキュリティグループにルールを追加するコマンドです。  
インバウンド接続許可ポートを指定することができます。

```
python3 network.py create_rule_on_secgroup
```

## `delete_rule_on_secgroup`

> https://www.conoha.jp/docs/neutron-delete_rule_on_secgroup.php

`create_rule_on_secgroup`コマンドで追加したルールを削除するコマンドです。