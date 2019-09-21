---  
layout: post  
title: Merge vs Rebase  
category: Command  
tags: Git  
keywords: Git  
---  

__Posted by [Tim Pettersen](https://link.juejin.im/?target=https%3A%2F%2Fdzone.com%2Farticles%2Fmerging-vs-rebasing)__  

__Translated by [银河1号](https://cloud.tencent.com/developer/article/1412819)__  

git rebase命令经常被认为是Git巫术，初学者应该远离它，但它实际上可以让开发团队在使用时更加轻松。在本文中，我们将git rebase与相关git merge命令进行比较。

## 概念

首先要理解的是git rebase和git merge解决了同样的问题。这两个命令都旨在将更改从一个分支集成到另一个分支 - 它们只是以不同的方式进行。

试想一下当你开始在专用分支中开发新功能时另一个团队成员以新提交更新master分支会发生什么。这会出现分叉历史记录，对于使用[Git作为协作工具的](https://link.juejin.im/?target=https%3A%2F%2Fbitbucket.org%2Fproduct%3Futm_source%3Ddzone%26utm_medium%3Dpaid-content%26utm_content%3Dmerging-vs-rebasing%26utm_campaign%3Dbitbucket_adexp-bbtofu_dzone-syn-content)任何人来说都应该很熟悉。

![](/assets/postAssets/2019/15690328008277.jpg)

现在，我们来说说当master新提交与你正在开发的功能相关。要将新提交合并到你的feature分支中，你有两个选择：merge或rebase。

### Merge

最简单的是将master分支合并到feature分支中：

`git checkout feature`

`git merge master`

或者，你可以简化为一行：

`git merge master feature`

这会在feature分支中创建一个新的“merge commit”，它将两个分支的历史联系在一起，为你生成如下所示的分支结构：

![](/assets/postAssets/2019/15690303754199.jpg)

合并很好，因为它是一种非破坏性的操作。现有分支结构不会以任何方式更改。这避免了rebase的所有潜在缺陷（下面讨论）。

另一方面，这也意味着每次上游更改时feature都需要合并，且有无关的合并提交。如果master改动非常频繁，这可能会严重污染你分支的历史记录。尽管可以使用高级git log选项减轻此问题的影响，但它可能使其他开发人员难以理解项目的历史更改记录。

### Rebase

作为merge的替代方法，你可以使用以下命令将feature分支rebase到master分支上：

`git checkout feature`

`git rebase master`

这会将整个feature分支移动到master分支的顶端，从而有效地整合了所有master的新提交。但是，rebase不是使用merge commit，而是通过为原始分支中的每个提交创建全新的提交来重写项目历史记录。

![](/assets/postAssets/2019/15690328241616.jpg)

rebase的主要好处是可以获得更清晰的项目历史记录。首先，它消除了不必要的git merge产生的merge commit。其次，正如在上图中所看到的，rebase也会产生完美线性的项目历史记录 - 你可以从feature分支顶端一直跟随到项目的开始而没有任何的分叉。这使得它比命令git log，git bisect和gitk更容易导航项目。

但是，对这个原始的提交历史记录有两个权衡：安全性和可追溯性。如果你不遵循rebase的黄金法则，重写项目历史记录可能会对你的协作工作流程造成灾难性后果。其次rebase会丢失merge commit提供的上下文 - 你无法看到上游更改何时合并到功能中。

### Interactive Rebase

Interactive rebase使你有机会在将提交移动到新分支时更改提交。这比自动rebase更强大，因为它提供了对分支提交历史的完全控制。通常，这用于在合并特征分支到master分支之前清理杂乱的历史记录。

要开始基于交互式会话，请将i选项传递给git rebase命令：

`git checkout feature`

`git rebase -i master`

这将打开一个文本编辑器，列出即将移动的所有提交：

`pick 33d5b7a Message for commit #1`

`pick 9480b3d Message for commit #2`

`pick 5c67e61 Message for commit #3`

列表准确给出了执行rebase后分支的概况。通过更改pick命令和（或）重新排序，可以使分支的历史记录成为你想要的内容。例如，如果第二次提交修复了第一次提交中的一个小问题，你可以使用以下fixup命令将它们压缩为单个提交：

`pick 33d5b7a Message for commit #1`

`fixup 9480b3d Message for commit #2`

`pick 5c67e61 Message for commit #3`

保存并关闭文件时，Git将根据你的指令执行rebase，从而产生如下所示的项目历史记录：

![](/assets/postAssets/2019/15690328429352.jpg)

消除这种无意义的提交使你的历史记录更可读。这是git merge无法做到的事情。

## rebase的黄金法则

一旦你理解了什么是rebase，最重要的是了解什么时候不使用它。git rebase的黄金法则是永远不要在公共分支使用它。

例如，想想如果你把master分支rebase到你的feature分支会发生什么：

![](/assets/postAssets/2019/15690328771967.jpg)

rebase将master所有提交移动到feature顶端。问题是这只发生在你的仓库中。所有其他开发人员仍在使用原始版本master。由于rebase导致全新的提交，Git会认为你的master分支的历史与其他人的历史不同。

同步两个master分支的唯一方法是将它们合并在一起，从而产生额外的合并提交和两组包含相同更改的提交（原始提交和来自rebase分支的更改）。这将是一个非常令人困惑的情况。

因此，在你运行git rebase之前，总是问自己，“还有其他人在用这个分支吗？”如果答案是肯定的，那就把你的手从键盘上移开，考虑使用非破坏性的方式进行（例如，git revert命令）。否则，你可以随心所欲地重写历史记录。

### 强制推

如果你尝试将rebase过的master分支推到远程仓库，Git将阻止你这样做，因为它与远程master分支冲突。但是，你可以通过传递--force标志来强制推送，如下所示：

`＃这个命令要非常小心！`

`git push --force`

这将覆盖远程master分支以匹配rebase过的分支，并使团队的其他成员感到困惑。因此，只有在确切知道自己在做什么时才能非常小心地使用此命令。

## 工作流

rebase可以根据你团队的需要尽多地或少量地整合到你现有的[Git工作流程](https://link.juejin.im/?target=https%3A%2F%2Fbitbucket.org%2Fproduct%3Futm_source%3Ddzone%26utm_medium%3Dpaid-content%26utm_content%3Dmerging-vs-rebasing%26utm_campaign%3Dbitbucket_adexp-bbtofu_dzone-syn-content)中。在本节中，我们将了解rebase在功能开发的各个阶段的好处。

任何工作流程git rebase的第一步是为每个功能创建专用分支。这为你提供了必要的分支结构，以安全地利用rebase：

![](/assets/postAssets/2019/15690328921980.jpg)

### 本地清理

将rebase加入[工作流程](https://link.juejin.im/?target=https%3A%2F%2Fbitbucket.org%2Fproduct%3Futm_source%3Ddzone%26utm_medium%3Dpaid-content%26utm_content%3Dmerging-vs-rebasing%26utm_campaign%3Dbitbucket_adexp-bbtofu_dzone-syn-content)的最佳方法之一是清理本地正在进行的功能。通过定期执行交互式rebase，你可以确保功能中的每个提交都具有针对性和意义。这使你可以写代码而无需担心将其分解为隔离多个的提交 - 你可以在事后修复它。

调用git rebase时，有两个基（base）选项：feature的父分支（例如master），或feature中的历史提交。我们在Interactive Rebasing部分看到了第一个选项的示例。当你只需要修复最后几次提交时，后一种选择很好。例如，以下命令仅针对最后3次提交的交互式rebase。

`git checkout feature`

`git rebase -i HEAD~3`

通过指定HEAD~3为新的基，你实际上并没有移动分支 - 你只是交互式地重写其后的3个提交。请注意，这不会将上游更改合并到feature分支中。

![](/assets/postAssets/2019/15690329066618.jpg)

如果要使用此方法重写整个功能，git merge-base命令可用于查找feature分支的原始基。以下内容返回原始基础的提交ID，然后你可以将其传递给git rebase：

`git merge-base feature master`

交互式rebase的使用是引入git rebase工作流的好方法，因为它只影响本地分支。其他开发人员唯一能看到的就是你的成品，这应该是一个简洁易懂的分支历史记录。

但同样，这仅适用于私有功能分支。如果你通过相同的分支与其他开发人员协作，则该分支是公共的，并且你能重写其历史记录。

### 将上游更改合并到feature中

在概念部分中，我们了解了feature分支如何使用git merge或git rebase合并master上游更改。merge是一个安全的选择，可以保留仓库的整个历史记录，而rebase则通过将feature分支移动到master顶端来创建线性历史记录。

这种使用git rebase类似于本地清理（并且可以同时执行），但在此过程中它包含了那些master上游提交。

请记住，rebase到远程分支而不是master。当与另一个开发人员协作使用相同的功能并且你需要将他们的更改合并到你的仓库时，就会发生这种情况。

例如，如果你和另一个名为John的开发人员新增了对feature分支的提交，从John的仓库中获取远程分支后，你的仓库可能如下所示：

![](/assets/postAssets/2019/15690329394768.jpg)

你可以用从master集成上游更改相同的方法来解决这个分叉问题：要么用john/feature合并本地feature，或rebase本地feature到john/feature。

![](/assets/postAssets/2019/15690329542407.jpg)

请注意，此rebase不违反黄金法则，因为只有你的本地feature提交被移动 - 之前的所有内容都不会受到影响。这就像是“将我的更改添加到John已经完成的工作。”在大多数情况下，这比通过merge与远程分支同步更直观。

默认情况下，git pull命令执行合并，但你可以通过向其传递--rebase选项来强制它与远程分支rebase集成。

### 集成已验证的feature

在你的团队通过某feature后，你可以选择将该feature rebase到master分支的顶端，然后git merge再将该功能集成到主代码库中。

这是将上游更改合并到功能分支中的类似情况，但由于你不允许在master分支中重写提交，因此你必须最终使用git merge该功能进行集成。但是，通过在合并之前执行rebase，你可以确保合并产生完美的线性历史记录。这也使你有机会压缩在拉取请求期间添加的任何后续提交。

![](/assets/postAssets/2019/15690330401854.jpg)

如果你不熟悉git rebase，可以随时在临时分支中执行rebase。这样，如果你不小心弄乱了feature的历史记录，可以查看原始分支，然后重试。例如：

`git checkout feature`
`git checkout -b temporary-branch`
`git rebase -i master`
`＃[清理历史]`
`git checkout master`
`git merge temporary-branch`

## 总结

这就是你需要知道的关于rebase你的分支。如果你更喜欢提交的干净，消除不必要合并的线性历史记录，那么你在继承另一分支的更改时应该使用git rebase 而不是git merge。

另一方面，如果你想保留项目的完整历史记录并避免重写公共提交的风险，你可以仍然使用git merge。这两种选择都是完全可以的，但至少可以选择利用git rebase有它的好处。
