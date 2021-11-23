# Identity API 関連

Identity API を用いた操作は [identity.py](../../src/identity.py) にて実現します。

## `post_tokens`

> https://support.conoha.jp/v/apitokens/  
> https://www.conoha.jp/docs/identity-post_tokens.php  

トークンを取得するコマンドです。(24時間の有効期限あり)  
取得した情報は `json/tokens.json` に保存されます。  

```
$ python3 identitiy.py post_tokens
```
