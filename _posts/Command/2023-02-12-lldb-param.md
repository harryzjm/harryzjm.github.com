---  
layout: post  
title: LLDB Parameter  
category: Command  
tags: LLDB  
keywords: LLDB  
---  

__Posted by [Airths](https://blog.csdn.net/Airths/article/details/122421435)__  


# 本文所使用的 LLDB 版本

```bash
(lldb) version
lldb-1200.0.44.2
Apple Swift version 5.3.2 (swiftlang-1200.0.45 clang-1200.0.32.28)
```

# address

```bash
(lldb) help <address>
# 目标程序可执行空间中的有效内存地址
```

# address-expression

```bash
(lldb) help <address-expression>
# 可以被解析为内存地址的表达式
```

# alias-name

```bash
(lldb) help <alias-name>
# 调试器命令的缩写或者别名
```

# arch

```bash
(lldb) help <arch>
# 以下是受支持的 CPU 架构的名称:
arm
armv4
armv4t
armv5
armv5e
armv5t
armv6
armv6m
armv7
armv7l
armv7f
armv7s
armv7k
armv7m
armv7em
xscale
thumb
thumbv4t
thumbv5
thumbv5e
thumbv6
thumbv6m
thumbv7
thumbv7f
thumbv7s
thumbv7k
thumbv7m
thumbv7em
arm64
armv8
armv8l
arm64e
arm64_32
aarch64
mips
mipsr2
mipsr3
mipsr5
mipsr6
mipsel
mipsr2el
mipsr3el
mipsr5el
mipsr6el
mips64
mips64r2
mips64r3
mips64r5
mips64r6
mips64el
mips64r2el
mips64r3el
mips64r5el
mips64r6el
powerpc
ppc601
ppc602
ppc603
ppc603e
ppc603ev
ppc604
ppc604e
ppc620
ppc750
ppc7400
ppc7450
ppc970
powerpc64le
powerpc64
ppc970-64
s390x
sparc
sparcv9
i386
i486
i486sx
i686
x86_64
x86_64h
hexagon
hexagonv4
hexagonv5
unknown-mach-32
unknown-mach-64
arc
```

# bool

```bash
(lldb) help <bool>
# hcg 注: 同 boolean
```

# [boolean](https://so.csdn.net/so/search?q=boolean&spm=1001.2101.3001.7020)

```bash
(lldb) help <boolean>
# 布尔值: true 或者 false
```

# breakpoint-id

```bash
(lldb) help <breakpoint-id>
# hcg 注: 断点编号，同 breakpt-id
```

# breakpoint-id-list

```bash
(lldb) help <breakpoint-id-list>
# hcg 注: 断点编号的列表，同 breakpt-id-list
```

# breakpoint-name

```bash
(lldb) help <breakpoint-name>
# 一个可以在创建断点时添加到断点的名称，或者稍后使用 "breakpoint name add" 命令添加
# 断点名称可用于在所有可以使用断点编号(breakpoint ID)和断点编号范围(breakpoint ID range)的地方指定断点
# 因此，断点名称提供了一种方便的方式来对断点进行分组，并在已创建的断点上进行操作而无需使用断点编号
# 请注意，在断点命令中使用断点名称设置的属性与该断点名称无关，而是在当前标记为该断点名称的所有断点上依次设置属性: 之后使用该断点名称标记的断点，将不会获取之前使用该断点名称所设置的属性
# 为了将断点名称与断点编号(breakpoint ID)和断点编号范围(breakpoint ID range)区分开来，断点名称必须以 a-z 或 A-Z 中的字母开头，并且不能包含空格、点(.)、杠(-)
# 此外，断点名称只能应用于断点，而不能应用于断点位置(即，断点名称只能应用于断点的主要编号，不能应用于断点的次要编号)
```

# breakpoint-name-list

```bash
(lldb) help <breakpoint-name-list>
# hcg 注: 断点名称的列表
```

# breakpt-id

```bash
(lldb) help <breakpt-id>
# 断点使用主要编号和次要编号来标识
# 主要编号对应于使用 'breakpoint set' 命令创建的单个实体
# 次要编号对应于根据主要编号的断点实际发现和设置的所有位置
# 一个完整的断点编号可能看起来类似于 3.14，这意味着为第 3 个断点设置的第 14 个位置
# 仅通过指示断点的主要编号，即可指定断点的所有位置
# 有效的断点编号只包含(主要编号)，或者(主要编号.次要编号)。例如，3 或者 3.2 都可以是有效的断点编号
```

# breakpt-id-list

```bash
(lldb) help <breakpt-id-list>
# 断点编号列表是一种指定多个断点的方式，可以通过以下三种机制来完成:
# 1.最简单的方法是只输入一个空格以分隔断点编号
# 2.要指定一个断点下的所有位置，可以使用断点的主要编号后跟星号(*)
#   例如: 5.* 表示断点 5 下的所有位置
# 3.还可以使用 <start-bp-id> - <end-bp-id> 来指定断点的范围
#   <start-bp-id> - <end-bp-id> 可以是任何有效的断点编号，但是通过跨主要断点编号的特定位置来指定断点的范围是不合法的
#   例如: 3.2 - 3.7 是合法的，2 - 5 是合法的，3.2 - 4.4 是不合法的
```

# byte-size

```bash
(lldb) help <byte-size>
# 要使用的字节数
```

# class-name

```bash
(lldb) help <class-name>
# 程序中调试信息中的类名
```

# [cmd](https://so.csdn.net/so/search?q=cmd&spm=1001.2101.3001.7020)\-name

```bash
(lldb) help <cmd-name>
# 一个不带任何选项或参数的调试器命令(可能由多个单词组成)
```

# cmd-options

```bash
(lldb) help <cmd-options>
# hcg 注: 命令选项，非通用参数类型
```

# column

```bash
(lldb) help <column>
# 源文件中的列号
```

# command

```bash
(lldb) help <command>
# 一个 LLDB 命令行命令
```

# command-options

```bash
(lldb) help <command-options>
# hcg 注: 命令选项，非通用参数类型
```

# connect-url

```bash
(lldb) help <connect-url>
# hcg 注: 目标系统平台的 URL 地址
```

# count

```bash
(lldb) help <count>
# 一个无符号整数
```

# description-verbosity

```bash
(lldb) help <description-verbosity>
# 'po' 命令的输出的详细程度
# 可用值: compact | full
```

# directory

```bash
(lldb) help <directory> 
# 目录的名称
```

# disassembly-flavor

```bash
(lldb) help <disassembly-flavor>
# 反汇编插件能识别的反汇编风格
# 目前，Intel 的 target 的唯一有效选项是 "att" 和 "intel"
```

# expr

```bash
(lldb) help <expr>
# hcg 注: 一个表达式
```

# expr-path

```bash
(lldb) help <expr-path>
# 表达式路径是在 C/C++ 中用于访问聚合对象(类)的成员变量的符号序列。例如，给定一个类:
# 	class foo {
# 	    int a;
# 	    int b;
# 	    foo* next;
# 	};
# 在 foo aFoo 的 next 指针指向的条目中读取成员变量 b 的表达式为 aFoo.next->b
# 鉴于 aFoo 可以是 foo 类型的任何对象，字符串 '.next->b' 就是表达式路径，因为它可以附加到任何 foo 类型的实例以达到效果
# LLDB 中的表达式路径包括点(.)和箭头(->)运算符，并且大多数使用表达式路径的命令也可以接受星号(*)运算符。这些运算符的含义与 C/C++ 标准赋予它们的一般含义相同
# LLDB 还支持表达式路径中的索引([])，并扩展了方括号运算符的传统含义以允许位域提取(bit field extraction):
# 对于原生类型(int、float、char、...)的对象，将 '[n-m]' 作为表达式路径(其中 n 和 m 是任何正整数，例如 [3-5])将导致 LLDB 从变量的值中提取第 n 到 m 位。如果 n == m，则允许使用 [n] 作为快捷语法
# 对于数组类型和指针类型，表达式路径只能包含一个索引，其操作的含义与 C/C++ 定义的相同(用于提取子元素)
# 一些命令扩展了数组类型和指针类型的位域语法，它们具有数组切片的含义(获取数组中第 n 到 m 处的元素 ，或指向内存)
```

# filename

```bash
(lldb) help <filename>
# 文件名(可以包括路径)
```

# format

```bash
(lldb) help <format>
# 用于显示变量值的格式名称:
"default"
'B' or "boolean"
'b' or "binary"
'y' or "bytes"
'Y' or "bytes with ASCII"
'c' or "character"
'C' or "printable character"
'F' or "complex float"
's' or "c-string"
'd' or "decimal"
'E' or "enumeration"
'x' or "hex"
'X' or "uppercase hex"
'f' or "float"
'o' or "octal"
'O' or "OSType"
'U' or "unicode16"
"unicode32"
'u' or "unsigned decimal"
'p' or
"pointer"
"char[]"
"int8_t[]"
"uint8_t[]"
"int16_t[]"
"uint16_t[]"
"int32_t[]"
"uint32_t[]"
"int64_t[]"
"uint64_t[]"
"float16[]"
"float32[]"
"float64[]"
"uint128_t[]"
'I' or "complex integer"
'a' or "character array"
'A' or "address"
"hex float"
'i' or "instruction"
'v' or "void"
'u' or "unicode8"
```

# frame-idx

```bash
(lldb) help <frame-idx>
# hcg 注: 线程的栈帧列表的索引，同 frame-index
```

# frame-index

```bash
(lldb) help <frame-index>
# 线程的栈帧列表的索引
```

# fullname

```bash
(lldb) help <fullname>
# hcg 注:
# 函数或者方法的全称
# 对于 C++ 而言，这意味着命名空间和所有参数
# 对于 Objective-C 而言，这意味着具有类名和方法选择器的完整函数原型
```

# function-name

```bash
(lldb) help <function-name>
# 函数的名称
```

# function-or-symbol

```bash
(lldb) help <function-or-symbol>
# 函数或符号的名称
```

# gdb-format

```bash
(lldb) help <gdb-format>
# GDB 格式由 repeat count、format letter、size letter 组成
# repeat count 是可选的，默认为 1
# format letter 是可选的，默认为之前使用的格式
# size letter 是可选的，默认为之前使用的大小

# 格式字母(format letter)包括:
o - octal
x - hexadecimal
d - decimal
u - unsigned decimal
t - binary
f - float
a - address
i - instruction
c - char
s - string
T - OSType
A - float as hex

# 大小字母(size letter)包括:
b - 1 byte  (byte)
h - 2 bytes (halfword)
w - 4 bytes (word)
g - 8 bytes (giant)

# 示例格式:
32xb # 显示 32 个 1 字节的十六进制整数值
16xh # 显示 16 个 2 字节的十六进制整数值
64   # 显示 64 个 2 字节的十六进制整数值(使用最后一个 gdb-format 的格式和大小，这里假设最后一个 gdb-format 是上面的 16xh)
dw   # 显示 1 个 4 字节十进制整数值(repeat count 是可选的，默认为 1)
```

# help-text

```bash
(lldb) help <help-text>
# 用作 LLDB 中某些其他命令实体的帮助文本
```

# hostname

```bash
(lldb) help <hostname>
# hcg 注: 主机名
```

# idx

```bash
(lldb) help <idx>
# hcg 注: 列表中的索引，同 index
```

# index

```bash
(lldb) help <index>
# 列表中的索引
```

# language-name

```bash
(lldb) help <language-name>
# hcg 注: 语言的名称，例如: cplusplus、objc、renderscript、swift
```

# linenum

```bash
(lldb) help <linenum>
# 源文件中的行号
```

# local-file-spec

```bash
(lldb) help <local-file-spec>
# hcg 注: 本地文件路径，用于 'platform get-file' 命令
```

# local-thing

```bash
(lldb) help <local-thing>
# hcg 注: 本地文件路径，用于 'platform target-install' 命令，特指 bundle 或 executable file 的路径
```

# log-category

```bash
(lldb) help <log-category>
# 日志通道中的类别名称，例如 all
# 尝试输入 "log list" 命令以查看所有日志通道及其类别的列表
```

# log-channel

```bash
(lldb) help <log-channel>
# 日志通道的名称，例如 process.gdb-remote
# 尝试输入 "log list" 命令以查看所有日志通道及其类别的列表
```

# method

```bash
(lldb) help <method>
# C++ 方法名称
```

# module

```bash
(lldb) help <module>
# hcg 注: 模块完整路径，或模块的基本名称
```

# name

```bash
(lldb) help <name>
# 可以是任何东西，这取决于它的使用位置和方式
# hcg 注: 根据使用场景的不同，表示各种不同含义的字符串
# hcg 注: 感觉这是一个单纯的占位符，用于让 LLDB 命令的使用格式的说明看起来规整和统一
```

# new-path-prefix

```bash
(lldb) help <new-path-prefix>
# 镜像搜索路径替换对(image search paths substitution pairs)中新路径的前缀
```

# none

```bash
(lldb) help <none>
# 可以是任何东西，这取决于它的使用位置和方式
# hcg 注: 根据使用场景的不同，表示各种不同含义的字符串
# hcg 注: 感觉这是一个单纯的占位符，用于让 LLDB 命令的使用格式的说明看起来规整和统一
```

# number-per-line

```bash
(lldb) help <number-per-line>
# 每行要显示的条目数
```

# num-lines

```bash
(lldb) help <num-lines>
# 用于表示源代码或汇编指令的行数
```

# offset

```bash
(lldb) help <offset>
# 偏移量
```

# old-path-prefix

```bash
(lldb) help <old-path-prefix>
# 镜像搜索路径替换对(image search paths substitution pairs)中旧路径的前缀
```

# one-line-command

```bash
(lldb) help <one-line-command>
# 作为单行文本输入的命令
```

# options-for-aliased-command

```bash
(lldb) help <options-for-aliased-command>
# 用作命令别名定义的一部分的命令选项
# 有关更多信息，请参阅 'help commands alias' 命令
```

# path

```bash
(lldb) help <path>
# 路径
```

# perms-numeric

```bash
(lldb) help <perms-numeric>
# 以八进制数形式给出的权限(例如 755)
```

# pid

```bash
(lldb) help <pid>
# 进程编号，进程 ID
```

# platform-name

```bash
(lldb) help <platform-name>
# 已安装的平台插件的名称
# 尝试输入 'platform list' 命令以查看已安装平台的完整列表
```

# plugin

```bash
(lldb) help <plugin>
# hcg 注: 插件的名称
```

# portnum

```bash
(lldb) help <portnum>
# 端口号
```

# process-name

```bash
(lldb) help <process-name>
# 进程的名称
```

# python-class

```bash
(lldb) help <python-class>
# Python 类的名称
```

# python-function

```bash
(lldb) help <python-function>
# Python 函数的名称
```

# python-script

```bash
(lldb) help <python-script>
# 用 Python 编写的源代码
```

# queue-name

```bash
(lldb) help <queue-name>
# 线程队列的名称
```

# raw-input

```bash
(lldb) help <raw-input>
# 无需事先经过解释而直接传递给命令的自由形式的文本，允许空格而不需要引号
# 为了传递参数(这里说的参数指的是命令选项)和自由形式的文本，在最后一个参数(这里说的参数指的是命令选项)和任何原始输入之间放置两个破折号 "--"
```

# regex

```bash
(lldb) help <regex>
# hcg 注: 正则表达式
```

# register-name

```bash
(lldb) help <register-name>
# 可以使用体系结构特定的名称来指定寄存器名称，也可以使用通用的名称来指定寄存器名称
# 并非所有通用实体在所有架构上都有支持它们的寄存器，如果支持通用名称的寄存器不存在，则使用通用名称将返回错误
# LLDB 中定义的通用名称有:
pc       # 程序计数寄存器(program counter register)
ra       # 返回地址寄存器(return address register)
fp       # 帧指针寄存器(frame pointer register)
sp       # 栈指针寄存器(stack pointer register)
flags    # 标志寄存器(the flags register)
arg{1-6} # 传递整型参数的寄存器(integer argument passing registers)
```

# regular-expression

```bash
(lldb) help <regular-expression>
# 符合 POSIX 标准的扩展正则表达式
```

# remote-file-spec

```bash
(lldb) help <remote-file-spec>
# hcg 注: 远程文件路径，用于 'platform get-file' 命令和 'platform get-size' 命令
```

# remote-sandbox

```bash
(lldb) help <remote-sandbox>
# hcg 注: 远程终端的沙盒路径，用于 'platform target-install' 命令
```

# remote-url

```bash
(lldb) help <remote-url>
# hcg 注: 远程调试服务的 URL 地址，用于 'process connect' 命令
```

# run-args

```bash
(lldb) help <run-args>
# 在开始执行目标程序时，要传递给目标程序的参数，用于 'process launch' 命令
```

# run-mode

```bash
(lldb) help <run-mode>
# hcg 注:
# 确定在单步执行当前线程的同时，如何运行其他线程
# 可用值: this-thread | all-threads | while-stepping
```

# script-cmd-synchronicity

```bash
(lldb) help <script-cmd-synchronicity>
# 用于运行与 LLDB 事件系统有关的脚本命令的同步性
# 可用值: synchronous | asynchronous | current
# 用于 'command script add' 命令
```

# script-code

```bash
(lldb) help <script-code>
# hcg 注: 脚本代码，用于 'script' 命令
```

# search-word

```bash
(lldb) help <search-word>
# 用于搜索目的的任何感兴趣的词，用于 'apropos' 命令
```

# sect-name

```bash
(lldb) help <sect-name>
# hcg 注: 节名(section name)，用于 'target modules load' 命令
```

# selector

```bash
(lldb) help <selector>
# Objective-C 方法选择器的名称，用于 'breakpoint set' 命令
```

# setting-index

```bash
(lldb) help <setting-index>
# 对作为数组的调试器设置变量的索引
# 尝试输入 'settings list' 命令以查看所有可能的设置变量及其类型
```

# setting-variable-name

```bash
(lldb) help <setting-variable-name>
# 可设置的内部调试器变量的名称
# 尝试输入 'settings list' 命令以查看所有可能的设置变量及其类型
```

# shell-command

```bash
(lldb) help <shell-command>
# hcg 注: shell 命令
```

# shlib-name

```bash
(lldb) help <shlib-name>
# 共享库的名称
```

# sort-order

```bash
(lldb) help <sort-order>
# 用于在转储符号表(symbol table)时指定排序顺序，用于 'target modules dump symtab' 命令
# 可用值: none | address | name
```

# source-file

```bash
(lldb) help <source-file>
# 源文件的名称
```

# source-language

```bash
(lldb) help <source-language>
# 以下是受支持的语言的名称:
c89
c
ada83
c++
cobol74
cobol85
fortran77
fortran90
pascal83
modula2
java
c99
ada95
fortran95
pli
objective-c
objective-c++
upc
d
python
opencl
go
modula3
haskell
c++03
c++11
ocaml
rust
c11
swift
julia
dylan
c++14
fortran03
fortran08
mipsassem
renderscript
objc
objc++
pascal
```

# subcommand

```bash
(lldb) help <subcommand>
# 一个 LLDB 命令行子命令
```

# sub-command

```bash
(lldb) help <sub-command>
# hcg 注: 一个 LLDB 命令行子命令，同 subcommand
```

# subcommand-options

```bash
(lldb) help <subcommand-options>
# hcg 注: 子命令选项，非通用参数类型
```

# sub-command-options

```bash
(lldb) help <sub-command-options>
# hcg 注: 子命令选项，非通用参数类型
```

# subst

```bash
(lldb) help <subst>
# hcg 注: 在通过 "command regex" 命令创建自定义命令时，所使用的替换(substitution)
```

# summary-string

```bash
(lldb) help <summary-string>
# 摘要字符串是一种从变量中提取信息以便使用摘要呈现变量的方法
# 摘要字符串包含: 静态文本(static text)、变量(variables)、作用域(scopes)、控制序列(control sequences)
# - 静态文本可以是任何非特殊字符的序列，即除了 { } $ \ 以外的任何字符
# - 变量是以 ${ 开头，以 } 结尾的字符序列，并且包含如下所述格式的符号
# - 作用域是 { 和 } 之间的任何文本序列。如果没有错误，则作用域中包含的任何内容都只会出现在输出摘要中
# - 控制序列是通常 C/C++ 的 \a、\n、...、以及 \$、\{、\}
# 摘要字符串的工作原理是: 逐字复制静态文本，将控制序列转换为对应的字符，扩展变量，尝试扩展作用域

# 变量通过给它一个值而不是它的文本表示来扩展，这样做的方式取决于 ${ 标记之后的内容
# 最常见的序列是 ${var 后跟一个表达式路径，它是访问聚合类型成员的文本，给定一个该类型的变量:
# 例如，如果类型 T 有一个名为 x 的成员，而 x 有一个名为 y 的成员，如果 t 的类型为 T，则表达式路径将为 .x.y，将其放入摘要字符串的方法是 ${var.x.y}
# 还可以使用 ${*var 后跟表达式路径，在这种情况下，路径引用的对象将在显示之前被取消引用。如果被引用的对象不是指针，这样做会导致错误
# 有关表达式路径的更多详细信息，你可以输入 'help expr-path'

# 默认情况下，摘要字符串尝试显示它们引用的任何变量的摘要。如果该变量的摘要显示失败，则显示该变量的值。如果两者都显示失败，则不显示任何内容

# 在摘要字符串中，还可以使用数组索引 [n] 或切片范围 [n-m]。数组索引和切片范围可以有两种不同的含义，具体取决于表达式路径所指的对象类型:
# - 如果表达式路径所指的对象类型是标量类型(任何基本类型，如 int、float、...)，则 [n] 和 [n-m] 表示的是位域，即从数字中提取索引操作符所指示的位，并作为单个变量显示
# - 如果表达式路径所指的对象类型是数组或指针，则索引运算符 [n] 或 [n-m] 指示的数组元素将显示为该变量的结果

# 如果表达式是一个数组，则打印真正的数组元素
# 如果表达式是一个指针，则使用将指针作为数组的语法来获取值(这意味着此情况可以没有范围检查)
# 如果你试图显示一个已知大小的数组，则你可以使用 [] 而不是给出一个精确的范围，[] 具有显示数组中从 0 到 size - 1 的子元素的效果

# 此外，变量可以包含一个可选的格式代码，如 ${var.x.y%code}，其中 code 可以是 'help format' 命令中描述的任何有效格式，或仅允许作为变量一部分的特殊符号之一:
# %V : 默认显示对象的值
# %S : 默认显示对象的摘要
# %@ : 显示运行时提供的对象描述(对于 Objective-C，它会调用 NSPrintForDebugger。对于 C/C++，它什么都不会做)
# %L : 显示对象的位置(内存地址或寄存器名称)
# %# : 显示对象的子节点的数量
# %T : 显示对象的类型

# 可以在摘要字符串中使用的另一个变量是 ${svar，当然也包括 ${*svar 变量
# 此变量的工作方式与 ${var 完全相同，但使用对象的合成子提供程序(synthetic children provider)而不是实际对象
# 例如，如果使用 STL 合成子提供程序，则以下摘要字符串将计算存储在 std::list 中的实际元素的数量:
# type summary add -s "${svar%#}" -x "std::list<"
```

# symbol

```bash
(lldb) help <symbol>
# 任何符号的名称(函数名称、变量名称、参数名称、等等)
```

# symfile

```bash
(lldb) help <symfile>
# hcg 注: 调试符号文件的路径，用于 'target symbols add' 命令
```

# thread-id

```bash
(lldb) help <thread-id>
# 线程编号，线程 ID
```

# thread-index

```bash
(lldb) help <thread-index>
# 进程的线程列表的索引
```

# thread-name

```bash
(lldb) help <thread-name>
# 线程的名称
```

# type-name

```bash
(lldb) help <type-name>
# 特指异常的类型，用于 'breakpoint set' 命令
```

# type-specifier

```bash
(lldb) help <type-specifier>
# 类型名称，用于 'type lookup' 命令
```

# unix-signal

```bash
(lldb) help <unix-signal>
# 有效的 Unix 信号的名称或编号(例如: SIGKILL、KILL、9)
```

# unsigned-integer

```bash
(lldb) help <unsigned-integer>
# 一个无符号整数
```

# uuid

```bash
(lldb) help <uuid>
# hcg 注: Universally Unique Identifier，通用唯一标识符
```

# value

```bash
(lldb) help <value>
# value 可以是任何东西，这取决于它的使用位置和方式
```

# variable-name

```bash
(lldb) help <variable-name>
# 程序中变量的名称
```

# watchpoint-id

```bash
(lldb) help <watchpoint-id> 
# hcg 注: 内存断点编号，同 watchpt-id
```

# watchpt-id

```bash
(lldb) help <watchpt-id>
# 内存断点编号，是正整数
```

# watchpt-id-list

```bash
(lldb) help <watchpt-id-list>
# 内存断点编号列表，例如: '1-3' 或 '1 to 3'
```

# watch-type

```bash
(lldb) help <watch-type>
# 用于指定内存断点的类型
# 可用值: read | write | read_write
```

# width

```bash
(lldb) help <width>
# hcg 注: 用于指定显示的宽度，用于 'target modules list' 命令中
```