---
title: C++基础
categories:
  - 编程语言
excerpt: 该笔记基于课程cs106l的学习，简单记录一些cpp的重要特性以及先前不曾了解的cpp特性。
tags:
  - C++
abbrlink: 44178
date: 2025-05-05 20:39:48
cover:
---

## 基础类型与结构体

### 基础数据类型

加上STL（Standard Template Library, 标准模板库）中的`string`类型，C++共有六种基本类型：

```cpp
int num = 5;        
char c = 'e';       
float num = 5.0;    
double num = 5.00;  
bool val = true;    
std::string = "101";
```

C++是静态类型语言，也称强类型语言。其中的变量、函数返回值类型需要在声明或定义时显式声明。

>**静态类型语言（编译型语言）** vs **动态类型语言（解释型语言）**  
>静态类型语言：  
> - 类型检查在编译时、运行前进行；类型检查严格，类型错误只可能发生在编译时  
>
>动态类型语言：
> - 类型检查在程序解释并运行时（**`runtime`**）进行。解释器自行判定变量、函数类型，可能导致意料之外的运行结果

### 函数重载

严格的类型检查机制使得C++可同时存在多个不同返回值类型的同名函数，称为**函数重载**

**e.g**:

```cpp
int half(int x, int divisor=2) {  // version (1)
    return x / divisor;
}

double half(double x) {           // version (2)
    return x / 2;
}

int main() {
    half(2);     // uses (1) returns 1
    half(5, 5);  // uses (1) returns 1
    half(2.0);   // uses (2) returns 1.000...
}
```


### `auto` 关键字

`auto`关键字可使编译器在编译时根据上下文信息自行判定变量或函数返回值的类型。注意不要混淆——使用`auto`时，类型检查仍是在编译时进行，并不是像解释型语言那样在程序运行时进行。

>**NOTE**
>
>`auto`关键字一般用于以下两种情况：  
>
> - 修饰变量的类型显而易见时
>
> - 变量类型编写过于冗长且明确时
>
>二者的目的均为提高生产效率

下面是`auto`的一个使用案例：

```cpp
#include <cmath>
#include <iostream>
#include <cassert>

using quadratic = std::pair<bool, std::pair<double, double>>;

quadratic quadraticSolution(double a, double b, double c) {
    assert (a != 0)

    double delta = b*b - 4*a*c;
    std::pair<double, double> solution = {
        (-b + sqrt(delta)) / 2*a,
        (-b - sqrt(delta)) / 2*a
    }

    if (delta < 0) {
        return {false, {std::nan(""), std::nan("")}};
    } else {
        return {true, solution};
    }
}

int main() {
    auto sol = quadraticSolution(1, -2, 1);

    return 0;
}
```

在上面的代码中，我们定义并使用了一个二元一次方程的求根函数，其中函数返回值的类型是我们定义的一个别名`quadratic`。在`main`函数中我们调用该函数时，我们通过`auto`关键字将接受该函数返回值的变量`sol`的类型交由编译器判定，编译时，编译器就会自动将`sol`的类型解析为`quadratic`，即`std::pair<bool, std::pair<double, double>>`。

### 结构体（`struct`）

本质上是一组变量，每个变量可拥有不同的类型。结构体可作为参数传递，也可作为函数返回值。

**e.g**：

```cpp
struct Student {
    std::string name;
    long int id;
    int age;
};

Student s1;
s1.name = "Ben";
s1.id = 110100010;
s1.age = 22;

Student s2 = {"A", 1010001001, 22};

void printStudentInfo(Student s) {
    std::cout << s.name << ': ' << s.id << '\n';
}

Student setStudentInfo(std::string name, long int id, int age) {
    Student s;
    s.name = name;
    s.id = id;
    s.age = age;
    return s;
}
```

前面我们提到`auto`关键字时曾使用了STL中的`std::pair`，其本质上也是结构体的一种，因此，`quadraticSolution`中的`solution`变量也可以使用以下形式替代：

```cpp
struct Solution {
    double x1;
    double x2;
};

Solution solution = {
    (-b + sqrt(delta)) / 2*a,
    (-b - sqrt(delta)) / 2*a
}
```

二者在效果上是一致的。

## 初始化和引用操作(`&`)

### 初始化

在C++中，变量初始化有三种方式：**直接初始化**、**统一初始化**和**结构化绑定**。

#### 直接初始化

