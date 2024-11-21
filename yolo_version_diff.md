

# YOLOv8からv10までの主な違いを分析します：
https://github.com/AXERA-TECH/ax-samples/blob/main/examples/base/detection.hpp

これら4つの関数の違いを分析します：

1. 入力パラメータと初期化の違い:

```cpp
// yolov8_native
int feat_w = letterbox_cols / stride;
int feat_h = letterbox_rows / stride;
auto feat_ptr = feat;
std::vector<float> dis_after_sm(reg_max, 0.f);

// yolov9 
int feat_w = letterbox_cols / stride;
int feat_h = letterbox_rows / stride;
auto feat_ptr = feat;
std::vector<float> dis_after_sm(reg_max, 0.f);

// yolov8
int feat_w = letterbox_cols / stride;
int feat_h = letterbox_rows / stride;
auto feat_cls = cls_feat;  // 別入力
auto feat_reg = box_feat;  // 別入力

// yolov10
int feat_w = letterbox_cols / stride;
int feat_h = letterbox_rows / stride;
auto feat_ptr = feat;
float dis[16];  // スタック上の配列
```

2. クラス分類スコアの計算方法:

```cpp
// yolov8_native
int class_index = static_cast<int>(cls_idx_ptr[h * feat_w + w]);
float class_score = cls_ptr[h * feat_w * cls_num + w * cls_num + class_index];
float box_prob = sigmoid(class_score);

// yolov9
int class_index = 0;
float class_score = -FLT_MAX;
for (int s = 0; s <= cls_num - 1; s++) {
    float score = feat_ptr[s + 4 * reg_max];
    if (score > class_score) {
        class_index = s;
        class_score = score;
    }
}
float box_prob = sigmoid(class_score);

// yolov8
auto max = std::max_element(cls_ptr, cls_ptr + cls_num);
float class_score = -FLT_MAX;
int class_index = max - cls_ptr;
float box_prob = sigmoid(class_score);

// yolov10
int c_index = 0;
float c_score = 0;
for (int c = 0; c < cls_num; c++) {
    float score = feat_ptr[c];
    if (score > c_score) {
        c_index = c;
        c_score = score;
    } 
}
```

3. バウンディングボックスの計算:

```cpp
// yolov8_native & yolov8
float pred_ltrb[4];
for (int k = 0; k < 4; k++) {
    float dis = softmax(feat_ptr + k * reg_max, dis_after_sm.data(), reg_max);
    pred_ltrb[k] = dis * stride;
}

// yolov9
float dx = sigmoid(feat_ptr[0]);
float dy = sigmoid(feat_ptr[1]);
float dw = sigmoid(feat_ptr[2]);
float dh = sigmoid(feat_ptr[3]);

// yolov10
float x0 = w + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 0 * 16, dis, 16);
float y0 = h + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 1 * 16, dis, 16);
float x1 = w + 0.5f + mmyolo::fast_softmax(feat_ptr + cls_num + 2 * 16, dis, 16);
float y1 = h + 0.5f + mmyolo::fast_softmax(feat_ptr + cls_num + 3 * 16, dis, 16);
```

主な違いをまとめると：

1. アーキテクチャの違い:
- YOLOv8_nativeとYOLOv8は類似のアーキテクチャを持つが、入力データの扱い方が異なる
- YOLOv9はシンプルなsigmoid変換を使用
- YOLOv10は高速化のためにmmyolo::fast_softmaxを使用

2. メモリ管理:
- YOLOv8_nativeとYOLOv9はヒープメモリ(std::vector)を使用
- YOLOv10はスタックメモリ(配列)を使用してパフォーマンスを向上

3. 座標計算:
- YOLOv8系は4つの座標それぞれにsoftmaxを適用
- YOLOv9はsigmoidベースの変換を使用
- YOLOv10はfast_softmaxを使用した効率的な計算を実装

