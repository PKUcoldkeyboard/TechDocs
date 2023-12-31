---
weight: 1053
date: "2023-09-15T02:21:15+00:00"
draft: false
author: "cuterwrite"
title: "“解构 K&R C” 已死"
icon: "circle"
toc: true
description: ""
publishdate: "2023-09-15T02:21:15+00:00"
---



> 原文：[Deconstructing K&RC Is Dead](http://c.learncodethehardway.org/book/krcritique.html)

> 译者：[飞龙](https://github.com/wizardforcel)

我彻底失败了。我放弃了多年以来尝试理清C语言如何编写的想法，因为它的发明是有缺陷的。起初，我的书中有一章叫做“解构 K&R C”。这一章的目的是告诉人们永远不要假设它们的代码是正确的，或者对于任何人的代码，不管它有多出名，也不能避免缺陷。这看起来似乎并不是革命性的想法，并且对我来说它只是分析代码缺陷和编写更好更可靠代码的一部分。

多年以来，我在写这本书的这一块时收到重挫，并且收到了比任何其它事情更多的批评和侮辱。不仅如此，而且书中这部分的批评以这些话而结束，“你是对的，但是你认为他们的代码很烂这件事是错的。”我不能理解，有一群被认为很聪明的人，他们的大脑中充满理性，却坚持“我可以是错的，但是同时也可以是对的”的观点。我不得不与这些学究在C IRC channels、邮件列表、评论上斗争，这包括每一个它们提出一些怪异的、迂腐的刻薄意见的情况，需要我对我的文章进行更多的逻辑性修改来说服他们。

有趣的一点是，在我写这部分之前，我收到了本书许多正面的评论。当时本书还在写作中，所以我觉得确实需要改进。我甚至设置了一些奖金让人们帮助改进。但可悲的是，一旦他们被自己的英雄蒙蔽，所崇拜的基调就发生了翻天覆地的变化。我变得十分令人讨厌，只不过是尝试教人们如何安全使用一个极易出错的垃圾语言，比如C语言。这是我很擅长的东西。

这些批评者向我承认，他们不写C代码也不教授它，他们只是死记硬背标准库来“帮助”其它人，这对我来说并不重要。我以一个开放的心态试图解决问题，甚至设置奖金给那些有助于修复它的人，这也不重要。这可以使更多的人爱上C语言，并且使其它人入门编程，这更不重要。重要的是我“侮辱”了他们的英雄，这意味着我所说的话永远地完蛋了，没有人会再次相信我。

坦率地说，这是编程文化极为的黑暗、丑陋、邪恶的一面。他们整天在说，“我与你们同在”，但是如果你不屈服于大师们海量的学识，以及乞求他们准许你质疑他们所信奉的东西，你突然就会变成敌人。程序员费尽心机地把自己放在权力的宝座上，来要求别人赞许他们高超的记忆能力，或者对一些微不足道的琐事的熟知，并且会尽全力消灭那些胆敢质疑的人。

这非常恶心，我对此也没什么能做的。我对老程序员无能为力。但他们注定会失败。它们通过标准化记忆所积累的学识，也会在咸鱼的下一次翻身中蒸发掉。它们对考虑如何事物的运作方式，以及如何改进它们，或者将它们的手艺传授给他人毫无兴趣，除非这里面涉及到大量的阿谀奉承并让他们觉得很爽。老程序员总会完蛋的。

他们向现在的年轻程序员施压，我对此并不能做任何事情。我不能阻止无能程序员的诽谤，他们甚至根本不像专业的C程序员那样。然而，我宁愿使本书有助于那些想要学习C语言以及如何编写可靠的软件的人，而不是和那些思维闭锁的保守派做斗争。它们贪图安逸的行为给人一种感觉，就是他们知道更多迂腐的、可怜的小话题，就比如未定义行为。

因此，我删除了书中的K&R C部分，并且找到了新的主题。我打算重写这本书，但是并不知道如何去做。我犹如在地狱中，因为我自己非常执着于我觉得很重要的一些事情，但我不知道如何推进。我现在算是明白了这是错的，因为它阻碍我将一些与C不相关的重要技巧教给许多新的程序员，包括编程规范、代码分析、缺陷和安全漏洞的检测，以及学习其它编程语言的方法。

现在我明白了，我将为这本书制作一些课程，关于编写最安全的C代码，以及将C语言代码打破为一种学习C和编程规范的方式。我会卑微地说我的书只是一个桥梁，所有人应该去读K&R C来迎合这些学究，并且在这些黄金法则的脚下顶礼膜拜。我要澄清我的C版本限制于一个固定的目的之中，因为这让我的代码更安全。我一定会提到所有迂腐的东西，比如每个书呆子式的，关于20世纪60年代的PDP-11电脑上空指针的要求。

之后，我会告诉人们不要再去写别的C程序。这不会很明显，完全不会，但我的目标是将人们从C带到能更好地编程的其它语言中。Go、Rust或者Swift，是我能想到的能处理C语言主要任务新型语言，所以我推荐人们学习它们。我会告诉他们，他们的技能在于发现缺陷，并且对C代码的严格分析将会对所有语言都有巨大的好处，以及使其它语言更易于学习。

但是C呢？C已经死了，它是为想要争论A.6.2章第四段的指针未定义行为的老程序员准备的。谢天谢地，我打算去学习Go（或者Rust，或者Swift，或者其它任何东西）了。
