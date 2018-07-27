---  
layout: post  
title: iOS Debug & Release  
category: Error  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

## 区别  

| Debug | Release | |  
| --- | --- | --- |  
| 调试信息 | 无 | 调试信息占用大小 |  
| 不优化 | 优化代码 包小速快 | 优化后 包小速快 |  
| 内存延迟释放 | 立即释放 | weak 对象的释放问题 |  
| 默认给初始化 | 不给 | OC: 中会出现<br>Swift: 强制初始化 没这毛病 |  

## 解决办法:  
1. 静态代码分析  

## 待续...  