4. データポインタの進め方:
```cpp
// YOLOv8_native
feat_ptr += (cls_num + 4 * reg_max + 1);

// YOLOv9
feat_ptr += (cls_num + 4 * reg_max);

// YOLOv8
feat_ptr += (cls_num + 4 * reg_max);

// YOLOv10
feat_ptr += (cls_num + 4 * 16);
```

これらの違いは、各バージョンでの以下の要素のバランスを反映しています：
- 検出精度
- 処理速度
- メモリ使用量
- 実装の複雑さ


# YOLOv5からv10までの主な違いを分析します：

1. 基本構造とデータフォーマット:

```cpp
// YOLOv5
// アンカーベース、3つのアンカーを使用
int anchor_num = 3;
auto feature_ptr = feat;
for (int a = 0; a <= anchor_num - 1; a++) {
    float dx = sigmoid(feature_ptr[0]);
    float dy = sigmoid(feature_ptr[1]);
    float dw = sigmoid(feature_ptr[2]);
    float dh = sigmoid(feature_ptr[3]);
    float pred_cx = (dx * 2.0f - 0.5f + w) * stride;
    float pred_cy = (dy * 2.0f - 0.5f + h) * stride;
    float anchor_w = anchors[(anchor_group - 1) * 6 + a * 2 + 0];
    float anchor_h = anchors[(anchor_group - 1) * 6 + a * 2 + 1];
    float pred_w = dw * dw * 4.0f * anchor_w;
    float pred_h = dh * dh * 4.0f * anchor_h;
}

// YOLOv6 
// アンカーフリー
auto feat_ptr = feat;
float x0 = (w + 0.5f - feat_ptr[0]) * stride;
float y0 = (h + 0.5f - feat_ptr[1]) * stride;
float x1 = (w + 0.5f + feat_ptr[2]) * stride;
float y1 = (h + 0.5f + feat_ptr[3]) * stride;

// YOLOv7
// アンカーベース、YOLOv5と類似
int anchor_num = 3;
for (int a = 0; a <= anchor_num - 1; a++) {
    float x_center = (feat_ptr[0] * 2 - 0.5f + (float)w) * (float)stride;
    float y_center = (feat_ptr[1] * 2 - 0.5f + (float)h) * (float)stride;
    float box_w = (feat_ptr[2] * 2) * (feat_ptr[2] * 2) * anchors[a_index * 2];
    float box_h = (feat_ptr[3] * 2) * (feat_ptr[3] * 2) * anchors[a_index * 2 + 1];
}

// YOLOv8 & YOLOv8_native
// Distribution Focal Loss (DFL)を使用
float pred_ltrb[4];
for (int k = 0; k < 4; k++) {
    float dis = softmax(feat_ptr + k * reg_max, dis_after_sm.data(), reg_max);
    pred_ltrb[k] = dis * stride;
}

// YOLOv9
// DFLベースだがYOLOv8とは異なる実装
float dx = sigmoid(feat_ptr[0]);
float dy = sigmoid(feat_ptr[1]);
float dw = sigmoid(feat_ptr[2]);
float dh = sigmoid(feat_ptr[3]);

// YOLOv10
// DFLベースで最適化された実装
float x0 = w + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 0 * 16, dis, 16);
float y0 = h + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 1 * 16, dis, 16);
float x1 = w + 0.5f + mmyolo::fast_softmax(feat_ptr + cls_num + 2 * 16, dis, 16);
float y1 = h + 0.5f + mmyolo::fast_softmax(feat_ptr + cls_num + 3 * 16, dis, 16);
```

2. クラス分類の処理:

