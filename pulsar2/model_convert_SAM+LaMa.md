AX650Nを用いた画像修復の実例（SAM + LaMa）
LaMa: Resolution-robust Large Mask Inpainting with Fourier Convolutions
SAM: Segment Anything Model
背景
写真撮影時によくある経験：背景に他の観光客がたくさん写り込んでしまい、写真を撮った後で自分を探すのに時間がかかる。観光客以外にも、ゴミ箱や画面に不要な要素が多すぎると写真全体の美しさを損なってしまいます。Photoshopの技術に自信のない人にとって、これらの要素を画面から取り除くのは非常に困難です。しかし、人工知能技術の発展は、このような作業を簡単にすることを目的としています。たった2ステップで、画面内の不要な要素をすべて取り除くことができます。
この記事では、視覚大規模モデルのSAM + LaMaを使用して、ターゲット領域のワンクリック選択+高品質修復のアプリケーションソリューションを紹介し、最新の愛芯派Pro（アイシンパイPro）コミュニティ開発ボードでインタラクティブな体験を提供します。
LaMa
通常、修復が必要な実際の写真は高解像度であり、より多くの計算コストが必要です。しかし、現在の画像修復手法の大部分は低品質の画像に焦点を当てています。画像の解像度を下げて小さな画像にし、修復結果を拡大して元の画像に適用する方法もありますが、最終結果は元の画像で直接修復を行うよりも品質が劣ります。
この問題に対して、サムスンの研究者たちは新しいモデルLaMa（LArge MAsk inpainting）を提案しました。これは高解像度画像において、画像内の様々な要素を自由に削除することができます。


以下が日本語訳です：

モデル生成
SAM
修正済みのsegment-anythingとsamexporterコードをダウンロード

```text
git clone https://github.com/ZHEQIUSHUI/segment-anything-noeinsum.git
git clone https://github.com/vietanhdev/samexporter.git
```

segment-anythingディレクトリに移動し、ブランチを切り替えてインストール

```text
cd segment-anything-noeinsum
git checkout no-einsum
pip install -e .
```

samexporterのインストール

```text
cd samexporter
pip install -e .
```

sam_vit_b_01ec64.pthのダウンロード

```text
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

onnxのエクスポート

```text
python -m samexporter.export_encoder --checkpoint ./sam_vit_b_01ec64.pth --output vit_b_encoder_noeinsum.onnx --model-type vit_b --opset 11
python -m samexporter.export_decoder --checkpoint ./sam_vit_b_01ec64.pth --output vit_b_decoder.onnx --model-type vit_b
```

onnxsimでonnxを最適化

```text
onnxsim vit_b_encoder_noeinsum.onnx vit_b_encoder_noeinsum.onnx
onnxsim vit_b_decoder.onnx vit_b_decoder.onnx
```

onnxをコンパイルしてcompiled.axmodelを生成、pulsar2 buildの対応する設定ファイルconfig.jsonは以下の通り

[設定ファイルの内容は原文のまま保持]

終わりに
Vision Transformerネットワークモデルの急速な発展に伴い、より多くの興味深いAIアプリケーションがクラウドサービスからエッジデバイスやエンドデバイスへと徐々に移行していきます。Transformerネットワーク構造に基づく先端的な人気モデルの適用成果を継続的に共有していきます：
* テキストベース画像検索
* 深度推定
* YOLO終結者

同時に、コミュニティ開発者のTransformerモデルのエッジ移植における研究のハードルを下げるため、業界優秀なオープンソースインテリジェントハードウェア企業の矽速科技が、AX650Nベースのコミュニティ開発ボード愛芯派Pro（MAIX-IV）を正式に発売しました。ぜひご購入ください。

また、前回の記事で繰り返し言及した新世代ツールチェーンPulsar2コミュニティ版がリリースされました。ぜひお試しください（イースターエッグあり）。

**謝辞**
* SAM+LaMaの適用とDEMO開発 @折秋水
* Segment Anything（SAM）論文解説
* サムスン研究員によるLaMaモデルの提案

私は圈圈虫、技術を愛する元ネット有名人の**中年おじさん**です。AXERAテクニカル交流QQグループ（139953715）にぜひご参加ください。業界の多くの専門家がオンラインで質問に答えています。また、AXera-Pi Pro（AX650N搭載）の最新情報もご注目ください。


