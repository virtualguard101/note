# Git

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

### 单分支基础版本控制

![](../../assets/tools/git-base.jpg)

暂存：
```bash
git add [files/paths]
```
提交（本地仓库）：
```bash
git commit -m "[commit message]"
```
推送（远程仓库，如GitHub、GitLab等）：
```bash
git push origin [branch]
```