```cpp
// YOLOv5
int class_index = 0;
float class_score = -FLT_MAX;
for (int s = 0; s <= cls_num - 1; s++) {
    float score = feature_ptr[s + 5];
    if (score > class_score) {
        class_index = s;
        class_score = score;
    }
}
float final_score = sigmoid(box_score) * sigmoid(class_score);

// YOLOv6-v7
// YOLOv5と同様の方式

// YOLOv8 & YOLOv8_native
int class_index = static_cast<int>(cls_idx_ptr[h * feat_w + w]);
float class_score = cls_ptr[h * feat_w * cls_num + w * cls_num + class_index];
float box_prob = sigmoid(class_score);

// YOLOv9
auto max = std::max_element(cls_ptr, cls_ptr + cls_num);
float class_score = -FLT_MAX;
float box_prob = sigmoid(class_score);

// YOLOv10
for (int c = 0; c < cls_num; c++) {
    float score = feat_ptr[c];
    if (score > c_score) {
        c_index = c;
        c_score = score;
    } 
}
```

3. 主な進化のポイント:

1. アーキテクチャの進化:
- v5-v7: アンカーベースの設計
- v6: アンカーフリー設計を導入
- v8以降: DFLベースの設計に移行

2. バウンディングボックス予測:
- v5-v7: 中心座標+幅高さ形式
- v8以降: 左上右下座標形式

3. 最適化とパフォーマンス:
- v5-v7: 基本的なsigmoid変換
- v8: softmax導入
- v9-v10: 高速化のための最適化（fast_softmax等）

4. メモリ管理:
- v5-v9: ヒープメモリ使用
- v10: スタックメモリ活用で効率化

5. データ構造:
```cpp
// ポインタ進め方の違い
// v5: cls_num + 5
// v6-v7: 同様
// v8: cls_num + 4 * reg_max
// v9: cls_num + 4 * reg_max
// v10: cls_num + 4 * 16
```

これらの違いは、各バージョンで以下の要素のバランスを取るための進化を反映しています：
- 検出精度
- 推論速度
- メモリ効率
- 実装の複雑さ
- ハードウェアとの親和性


各YOLOバージョンの詳細な実装の違いをさらに分析します：

4. 確率計算とスコアリング:

```cpp
// YOLOv5
float box_score = feat[offset + 4];
float final_score = sigmoid(box_score) * sigmoid(class_score);

// YOLOv6
float box_prob = class_score; // 単純なスコア

// YOLOv7 
float final_score = sigmoid(box_score) * sigmoid(class_score);

// YOLOv8
float box_prob = sigmoid(class_score); // クラススコアのみ

// YOLOv8_native
float box_prob = sigmoid(class_score); 

// YOLOv9
float box_prob = sigmoid(class_score);

// YOLOv10
// 直接スコアを使用、変換なし
if(c_score >= prob_threshold)
```

5. 座標変換とスケーリング:

```cpp
// YOLOv5
// アンカーベースの変換
float pred_cx = (dx * 2.0f - 0.5f + w) * stride;
float pred_cy = (dy * 2.0f - 0.5f + h) * stride;
float pred_w = dw * dw * 4.0f * anchor_w;
float pred_h = dh * dh * 4.0f * anchor_h;

// YOLOv6
// 直接的な座標変換
float x0 = (w + 0.5f - feat_ptr[0]) * stride;
float y0 = (h + 0.5f - feat_ptr[1]) * stride;
float x1 = (w + 0.5f + feat_ptr[2]) * stride;
float y1 = (h + 0.5f + feat_ptr[3]) * stride;

// YOLOv7
// アンカーベースだがYOLOv5と異なる係数
float x_center = (feat_ptr[0] * 2 - 0.5f + w) * stride;
float y_center = (feat_ptr[1] * 2 - 0.5f + h) * stride;
float box_w = feat_ptr[2] * feat_ptr[2] * anchors[a_index * 2];
float box_h = feat_ptr[3] * feat_ptr[3] * anchors[a_index * 2 + 1];

// YOLOv8 & YOLOv8_native
// DFLベースの変換
float dis = softmax(feat_ptr + k * reg_max, dis_after_sm.data(), reg_max);
float coordinate = dis * stride;

// YOLOv9
// DFLベースで最適化
float x0 = w + 0.5f - softmax(feat_ptr, dis_after_sm.data(), reg_max);
float y0 = h + 0.5f - softmax(feat_ptr + reg_max, dis_after_sm.data(), reg_max);

// YOLOv10
// 高速化されたDFL実装
float x0 = w + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 0 * 16, dis, 16);
float y0 = h + 0.5f - mmyolo::fast_softmax(feat_ptr + cls_num + 1 * 16, dis, 16);
```