直接初始化使用**赋值操作符**`=`或包含常量值的括号`()`进行：

```cpp
#include <iostream>

int main() {
    int num = 5;
    double val(5.5);

    std::cout << "num = " << num << " val = " << val << '\n';

    return 0;
}
```

然而在使用直接初始化可能会出现一个致命问题：**数据丢失**。

假设有以下程序，需要传递并操作一个重要参数：

```cpp
#include <iostream>

int main() {
    int criticalSystemVal(5.5); // Direct initialization with a float-point value

    // Some system operation
    // .....
    
    std::cout << "Critical system value: " << criticalSystemVal << '\n';

    return 0;
}
```

编译并执行后上述程序后，结果如下：

```bash
Critical system value: 5
```

可以看出，当初始化的数据类型与声明类型不对应时，变量`criticalSystemVal`的数据出现了丢失。

在直接初始化中，编译器不会对变量和赋值数据进行严格的类型检查，因此极易触发**窄化转换（Narrow Conversion）**导致数据失真，这在数据精确度要求较高的项目环境中是一个致命的问题。

#### 统一初始化

为了提供一种一致、简化和更加安全的对象初始化方法，C++11标准中引入了一种新的初始化语法，称为**统一初始化(Uniform initialization)**。统一初始化使用大括号`{}`进行，语法如下：

```cpp
#include <iostream>

int main() {
    int num{5};
    double val{5.5};

    std::cout << "num = " << num << " val = " << val << '\n';

    return 0;
}
```

若对上文的变量`critialSystemVal`使用统一初始化：

```cpp
#include <iostream>

int main() {
    int criticalSystemVal{5.5}; // Uniform initialization with a float-point value

    // Some system operation
    // .....
    
    std::cout << "Critical system value: " << criticalSystemVal << '\n';

    return 0;
}
```

编译时就会出现如下错误：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:4:30: error: narrowing conversion of ‘5.5e+0’ from ‘double’ to ‘int’ [-Wnarrowing]
    4 |     int criticalSystemVal{5.5}; // Direct initialization with a float-point value
      |                              ^
```

使用统一初始化方法对变量进行初始化，编译时编译器就会对变量类型与初始化值进行严格的类型检查，从而将因类型问题导致的数据失真问题拦截在编译时，使程序更加**安全**的同时提升代码可读性与**一致性**。

**一致性**是指任何数据类型和对象都可使用统一初始化方法进行初始化，如：

```cpp
// Map
std::map<int std::string> id{
    {"A", 101},
    {"B", 102}
};

// Vector
std::vector<int> nums{1, 2, 3, 4, 5};

// Struct
struct Student {
    std::string name;
    long int id;
};
Student s{"A", 100100101};

// Other objects in cpp.....
```

#### 结构化绑定

C++17引入了了一个新特性，称为**结构化绑定**。结构化绑定是一种从固定大小的多变量数据结构（元组、数组、结构体、`std::pair`）初始化变量的初始化方式，其允许通过返回多变量数据结构的函数访问对象的数据成员。

直接通过定义理解可能会比较抽象，下面给出语法实例：

```cpp
#include <iostream>
#include <tuple>

// tuple returned by funtion
std::tuple<std::string, std::string> getClassInfo() {
    std::string classCode = "CS106L";
    std::string programLanguage = "C++";
    return {classCode, programLanguage};
}

// use struct
struct Person {
    std::string name;
    int age;
};

int main() {
    // binding
    auto [classCode, programLanguage] = getClassInfo();
    // or 
    auto classInfo = getClassInfo();
    std::string classCode = std::get<0>(classInfo);
    std::string programLanguage = std::get<1>(classInfo);

    // binding from struct
    Person person{"A", 19};
    auto [name, age] = person;

    // binding from array
    int arr[]{1, 2, 3, 4, 5};
    auto [a, b, c, d, e] = arr;

    return 0;
}
```

结构化绑定为多变量聚合性数据结构提供了一个简洁高效的初始化方式。注意使用时需确保绑定变量和对象成员数量相同。

### 引用(`&`)

#### 引用基础

声明具名变量为引用，即既存对象或函数的别名。（Declares a named variable as a reference, that is, an alias to an already-existing object or function.）

引用使用操作符`&`(ampersand)，语法如下：

```cpp
int num = 5;
int& ref = num;
ref = 10; // Assigning a new value through the reference.
std::cout << num << '\n';  // Output 10
```

在上面的代码中，`num`是一个`int`型变量，被初始化为`5`。`ref`是一个`int&`类型变量，是变量`num`的**别名**。

因此当我们将`10`赋值给`ref`时，会同时改变变量`num`的值，等效于直接将`10`赋给`num`。

可视化：

```md
int num = 5;                int &ref = num;              ref = 10;

 Memory
