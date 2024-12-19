


个人精力有限，无法编写出完美的 c++ tokenizer 解析器，
目前 DEMO 采用 HTTP tokenizer 代理的方式，远程或板子本地启用一个 tokenizer 解析服务器实现

1、python internvl2_tokenizer.py --host xxx.xxx.xxx.xxx --port 12345
其中 --host xxx.xxx.xxx.xxx 设置 tokenizer 解析服务器的 IP 地址，
确保 AX630C 能正常访问该地址。可以在具备 python 环境的 AX630C 本地运行
2、修改 run_internvl2_ax630c.sh 中 --filename_tokenizer_model 的 IP 信息和步骤1中的一致
3、运行 run_internvl2_ax630c.sh 即可

個人の力には限りがあるため、完璧なC++トークナイザ解析器を作成することはできません。
現在のデモでは、HTTPトークナイザプロキシ方式を使用しています。
これにより、リモートまたはボード上でトークナイザ解析サーバーを有効にすることで実現しています。
手順:
python internvl2_tokenizer.py --host xxx.xxx.xxx.xxx --port 12345

1、--host xxx.xxx.xxx.xxx でトークナイザ解析サーバーのIPアドレスを設定します。
AX630Cがこのアドレスに正常にアクセスできることを確認してください。
2、Python環境が整っているAX630Cのローカルでこのスクリプトを実行することも可能です。
run_internvl2_ax630c.sh 内の --filename_tokenizer_model のIP情報を手順1で指定したIPと一致するように変更します。
3、run_internvl2_ax630c.sh を実行します。


