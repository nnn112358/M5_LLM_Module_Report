

背景
セマンティックセグメンテーション（**Semantic Segmentation**）はコンピュータービジョンにおける基本的なタスクです。単一画像の分類タスクと比較すると、セマンティックセグメンテーションはピクセルレベルでの分類タスクと言えます。セマンティックセグメンテーションは、多くのダウンストリームアプリケーション、特にここ数年の自動運転技術の実用化を可能にしました。

本稿では、Segformerの基本原理を簡単に紹介し、同時にONNXモデルのエクスポート方法と、優れたエッジAIチップ**AX650N**への展開方法について解説します。エッジ/エンドデバイスでのTransformerモデルの展開に興味を持つ業界関係者に新しい視点を提供できればと思います。

SegFormerの紹介
論文では、Transformersと軽量なMulti-Layer Perceptron（MLP）デコーダーを組み合わせたシンプルで効率的、かつパワフルなセマンティックセグメンテーションフレームワークSegFormerが提案されています。SegFormerには2つの魅力的な特徴があります：

1. SegFormerは、マルチスケール特徴を出力する新しい階層的Transformerエンコーダーを含んでいます。位置エンコーディングを必要としないため、位置エンコーディングの補間が不要です。

2. SegFormerは複雑なデコーダーを回避しています。提案されたMLPデコーダーは異なる層から情報を集約し、Local AttentionとGlobal Attentionを組み合わせて強力な表現を実現します。このシンプルで軽量な設計が、Transformerを使用した効率的なセグメンテーションの鍵となっています。

論文では上記のアプローチを拡張し、SegFormer-B0からSegFormer-B5まで、異なるサイズのモデルシリーズを開発しました。これらは従来のセグメンテーションモデルと比較して、より優れた性能と効率を達成しています。例えば、SegFormer-B4はADE20Kにおいて64Mのパラメータで50.3%のmIoUを実現し、最高モデルのSegFormer-B5はCityscapesの検証セットで84.0%のmIoUを達成しています。

論文リンク：https://arxiv.org/pdf/2105.15203.pdf
Githubリンク：https://github.com/NVlabs/SegFormer

バックボーンネットワーク

