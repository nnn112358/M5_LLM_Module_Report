
## 目的
M5Stack LLM ModuleのLLMサーバ StackFlowをビルドする手順

ARM64向けのクロスコンパイラをダウンロード・インストールし、Pythonの開発環境を整えた上で、M5StackのLLMフレームワークのソースコードをクローンして必要なサブモジュールを初期化し、最後にSConsを使用して並列ビルドを実行する一連のセットアップコマンドです。

```

wget https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/linux/llm/gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu.tar.gz
sudo tar zxvf gcc-arm-10.3-2021.07-x86_64-aarch64-none-linux-gnu.tar.gz -C /opt

sudo apt install python3 python3-pip libffi-dev
pip3 install parse scons requests 

git clone https://github.com/m5stack/StackFlow.git
cd StackFlow
git submodule update --init
cd projects/llm_framework
scons distclean
scons -j22

```

## json
https://x.com/washishi/status/1866229894763708587

https://drive.google.com/file/d/1APQY5jCzXhmBu_PnOhK2sVUoT-fkIPn9/view?usp=drive_link
telnetへ流し込んでるので
apt install telnet で
telnetクライアントを追加インストールしてください

これを /usr/local/m5stackに置いて
http://startup-script.sh の最後に
(sleep 5;sh /usr/local/m5stack/talk_ip.sh) &
等を追加して動かしてください

```
#!/bin/bash
cd `dirname $0`
WIFI_IP=`ip address  show dev wlan0 | grep "inet "|awk -F/ '{print $1}'|sed 's/ *inet //'`
if [ _$WIFI_IP != "_" ]
  then
( echo open localhost 10001;
  sleep 1;
  echo '{"request_id":"1","work_id":"audio","action":"setup","object":"audio.setup","data":{"capcard":0,"capdevice":0,"capVolume":0.5,"playcard": 0,"playdevice": 1,"playVolume":0.5}}';
  sleep 1;
  echo '{"request_id":"2","work_id":"tts","action":"setup","object":"tts.setup","data":{"model":"single_speaker_english_fast","response_format":"tts.base64.wav","input":"tts.utf-8.stream","enoutput":true, "enkws": true}}';
  sleep 1;
  echo '{"request_id":"3","work_id":"tts.1001","action":"inference","object":"tts.utf-8", "data":"Wi-Fi IP Address is '$WIFI_IP'"}'
  sleep 10;
  echo '{"request_id":"4","work_id":"sys","action":"reset"}';
) | tee | telnet > talk_ip.log 2>&1
fi

talk_ip.sh
talk_ip.sh を表示しています。
```
