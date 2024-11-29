
## pulsar2でのモデル変換

### 概要
https://pulsar2-docs.readthedocs.io/en/latest/user_guides_advanced/advanced_build_guides.html
を翻訳した。

pulsar2 build は、モデルのグラフ最適化、量子化、コンパイルなどの操作に使用されます。その操作の図は以下の通りです：
![image](https://github.com/user-attachments/assets/81ef5cf2-af8e-4d98-ac17-5c9329fbdcd4)


pulsar2 buildは、入力モデル（model.onnx）、PTQキャリブレーションデータ（calibration.tar）、設定ファイル（config.json）を使用して、出力モデル（axmodel）を生成します。
pulsar2 buildのコマンドラインパラメータは、設定ファイル内の特定の対応する部分を上書きし、pulsar2 buildが上書きされた設定ファイルを出力するようにします。設定ファイルの詳細については、《設定ファイルの詳細》をご参照ください。





6.2. モデルコンパイルの詳細説明
このセクションでは、pulsar2 buildコマンドの完全な使用方法について説明します。
pulsar2 build -hで詳細なコマンドラインパラメータを表示できます：

```

基本的なパラメータ：
* `--config`：設定ファイルのパス（json/yaml/toml/prototxt形式をサポート）
* `--input`：入力モデルファイルのパス（必須）
* `--output_dir`：axmodelの出力ディレクトリ（必須）
* `--output_name`：出力axmodelの名前を変更（デフォルト：compiled.axmodel）
* `--work_dir`：一時データの出力ディレクトリ
* `--model_type`：入力モデルタイプ（ONNX、QuantAxModel、QuantONNX）
* `--target_hardware`：ターゲットハードウェア（AX650、AX620E、M76H）
* `--npu_mode`：NPUモード（AX650の場合：NPU1/NPU2/NPU3、AX620Eの場合：NPU1/NPU2）

ONNX最適化関連：
* `--onnx_opt.disable_onnx_optimization`：ONNX最適化を無効化
* `--onnx_opt.enable_onnxsim`：ONNXシンプリファイを有効化
* `--onnx_opt.model_check`：モデルチェックを有効化

量子化関連：
* `--quant.calibration_method`：量子化キャリブレーション方法（MinMax、Percentile、MSE）
* `--quant.precision_analysis`：量子化精度分析を有効化
* `--quant.highest_mix_precision`：最高混合精度量子化を有効化
* `--quant.enable_smooth_quant`：conv 1x1用のスムース量子化戦略を有効化

コンパイラ関連：
* `--compiler.static_batch_sizes`：静的バッチサイズ
* `--compiler.max_dynamic_batch_size`：最大動的バッチサイズ
* `--compiler.check`：コンパイラチェックレベル（0：チェックなし、1：シミュレート、2：シミュレートとチェック）
* `--compiler.debug`：コンパイラデバッグレベル

これらのパラメータを適切に設定することで、モデルの最適化、量子化、およびコンパイルプロセスをカスタマイズすることができます。
```
ユーザーはパラメータ仕様に従ってjson/yaml/toml/prototxt形式の設定ファイルを作成し、コマンドラインパラメータ--configを通じて設定ファイルを指定することができます。
一部のコンパイルパラメータはコマンドライン入力をサポートしており、設定ファイルよりも優先順位が高くなります。サポートされているコマンドラインコンパイルパラメータを表示するにはpulsar2 build -hを使用してください。例えば、コマンドラインパラメータ--quant.calibration_methodは、QuantConfig構造体のcalibration_methodフィールドの設定と同等です。

**6.2.1. パラメータの詳細説明**
**pulsar2 buildのパラメータ説明**

**--config**
* データ型：string
* 必須：はい
* 説明：設定ファイルのパス、`json/yaml/toml/prototxt`形式をサポート、構造については《設定ファイルの詳細説明》を参照

**--work_dir**
* データ型：string
* 必須：いいえ
* デフォルト値：output_dirと同じ
* 説明：中間結果の出力ディレクトリ

**--input**
* データ型：string
* 必須：はい
* 説明：モデル入力パス

**--output_dir**
* データ型：string
* 必須：はい
* 説明：コンパイル結果の出力ディレクトリ、コンパイルされたモデルはcompiled.axmodelという名前になります

**--model_type**
* データ型：enum
* 必須：いいえ
* デフォルト値：ONNX
* 説明：入力モデルタイプ、サポートされる列挙型：`ONNX`、`QuantAxModel`、`QuantONNX`

**--target_hardware**
* データ型：enum
* 必須：いいえ
* デフォルト値：AX650
* 説明：モデルコンパイル用のターゲットSoCプラットフォームタイプ、`AX650`、`AX620E`、`M76H`をサポート

**--npu_mode**
* データ型：enum
* 必須：いいえ
* デフォルト値：NPU1
* 説明：モデルコンパイルモード
   * SoCプラットフォームが`AX650`の場合、サポートされる列挙型：`NPU1`、`NPU2`、`NPU3`
   * SoCプラットフォームが`AX620E`の場合、サポートされる列挙型：`NPU1`、`NPU2`
 
**--compiler**
BuildConfigのメンバー変数compiler

* static_batch_sizes
   * データ型：整数のリスト
   * 必須：いいえ
   * デフォルト値：0
   * 説明：ユーザーが提供するバッチの組み合わせに従ってコンパイルを実行。このバッチモデルのセットに基づき、実行時に任意のbatch_size入力の効率的な推論をサポート可能。詳細は《静的マルチバッチモード》を参照

* max_dynamic_batch_size
   * データ型：int
   * 必須：いいえ
   * デフォルト値：0
   * 説明：NPUが効率的に実行でき、max_dynamic_batch_size以下のバッチモデルの組み合わせを自動的に導出。このバッチモデルのセットに基づき、実行時に任意のbatch_size入力の効率的な推論をサポート可能。詳細は《動的マルチバッチモード》を参照

* ddr_bw_limit
   * データ型：float
   * 必須：いいえ
   * デフォルト値：0
   * 説明：コンパイル時のエミュレーションDDRバンド幅制限をGB単位で設定

* disable_ir_fix
   * データ型：bool
   * 必須：いいえ
   * デフォルト値：false
   * 説明：マルチバッチコンパイル時のコンパイラのデフォルトReshape演算子属性修正動作を無効にするかどうか

* npu_perf
   * データ型：bool
   * 必須：いいえ
   * デフォルト値：false
   * 説明：NPUコンパイル時にデバッグファイルをエクスポート

* check
   * データ型：int
   * 必須：いいえ
   * デフォルト値：0
   * 説明：シミュレーションを通じてコンパイル結果の正確性をチェックするかどうか。0はチェックなし、1はコンパイル結果が正しく実行できるかチェック、2はモデルの出力データが正しいかチェック

* check_mode
   * データ型：enum
   * 必須：いいえ
   * デフォルト値：0
   * 説明：二分探索モード。CheckOutputは結果のみを二分探索。CheckPerLayerは層ごとに二分探索

* check_rtol
   * データ型：float
   * 必須：いいえ
   * デフォルト値：1e-5
   * 説明：--compiler.checkパラメータが1の時に有効。相対誤差パラメータ

* check_atol
   * データ型：float
   * 必須：いいえ
   * デフォルト値：0
   * 説明：--compiler.checkパラメータが1の時に有効。相対誤差パラメータ

* check_cosine_simularity
   * データ型：float
   * 必須：いいえ
   * デフォルト値：0.999
   * 説明：--compiler.checkパラメータが3の時のみ有効。テンソルのコサイン類似度チェックの閾値を指定

* check_tensor_black_list
   * データ型：文字列のリスト
   * 必須：いいえ
   * デフォルト値：[]
   * 説明：チェックに含まれないテンソルのリスト。正規表現マッチングをサポート

* input_sample_dir
   * データ型：string
   * 必須：いいえ
   * デフォルト値：空
   * 説明：コンパイラチェックに使用する入力データディレクトリを設定。指定しない場合、量子化キャリブレーションデータが優先的に使用される


6.3. マルチコアコンパイルの詳細説明
ユーザーは、pulsar2 buildの--npu_modeオプションを変更することで、NPUコンパイルモードを柔軟に設定し、計算能力を最大限に活用することができます。
6.3.1. NPUシングルコアモード
--npu_modeのデフォルト設定はNPU1で、これは1 NPUコアモードです。前の《モデルコンパイル》の章では、デフォルトのNPU1設定を使用して説明を行いました。
6.3.2. NPUデュアルコアモード
--npu_modeの設定をNPU2に変更すると、2 NPUコアモードになります。mobilenetv2モデルの変換を例にとると、設定ファイルは以下のように変更します：


6.4. マルチバッチコンパイルの詳細説明
pulsar2 buildは、モデルのbatch_sizeの設定をサポートしており、静的マルチバッチと動的マルチバッチコンパイルの2つのモードに分かれています。この2つのモードは相互に排他的です。この章ではAX650を例として使用します。
6.4.1. 静的マルチバッチモード
コンパイラはユーザーが提供するバッチの組み合わせに従ってコンパイルを行い、コマンドラインパラメータ--compiler.static_batch_sizesでの設定と設定ファイル内のcompiler.static_batch_sizesの変更という2つの方法をサポートしています。

静的マルチバッチコンパイルを設定した後、onnx inspect -m -n -tを通じてcompiled.axmodelを確認すると、入出力のshapeのバッチ次元はユーザーが指定した最大バッチになります。

バッチ間で重みデータが可能な限り再利用されるため、モデルサイズは各バッチを個別にコンパイルした場合のモデルサイズの合計よりも小さくなります。


mobilenetv2モデルを例にとると、元のモデル入力inputのshapeは[1, 224, 224, 3]ですが、static_batch_sizesを[1, 2, 4]として静的マルチバッチコンパイルを行うと、shapeは[4, 224, 224, 3]になります。

6.4.2. 動的マルチバッチモード
コンパイラは、NPUが効率的に実行でき、max_dynamic_batch_size以下のバッチモデルの組み合わせを自動的に導出します。このバッチモデルのセットに基づき、実行時に任意のbatch_size入力の効率的な推論をサポートすることができます。コマンドラインパラメータ--compiler.max_dynamic_batch_sizeでの設定と設定ファイル内のcompiler.max_dynamic_batch_sizeの変更という2つの方法をサポートしています。

コンパイラはバッチ1から開始し、2倍ずつ増加させてコンパイルを行います。バッチが設定されたmax_dynamic_batch_sizeより大きくなるか、現在のバッチの理論的推論効率が前のバッチより低くなった時点で停止します。

バッチ理論的推論効率：理論的推論時間 / batch_size
バッチ間で重みデータが可能な限り再利用されるため、モデルサイズは各バッチを個別にコンパイルした場合のモデルサイズの合計よりも小さくなります。


動的マルチバッチコンパイルを設定した後、onnx inspect -m -n -tを通じてcompiled.axmodelを確認すると、入出力のshapeのバッチ次元はmax_dynamic_batch_sizeになります。

mobilenetv2モデルを例にとると、元のモデル入力inputのshapeは[1, 224, 224, 3]ですが、max_dynamic_batch_sizeを4として動的マルチバッチコンパイルを行うと、shapeは[4, 224, 224, 3]になります。

実行時には、推論時にユーザーが設定した動的バッチサイズに基づいて、適切なバッチの組み合わせを見つけ、複数回の推論を実行します。

## Hint

モデルの理論的推論効率がバッチ数の増加に伴って向上し、コンパイル後にNPUサブグラフが1つだけ存在し、max_dynamic_batch_sizeが4に設定されている場合、コンパイルされたcompiled.axmodelには[1, 2, 4]の3つのバッチモデルが含まれます。
推論やシミュレーション時：

動的バッチ値が3に設定されている場合：

axengine inference frameworkとpulsar2 run emulatorは内部で「バッチ2 + バッチ1」の組み合わせでNPU推論またはシミュレーションを実行します。


動的バッチ値が9に設定されている場合：

axengine inference frameworkとpulsar2 run emulatorは内部で「バッチ4 + バッチ4 + バッチ1」の組み合わせで3回のNPU推論またはシミュレーションを実行します。



つまり、実行時には利用可能なバッチサイズを組み合わせて、要求された動的バッチサイズに最も効率的に対応する方法を自動的に選択します。




### リンク
pulsar2-docs<br>
https://pulsar2-docs.readthedocs.io/en/latest/index.html<br>
https://axera-pi-zero-docs-cn.readthedocs.io/zh-cn/latest/doc_guide_algorithm.html<br>

