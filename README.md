# M5_LLM_Module
<img src="https://github.com/user-attachments/assets/92a2667d-ed4e-4194-955a-eb18aa583dbc" width="300">

<br>

## ax-samplesのビルド手順
[ax-samplesのビルド手順](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/ax-samples_build.md)<br>

## axera-techのリポジトリ調査
[axera-techのリポジトリ調査](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/axera_sample_repo.md)<br>

## ncnnでのCPU推論ベンチマーク
[NCNNでのCPU推論ベンチマーク比較](https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/benchmark.md)<br>

<br>


## 起動音の消し方

startup-scriptのtinyplayの行をコメントアウトします。

```
root@m5stack-LLM:~# vi /usr/local/m5stack/startup-script.sh

#!/bin/sh
. /etc/profile
insmod /lib/modules/4.19.125/led-class.ko
insmod /lib/modules/4.19.125/leds-lp55xx-common.ko
insmod /lib/modules/4.19.125/leds-lp5562.ko
sleep 0.1

echo 0  > /sys/class/leds/R/brightness
echo 50 > /sys/class/leds/G/brightness
echo 0  > /sys/class/leds/B/brightness
#tinyplay -D0 -d1 /usr/local/m5stack/logo.wav > /dev/null 2>&1 &
```

## Lチカの仕方

LEDのデバイスファイルが /sys/class/leds/ あります。
brightness の値は、通常0から255の範囲で指定します。値が 0 だと消灯、最大の 255 で最も明るく点灯します。

<img src="https://github.com/user-attachments/assets/03ad22df-3e69-4205-bc25-951f82b6a979" width="300">

```
root@m5stack-LLM:~# echo 100 > /sys/class/leds/R/brightness
root@m5stack-LLM:~# echo 100 > /sys/class/leds/G/brightness
root@m5stack-LLM:~# echo 100 > /sys/class/leds/B/brightness

```

## デバック基盤のつなぎ方


<img src="https://github.com/user-attachments/assets/2fdaa79b-241d-4e46-b5c5-eaffe938967d" width="300">
<img src="https://github.com/user-attachments/assets/e5ae0bd0-fb4d-4603-b28a-8ca44e5deded" width="300">


①基板と外枠とのネジを外す
②スピーカーを外す。その下にFFCコネクタがある。
③FFCコネクタを上に立てて、FFC刺す。その後コネクタを寝かす。
④スピーカーと外枠を戻す


## I2Cについて

こちらのXの投稿より、<br>
<img src="https://github.com/user-attachments/assets/3824a95b-849c-42f1-a66a-a5ed38a27480" width="500"><br>
https://x.com/HanxiaoM/status/1856908829411483666<br>

I2Cは、LLMモジュールの背面にジャンパーが出ています。<br>
I2Cの上のパッドの右側がBUSの17pin、I2Cの下のパッドの右側がBUSの18pinでした。<br>
SCLの丸いパッドとSDLの丸いパッドもあるが、I2Cのパッド(BUS_SCL、BUS_SDL)とは繋がっていませんでした。<br>
<img src="https://github.com/user-attachments/assets/dfcd5124-b171-4463-ba3d-0a8a01611ea7" width="500"><br>

## 参考リンク
m5-docs:Module-LLM<br>
https://docs.m5stack.com/ja/module/Module-LLM<br>
Product Guide:Module-LLM<br>
https://docs.m5stack.com/zh_CN/guide/llm/llm/arduino<br>
Module-LLM arduino example<br>
https://github.com/m5stack/M5Module-LLM<br>

pulsar2-docs<br>
https://pulsar2-docs.readthedocs.io/en/latest/index.html<br>

@AXERA-TECH/ax-llm<br>
https://github.com/AXERA-TECH/ax-llm<br>

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
