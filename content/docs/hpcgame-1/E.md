---
weight: 3005
title: "E. 齐心协力"
author: "cuterwrite"
description: ""
icon: "circle"
toc: true
date: "2024-01-30T02:21:15+00:00"
publishdate: "2024-01-30T02:21:15+00:00"
draft: false
katex: true
---

> 分数：120 分

**重要：注：如果遇到 `Cannot Connect to GCS` 或类似报错的请在选手群内私聊管理提交链接重测，这是由 Ray 集群启动异常造成的。如果遇到 `Actor Died` 或类似报错，那是由于超出了内存限制，请自行研究解决，感谢！**

## 题目描述
遥远的开爱大陆盛产毒药，这些毒药威力并不高，只是会让人痛苦不堪，乖乖地给开爱国王交上赎金获取解药。开爱国王富得流油，但人们对此苦不堪言。

你和宿舍小伙伴们是拉玛大陆骑士学院的优秀学员，致力于推翻开爱国王对解药的垄断，于是踏上了寻找解药方法的路程。路上你们遇到了善良的开爱国公主，她告诉你们，每一种毒药都有 40000 种可能的原料，构成药物空间的一个 40000 维 32 位浮点向量。而对应的解药就是将这个向量进行变幻得到的另一种配方。

经过对厚厚几万页配方书的阅读，你们最终发现，从毒药到解药的变换分四步，每一步都是先进行一个线性变换，然后对 0 取 Max（因为原料没有负数个）。这个线性变换类似于神经网络，具体描述如图。其中每个矩阵是的维度是(40000, 40000)。

大家都听说你们掌握了破解毒药的方法，纷纷找你们帮忙。虽然你们可以手算解药变换，不过依然是太慢了。于是你们打算用高性能计算的思想，让电脑来算这件事。但是你们宿舍的电脑都只有 16G 内存，每一个矩阵就需要 12G 内存，在一台电脑上放不下，需要四个人齐心协力，共同计算。但是天上不会掉馅饼，怎么才能让四台电脑一起计算呢？你听说 Ray 最近很热，是基于 Python 的，编程比 MPI 更加自然，于是想要试一试。


<figure style="text-align:center;">
<img src="https://cuterwrite-1302252842.file.myqcloud.com/img//1th_ray_fcrelu-2024-02-01.webp" alt="relu" width="20%" loading="lazy"/>
</figure>


## 任务描述
对于一百个(200, 40000)的矩阵 $x$ ，计算如下结果，其中 $A、B、C$ 和 $D$ 都是 (40000, 40000) 的矩阵。其中四个矩阵需要被放置在四个不同的节点上，每个节点有 4 个核心、16G 内存。你需要对于输入的每一个 $x$ ，计算得出最终的 $output$ 。

{{< katex >}}
$$
\begin{aligned}
& y_1=ReLU(xA) \\
& y_2=ReLU(y_1B) \\
& y_3=ReLU(y_2C) \\
& output=ReLU(y_3D) \\
\end{aligned}
$$
{{< /katex >}}


## 输入输出约定
### 输入
在 `inputs` 文件夹中有 `input_0.npy` 到 `input_99.npy` 共 100 个文件，每个文件都是(200, 40000)的 `numpy` 的 `ndarry` ，可以通过 `np.load` 方法读取，如 `np.load(f"inputs/input_{i}.npy")`

 $A、B、C$ 和 $D$ 矩阵保存在 `weights` 文件夹下，命名为 `weight_[0-4].npy` ，如保存在 `weight_0.npy` 中。

### 输出
对于 inputs 中的每个输入，计算完成后将 `ndarray` 通过 `np.save` 的方式保存到 `outputs` 文件夹下，如 `np.save(f"outputs/output_0.npy", output)` 。

提示：`outputs` 文件夹需要自己建。

### 误差范围
与标准答案的相对误差在 `1e-4` 的范围内即即为正确。

### 说明
输入输出文件夹都使用了超级高速文件系统。不需要太考虑优化读写。

权重文件夹没有使用超级高速文件系统，不建议重复读写权重。

## 环境说明和程序调用方式
提供四个节点，node1-4，每个节点 4 个核心，16G 内存，节点之间有 100G 高速网络连接。

我们会在 node1 上通过 `python3 main.py` 运行你的程序，并在你的程序运行完后比较 `output` 文件夹中的输出。`module load python/hpcgame` 可以在超算集群上使用 `python` 。注意，环境里没有 `pytorch` 。

四个节点已经启动了 `ray` 集群，Head 节点地址可以通过环境变量 `RAY_CLUSTER_ADDR` 读到。通过以下命令可以连接到集群。

{{< prism lang="python" linkable-line-numbers="true" line-numbers="true" >}}
import os
import ray

ray.init(address=f"{os.environ['RAY_CLUSTER_ADDR']}")
{{< /prism >}}

## Ray 的简要介绍
1. 核心介绍：[https://docs.ray.io/en/latest/ray-core/walkthrough.html](https://docs.ray.io/en/latest/ray-core/walkthrough.html)，参考 `Ray Core` 部分，主要是 Task 和 Actor 的抽象。当然，其他部分也很好，不过本次比赛没有涉及。
2. Placement Groups 的概念：[https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html](https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html)，在本题中，使用 PACK 就可以。

## 提示
可以在四个机器之间维护一个 pipeline，最大化硬件利用率。[这篇文章](https://medium.com/nerd-for-tech/an-overview-of-pipeline-parallelism-and-its-research-progress-7934e5e6d5b8) 介绍了 pipeline parallelism 的相关概念，如果你学过 ICS 或者相似课程的话，应该很好理解。如下图，横轴是每个已经加载好权重的 worker，纵轴是随着时间的流逝，每个 worker 里面处理的 batch。可以看到，每个 worker 权重是确定的，接收前一个 worker 传递过来的中间数据，处理完再传递给下一个 worker 或者输出。

<figure style="text-align:center;">
<img src="https://cuterwrite-1302252842.file.myqcloud.com/img/1th_ray_pp-2024-02-01.webp" alt="pipeline parallelism" width="60%" loading="lazy"/>
<figcaption><h4 style="font-size:1.4rem; color:#747474">pipeline parallelism</h4></figcaption>
</figure>

## 出题人的话
以往大家学高性能计算，都是从 MPI 和 OpenMP 出发的，出题人也不例外。不过近些年，许多具有更高抽象层次的 API 出现，比起消息传递来说更加符合入门的认知规律。这次给大家介绍的 Ray，就是高抽象层次 API 中的典型代表。

## 得分标准
{{< table "table-responsive table-hover" >}}
|最低得分时间 | 满分时间 | 最低得分 | 满分 |
|---|---|---|---|
| 400s | 200s | 1% | 100% |
{{< /table >}}

## 测试指南
选手可以在集群自己提交任务，进行测试。具体来说，我们在附件提供了三个 sbatch 文件和一个 shell 脚本。将脚本和 Python 文件，以及你自己准备的 input 和 output 放在同一个文件夹下，就能进行测试。


## 附件路径
- [ray-slurm-v6.zip](https://cuterwrite-1302252842.file.myqcloud.com/attachments/ray-v6.zip)