---------                   ---------                    ----------
|   5   | 0 <-- num         |   5   | 0 <-- num          |~~5~~ 10| 0 <-- num
---------                   ---------   \                ----------   \
|       | 1                 |       | 1  -> ref          |        | 1  -> ref
---------                   ---------                    ---------- 
|       | 2         ====>   |       | 2          ====>   |        | 2
---------                   ---------                    ----------
|       | 3                 |       | 3                  |        | 3
---------                   ---------                    ----------
|       | 4                 |       | 4                  |        | 4
---------                   ---------                    ----------
```

#### 通过引用传递变量

向函数传递引用变量在C++中是一个常见且重要的操作。

```cpp
#include <iostream>
#include <math.h>

void square(int& x) { // n is a referenced value!
    x = std::pow(n, 2);
}

int main() {
    int n = 5;
    square(n);
    std::cout << n << '\n'; // Output 25

    return 0;
}
```

通过引用传参的本质是对内存中的值直接进行操作，**避免拷贝**，提高函数调用效率。对变量的引用同理。

若通过拷贝进行参数传递，拷贝的变量值需要额外占用内存空间。这在降低效率的同时也意味着拷贝变量受**作用域**约束，当接收变量的函数在调用完成后，其栈帧空间被释放，拷贝变量也随之丢失。同时由于函数的操作只作用在拷贝变量上，因此这些操作在函数调用完成后不会反映在原参数上，具体表现为被传递参数的值并不会改变。

简易可视化：

```cpp
#include <iostream>
#include <math.h>

void square(int x) { // Passing n without referenced
    n = std::pow(n, 2);
}

int main() {
    int n = 5;
    square(n);
    std::cout << n << '\n'; // Output 5

    return 0;
}
```

```md
In main()          Calling void square(int x)     After calling square(int x)

 Memory
---------   ---             ---------   ---              ---------   ---
| n = 5 | 0  |              | n = 5 | 0  |               | n = 5 | 0  |
---------  main()           ---------  main()            ---------  main()
|       | 1  |              |       | 1  |               |       | 1  | 
---------   ---             ---------   ---              ---------   ---
|       | 2       ====>     |       | 2          ====>   |       | 2
---------                   ---------    ---             ---------
|       | 3                 | x = 25| 3   |              |       | 3
---------                   ---------  square()          ---------
|       | 4                 |       | 4   |              |       | 4
---------                   ---------    ---             ---------
```

但若是最初采用引用的版本，则调用`square`时，由于其在传参时使用了引用，其对`x`的操作就会直接反映在从`main`函数传递的`n`上：

```md
In main()           Calling void square(int& x)   After calling square(int& x)

 Memory
---------   ---             ---------   ---              ---------   ---
| n = 5 | 0  |            ->| n = 5 | 0  |               | n = 25| 0  |
---------  main()         | ---------  main()            ---------  main()
|       | 1  |            | |       | 1  |               |       | 1  | 
---------   ---           | ---------   ---              ---------   ---
|       | 2       ====>   | |       | 2          ====>   |       | 2
---------                 | ---------    ---             ---------
|       | 3               --|   x   | 3   |              |       | 3
---------                   ---------  square()          ---------
|       | 4                 |       | 4   |              |       | 4
---------                   ---------    ---             ---------
```

#### 引用案例

```cpp
#include <iostream>
#include <cmath>
#include <vector>

void shift(std::vector<std::pair<int , int>>& nums) { //Passed in by reference
    for(auto& [num1, num2]: nums) { // In for-each, note the ampersand(&) after auto
        num1++;
        num2++;
    }
}
```

在上面的代码中，需要特别注意`for-each`中`auto`后的`&`。`for-each`中的操作是典型的**结构化绑定**，在绑定过程中，`auto`提示编译器自动判定变量类型。若未进行显式声明，在这里`num1`和`num2`就会被判定为`int`型而不是引用类型`int&`，函数对这两个变量的操作也就不会对通过引用传递的对象`nums`生效。这种现象被称为**剥离引用**。

#### 左值与右值

左值可以位于等号的左侧或右侧：

```cpp
int x = 1;
int y = x;
```

右值只能位于等号的右侧：

```cpp
int n = 0;
0 = m;  // Error!
```
同时，我们认为右值是**临时值**。

现有以下代码：

```cpp
#include <iostream>
#include <cmath>

