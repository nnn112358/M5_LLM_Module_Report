# M5_LLM_Module
<img src="https://github.com/user-attachments/assets/92a2667d-ed4e-4194-955a-eb18aa583dbc" width="300">
<br>

## NPUの使用メモリを確認する

https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/cmm_memory_change.md

```
cat /proc/ax_proc/mem_cmm_info
```


## Module-LLMへファイル転送を行うには
[Module-LLMへファイル転送を行うには](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/file_copy.md)


## ax-samplesのビルド手順
[ax-samplesのビルド手順](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/ax-samples_build.md)<br>

## YOLO11をModule-LLMのNPU用モデルへ変換する
[YOLO11をModule-LLMのNPU用モデルへ変換する](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/pulsar2/model_conv.md)<br>

## 起動音の消し方,Lチカの仕方,デバック基板のつなぎ方,I2Cについて
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/info_memo_241206.md

## axera-techのリポジトリ調査
[axera-techのリポジトリ調査](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/ax-sample_repo.md)<br>

## ncnnでのCPU推論ベンチマーク
[NCNNでのCPU推論ベンチマーク比較](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/benchmark.md)<br>

## PythonでのNPU推論とCPU推論の比較ベンチマーク
https://github.com/nnn112358/ax-classification_benchmark

## UART通信
[LLM ModuleとM5Stack CoreS3SEとの間でUART通信を行う](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/serial_com.md)<br>



<br>

## LLMのサンプルプログラム


## CPU温度の確認

CPU温度の確認  
CPU温度は、デバイスファイル"/sys/class/thermal/thermal_zone0/temp"で確認することができます。ただし、この値は1000で割る必要があります。  

```
# cat /sys/class/thermal/thermal_zone0/temp
47350
この場合は、CPU温度47.350℃を表します。
```


## 参考リンク
m5-docs:Module-LLM<br>
https://docs.m5stack.com/ja/module/Module-LLM<br>
Product Guide:Module-LLM<br>
https://docs.m5stack.com/zh_CN/guide/llm/llm/arduino<br>
Module-LLM arduino example<br>
https://github.com/m5stack/M5Module-LLM<br>
StackFlow<br>
https://github.com/m5stack/StackFlow<br>

pulsar2-docs<br>
https://pulsar2-docs.readthedocs.io/en/latest/index.html<br>
https://axera-pi-zero-docs-cn.readthedocs.io/zh-cn/latest/doc_guide_algorithm.html<br>

@AXERA-TECH/ax-llm<br>
https://github.com/AXERA-TECH/ax-llm<br>

@tokkyo/おなかすいたWiKi<br>
https://wiki.onakasuita.org/pukiwiki/?Module%20LLM<br>

@airpocket/M5Stack LLM ModuleをLinuxボードとして利用する際のFAQ/Tips<br>
https://elchika.com/article/0e41a4a7-eecc-471e-a259-4fc8d710c26a/<br>
@airpocket/M5Stack LLM ModuleでONNX モデルを変換して使うデモ<br>
https://elchika.com/article/f393da46-65bd-4f76-951c-d0e31dba2987/<br>

@Abandon-ht/ax-AI_develop_guide<br>
https://github.com/Abandon-ht/ax-AI_develop_guide<br>
How to export YOLOv8’s ONNX model;<br>
https://axera-pi-zero-docs-cn.readthedocs.io/en/latest/doc_guide_algorithm.html<br>

ksasao/TextAssistant.ino<br>
https://gist.github.com/ksasao/37425d3463013221e7fd0f9ae5ab1c62<br>
@ciniml/ cross compile modules for M5Stack Module LLM <br>
https://gist.github.com/ciniml/de14b22991c16fbe76558fe86eda8565<br>
M5Stack ModuleLLMでUSB-WiFiドングルを使用する。<br>
https://zenn.dev/mongonta/articles/35b37ee0bc057c<br>

sipeed/maixIV<br>
https://wiki.sipeed.com/hardware/zh/maixIV/m4ndock/axmodel-deploy.html<br>
https://dl.sipeed.com/shareURL/MaixIV/M4N-Dock<br>

maixHub axera-pi<br>
https://maixhub.com/model/zoo?name=yolo&sort=recently&platform=axera-pi<br>

爱芯元智AX650N部署yolov5s 自定义模型<br>
https://www.cnblogs.com/smallwxw/p/17836977.html<br>
https://github.com/derronqi/yolov8-face?tab=readme-ov-file<br>

[经验] 【爱芯派 Pro 开发板试用体验】人体姿态估计模型部署后期尝试<br>
https://bbs.elecfans.com/jishu_2408487_1_1.html<br>
