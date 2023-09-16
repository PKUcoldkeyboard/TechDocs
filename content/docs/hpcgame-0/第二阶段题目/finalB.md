---
weight: 2023
date: "2023-09-15T02:21:15+00:00"
draft: false
author: "cuterwrite"
title: "B. 高性能存储阵列的软件开销优化"
icon: "circle"
toc: true
description: ""
publishdate: "2023-09-15T02:21:15+00:00"
---

## 一、背景介绍

近些年来，SSD因其高带宽、低延迟、低能耗的特点，已经成为了高性能计算、数据中心、云服务等场景下的主要存储设备。但不幸的是，由于其自身的物理性质，相较于HDD，SSD通常更容易损坏，导致数据丢失。

存储阵列（RAID）是解决这个问题的手段之一。通过条带化技术，RAID可以聚合多个SSD的性能，同时对外提供服务，以驱动高性能计算中大量I/O的场景；通过校验和技术，RAID可以保证存储阵列具有一定的容错性，即使其中的一个磁盘损坏，也能从剩余的磁盘中恢复数据。

Linux software RAID（mdraid）是Linux内核中自带的RAID引擎，设计于二十多年前，因其高昂的软件开销，已不再适合用来创建和管理现有的高性能存储设备（如NVMe SSD）。如何优化mdraid，使得高性能SSD组成的存储阵列能够发挥出优异的性能，是现在学术界和工业界关注和研究的重点。

## 二、赛题描述

本次比赛允许优化mdraid中的任何软件开销，考虑到比赛时间限制，参赛者可以通过阅读论文[1][2]了解到mdraid中已知的可优化的开销。同时，我们鼓励参赛者自己通过perf，fio等工具剖析RAID软件栈，找出其他可优化的部分。

下面简单介绍一下mdraid中的一个和锁相关开销，该开销的详细分析和说明可见论文[1]。如下图所示，在mdraid中，当I/O线程在处理写请求时，它首先会将数据分割为多个stripe unit。拥有相同offset的stripe unit属于同一个条带，它们会被一起处理 ①。但在处理之前，I/O线程需要向守护进程获取一个名为stripe_head的数据结构 ②。但是，为了防止多线程之间的冲突，mdraid使用全局的锁去管理stripe_head的分配。因此，如果我们使用多个线程来处理I/O请求，它们就会被这个锁阻塞，无法并行处理，造成大量的软件开销。解决这个问题的办法很简单，我们可以给每个stripe_head都分配一个锁，单独进行管理，再使用hash算法让不同的线程去找到不同的stripe_head，从而最大化线程的并行度。

