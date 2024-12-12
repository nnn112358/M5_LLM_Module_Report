

背景

知乎での投稿を定期的にフォローしている方々はご存知の通り、私たちの記事はCNNモデルやビジョン大規模モデルの適用事例の共有が中心でした。しかし、今年はマルチモーダル大規模モデルやエンドツーエンド大規模モデルのアプリケーション事例が増加し、技術コミュニティのメンバーから音声大規模モデルのエッジ適用事例の共有を求める声が多く寄せられました。そこで、ASRとTTSに関する2つの記事を執筆することにしました。

この記事を通じて、MeloTTSの基本的な技術特性と、愛心派Pro（AX650N）上での展開方法を理解することができます。音声認識大規模モデルの展開に関わる開発者に新しい視点を提供し、音声認識大規模モデルのエッジ展開の探求を促進することを目指しています。

MeloTTS

MeloTTSは、マサチューセッツ工科大学（MIT）とMyShell.aiが共同開発した高品質な多言語テキスト音声変換（TTS）ライブラリです。

github：MeloTTS: High-quality multi-lingual text-to-speech library by MyShell.ai
Huggingface：https://huggingface.co/myshell-ai

技術特性：

* **多言語サポート**：英語（アメリカ、イギリス、インド、オーストラリア）、スペイン語、フランス語、中国語、日本語、韓国語などの多言語をサポート
* **中英混合サポート**：特に中国語ユーザー向けに、英単語を含む中国語テキストの発音をサポート
* **オープンソースとカスタマイズ可能**：オープンソースプロジェクトとして、自由な使用とコミュニティからの貢献やカスタム開発を奨励し、継続的な改善と革新のための肥沃な土壌を提供
* **高い拡張性**：新しいデータセットやモデル構造の統合が容易

MeloTTSの核心は、シンプルな設計理念と強力なパフォーマンスにあります。エンドツーエンドの学習モードを採用し、深層学習モデルを通じて入力テキストを自然で滑らかな音声に変換します。モデルアーキテクチャは主にTacotron 2とWaveGlow構造を採用しており、Tacotron 2はシーケンスツーシーケンスの音響モデリングフレームワーク、WaveGlowは波形合成ネットワークで、両者の組み合わせにより高品質な音声を生成できます。MeloTTSは特に軽量化と効率性に注力しており、低リソース環境での実行が可能で、モバイルデバイスやIoTデバイスへの展開に適しています。


モデル変換

AIチップ上でAIアルゴリズムモデルを展開した経験のある方なら、モデルをチップのNPUで実行するためには、チップメーカーが提供するNPUツールチェーンを使用する必要があることをご存知でしょう。ここでは、Pulsar2を使用します。

Axera Pulsar2ツールチェーン:
pulsar2-docs.readthedocs.io/zh-cn/latest/index.html

MeloTTSのONNXモデル取得と量子化キャリブレーションデータ取得を容易にするため、オープンソースプロジェクトを提供しています:
GitHub - ml-inory/melotts.axera: MeloTTS demo on Axera
github.com/ml-inory/melotts.axera

ONNXモデルの取得:
```text
conda create -n melotts python=3.9  
conda activate melotts
git clone https://github.com/ml-inory/melotts.axera.git
cd model_convert 
sudo apt install libmecab-dev
pip install unidic-lite fugashi
pip install -r requirements.txt
python convert.py
```

これにより以下が完了します：
* プロジェクトのダウンロード
* Python仮想環境のインストール
* プロジェクト依存関係のインストール
* MeloTTSのONNXモデルのエクスポート

最終的に、encoder、decoderの2つのonnxモデルファイル、量子化データセット、その他必要なファイルが生成されます。

axmodelの取得:
```text
pulsar2 build --input decoder.onnx --config config_decoder_u16.json --output_dir decoder --output_name decoder.axmodel --target_hardware AX650 --npu_mode NPU3 --compiler.check 0
```
* 変換後にdecoder/decoder.axmodelが生成されます

```
/mnt/qtang/melotts.axera/cpp # ./install/melotts -h
undefined short option: -h
usage: ./install/melotts [options] ...
options:
  -e, --encoder        encoder onnx (string [=../models/encoder.onnx])
  -d, --decoder        decoder axmodel (string [=../models/decoder.axmodel])
  -l, --lexicon        lexicon.txt (string [=../models/lexicon.txt])
  -t, --token          tokens.txt (string [=../models/tokens.txt])
      --g              g.bin (string [=../models/g.bin])
  -s, --sentence       input sentence (string [=爱芯元智半导体股份有限公司，致力于打造世界领先的人工智能感知与边缘计算芯片。服务智慧城市、智能驾驶、机器人的海量普惠的应用])
  -w, --wav            wav file (string [=output.wav])
      --speed          speak speed (float [=0.8])
      --sample_rate    sample rate (int [=44100])
  -?, --help           print this message
/mnt/qtang/melotts.axera/cpp # 
/mnt/qtang/melotts.axera/cpp # ./install/melotts
encoder: ../models/encoder.onnx
decoder: ../models/decoder.axmodel
lexicon: ../models/lexicon.txt
token: ../models/tokens.txt
sentence: 爱芯元智半导体股份有限公司，致力于打造世界领先的人工智能感知与边缘计算芯片。服务智慧城市、智能驾驶、机器人的海量普惠的应用
wav: output.wav
speed: 0.800000
sample_rate: 44100
Load encoder take 4658.14 ms
Load decoder take 932.28 ms
Encoder run take 985.42 ms
Decoder run 9 times take 364.13 ms
wav len: 525824
Saved audio to output.wav
/mnt/qtang/melotts.axera/cpp #
```


ボード上での実行例:
* プリコンパイル済みのaxmodel、実行プログラム、テスト音声ファイルはネットワークドライブから入手可能
* 生成される音声ファイルの品質を確保するため、encoderモデルは現在onnxruntimeで実行

実行結果では、音声生成に合計12秒かかり、愛心派Pro上でのMeloTTSモデルの実行時間は1.3秒、RTF（Real-Time Factor）は0.11となっています。**RTFが低いほど**TTSシステムの音声処理速度が速いことを意味し、リアルタイムの応答が必要なアプリケーション（音声アシスタントなど）で特に重要です。

結びに:
エッジでのマルチモーダル大規模モデルのローカル（オフライン）展開の需要が増加するにつれ、TTSモデルのローカル展開の需要も増加すると予想されます。より高品質な音声大規模モデルの展開を継続的に試みていきます。





1. エンコーダーの配置について質問と議論:
   * 質問者: 「8コアA55上でonnxruntimeを実行しているのでしょうか？」
   * 別の人の指摘: 「Transformerの経験から言えば、エンコーダーの方が配置が容易なはずです。視覚やLLMにおいて、デコーダーの方がエンコーダーより複雑です」
   * 著者の回答: 「エンコーダー部分だけが一時的にCPUで実行され、デコーダーはNPU上で実行されています」

2. レイテンシーに関する議論:
   * 質問: 「最初のフレームの遅延はどのくらいですか？」
   * 著者の回答: 
     * 「エンコーダー + 最初のデコーダーの所要時間は約1000msです」
     * 「エンコーダー部分の量子化の微調整がまだできていませんが、デモには影響がないようです」
     * 「エンコーダーモデルは変換できましたが、音声の量子化については初心者で、様々な問題に直面しています」

3. 興味深い指摘:
   * MeloTTSの論文が見つからないという言及
   * 最後の指摘: 「GPTで生成した記事なのではないですか（笑）。遅いと思ったら、meloはbert vits2を実行しているんですね。特別な処理をしないと確かに遅いです」
