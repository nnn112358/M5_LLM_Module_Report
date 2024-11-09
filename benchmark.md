
## Result
![image](https://github.com/user-attachments/assets/bba13527-40cb-452f-ab71-6b98cc16fa62)


```
root@m5stack-LLM:~/benchmark_aarch64# ./benchncnn 4 1 0 -1 1
./benchncnn: /usr/lib/libgomp.so.1: no version information available (required by ./benchncnn)
./benchncnn: /usr/lib/libgomp.so.1: no version information available (required by ./benchncnn)
loop_count = 4
num_threads = 1
powersave = 0
gpu_device = -1
cooling_down = 1
          squeezenet  min =  128.71  max =  130.94  avg =  129.69
     squeezenet_int8  min =  121.99  max =  122.16  avg =  122.10
           mobilenet  min =  208.50  max =  208.89  avg =  208.71
      mobilenet_int8  min =  186.57  max =  186.67  avg =  186.64
        mobilenet_v2  min =  147.75  max =  148.21  avg =  147.89
        mobilenet_v3  min =  123.79  max =  124.46  avg =  124.14
          shufflenet  min =   79.79  max =   80.01  avg =   79.89
       shufflenet_v2  min =   74.18  max =   74.86  avg =   74.41
             mnasnet  min =  145.36  max =  145.45  avg =  145.41
     proxylessnasnet  min =  205.06  max =  205.65  avg =  205.44
     efficientnet_b0  min =  253.43  max =  254.02  avg =  253.60
   efficientnetv2_b0  min =  288.97  max =  289.68  avg =  289.33
        regnety_400m  min =  187.21  max =  187.48  avg =  187.32
           blazeface  min =   22.50  max =   22.84  avg =   22.70
           googlenet  min =  479.23  max =  479.99  avg =  479.56
      googlenet_int8  min =  416.20  max =  419.48  avg =  417.40
            resnet18  min =  376.56  max =  377.02  avg =  376.81
       resnet18_int8  min =  289.09  max =  291.08  avg =  289.92
             alexnet  min =  298.32  max =  299.11  avg =  298.57
Segmentation fault (core dumped)
root@m5stack-LLM:~/benchmark_aarch64# ./benchncnn 4 2 0 -1 1
./benchncnn: /usr/lib/libgomp.so.1: no version information available (required by ./benchncnn)
./benchncnn: /usr/lib/libgomp.so.1: no version information available (required by ./benchncnn)
loop_count = 4
num_threads = 2
powersave = 0
gpu_device = -1
cooling_down = 1
          squeezenet  min =   74.74  max =   82.12  avg =   76.87
     squeezenet_int8  min =   70.57  max =   70.78  avg =   70.70
           mobilenet  min =  111.99  max =  117.73  avg =  113.57
      mobilenet_int8  min =  106.10  max =  110.98  avg =  108.64
        mobilenet_v2  min =   85.62  max =   86.13  avg =   85.80
        mobilenet_v3  min =   73.50  max =   73.70  avg =   73.60
          shufflenet  min =   53.28  max =   61.51  avg =   55.48
       shufflenet_v2  min =   47.94  max =   48.16  avg =   48.04
             mnasnet  min =   84.82  max =   85.09  avg =   84.90
     proxylessnasnet  min =  113.60  max =  120.17  avg =  115.43
     efficientnet_b0  min =  139.99  max =  140.51  avg =  140.18
   efficientnetv2_b0  min =  160.97  max =  168.35  avg =  162.86
        regnety_400m  min =  120.19  max =  120.55  avg =  120.36
           blazeface  min =   14.30  max =   20.97  avg =   16.01
           googlenet  min =  264.75  max =  271.99  avg =  269.56
      googlenet_int8  min =  227.13  max =  234.06  avg =  229.03
            resnet18  min =  209.92  max =  216.98  avg =  211.83
       resnet18_int8  min =  157.32  max =  164.37  avg =  159.27
             alexnet  min =  156.20  max =  157.30  avg =  156.77
Segmentation fault (core dumped)

```



```
root@m5stack-LLM:~# uname -m
aarch64

root@m5stack-LLM:~# uname -v
#1 SMP PREEMPT Mon Oct 21 17:53:51 CST 2024

root@m5stack-LLM:~# cat /proc/cpuinfo
processor       : 0
BogoMIPS        : 48.00
Features        : fp asimd evtstrm crc32 cpuid
CPU implementer : 0x41
CPU architecture: 8
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

processor       : 1
BogoMIPS        : 48.00
Features        : fp asimd evtstrm crc32 cpuid
CPU implementer : 0x41
CPU architecture: 8
CPU variant     : 0x0
CPU part        : 0xd03
CPU revision    : 4

root@m5stack-LLM:~#  cat /proc/meminfo
MemTotal:         981752 kB
MemFree:          718960 kB
MemAvailable:     802660 kB
Buffers:            8492 kB
Cached:           130708 kB
SwapCached:            0 kB
Active:            84556 kB
Inactive:         108956 kB
Active(anon):      54680 kB
Inactive(anon):      460 kB
Active(file):      29876 kB
Inactive(file):   108496 kB
Unevictable:           0 kB
Mlocked:               0 kB
SwapTotal:             0 kB
SwapFree:              0 kB
Dirty:               708 kB
Writeback:             0 kB
AnonPages:         53252 kB
Mapped:            76948 kB
Shmem:               844 kB
Slab:              47320 kB
SReclaimable:      14516 kB
SUnreclaim:        32804 kB
KernelStack:        2352 kB
PageTables:         1768 kB
NFS_Unstable:          0 kB
Bounce:                0 kB
WritebackTmp:          0 kB
CommitLimit:      490876 kB
Committed_AS:     372796 kB
VmallocTotal:   135290290112 kB
VmallocUsed:           0 kB
VmallocChunk:          0 kB
Percpu:              536 kB
HardwareCorrupted:     0 kB
AnonHugePages:      4096 kB
ShmemHugePages:        0 kB
ShmemPmdMapped:        0 kB
HugePages_Total:       0
HugePages_Free:        0
HugePages_Rsvd:        0
HugePages_Surp:        0
Hugepagesize:       2048 kB
Hugetlb:               0 kB

root@m5stack-LLM:~# cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04 (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
root@m5stack-LLM:~# cat /etc/issue
Ubuntu 22.04 LTS \n \l

root@m5stack-LLM:~# df -h
Filesystem       Size  Used Avail Use% Mounted on
/dev/root        7.8G  3.1G  4.7G  40% /
tmpfs            480M     0  480M   0% /dev/shm
tmpfs            192M  844K  191M   1% /run
tmpfs            5.0M     0  5.0M   0% /run/lock
tmpfs            480M     0  480M   0% /tmp
/dev/mmcblk0p17  928K  236K  592K  29% /param
/dev/mmcblk0p19   12G  1.7G   11G  14% /opt
/dev/mmcblk0p18  992M  8.0M  968M   1% /soc
tmpfs             96M     0   96M   0% /run/user/0

root@m5stack-LLM:~# free -h
               total        used        free      shared  buff/cache   available
Mem:           958Mi       105Mi       702Mi       0.0Ki       150Mi       784Mi
Swap:             0B          0B          0B

```


