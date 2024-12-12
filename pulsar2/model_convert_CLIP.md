CLIPの背景と登場の意義について説明します：

写真整理の課題：
* "元気いっぱいの中秋節と国慎節8日間の連休"で1000枚以上の写真が生成
* 目的の写真（例：**金髪の女性**など）を見つけることが困難
* 正確なテキストベースの画像検索方法が必要

従来のCV（Computer Vision）モデルの限界：
* 監視学習方式による限定的なカテゴリーの学習
* 厳格な監督学習による汎化性と実用性の制限
* 学習時に見ていない視覚"概念"には追加のアノテーションデータが必要


![v2-a7cc6808055b3f0e9605fd3fbacc633c_1440w](https://github.com/user-attachments/assets/31a3726a-3df2-405c-a420-573ff7337238)

CLIPモデルの登場：
* 2021年初頭にOpenAIが発表
* zero-shotの視覚分類モデル
* Contrastive Language–Image Pre-trainingの略
* ファインチューニング無しでも下流タスクで優れた転移効果

CLIPの驚くべき性能：
* ImageNetでファインチューニングせずに、ImageNetで学習済みのResNet50と同等の性能
* 30以上のデータセットでテスト（OCR、動作検出、座標特定など）

従来の深層学習CVの課題：
1. データセットのアノテーションが労働集約的で高コスト
2. 単一タスクに特化し、新タスクへの転移が困難
3. 汎化能力が限定的

これらの課題に対して、CLIPは"万物認識"の可能性を提供する画期的なモデルとして注目されています。

![v2-c136510643074efcd12c73b80c23f709_1440w](https://github.com/user-attachments/assets/4fec5acb-2b8f-42f9-97ad-5b3b2cf91af6)
CLIPの推論プロセス（Zero-Shot）について説明します：

推論の仕組み：
1. 与えられた画像に対して、事前学習済みネットワークを用いて分類を行う
2. 作者が巧妙な"多肢選択"方式を考案

具体的な処理フロー：
1. 複数の分類ラベル（例：cat, dog, bird）を準備
2. テキストエンコーダーを使用してラベルをベクトル表現に変換
3. 各ラベルと画像間のコサイン類似度を計算
4. 類似度が最も高いラベルを予測結果として出力

この手法により、事前に定義されていないカテゴリーでも柔軟な分類が可能になります。

![v2-fe43a1d033f8c1e82b33718b46893c7d_1440w](https://github.com/user-attachments/assets/35c8f48d-121c-4271-af0d-f61ece43ce1d)

![v2-6a8463e7d967a6b6af650e69f3d06755_1440w](https://github.com/user-attachments/assets/3db5a1e1-95ac-457e-b2fc-42d3d256c29c)
CLIPの性能評価について説明します：

論文で公開された結果は非常に印象的で、CLIPは特に以下の点で優れています：

1. 強力なZero-Shot転移能力：
* ImageNetの各種分類タスクにおいて
* ImageNetのアノテーションデータによる学習なしで
* ResNetの監視学習と同等の分類性能を達成

2. 優れた特性：
* より優れた汎化性能
* より高い頑健性

このことは、CLIPが従来の監視学習ベースのアプローチを超える可能性を示しています。画像認識タスクにおいて、より柔軟で効率的なソリューションを提供できることを示唆しています。

具体的な性能データや比較結果があれば、それらも共有できます。

https://link.zhihu.com/?target=https%3A//github.com/AXERA-TECH/CLIP-ONNX-AX650-CPP

上板デモについての説明：

簡単なCLIP体験のため、GitHubで対応するDEMOと関連する事前コンパイル済みNPUモデルを公開：
AXERA-TECH/CLIP-AX650-CPP
github.com/AXERA-TECH/CLIP-ONNX-AX650-CPP

提供DEMOパッケージの内容：

| ファイル名 | 説明 |
|------------|------|
| main | DEMO実行プログラム |
| image_encoder.axmodel | 画像エンコーダモデル（AX650N NPU用） |
| image_encoder.onnx | 画像エンコーダモデル（CPU用） |
| images | テスト画像セット |
| text_encoder.onnx | テキストエンコーダモデル |
| text.txt | テキスト入力シーケンス |
| vocab.txt | テキスト語彙集 |
| feature_matmul.onnx | 特徴比較モデル |

処理時間統計：
CLIP画像エンコーダモデルには、より高精度なViT-Bベースのバックボーンを採用

バックボーンの仕様：
| 項目 | 仕様 |
|------|------|
| モデル | ViT-B/32 |
| 入力サイズ | 1,3,224,224 |
| パラメータ数 | 86M |
| 計算量 | 4.4G MACs |

単独実行の処理時間分析については、具体的なデータがあれば追加できます。

処理時間の統計分析：

CLIPの画像エンコーダモデル仕様：
| 項目 | 仕様 |
|------|------|
| バックボーン | ViT-B/32 |
| 入力サイズ | 1,3,224,224 |
| パラメータ数 | 86M |
| 計算量 | 4.4G MACs |

単独実行の性能結果：
```text
root@maixbox:~/qtang/CLIP# /opt/bin/ax_run_model -m image_encoder.axmodel -w 3 -r 10
 Run AxModel:
       model: image_encoder.axmodel
        type: NPU3
        vnpu: Disable
    affinity: 0b001
      repeat: 10
      warmup: 3
       batch: 1
 pulsar2 ver: 1.8-patch1 6fa8d395
  engine ver: [Axera version]: libax_engine.so V1.27.0_P3_20230627143603 Jun 27 2023 14:58:22 JK 1.1.0
    tool ver: 1.0.0
    cmm size: 93238580 Bytes
  ------------------------------------------------------
  min =   4.158 ms   max =   4.220 ms   avg =   4.198 ms
  ------------------------------------------------------
```

性能分析：
* AX650NのNPU上での画像エンコーダの実行速度：238画像/秒
* 1000枚の写真の特徴抽出にわずか**4.2秒**で完了可能

テスト1：
5枚の画像を使用してCLIPの効果を簡単にデモンストレーション予定

![v2-f707980fc3a272f5a98f3729107d1883_1440w](https://github.com/user-attachments/assets/26c55694-74ef-45a2-bde5-664074ee5aba)

AXERA-TECH/CLIP-AX650-CPPの事前コンパイルDEMOの使用方法を説明します：

使用方法：
```text
root@maixbox:~/qtang/CLIP# ./main
usage: ./main --ienc=string --tenc=string --dec=string --image=string --text=string --vocab=string --language=int [options] ...
options:
      --ienc        エンコーダモデル(onnxモデルまたはaxmodel)
      --tenc        テキストエンコーダモデル(onnxモデルまたはaxmodel)
  -d, --dec         デコーダモデル(onnx)
  -i, --image       画像ファイルまたはフォルダ(jpg pngなど)
  -t, --text        テキストまたはtxtファイル
  -v, --vocab       語彙パス
  -l, --language    言語選択、0:英語 1:中国語
  -?, --help        このメッセージを表示
```

テスト結果例：

1. "pretty girl"での検索：
```text
テキストエンコード時間：0.186011秒
画像エンコード時間：0.0112854秒〜0.0109678秒
行列積計算時間：0.000777559秒

結果：Crystal.jpeg が最も高いスコア(0.88)を示す
```

2. "a cartoon human with blond hair"での検索：
```text
結果：Asuna.jpg が最も高いスコア(0.92)を示す
```

3. "girl black hair"での検索：
```text
結果が一部のみ表示(0.05 for Asuna.jpg)
```

各テストケースで、異なるテキストプロンプトに対する画像とのマッチング度合いが数値で示されており、CLIPモデルの柔軟な画像検索能力を実証しています。

![v2-4a983c94637fbc85eba3331ea7b0d6e0_1440w](https://github.com/user-attachments/assets/ec56db2c-ad19-4ff0-973e-94db1daa9f94)

批量テスト結果の分析：

実行ログから得られる重要な性能指標：
* 特徴マッチング（"matmul Inference"）の処理時間：＜0.0008秒
* 1000枚の画像から対応するテキストに最も一致する画像を検索するのに1ミリ秒未満

テスト2の比較：
AX650N上のCLIP DEMOパイプラインにおける画像エンコーダモデルの比較：
* CPUでの実行時の**処理時間**と**CPU負荷**
* NPUでの実行時の**処理時間**と**CPU負荷**

これらの結果は、NPUの使用が処理時間とCPU負荷の両面で大きな改善をもたらすことを示唆しています。
![v2-6486edeb39e16b69c37c9f88acc37c3b_1440w](https://github.com/user-attachments/assets/ae43449a-5956-47da-b6dc-9d0b154b56a7)
![v2-86b6fa270421c491af54ccde6a7682d3_1440w](https://github.com/user-attachments/assets/a58aaeea-fab0-4d6b-9be9-64da1ca1ce50)

以下は日本語訳です：

結びの言葉
Vision Transformer ネットワークモデルの急速な発展に伴い、ますます多くの興味深いAIアプリケーションが徐々にクラウドサービスからエッジデバイスとエンドデバイスへと移行していくでしょう。私たちは、Transformerネットワーク構造に基づく最先端の人気モデルの適応成果を継続的に共有していきます：

* 画像修復（SAM+LaMa）
* テキストによる画像検索（本稿）
* 単眼深度推定（開発中）
* YOLO終結者（開発中）

**謝辞**
* CLIPの適応およびデモ開発
@折秋水
* 李沐と読むシリーズ——CLIP
@暧暧内含光
* OpenAIの最新作CLIPをどう評価するか
@hzwer


はい、以下は中国語の投稿の直接的な日本語訳です：

周舒畅

CLIPは端末上で最もコストパフォーマンスの高いTransformerモデルと言えるでしょう。計算能力の要求が低く、応用範囲が広く、SAMなどと統合できます
2023-10-11 · 北京

LOGIC
周舒畅
CLIPそのものは1つのモデルではなく、テキストと画像を対応付ける方法です。モデルについては、CLIPの2つのエンコーダは交換可能で、OpenAIも時々更新しています
08-31 · 北京

圈圏虫
作者
周舒畅
大先生のご支援に感謝します。これからも頑張ります
2023-10-11 · 広東

momo
確かに素晴らしいですね。具身知能に発展できそうです
2023-10-11 · 広東

Cydiachen
AXボードは本当に素晴らしいです
2023-10-11 · 中国香港

maja
OpenVinoと比較したことはありますか？我々のテストではx86の普通のCPUで80ミリ秒でした（具体的な型番は忘れました）
2023-10-18 · 北京

圏圏虫
作者
していません
2023-10-19 · 広東

映水之境
虫叔の生産性は爆発的です
2023-10-12 · 江蘇

元峰
すごいです
