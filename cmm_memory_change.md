

## 目的

Module-LLMは、OSが使用するメモリが1GBと設定されています。
Pythonで大きなライブラリを使用する際などに、メモリが1GBでは不足する場合があります。

ここでは、
 - OSとNPUの使用メモリの割当を変更する。  
 - スワップメモリを使用する。  
の方法を紹介します。  

## 現在のメモリの確認

OSが使用するメモリはfreeコマンドで確認します。

```
root@m5stack-LLM:~# free -h
               total        used        free      shared  buff/cache   available
Mem:           958Mi       128Mi       640Mi       2.0Mi       189Mi       759Mi
Swap:             0B          0B          0B
```

NPUが使用するメモリは"/proc/ax_proc/mem_cmm_info"で確認します。

```
root@m5stack-LLM:~# cat /proc/ax_proc/mem_cmm_info
--------------------SDK VERSION-------------------
[Axera version]: ax_cmm V2.0.0_P7_20240513101106 May 13 2024 10:22:59 JK
+---PARTITION: Phys(0x80000000, 0x13FFFFFFF), Size=3145728KB(3072MB),    NAME="anonymous"
 nBlock(Max=13, Cur=13, New=13, Free=0)  nbytes(Max=458752B(448KB,0MB), Cur=458752B(448KB,0MB), New=458752B(448KB,0MB), Free=0B(0KB,0MB))  Block(Max=135168B(132KB,0MB), Min=4096B(4KB,0MB), Avg=30549B(29KB,0MB))
   |-Block: phys(0x80000000, 0x80000FFF), cache =non-cacheable, length=4KB(0MB),    name="dma"
   |-Block: phys(0x80001000, 0x80006FFF), cache =non-cacheable, length=24KB(0MB),    name="VPP_CMD0"
   |-Block: phys(0x80007000, 0x80007FFF), cache =non-cacheable, length=4KB(0MB),    name="VPP_CMD3"
   |-Block: phys(0x80008000, 0x80008FFF), cache =non-cacheable, length=4KB(0MB),    name="GDC_CMD3"
   |-Block: phys(0x80009000, 0x8000BFFF), cache =non-cacheable, length=12KB(0MB),    name="GDC_CMD0"
   |-Block: phys(0x8000C000, 0x8002CFFF), cache =non-cacheable, length=132KB(0MB),    name="TDP_CMD0"
   |-Block: phys(0x8002D000, 0x8002DFFF), cache =non-cacheable, length=4KB(0MB),    name="TDP_CMD3"
   |-Block: phys(0x8002E000, 0x8003DFFF), cache =non-cacheable, length=64KB(0MB),    name="venc_ko"
   |-Block: phys(0x8003E000, 0x8004DFFF), cache =non-cacheable, length=64KB(0MB),    name="venc_ko"
   |-Block: phys(0x8004E000, 0x8004EFFF), cache =non-cacheable, length=4KB(0MB),    name="venc_ko"
   |-Block: phys(0x8004F000, 0x8005EFFF), cache =non-cacheable, length=64KB(0MB),    name="jenc_ko"
   |-Block: phys(0x8005F000, 0x8006EFFF), cache =non-cacheable, length=64KB(0MB),    name="jenc_ko"
   |-Block: phys(0x8006F000, 0x8006FFFF), cache =non-cacheable, length=4KB(0MB),    name="jenc_ko"

---CMM_USE_INFO:
 total size=3145728KB(3072MB),used=448KB(0MB + 448KB),remain=3145280KB(3071MB + 576KB),partition_number=1,block_number=13
```

 - /proc/ax_proc/mem_cmm_infoの情報一覧
   