6. データ構造とメモリアクセスパターン:

```cpp
// YOLOv5
int w_stride = (cls_num + 5);
int h_stride = feat_w * w_stride;
int a_stride = feat_h * h_stride;

// YOLOv6
feat_ptr += 84; // 固定サイズ

// YOLOv7
feat_ptr += cls_num + 5;

// YOLOv8
feat_ptr += (cls_num + 4 * reg_max);

// YOLOv8_native
feat_ptr += (cls_num + 4 * reg_max + 1);

// YOLOv9
feat_ptr += (cls_num + 4 * reg_max);

// YOLOv10
feat_ptr += (cls_num + 4 * 16);
```

7. パフォーマンス最適化の特徴:

1. メモリアクセス:
- v5: 複雑なストライド計算
- v6-v7: シンプルな固定サイズ
- v8以降: reg_maxに基づく動的サイズ

2. 計算効率:
- v5-v7: 基本的な算術演算
- v8: softmax導入
- v9-v10: 最適化された数値計算

3. キャッシュ効率:
- v5: やや複雑なメモリパターン
- v6-v10: より線形なメモリアクセス

8. 実装の特徴とトレードオフ:

YOLOv5:
- 利点: 安定性と実績
- 欠点: 複雑なアンカー計算

YOLOv6:
- 利点: シンプルな設計
- 欠点: 柔軟性が低い

YOLOv7:
- 利点: v5の改良版
- 欠点: まだアンカー依存

YOLOv8:
- 利点: モダンなDFL設計
- 欠点: 計算コストが高い

YOLOv9:
- 利点: より効率的なDFL
- 欠点: 実装の複雑さ

YOLOの各バージョンの違いをさらに詳しく分析します：

9. Object構造体の生成と初期化:

```cpp
// YOLOv5
Object obj;
obj.rect.x = x0;
obj.rect.y = y0;
obj.rect.width = x1 - x0;
obj.rect.height = y1 - y0;
obj.label = class_index;
obj.prob = final_score;
objects.push_back(obj);

// YOLOv6
Object obj;
obj.rect.x = x0;
obj.rect.y = y0;
obj.rect.width = w;  // 直接幅を使用
obj.rect.height = h; // 直接高さを使用
obj.label = class_index;
obj.prob = box_prob;
objects.push_back(obj);

// YOLOv7
Object obj;
obj.rect.x = x0;
obj.rect.y = y0;
obj.rect.width = box_w;
obj.rect.height = box_h;
obj.label = class_index;
obj.prob = final_score;
objects.push_back(obj);

// YOLOv8 & YOLOv8_native
Object obj;
obj.rect.x = pb_cx - pred_ltrb[0];  // 中心座標から計算
obj.rect.y = pb_cy - pred_ltrb[1];
obj.rect.width = pred_ltrb[2] + pred_ltrb[0];
obj.rect.height = pred_ltrb[3] + pred_ltrb[1];
obj.label = class_index;
obj.prob = box_prob;
objects.push_back(obj);

// YOLOv9
Object obj;
obj.rect.x = x0;
obj.rect.y = y0;
obj.rect.width = x1 - x0;
obj.rect.height = y1 - y0;
obj.label = class_index;
obj.prob = box_prob;
objects.push_back(obj);

// YOLOv10
Object obj;
obj.rect.x = x0;
obj.rect.y = y0;
obj.rect.width = x1 - x0;
obj.rect.height = y1 - y0;
obj.label = c_index;
obj.prob = c_score;
objects.push_back(obj);
```