void square_L(int& x) {
    x = std::pow(x, 2);
}

int main() {
    int n = 5;
    square_L(n);
    square_L(5);    // Error
 
    return 0;
}
```
编译以上代码，我们会得到类似如下的错误：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:23:14: error: cannot bind non-const lvalue reference of type ‘int&’ to an rvalue of type ‘int’
   23 |     square_L(5);
      |              ^
demo.cpp:4:20: note:   initializing argument 1 of ‘void square_L(int&)’
    4 | void square_L(int& x) {
      |               ~~~~~^
```

对于引用操作而言，在一次引用中确定了一个引用对象，我们就无法改变这个引用所指向的对象（注意不是对象的值，不要混淆）。由于我们认为右值是**临时的**，故在引用中我们不能传递右值。

但自C++11起，cpp引入了一种新的语法，使得我们可以在引用中传递右值。

我们可以通过使用操作符`&&`显式声明一个右值引用：

```cpp
#include <iostream>
#include <cmath>

void square_R(int&& x) {
    x = std::pow(x, 2);
}

int main() {
    square_R(5);

    return 0;
}
```
上面的操作称为**右值引用**，前文的则称为**左值引用**。更多关于引用的用法，可参考[cppreference](https://zh.cppreference.com/w/cpp/language/reference)

### `const` 关键字

`const`关键字用于在修饰对象时声明对象的值**不可修改**。

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec{1, 2, 3}; // normal vector
    const std::vector<int> const_vec{1, 2, 3}; // a const vetor
    std::vector<int>& ref{ vec }; // a reference to 'vec'
    const std::vector<int> const_ref{ vec }; // a const reference

    vec.push_back(3);
    const_vec.push_back(3); // error! it's const!
    ref.push_back(3);
    const_ref.push_back(3); // this is const too!

    return 0;
}
```

若尝试编译上述源码，则会产生以下错误信息：

```bash
demo.cpp: In function ‘int main()’:
demo.cpp:11:24: error: passing ‘const std::vector<int>’ as ‘this’ argument discards qualifiers [-fpermissive]
   11 |     const_vec.push_back(3);
      |     ~~~~~~~~~~~~~~~~~~~^~~
In file included from /usr/include/c++/11/vector:67,
                 from demo.cpp:2:
/usr/include/c++/11/bits/stl_vector.h:1203:7: note:   in call to ‘void std::vector<_Tp, _Alloc>::push_back(std::vector<_Tp, _Alloc>::value_type&&) [with _Tp = int; _Alloc = std::allocator<int>; std::vector<_Tp, _Alloc>::value_type = int]’
 1203 |       push_back(value_type&& __x)
      |       ^~~~~~~~~
demo.cpp:13:24: error: passing ‘const std::vector<int>’ as ‘this’ argument discards qualifiers [-fpermissive]
   13 |     const_ref.push_back(3);
      |     ~~~~~~~~~~~~~~~~~~~^~~
In file included from /usr/include/c++/11/vector:67,
                 from demo.cpp:2:
/usr/include/c++/11/bits/stl_vector.h:1203:7: note:   in call to ‘void std::vector<_Tp, _Alloc>::push_back(std::vector<_Tp, _Alloc>::value_type&&) [with _Tp = int; _Alloc = std::allocator<int>; std::vector<_Tp, _Alloc>::value_type = int]’
 1203 |       push_back(value_type&& __x)
      |       ^~~~~~~~~
```

使用`const`修饰的对象在引用时也必须在引用声明前加上`const`修饰：

```cpp
#include <iostream>
#include <vector>

