---
weight: 3001
title: "A. 欢迎参赛"
author: "cuterwrite"
description: ""
icon: "circle"
toc: true
date: "2024-01-30T02:21:15+00:00"
publishdate: "2024-01-30T02:21:15+00:00"
draft: false
---

> 分数：10 分

## 关于本题
为了确保每位选手都详细地阅读参赛须知，所以我们把创建集群账户这一步操作放在了这道题目中。当你完成了这道题目，**您会在评测结果中收到登录 SCOW 平台（本次比赛选手与超算直接交互的平台）的地址和凭据。** 请您往下阅读，即可获得通过此题的方法。

请不要使用 `https://scow.pku.edu.cn/` 的集群，比赛有专门的集群，在本题的评测结果中发放给您，请注意检查评测结果！集群由登录节点和计算节点两部分组成，SCOW 的 shell 进入的是登录节点。对于所有任务，请提交脚本交由计算节点进行计算，具体方式可以参考这个 [slrum 使用说明](https://hpc.pku.edu.cn/ug/guide/slurm/)。具体的，您需要关注 slurm 介绍、`salloc` 、`sinfo` 、`squene` 、`sacct` 和 `scancel` 命令的使用。

特别地，教程中的 `sbatch` 是旧版，对于比赛集群使用的新版，`--ntasks-per-node` 只是每个节点上最多开的进程数，还需要指定 `--ntasks` 以确定总进程数。该版本的 slurm 也不需要像教程例子那样处理 `hostfile` 了。这里给出一个新版本跑 MPI 的例子：

{{< prism lang="bash" linkable-line-numbers="true" line-numbers="true" >}}
#!/bin/bash
#SBATCH -o job.%j.out
#SBATCH --partition=C064M0256G
#SBATCH --qos=normal
#SBATCH -J myFirstMPIJob
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4

# 导入 MPI 运行环境
module load openmpi

# 执行 MPI 并行计算程序
mpirun -n 8 hostname > log
{{< /prism >}}

如果登录到计算节点提示需要密码，请使用

{{< prism lang="bash" linkable-line-numbers="true" line-numbers="true" >}}
ssh-keygen（一路回车）
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
{{< /prism >}}

即可在所有节点免密登录

## 超算平台软硬件环境
1. 硬件: 每台机器为 Intel Xeon Platinum 8358 * 2, 256G 内存。GPU 为经过拆分的 A100 ，选手写题使用 1/7 张 A100 80G GPU，评测使用 1/2 张 A100 40G。
2. 操作系统和基础软件环境: RockyLinux 8.7, Kernel 4.18, GCC 8.5, CMake 3.26。GPU 节点安装 CUDA 12.3.2。
3. 文件系统：集群为 30T 的全闪 Lustre 文件系统，可以使用 mpi-io 加速读写，但是正常读写也不会成为性能瓶颈。
4. 附加软件：使用 `environment-modules` 管理，`module avail` 可以查看可用软件，`module load` 即可加载。这些软件在整个集群都可用，评测时和向 slurm 提交任务的时候也可用。如果需要更多包，请在 QQ 群联系管理员。
5. 软件列表：`Intel OneAPI 2024.0.1` , `gcc/12` , `gcc/13` , `openmpi` , `conda` , `openssl` , `julia` 。Conda 中已配置好 `hpcgame` 和 `pytorch` 两个环境，`module load conda` 后 `mamba activate` 即可使用。如果需要补充 Python 包，也请联系管理员。当然，可以创建自己的 Python Virtualenv 使用，但是评测机访问不到选手的环境。对于所有提交的题目，请使用 `modules` 管理的环境。所有需要换源的软件均已替换至 [PKU Mirrors](https://mirrors.pku.edu.cn/)。

## 成绩计算方法
每道小题都是 100 分制，但是在计算总分和排名的时候会根据题目难度赋分。

## 参赛须知
1. 不得作弊。比赛是个人赛，任何多人合作完成比赛的行为都将被认为作弊。组委会在多处设置了作弊检查点，并将进行代码查重，希望大家诚信比赛，赛出风采。
2. 不得攻击 OJ 和 SCOW 平台。本比赛不是 CTF，不考察任何形式的平台攻击。如果我们发现任何攻击行为，选手将会被除名。如果您发现任何 Bug 或可能的安全漏洞，请您与我们联系，我们会给予充分报答，但不包括比赛分数上的奖励。
3. 赛题分批次放出。我们计划在 2024/01/24 12:00 和 2024/01/25 12:00 释出部分未释出的试题，释出顺序与题目难度无关。
4. 比赛的所有题目场景均为虚构，不反映现实或历史。所有人物均为虚拟人物，并非真实人物的对应。
5. 在 SCOW 平台上，如果需要使用 GPU，请使用 `GPU80G` 分区，为拆分过的 A100 80G 显卡。
6. 请勿滥用 SCOW 平台计算资源，一经发现，立即封号。
  1. 开启 VSCode 任务时，请只需要分配 1 核心 CPU（CPU 分区） / 1 块 GPU（GPU 分区，GPU 分区至少分配 8 核心 CPU，这是没问题的）。这足够您的使用。否则我们会直接结束您的任务，对此造成的损失由您自己承担。
  2. 请及时结束自己的任务，组委会定期取消超过 2 小时未结束的任务（VSCode 任务允许 4 小时），造成的后果由选手自己承担。
7. 我们发现有部分选手直接大段使用互联网上的代码乃至成千行地照搬开源项目代码；我们鼓励参考借鉴各种优秀实现，广泛学习；但我们希望大家能真的从比赛中学到东西。因此，如果我们发现选手大段连续使用互联网上现成代码的，请主动提交 对这份代码的理解和对题目要求的理解说明文档，字数至少为代码行数除以 6（向上取整百，例如 9100 行代码，需要提交不少于 1600 字的说明文档），需要包括用户名、题号，请使用 PDF 格式主动发送至 hpcgame@pku.edu.cn ，否则我们将会把本题得分记为 0 分。如有异议，请向同一邮箱提出。

## 隐私协议
1. 我们（北京大学高性能计算综合能力竞赛组委会）高度重视您的隐私，将会采取一切必要措施保护您的隐私安全；
2. 在比赛过程中我们会收集您的个人信息、做题情况等信息。这些信息只供本次比赛所用，赛后您可要求组委会永久删除；
3. 我们可能会将您的部分个人信息（姓名、邮箱等）提供给赞助商作为校招等用途。组委会与赞助商约定，如您无回复，每半年最多打扰您一次。如您不同意本条，可以发送主题为“HPCGame+邮箱+不同意校招信息分享”的邮件至 `hpcgame@pku.edu.cn` ，我们将不会分享您的信息。
4. 对于本协议的最终解释权归组委会所有。

请注意，提交本题表示您已阅读并同意参赛须知和隐私协议。

## 通过本题
切换到“提交”选项卡，点击“提交”按钮即可。不要忘记在“提交记录”里查看集群访问方式哦！

## FAQ
![](https://cuterwrite-1302252842.file.myqcloud.com/img/sining-example-2024-02-01.webp)