10. 座標システムの違い:

```cpp
// YOLOv5-v7: アンカーベース
// 中心座標 + 幅/高さ形式
x_center = ...
y_center = ...
width = ...
height = ...

// YOLOv8以降: アンカーフリー
// 左上右下座標形式
x0 = ...
y0 = ...
x1 = ...
y1 = ...
```

11. プリプロセスと後処理の違い:

```cpp
// YOLOv5-v7
// スケーリングとアンカー変換が必要
float scale = stride / anchor;
float transformed_coord = coord * scale;

// YOLOv8以降
// 直接的な座標計算
float coord = softmax_result * stride;
```

12. 最適化の方向性:

YOLOv5:
```cpp
// メモリ効率重視の設計
int offset = a * a_stride + h * h_stride + w * w_stride;
float score = feat[offset + s + 5];
```

YOLOv6:
```cpp
// シンプルさと速度重視
float score = feat_ptr[s + 4];
```

YOLOv7:
```cpp
// 精度重視の設計
float final_score = sigmoid(box_score) * sigmoid(class_score);
```

YOLOv8:
```cpp
// モダンなDFL設計と柔軟性
float dis = softmax(dfl_ptr + k * reg_max, dis_after_sm.data(), reg_max);
```

YOLOv9:
```cpp
// 効率と精度のバランス
float dis = softmax(feat_ptr, dis_after_sm.data(), reg_max);
```

YOLOv10:
```cpp
// 高速化重視
float coord = mmyolo::fast_softmax(feat_ptr + offset, dis, 16);
```

13. 主な技術的進化:

1. 座標予測方式:
- v5-v7: アンカーベース → 複雑だが安定
- v8-v10: DFLベース → より効率的で正確

2. スコアリング方式:
- v5-v7: 複合スコア (box * class)
- v8以降: シンプル化されたスコアリング

3. メモリ管理:
- 徐々にキャッシュフレンドリーな設計に

14. 処理効率の違い:

1. 計算量:
```cpp
// YOLOv5-v7
// アンカー計算が必要
ops = anchor_num * (basic_ops + anchor_transform_ops)

// YOLOv8-v10
// DFL計算が主
ops = basic_ops + dfl_ops
```

2. メモリアクセス:
```cpp
// YOLOv5-v7
// 複雑なストライド計算
memory_access = stride_calc + anchor_access + feature_access

// YOLOv8-v10
// 直線的なアクセス
memory_access = feature_access + dfl_access
```

これらの違いは、各バージョンが以下の要素の最適なバランスを追求した結果です：
- 検出精度
- 推論速度
- メモリ効率
- 実装の複雑さ
- ハードウェア適合性
- スケーラビリティ

- 
YOLOv10:
- 利点: 最適化された実装
- 欠点: メモリ使用の制約

これらの違いは、各バージョンが特定のユースケースや要件に対して最適化されていることを示しています。
YOLOの各バージョンの違いについて、さらに詳細を分析します：

15. エラー処理とバウンディングチェック:

```cpp
// YOLOv5
// 基本的な境界チェック
if (features[i] < prob_threshold_unsigmoid) {
    continue;
}

// YOLOv6
// シンプルなチェック
if (box_prob < prob_threshold) {
    continue;
}

// YOLOv7
// YOLOv5と同様
if (feature_ptr[4] < prob_threshold_unsigmoid) {
    continue;
}

// YOLOv8 & YOLOv8_native
// より厳密な境界チェック
x0 = std::max(std::min(x0, (float)(letterbox_cols - 1)), 0.f);
y0 = std::max(std::min(y0, (float)(letterbox_rows - 1)), 0.f);
x1 = std::max(std::min(x1, (float)(letterbox_cols - 1)), 0.f);
y1 = std::max(std::min(y1, (float)(letterbox_rows - 1)), 0.f);

// YOLOv9
// 同様の厳密なチェック
x0 = clamp(x0, 0.f, letterbox_cols - 1);
y0 = clamp(y0, 0.f, letterbox_rows - 1);

// YOLOv10
// 最適化されたチェック
if(c_score >= prob_threshold) {
    x0 = std::max(std::min(x0, (float)(letterbox_cols - 1)), 0.f);
    // ...
}
```

