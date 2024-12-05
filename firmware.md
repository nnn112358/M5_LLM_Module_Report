

LLM Module ファームウェアアップグレードガイド
https://docs.m5stack.com/ja/guide/llm/llm/image


Airpocketさんの言う通り、AXDLは
①axpファイルを読み込む
②ダウンロードボタン▶を押す（■になる）
③ダウンロードボタンを押しながらModuleLLMを接続する
https://x.com/mongonta555/status/1858107431412466097


AXDL の Settings ですが、このダイアログ画面を出した状態だと、Port のリストが更新されない仕様のようで。
LLM Module の電源ボタンを押しながら結線した直後に、AXDL の Settings ボタンをクリックすると、
ダイアログ画面の Port のリストに COM が見えてくると思います。
https://x.com/hirotakaster/status/1856666870717579607


1. AXDLを立ち上げて、書き込みイメージを読み込み
2. LLM moduleの電源ボタンを押しながらPC側のUSBと結線
3. PC側 AXDL の歯車アイコン(左から2番目)をそっこークリックして、LLM moduleの書き込みポートを設定
4. また 2 の手順でDLモードの瞬間にAXDL書き込み実行




```
root@m5stack-LLM:~# df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        7.8G  3.2G  4.6G  42% /
tmpfs            983M     0  983M   0% /dev/shm
tmpfs            394M  848K  393M   1% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
tmpfs            983M     0  983M   0% /tmp
/dev/mmcblk0p19   20G  1.8G   18G  10% /opt
/dev/mmcblk0p18  992M  8.0M  968M   1% /soc
/dev/mmcblk0p17  928K  236K  592K  29% /param
tmpfs            197M     0  197M   0% /run/user/0
root@m5stack-LLM:~# free
               total        used        free      shared  buff/cache   available
Mem:         2012408      125116     1630584         848      256708     1816504
Swap:              0           0           0

```


## M5_LLM_ubuntu22_04_20241115.axp
```
root@m5stack-LLM:/etc/samba# reboot
[FAILED] Failed unmounting /tmp.
[27535.044974] watchdog: watchdog0: watchdog did not stop!
[27535.312815] reboot: Restarting system
V0EUEURSE/TC:0 0 ax_huk_read:115 ax efuse EFUSE_BONDOPT_BLK:0x00000000, EFUSE_SPACE bit isn't set, cannot access expected blks
E/TC:0 0 tee_otp_get_hw_unique_key:225
Unique key is not fetched from the platform.


U-Boot 2020.04 (Nov 14 2024 - 17:40:03 +0800)

U-Boot code: 5C000400 -> 5C0FA5E8  BSS: -> 5C1245E0
Model: AXERA AX620E_emmc Board
DRAM:  Monitor len: 001241E0
Ram size: 7FFFF000
Ram top: C0000000
TLB table from bfff0000 to bfffe000
Reserving 1168k for U-Boot at: bfecb000
Reserving 66560k for malloc() at: bbdcb000
Reserving 152 Bytes for Board Info at: bbdcaf68
Reserving 392 Bytes for Global Data at: bbdcade0
Reserving 14400 Bytes for FDT at: bbdc75a0

RAM Configuration:
Bank #0: 40001000
DRAM:  2 GiB
New Stack Pointer is: bbdc7590
Relocation Offset is: 63ecac00
Relocating to bfecb000, new gd at bbdcade0, sp at bbdc7590
ax_adc_probe
No available THERMAL device
MMC:   pull up sd cmd&data
mmc@1B40000: 0, mmc@104E0000: 1
Loading Environment from MMC... selecting mode MMC legacy (freq : 0 MHz)
selecting mode MMC legacy (freq : 25 MHz)
set_emmc_boot_mode_after_dl: storage_sel:0 , boot_type: 1
set_emmc_boot_mode_after_dl: 1800, Not in emmc boot mode, do not need to set ext_csd regs
trying mode MMC High Speed (52MHz) width 8 (at 52 MHz)
selecting mode MMC High Speed (52MHz) (freq : 52 MHz)
get_part_info part: env, bootargs not found in env, will use default
OK
enter designware_i2c_probe
initr_display:video fail probe
reading splash logo image++ ...
load logo image addr = 0xbc000000
ax_bootlogo_show inLogoFmt: FMT_BMP
ax_bootlogo_show bmp info: [800, 480, 24, 54]
In:    serial
Out:   serial
Err:   serial
From slota boot
Saving Environment to MMC... Writing to MMC(0)... OK
Current chip type: AX630C_CHIP
Current board type: AX630C_DEMO_LP4_V1_0
boot_reason:0x4
wdt0 reset
boot_mode->magic = 0x12345678
boot_mode->dl_channel = 0
boot_mode->storage_sel = 0
boot_mode->boot_type = 1
Sysdump started, dump_reason: 4
addr = 0x480f0000  size = 0x3000
memory_addr = 0x40000000
emmc  memory dumping ...
boot_reason = 0x4 reason_mask = 0x0
selecting mode MMC legacy (freq : 0 MHz)
Card did not respond to voltage select!
mmc_init: -95, time 24
no sd card
enter normal boot mode
boot_info_data.mode = 7
Net:
Warning: ethernet@0x104C0000 (eth0) using random MAC address - 5a:f8:b5:7a:3f:47
eth0: ethernet@0x104C0000
Hit any key to stop autoboot:  0
Setting bus to 4
enter do_axera_boot
reading kernel image ...
reading dtb image ...
header_info.blk_num=21, isize=5924096, osize=11841544, tile_cnt=12, last_tile_size=427248
header_info.blk_num=1, isize=22016, osize=142568, tile_cnt=2, last_tile_size=13808
boot cmd is :booti 0x40200000 - 0x40001000
## Flattened Device Tree blob at 40001000
   Booting using the fdt blob at 0x40001000
   Using Device Tree in place at 0000000040001000, end 0000000040026ce7

Starting kernel ...

[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
[    0.000000] Linux version 4.19.125 (nihao@nihao-z690) (gcc version 9.2.1 20191025 (GNU Toolchain for the A-profile Architecture 9.2-2019.12 (arm-9.10))) #1 SMP PREEMPT Thu Nov 14 17:40:17 CST 2024
[    0.000000] Machine model: axera,ax620e
[    0.000000] Memory limited to 2048MB
[    0.000000] earlycon: uart8250 at MMIO32 0x0000000004880000 (options '')
[    0.000000] bootconsole [uart8250] enabled
[    5.090361] rc.local[2013]: rx unmodified, ignoring
[    5.120899] rc.local[2013]: no pause parameters changed, aborting
[    5.155410] rc.local[2028]: run auto_load_all_drv.sh start
[    6.268220] rc.local[2028]: run auto_load_all_drv.sh end
[    6.291515] rc.local[2342]: run npu_set_bw_limiter.sh start
[    6.320846] rc.local[2342]: already register bw limit for NPU
[    6.350740] rc.local[2342]: this chip type is AX630C_CHIP
[    6.380820] rc.local[2342]: run npu_set_bw_limiter.sh end
[    6.411981] rc.local[2349]: usb adb start
[    7.401107] rc.local[2349]: enable usb gadget adb
[    7.467249] rc.local[2385]: you can reboot, switch to system A
[    7.534303] rc.local[2389]: Starting ota check

Ubuntu 22.04 LTS m5stack-LLM ttyS0

m5stack-LLM login: root (automatic login)

Welcome to Ubuntu 22.04 LTS (GNU/Linux 4.19.125 aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Tue Aug 22 06:11:46 JST 2023 on ttyS0
````
