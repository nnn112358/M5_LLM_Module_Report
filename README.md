# M5_LLM_Module



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

```
root@m5stack-LLM:~# echo 100 > /sys/class/leds/R/brightness
root@m5stack-LLM:~# echo 100 > /sys/class/leds/G/brightness
root@m5stack-LLM:~# echo 100 > /sys/class/leds/B/brightness

```





