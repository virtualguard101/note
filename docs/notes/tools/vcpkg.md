# vcpkg

**vcpkg**是微软提供并维护的一个开源的**C++包管理器**，形式上类似于Python的**pip**/**uv**等工具。

- 官方中文文档 & 教程：[vcpkg 文档](https://learn.microsoft.com/zh-cn/vcpkg/)

## 配合CMake进行使用

- 官方教程：[通过 CMake 安装和使用包](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started?pivots=shell-bash#1---set-up-vcpkg)

适合较为轻量的项目。

使用vscode配合CMake的操作差别不大，详情可参考[在 Visual Studio Code 中通过 CMake 安装和使用包](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started-vscode?pivots=shell-bash)

安装过程官方教程有详尽的说明，这里不再赘述。

- 初始化

通过以下命令在项目的目录中创建清单文件：
```bash
vcpkg new --application
```

该命令会在项目的根目录下创建`vcpkg.json`和`vcpkg-configuration.json`。二者的作用分别是**作为依赖项列表**及**引入[基线](https://learn.microsoft.com/zh-cn/vcpkg/reference/vcpkg-configuration-json#registry-baseline)约束**。

- 修改`CMakeLists.txt`

在`CMakeLists.txt`中添加以下内容：
```bash
find_package([your_lib] CONFIG REQUIRED)
```
表示使用第三方库的 CMake 配置文件查找该库。`REQUIRED`关键字确保在找不到包时生成错误。

注意`target_link_libraries`列表中也需添加引入的第三方库名。

- 创建 CMake 配置

参考[官方教程](https://learn.microsoft.com/zh-cn/vcpkg/get_started/get-started?pivots=shell-bash#4---build-and-run-the-project)配置CMake工具链。

!!! note
    `CMakeUserPresets.json` 文件会将 `VCPKG_ROOT` 环境变量设置为指向包含 `vcpkg` 本地安装的绝对路径，因此注意配置完成后将`CMakeUserPresets.json`移入`.gitignore`，以避免信息泄漏等问题。

配置完成后即可进行生成与构建运行。
