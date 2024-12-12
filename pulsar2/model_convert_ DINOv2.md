AX650Nにおける DINOv2の導入

背景
最近、Transformerネットワーク構造に基づく大規模ビジョンモデルが爆発的に増加しています。Segment Anything（SAM）に続いて、Meta AIは再び重要なオープンソースプロジェクト——DINOv2をリリースしました。DINOv2は強力な画像特徴を抽出でき、下流タスクで**ファインチューニングが不要**なため、多くの異なるアプリケーションにおける新しいBackboneとして適しています。

以前リリースされたSegment Anythingと比較して、DINOv2は応用分野と適用範囲がより広く、原論文の実験も複数のCV分野の古典的な下流タスク（深度推定、セマンティックセグメンテーション）をカバーしています。

本文では、DINOv2の基本原理を簡単に紹介し、同時にONNXモデルのエクスポート方法や、優れたエッジAIチップ**AX650N**への導入とリアルタイム実行（**フレームレート＞30fps**）の方法を説明します。DINOv2を基に下流タスクの移行を行っている業界の皆様に、エッジデバイスでの実装参考として提供できれば幸いです。

DINOv2の概要
Meta AI公式ブログでは、DINOv2の特徴を以下のようにまとめています：
* 自己教師あり学習
* 下流タスクへの移行時にファインチューニングが不要
* すぐに使える視覚基盤大規模モデル

DINOv2は、自己教師あり学習を使用して、この分野で使用される標準的な手法と同等またはそれを上回る結果を達成する、新しい高精度コンピュータビジョンモデルの学習方法です。他の自己教師ありシステムと同様に、DINOv2手法を使用するモデルは、関連するメタデータを必要とせずに、任意の画像コレクションで学習できます。これは、特定のラベルやタイトルのセットを含む画像だけでなく、受け取ったすべての画像から学習できることを意味します。DINOv2は、単純な線形分類器の入力として直接使用できる高性能な特徴を提供します。この柔軟性により、DINOv2は多くの異なるコンピュータビジョンタスクのための多目的なバックボーンとして使用できます。