int main() {
    const std::vector<int> nums{1, 2, 3, 4, 5};

    std::vector<int>& ref{ nums }; // Bad work
    const std::vector<int>& ref{ nums }; // OK!

    return 0;
}
```

## 流

在C++中，流(`stream`)是一个十分重要的概念，它是**I/O（Input/Output, 输入输出）的一般抽象**，表示数据的流动方向和方式。

>**Note**
>
>抽象（Abstractions）通常为各种操作提供一个统一的**接口（Interface）**。在这里，`stream`就是**数据读写**的接口。

### 标准输入输出流

最常用的标准输入输出流就是`cin`和`cout`了，他们工作时分别从控制台读取数据和向控制台输出数据。

在标准输入输出流中，还有两个输出流：

- `cerr`：**标准错误输出流**，用于输出错误信息。与`cout`的不同在于不会被缓冲，会立即输出
- `clog`：**标准日志输出流**，用于输出非关键日志信息。与`cerr`类似，但会进行缓冲

更多信息可参考[Difference between cerr and clog | GeeksForGeeks](https://www.geeksforgeeks.org/difference-between-cerr-and-clog/)

#### `std::cin`/`std::cout`

```cpp
#include <iostream>

int main() {
    double pi;
    std::cin >> pi;
    // verify the value of pi
    std::cout << pi << '\n';

    return 0;
}
```
编译并执行上述cpp程序，我们在终端输入`3.14`，终端最终返回`1.57`。

这里就会有一个疑问：从终端读取的数据显然是数据的**字符表示形式**，而程序中的`pi`是`double`型的，中间是否有什么处理或转换的过程呢？

答案是肯定的。作为I/O的一般抽象，`stream`允许以一种通用的方式处理来自外部的数据。

本质上，所有的`stream`都可以归为`Input stream(I)`和`Output stream(O)`中的一种。对于相同类型的输入输出流，它们在数据源/目标是互补的。在后面的章节中，我们还会详细介绍这两个流。

### 字符串流

字符串流将字符串视为流，用于在内存中处理数据，在处理多中数据类型混合的应用场景是一个高效的处理接口。

`std::stringstream`示例：

```cpp
#include <string>
#include <iostream>
#include <sstream>

void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot"; 
    
    /// create a stringstream
    std::stringstream ss(initial_quote);
    // another way to insert 'initial_quote'
    // std::stringstream ss;
    // ss << initial_quote;
    
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
        
    ss >> first >> last >> language >> extracted_quote;
    std::cout << first << " " << last << " said this: "<< language << " " << extracted_quote << std::endl;
}

int main() {
    foo();
    return 0;
}
```
在上面的示例中，我们为字符串变量`initial_quote`创建了一个字符串流`ss`，并通过`>>`（输出流操作符）将流数据++从原始数据移动到`first`、`last`等目的地++。这就是流的作用，即**将数据从内存中的一个地方移动到另一个地方**。将数据比作货物，流就是装载货物的货车，而创建数据流的过程就是将货物装车的操作。

但上面的程序存在一个小小的bug：

这是上述程序编译并执行的结果：
```bash
Bjarne Stroustrup said this: C makes
```
这显然不是我们预期的结果，那么为什么呢？

通过数据流，我们将变量字符串变量`initial_quote`的第一第二以及第三个单词分别从字符串流`ss`移动到了字符串变量`first`、`last`和`language`上。接下来，我们的预期是将`initial_quote`的剩余部分全部赋给`extracted_quote`，但是`>>`（输出流操作符）在读取数据时遇到空格就会停止，因此数据流只转移了一个单词。

解决方法是使用`std::getline()`：

```cpp
#include <iostream>
#include <string>
#include <sstream>

void foo() {
    /// partial Bjarne Quote
    std::string initial_quote = "Bjarne Stroustrup C makes it easy to shoot yourself in the foot";
    
    /// create a stringstream
    std::stringstream ss(initial_quote);
    
    /// data destinations
    std::string first;
    std::string last;
    std::string language, extracted_quote;
    ss >> first >> last >> language;
    std::getline(ss, extracted_quote);
    std::cout << first << " " << last << " said this: \'" << language << " " << extracted_quote + "‘" << std::endl;
    }

    
int main() {
    foo();
    return 0;
}
```

下面是`std::getline()`的定义：

```cpp
istream& getline(istream& is, std::string& str, char delim)
```
`std::getline()`读取输入流`is`，**直到遇到字符型分隔符`delim`**，并将数据存入字符串型缓存`str`中。其中`delim`的默认值为`\n`。

### 输出流

#### `std::cout`

`Output Stream`用于将数据写入目标地址或外部设备，例如`std::cout`将数据写入控制台。实际操作时，我们使用操作符`<<`将数据写入输出流。

输出流的数据在加载至目标区域前会事先存储在中间缓存中：

```md
                        Buffer
