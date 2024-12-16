

背景を整理してお伝えします：

目標検出の進化：
* コンピュータビジョン応用の基礎タスクとして、常に業界から注目
* 発展の流れ：
  * 最初の学術的Two-StageアプローチのFaster-RCNN
  * 産業界での効率的な展開に適した最初のOne-StageアプローチのSSD
  * 近年よく知られているYOLOシリーズ（v1からv8、xまで）

従来の検出器の特徴：
* CNNをバックボーンとして特徴抽出
* 検出手法：
  * Anchor-Base（Faster-RCNN、SSD、YOLOv1-v7）
  * Anchor-Free（YOLOv8、YOLOX）
* 非最大値抑制（NMS）による最終的な目標フレームの選択

従来手法の課題：
* NMSによる後処理が推論性能のボトルネック
* NMSは画像情報を使用しないため、バウンディングボックスの保持と削除で誤りが発生しやすい

Transformer系モデルの状況：
* DETRの適用は既に実施したが、YOLOv8やPP-YOLOE+ほどの精度は得られず
* 「AX650Nへのdetr展開」から半年以上経過
* より高速で強力、展開が容易なTransformer目標検出モデルの登場を期待
* **残念ながら、まだ登場していない**

そこで：
* RT-DETR（Real Time Detection Transformer）の展開事例を共有
* 提案から約1年経過しているが、古典的なアプローチの再検討は依然として価値がある
* AX650Nでのエンドツーエンド展開を試み、エッジ/エンド側でのTransformerモデル展開に興味を持つ業界関係者に新しい視点を提供



RT-DETR（Real-Time DEtection TRansformer）の紹介：

論文リンク：
https://arxiv.org/pdf/2304.08069.pdf

GitHubプロジェクト：
GitHub - lyuwenyu/RT-DETR
github.com/lyuwenyu/RT-DETR

概要：
RT-DETRは、百度（Baidu）の研究者によって提案された新しい種類のリアルタイムエンドツーエンド物体検出器です。この研究は、後処理（非最大値抑制NMSなど）に依存しない、リアルタイム物体検出タスクにおける初めてのエンドツーエンドの検出器の実現に成功しました。

継続してRT-DETRの技術的特徴や実装の詳細について説明できます。