| 項目 | 値 |- |
|------|-----|- |
| SDKバージョン | ax_cmm V2.0.0_P7_20240513101106| (2024年5月13日ビルド)  |
| 総メモリ容量 | 3072MB  |(0x80000000 から 0x13FFFFFFF)|
| 現在のブロック数 | 13 |- |
| 使用中のメモリ | 448KB |- |
| 残りメモリ | 約3071MB |- |
| dma | 4KB | - |
| VPP関連 | 28KB | CMD0: 24KB, CMD3: 4KB |
| GDC関連 | 16KB | CMD0: 12KB, CMD3: 4KB |
| TDP関連 | 136KB | CMD0: 132KB, CMD3: 4KB |
| venc_ko | 132KB | - |
| jenc_ko | 132KB | - |


## OSとNPUのメモリの割当を変更する

## 1.ファームウェアの更新

OSとNPUのメモリの割当を変更するすることは、執筆時点(24/12/13)にM5Stakがリリースしているファームウェア(AX630C_emmc_arm64_k419_ubuntu_rootfs_V2.0.0_P7_20241024)では対応していません。
M5Stackの開発者の@HanxiaoM 氏がプレリリースで公開している、プレリリース版ファームウェア(M5_LLM_ubuntu22_04_20241115.axp)をします。  
LLM Module ファームウェアアップグレードガイドのファームウェアが正式にバージョンした場合には、正式版のファームウェアを使用してください。   
ファームウェアの書き換え手順は、LLM Module ファームウェアアップグレードガイドのページを参照してください。  

- プレリリース版ファームウェア  
https://x.com/HanxiaoM/status/1861386717640708412  

- LLM Module ファームウェアアップグレードガイド　　
https://docs.m5stack.com/ja/guide/llm/llm/image　　

<blockquote class="twitter-tweet"><p lang="en" dir="ltr"><a href="https://twitter.com/hashtag/M5StackLLM?src=hash&amp;ref_src=twsrc%5Etfw">#M5StackLLM</a> Pre-relrease of new <a href="https://twitter.com/hashtag/ModuleLLM?src=hash&amp;ref_src=twsrc%5Etfw">#ModuleLLM</a> image: <br>1. Add core-config utility (Support for adjusting the CMM by user)<br>2. Upgrade bootlodaer<br>3. Newer version of StackFlow<br>4. Merge opt space to user space<br>5. Other system level bug fix<a href="https://t.co/zB9ejOOsoK">https://t.co/zB9ejOOsoK</a></p>&mdash; HanxiaoMeow (@HanxiaoM) <a href="https://twitter.com/HanxiaoM/status/1861386717640708412?ref_src=twsrc%5Etfw">November 26, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## 2.core-configの実行

rootアカウントで、core-configコマンドを実行します。

```
root@m5stack-LLM:~# core-config
```

<img width="66%"  src="https://github.com/user-attachments/assets/8fc26119-3c7e-4c04-8676-0f3e112dfc1a">

" LLM Software Configuration Tool (core-config)"が起動します。
メニューで、"3 Advanced Options             Configure advanced settings"→"A4 MEM          Set Kernel MEM size, reboot to apply the configuration."と進むと、メモリのサイズを設定する画面に遷移します。

<img width="66%"  src="https://github.com/user-attachments/assets/27ae1c58-cef9-4155-92b7-3a5bef4a3717">

OS側に割り当てるメモリの量を打ち込みます。

<img width="66%"  src="https://github.com/user-attachments/assets/def0b235-75e2-466b-9551-c9b733878ea4">

再起動を選択すると、Ubuntuが再起動します。

<img width="66%"  src="https://github.com/user-attachments/assets/dc6a6260-97ba-4c22-9c4b-661705d724f5">

再起動後にfreeコマンドで、メモリ容量が変更されていることを確認します。

```
root@m5stack-LLM:~# free
               total        used        free      shared  buff/cache   available
Mem:         2012408      134176     1698352        2556      179880     1805984
Swap:              0           0           0
```

# スワップメモリ設定手順

## スワップメモリとは
スワップメモリは、コンピュータの物理メモリ（RAM）が不足した際に、ハードディスクやSSDの一部を一時的なメモリとして使用する仕組みです。
RAMが不足すると、あまり使用されていないデータがスワップ領域に移動され、必要な時にRAMに戻されます。これにより、実際のRAM容量以上のメモリ空間を確保できます。ただし、ハードディスクやSSDはRAMよりも処理速度が遅いため、頻繁なスワップの発生はシステムの性能低下を招く可能性があります。


