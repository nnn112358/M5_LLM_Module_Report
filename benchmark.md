

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