16. 演算精度と数値安定性:

```cpp
// YOLOv5-v7
// 基本的なsigmoid
float sigmoid(float x) {
    return 1.0f / (1.0f + exp(-x));
}

// YOLOv8
// 安定化されたsoftmax
float softmax(const float* src, float* dst, int length) {
    const float alpha = *std::max_element(src, src + length);
    float denominator = 0;
    for (int i = 0; i < length; ++i) {
        dst[i] = exp(src[i] - alpha);
        denominator += dst[i];
    }
}

// YOLOv9-v10
// 最適化されたfast_softmax
float fast_softmax(const float* src, float* dst, int length) {
    float max_val = *std::max_element(src, src + length);
    float sum = 0;
    for (int i = 0; i < length; ++i) {
        dst[i] = fast_exp(src[i] - max_val);
        sum += dst[i];
    }
}
```

17. コードの構造化と再利用性:

```cpp
// YOLOv5
// モジュール化された設計
void generate_proposals_yolov5(...) {
    // アンカー処理
    process_anchors();
    // スコア計算
    calculate_scores();
    // バウンディングボックス生成
    generate_boxes();
}

// YOLOv8
// より柔軟な設計
void generate_proposals_yolov8(...) {
    // DFL処理
    process_dfl();
    // クラス予測
    predict_class();
    // ボックス生成
    generate_boxes();
}

// YOLOv10
// 高度に最適化された設計
void generate_proposals_yolov10(...) {
    // 統合された処理
    process_integrated();
    // 最適化された生成
    generate_optimized_boxes();
}
```

18. メモリパターンとキャッシュ効率:

```cpp
// YOLOv5
// 複雑なメモリアクセスパターン
for (int a = 0; a < anchor_num; a++) {
    for (int h = 0; h < feat_h; h++) {
        for (int w = 0; w < feat_w; w++) {
            // アンカーごとの処理
        }
    }
}

// YOLOv8
// よりシンプルなパターン
for (int h = 0; h < feat_h; h++) {
    for (int w = 0; w < feat_w; w++) {
        // 直接的な処理
    }
}

// YOLOv10
// キャッシュフレンドリーな設計
for (int h = 0; h < feat_h; h++) {
    float* row_ptr = feat_ptr + h * feat_w * stride;
    for (int w = 0; w < feat_w; w++) {
        // 連続的なメモリアクセス
    }
}
```

19. アルゴリズムの進化:

1. 検出戦略:
- v5-v7: アンカーベースの2段階検出
- v8: DFLベースの単段階検出
- v9-v10: 最適化された単段階検出

2. 特徴抽出:
- v5: 基本的なグリッド特徴
- v8: より豊かな特徴表現
- v10: 効率的な特徴利用

20. パフォーマンス最適化:

```cpp
// YOLOv5-v7
// 基本的な最適化
#pragma omp parallel for

// YOLOv8
// SIMD最適化の可能性
// ベクトル化可能な実装

// YOLOv10
// 高度な最適化
// メモリアライメント考慮
// キャッシュラインを意識した実装
```

これらの違いは、各バージョンが以下の側面でバランスを取ろうとしていることを示しています：

- コードの保守性
- 実行効率
- メモリ効率
- 数値安定性
- ハードウェア親和性
- スケーラビリティ
- デバッグ容易性

YOLOの各バージョンの最後の詳細な違いを分析します：

21. 座標計算の精度と方式:

