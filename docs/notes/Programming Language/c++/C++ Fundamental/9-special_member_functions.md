# 特殊成员函数

## 概述

特殊成员函数指的是一些具有特殊语义和默认行为的成员函数，通常用于对象的生命周期管理、拷贝控制和移动操作等。**特殊成员函数只会在它们被调用和用户显式定义时生成。**

特殊成员函数共有六种：

- **默认构造函数**(*Default constructor*)

- **析构函数**(*Destructor*)

- **拷贝构造函数**(*Copy constructor*)

- **赋值运算符**(*Copy assignment operator*)

- **移动构造函数**(*Move constructor*)

- **移动赋值运算符**(*Move assignment operator*)

```cpp
class Widget {
  public:
    /* Takes no parameters and creates a new object. */
    Widget();                             // default constructor

    /* Creates a new object as member-wise copy of another. */
    Widget(const Widget& w);              // Copy constructor

    /*Assigns an already exisiting object to another. */
    Widget& operator = (const Widget& w); // Copy assignment operator

    /* Called and delete the object when it goes out of scope. */
    ~Widget();                            // Destructor

    Widget(Widget&& rhs);                 // Move constructor
    Widget& operator = (Widget&& rhs);    // Move assignment operator
};
```

最后两个特殊成员函数是我们前面所不曾见过的，我们将在这个章节学习它们。

## 拷贝与赋值(*Copy* & *Copy assignment*)

默认情况下（未重载），拷贝构造函数在被调用时会对对象的每个成员变量进行拷贝，即**逐成员拷贝(*member-wise copy*)**。但这样足够了吗？

如果一个成员变量是指针变量，那么逐成员拷贝就会使新对象的这个成员变量指向相同的已分配的数据，而不是生成一个新的拷贝。

```cpp
template<typename Type>
vector<Type>::vector<Type>(const vector::vector<Type>& other) : 
  _size(other.size),
  _capacity(other.capacity),
  _elems(other.elems) { }
```

在上面的拷贝构造中，针对`_elems`的拷贝就仅仅只是简单地复制了指针或引用。如果成员变量`elems`是一个指针，那么拷贝操作后的新对象和传入这个拷贝构造函数的`other`对象在底层上将**共享同一块内存空间。**具体表现就是**新对象的成员变量`elems`在底层上与旧对象`other`的`elems`指向同一个数组。**

这就是我们通常所说的**浅拷贝(*shallow copy*)**，与之对应的就是**深拷贝(*deep copy*)**。

深拷贝会创建一个与原始对象完全相同且与之相互独立的全新副本。与类的普通成员函数类似，深拷贝的拷贝构造函数需要用户在源文件`.cpp`中自行实现，以覆盖编译器默认的浅拷贝构造。

更多有关浅/深拷贝的内容，可参考[Shallow Copy and Deep Copy in C++ | GeeksForGeeks](https://www.geeksforgeeks.org/shallow-copy-and-deep-copy-in-c/)

