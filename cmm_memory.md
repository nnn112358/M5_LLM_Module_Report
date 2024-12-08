Module-LLMのOSとNPUとのメモリ割当を変更する




```
root@m5stack-LLM:# cat /proc/ax_proc/mem_cmm_info

--------------------SDK VERSION-------------------
[Axera version]: ax_cmm V2.0.0_P7_20240513101106 May 13 2024 10:22:59 JK
+---PARTITION: Phys(0x80000000, 0x13FFFFFFF), Size=3145728KB(3072MB),    NAME="anonymous"
 nBlock(Max=0, Cur=13, New=0, Free=0)  nbytes(Max=0B(0KB,0MB), Cur=458752B(448KB,0MB), New=0B(0KB,0MB), Free=0B(0KB,0MB))  Block(Max=0B(0KB,0MB), Min=0B(0KB,0MB), Avg=0B(0KB,0MB))
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

SDKバージョン:ax_cmm V2.0.0_P7_20240513101106 (2024年5月13日ビルド)

メモリパーティション概要:
総メモリ容量: 3072MB (0x80000000 から 0x13FFFFFFF)
現在のブロック数: 13
使用中のメモリ: 448KB
残りメモリ: 約3071MB

メモリブロックの割り当て状況:
dma: 4KB
VPP関連: 28KB (CMD0: 24KB, CMD3: 4KB)
GDC関連: 16KB (CMD0: 12KB, CMD3: 4KB)
TDP関連: 136KB (CMD0: 132KB, CMD3: 4KB)
venc_ko: 132KB合計
jenc_ko: 132KB合計
```
