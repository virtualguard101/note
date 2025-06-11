# Shell Script

>[The Shell Scripting Tutorial](https://www.shellscript.sh/)

!!! note
    从定义角度来看，`shell`其实应该算是一种**解释型编程语言**，之所以将其放在`tools`而不是`programming language`则是因 shell 在实际应用上作为辅助工具的使用几乎占据了其所有的应用场景；介于其糟糕的接口以及极差的代码复用性，网络上的部分观点甚至都不被认为 shell 是一个真正意义上的编程语言。对于 shell 与普通编程语言的对比，可参考[Shell scripting vs programming language | stackoverflow](https://stackoverflow.com/questions/4955686/shell-scripting-vs-programming-language)

## shebang

shebang（或 hashbang），指脚本文件开头的特殊**注释**行，用于**指定执行该脚本的解释器**：
```sh
#!/path/to/interpreter
```
语法构造上，第一个字符为`#`(hash)，第二个字符为`!`(bang)，故称为 "shebang" 或 "hashbang"。

!!! note
    注意`#!`后是解释器的**绝对路径**；`shebang`是 Unix 和类 Unix 的系统特性，在其他系统中通常不受支持或需要工具辅助支持。关于`shebang`的详细信息还可参考[Shebang (Unix) | Wikipedia](https://en.wikipedia.org/wiki/Shebang_(Unix))


## `echo` && `read`

在 shell 中，`echo`用于将文本信息输出到终端上：
```sh
echo [options] [params]
```

!!! tip
    注意下面二者的区别：
    ```sh
    # echo without double/single quote
    echo Hello World

    # echo with quote
    echo "Hello World"
    ```
    后者的`echo`将`Hello World`视为**一个**文本参数，前者的`echo`则将其视为**两个**文本参数；在前者中，无论`Hello`与`World`间存在多少个空格或是`tab`，最终在解释器眼里都是一样的操作，执行结果也就一致。

`read`则用于交互地从用户读取数据：
```sh
#!/bin/sh
echo "What's your name?"
read USER
echo "Hello, $USER"
```
同样注意引号；而这里的文本信息中还包含了特殊字符`'`，需要使用双引号。

!!! note
    在执行脚本时，输入变量的过程中则不需要再为右值添加双引号或其他转义字符，`read`会自动完成这一操作

## 变量

### 类型安全

![](https://samgrayson.me/raw-binary/stop-writing-shell-scripts//moneyball.png)

*Source of the Image: [Stop writing shell scripts](https://samgrayson.me/essays/stop-writing-shell-scripts/)*

图片的源文章很有意思，强烈建议参考阅读。

### 赋值

注意赋值时`=`前后不能有空格：
```sh
VAR1="Hello World"

# This may get some wrong
VAR2 = "Hello World"
```
!!! warning
    上面的例子中，shell 解释器会将变量`VAR2`当作是一个名为`VAR2`的**命令**执行；自然地，后面的`=`与文本信息也就成了这个“命令”的参数。当我们尝试使用`echo`输出`VAR2`时，可能会出现如下报错：
    ```bash
    bash: VAR: command not found
    ```

同时，这时的`Hello World`就必须使用双引号引用，否则`World`就会被解释器当作变量赋值操作后需要尝试执行的**命令**。
!!! tip
    并不是所有的字符串变量都需要使用引号，当然，在使用字符串时通过引号引用是一个良好的编程习惯。

最后还需注意在引用时，`"`与`'`的区别，以以下脚本为例：
```bash
var1="Hello, $USER"
var2='Hello, $USER'

echo $var1
echo $var2
```

- 前者允许变量扩展或命令替换，因此第一个`echo`输出的结果会将`$USER`替换为变量`USER`的值

- 后者则保留完整的原始字符串

### 变量作用域

#### 未定义变量

在 shell 脚本中，若尝试访问一个**未定义**的变量：
```sh
USER=virtualguard
echo "Hello, $USOR"   # mis-spelled
```

!!! tip inline end
    可通过在脚本开头添加`set -u`解决这个的问题，这会使shell解释器在遇到未定义变量时报错；
    
    然而 shell 还有一个致命问题就是在遇到错误时默认不会中断，而是继续执行脚本的内容...🙃，这可通过在`set`后添加`-e`参数解决。

shell 解释器并不会报错，而是返回一个**空字符串**：
```bash
./var.sh
Hello, 
```
这也是 shell 最受人诟病的问题之一，因为其难以调试。

#### `export`

在使用交互式 shell（shell会话）时，可直接进行变量赋值：
```bash
NAME=virtualguard
```
但这样的变量设置存在一个问题，当我们想要在当前 shell 会话中通过脚本调用这个变量时，shell解释器并不会“设置”这个变量：
```sh
#!/bin/sh
set -u

echo "hello, $NAME"
NAME=vg
echo "hello, $NAME"
```
```bash
./test.sh
./test.sh: 行 4: NAME: 未绑定的变量
```
这是因为在执行一个shell脚本时，系统会启动一个新的shell进程来完成这一操作，这是前文中提到的**shebang**的作用效果，即**独立指定运行脚本的解释器**，从而**隔离**了脚本与当前shell会话（父进程）的环境；一旦脚本退出，对应的环境就会销毁。这也就解释了为什么shebang可以设置为任何与脚本内容对应的解释器。

!!! note inline end
    注意在设置变量（如使用`export`）时不需要在变量前添加`$`，但在获取变量值时则需要添加。

    若需要将变量名用于拼接，可使用`{}`将变量名包裹起来，注意引号：
    ```sh
    read APP
    echo "Create ${APP}.conf for config"
    touch "${APP}.conf"
    ```

熟悉 Linux 的话应该知道可使用`export`命令在当前 shell 会话设置环境变量来解决这个问题，使得变量能够传递给子进程：
```bash
export NAME
NAME=virtualguard

# Or for one step
export VAR=virtualguard
./test.sh
hello, virtualguard
hello, vg
```

!!! info
    还有两种方法：
    ```bash
    # Set the variable at the same line with executed command
    NAME=virtualguard ./test.sh  #  valid only on this command

    # Execute in current shell
    source ./test.sh  # or . ./test.sh
    ```

## 转义字符

在 shell 中，部分字符具有特殊意义，如 `"` 被 shell 解释器用于定义字符串边界，会影响 shell 对文本参数的解释。

但在某些场景我们可能希望不希望这些字符被 shell 解释，而是直接在终端上输出它们；若尝试直接在命令或脚本中拼接它们，例如：
```bash
echo "hello, " world! ""
```

!!! note inline end
    `world`两端与`"`间是否存在空格是有区别的，前者 shell 认为这段信息有三个参数，而后者则只有一个参数，可通过`ls`命令验证这一点：
    ```bash
    ls "hello, " world! ""
    ls: 无法访问 'hello, ': 没有那个文件或目录
    ls: 无法访问 'world!': 没有那个文件或目录
    ls: 无法访问 '': 没有那个文件或目录

    ls "hello "world""
    ls: 无法访问 'hello world': 没有那个文件或目录
    ```

解释器则会将上面的文本信息解释为以下三个参数：

1. `"hello, "`

2. `world!`

3. `""`

然后输出：
```bash
hello,  world!
```
这显然不是预期的结果。

使用`\`对这类符号进行**转义**操作：
```bash
echo "hello, \"world\""
hello, "world
```

!!! note
    大部分特殊字符(e.g. `*`, `'`, etc)在`"`的包裹下不会被 shell 解释，而是直接输出：
    ```bash
    echo *
    build.py docs LICENSE mkdocs.yml overrides README.md requirements.txt scripts

    echo "*"
    *
    ```
    常用的，且被`"`包裹仍会被 shell 解释的特殊字符有 `"`、`$`、`\`。想要输出它们就需要使用转义字符


## 循环控制语句

### `for`循环

语法如下：
```sh
for __var__ in __var_list__
do
    # .....
done
```
**e.g.**

!!! note inline end
    这里的`*`就是**通配符**，表示当前路径下的所有文件和文件夹；如果对其使用转义字符(`\*`)，则会直接输出`*`本身
    ```bash
    ./test.sh
    Looping ... i is set to hello
    Looping ... i is set to 1
    Looping ... i is set to *
    Looping ... i is set to 2
    Looping ... i is set to goodbye
    ```

```sh
#!/bin/sh
set -ue

for i in 1 * goodbye
do
    echo "Looping ... i is $i"
done
```
```bash
./test.sh
Looping ... i is set to 1
Looping ... i is set to test.sh
Looping ... i is set to goodbye
```

### `while`循环

语法如下：
```sh
while [ __condition__ ]
do
    # .....
done
```

**e.g.**

- 

!!! tip inline end
    `:`表示死循环，在 shell 中还有以下方法表示死循环(表达式为“真”):

    - 使用`true`
    ```sh
    while true
    do
        # .....
    done
    ```

    - 使用数值 1(注意[ ])
    ```sh
    while [ 1 ]
    do
        # .....
    done
    ```

    - 使用字符串(注意[ ])
    ```sh
    while [ "true" ]
    do
        # .....
    done
    ```

```sh
#!/bin/sh
set -ue

while :
do
    echo "You're welcome to leave some message here, type \"^C\" to quit"
    read INPUT
    echo "You typed $INPUT"
done
```
```bash
./test.sh
You're welcome to leave some message here, type "^C" to quit
hello
You typed hello
You're welcome to leave some message here, type "^C" to quit
5
You typed 5
You're welcome to leave some message here, type "^C" to quit
bye
You typed bye
You're welcome to leave some message here, type "^C" to quit
^C
```

- 

```sh
#!/bin/sh
set -ue

while read input_text 
do
    case $input_text in
        hello)      echo English    ;;
        howdy)      echo American   ;;
        你好)       echo Chinese    ;;
        *)          echo "Unknown Language: $input_text"    ;;
    esac
done < test.txt
```
!!! tip inline end
    这个例子用于从文件中读取信息并进行匹配。其中使用了`case`语句，它的用法类似于 C 中的`switch...case...`语句，后文我们会再介绍。

假设有`test.txt`：
```txt
hello
你好
howdy
hola
```
则：
```bash
./test.sh
English
Chinese
American
Unknown Language: hola
```

## 测试(`test`)与条件控制语句
