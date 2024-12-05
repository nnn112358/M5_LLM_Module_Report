

LLM Module ファームウェアアップグレードガイド
https://docs.m5stack.com/ja/guide/llm/llm/image


Airpocketさんの言う通り、AXDLは
①axpファイルを読み込む
②ダウンロードボタン▶を押す（■になる）
③ダウンロードボタンを押しながらModuleLLMを接続する
https://x.com/mongonta555/status/1858107431412466097


AXDL の Settings ですが、このダイアログ画面を出した状態だと、Port のリストが更新されない仕様のようで。
LLM Module の電源ボタンを押しながら結線した直後に、AXDL の Settings ボタンをクリックすると、
ダイアログ画面の Port のリストに COM が見えてくると思います。
https://x.com/hirotakaster/status/1856666870717579607


1. AXDLを立ち上げて、書き込みイメージを読み込み
2. LLM moduleの電源ボタンを押しながらPC側のUSBと結線
3. PC側 AXDL の歯車アイコン(左から2番目)をそっこークリックして、LLM moduleの書き込みポートを設定
4. また 2 の手順でDLモードの瞬間にAXDL書き込み実行


