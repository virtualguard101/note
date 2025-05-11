---
title: 工程类资源归档
keywords:
  - 工程化
  - 标准化
math: true
mermaid: false
categories:
  - 资源归档
tags:
  - resources
abbrlink: 48185
date: 2025-04-13 09:07:13
lastmod: 2025-04-18 09:07:13
---


*计算机工程类资源汇总归档，收录实用项目构建、项目标准化、工程化工具使用等计算机工程化相关资料*

## 部分JD

>在学习过程中，找到自己感兴趣的方向很重要，其决定了你未来深耕的道路。可通过研读各个企业的招聘信息来决定自己未来的学习方向，并将其记录下来，作为自己的学习参照。

- [miHoYo校园招聘](https://jobs.mihoyo.com/?channelToken=xzad4a23ad-7daa4c92b60e-abb13ba588ce#/campus/position?competencyTypes%5B0%5D=1)
- [miHoYo JD](https://researching.virtualguard101.xyz/miHoYo-JD/)

## 工程化基础

### 常用工具
>事实上，这个模块所提及的工具基本可以在课程[计算机教育中缺失的一课](https://missing-semester-cn.github.io/)中见到。下面归档我个人认为对我帮助很大的几个资源。

#### Linux 操作系统

##### OverTheWire: Bandit
>这个教程旨在通过**hack游戏**的方式使初学者了解**Linux系统**的各种常用命令，形式上类似于**CTF(Capture the Flag)**，即通过某些手段获取远程主机上的某个关键信息以通过关卡。同时，这个教程的[网址根目录](https://overthewire.org/)上还有许多其他有意思的**wargames（网络对抗）**小游戏可供学习品鉴😋。

- 教程网址：[OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)
- 通关教程：[Linux命令-bandit通关日志 | 掘金-ReisenSS](https://juejin.cn/post/7234467007717982268)

#### Git（分布式版本控制系统）
>Git与Linux均出自荷兰程序员Linus Torvalds之手。Git是Linus为了帮助管理Linux内核开发而开发的一个**版本控制软件**（据说是他本人嫌弃当时现有的版本控制工具不好用，然后就自己搞了一个，大佬就是这么任性）。Git在项目标准化中的作用是不言而喻的，由于其**开源**以及**高性能**的特性，Git已经成为广泛运用于各种项目的版本控制利器。对于工程化的学习，Git是必不可少的。

##### Learn Git Branch
>与[OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)相同，旨在通过关卡游戏的方式让初学者了解Git的各种命令。不同的是，这个教程制作了精美的图形界面，将Git的各种命令通过生动形象的动画展示出来，使人能够更加深入理解不同命令的作用效果。正如进入网页后教程的欢迎辞所言，这是我目前所见过的“最好的Git教程”。

- 教程网址：[Learn Git Branching](https://learngitbranching.js.org/)

#### Vim（基于命令行的文本编辑器）
>绝大多数人在刚开始接触Vim时会被其“反人类”的设计所折磨，但我想说的是，当你真正掌握vim的正确打开方式时，你会发现你在使用它写文档/代码时，双手几乎可以不用离开键盘。以我为例，尽管我更喜欢使用[vscode](https://code.visualstudio.com/)作为我的代码编辑器，但我仍然为它装载了[Vim 模式的插件](https://github.com/VSCodeVim/Vim)  
>下面直接引用[编辑器（Vim） | the missing semester of your cs education](https://missing-semester-cn.github.io/2020/editors/)中的一段话来作推荐Vim的理由：  
>在编程的时候，你会把大量时间花在阅读/编辑而不是在写代码上。所以，Vim 是一个 多模态 编辑 器：它对于插入文字和操纵文字有不同的模式。Vim 是可编程的（可以使用 Vimscript 或者像 Python 一样的其他程序语言），Vim 的接口本身也是一个程序语言：键入操作（以及其助记名） 是命令，这些命令也是可组合的。Vim 避免了使用鼠标，因为那样太慢了；Vim 甚至避免用 上下左右键因为那样需要太多的手指移动。这样的设计哲学使得 Vim 成为了一个能跟上你思维速度的编辑器。

##### 编辑器（Vim）| MIT missing semester
>你说的对，但它确实讲解的挺全面的，从基本操作到自定义扩展，再到进阶操作，应有尽有。

- 教程网址：[编辑器（Vim） | the missing semester of your cs education](https://missing-semester-cn.github.io/2020/editors/)

##### 辅助文档
>这时**文档型教程**的作用就体现出来了。使用得当，它也能单方面提高学习效率，而不是拉低学习效果。  
>~~为了提高效率，对它使用文档型教程吧！~~

- 文档网址：[Linux vi/vim | 菜鸟教程](https://www.runoob.com/linux/linux-vim.html)


## 项目案例

### C++项目

#### 项目集群

- [初学阅读 | 星辰暗涌](https://www.zhihu.com/question/20138166/answer/49707025957?share_code=ib7hm5OZ97r8&utm_psn=1902778157527990437)