![v2-5b38e0988e021ae5e4b4a7226756e1a6_r](https://github.com/user-attachments/assets/8bbd1d0c-9c76-49df-b8eb-79109a22ab2f)



論文の実験では、DINOv2の下流タスクにおける優れた能力が示されており、例えば分類、セグメンテーション、画像検索などの応用分野での成果が報告されています。特に最も驚くべき点は、深度推定において、DINOv2の結果がin-domainとout-of-domainの両方でSOTAのパイプラインを明確に上回っていることです。著者らは、この強力なドメイン外でのパフォーマンスは、自己教師あり特徴学習と軽量なタスク特有モジュール（例えば線形分類器）を組み合わせた結果だと考えています。

論文リンク：https://arxiv.org/pdf/2304.07193.pdf
Githubリンク：https://github.com/facebookresearch/dinov2
Meta提供のDINOv2オンラインDEMO：DINOv2 by Meta AI

この論文の詳細な中国語解説については、**OpenMMLab**が共有している技術記事を参照することをお勧めします。

https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/fjsmYZ6DK-uRTdTnHEIaEw


AX650Nは、高い演算能力と電力効率を兼ね備えたSoCチップです。以下の機能を統合しています：

* **8コアCortex-A55** CPU
* **18TOPs@INT8** NPU（**Transformerモデル向けに最適化済み**）
* **8K@30fps**対応の**ISP**
* H.264、H.265コーデック対応VPU

インターフェースについては：
* **64bit LPDDR4x**をサポート
* 複数のMIPI入力
* ギガビットEthernet
* USB
* HDMI 2.0b出力
* **32チャンネル1080p@30fpsデコード**に対応

この強力な性能により、AX650Nはスマートシティ、スマート教育、スマート製造などの分野でユーザーにより大きな価値を提供することができます。

以下が日本語訳です：

モデル変換
本文ではDINOv2が提供する事前学習モデルViT-S/14を例に導入プロセスを説明します。

モデルのダウンロード
* DINOv2のオープンソースプロジェクトをダウンロード

```text
git clone https://github.com/facebookresearch/dinov2.git
```

* dinov2ディレクトリに移動し、以下のファイルでdinov2/models/vision_transformer.pyを置き換え
https://github.com/AXERA-TECH/ax-samples/releases/download/v0.4/vision_transformer.py
github.com/AXERA-TECH/ax-samples/releases/download/v0.4/vision_transformer.py

* ONNXモデルの取得、dinov2のルートディレクトリで実行

```python3
from dinov2.models import vision_transformer as vits
import torch

_DINOV2_BASE_URL = "https://dl.fbaipublicfiles.com/dinov2"

def _make_dinov2_model_name(arch_name: str, patch_size: int) -> str:
    compact_arch_name = arch_name.replace("_", "")[:4]
    return f"dinov2_{compact_arch_name}{patch_size}"

def make_model(
    *,
    arch_name: str = "vit_large",
    img_size: int = 518,
    patch_size: int = 14,
    init_values: float = 1.0,
    ffn_layer: str = "mlp",
    block_chunks: int = 0,
    pretrained: bool = True,
    **kwargs,
):
    model_name = _make_dinov2_model_name(arch_name, patch_size)
    vit_kwargs = dict(
        img_size=img_size,
        patch_size=patch_size,
        init_values=init_values,
        ffn_layer=ffn_layer,
        block_chunks=block_chunks,
    )
    vit_kwargs.update(**kwargs)
    model = vits.__dict__[arch_name](**vit_kwargs)

    if pretrained:
        url = _DINOV2_BASE_URL + f"/{model_name}/{model_name}_pretrain.pth"
        state_dict = torch.hub.load_state_dict_from_url(url, map_location="cpu")
        model.load_state_dict(state_dict, strict=False)

    return model

model = make_model(arch_name="vit_small", pretrained=True)
model.eval()

dummy_input = torch.randn(1, 3, 518, 518, dtype=torch.float32)
torch.onnx.export(model, dummy_input, "dinov2_small_518.onnx", verbose=True, opset_version=11)
```

* onnxsimを使用して計算グラフを最適化し、dinov2_small_518-sim.onnxモデルを取得

```text
$ pip install onnxsim
```



以下が日本語訳です：

ONNXグラフの最適化を実行

```
$ onnxsim dinov2_small_518.onnx dinov2_small_518-sim.onnx
```
[詳細な出力ログの翻訳は省略]

ONNXモデルフォーマットでDINOv2モデルをサポートするために必要な演算子は以下のものだけです：
Add、Concat、Conv、Div、Erf、Gather、MatMul、Mul、Pow、ReduceMean、Reshape、Slice、Softmax、Sqrt、Sub、Transpose

モデルのコンピレーション
AX650N付属のAIツールチェーンPulsar2を使用し、グラフ最適化、オフライン量子化、コンピレーション、検証機能をワンクリックで実行します。

```
$ pulsar2 build --input model/dinov2_small_518-sim.onnx --output_dir dinov2 --config config/dinov2_config.json
```
[詳細なビルドログの翻訳は省略]

config.jsonの内容は以下の通りです。このconfig.jsonを個別に示す目的は、AX650NのツールチェーンがTransformerモデル向けに特別な量子化精度調整設定を持っていることを説明するためです。有効にすると、生成されるモデルの精度が向上します。

```json
{
  "model_type": "ONNX",
  "npu_mode": "NPU3",
  "quant": {
    "input_configs": [
      {
        "tensor_name": "DEFAULT",
        "calibration_dataset": "./dataset/imagenet-32-images.tar",
        "calibration_size": 32,
        "calibration_mean": [123.675, 116.28, 103.53],
        "calibration_std": [58.395, 57.12, 57.375]
      }
    ],
    "calibration_method": "MSE",
    "transformer_opt_level": 1
  },
  "input_processors": [
    {
      "tensor_name": "DEFAULT",
      "tensor_format": "RGB",
      "src_format": "BGR",
      "src_dtype": "U8",
      "src_layout": "NHWC"
    }
  ],
  "compiler": {
    "check": 0
  }
}
```

ボードへの導入
AX-Samples
オープンソースプロジェクトAX-Samplesは、爱芯元智のAI SoC上での一般的な深層学習オープンソースアルゴリズムの実装例を提供し、コミュニティの開発者が迅速な評価と適応を行えるようにしています。

最新バージョンではAX650シリーズのNPUサンプルの提供を開始しており、本文で紹介したDINOv2の参考コードも含まれています。
ax_dinov2



以下が日本語訳です：

実行
DINOv2の公式Model ZOOは基盤モデルのみを提供しているため、そのPCA実装を参考に特徴マップの可視化出力のみ可能です。

```text
# ./ax_dinov2 -m dinov2_small_518_precision_opt.axmodel -i dog-chai.jpeg -r 100
--------------------------------------
model file : dinov2_small_518_precision_opt.axmodel
image file : dog-chai.jpeg
img_h, img_w : 518 518
--------------------------------------
--------------------------------------
post process cost time:111.22 ms
--------------------------------------
Repeat 100 times, avg time 28.64 ms, max_time 28.69 ms, min_time 28.63 ms
--------------------------------------
--------------------------------------
#
```

テスト画像1
* 「テスト画像1」：DINOv2は「柴犬」の胴体、前脚、頭部、目、鼻、耳などの意味的情報を明確に区別できます。

テスト画像2
* 「テスト画像2」：DINOv2は画像中の犬、自転車、柵などの意味的情報を明確に区別できます。

性能統計
モデル | 入力サイズ | AX650N推論時間(ms) | フレームレート
---|---|---|---
ViT-S/14 distilled | 518*518 | 28 | 35
ViT-B/14 distilled | 518*518 | 92 | 10
ViT-L/14 distilled | 518*518 | 30 | 53

結論
DINOv2は、ファインチューニングが不要な自己教師あり学習手法として、画像特徴抽出において優れた性能を示し、様々な視覚タスクに適用可能です。DINOv2を基にした下流タスクの更なる登場が期待されます。

**謝辞**
* DINOv2：ファインチューニング不要、SAMの空白を埋め、複数の下流タスクをサポート
@OpenMMLab
* onnxsimツール
@大缺弦
* dumpツール
@許欣然
* ax_dinov2コード
@折秋水

更新
私は圈圈虫、技術を愛する元ネット有名人の**中年おじさん**です。AXERA技術交流QQグループ（139953715）に参加してください。業界の多くの専門家がオンラインで質問に答えています。また、AXera-Pi Pro（AX650N搭載）の最新情報にもご注目ください。

2024年3月20日17:21編集・IP所在地：広東

