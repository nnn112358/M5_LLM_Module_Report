


*MiniCPM-V 2.0: 優れたOCRと理解能力を備えたエッジ向け高効率マルチモーダル大規模モデル*

背景
今年4月、面壁智能＆清華大学自然言語処理研究室は、MiniCPMシリーズの最新マルチモーダルバージョンMiniCPM-V 2.0をリリースしました。このモデルはMiniCPM 2.4BとSigLip-400Mをベースに構築され、合計2.8Bのパラメータを持っています。MiniCPM-V 2.0は優れた光学文字認識（OCR）とマルチモーダル理解能力を備えています。このモデルは、総合的なOCR能力評価ベンチマークOCRBenchにおいてオープンソースコミュニティで最高レベルを達成し、シーンテキスト理解においてはGemini Proに近い性能を実現しています。簡単に言えば、画像内の内容をより良く理解し、正確な「画像から文章を生成する」能力を実現し、見たものがそのまま得られるということです。

本文では、MiniCPM-V 2.0の新機能を概観的に探ります。また、愛芯元智のAX650Nチップ上でのMiniCPM-V 2.0の適応に関する最新の進展を共有し、エッジ向けマルチモーダル大規模モデルの開発者に新しい視点を提供し、エッジ向けマルチモーダル大規模モデルの探求を促進します。

MiniCPM-V 紹介
githubアドレス：https://github.com/OpenBMB/MiniCPM-V
公式ブログ：https://openbmb.vercel.app/minicpm-v-2

MiniCPM-V 2.0の特徴
1. **優れたOCRとマルチモーダル理解能力。**MiniCPM-V 2.0はOCRとマルチモーダル理解能力を大幅に向上させ、シーンテキスト理解能力はGemini Proに匹敵し、複数の主要評価ベンチマークにおいて、より大きなパラメータ規模（例：17-34B）の主流モデルを上回る性能を示しています。

2. **信頼性のある動作。**MiniCPM-V 2.0は、マルチモーダルRLHF（RLHF-V [CVPR'24]シリーズ技術による）によってアラインメントされた最初のエッジ向けマルチモーダル大規模モデルです。このモデルはObject HalBenchにおいてGPT-4Vに匹敵する性能を達成しています。

3. **任意のアスペクト比を持つ高解像度画像の効率的なエンコーディング。**MiniCPM-V 2.0は、180万ピクセルの任意のアスペクト比を持つ画像入力（最新のLLaVA-UHD技術に基づく）を受け入れることができ、これにより小さなオブジェクトや密集したテキストなど、より細かい粒度の視覚情報を認識できます。

4. **効率的な展開。**MiniCPM-V 2.0は、ほとんどの一般向けグラフィックスカード、パーソナルコンピュータ、モバイル端末などに効率的に展開できます。

5. **バイリンガルサポート。**MiniCPM-V 2.0は、優れた中国語と英語のバイリンガルマルチモーダル能力をサポートしています。この能力はVisCPM [ICLR'24]論文で提案されたマルチモーダル能力の言語間汎化技術によって実現されています。

マルチモーダルの「小型パワーハウス」
MiniCPM-V 2.0は、より大きなパラメータ規模のマルチモーダル大規模モデルと比較しても優れた成績を示しており、業界の「小型パワーハウス」の名に恥じない性能を発揮しています。


![v2-a33c171f5af40eb2799242b870bfe096_1440w](https://github.com/user-attachments/assets/720d70ea-5124-453b-bce2-9d57e515f4dc)


上板デプロイ

コマンドラインとUIの2種類のサンプルを提供しており、ネットワークドライブにアップロードしています。ぜひお試しください。

**コマンドラインバージョン** 
**テスト画像：**



![v2-158fbf507aa5eb0025d2b5019ce9d345_1440w](https://github.com/user-attachments/assets/9e2f8a7a-4411-428b-930e-a85e5ee61340)

![v2-4842b58babf0e0c7e33db3b7cf627022_1440w](https://github.com/user-attachments/assets/6c1af919-1eea-4514-8512-7c6d40eeb7f8)

性能統計
項目仕様：
入力画像サイズ：280 x 280
Image Encoder：0.8秒
Input Prompt：96トークン
Prefill Time：0.4秒
Decoder：5トークン/秒

終わりに
大規模言語モデルの小型化が急速に進展する中、クラウドサービスからエッジデバイスやエンドデバイスへと、より多くの興味深いマルチモーダルAIアプリケーションが徐々に移行していくでしょう。私たちは業界の最新動向を追い続け、より多くのエンドデバイス向け大規模モデルに対応していきます。引き続きご注目ください。

謝辞
* MiniCPM-V DEMOの開発：@折秋水
* Kimi Chat - より広い世界を見せ、マルチモーダル大規模言語モデルの学習をサポート



