# 目的

Module-LLM(ax630c)のNPUでYOLO11を動かすために、
YOLO11のオブジェクト認識、ポーズ認識、セグメンテーションのモデルをaxmodelへの変換を行います。

# 注意点
・UltralyticsのYOLO11は、デフォルトでonnx変換を行うとopset19になるのですが、pulsar2がopset19に対応していないので、onnxへ変換するときにはopsetを18以下のバージョンへ指定します。YOLO11のモデルはopset19を含んでいると、Pulsar2でaxモデルへ変換するときに、Splitのオペランドでエラーが発生します。<br>
<img src="https://github.com/user-attachments/assets/cb086375-6049-4f68-83bf-02ea5c56dd6f" width="500"><br>


・Pulsar2はver 3.2-patch1-temp-vlm以降のバージョンにします。ver 3.2でYOLO11の変換を行うと、Shapeの形状不一致のエラーが発生します。<br>
<img src="https://github.com/user-attachments/assets/a6c9e084-b394-4731-ab3a-cf86cb3d5554" width="500"><br>


## pulsar2のインストール

@qqc -sanが管理するGoogleDriveからax_pulsar2_3.2_patch1_temp_vlm.tar.gzをダウンロードしてきます。
<https://drive.google.com/drive/folders/10rfQIAm5ktjJ1bRMsHbUanbAplIn3ium>

dockerをインストールし、以下のコマンドでdockerを読み込みます。

```
sudo docker load -i ax_pulsar2_3.2_patch1_temp_vlm.tar.gz
```
Dockerイメージを確認します。
```
$ sudo docker image ls
REPOSITORY                  TAG             IMAGE ID       CREATED         SIZE
pulsar2                     3.2             9a6b9d26f6a1   2 months ago    2.58GB
pulsar2                     temp-58aa62e4   c6ccb211d0bc   4 weeks ago     2.58GB
```

Dockerを起動します。

```
$ sudo docker run -it --net host --rm -v $PWD:/data pulsar2:temp-58aa62e4
 ```

Dockerを終了します。
```
$ exit
 ```

## Ultralyticsのインストール

Pytorchをインストールした後に、Ultralytics をインストールします。
ここでは、CPU環境のPytorchをインストールしています。

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install ultralytics
```



## axモデルへの変換1

このリポジトリをダウンロードし、pythonスクリプトを実行します。

```
$ git clone https://github.com/nnn112358/ax_model_convert_YOLO11
$ cd ax_model_convert_YOLO11
```


datasetフォルダの下に、こちらから coco_1000.tarをダウンロードしてきて配置します。
[coco_1000.tar](https://drive.google.com/drive/folders/1pnbZ-iX6tEekjlsYhyjacK2Y02TVmLU1)


### オブジェクト認識モデル
オブジェクト認識モデルをUltralyticsからダウンロードして、モデルの最終段のカットを行います。<br>
YOLO11のm/s/nサイズをダウンロードします。

```
$ python yolo11_download.py
```
yolo11_download.py
``` yolo11_download.py
from ultralytics import YOLO
import os
os.chdir('./model')

# Load a model,Export to onnx with simplify
model = YOLO("yolo11n.pt")
model.info()
model.export(format='onnx', simplify=True,opset=17)
```

 yolo11_cut-onnx.py
```
$ python yolo11_cut-onnx.py
```

```yolo11_cut-onnx.py
import onnx
import os
def extract_onnx_model(input_path, output_path):
   input_names = ["images"]
   output_names = [
       "/model.23/Concat_output_0",
       "/model.23/Concat_1_output_0", 
       "/model.23/Concat_2_output_0"
   ]
   onnx.utils.extract_model(input_path, output_path, input_names, output_names)

# Usage
os.chdir('./model')
extract_onnx_model("yolo11n.onnx", "yolo11n-cut.onnx")

```

<img src="https://github.com/user-attachments/assets/2fda3d7e-709c-4f9b-94c1-8caa53b6ae37" width="300"><br>

### セグメンテーション認識モデル
セグメンテーション認識モデルをUltralyticsからダウンロードして、モデルの最終段のカットを行います。<br>
YOLO11-segのm/s/nサイズをダウンロードします。

```
$ python yolo11-seg_download.py
$ python yolo11-seg_cut-onnx.py
```
<img src="https://github.com/user-attachments/assets/d5d8fe37-71bf-489e-a41a-56fedca66dda" width="300"><br>

### ポーズ認識モデル

ポーズ認識モデルをUltralyticsからダウンロードして、モデルの最終段のカットを行います。<br>
YOLO11-poseのm/s/nサイズをダウンロードします。

```
$ python yolo11-pose_download.py
$ python yolo11-pose_cut-onnx.py
```
<img src="https://github.com/user-attachments/assets/2f6199f8-1b7b-478f-be3a-c0657044e22e" width="300"><br>


### 補足

モデルの最終段のカットを行う目的は、モデルをNPUで実行するために量子化を行うと整数精度の処理になり精度が低下するのですが、
モデルから最終段を削除し、最終段をCPUで演算することで浮動小数点精度で処理し、不必要な精度低下を防ぐためです。


https://x.com/qqc1989/status/1859293298877399322

## axモデルへの変換2

Pulsar2がインストールされている、Dockerを起動します。

```
$ sudo docker run -it --net host --rm -v $PWD:/data pulsar2:temp-58aa62e4
```

Pulsar2のbuildコマンドで、onnxモデルをModule-LLM(ax630c)のNPUに対応するaxモデルに変換します。

```
# pulsar2 build --input model/yolo11n-cut.onnx --output_dir output --config config/yolo11-config.json --target_hardware AX620E
# cp output/compiled.axmodel model/yolo11n.axmodel

# pulsar2 build --input model/yolo11n-pose-cut.onnx --output_dir output --config config/yolo11-pose_config.json --target_hardware AX620E
# cp output/compiled.axmodel model/yolo11n-pose.axmodel

# pulsar2 build --input model/yolo11n-seg-cut.onnx --output_dir output --config config/yolo11-seg_config.json --target_hardware AX620E
# cp output/compiled.axmodel model/yolo11n-seg.axmodel
```

モデルが生成できていることを確認します。<br>

```
$ ls model/*.axmodel
model/yolo11n-pose.axmodel  model/yolo11n.axmodel       model/yolo11s-seg.axmodel
model/yolo11n-seg.axmodel   model/yolo11s-pose.axmodel  model/yolo11s.axmodel
```



# 参考リンク
@nnn112358/M5_LLM_Module_Report
https://github.com/nnn112358/M5_LLM_Module_Report

pulsar2-docs
https://pulsar2-docs.readthedocs.io/en/latest/index.html
https://axera-pi-zero-docs-cn.readthedocs.io/zh-cn/latest/doc_guide_algorithm.html
