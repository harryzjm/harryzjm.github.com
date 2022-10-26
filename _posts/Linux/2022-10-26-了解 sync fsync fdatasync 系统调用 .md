---  
layout: post  
title: 了解 sync fsync fdatasync 系统调用  
category: Linux  
tags: Linux  
keywords: Linux  
---  

__Posted by [赐我白日梦](https://www.cnblogs.com/ZhuChangwu/p/14047108.html)__  

### 缓冲

传统的UNIX实现的内核中都设置有缓冲区或者页面高速缓存，大多数磁盘IO都是通过缓冲写的。

当你想将数据write进文件时，内核通常会将该数据复制到其中一个缓冲区中，如果该缓冲没被写满的话，内核就不会把它放入到输出队列中。

当这个缓冲区被写满或者内核想重用这个缓冲区时，才会将其排到输出队列中。等它到达等待队列首部时才会进行实际的IO操作。

[![](/assets/postAssets/2022/16667921909449.png)](/assets/postAssets/2022/16667921909449.png)

这里的输出方式就是大家耳熟能详的： 延迟写

这个缓冲区就是大家耳熟能详的：OS Cache

  

### 延迟写的优缺点

很明显、延迟写降低了磁盘读写的次数，但同时也降低了文件的更新速度。

这样当OS Crash时由于这种延迟写的机制可能会造成文件更新内容的丢失。而为了保证磁盘上的实际文件和缓冲区中的内容保持一致，UNIX系统提供了三个系统调用：sync、fsync、fdatasync

  

### sync、fsync、fdatasync

```C
#include<unistd.h>
int fsync(int filedes);
int fdatasync(int filedes);
int sync();
```

#### sync
将所有修改过的缓冲区排入写队列，然后就返回了，它并不等实际的写磁盘的操作结束。所以它的返回并不能保证数据的安全性。通常会有一个update系统守护进程每隔30s调用一次sync。

#### fsync
需要你在入参的位置上传递给他一个fd，然后系统调用就会对这个fd指向的文件起作用。fsync会确保一直到写磁盘操作结束才会返回。所以fsync适合数据库这种程序。

#### fdatasync
和fsync类似但是它只会影响文件的一部分，因为除了文件中的数据之外，fsync还会同步文件的属性。


参考：《UNIX环境高级编程》
