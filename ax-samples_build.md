## ax-samplesのビルド手順


### ax620q_bsp_sdkのダウンロードとパスの設定

```
git clone https://github.com/AXERA-TECH/ax620q_bsp_sdk.git
export ax_bsp=$PWD/ax620q_bsp_sdk/msp/out/arm64_glibc/
echo $ax_bsp
```

### ax-samplesの最新版(v0.7)のダウンロードと解凍
```
wget https://github.com/AXERA-TECH/ax-samples/archive/refs/tags/v0.7.zip
unzip ax-samples-0.7.zip
```

### OpenCVのダウンロードと解凍

```
cd ax-samples-0.7
mkdir -p ./3rdparty
wget https://github.com/AXERA-TECH/ax-samples/releases/download/v0.1/opencv-aarch64-linux-gnu-gcc-7.5.0.zip
unzip opencv-aarch64-linux-gnu-gcc-7.5.0.zip -d ./3rdparty
```


### aarch64のパッケージの導入とaarch64-linux-gnu.toolchain.cmakeファイルの作成
オフィシャルの手順ではaarch64-none-linux-gnu.toolchainをインストールするが、
Ubuntu22.04のaarch64-linux-gnuでもLLM Moduleで動くので、変更している。

```
$ sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```
../toolchains/aarch64-linux-gnu.toolchain.cmakeに以下のファイルを作成

```/toolchains/aarch64-linux-gnu.toolchain.cmake
# set cross-compiled system type, it's better not use the type which cmake cannot recognized.
SET (CMAKE_SYSTEM_NAME Linux)
SET (CMAKE_SYSTEM_PROCESSOR aarch64)

# aarch64-linux-gnu-gcc DO NOT need to be installed, so make sure aarch64-linux-gnu-gcc and aarch64-linux-gnu-g++ can be found in $PATH:
SET (CMAKE_C_COMPILER   "aarch64-linux-gnu-gcc")
SET (CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++")

# set searching rules for cross-compiler
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

参考

https://github.com/AXERA-TECH/ax-samples/blob/main/.github/workflows/build_630c_glibc.yaml




