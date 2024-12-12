

## 前提

Module-LLMにモデルを導入するには、モデルをINT8に量子化してモデルサイズを縮小し、実行速度を向上させる必要があります。
pulsar2というツールを使用してモデルを量子化します。手順は以下の通りです：
1. 浮動小数点モデルを準備します。
2. モデル量子化とフォーマット変換ツールを使用して、Module-LLMがサポートするフォーマットに変換します。ここではAXeraの公式ツールであるpulsar2を使用します。
3. Module-LLM上でモデルを実行します。

一、浮動小数点モデルの準備#
Pytorchでモデルを学習し、モデルをonnx形式で保存しておきます。
AX630Cがサポートする演算子のみを使用できることに注意が必要です。サポートされている演算子のリストをご確認ください。
一部のネットワークでは、後処理を分離してCPUで処理する必要がある場合があります。


1.1. 例示#
例として、PyTorch Hubからmobilenetv2を使用してみましょう：

```python
import torch
model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)
model.eval()
```

`onnx`形式へのエクスポート：

```python
x = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, x, "mobilenetv2.onnx", export_params = True, verbose=True, opset_version=11)
```

一部のモデルでは`onnxsim`を使用してネットワーク構造を簡略化できます（このモデルは実際には必要ありません）：

```none
pip install onnx-simplifier
python -m onnxsim mobilenetv2.onnx mobilenetv2-sim.onnx
```


以下が日本語訳です：

二、モデル量子化とフォーマット変換#
2.1. `docker`のインストール#
インストールチュートリアル
インストール後の確認

```none
docker --version
```

`Linux`では、現在のユーザーを`docker`グループに追加することで、`sudo`を使用せずに`docker`コマンドを実行できるようになります。以下のコマンドで追加できます：

```shell
sudo gpasswd -a $USER docker
newgrp docker
```




以下が日本語訳です：

2.2. 変換ツールのダウンロード#
変換ツールはdockerイメージとして提供されており、ダウンロード後にdockerでイメージを読み込むことができます。

ダウンロードサイト | 概要 | 使用方法
---|---|---
dockerhub | コマンドを実行するだけでオンラインダウンロード | `docker pull sipeed/pulsar`
dockerhub中国国内ミラー | 中国国内でのダウンロード高速化 | 1. `/etc/docker/daemon.json`を編集し、`"registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"],`を追加（阿里雲などの他のミラーも使用可） 2. その後 `docker pull sipeed/pulsar` でイメージを取得

イメージの取得後、`docker images`コマンドで`sipeed/pulsar:latest`イメージが表示されます。

注意：ここでイメージ名は`sipeed/pulsar`ですが、ドキュメントの一部で`axera/neuwizard`と表記されている場合があります。これらは同等で、名前が異なるだけです。

次にコンテナを作成します：

```shell
docker run -it --net host --rm --shm-size 32g -v $PWD:/data sipeed/pulsar
```

* `--shm-size`の共有メモリサイズは、お使いのコンピュータのメモリサイズに応じて設定してください。
* `--rm`を使用しないとコンテナが保持されます。`-name xxx`でコンテナに名前を付けることを推奨します。次回は`docker start xxx && docker attach xxx`でコンテナに入れます。
* `-v ホストマシンのパス:/data`は、ホストマシンのディレクトリをコンテナの`/data`ディレクトリにマウントし、コンテナ内からホストマシンのファイルを直接操作できるようにします。

コンテナ作成後、自動的にコンテナ内に入ります。`pulsar -h`コマンドで関連コマンドを確認できます。

2.3. モデルの量子化と変換#
pulsarのドキュメントで説明されている変換コマンドと設定ファイルの方法に従って、モデルの量子化とフォーマット変換を行います。
注意：`AXera-Pi`は仮想NPUの概念を使用して演算能力を分割し、全演算能力をNPUに割り当てるか、NPUとAI-ISPで半分ずつ分割するかを選択できます。


以下が日本語訳です：

2.3.1. 例示#
引き続き`mobilenetv2`を例として：
* `pulsar`のドキュメントに従って、設定ファイル`config_mobilenetv2.prototxt`を準備します（具体的な形式の説明は設定ファイルの詳細説明を参照）。内容は以下の通り：

config_mobilenetv2.prototxt
```protobuf

```

次に、`docker`コンテナ内で実行します（注意：ファイルは前述の`docker run`の`-v`パラメータで指定したホストマシンのディレクトリがコンテナにマウントされているので、そのホストマシンのディレクトリに直接コピーすれば良いです）：

