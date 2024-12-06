


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

## デバック基板のつなぎ方

<img src="https://github.com/user-attachments/assets/2fdaa79b-241d-4e46-b5c5-eaffe938967d" width="300">
<img src="https://github.com/user-attachments/assets/e5ae0bd0-fb4d-4603-b28a-8ca44e5deded" width="300">

1. 基板と外枠についている六角ネジを外します。
2. スピーカーを取り外します。スピーカは両面テープでとまっているのでゆっくり剥がします。
　　スピーカーの下にFFCコネクタがあることを確認します。
3. FFCとFFCコネクタを接続します。FFCコネクタを上に開けると、FFCを挿抜することができます。FFCを差し込み、FFCコネクタを横に倒して、固定てします。
4. スピーカーと外枠を元に戻して完了です。

## I2Cについて

こちらのXの投稿より、<br>
<img src="https://github.com/user-attachments/assets/3824a95b-849c-42f1-a66a-a5ed38a27480" width="500"><br>
https://x.com/HanxiaoM/status/1856908829411483666<br>

I2Cは、LLMモジュールの背面にジャンパー(Net Tile)が出ています。<br>
I2Cの上のパッドの右側がBUSの17pin、I2Cの下のパッドの右側がBUSの18pinでした。<br>
SCLの丸いパッドとSDLの丸いパッドもあるが、I2Cのパッド(BUS_SCL、BUS_SDL)とは繋がっていませんでした。<br>
<img src="https://github.com/user-attachments/assets/dfcd5124-b171-4463-ba3d-0a8a01611ea7" width="500"><br>
