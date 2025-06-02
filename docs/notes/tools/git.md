# Git

>如果是深入学习，没有什么是比[官方文档](https://git-scm.com/docs)与[官方教程](https://git-scm.com/book/zh/v2)更好的参考资料了

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

- 可参考[Learn Git Branching](https://learngitbranching.js.org/)

>这个教程制作了精美的图形界面，将Git的各种命令通过生动形象的动画展示出来，使人能够更加深入理解不同命令的作用效果。正如进入网页后教程的欢迎辞所言，这是我目前所见过的“最好的Git教程”。

基础使用的部分也可简单参考下图：
![](../../assets/tools/git-base.jpg)

*图片来源于网络，仅供参考*
### 单分支基础版本控制

- 暂存
```bash
git add [files/paths]
```
- 提交（本地仓库）
```bash
git commit -m "[commit message]"
```
- 推送（远程仓库，如GitHub、GitLab等）
```bash
git push origin [branch]
```

- 检查更改（工作区与本地仓库的差异）
```bash
git diff [files/paths]
```
没有文件参数则默认比较整个工作区。

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
