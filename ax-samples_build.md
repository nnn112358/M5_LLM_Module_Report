# ax-samplesのビルド手順

### 目的
LLM_Moduleでmobilenetv2でのクラス分類やyoloでのオブジェクトを行うC++のプログラムをビルドする手順について説明する。


### ax-samplesの最新版のダウンロードと解凍
axera-techのax-samplesのリポジトリのファイルをダウンロードして解凍する。

```bash
$ git clone https://github.com/AXERA-TECH/ax-samples
```

### ax620q_bsp_sdkのダウンロードとパスの設定
次に、ビルドに必要な「ax620q_bsp_sdk」をダウンロードします。このSDKのパスを環境変数ax_bspに設定しておきます。


```bash
$ git clone https://github.com/AXERA-TECH/ax620q_bsp_sdk.git
$ export ax_bsp=$PWD/ax620q_bsp_sdk/msp/out/arm64_glibc/
$ echo $ax_bsp
```


### OpenCVのダウンロードと解凍
サンプルプログラムで使用するOpenCVも必要です。以下の手順でダウンロードし、サードパーティフォルダ（3rdparty）に展開します。

```bash
$ cd ax-samples
$ mkdir -p ./3rdparty
$ wget https://github.com/AXERA-TECH/ax-samples/releases/download/v0.1/opencv-aarch64-linux-gnu-gcc-7.5.0.zip
$ unzip opencv-aarch64-linux-gnu-gcc-7.5.0.zip -d ./3rdparty
```


### aarch64のパッケージの導入とaarch64-linux-gnu.toolchain.cmakeファイルの作成

ARMプロセッサ向けにビルドするために、aarch64用のコンパイラをインストールします。

オフィシャルの手順ではgcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnuをインストールしますが、
Ubuntu22.04のaptでインストールできるaarch64-linux-gnuでもビルドできるため、aarch64-linux-gnuを使用しました。
問題があれば、gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnuをインストールして置き換えることが必要です。

```
$ sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

以下の内容で../toolchains/aarch64-linux-gnu.toolchain.cmakeというファイルを作成します。このファイルは、CMakeでクロスコンパイルをする際の設定を記述したものです。

```cpp
SET (CMAKE_SYSTEM_NAME Linux)
SET (CMAKE_SYSTEM_PROCESSOR aarch64)

SET (CMAKE_C_COMPILER   "aarch64-linux-gnu-gcc")
SET (CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++")

SET (CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET (CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET (CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```



### ax-samplesのビルド

ビルド用のフォルダを作成し、ビルドの準備をします。
次に、実行ファイルをビルドします。並列処理でビルドを高速化するため、make -j8と指定します。

```bash
$ mkdir build
$ cd build
$ cmake -DCMAKE_TOOLCHAIN_FILE=../toolchains/aarch64-linux-gnu.toolchain.cmake -DBSP_MSP_DIR=${ax_bsp}/ -DAXERA_TARGET_CHIP=ax630c ..
$ make -j8
$ make install
```


./ax-samples/build/install/ax630c/のフォルダに実行ファイルが生成されました。

```
./ax-samples/build/install/ax630c/
├── ax_classification
├── ax_crowdcount
├── ax_depth_anything
├── ax_imgproc
├── ax_model_info
├── ax_rtdetr
├── ax_scrfd
├── ax_simcc_pose
├── ax_yolo11
├── ax_yolo11_pose
├── ax_yolo11_seg
├── ax_yolo_world
├── ax_yolo_world_open_vocabulary
├── ax_yolov10
├── ax_yolov10_u
├── ax_yolov5_face
├── ax_yolov5s
├── ax_yolov5s_seg
├── ax_yolov6
├── ax_yolov7
├── ax_yolov7_tiny_face
├── ax_yolov8
├── ax_yolov8_pose
├── ax_yolov8_seg
├── ax_yolov9
├── ax_yolov9_u
└── ax_yolox

```


参考

https://github.com/AXERA-TECH/ax-samples/blob/main/.github/workflows/build_630c_glibc.yaml




