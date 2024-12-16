

背景:
エッジデバイスのシナリオでは、モデル推論のリアルタイム性が重要な要件となります。しかし、大半の軽量Vision Transformerネットワークは、既存のエッジ/エンドポイントAIデバイス(CPU、NPU)上で、MobileNetのような軽量CNNと同等の速度を達成できていません。
このViTモデルのリアルタイムデプロイメントを実現するため、マイクロソフトと香港中文大学が共同でCVPR2023で論文「EfficientViT: Memory Efficient Vision Transformer with Cascaded Group Attention」を発表しました。
目的:
この投稿では:

EfficientViTの基本アーキテクチャの原理を紹介
論文のGitHubプロジェクトを使用してONNXモデルをエクスポートする方法
エッジAIチップ「AX650N」へのデプロイ方法

を説明し、エッジ/エンドポイントでのTransformerモデルのデプロイメントに興味がある方々に新しいアプローチを提供することを目指します。

EfficientViTの詳細な紹介をさせていただきます。

**速度のボトルネックの分析**
論文では、ViTの速度ボトルネックを3つの側面から分析しています：
1. 多頭自己注意機構（MHSA）による大量のメモリアクセス時間
2. 注意力ヘッド間の計算の冗長性
3. 非効率なモデルパラメータの配分

**EfficientViTの主要な革新点**

1. **基本構造：EfficientViT Block**
   - サンドイッチレイアウト（Sandwich Layout）
   - カスケード型グループ注意機構（Cascaded Group Attention, CGA）

2. **パラメータの再配分（Parameter Reallocation）**
   効率的な以下の要素間のトレードオフを実現：
   - チャネル数
   - ブロック数
   - ステージ数

**性能評価**

1. **精度**
   - ImageNetデータセットでTop-1分類精度77.1%を達成
   - MobileNetV3-Largeを1.9%上回る精度

2. **スループット改善**
   - NVIDIA V100 GPU：40.4%向上
   - Intel Xeon CPU：45.2%向上

3. **総合的な優位性**
   他の軽量ViTモデルと比較して：
   - 速度面で大幅な優位性
   - 精度面での優位性
   を同時に実現

**参考情報**
- 論文：arxiv.org/abs/2305.070271
- 実装：github.com/microsoft/Cream/tree/main/EfficientViT

このアーキテクチャは、特にエッジデバイスでの展開を考慮した場合、メモリ効率と計算効率の両面で優れた特性を示しています。

