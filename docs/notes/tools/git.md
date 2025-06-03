# Git

>如果是深入学习，没有什么是比[官方文档](https://git-scm.com/docs)与[官方教程(Pro Git)](https://git-scm.com/book/zh/v2)更好的参考资料了

## 配置

```bash
# config username
git config --global user.name "<name>"
```
```bash
# config email
git config --global user.email "<email>"
```
```bash
# config syntax highlight
git config --global color.ui auto
```

后续配置，如代理、默认编辑器等参数，或是需要修改其他全局配置，可通过以下命令进入编辑：
```bash
# modify global config
git config --global -e
```

## 基本使用

可参考以下两个内容：

- [Learn Git Branching](https://learngitbranching.js.org/)
>这个教程制作了精美的图形界面，将Git的各种命令通过生动形象的动画展示出来，使人能够更加深入理解不同命令的作用效果。正如进入网页后教程的欢迎辞所言，这是我目前所见过的“最好的Git教程”。

- [版本控制(Git) | Missing-Semester/CN](https://missing-semester-cn.github.io/2020/version-control/)
>除了介绍基础使用与一些有用的配置方案，这个教程还提及了Git的一些底层设计与思想以及一些拓展阅读资源。

基础使用的部分也可简单参考下图：
![](../../assets/tools/git-base.jpg)

*图片来源于网络，仅供学习参考*
### 单分支基础版本控制

- 暂存
```bash
git add [files/paths]
```
- 提交（本地仓库）
```bash
git commit -m "[commit message]"
```

!!! note "提交信息标准化"
    关于这部分内容，与**代码格式化**与**代码注释**相同，或许有人会认为这是多此一举，但在较大的独立项目乃至团队开发中，良好的提交信息可以在遇到问题时帮助你快速**重建代码**，从而提高开发效率。

    在提交时，直接执行`git commit`命令以进入提交信息正文（提交信息详细描述）的编辑。

    对于标准化的参考，业内早已达成了一些微妙的共识，可参考文章[How to Write a Git Commit Message](https://cbea.ms/git-commit/)

- 推送（远程仓库，如GitHub、GitLab等）
```bash
git push origin [branch]
```

- 检查更改（工作区与本地仓库的差异）
```bash
git diff [files/paths]
```
没有路径参数则默认比较整个工作区。

### 多分支基础版本控制

#### 创建与切换分支

- 新建分支
```bash
git branch [branch-name] <commit-hash>
```
`<commit-hash>`默认是当前分支的最后一次提交的提交哈希值，指新建分支的起点。
也可通过符号引用（symbolic reference）创建分支：
```bash
git branch [branch-name] HEAD~3
```
这里就指将当前分支的第三个父提交作为新分支的起点

- 切换分支
```bash
git checkout [branch-name]
```

!!! note "`git checkout -b`"
    新建分支时，`git checkout -b`可以同时实现新建与切换：
    ```bash
    git checkout -b [branch-name] <commit-hash/HEAD~3>
    ```

#### 推送分支

- 远程推送
```bash
git push origin [local_branch_name]:[remote_branch_name]
```

- 本地关联远程分支
```bash
git push --set-upstream-to=origin/[remote_branch_name] [local_branch_name]
```
这样后续 push 或 pull 时不需要再指定远程分支，git会自动使用这个上游分支。

- 推送同时本地关联远程分支
```bash
git push -u origin [branch_name]
```
这样表示本地分支与远程分支的名称相同。

#### 删除分支

- 删除本地分支
```bash
git branch -d [branch_name]
```
若分支未合并，git会报错。

- 强制删除本地分支
```bash
git branch -D [branch_name]
```

- 删除远程分支
有两种方法，一种是直接删除：
```bash
git push origin -d [branch_name]
```
还有一种是推送空分支到远程：
```bash
git push origin :[branch_name]

- 删除远程分支后，更新本地分支列表（将远程仓库拉取到本地仓库）
```bash
git fetch -p
# or full name
git fetch --prune
```

#### 分支重命名

- 重命名本地分支
```bash
git branch -m [old_name] [new_name]
```

- 重命名远程分支
直接先删除远程分支：
```bash
git push origin -d [old_name]
```
然后再关联推送本地分支即可：
```bash
git push -u [new_name]
```

#### 合并分支

- 普通合并
```bash
git merge [branch_name]
```
这个命令会将分支`[branch_name]`合并至当前分支，同时保留分支**树状**的提交历史。

- 变基合并
```bash
git rebase [branch_name]
```
这个命令会将当前分支合并至分支`[branch_name]`，并将这次合并记录为`[branch_name]`的一次新的提交。若在版本控制中完全使用`rebase`进行分支合并，则会使提交历史呈**线性**分布，使得整个提交记录更加清晰简洁。

!!! note
    注意二者的区别除去提交历史上的不同还有命令上分支目标参数的区别：
    - `merge`后的分支参数是**被合并的分支**

    - `rebase`后的参数是要**合并到的目标分支**

关于这部分的内容，在[Learn Git Branching](https://learngitbranching.js.org/)中有形象的教程可供参考。

!!! warning
    使用`rebase`可能会改变提交的历史顺序与哈希值，这可能导致一些混淆问题。在团队协同开发中，一般不建议使用`rebase`进行分支合并。

无论使用哪种方法，在分支合并的过程中，若出现**冲突**，都需要用户进行手动合并。关于合并的一些操作会在后文提及。

## 进阶使用

上文所述，在个人独立项目及普通的版本控制（不一定非是开发环境才可用版本控制系统）基本就已经够用了。接下来，我们学习记录一些进阶的用法。

### 自定义Git属性

在项目中，我们可以自定义**Git属性**。这些属性可以控制 Git 在处理文件时的行为，它们通常定义于项目（Git仓库）的根目录下的`.gitattributes`文件中。

>具体用法可参考[官方教程](https://git-scm.com/book/zh/v2/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-Git-%E5%B1%9E%E6%80%A7)

!!! note "`.gitattributes`模板"
    对于`.gitattribute`文件，[这个仓库](https://github.com/gitattributes/gitattributes)收录了大量的**模板**以供参考。

### 引用

在上文中我们有提到，提交记录在Git程序底层可用**哈希值（SHA-1）**标记，但对于人类而言，记住一串40位的16进制字符不太现实，**引用**便由此而生。

在底层，可简单将引用理解为一个**可变的**，指向提交的**指针**。例如，在使用Git时我们常见到的`master`/`main`就是一个通常**指向主分支最新提交**的一个引用。

#### HEAD

`HEAD` 是指向当前分支最新提交的引用，简单来说，它指向**我们当前所在的位置**。在使用Git时，`HEAD`使我们能够直接以它为参考（即**相对位置**）进行一系列操作。

可通过以下命令查看当前`HEAD`指向的位置：
```bash
cat .git/HEAD
```
这个命令会输出一个提交的**哈希值**（如果你改变了它的默认位置的话）。当然，默认情况下，如上面所说，`HEAD`指向当前分支的最新提交，所以默认的输出一般是这样的：
```bash
ref: refs/heads/main
```
当然，我们也可以改变`HEAD`指向的位置，最常见的例子就是**切换分支**的操作，这通常通过`git checkout`实现。大多数修改提交树的 Git 命令都是从改变 HEAD 的指向开始的。

!!! note
    事实上，对引用的应用已经涉及到[Git内部原理](https://git-scm.com/book/zh/v2/Git-%e5%86%85%e9%83%a8%e5%8e%9f%e7%90%86-Git-%e5%bc%95%e7%94%a8)的内容了，从底层原理自下而上地理解更有利于记忆这部分内容。

#### 相对引用

在实际操作中，我们可以使用诸如`^`、`~{n}`的修饰符结合`HEAD`，使得我们能够轻松地访问`HEAD`的相对位置，这就是**相对引用**。

相对引用有两种形式：

- `^`：被修饰引用的一级父亲提交
    - `^^`：二级父提交（以此类推）

- `~`：被修饰引用的一级父亲提交
    - `~~...(n个~)/~n`：$n$级父提交

这部分内容的简单运用在[Learn Git Branching](https://learngitbranching.js.org/)的高级篇关卡中有极为生动形象的动画演示。

>也可参考[git HEAD / HEAD^ / HEAD~ 的含义](https://segmentfault.com/a/1190000022506884)

```bash
# 当前提交
HEAD = HEAD~0 = HEAD^0

# 主线回溯
HEAD~1 = HEAD^ 主线的上一次提交
HEAD~2 = HEAD^^ 主线的上二次提交
HEAD~3 = HEAD^^^ 主线的上三次提交

# 如果某个节点有其他分支并入
HEAD^1 主线提交（第一个父提交）
HEAD^2 切换到了第2个并入的分支并得到最近一次的提交
HEAD^2~3 切换到了第2个并入的分支并得到最近第 4 次的提交
HEAD^3~2 切换到了第3个并入的分支并得到最近第 3 次的提交

# ^{n} 和 ^ 重复 n 次的区别 
HEAD~1 = HEAD^
HEAD~2 = HEAD^^
HEAD~3 = HEAD^^^
# 切换父级
HEAD^1~3 = HEAD~4 
HEAD^2~3 = HEAD^2^^^
HEAD^3~3 = HEAD^3^^^
```

### 撤销变更

撤销操作有两种方式：`git reset`与`git revert`

![](../../assets/tools/git_2.jpg)

*图片来源于网络，仅供学习参考*

前者本质上是对Git引用的一个简单应用（直接把分支引用的指针回退一个版本），后者本质上是创建一个新的提交。

在执行撤销时提交树的操作效果上，这部分内容同样在[Learn Git Branching](https://learngitbranching.js.org/)的高级篇关卡中有极为生动形象的动画演示。下面记录一些使用细节。

#### `git reset`

>参考：[Git Reset and Revert Tutorial for Beginners](https://www.datacamp.com/tutorial/git-reset-revert-tutorial)

![](https://media.datacamp.com/legacy/image/upload/v1671196209/Diagram_of_Before_and_After_Git_Reset_9af0fcc3e8.png)

*图片来源于网络，仅供学习参考*

!!! warning
    由于`reset`直接操作分支引用的特性，若在本地版本控制使用了它，推送至远程后是不会有任何相关记录的，因此在使用它前必须慎重考虑是否符合当前的应用场景，特别是涉及到会**清除数据**的操作（如硬回退）！
    
    这里引用[Pro Git](https://git-scm.com/book/zh/v2/Git-%e5%9f%ba%e7%a1%80-%e6%92%a4%e6%b6%88%e6%93%8d%e4%bd%9c)的一个忠告：记住，在 Git 中任何 已提交 的东西几乎总是可以恢复的。甚至那些被删除的分支中的提交或使用 --amend 选项覆盖的提交也可以恢复。然而，任何你未提交的东西丢失后很可能再也找不到了。

- 软回退(`--soft`)：仅将分支引用回退至指定版本，暂存区及工作区内容保持不变

    一个简单的应用案例就是假设我们在一次提交中遗漏某些文件，那么就可以通过软回退先撤销提交，将遗漏的文件一同包含至暂存区后再次提交。

- 混合回退(`--mixed`，默认选项)：将分支引用回退至指定版本，同时将暂存区重置为指定版本的**commit状态**，工作区内容保持不变
```bash
# 假设当前状态
# HEAD: commit C
# 暂存区: 有一些修改待提交
# 工作区: 有一些修改

# 执行 reset --mixed
git reset --mixed HEAD~1

# 结果：
# HEAD: 移动到 commit B (HEAD~1)
# 暂存区: 重置为 commit B 的状态
# 工作区: 保持原来的修改不变
```
```bash
# 重置到上一个commit，暂存区变为上一个commit的状态
git reset --mixed HEAD~1

# 重置到特定commit
git reset --mixed <commit-hash>

# 重置到当前commit（相当于清空暂存区）
git reset --mixed HEAD
# 或简写为
git reset HEAD
```
!!! note
    在理解混合回退的实际效果时，有一个前提概念需要理解：commit操作是**复制**文件而不是**移动**文件！工作区、暂存区、版本库三者的存储是相互独立的。
    ```bash
    # Git实际上为每个区域维护独立的对象
    .git/
    ├── objects/     # 版本库对象存储
    ├── index        # 暂存区索引文件
    └── refs/        # 分支引用
    ```
    ![](../../assets/tools/git_4.jpg)

    *图片来源于网络，仅供学习参考*
    
    这也就解释了为什么`git reset`可以独立操作各个区域 

- 硬回退(`--hard`)：将分支引用回退至指定版本，同时重置暂存区与工作区的所有内容，**丢弃这些位置的所有更改**

    这是一个相当危险⚠️的操作，其效果直接了当：使`HEAD`回到指定的提交节点，**删除这之后的所有内容**。

!!! note
    由于`reset`操作会直接修改提交历史，在本地执行`reset`操作后，若需推送至远程，需要添加`-f`参数强制推送，否则Git可能会阻止推送并提示*当前分支的最新提交落后于其对应的远程分支*

#### `git revert`

>参考：[Git Reset and Revert Tutorial for Beginners](https://www.datacamp.com/tutorial/git-reset-revert-tutorial)

![](https://media.datacamp.com/legacy/image/upload/v1671196209/Diagram_of_Revert_Before_and_After_4b427cf59b.png)

*图片来源于网络，仅供学习参考*

与`reset`不同，`revert`不会删除任何东西，而是通过**创建一个具有原始提交反向内容的新提交**来反转原始提交引入的更改。这就是一个安全的撤销操作，因为整个过程**没有任何删除操作**，这就意味着在撤销的过程中版本库中有所记录的一切（文件更改、提交历史等）都会完好无损地保存在本地乃至远程服务器上。

关于两个撤销操作的对比，还可参考[这篇文章](https://www.geeksforgeeks.org/git-difference-between-git-revert-checkout-and-reset/)末尾的表格（其中还提及了`checkout`）

包含`checkout`的操作可视化，也可参考下图：

![](../../assets/tools/git_3.jpg)

*图片来源于网络，仅供学习参考*

实际开发中，特别是团队协作开发，除非是在本地有比较低级的更改或错误需要撤销，一般建议使用`git revert`以确保信息可控。
