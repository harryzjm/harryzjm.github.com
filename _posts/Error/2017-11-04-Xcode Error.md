---  
layout: post  
title: Xcode Error  
category: Error  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

| Error | Reason | Solve |  
| --- | --- | --- |  
| libc++abi.dylib`__cxa_throw | 设置了全局异常断点, 类型为all, 而c++异常也会报错 | 把全局断点设置成objective-c类型 |  

