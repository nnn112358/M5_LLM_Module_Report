** 爱芯通元NPUの高性能**、高精度、容易な展開という特性により、NPUベースのYOLOv9の適用をいち早く完了しました。
はじめに
本稿では以下の内容をご紹介します：

YOLOv9のONNXモデルのエクスポート方法
ONNXの組み込みツールを使用した最適化済み計算グラフの取得方法
Pulsar2ツールチェーンによる量子化とコンパイルを通じたAX650向けNPUモデルの生成方法
YOLOv9をコミュニティ開発ボード愛心派Pro上で効率的に実行する方法


YOLOv9は、YOLOv7研究チームが発表した最新の物体検出ネットワークで、YOLO（You Only Look Once）シリーズの最新イテレーションです。YOLOv9は、深層学習における情報ボトルネックの問題を解決し、様々なタスクにおけるモデルの精度とパラメータ効率を向上させることを目指して設計されています。

YOLOv9の主な特徴：

* **Programmable Gradient Information (PGI)**：
  * 可プログラム勾配情報という新しい補助監視フレームワークを導入
  * ネットワークの重みを更新する際の信頼性の高い勾配情報を生成
  * 補助可逆分岐を通じて深層ネットワークの深化による問題を解決
  * 目的関数の計算に完全な入力情報を提供

* **Generalized Efficient Layer Aggregation Network (GELAN)**：
  * 勾配経路計画に基づく新しい軽量ネットワークアーキテクチャ
  * 従来の畳み込み演算を使用
  * 深さ方向分離畳み込みベースの最先端手法よりも優れたパラメータ利用率を実現

* **高効率な性能**：
  * MS COCOデータセットの物体検出タスクで優れた性能を達成
  * これまでのリアルタイム物体検出手法をすべて上回る
  * 精度、パラメータ利用率、計算効率の面で顕著な優位性を示す
 
