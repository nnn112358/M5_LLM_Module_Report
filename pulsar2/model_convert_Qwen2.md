基于 AX650N/AX630C 部署 Qwen2
https://zhuanlan.zhihu.com/p/706645301


背景

クラウド大規模モデル、エッジ側小規模モデル、クラウドとエッジの連携による
ユーザー体験向上は、今年の大規模言語モデル（LLM）製品化における注目トピックとなっています。今年に入り、各スマートフォンメーカーが次々とエッジ側小規模モデルを発表しています。例えば、GoogleのGemini-nano（1.8B）、VIVOのブルースター大規模モデル（1B）、中国国内の「小型パワフル」MiniCPM（1B）などが、それぞれのスマートフォンに実装され、スマートフォンのインテリジェンス性と利便性を高めています。

では、デバイス数がさらに多いIoT分野でも、経済的で実用的なLLMを実装できるでしょうか？例えば、ローカルな対話、AIエージェント、ファンクションコールなどの機能を実現できるでしょうか？

本稿では、最新のエッジ側大規模言語モデルをコストパフォーマンスの高いSoCに実装する方法を共有し、エッジ側大規模モデル実装の開発者に新しい視点を提供します。

Qwen2の紹介

QwenはアリババグループのQwenチームが開発した大規模言語モデルおよび大規模マルチモーダルモデルシリーズです。現在、言語モデルはQwen2バージョンにアップグレードされています。言語モデルもマルチモーダルモデルも、大規模な多言語・マルチモーダルデータで事前学習され、高品質なデータで微調整することで人間の嗜好に近づけています。Qwenは、自然言語理解、テキスト生成、視覚理解、音声理解、ツール使用、ロールプレイング、AIエージェントとしての対話など、多様な能力を備えています。

最新版のQwen2には以下の特徴があります：

* 0.5B、1.5B、7B、57B-A14B、72Bを含む5つのモデルサイズ
* 各サイズにおいて、基本モデルと指示微調整モデルを提供し、指示微調整モデルは人間の嗜好に合わせて調整されています
* 基本モデルと指示微調整モデルの多言語サポート
* すべてのモデルで32Kの長文コンテキストを安定的にサポート
* ツール呼び出し、RAG（検索拡張テキスト生成）、ロールプレイ、AIエージェントなどをサポート

Hugging Faceの共同創設者兼CEOのClem Delangueは6月26日、Xプラットフォームで、**アリババクラウドがオープンソース化した通義千問（Qwen）の指示微調整モデルQwen2-72Bがオープンソースモデルのランキングで首位を獲得したと**発表しました。

