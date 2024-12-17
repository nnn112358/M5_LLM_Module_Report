


背景

InternVL2（中国語名：書生·万象）は上海人工知能研究所のOpenGVLabが発表したマルチモーダル大規模モデルです。このモデルは、マルチ分野質問応答（MMMU）などのタスクで優れた性能を示し、多様なモーダルデータを処理する能力を備えています。

本稿では、InternVL2ファミリーの中で最小のInternVL2-1Bモデルを通じて、その技術的特徴を概観的に紹介します。同時に、アイチップスマートのAX650NとAX630Cという2つのエッジAIチップでInternVL2-1Bを適用する基本的な方法も共有します。これにより、エッジ側でのマルチモーダル大規模モデル展開に関わる開発者に新しい視点を提供し、エッジ側でのマルチモーダル大規模モデルの探求を促進することを目指します。


InternVL2-1B

GitHubリポジトリ：https://github.com/OpenGVLab/InternVL
公式ブログ：InternVL2 https://link.zhihu.com/?target=https%3A//internvl.github.io/blog/2024-07-02-InternVL-2.0/
オンラインデモ：https://internvl.opengvlab.com/

技術的特徴
![v2-ea0b077ee35bada96701cd926a3c9bf5_1440w](https://github.com/user-attachments/assets/3794f79e-c089-4c21-9120-f0023d123f19)

1. **マルチモーダル処理能力**：より大規模なバージョンと同様に、InternVL2-1Bは画像とテキストデータの統合処理をサポートし、クロスモーダルコンテンツの理解と生成を目指しています。

2. **軽量化設計**：1Bパラメータ規模は比較的小さなモデルサイズを意味し、これによりInternVL2-1Bはモバイルデバイスやエッジコンピューティングなど、リソースが制限された環境への展開に適しています。パラメータは少ないものの、緻密な設計により良好な性能を維持しています。

3. **段階的アライメント学習戦略**：小から大へ、粗から精へという方式で学習を行い、より少ない計算リソースで高い効果を達成すると同時に、モデルの知識転移能力も促進しています。

4. **効率的なアーキテクチャ設計**：限られたパラメータで最適な性能を実現するため、InternVL2-1Bは特別に最適化されたネットワーク構造や注意機構を採用し、少ないパラメータ数でも効果的に複雑な視覚言語の関連性を捉えることができます。

5. **多様なダウンストリームタスクのサポート**：小型モデルではありますが、InternVL2-1Bは画像説明生成や視覚的質問応答など、一連の基本的な視覚-言語タスクを実行でき、ユーザーに一定の機能の多様性を提供しています。

6. **オープンソースコードとモデルの重み**：OpenGVLabの一貫した方針に従い、InternVL2-1Bのコードと事前学習モデルもオープンソースで提供され、研究者や開発者が利用しやすくなっています。

性能指标
![v2-9b52ab70475332c198e43c73aadd5ab5_r](https://github.com/user-attachments/assets/3d91d035-acf5-4842-aceb-a8f36d2c245f)
![v2-4018121051cc7a032574a552d64d3e33_r](https://github.com/user-attachments/assets/34020adf-f160-45a9-80ce-40ebc1f6a0f4)

模型変換について説明します。

AIチップ上でAIアルゴリズムモデルを展開する経験のある方なら、モデルをチップのNPUで実行するためには、チップメーカーが提供するNPUツールチェーンを使用する必要があることをご存知でしょう。ここでは、Pulsar2を使用します。

Pulsar2はアイチップスマートの新世代NPUツールチェーンで、以下の4つの強力な機能を統合しています：
- モデル変換
- オフライン量子化
- モデルコンパイル
- ヘテロジニアススケジューリング

これらの機能により、ネットワークモデルの効率的な展開ニーズをさらに強化しています。第3世代・第4世代NPUアーキテクチャに対して深いカスタマイズ最適化を行うと同時に、演算子とモデルのサポート能力と範囲を拡張し、Transformer構造のネットワークも良好にサポートしています。

最新のPulsar2 3.2バージョンでは、大規模言語モデルのコンパイル機能が密かに追加され、`pulsar2 llm_build`のサブコマンドに隠されています。

モデルの取得と変換手順について説明します：

1. モデルの取得:
```text
git clone https://github.com/AXERA-TECH/ax-llm-build.git
cd ax-llm-build
pip install -U huggingface_hub
mkdir -p OpenGVLab/InternVL2-1B/
huggingface-cli download --resume-download OpenGVLab/InternVL2-1B/ --local-dir OpenGVLab/InternVL2-1B/
```

* ax-llm-buildは、LLMとVLMをコンパイルする際に必要な各種補助ツールやスクリプトファイルを一時的に格納するためのリポジトリです（継続的に更新）

2. ワンクリックコンパイル:
```text
pulsar2 llm_build --input_path OpenGVLab/InternVL2-1B/ --output_path OpenGVLab/InternVL2-1B-ax650 --kv_cache_len 1023 --hidden_state_type bf16 --prefill_len 128 --chip AX650
```

3. 埋め込み処理と最適化:
```text
chmod +x ./tools/fp32_to_bf16
chmod +x ./tools/embed_process.sh
./tools/embed_process.sh OpenGVLab/InternVL2-1B/ OpenGVLab/InternVL2-1B-ax650
```

最終的にInternVL2-1B-ax650ディレクトリには以下のファイルが含まれます：

```text
OpenGVLab/InternVL2-1B-ax650/
├── intervl_vision_part_224.axmodel         // vit-lモデル (325MB)
├── model.embed_tokens.weight.bfloat16.bin  // 埋め込みファイル (259MB)
├── qwen2_p128_l0_together.axmodel          // llmレイヤー (16MB)
├── qwen2_p128_l10_together.axmodel         // 以下同様のレイヤーファイル
...
├── qwen2_p128_l9_together.axmodel
└── qwen2_post.axmodel                      // 後処理モデル (141MB)
```

このプロセスでは、モデルの取得、コンパイル、最適化が行われ、AIチップ上で実行可能な形式に変換されています。


上板デモについて説明します：

関連資料
迅速な試用を可能にするため、ネットワークドライブに以下のプリコンパイル済みの資料を提供しています：
* AX630C向け
* AX650N向け

ファイル構成：
* `run_internelvl2.sh` - 実行スクリプト
* `main_internvl` - メインプログラム
* `internvl`フォルダ - プリコンパイル済みのモデルファイルと埋め込みファイルを含む
* `internvl_tokenizer.py` - transformerライブラリベースのtokenizerパーサーサービス
* `readme.txt` - ボード上での実行手順と注意事項

大サイズ処理機能
AX650Nをベースに、448×448ピクセルの入力画像サイズでのデモを提供しています。画像情報量が多いため、より詳細な解析が可能で、OCR機能や中英翻訳能力まで実演できます。

これらの資料の詳細な使用例や具体的な実行結果があれば、続けて説明できます。
![v2-e63b890ccd78d1fc96795b64fa762138_1440w](https://github.com/user-attachments/assets/7b038513-3dbb-456f-a421-884e414a7e63)

![v2-09ef14c275fa05a5bb071aff6ddf63c1_1440w](https://github.com/user-attachments/assets/c224c5e9-ca7d-4b13-aab3-11e27a1d7626)



小サイズ処理機能
AX630Cをベースに、224×224ピクセルの入力画像サイズでのデモを提供しています。
より具体的な処理結果や性能に関する情報があれば、それらを共有するのが有用でしょう。小サイズの画像処理は、計算リソースの制約がより厳しいエッジデバイスでの使用に適していると考えられます。


![v2-0c0d8d1af5f4bf02b2dc238ff923b8eb_1440w](https://github.com/user-attachments/assets/fb480d67-cc5b-4fff-923f-8ab6c485742f)
![v2-593e5771f28b50c63abc2bf1bf1514a2_1440w](https://github.com/user-attachments/assets/5c1daa0c-1fc5-4bb7-a642-3e56913fd2c2)

現在の実装状況と最適化の考察について説明します：

現状の制限：
* Vision Partモジュールのビット-Lモデルの量子化加速をまだ実施していないため、画像エンコーディングの速度がやや遅くなっています
* ただし、AX650NとAX630Cは本来ViTモデルの計算効率が非常に高く、今後も推論時間の最適化を継続的に行っていく予定です

展開最適化に関する考察：

1. 画像サイズの影響：
* 入力画像が大きいほど、Vision Part（Image Encoder）が生成する特徴ベクトルが増加
* 計算量も増大
* InternVL2ファミリーの最小1Bバージョンでも、Vision PartにViT-Large規模の画像エンコーディングモデルを採用している

2. 処理効率への影響：
* 画像から生成される特徴ベクトルが多いほど、LLMへの入力プロンプトが長くなる
* 入力トークン数が増加
* TTFT（Time To First Token、最初のトークンまでの時間）が増加

このトレードオフを考慮した最適化が今後の課題となっています。
![v2-196b3510e4a561c041e9f64b8bc9be25_1440w](https://github.com/user-attachments/assets/04197323-1c91-46a9-a36b-880054a0f890)



224と448の2つの入力サイズにおけるU8とU16量子化後の推論時間統計を示します：

| モデル | 入力サイズ | 量子化精度 | 計算量 | AX650N | AX630C |
|--------|------------|------------|---------|---------|---------|
| ViT-300M | 1,3,224,224 | U8 | 162 GOPs | 25 ms | 145 ms |
| | | U16 | | 49 ms | 290 ms |
| | 1,3,448,448 | U8 | 724 GOPs | 140 ms | 737 ms |
| | | U16 | | 347 ms | TBD |

結びに：

* 最小のInternVL2-1Bのみの展開を試みましたが、本来は低コスト家庭用カメラチップ（AX630C）として位置づけられているチップ上でVLMをローカルでスムーズに実行できることは大きな breakthrough です。例えば：
  * ネットワーク接続（Bluetooth含む）不要のスマートグラス
  * スマートなインスタントカメラ
  * 様々な興味深いウェアラブルデバイス

* 大規模言語モデルの小型化が急速に発展するにつれ、より多くの興味深いマルチモーダルAIアプリケーションがクラウドサービスからエッジデバイスへと移行しています。業界の最新動向を追跡し、より多くのエッジ向け大規模モデルに対応していきますので、引き続きご注目ください。

謝辞：
* ax-llmプロジェクトへのInternVL2対応追加 @折秋水
* AI技術部のメンバーの皆様
* 




