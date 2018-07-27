---  
layout: post  
title: subscribeOn & observeOn  
category: ReactiveX  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

```swift  
//程序运行于 queue0  
Observable.create   // 1  
    .map            // 2  
    .切换1 queue1  
    .map            // 3  
    .切换2 queue2  
    .map            // 4  
    .subscribe      // 5  
```  

![subscribeOn - observeOn](/assets/postAssets/2018/subscribeOn-observeOn.webp)  

**简单理解:**  
**subscribeOn**: 管理之前 默认沿用于后 越上优先级越高 不分层  
**observeOn**:   管理之后 越下优先级越高 均高于subscribeOn 分层  

