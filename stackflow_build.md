
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
