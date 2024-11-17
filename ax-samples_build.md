# ax-samplesのビルド手順

### 目的
LLM_Moduleでmobilenetv2でのクラス分類やyoloでのオブジェクトを行うC++のプログラムをビルドする手順について説明する。


### ax-samplesの最新版(v0.7)のダウンロードと解凍
axera-techのax-samplesのリポジトリのファイルをダウンロードして解凍する。

```
wget https://github.com/AXERA-TECH/ax-samples/archive/refs/tags/v0.7.zip
unzip ax-samples-0.7.zip
```

### ax620q_bsp_sdkのダウンロードとパスの設定
axera-techのax620q_bsp_sdkのリポジトリのファイルをダウンロードして解凍する。
後述するax-samplesのビルド時にコマンドを短くするために、ax620q_bsp_sdkのパスを"ax_bsp"と命名する。 

```
git clone https://github.com/AXERA-TECH/ax620q_bsp_sdk.git
export ax_bsp=$PWD/ax620q_bsp_sdk/msp/out/arm64_glibc/
echo $ax_bsp
```


### OpenCVのダウンロードと解凍

```
cd ax-samples-0.7
mkdir -p ./3rdparty
wget https://github.com/AXERA-TECH/ax-samples/releases/download/v0.1/opencv-aarch64-linux-gnu-gcc-7.5.0.zip
unzip opencv-aarch64-linux-gnu-gcc-7.5.0.zip -d ./3rdparty
```


### aarch64のパッケージの導入とaarch64-linux-gnu.toolchain.cmakeファイルの作成
オフィシャルの手順ではgcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnuをインストールするが、
Ubuntu22.04のaptでインストールできるaarch64-linux-gnuでもビルドできるので、ここではaarch64-linux-gnuを使用する。
問題があれば、gcc-arm-9.2-2019.12-x86_64-aarch64-none-linux-gnuをインストールすること。

```
$ sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```
../toolchains/aarch64-linux-gnu.toolchain.cmakeに以下のファイルを作成

```/toolchains/aarch64-linux-gnu.toolchain.cmake
SET (CMAKE_SYSTEM_NAME Linux)
SET (CMAKE_SYSTEM_PROCESSOR aarch64)

SET (CMAKE_C_COMPILER   "aarch64-linux-gnu-gcc")
SET (CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++")

SET (CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET (CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET (CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```



### ax-samplesのビルド
```
mkdir build
cd build
cmake -DCMAKE_TOOLCHAIN_FILE=../toolchains/aarch64-linux-gnu.toolchain.cmake -DBSP_MSP_DIR=${ax_bsp}/ -DAXERA_TARGET_CHIP=ax630c ..
make -j8
make install
```

以下の実行ファイルが生成される。

```
./ax-samples-0.7/build/install/ax630c/
├── ax_classification
├── ax_crowdcount
├── ax_depth_anything
├── ax_imgproc
├── ax_model_info
├── ax_rtdetr
├── ax_scrfd
├── ax_simcc_pose
├── ax_yolo_world
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
└── ax_yolox
```


参考

https://github.com/AXERA-TECH/ax-samples/blob/main/.github/workflows/build_630c_glibc.yaml




