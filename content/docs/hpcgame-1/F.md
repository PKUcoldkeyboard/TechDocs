---
weight: 3006
title: "F. 高性能数据校验"
author: "cuterwrite"
description: ""
icon: "circle"
toc: true
date: "2024-01-30T02:21:15+00:00"
publishdate: "2024-01-30T02:21:15+00:00"
draft: false
---

> 分数：120 分

## 背景
由于网络波动等等不可控的因素，文件有可能在传输过程和存储过程中损坏，而文件损坏可能会对后续任务产生不可估量的后果和破坏。 校验码是用来检测这种现象的有效手段。但是，通常的校验码实现往往是单线程的，很难利用到现代计算机的多核特性以及并行文件系统的强悍能力。

本题使用一种基于 SHA512 算法的可并行数据校验算法对数据进行分块校验。（SHA512 是一种高度安全的校验码实现，具体算法不需关心）

算法的流程如下（对算法的具体解释见 baseline 代码）：
1. 对数据进行分块，每一块的大小为 M=1MB，记划分的块数为 n。如果文件剩余内容不足一块的大小，则补二进制 0 至一个块大小。
2. 对于第 i 个块，在其末尾连接上第 i-1 个块的 SHA512 校验码的二进制值，将所得到的 M + 64 大小的数据进行 SHA512 校验，得到第 i 个块的校验码。（i 从 0 开始）
    - 注，第 -1 个块的校验码为空文件的校验码
3. 最后一个块的校验码，即为文件的校验码
    - 注，大小为 0 的文件的校验码定义为空文件的 SHA512 校验码

## 输入
选手的程序应当要能接收两个命令行参数。第一个命令行参数是输入文件，这个参数指定了待校验的文件路径。输入文件储存在我们的 lustre 并行文件系统上。

## 输出
程序的第二个参数是输出文件路径，程序应当将校验码输出到输出文件中。

校验码的输出格式为 16 进制数的字符串表示，结尾 **不需要换行** 。例如：

`a777f78b580aa6f095e16415e35cf4ce414bf425c7b2441582c1b3e7f47f0741ca1da2213b06c36070db1428b24037380d96be51b3052ae0079dfe72c147d73b`

注意，所有来自 **标准输出** 的内容都会被忽略。测评程序只会检查输出文件中的结果。

本题提供了使用 libcrypto 库的 baseline 代码（串行，引入 MPI 是为了兼容评测环境）。

## 评测
提交单个 C++ 代码文件，我们将会使用 OpenMPI + GCC 来编译你的代码（编译参数为 `-lcrypto -O3` ）。 并且使用 `mpirun -np 8` 来运行你的程序。你的代码将会运行在两个节点，每台节点 4 个核心上，所以进程和核心是一一对应的。

## Baseline 代码和数据生成器
请在 “附件” 选项卡中下载。

你可以在 scow 集群上用 `mpicxx -O3 -L/lustre/toolchain/openssl/lib64/ -lcrypto` 来编译你的代码。

注意，需要先 `module load gcc/13 openmpi/4.1.6 openssl/3` 。

## 提示
以下两个代码片段在效果上是等价的

{{< prism lang="cpp" linkable-line-numbers="true" line-numbers="true" >}}
uint8_t md[SHA512_DIGEST_LENGTH];
SHA512(data, len, md);
{{</prism >}}


{{< prism lang="cpp" linkable-line-numbers="true" line-numbers="true" >}}
uint8_t md[SHA512_DIGEST_LENGTH];
EVP_MD_CTX *ctx = EVP_MD_CTX_new();
EVP_MD *sha512 = EVP_MD_fetch(nullptr, "SHA512", nullptr);

EVP_DigestInit_ex(ctx, sha512, nullptr);

EVP_DigestUpdate(ctx, data, len);

unsigned int len = 0;
EVP_DigestFinal_ex(ctx, md, &len);
EVP_MD_CTX_free(ctx);
EVP_MD_free(sha512);
{{</prism >}}

## 评分标准和说明
为了模拟处理新磁盘文件的校验文件场景，而评测的时候是无缓存的，所有文件访问将全部经过文件系统。选手在本地测试的时候文件系统通常是有内存缓存的，这会导致本地测试和评测结果不一致。

{{< table "table-responsive table-hover" >}}
|编号|	基础分数|	满分|	超时时间|	满分时间|	输入大小|
|---|---|---|---|---|---|
|1|	1|	15|	3s|	1.4s|	1G|
|2	|1	|35	|8s	|2.75s|	4G|
|3|	1|	50|	20s|	6.3s|	16G|
{{< /table >}}

## 附件路径
- [generate.cpp](https://cuterwrite-1302252842.file.myqcloud.com/attachments/F-checksum/generate.cpp)
- [baseline.cpp](https://cuterwrite-1302252842.file.myqcloud.com/attachments/F-checksum/baseline.cpp)