double n = 5.50         -------------------------             ---------
std::cout << n;  ====>  | 5 | . | 5 | 0 |   |   |    ======>  |>_     |
                        -------------------------             |       |
                                                              ---------
```

`std::cout`输出流是**行缓冲流**。缓冲区中的数据不会显示在控制台上，直到缓冲区执行刷新（flush）操作。

#### `std::endl`

`std::endl`用于提示`cout`当前数据流到达行末，需要进行换行操作。

```cpp
int main() {
    for (int i=0; i < 5; i++) {
        std::cout << i << std::endl;
    }

    return 0;
}
```
result:
```bash
0
1
2
3
4
```

如果去掉上面的`std::endl`，结果就会变成这样：
```bash
01234
```

换行的同时，`std::endl`还会提示流进行刷新（flash）操作，下面是该过程的可视化：

```md
Buffer
------------------  flash   ------------------  flash
| 1 |'\n'|   |   |   ===>   | 2 |'\n'|   |   |   ===> ......
------------------          ------------------
```

每个数在被放入流后都会立即刷新，直接输出到控制台上。使用`\n`的情况相同，详情可参考[std::endl | cppreference](https://zh.cppreference.com/w/cpp/io/manip/endl)

#### 文件输出流

文件输出流用于将数据流写入文件，其具有数据类型`std::ofstream`。在实际操作中，我们使用操作符`<<`将数据流传输至文件。

下面是具体用法：

```cpp
#include <fstream>

int main() {
  /// associating file on construction
  std::ofstream ofs("hello.txt");
  if (ofs.is_open()) {
    ofs << "Hello CS106L !" << '\n';
  }
  ofs.close();
  ofs << "this will not get written";

  /* try adding a 'mode' argument to the open method, like std::ios:app
   * What happens?
   */
  ofs.open("hello.txt");
  ofs << "this will though! It’s open again";
  return 0;
}
```

要使用文件输出流，我们首先要创建一个具有类型`std::ofstream`的流。上面的示例中：  
- `ofs(hello.txt)`创建了一个指向`hello.txt`的文件输出流`ofs`
- 使用`is_open()`检查文件输出流是否打开
- 使用`<<`尝试写入数据
- 写入第一行数据后，使用`close()`关闭文件输出流
- 文件关闭后，无法向文件中写入数据
- 使用`open()`再次打开文件输出流`ofs`
- 打开文件输出流后，可继续向文件写入数据

在关闭文件输出流并进行再次打开的操作时，如不希望已写入文件的数据被覆盖，可在`open()`方法的参数中添加追加模式的标签：
```cpp
ofs.open("hello.txt", std::ios::app)
```

#### 文件输入流

文件输入流用于从文件读取数据，本质与文件输出流相同。

假设有文件`input.txt`，其内容如下：

```txt
line1
line2
```
在相同路径下编译并执行以下程序：

```cpp
#include <fstream>
#include <iostream>

int main() {
  std::ifstream ifs("input.txt");
  if (ifs.is_open()) {
    std::string line;
    std::getline(ifs, line);
    std::cout << "Read from the file: " << line << '\n';
  }
  if (ifs.is_open()) {
    std::string lineTwo;
    std::getline(ifs, lineTwo);
    std::cout << "Read from the file: " << lineTwo << '\n';
  }
  return 0;
}
```
则会得到如下结果：
```bash
Read from the file: line1
Read from the file: line2
```

### 输入流

在文件流中我们简要了解了文件输入流的用法，下面我们将详细学习输入流的概念与应用。

输入流用于从目标或外部数据源读取数据，其具有数据类型`std::istream`。实际操作中，我们使用`>>`从输出流中读取数据。

#### `std::cin`

与`std::cout`相同，`std::cin`也是行缓冲流。可将`std::cin`的行缓冲区理解为用户暂存数据，随后从中读取数据的区域。

需要注意的是，`std::cin`的缓冲区遇到空格时会停止接受数据。

```cpp
int main() {
    double pi;
    std::cin;
    std::cin >> pi;

    std::cout << pi << '\n';

    return 0;
}
```

在上面的示例中：
- 最开始时缓冲区为空，所以首个`std::cin`会提示用户进行输入
- 到第二个`std::cin`时，缓冲区中不为空，所以`cin`会从其中读取数据，直到遇到空格，并将数据存入变量`pi`

在日常开发中，我们通常直接将输入操作与数据流转移写在同一个语句：

```cpp
int main() {
    double pi;
    std::cin >> pi;

    std::cout << pi << '\n';

    return 0;
}
```

与在了解字符串流时遇到的一个问题类似，`std::cin`在从目标读取数据时，遇到空格就会停止读取数据：

```cpp
#include <iostream>