![v2-375954b8d4dc6b4ece91f27842e6a53e_1440w](https://github.com/user-attachments/assets/a4c27e6b-1343-4cc9-8831-19a339d9d3d7)


階層的Transformerエンコーダー
一連のMix Transformerエンコーダー（MiT）をMiT-B0からMiT-B5まで設計しました。これらは同じ構造を持ちながら、サイズが異なります。MiT-B0は高速推論のための軽量モデルであり、MiT-B5は最高性能を追求した最大モデルです。MiTの設計は部分的にViTからインスピレーションを得ていますが、セマンティックセグメンテーション向けにカスタマイズと最適化が施されています。

軽量なAll-MLPデコーダー
MLPレイヤーのみで構成される軽量なデコーダーを統合しています。これにより、他の手法で一般的に使用される手作業の実装や計算負荷の高いコンポーネントを回避しています。このようなシンプルなデコーダーの実現が可能な理由は、階層的Transformerエンコーダーが従来のCNNエンコーダーよりも大きな有効受容野（ERF）を持っているためです。

![v2-6cc6dd86a05bdd0ec4a160ff2c937da9_1440w](https://github.com/user-attachments/assets/751a4916-9591-406e-8104-b026c6b6ee16)

モデル変換

本記事では、segformer-b0-cityscapes-640-1280を例として説明します。

モデルのダウンロード
今回は、Huggingfaceの ModelZooから直接モデルをダウンロードすることをお勧めします（NVIDIAはHuggingfaceに多くのモデルをアップロードしています）。

![v2-26a6ae975541d3192fc70ea965d22a1d_1440w](https://github.com/user-attachments/assets/075d980d-b474-4143-ad88-6453102418d3)

```python
# ONNXモデルエクスポートのスクリプト

import torch
from transformers import SegformerForSemanticSegmentation, SegformerFeatureExtractor
from pathlib import Path
from onnxruntime.quantization import quantize_dynamic, QuantType, preprocess 
import onnx
import onnxruntime
import os
from PIL import Image
from typing import List

def export_model(model_name: str, export_dir: str, input_sample: torch.Tensor):
    model = SegformerForSemanticSegmentation.from_pretrained(model_name)
    model.eval()
    export_path = os.path.join(export_dir, model_name)
    Path(export_path).mkdir(parents=True, exist_ok=True) 
    onnx_path = os.path.join(export_path, "model.onnx")
    # 最初の次元を動的に保持しながらモデルをONNXにエクスポート
    torch.onnx.export(model, input_sample, onnx_path, export_params=True,
                        opset_version=11,
                        input_names=["input"],
                        output_names=["output"],
                        )

export_dir = "./segformer_export/"

model_name = "nvidia/segformer-b0-finetuned-cityscapes-640-1280"
export_model(model_name, export_dir, torch.randn([1,3,640,1280]))
```

```bash
# onnxsimの最適化

$ onnxsim segformer-b0-cityscapes-640-1280.onnx segformer-b0-cityscapes-640-1280-sim.onnx
Simplifying...
Finish! Here is the difference:
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃            ┃ Original Model ┃ Simplified Model ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Add        │ 136            │ 136              │
│ Concat     │ 21             │ 1                │
│ Constant   │ 176            │ 0                │
│ Conv       │ 20             │ 20               │
│ Div        │ 46             │ 46               │
│ Erf        │ 8              │ 8                │
│ MatMul     │ 68             │ 68               │
│ Mul        │ 46             │ 46               │
│ Pow        │ 30             │ 30               │
│ ReduceMean │ 60             │ 60               │
│ Relu       │ 1              │ 1                │
│ Reshape    │ 76             │ 76               │
│ Resize     │ 4              │ 4                │
│ Shape      │ 20             │ 0                │
│ Slice      │ 20             │ 0                │
│ Softmax    │ 8              │ 8                │
│ Sqrt       │ 30             │ 30               │
│ Sub        │ 30             │ 30               │
│ Transpose  │ 76             │ 76               │
│ Model Size │ 14.3MiB        │ 14.3MiB          │
└────────────┴────────────────┴──────────────────┘
```

# argmax出力ヘッドの追加
AX650NのNPUはargmaxオペレータをサポートしているため、モデルの出力ヘッドにargmaxを追加し、各ピクセルの最も確信度の高いクラスIDを直接取得することができます。

まず、onnx_graphsurgeonの依存関係をインストールします：

```bash
pip install onnx_graphsurgeon --index-url https://pypi.ngc.nvidia.com
```

argmax opの追加：

```python
import numpy as np
import onnx
import onnx_graphsurgeon as gs

model_path = "./segformer-b0-cityscapes-640-1280-sim.onnx"
output_model_path = "./segformer-b0-cityscapes-640-1280-sim-argmax.onnx"

onnx_model = onnx.load(model_path)
onnx_graph = gs.import_onnx(onnx_model)
node_last_conv = onnx_graph.nodes[-1]

# ArgMaxの属性
axis = 1
keepdims = 1

argmax_out_shape = node_last_conv.outputs[0].shape.copy()
argmax_out_shape[axis] = 1

argmax_out = gs.Variable(
    "argmax_output",
    dtype=np.int64,
    shape=argmax_out_shape,
)

argmax_node = gs.Node(
    op="ArgMax",
    name="decode_head_ArgMax",
    inputs=[node_last_conv.outputs[0]],
    outputs=[argmax_out],
    attrs={"axis": axis, "keepdims": keepdims},
)

onnx_graph.nodes.append(argmax_node)
onnx_graph.outputs.clear()
onnx_graph.outputs = [argmax_out]
onnx_graph.cleanup().toposort()
onnx_model_with_argmax = gs.export_onnx(onnx_graph)
onnx_model_with_argmax.ir_version = onnx_model.ir_version

onnx.save(onnx_model_with_argmax, output_model_path)
```

argmax追加前後の2つのONNXモデルの比較：

![v2-2b3487d39c04d191775e0ce7081e3adc_1440w](https://github.com/user-attachments/assets/d6fa5c82-03e7-499e-aebc-6145b0b85dd5)

モデルのコンパイル

AX650Nに付属するAIツールチェーンPulsar2を使用して、グラフ最適化、オフライン量子化、コンパイル、比較機能をワンクリックで実行します。

```bash
$ pulsar2 build --input model/segformer-b0-cityscapes-640-1280-sim-argmax.onnx --output_dir segformer/ --config config/segformer_config.json --npu_mode NPU3
```

[実行ログの詳細は省略]

ボード上のデプロイ

AX-Samples

オープンソースプロジェクトAX-Samplesは、愛芯元智のAI SoC上での一般的な深層学習オープンソースアルゴリズムのサンプルコードを実装しており、コミュニティの開発者が迅速な評価と適応を行えるようにしています。

最新バージョンではAX650シリーズのNPUサンプルの提供を開始しており、本記事で紹介したSegformerのリファレンスコードも含まれています。

ax_segformer
github.com/AXERA-TECH/ax-samples/blob/main/examples/ax650/ax_segformer_steps.cc

実行例：
```bash
# ./ax_segformer -m segformer-b0-cityscapes-640-1280-argmax.axmodel -i segformer_test.png
--------------------------------------
model file : segformer-b0-cityscapes-640-1280-argmax.axmodel
image file : segformer_test.png
img_h, img_w : 640 1280
--------------------------------------
post process cost time:7.07 ms
--------------------------------------
Repeat 1 times, avg time 48.15 ms, max_time 48.15 ms, min_time 48.15 ms
--------------------------------------
--------------------------------------
```
![v2-a98ad655cb02ff9e7a41e847be754922_1440w](https://github.com/user-attachments/assets/088bbb2d-4ff4-4e6f-a53c-15d56f1b6ee5)

今後の計画
- ビジョン大規模モデルDINOv2のデプロイを試みる予定です。ご期待ください！

謝辞
- SegFormer：シンプルで効果的なセマンティックセグメンテーションの新しいアプローチ @Anonymous
- onnxsimツール @大缺弦
- argmaxオペレータ追加スクリプト @走走
- ax_segformerコード @折秋水

私は圈圈虫、技術を愛する元ネット有名人の中年おじさんです。AXERA技術交流QQグループ（139953715）にぜひご参加ください。業界の多くの専門家がオンラインで質問に答えています。また、AXera-Pi Pro（AX650N搭載）の最新情報もフォローしてください。






