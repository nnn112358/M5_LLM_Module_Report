https://x.com/devemin/status/1863391008127615392

https://gist.github.com/ciniml/de14b22991c16fbe76558fe86eda8565

from:@devemin
```
まず wlx なんちゃらとデバイス名が変わるので、wlan0 と固定する。

vi /etc/udev/rules.d/70-persistent-net.rules
（修正は i キー、保存は :wq キー。）

SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="b8:27:eb:48:76:23", ATTR{type}=="1", NAME="wlan0"

address のところを "ip a" コマンドとかで MAC アドレスを調べ書き換える。
```