![v2-e2bb7773467f51f0c9ef25e731c8204a_1440w](https://github.com/user-attachments/assets/17d4dbea-afbb-45fd-a748-08cfd74cc4f3)
AX650N
アイチップスマート社の第3世代高効率インテリジェントビジョンチップAX650N。8コアCortex-A55 CPU、高効率NPU、8K@30fps対応のISP、そしてH.264、H.265コーデック対応のVPUを統合しています。インターフェースに関しては、AX650Nは64bit LPDDR4x、複数のMIPI入力、ギガビットEthernet、USB、HDMI 2.0b出力をサポートし、32チャンネルの1080p@30fpsデコードに対応しています。高い演算能力と強力なコーデック機能を内蔵し、産業界における高性能エッジインテリジェンス計算のニーズを満たします。内蔵された多様な深層学習アルゴリズムにより、ビジョン構造化、行動分析、状態検出などのアプリケーションを実現し、Transformer構造ベースのビジョン大規模モデルと言語大規模モデルを効率的にサポートします。豊富な開発ドキュメントを提供し、ユーザーの二次開発を容易にします。


AX630C
アイチップスマート社の第4世代インテリジェントビジョンチップAX630C。このチップは新世代スマートアイ4.0AI-ISPを統合し、最大4K@30fpsのリアルタイム暗視に対応しています。同時に新世代通元4.0高性能・高効率NPUエンジンを統合し、低消費電力、高画質、インテリジェント処理・分析などの面で業界をリードしています。安定性が高く使いやすいSDKソフトウェア開発キットを提供し、ユーザーの低コスト評価、二次開発、量産化の迅速な実現を可能にします。スマートホームアプリケーションや他のAIOTプロジェクトにおいて、ユーザーがより大きな価値を発揮できるよう支援します。

AX630Cの製品仕様を考慮し、今回のデモモデルとして最適なQwen2 0.5B-Instructを選択しました。
LLMのコンパイル
Pulsar2
Pulsar2は新世代のAIツールチェーンで、モデル変換、オフライン量子化、モデルコンパイル、ヘテロジニアススケジューリングの4つの強力な機能を統合し、ネットワークモデルの効率的な展開ニーズをさらに強化しています。第3世代・第4世代NPUアーキテクチャに対して深いカスタマイズ最適化を行うと同時に、演算子とモデルのサポート能力と範囲を拡張し、Transformer構造のネットワークも良好にサポートしています。
最新リリースのPulsar2 3.0バージョンに基づき、AX650NとAX630Cそれぞれに対して暫定版のサポートを提供しています。ぜひお試しください。


ax-llm-buildプロジェクトのダウンロードと実行

まずPulsar2 v3.0-temp版のドキュメントの「開発環境準備」セクションに従って、dockerイメージをインストールしPulsar2のdocker環境に入っていることを前提とします。

```text
git clone https://github.com/AXERA-TECH/ax-llm-build.git
```

Qwen2-0.5B-Instructのダウンロード:
```text
cd ax-llm-build
pip install -U huggingface_hub
huggingface-cli download --resume-download Qwen/Qwen2-0.5B-Instruct --local-dir Qwen/Qwen2-0.5B-Instruct
```

コンパイルの実行:
```text
pulsar2 llm_build --input_path Qwen/Qwen2-0.5B-Instruct/ --output_path Qwen/Qwen2-0.5B-w8a16/ --kv_cache_len 1023 --model_config config/qwen2-0.5B.json --hidden_state_type bf16 --weight_type s8
```

埋め込み処理と最適化:
```text
python tools/extract_embed.py --input_path Qwen/Qwen2-0.5B-Instruct/ --output_path Qwen/Qwen2-0.5B-w8a16/
python tools/embed-process.py --input Qwen/Qwen2-0.5B-w8a16/model.embed_tokens.weight.npy --output Qwen/Qwen2-0.5B-w8a16/model.embed_tokens.weight.float32.bin
chmod +x ./tools/fp32_to_bf16
./tools/fp32_to_bf16 Qwen/Qwen2-0.5B-w8a16/model.embed_tokens.weight.float32.bin Qwen/Qwen2-0.5B-w8a16/model.embed_tokens.weight.bfloat16.bin
```

出力ファイルの説明:
model.embed_tokens.weight.bfloat16.bin、qwen_l0.axmodel〜qwen_l23.axmodel、qwen_post.axmodelがボード上で実行に必要なファイルです。

ax-llmプロジェクト:
ax-llmプロジェクトは、業界で一般的な**LLM（大規模言語モデル）**をAXERAの既存チッププラットフォームに実装する可能性と能力の限界を探るためのものです。コミュニティの開発者が自身の**LLMアプリケーション**の**迅速な評価**と**二次開発**を**容易に**行えるようにします。

AXERA-TECH/ax-llm:
github.com/AXERA-TECH/ax-llm

また、AX650NとAX630Cプラットフォーム向けにプリコンパイルされたLLMサンプルをネットワークドライブで提供しています。
LLM-AX:
pan.baidu.com/s/1_LG-sPKnLS_LTWF3Cmcr7A?pwd=ph0e

実行プロセス（AX650N開発ボード上）の例も提示されており、応答速度は約24.51トークン/秒を達成しています。


性能統計

AX650NとAX630Cは現在W8A16量子化方式を採用しています。

**AX650N：**
| モデル名 | パラメータ数 | 速度(token/s) |
| --- | --- | --- |
| TinyLlama-1.1 | 1.1B | 16.5 |
| Qwen2.0 | 0.5B | 29.0 |
| Qwen2.0 | 1.5B | 11.2 |
| MiniCPM | 2.4B | 6.0 |
| Phi3 | 3.8B | 5.0 |
| Llama3 | 8B | 2.5 |

**AX630C：**
| モデル名 | パラメータ数 | 速度(token/s) |
| --- | --- | --- |
| TinyLlama-1.1 | 1.1B | 5.8 |
| Qwen2.0 | 0.5B | 10.7 |
| Qwen2.0 | 1.5B | 4.0 |

結びに

大規模言語モデルの小型化が急速に発展する中、より多くの興味深いマルチモーダルAIアプリケーションが、クラウドサービスからエッジデバイスやエンドデバイスへと徐々に移行していくでしょう。私たちは業界の最新動向を常に追跡していきますので、引き続きご注目ください。

7月4日から7日まで、アイチップスマートは2024WAICに出展します。上海世博展覧館2号館C1525（H2-C1525）にて、皆様のご来場をお待ちしております。

謝辞
* ax-llm DEMOの開発 @折秋水
* Kimi Chat - より広い世界を見せ、大規模言語モデルの学習をサポート

* 


