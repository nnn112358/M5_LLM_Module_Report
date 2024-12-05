

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




```
root@m5stack-LLM:~# df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        7.8G  3.2G  4.6G  42% /
tmpfs            983M     0  983M   0% /dev/shm
tmpfs            394M  848K  393M   1% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
tmpfs            983M     0  983M   0% /tmp
/dev/mmcblk0p19   20G  1.8G   18G  10% /opt
/dev/mmcblk0p18  992M  8.0M  968M   1% /soc
/dev/mmcblk0p17  928K  236K  592K  29% /param
tmpfs            197M     0  197M   0% /run/user/0
root@m5stack-LLM:~# free
               total        used        free      shared  buff/cache   available
Mem:         2012408      125116     1630584         848      256708     1816504
Swap:              0           0           0

```
