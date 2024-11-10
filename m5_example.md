## M5 LLM Moduleのexampleについて

arduinoのサンプルが通信しているLLM Moduleのバイナリを起動しているスクリプトの場所について。
Linuxの自動時にサービスとして起動しています。

## サービスの一覧
サービスの一覧から起動していることを確認できます。

```
root@m5stack-LLM:~# systemctl list-units --type=service --state=running
  UNIT                        LOAD   ACTIVE SUB     DESCRIPTION                >
~~~~~~
  llm-asr.service             loaded active running llm-asr Service
  llm-audio.service           loaded active running llm-audio Service
  llm-kws.service             loaded active running llm-kws Service
  llm-llm.service             loaded active running llm-llm Service
  llm-sys.service             loaded active running llm-sys Service
  llm-tts.service             loaded active running llm-tts Service
~~~~~~
```

## サービスの設定ファイル
サービスの設定ファイルは/usr/lib/systemd/system/にあります。

```

root@m5stack-LLM:~# cat /usr/lib/systemd/system/llm-asr.service
[Unit]
Description=llm-asr Service
After=llm-sys.service
Requires=llm-sys.service

[Service]
ExecStart=/opt/m5stack/bin/llm_asr
WorkingDirectory=/opt/m5stack
Restart=always
RestartSec=1
StartLimitInterval=0

[Install]
WantedBy=multi-user.target

root@m5stack-LLM:~# cat /usr/lib/systemd/system/llm-kws.service
[Unit]
Description=llm-kws Service
After=llm-sys.service
Requires=llm-sys.service

[Service]
ExecStart=/opt/m5stack/bin/llm_kws
WorkingDirectory=/opt/m5stack
Restart=always
RestartSec=1
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
```

## バイナリの場所

/opt/m5stack/bin以下にバイナリが置いてあります。

```
root@m5stack-LLM:~# ls /opt/m5stack/bin/
llm_asr  llm_audio  llm_kws  llm_llm  llm_sys  llm_tts
```