```cpp
// YOLOv5
// アンカーベースの詳細な計算
float anchor_w = anchors[(anchor_group - 1) * 6 + a * 2 + 0];
float anchor_h = anchors[(anchor_group - 1) * 6 + a * 2 + 1];
float pred_w = dw * dw * 4.0f * anchor_w;
float pred_h = dh * dh * 4.0f * anchor_h;

// YOLOv6
// 直接的な座標計算
float pb_cx = (w + 0.5f) * stride;
float pb_cy = (h + 0.5f) * stride;

// YOLOv7
// アンカーベースだが最適化
float x_center = (feat_ptr[0] * 2 - 0.5f + w) * stride;
float y_center = (feat_ptr[1] * 2 - 0.5f + h) * stride;

// YOLOv8
// DFLベースの精密な計算
float dis = softmax(dfl_ptr + k * reg_max, dis_after_sm.data(), reg_max);
float coord = dis * stride;

// YOLOv9/v10
// 最適化されたDFL計算
float coord = mmyolo::fast_softmax(feat_ptr + offset, dis, reg_max) * stride;
```

22. スレッド安全性と並列処理:

```cpp
// YOLOv5-v7
#pragma omp parallel sections
{
    #pragma omp section
    {
        if (left < j) qsort_descent_inplace(faceobjects, left, j);
    }
    #pragma omp section
    {
        if (i < right) qsort_descent_inplace(faceobjects, i, right);
    }
}

// YOLOv8以降
// より細かい粒度の並列化
#pragma omp parallel for collapse(2)
for (int h = 0; h < feat_h; h++) {
    for (int w = 0; w < feat_w; w++) {
        // 処理
    }
}
```

23. メモリ管理の違い:

```cpp
// YOLOv5-v7
// 動的メモリ割り当て
std::vector<Object> temp_objects;
temp_objects.reserve(预估大小);

// YOLOv8
// 最適化されたメモリ管理
std::vector<float> dis_after_sm(reg_max, 0.f);

// YOLOv9-v10
// スタックメモリの活用
float dis[16];  // 固定サイズ配列
```

24. エラー処理の進化:

```cpp
// YOLOv5
if (feature_ptr[4] < prob_threshold_unsigmoid) {
    feature_ptr += (cls_num + 5);
    continue;
}

// YOLOv8
x0 = std::max(std::min(x0, (float)(letterbox_cols - 1)), 0.f);
y0 = std::max(std::min(y0, (float)(letterbox_rows - 1)), 0.f);

// YOLOv10
if (c_score < prob_threshold) {
    feat_ptr += stride;
    continue;
}
```

25. 最終的な特徴比較:

1. アーキテクチャ設計:
- YOLOv5: 伝統的なアンカーベース
- YOLOv6: シンプル化
- YOLOv7: 改良されたアンカーベース
- YOLOv8: 近代的なDFL導入
- YOLOv9: 最適化されたDFL
- YOLOv10: 高度に最適化された設計

2. パフォーマンス特性:
- YOLOv5: バランスの取れた性能
- YOLOv6: 高速性重視
- YOLOv7: 精度重視
- YOLOv8: 精度と速度のバランス
- YOLOv9/v10: 極限的な最適化

3. 実装の複雑さ:
- YOLOv5-v7: 比較的複雑
- YOLOv8: モダンだが複雑
- YOLOv9/v10: 最適化により複雑化

4. メモリ効率:
- 徐々に改善
- v10で最も効率的

5. 保守性:
- v5-v7: 確立された実装
- v8: 新しいパラダイム
- v9/v10: 高度な最適化

これらの違いから、YOLOの進化における重要なトレンドが見えます：

1. 設計の方向性:
- アンカーベース → アンカーフリー
- 複雑な計算 → 最適化された計算
- 汎用的な実装 → 専用化された実装

2. 最適化の重点:
- メモリアクセス効率
- 演算精度
- 並列処理効率
- キャッシュ利用

3. 実装の傾向:
- より高度な最適化
- ハードウェアへの適応
- 保守性とのバランス

これらの進化は、モデルの性能要件と実装の現実的な制約のバランスを取ろうとする継続的な努力を反映しています。