void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::cin >> name;
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetlineBug();
    return 0;
}
```
```bash
3.14
Benjamin C
my name is : Benjamin tao is : 0 pi is : 3.14
```
程序甚至还未等到我们输入第三个数据就停止从控制台读取数据了。这是由于在读取第二个数据时，`cin`缓冲区不为空，因此它在读取数据时遇到空格后就立刻停止继续读取数据：

```md
Buffer
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
                            ^
                     stop read data here
```

那么有了之前字符串流的修复经验，你可能会给出以下修复版本：

```cpp
#include <iostream>

void cinGetlineBug() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetlineBug();
    return 0;
}
```
然而，实际的执行效果却是这样的：
```bash
3.14
Benjamin C
my name is :  tao is : 0 pi is : 3.14
```
这次甚至连第二个数据也丢失了🤯.....

事实上，第二个数据并不是“丢失了”，而是`getline()`的特性导致的：

在介绍字符串流时，我们曾介绍过`std::getline()`的定义，其中提到了，**`getline()`默认将`\n`作为字符分隔符，并在遇到它时“消耗它”并停止继续读取数据**，那么针对上面失败的修改我们可以想象出如下可视化过程：

```md
Buffer   std::cin >> pi;
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
        ^               pi: 3.14
                || 
                \/

   std::getline(std::cin, name);
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
           ^            pi: 3.14
                        name: ""
         std::cin >> tao;
-----------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|
-----------------------------------
            ^^^^^^^^^^^^^^^^^^^^
The buffer is not empty, and cin try to read the part, but 'tao' is double type!
                        pi: 3.14
                        name: ""
                        tao: 🗑
```

那么应该如何修复这个问题呢？

既然`getline()`在遇到`\n`时会“消耗它”并停止读取数据，那么我们不妨在第一个`getline()`消耗`\n`后在添加一个`getline()`来读取`name`的内容：

```cpp
#include <iostream>

void cinGetline() {
  double pi;
  double tao;
  std::string name;
  std::cin >> pi;
  std::getline(std::cin, name);
  std::getline(std::cin, name);
  std::cin >> tao;
  std::cout << "my name is : " << name << " tao is : " << tao
            << " pi is : " << pi << '\n';
}

int main() {
    cinGetline();
    return 0;
}
```
这时再执行程序，bug也就被修复了：
```bash
3.14
Benjamin C
5
my name is : Benjamin C tao is : 5 pi is : 3.14
```

其可视化过程如下：

```md
Buffer   std::cin >> pi;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
        ^               pi: 3.14
                || 
                \/

   std::getline(std::cin, name);
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
           ^            pi: 3.14
                        name: ""
                || 
                \/

   std::getline(std::cin, name);
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
                                  ^
                        pi: 3.14
                        name: "Benjamin C"
                || 
                \/

         std::cin >> tao;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n| |  |
----------------------------------------
                                   ^
The stream now is empty, so is going to promot user for input!
                        pi: 3.14
                        name: "Benjamin C"
                        tao: 
                || 
                \/

         std::cin >> tao;
----------------------------------------
|3|.|1|4|\n|B|e|n|j|a|m|i|n| |C|\n|5|\n|
----------------------------------------
                                       ^
                        pi: 3.14
                        name: "Benjamin C"
                        tao: 5(double)
