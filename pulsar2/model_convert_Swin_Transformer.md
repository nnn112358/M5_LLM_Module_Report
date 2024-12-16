基于 AX650N 部署 Swin Transformer  
https://zhuanlan.zhihu.com/p/621582671  
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/pulsar2/model_convert_Swin_Transformer.md  



背景

ChatGPTに代表される大規模モデルの印象的な効果により、AI業界は今年新たな推進力を得ています。様々なAIGCアプリケーションが次々と登場しています。ChatGPTのような大規模モデルの核となるネットワーク構造は、すべてGoogleが2017年の論文「Attention Is All You Need」で提案したTransformerに基づいていることは周知の事実です。コンピュータビジョンのモデリングは長らく畳み込みニューラルネットワーク（CNN）が主流でした。Transformer構造のネットワークモデルは、主要な学会で「ランキング上位」の段階に長く留まり、実際の大規模な実用化は目立ちませんでした。ICCV 2021の最優秀論文「Swin Transformer」によって、ようやく精度とパフォーマンスの両面で優れた結果が達成されました。

しかし現在まで、Swin Transformerのようなビジョン系Transformerネットワークモデルの大半はクラウドサーバー上に展開されています。これはGPUがMHA構造の計算により適しているためです。一方、エッジ/エンド側のAIチップは、そのDSAアーキテクチャの制限により、CNN構造のモデル効率を確保することを優先し、MHA構造に対する性能最適化はほとんど行われておらず、場合によってはネットワーク構造の修正が必要なほどです。このことは、アルゴリズムエンジニアがエッジコンピューティングアプリケーションにおいてTransformerネットワークの可能性をさらに追求することを間接的に制限してきました。

今年3月、アイチップスマートは新世代製品AX650Nを発表しました。自社開発の第3世代ニューラルネットワークユニットを搭載し、最新のAIアルゴリズムモデルの展開能力をさらに向上させ、スマートシティ、スマート教育、スマート製造などの分野でユーザーがより大きな価値を発揮できるよう支援します。最近、正式なルートを通じてAX650Nデモボードを入手し、先行体験する機会を得ました。


Swin Transformer

![v2-2a4aa7deed038a36582b226838dc4120_1440w](https://github.com/user-attachments/assets/899ef230-21da-4b69-b46c-d02f00567479)

現在のTransformerの画像分野への応用における主な2つの課題：

* 視覚的実体の変化が大きく、異なるシーンでの視覚Transformerの性能が必ずしも良好ではない
* 画像解像度が高く、ピクセル数が多いため、Transformerのグローバル自己注意に基づく計算により計算量が大きくなる

原理

上記の2つの問題に対して、**スライディングウィンドウ操作と階層的設計**を含むSwin Transformerが提案されました。スライディングウィンドウ操作には、**重複しないローカルウィンドウと重複するクロスウィンドウ**が含まれます。注意の計算をウィンドウ内に制限することで、**一方ではCNN畳み込み演算の局所性を導入し、他方では計算量を削減**できます。様々な画像タスクにおいて、Swin Transformerは優れた性能を示しています。

TransformerやSwin Transformerの詳細な説明は内容が長くなるため、興味のある方は以下を参照してください：
* 台湾大学李宏毅教授の自己注意メカニズムとTransformerの詳細解説
* DHan：Swin Transformer論文読解ノート
* 大康子：図解Swin Transformer

分析
* 一般的なCNNネットワークモデルと比較して、本質的にはMHA（Multi Head Attention）という重要な演算子が追加されただけ
  * LayerNormalization
  * Matmul
  * GELU
* 量子化
  * LN、GELU、Matmulには精度低下のリスクが存在
* 計算効率
  * 最も大きな計算操作がConvからMatmulに変わったため、ハードウェアプラットフォームのMatMul計算能力が重要

モデル変換

Pulsar2の紹介
Pulsar2（仮称）は新世代のAIツールチェーンで、前世代のツールチェーンPulsarの優れた業界経験と不足点の反省を踏まえて再構築されました。モデル変換、オフライン量子化、モデルコンパイル、ヘテロジニアススケジューリングの4つの強力な機能を引き続き含み、ネットワークモデルの迅速かつ効率的な展開ニーズをさらに強化しています。第3世代NPUアーキテクチャに対して深いカスタマイズ最適化を行うと同時に、演算子とモデルのサポート能力と範囲を拡張し、Transformer構造のネットワークも良好にサポートしています。
![v2-e950b9046490b65471d9b1573aea2ef2_1440w](https://github.com/user-attachments/assets/82a4440f-01cd-4121-85dd-1aa334c3973e)


スウィントランスフォーマーモデルのダウンロードと形式変換について説明します。

公式リポジトリからモデルを取得します。PyTorchで学習されたpthフォーマットのモデルを、デプロイメントに適したonnxフォーマットに変換するワンクリックスクリプトを提供します。これによりSwin Transformerの導入障壁を下げ、初心者でも主要な操作を直接把握できるようになります。

```python3
import onnx
import torch
import requests
from onnxsim import simplify
from PIL import Image
from transformers import AutoFeatureExtractor, SwinForImageClassification

def download_swin_model(model_name):
    prefix = "microsoft"
    model_id = f"{prefix}/{model_name}" 
    
    # 画像のダウンロードと推論テスト
    url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    image = Image.open(requests.get(url, stream=True).raw)
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_id)
    model = SwinForImageClassification.from_pretrained(model_id)
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    print("Predicted class:", model.config.id2label[predicted_class_idx])

    # ONNXエクスポート
    model_path = f"{model_name}.onnx"
    torch.onnx.export(
        model,
        tuple(inputs.values()),
        f=model_path,
        do_constant_folding=True,
        opset_version=13,
        input_names=["input"],
        output_names=["output"]
    )

    # ONNXの単純化
    model = onnx.load(model_path)
    model_simp, check = simplify(model)
    assert check, "Simplified ONNX model could not be validated"
    simp_path = f"{model_name}_sim.onnx"
    onnx.save(model_simp, simp_path)

def main():
    download_swin_model(model_name="swin-tiny-patch4-window7-224")

if __name__ == "__main__":
    main()
```

onnx-simplifierの作者@大缺弦に感謝を表します。新しい会社でも素晴らしいオープンソースプロジェクトを生み出し、多くのユーザーに貢献されることを願っています。

モデルのコンパイル:
現在のPulsar2のユーザー体験は、既存のPulsarユーザーの移行抵抗を減らすため、基本的に元のスタイルを踏襲しています。Dockerの環境、コマンドライン、設定ファイルのパラメータ、シミュレーション機能などが含まれます。同時に、コンパイル速度が遅いという問題点に対して大幅な最適化を行い、処理時間を平均して1桁（分単位から秒単位へ）短縮しました。

```bash
$ pulsar2 build --input model/swin-t.onnx --output_dir output --config config/swin-t.json --target_hardware=AX650
```

コンパイルログから、計算グラフの最適化、PTQ量子化、オフラインコンパイルの合計所要時間が約50秒であることがわかります。次に、皆さんが気になるMHA構造がどのように変化したかを見てみましょう。


![v2-d480510e85b69a64fd2891f3260ddc21_1440w](https://github.com/user-attachments/assets/d4869b92-3db9-496f-9530-1acfbab0b36b)

![v2-c79db719673b1a42c955d3bf8591bd82_1440w](https://github.com/user-attachments/assets/eda99181-6aff-4e7f-a379-d02d65f4f4ad)






