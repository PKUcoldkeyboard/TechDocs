---
weight: 2025
date: "2023-09-15T02:21:15+00:00"
draft: false
author: "cuterwrite"
title: "D. Linkpack节点的选择程序优化"
icon: "circle"
toc: true
description: ""
publishdate: "2023-09-15T02:21:15+00:00"
---

## 赛题描述

给定2个SPINE交换机下48个候选节点，要求在不超过3次Linpack计算的情况下，**通过程序或脚本以全自动的方式**选择16个节点，得到16节点的Linpack最优值。

linpack的评测指标是gflops。

## 输入

无，选手可自行获取相关信息

## 输出

结果输出到`output.txt`，其中包含16个节点名(可通过`hostname -s`获取)。与最优值误差在0.1%之内的结果都算正确。

## 提交方式

选手提交一个压缩包，我们运行其中run.sh，选手程序输出结果，我们进行核验。选手程序中NB值等可在run.sh指定，最后输出gflops值。

## 测试环境

我们提供了一个样例集群共选手实验提交之用，请注意，该集群及网络拓扑与最终测试的集群并不一致，选手程序需要有通用性，请勿针对该集群进行设计。

选手可以向`linpack`分区提交任务以测试。请注意，单次申请节点数不得超过4个，单次申请时间不得超过30分钟，否则将失去该节点申请资格。建议选手在compute节点进行编码，向linpack提交任务进行测试。

申请节点时请加上`--exclusive`选项，以免受其他评测影响。

## 提示

1． 使用Intel OneAPI MKL函数库下的mp_linpack软件测试包用于Linpack测试（安装在`/data/software/intel/mkl/`）。我们的集群中，只有`SCOW`集群安装了该脚本，请 2． 建议编写dgemm测试程序用于筛选Linpack测试的NB值，以及筛选候选节点的双精度性能 3． 建议采用MPI pingpong测试的方式分析出候选节点的网络拓扑