![v2-cd8b53927617fb00bcc99cabc83594fd_b](https://github.com/user-attachments/assets/814330e1-3ca4-4625-87ad-dbe5f10cc847)



EfficientViTの核心となる技術革新について詳しく説明します。

**EfficientViT Blockの構造**

1. **基本的な処理フロー**
- 入力特徴 → N個のFFN → CGAレイヤー → N個のFFN → 出力特徴

2. **主要な改善点**
- 注意機構の使用を削減し、メモリアクセスによる時間消費を緩和
- 各FFNの前にDWConv（Depth-wise Convolution）レイヤーを追加
  - ローカルトークン間の情報交換を促進
  - 帰納バイアスの導入に貢献

**最適化のための工夫**

1. **正規化層の変更**
- Layer Normalization → Batch Normalization に置換
- 理由：BNはFC層やConv層と推論時に融合可能で、高速化が実現可能

2. **アーキテクチャの効率化**
- 大きなスケールの層では層数を削減
- 各stageでは2未満の幅拡大係数を使用
  - 深層部での冗長性を軽減
  - より効率的なモデル構造を実現

このアーキテクチャは、計算効率とモデル性能のバランスを巧みに取りながら、特にエッジデバイスでの実用性を重視して設計されています。正規化層の工夫や層数の最適化により、実際のデプロイメント時のパフォーマンスも考慮されています。

![v2-f9e69a89d68005108e101676a6c661a4_1440w](https://github.com/user-attachments/assets/9f2f6508-514b-46b0-b1e3-aa8222793128)

![v2-382b59d11d021a0315bd4e83add29706_1440w](https://github.com/user-attachments/assets/77787ce7-7d99-43c1-93ed-e42cec8fc952)

EfficientViTのモデル変換プロセスについて、詳しく説明させていただきます。

**使用するモデル**：EfficientViT-M5

**Pulsar2について**
Pulsar2は新世代AIツールチェーンで、4つの主要機能を統合しています：
- モデル変換
- オフライン量子化
- モデルコンパイル
- 異種混合スケジューリング

特に第3世代NPUアーキテクチャに対して最適化されており、Transformer構造のネットワークもサポートしています。

**変換手順**

1. **環境準備**
```bash
git clone https://github.com/microsoft/Cream.git
cd Cream/EfficientViT/classification/
pip install -r requirements.txt
```

2. **PyTorchモデルの準備**
- バッチサイズ=1のONNXモデルを生成（エッジデバイスに適した設定）
```bash
wget https://github.com/xinyuliu-jeffrey/EfficientViT_Model_Zoo/releases/download/v1.0/efficientvit_m5.pth
```

```export_onnx_efficientvit_m5.py
from model import build
from timm.models import create_model
import torch

model = create_model(
        "EfficientViT_M5",
        num_classes=1000,
        distillation=False,
        pretrained=False,
        fuse=False,
    )

checkpoint = torch.load("./efficientvit_m5.pth", map_location='cpu')
state_dict = checkpoint['model']
model.load_state_dict(state_dict)
model.eval()
dummy_input = torch.rand([1,3,224,224])

model(dummy_input)

torch.onnx.export(model, dummy_input, "efficientvit_m5.onnx", opset_version=11)

```


3. **ONNXモデルのエクスポートと最適化**
```bash
python export_onnx_efficientvit_m5.py
onnxsim efficientvit_m5.onnx efficientvit_m5-sim.onnx
```

4. **モデルコンパイル**
```bash
pulsar2 build --input model/efficientvit_m5-sim.onnx --output_dir efficientvit-m5/ --config config/effientvit_config.json
```

**最適化のポイント**
- 出力層のBNとFCの構造を融合
- 実行効率の向上を実現
- コンパイル時間は約20秒

この変換プロセスにより、エッジデバイスでの効率的な実行が可能になります。特にBatchNormalizationとFully Connected層の融合は、実行効率の向上に重要な役割を果たします。

![v2-57ec96418382bc8f08d352848ced6f97_1440w](https://github.com/user-attachments/assets/091191e3-db57-4012-8cac-8fbcecbc08e5)

![v2-a5d44310a394599912efdc9fa961faf7_1440w](https://github.com/user-attachments/assets/fe0e7ec8-d947-4712-abe7-1ac1cbc5ac25)


AX-Samplesは、一般的なオープンソースの深層学習アルゴリズムを爱芯元智のAI SoC上で実装したサンプルコードを提供するオープンソースプロジェクトです。このプロジェクトは、コミュニティの開発者が素早く評価や適応を行えるよう支援することを目的としています。最新バージョンでは、AX650シリーズのNPU実装例が徐々に整備されており、Classificationの汎用サンプルでは前述の章で説明したEfficientViTモデルを直接実行することができます。


**実行結果**
```text
# sample_npu_classification -m efficientvit-m5-npu1.axmodel  -i cat.jpg -r 10
--------------------------------------
model file : efficientvit-m5-npu1.axmodel
image file : cat.jpg
img_h, img_w : 224 224
--------------------------------------
topk cost time:0.07 ms
5.5997, 285
5.3721, 283
5.0079, 281
4.5982, 284
4.1884, 282
--------------------------------------
Repeat 10 times, avg time 1.24 ms, max_time 1.24 ms, min_time 1.24 ms
--------------------------------------
```

**性能統計**

AX650Nの総演算性能は18TOPS@Int8で、3つの小コアまたは1つの大コアに分割可能です：
- NPU1：6TOPS
- NPU3：18TOPS

モデル別性能（FPS）：

モデル | NPU1 Batch 8 | NPU3 Batch 8
---|---|---
EfficientViT-M0 | 4219 | 6714
EfficientViT-M1 | 3325 | 5263
EfficientViT-M2 | 2853 | 4878
EfficientViT-M3 | 2388 | 4096
EfficientViT-M4 | 2178 | 3921
EfficientViT-M5 | 1497 | 2710

**今後の計画**
- 論文のCOCOデータセットで学習した物体検出モデルの実装を予定
- 現時点では、**速度**、**精度**、**使いやすさ**のすべてにおいてYOLOv5sを**上回る**Vision Transformerネットワークは見つかっていない

**参考文献**
- CVPR 2023｜EfficientViT：ViTの複数デプロイメントシナリオでのリアルタイム推論を実現

筆者は圈圈虫（クエンクエンチョン）、技術を愛する**中年おじさん**です。AXERA技術交流QQグループに参加して業界の専門家に質問したり、AXera-Pi Pro（AX650N搭載）の最新情報をフォローしたりしましょう。