## 1. 現在のスワップ状況確認

初期の設定では、スワップメモリは割り当てがされていません。

```bash
# 現在のスワップ使用状況を確認
root@m5stack-LLM:~# free -h
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       131Mi       1.6Gi       2.0Mi       176Mi       1.7Gi
Swap:             0B          0B          0B

# 詳細なスワップ情報を確認
swapon --show
```

## 2. スワップファイル作成

スワップファイルを作成は、Module-LLMのディスク割当の中で比較的、容量の大きい
/optフォルダの下で作成してみます。

```bash
root@m5stack-LLM:~# df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        7.8G  4.6G  3.3G  59% /
tmpfs            983M     0  983M   0% /dev/shm
tmpfs            394M  2.5M  391M   1% /run
tmpfs            5.0M  4.0K  5.0M   1% /run/lock
tmpfs            983M     0  983M   0% /tmp
/dev/mmcblk0p19   20G  2.8G   17G  15% /opt
/dev/mmcblk0p17  928K  236K  592K  29% /param
/dev/mmcblk0p18  992M  8.0M  968M   1% /soc
tmpfs            197M     0  197M   0% /run/user/0
```bash

まず、/opt/swapfileに1GBのスワップファイルを作成します。これにはfallocateコマンドを使用します。

```bash
# スワップファイルを作成（例：1GB）
sudo fallocate -l 1G /opt/swapfile
```

次に、セキュリティのためスワップファイルのアクセス権限を600（所有者のみ読み書き可能）に設定します。その後、mkswapコマンドでこのファイルをスワップ領域として初期化します。

```bash
# スワップファイルのパーミッションを設定
sudo chmod 600 /opt/swapfile

# スワップファイルとして初期化
sudo mkswap /opt/swapfile
```

最後に、swaponコマンドで作成したスワップ領域を即座に有効化し、システム再起動後も自動的にスワップが有効になるよう、/etc/fstabファイルにスワップファイルの設定を追加します。
これにより、システムの起動時に自動的にスワップ領域がマウントされるようになります。

```bash
# スワップを有効化
sudo swapon /opt/swapfile

# 起動時に自動的にスワップを有効化するための設定
sudo echo '/opt/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 3. スワップ設定の確認

free -hとswapon --showコマンドの実行結果は、システムのメモリとスワップの状況を示しています。
1GBのスワップファイルが/opt/swapfileに正しく設定され、認識されていることがわかります。
このコマンドの結果では、現在はメモリに十分な空きがあるため、スワップは使用されていない（0B）状態です。

```bash
# スワップが正常に追加されたか確認
root@m5stack-LLM:~# free -h
               total        used        free      shared  buff/cache   available
Mem:           1.9Gi       133Mi       1.6Gi       2.0Mi       233Mi       1.7Gi
Swap:          1.0Gi          0B       1.0Gi
root@m5stack-LLM:~# swapon --show
NAME          TYPE  SIZE USED PRIO
/opt/swapfile file 1024M   0B   -2
```



## 4.注意事項

1. スワップファイルはルートパーティション（/）に十分な空き容量がある場所に作成する必要があります
2. btrfsファイルシステムを使用している場合は、特別な設定が必要になる場合があります
3. 既存のスワップファイルを変更する場合は、まず古いスワップを無効化する必要があります：
   ```bash
   sudo swapoff /swapfile
   ```

## 5. パフォーマンス調整

スワップの使用頻度を調整するには、`/etc/sysctl.conf`にて`vm.swappiness`の値を設定します：

```bash
# 現在の値を確認
cat /proc/sys/vm/swappiness

# 値を変更（例：10に設定）
sudo echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

- 値の範囲：0～100
- 低い値：メモリを優先して使用
- 高い値：スワップを積極的に使用
- デフォルト：60