![v2-5975aeb1595401328102b943d91cca03_1440w](https://github.com/user-attachments/assets/68869de6-1d69-4442-b047-2c836207c7e9)
![v2-c5823cc73f2aa54751342d4e818d2493_1440w](https://github.com/user-attachments/assets/7ea09057-2753-4685-bd3f-f863d6fce791)

RT-DETRの主要な技術的特徴：

1. **後処理不要**：
* 既存のリアルタイム物体検出器と異なり、NMSなどの後処理が不要
* 推論の遅延を減少させ、検出速度を向上

2. **効率的なハイブリッドエンコーダ**：
* マルチスケール特徴の処理と計算効率の向上
* 内部スケール間の相互作用とクロススケール融合の分離
* 異なるスケールの特徴を効率的に処理

3. **IoU認識クエリ選択**：
* 学習過程でIoU制約を導入
* デコーダにより高品質な初期オブジェクトクエリを提供
* 検出性能の向上

4. **柔軟な推論速度調整**：
* デコーダ層の数を変更することで推論速度を調整可能
* 再学習不要
* 異なるリアルタイムシナリオへの適応が可能

5. **既存技術との比較**：
* 同規模のYOLOシリーズ検出器と比較して速度と精度で優位
* 同じバックボーンネットワークを使用した最先端のエンドツーエンド検出器を上回る性能も

6. **スケーラビリティ**：
* バックボーンネットワークとハイブリッドエンコーダの深さ乗数と幅乗数を調整可能
* 異なるパラメータ数と推論速度のバージョンを実現

RT-DETRはリアルタイム物体検出分野に新たなブレークスルーをもたらし、特にエンドツーエンド検出器のリアルタイム化において、将来の研究と応用に新しい方向性を提示しています。

さらに、RT-DETRv2バージョンがまもなくリリースされる予定とのことで、注目が集まっています。


モデル変換手順について説明します：

必要なリファレンスファイルを提供：

| ファイル名 | 説明 |
|------------|------|
| ax_rtdetr | AX650NベースのDEMO（NPU計算用） |
| rtdetr_config.json | pulsar2 build依存の設定ファイル |
| rtdetr_r18vd_5x_coco_objects365_from_paddle.onnx | エクスポート済みONNXモデル |
| rtdetr_r18.axmodel | pulsar2 buildでコンパイルされたNPUモデル |
| rtdetr_r18_msda.axmodel | 最適化版axmodel |
| ssd_horse.jpg | テスト画像 |
| avgpool_optimize.py | 必要な最適化ツール |

ONNXエクスポート：
RT-DETRが公開されてからかなりの時間が経過していますが、エッジ/エンド側のAIチップ企業で実際の展開例を公開している企業はありませんでした。これは、まだ深く研究する価値のあるTrickが存在することを示しています。

そこで、公式リポジトリに対して精度に影響を与えない範囲で若干の修正（RT-DETR Optimize）を行い、後続のボード展開をより便利にしました。

```powershell
git clone https://github.com/AXERA-TECH/RT-DETR.git
cd rtdetr_pytorch && mkdir weights 
wget https://github.com/lyuwenyu/storage/releases/download/v0.1/rtdetr_r18vd_5x_coco_objects365_from_paddle.pth -o ./weights
python tools/export_onnx.py --config configs/rtdetr/rtdetr_r18vd_6x_coco.yml --resume weights/rtdetr_r18vd_5x_coco_objects365_from_paddle.pth --file-name weights/rtdetr_r18vd_5x_coco_objects365_from_paddle.onnx --simplify --check
python avgpool_optimize.py
```

This error indicates another compatibility issue with the torchvision version. The `datapoints` module was added in a more recent version of torchvision (0.14.0+).

Looking at the RT-DETR code, it seems to be using newer torchvision features. Let's install a specific compatible version:

```bash
pip install torch==2.1.0 torchvision==0.16.0
```

If that doesn't work, we can modify the code to work with older versions. Open `/src/data/coco/coco_dataset.py` and locate these imports. You might need to replace the `datapoints` import with traditional torchvision transforms.

Here's how you can modify the file:

```python
# Find this line:
from torchvision import datapoints

# Replace it with:
import torchvision.transforms as transforms
```

You'll likely need to modify other parts of the code that use `datapoints`. If you'd like, share the content of `coco_dataset.py` and I can help you make the necessary adjustments to make it compatible with your torchvision version.



これらの操作により、rtdetr_r18vd_5x_coco_objects365_from_paddle.onnxモデルが生成されます。

また、**ハードウェアレベルでMultiScaleDeformableAttnをサポート**した、より最適化されたバージョンも提供しています。


![v2-5b387ba9707b34c4f23e8c2d7ec90765_1440w](https://github.com/user-attachments/assets/de50f9ad-1d66-4538-83ba-935d272c2501)

Pulsar2のコンパイルについて説明します：

Pulsar2は新世代のAIツールチェーンで、以下の4つの強力な機能を統合しています：
1. モデル変換
2. オフライン量子化
3. モデルコンパイル
4. ヘテロジニアススケジューリング

これらの機能により、ネットワークモデルの効率的な展開ニーズをさらに強化しています。

主な特徴：
* 第3世代・第4世代NPUアーキテクチャに対する深いカスタマイズ最適化
* 演算子とモデルのサポート能力と範囲の拡張
* Transformer構造のネットワークに対する良好なサポート

これら特徴により、効率的なモデル展開が可能になります。


![v2-6d6b66fab86bc73298b593df9d12718d_1440w](https://github.com/user-attachments/assets/c3856060-9ec4-4093-b290-592d40e44f2c)

これらの機能が統合され、グラフ最適化、オフライン量子化、コンパイル、分割機能を一括で実行できます。

重要なポイント：
* 処理時間は5分未満
* 前世代のツールチェーンと比較して、モデルコンパイル効率が桁違いに向上

この大幅な効率改善により、開発者の生産性が大きく向上し、より迅速なモデル展開が可能になっています。


```
qtang@gpux2:~/quick_start_example$ pulsar2 build --input rtdetr/rtdetr_r18vd_5x_coco_objects365_from_paddle.onnx 
--config rtdetr/detr_config.json --output_dir rtdetr/r18_test/ --npu_mode NPU3 --output_name rtdetr_r18_msda.axmodel
......
                                                   Quant Config Table
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳┓
┃ Input  ┃ Shape            ┃ Dataset Directory ┃ Data Format ┃ Tensor Format ┃ Mean            ┃ Std                  ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇┩
│ images │ [1, 3, 640, 640] │ images            │ Image       │ BGR           │ [0.0, 0.0, 0.0] │ [255.0, 255.0, 255.0]│
└────────┴──────────────────┴───────────────────┴─────────────┴┘
Transformer optimize level: 0
32 File(s) Loaded.
[11:26:20] AX Set Float Op Table Pass Running ...         Finished.
Get Outlier Progress: 100%|███████████████| 32/32 [00:41<00:00,  1.30s/it]
[11:27:02] AX Set MixPrecision Pass Running ...           Finished.
[11:27:02] AX Set LN Quant dtype Quant Pass Running ...   Finished.
[11:27:02] AX Topk Operation Format Pass Running ...      Finished.
[11:27:02] AX Refine Operation Config Pass Running ...    Finished.
[11:27:02] AX Reset Mul Config Pass Running ...           Finished.
[11:27:02] AX Tanh Operation Format Pass Running ...      Finished.
[11:27:02] AX Confused Op Refine Pass Running ...         Finished.
[11:27:02] AX Quantization Fusion Pass Running ...        Finished.
[11:27:02] AX Quantization Simplify Pass Running ...      Finished.
[11:27:02] AX Parameter Quantization Pass Running ...     Finished.
Calibration Progress(Phase 1): 100%|███████████| 32/32 [00:45<00:00,  1.43s/it]
Finished.
[11:27:50] AX Quantization Alignment Pass Running ...     Finished.
[11:27:50] AX Passive Parameter Quantization Running ...  Finished.
[11:27:50] AX Parameter Baking Pass Running ...           Finished.
[11:27:50] AX Refine Int Parameter Pass Running ...       Finished.
[11:27:50] AX Refine Weight Parameter Pass Running ...    Finished.
Network Quantization Finished.
quant.axmodel export success: rtdetr/r18_test/quant/quant_axmodel.onnx
===>export per layer debug_data(float data) to folder: rtdetr/r18_test/quant/debug/float
===>export input/output data to folder: rtdetr/r18_test/quant/debug/test_data_set_0
===>export input/output data to folder: rtdetr/r18_test/quant/debug/io
Building native ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Building native ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
2024-02-22 11:27:58.549 | INFO     | yamain.command.load_model:pre_process:586 - tensor: images, (1, 640, 640, 3), U8
2024-02-22 11:27:58.550 | INFO     | yamain.command.load_model:pre_process:586 - tensor: tensor:pre_norm_1, (1, 640, 640, 3), FP32
2024-02-22 11:27:59.002 | INFO     | yamain.command.build:compile_ptq_model:1012 - QuantAxModel macs: 30,743,859,200
2024-02-22 11:27:59.019 | INFO     | yamain.command.build:compile_ptq_model:1078 - subgraph [0], group: 0, type: GraphType.NPU
2024-02-22 11:27:59.071 | INFO     | yasched.test_onepass:test_onepass_ir:2967 - schedule npu subgraph [0]
......
2024-02-22 11:28:12.157 | INFO     | yasched.test_onepass:results2model:2427 - clear job deps
2024-02-22 11:28:12.322 | INFO     | yasched.test_onepass:results2model:2436 - max_cycle = 8,368,117
2024-02-22 11:28:21.411 | INFO     | yamain.command.build:compile_ptq_model:1088 - fuse 1 subgraph(s)
```


コンパイル出力とボード展開について説明します：

コンパイル出力：
* 出力ファイルはoutputフォルダに保存
* `rtdetr_r18_msda.axmodel`がAX650N Demoボード上での実行に使用

ボード展開：

AX-Samples：
* オープンソースプロジェクトとして、一般的な深層学習オープンソースアルゴリズムの愛芯元智AI SoC上での実装例を提供
* コミュニティ開発者の迅速な評価と適用を支援

最新バージョンでサポートされているプラットフォーム：
* AX650シリーズ（AX650A、AX650N）
* AX620Eシリーズ（AX630C、AX620E）
* RT-DETRの参照コードも含む

これにより、開発者はRT-DETRを各プラットフォームに効率的に展開することができます。

性能結果とまとめ：

性能：
* AX650NでのRT-DETR実行時間：**10ms未満**
* リアルタイム実行要件を完全に満たす
* 後処理（post process）時間：**わずか0.17ms**
* **CPU負荷を大幅に削減**

結論：
Vision Transformerネットワークモデルの急速な発展により、より多くの興味深いAIアプリケーションがクラウドサービスからエッジデバイスやエンドデバイスに移行しつつあります。

すでに適用済みのTransformerベースの最先端モデル：
* 単眼深度推定（Depth Anything）
* オープンセット物体検出（OWL-ViT）
* 画像検索（CLIP）
* 画像修復（SAM+LaMa）
* DINOv2
* SegFormer
* EfficientViT
* DETR
* Swin Transformer

新年度にはより多くのエンドデバイスで優れたTransformerネットワークの展開が期待されます。

謝辞：
* RT-DETRの適用とDEMO開発：@折秋水
* Kimi Chat - より広い世界を見せ、RT-DETRの学習をサポート

著者の「圈圈虫」は、技術を愛する"中年おじさん"として、AXERAテクニカル交流グループへの参加を呼びかけています。グループには多くの業界専門家がオンラインで質問に答えており、AXera-Pi Pro（AX650N基盤）とAXera-Pi Zero（AX620Q基盤）の最新情報も提供されています。