```none
pulsar build --input mobilenetv2.onnx --output mobilenetv2.joint --config config_mobilenetv2.prototxt --output_config out_config_mobilenet_v2.prototxt
```

しばらく待つと、変換されたモデル`mobilenetv2.joint`が得られます。

2.4. dockerでGPUを使用したモデルの量子化とフォーマット変換#
デフォルトではdockerはGPUドライバーを使用できませんが、必要な場合の設定方法は簡単です：
* ホストマシンに通常通りGPUドライバーをインストールします。例えば`ubuntu`ではパッケージマネージャーから直接インストールできます。
* nvidia-dockerの説明に従ってインストールし、使用可能か次のようにテストします：

```none
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

これにより`nvidia-smi`コマンドが実行され、dockerにマッピングされたGPU情報が表示されます。
* GPUを使用するコンテナを作成する際に、`--gpus all`パラメータを追加してすべてのGPUドライバーをコンテナ内にマッピングします。特定のGPU番号を指定する場合は`--gpus '"device=2,3"'`のように指定できます。例：

```none
docker run -it --net host --rm --gpus all --shm-size 32g -v $PWD:/data sipeed/pulsar
```

注意：現在のバージョン（0.6.1.20）の`pulsar build`は、sm_37 sm_50 sm_60 sm_70 sm_75アーキテクチャのGPUのみをサポートしています。30/40シリーズのGPUは現在サポートされていません。

以下が日本語訳です：

三、AXera-Pi上でのモデルテスト実行#
ドキュメントに従ってモデルを変換した後、`scp`または`adb`を使用してモデルを`AXera-Pi`に転送し、ドキュメントに記載されているモデルテスト実行コマンドで実行できます。

3.1. 例示#
引き続き`mobilenetv2`を例として：テスト画像を`cat.jpg`として保存します：
* まずコンピュータ上で`onnx`との結果を比較します：

```none
pulsar run mobilenetv2.onnx mobilenetv2.joint --input cat.jpg --config out_config_mobilenet_v2.prototxt --output_gt gt
```

コサイン距離が得られ、この場合は`0.9862`です。これは`joint`モデルと`onnx`モデルの出力結果の類似度が`98.62%`であることを示し、許容範囲内です。値が小さすぎる場合は、量子化過程でエラーが発生したことを示すため、設定ミスや量子化入力データの問題、モデル設計の問題を検討する必要があります。

```log
Layer: 536  2-norm RE: 17.03%  cosine-sim: 0.9862
```

* モデルを`AXera-Pi`にコピーして直接実行します（`scp`コマンドで`joint`形式のモデルファイルを開発ボードにコピー）：
ボード上でモデルを実行：

```none
time run_joint mobilenetv2.joint --repeat 100 --warmup 10
```

モデルの実行時間は`2.1ms`で、仮想NPUを有効にしていない場合です。仮想NPUを有効にすると時間は倍の`4ms`になります。また、`overhead 250.42 ms`はその他の処理時間（モデルのロードやメモリ割り当てなど）を示します。

```none
Run task took 2143 us (99 rounds for average)
        Run NEU took an average of 2108 us (overhead 9 us)
```

入力をテストする場合は、まず画像をバイナリコンテンツに変換する必要があります（`HWC + RGB`配列）。`--data`でバイナリファイルを指定します。

```none
run_joint mobilenetv2.joint --data cat.bin --bin-out-dir ./
```

すると、ディレクトリに`bin`ファイルが生成され、サイズは`4000`バイト（`1000`個の`float32`）です。`python`で読み込んで最大値を見つけることができます：

```python
out = np.fromfile("536.bin", dtype=np.float32)
print(out.argmax(), out.max())
```

結果は`282 8.638927`となり、labelsで索引`282`（`283`行目）を見ると`tiger cat`です。これはコンピュータで直接浮動小数点モデルを実行した結果`282 9.110947`とも一致しています。値にわずかな違いはありますが、許容範囲内です。
注意：ここでは`softmax`計算を行っていないため、`out.max()`は確率値ではありません。

[次のセクションに続きます...]

人: 残りのセクションの翻訳をお願いします。




六、QAT量子化とその他の最適化方法#
QAT（Quantization aware training：量子化考慮型学習）は、学習済みモデルに対して量子化を行うPTQとは異なり、学習時から量子化推論をシミュレートすることで、量子化誤差を低減します。学習後量子化のPTQと比較して、より高い精度が得られますが、プロセスはより複雑になるため、初めから使用することは推奨されません。
詳細についてはsuperpulsarをご覧ください。ドキュメントは継続的に更新されます。もしこの分野に詳しい方は、右上の「このページを編集」をクリックして、ここに説明を追加していただくことも歓迎します。