![v2-c9f5aabc2d9e33c4a3f6699a679109a4_1440w](https://github.com/user-attachments/assets/bac05b2e-1ff8-4958-a9cf-617c6adad618)

YOLOv9の追加的な主要特徴：

* **様々な規模のモデルに適用可能**：
  * PGIは軽量から大規模まで多様なモデルに適用可能
  * 完全な情報を取得可能
  * ゼロからの学習でも、大規模データセットで事前学習された最先端モデルと同等以上の性能を達成

* **改良されたネットワークアーキテクチャ**：
  * ダウンサンプリングモジュールの簡素化
  * アンカーレス予測ヘッドの最適化
  * これらの改良によりモデルの効率性と精度が向上

* **学習戦略**：
  * YOLOv7 AFの学習設定を踏襲
  * SGDオプティマイザーを使用して500エポックの学習
  * 線形ウォームアップと減衰戦略を学習過程で採用

* **データ拡張**：
  * HSV彩度・値の拡張
  * 平行移動拡張
  * スケール拡張
  * モザイク拡張
  * これらの技術によりモデルの汎化能力を向上

総じて、YOLOv9は革新的なPGIとGELANアーキテクチャ、および既存の学習戦略の改良を通じて、高効率かつ高精度な物体検出ソリューションを提供し、様々な規模のモデルと異なるアプリケーションシナリオに適用可能です。
![v2-64b42b1aabc227709143fd48a395236f_1440w](https://github.com/user-attachments/assets/1a2d4ab0-e7fb-408c-ba93-7abbe7e27dc5)
![v2-2a0b9b9e73f2aa04ce0d3568730f1643_1440w](https://github.com/user-attachments/assets/ce827a3b-d65d-4b22-b375-3b4a5bfbaeea)


模型取得について説明します：

実験を容易にするため、以下の必要なリファレンスファイルを提供しています：

| ファイル名 | 説明 |
|------------|------|
| ax_yolov9 | AX650NベースのDEMO、NPU計算用 |
| yolov9_config.json | pulsar2 buildが依存する設定ファイル |
| cut-onnx.py | 必要な最適化ツール |
| yolov9c.axmodel | pulsar2 buildでコンパイルされたNPUモデル |
| yolov9-c.onnx | エクスポートされたONNXモデル |
| yolov9-c-cut.onnx | pulsar2 buildが依存するONNXモデル |

これらのファイルにより、YOLOv9モデルの実装と実験を効率的に進めることができます。

モデルの変換手順について説明します：

1. ONNXモデルのエクスポート:
```text
git clone https://github.com/AXERA-TECH/yolov9.git
cd yolov9
pip install -r requirements.txt
wget https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt
python export.py --weights yolov9-c.pt --include onnx
onnxsim yolov9-c.onnx yolov9-c.onnx
```

この手順で`yolov9-c.onnx`モデルを取得できます。オリジナルのリポジトリに対して、精度に影響を与えない範囲で若干の修正を加え、後続のボード展開をより便利にしています。

2. モデル変換:
ONNXモデルの最適化：
**pulsar2**ツールチェーンで変換する前に、前のステップで取得した`yolov9-c.onnx`モデルに対して必要な計算グラフの最適化を行います。これにより、モデル展開の効率を向上させることができます。最適化後に`yolov9-c-cut.onnx`が生成されます。


```
import onnx
input_path = "yolov9-c.onnx"
output_path = "yolov9-c-cut.onnx"
input_names = ["images"]
output_names = ["/model.38/Concat_output_0", "/model.38/Concat_1_output_0", "/model.38/Concat_2_output_0"]
onnx.utils.extract_model(input_path, output_path, input_names, output_names)
```

![v2-fbb46894da6e15974e7df8dff61d8f47_1440w](https://github.com/user-attachments/assets/77d36e64-43cb-4d19-8e49-a436f1ae5229)
![v2-7e113a2b452295ad84d833b43631b334_1440w](https://github.com/user-attachments/assets/c8145580-0e3c-4c4a-a183-3d21a00057d5)
![v2-8699782263472a59659d27441ea309cb_1440w](https://github.com/user-attachments/assets/dc0ccc1b-27ea-4b66-80f8-897363666f60)

Pulsar2のコンパイルについて説明します：

**Pulsar2**は新世代のAIツールチェーンで、以下の4つの強力な機能を統合しています：
- モデル変換
- オフライン量子化
- モデルコンパイル
- ヘテロジニアススケジューリング

これらの機能により、ネットワークモデルの効率的な展開ニーズをさらに強化しています。

重要な特徴：
* 第3世代・第4世代NPUアーキテクチャに対する深いカスタマイズ最適化
* 演算子とモデルのサポート能力と範囲の拡張
* Transformer構造のネットワークに対する良好なサポート

これらの特徴により、効率的なモデル展開が可能になります。具体的なコンパイル手順や設定があれば、続けて説明できます。
![v2-6d6b66fab86bc73298b593df9d12718d_1440w](https://github.com/user-attachments/assets/cdb14786-7d77-42f7-bc11-d1ddf887495a)

モデルのコンパイルと展開プロセスについて詳しく説明します：

1. Pulsar2による一括処理
グラフ最適化、オフライン量子化、コンパイル、分割機能を一括で実行できます。
* 処理時間は5分未満
* 前世代のツールチェーンと比べて、モデルコンパイル効率が桁違いに向上
* Dockerベースのパルサー2ツールチェーン環境が前提

2. 必要なファイル：
* `yolov9_config.json` - モデル変換用設定ファイル
* `yolov9-c-cut.onnx` - 変換対象のONNXモデル
* `coco_1000.tar` - PTQ量子化用キャリブレーションデータセット

3. 設定ファイル（yolov9_config.json）の重要な修正点：
* `output_processors`の3つの`tensor_name`を修正
* 出力ノードの形状を変更：
```text
1*144*80*80 → 1*80*80*144
1*144*40*40 → 1*40*40*144
1*144*20*20 → 1*20*20*144
```

4. モデル変換コマンド：
```text
pulsar2 build --input yolov9-c-cut.onnx --config yolov9_config.json --output_dir output --output_name yolov9c.axmodel --npu_mode NPU3 
```

5. ボード展開：
AX-Samplesプロジェクトを使用：
* 愛芯元智のAI SoC上での一般的な深層学習オープンソースアルゴリズムの実装例を提供
* AX650シリーズ（AX650A、AX650N）、AX620Eシリーズ（AX630C、AX620E）のNPU例を含む
* YOLOv9の参照コードも含まれる

6. 実行に必要なファイル：
* `ax_yolov9` - AX650NベースのYOLOv9 DEMO（NPU計算用）
* `yolov9c.axmodel` - Pulsar2で変換生成したaxmodel
* `ssd_horse.jpg` - テスト画像

これらの手順により、効率的なモデルの変換と展開が可能になります。

実行結果の解析と性能評価について説明します：

実行コマンドと結果：
```text
/opt/test # ./ax_yolov9 -i ssd_horse.jpg -m yolov9c.axmodel
```

検出結果：
* 処理時間：26.22ms平均
* 検出数：6個の物体
* 検出詳細：
  * 馬：94%の確度
  * 犬：88%の確度
  * 人物：87%と79%の確度で2人
  * トラック：76%の確度
  * ベンチ：47%の確度

性能評価：
* AX650NでのYOLOv9-C実行時間：26ms（38 FPS）
* リアルタイム実行要件を完全に満たす
* YOLOv9-Cの計算量：177 GOPs
* AX650Nの演算能力利用率：60%以上

結論：
* この展開方式はAX650A、AX650N、AX630C、AX620Qすべてに適用可能

謝辞：
* YOLOv9の適用とDEMO開発：@折秋水
* YOLOv9のONNXモデルエクスポート：@三木君
* Kimi Chat - より広い世界を見せ、YOLOv9の学習をサポート

投稿者の圈圈虫は、技術を愛する"中年おじさん"として自己紹介し、詳細についてはAXERA技術交流グループへの参加を推奨しています。AXera-Pi Pro（AX650N基盤）とAXera-Pi Zero（AX620Q基盤）の最新情報もフォローできます。


この一連の質問と回答を整理します：

評価とプロセスについての質問：
* "本当に速いですね、すごい！"
* "このような速度はすごい"
* "YOLOv8同等クラスのモデル（Sなど）との推論速度の比較はありますか？"

技術的な質問：
* "ここでの量子化はPTQやQATのような量子化ですか？"
* 回答: "単純なPTQです"
* フォローアップ: "通常のもので十分ということですか？効率や性能の比較はありますか？"

チップと会社に関する質問：
* "このチップはいくらですか？"
* 回答: "同じクラスの他のチップと比べて若干優位です"
* "アイシンのエンジニアですか？"
* 回答: "考えてみてください"

開発スピードへの感想：
* "YOLOv9を見たばかりなのにすぐに実装されていて、とても効率的ですね"
* "とても迅速ですね"

これらのコメントは、実装の速度と性能の両方に対して高い評価を示しています。


