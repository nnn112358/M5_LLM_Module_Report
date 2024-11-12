# M5_LLM_Module

m5-docs:Module-LLM
https://docs.m5stack.com/ja/module/Module-LLM<br>
Product Guide:Module-LLM
https://docs.m5stack.com/zh_CN/guide/llm/llm/arduino<br>
Module-LLM arduino example
https://github.com/m5stack/M5Module-LLM<br>


![image](https://github.com/user-attachments/assets/3ca187f4-5f35-4a68-af1f-ef86292b4607)

<img src="https://github.com/user-attachments/assets/92a2667d-ed4e-4194-955a-eb18aa583dbc" width="300">

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