```

事实上，在实际应用的过程中，由于`cin`和`getline()`解析数据的方式有所差异，我们并不会在一个场景内同时使用二者。但确有需求的话，像上面的操作也是可行的，但还是不建议这样做。

## 容器

容器（container），在C++中指一种能将其他对象聚合在一起，并能够通过某些方式与它们交互的对象。在前面的章节中，我们在程序中使用的`vector`就是容器的一种。

通常情况下，容器会提供一些标准、基本的功能：

- 允许储存相同类型的多个对象
- 允许使用某种方式访问容器内的元素，同时允许对所有元素进行**迭代操作**
- 可以对元素进行编辑/删除操作

容器在形式上可分为两种：**序列容器**和**关联容器**

### 序列容器

在序列容器中，元素能够按顺序访问。我们通常将具有线性规律的数据存放在序列容器中。

在实际开发中，我们最常使用的序列容器通常有`std::vector`和`std::deque`

#### `std::vector`

`vector`是由若干相同数据类型元素组成的**大小可变**的**有序集合**。本质上，`vector`就是一个大小可变的数组。

STL为`vector`提供了以下常用方法：

| 语法 | 效果 |
|:---:|:----------------:|
|`std::vector<int> nums`| 创建一个`int`型空向量`nums` |
|`std::vector<int> nums(n)`| 创建包含`n`个`int`型默认值的向量 |
|`std::vector<int> nums(n, e)`| 创建包含`n`个`int`型，且数值为`e`的向量 |
|`nums.push_back(e)`| 在`nums`的末端追加元素`e` |
|`nums.pop_back()`| 删除`nums`的最后一个元素，但**并不会返回这个元素** |
|`nums.empty()`| 检查`nums`是否为空，并返回一个`bool`值 |
|`int e = nums[i]` `nums[i] = e`| 访问或写入引索为`i`的元素。**不进行边界检查（若超出边界则直接返回默认值或添加写入元素）** |
|`int e = nums.at(i)` `nums.at(i) = e`| 同上，但**执行边界检查**，超出边界则抛出错误|
|`nums.clear()`| 清空`nums`的所有元素|

#### `std::deque`

与`std::vector`类似，但可从**两端**进行元素的插入或删除操作。

关于`std::vector`与`std::deque`的底层原理可直接参考[CS106L的textbook](https://cs106l.github.io/textbook/containers/sequence-containers)

有关序列容器应用场景/特性与实现效率之间的关系，可使用以下表格概括：

| 使用场景 | `std::vector` | `std::deque` | `std::list` |
|:-------:|:-------------:|:------------:|:-----------:|
| 在前端插入/删除元素 | slow | fast | fast |
| 在末端插入/删除元素 | super fast | very fast | fast |
| 访问元素 | super fast | fast | x |
| 在内部插入/删除元素 | slow | fast | very fast |
| 内存占用率 | low | high | high |
| 组合操作（拼接/连接）| slow | very slow | fast |
| 稳定性（用于迭代/并发操作）| bad | very bad | good |
*以上表格来源于[CS106L](https://web.stanford.edu/class/cs106l/)的课程幻灯片。*

对于序列容器，请记住以下几个要点：
- 需要对数据强制设定某种顺序时使用
- `std::vector`可解决大多数应用场景
- 需要在容器开头插入元素时，`std::deque`可能会是高效的选择
- 若需要将数据进行连接或与多个列表进行关联操作，考虑使用`std::list`（这种情况非常少见）

### 关联容器

与序列容器不同，关联容器中并没有强制的线性顺序。同时，“关联”意味着其中的数据存在某种**映射关系**，这也使得其中的数据更加容易查找。在概念上，关联容器类似于`Python`中的`dict`和`set`，即**存在唯一键值对的数据**。

常用的关联容器有`std::map<type1, type2>`和`std::set<type>`。还需留意他们的**无序版本**：`std::unordered_map<type1, type2>`、`std::unordered_set<type1>`。注意，不要将这里的有序与无序（存储有序，按照键值进行排序）与序列容器中的线性有序（按照元素插入顺序进行排序）混淆。

#### `std::map<type1, type2>`

`map`基于成对的数据结构实现，在C++中即`std::pair<type1, type2>`。

需要特别注意，键的值必须是`const`的，即不可变的。对`map`进行引索操作（mapName[key]）会首先在成对的数据（`std::pair`）集合中查找第一个属性，即`key`，随后返回它的第二个属性`value`。

#### `unordered_map/set`

这里的无序并不是真正意义上的“无序”，而是将映射关系或元素比较的定义交由用户进行自定义——通常是一个**哈希函数**。在性能方面，一般情况下无序也比有序的要快。

哈希函数本质上就是将一些复杂对象映射为一串数字。对这个数字的计算过程就是所谓的“哈希”。

一个良好的哈希函数通常需要具备以下特征：
- 能够被快速计算
- 输入与输出具有唯一映射性
- 尽可能避免碰撞发生

无序容器的运行速度快，但似乎也就只有“快”而已。在处理嵌套容器/集合时，无序容器的复杂度较高。如需使用复杂的数据类型，或是不熟悉哈希函数，那么建议使用有序容器。