![](https://cuterwrite-1302252842.file.myqcloud.com/img/20230214152652.png)

类似的软件开销还有很多，请参赛者务必阅读论文[1][2]，以对mdraid相关的设计和开销形成初步的了解。除此之外，这里推荐查看资料[3]，辅助阅读mdraid相关的代码。

## 三、评测说明

1. 我们允许修改附件中md文件夹下的任何代码，但其中很多代码只是因为编译需要而存在，和本次比赛相关度较低，因此我们建议参赛者关注文件raid5.*，md*.*；

2. 修改代码后，参赛者可以根据附件README安装测试环境，测试自己代码的正确性。评测过程中也会使用相同的内核（linux-5.11-46）；

3. 在评测过程中，我们会使用mdadm创建RAID5，参赛者可以参考[4]学习mdadm的使用方法；

4. 在评测过程中，我们会使用高性能的NVMe SSD组建RAID,如果参赛者自己的Coding环境没有足够的磁盘，可以参考附录A，使用RAM模拟磁盘;

5. [1]的代码是开源的，我们允许参赛者整合该开源代码作为基础继续修改，但必须有其他的设计以作为此次参赛的内容；

6. 在评测过程中，我们会使用fio产生IO请求，参赛者可以参考[5]学习fio的使用。

## 四、评分标准

我们会用高性能的NVMe SSD组成2+1，4+1两种RAID5，并使用fio评估I/O的带宽和完成时延。带宽越高分数越高，延迟越低分数越高，按排名正态分布给分。我们使用到的测试参数如下表所示，其中worker thread的定义可以参考论文[1][2],并通过修改文件/sys/block/mdx/md/group_thread_cnt修改，这里mdx是你通过mdadm创建的RAID：

| RAID类型 | I/O Size | No. of I/O threads | No. of Worker threads | IO depth | 类别  | 指标  | 分数占比   |
| ------ | -------- | ------------------ | --------------------- | -------- | --- | --- | ------ |
| 2+1    | 64 KB    | 8                  | 8                     | 32       | 随机写 | 带宽  | 6.25 % |
| 2+1    | 128 KB   | 8                  | 8                     | 32       | 随机写 | 带宽  | 6.25 % |
| 4+1    | 64 KB    | 8                  | 8                     | 32       | 随机写 | 带宽  | 6.25 % |
| 4+1    | 256 KB   | 8                  | 8                     | 32       | 随机写 | 带宽  | 6.25 % |
| 2+1    | 64 KB    | 8                  | 8                     | 32       | 顺序写 | 带宽  | 6.25 % |
| 2+1    | 128 KB   | 8                  | 8                     | 32       | 顺序写 | 带宽  | 6.25 % |
| 4+1    | 64 KB    | 8                  | 8                     | 32       | 顺序写 | 带宽  | 6.25 % |
| 4+1    | 256 KB   | 8                  | 8                     | 32       | 顺序写 | 带宽  | 6.25 % |
| 2+1    | 4 KB     | 1                  | 1                     | 1        | 随机写 | 延迟  | 12.5 % |
| 4+1    | 4 KB     | 1                  | 1                     | 1        | 随机写 | 延迟  | 12.5 % |
| 2+1    | 4 KB     | 1                  | 1                     | 1        | 顺序写 | 延迟  | 12.5 % |
| 4+1    | 4 KB     | 1                  | 1                     | 1        | 顺序写 | 延迟  | 12.5 % |

附件fio.conf，给出了第一组测试的fio配置文件。

## 五、参考文献

[1] Yi, Shushu, et al. "ScalaRAID: optimizing linux software RAID system for next-generation storage." Proceedings of the 14th ACM Workshop on Hot Topics in Storage and File Systems. 2022.（编者注：https://dl.acm.org/doi/10.1145/3538643.3539740 ，已在附件中包含，仅供学习研究之用）

[2] Wang, Shucheng, et al. "{StRAID}: Stripe-threaded Architecture for Parity-based {RAIDs} with Ultra-fast {SSDs}." 2022 USENIX Annual Technical Conference (USENIX ATC 22). 2022.（编者注：https://www.usenix.org/conference/atc22/presentation/wang-shucheng ，文档开放获取）

[3] [小表弟皮卡丘的博客_CSDN博客-linux kernel,raid,存储领域博主](https://blog.csdn.net/chenyouxu)

[4] [A guide to mdadm - Linux Raid Wiki](https://raid.wiki.kernel.org/index.php/A_guide_to_mdadm)

[5] https://fio.readthedocs.io/en/latest/index.html

# 附录A: 如何搭建测试环境（buildenv.md）

## 一、安装内核

评测中将使用的内核版本为`linux-5.11-46`，请在测试中尽量使用相同的内核版本。mdraid模块默认是不可修改的，如果想要修改，需要在编译内核文件时将相关配置设置为[M]。我们提供的ubuntu环境已经配置完成，如果你想使用自己的设备，请自行编译内核。

我们在附件中提供了`linux-image`的deb包，可用于`ubuntu 20.04`版本安装，具体步骤如下。

```
dpkg -i linux-image-unsigned-5.11.0-46-generic_5.11.0-46.51~20.04.1_amd64.deb \
             linux-modules-5.11.0-46-generic_5.11.0-46.51~20.04.1_amd64.deb

apt install linux-headers-5.11.0-46-generic \
                 linux-modules-extra-5.11.0-46-generic \
                 linux-buildinfo-5.11.0-46-generic \
                 linux-tools-5.11.0-46-generic
```

## 二、优化 & 编译

我们允许参赛者优化md文件夹下的任何代码，我们已经写好了Makefile文件，优化完成后，参赛者可以直接通过`make`指令进行编译。编译完成后会生成一系列`.ko`文件，这就是内核模块文件。请参赛者仔细阅读Makefile文件，确定自己的修改涉及到哪几个`.ko`文件，并安装这些修改后的模块。

## 三、安装模块

1. 首先进入存放mdraid相关模块的文件夹：`cd /lib/modules/5.11.0-46-generic/kernel/drivers/md/` ；

2. 假设我们修改的模块是`md-mod.ko`。我们先备份这个文件：`cp md-mod.ko md-mod.ko.bak`；

3. 然后我们删除原有的未经修改的md-mod模块。由于许多模块依赖于md-mod模块，因此我们需要先删除这些依赖的模块，并最后删除md-mod。参赛者可以通过`lsmod | grep md`来查看模块的依赖关系。假设md-mod被模块linear，raid0，raid456，...依赖：
   
   ```bash
   # 删除依赖md-mod的模块
   rmmod raid1
   rmmod raid10
   rmmod raid0
   rmmod linear
   rmmod raid456
   rmmod multipath
   # 请检查自己系统，查看是否有其他依赖
   
   # 删除md-mod模块
   rmmod md-mod
   ```

4. 然后我们将之前编译产生的`md-mod.ko`复制的这里：`sudo cp path/md-mod.ko ./`；

5. 最后我们安装md-mod模块以及之前删除的模块：
   
   ```bash
   // 安装md-mod模块
   insmod md-mod.ko
   
   // 安装之前删除的模块
   insmod raid1.ko.
   insmod raid10.ko
   insmod raid0.ko
   insmod linear.ko
   insmod raid456.ko
   insmod multipath.ko
   ```

至此，你的修改已经嵌入到内核中，可以通过mdadm创建RAID5并使用fio进行测试。

# 附录B：使用内核模块`brd`创建内存盘

`block ram disk`，缩写为`brd`，是Linux kernel中提供的创建内存盘的模块，代码可以在`kernel`中`drivers/block/brd.c`找到。

由`brd`创建的内存盘和`brd`模块的生命周期相同重启时会消失，具体来说：

1. 加载模块、创建内存盘：`modprobe brd`
   
   这个命令有三个可选参数：
   
   `rd_nr` : 创建内存盘的数量 `rd_size` : 内存盘的最大大小，单位为kb `max_part` : 每个内存盘的最多分区数
   
   下面例子在创建了5个大小为2G的单分区内存盘，位于`/dev/ram0`到`/dev/ram4`
   
   ```
   modprobe brd rd_size=2048000 max_part=1 rd_nr=5
   ```

2. 卸载模块、删除所有内存盘：`rmmod brd`

3. 分区与fdisk的使用：[https://wiki.archlinux.org/title/fdisk，本题中，可以使用如下命令进行分区](https://wiki.archlinux.org/title/fdisk%EF%BC%8C%E6%9C%AC%E9%A2%98%E4%B8%AD%EF%BC%8C%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E5%A6%82%E4%B8%8B%E5%91%BD%E4%BB%A4%E8%BF%9B%E8%A1%8C%E5%88%86%E5%8C%BA)

```shell
TGTDEV=/dev/ram0
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk ${TGTDEV}
  n # new partition
  p # primary partition
  1 # partition number 1
    # default - start at beginning of disk 
    # default - default size
  t # change partition type
  fd# to Linux raid autodetect
  w # write the partition table
  q # and we're done
EOF
```

### 附件

参考资料1

下载`ScalaRAID.pdf`

说明与工作区

下载`raid.zip`
