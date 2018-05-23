---  
layout: post
title: UIScrollView中布局错乱
category: Error
tags: Swift Define
keywords: Jekyll,Github
description: 
---  

用SnapKit布局时遇到这种情况:  
![2](/assets/postAssets/2018/2.webp)  
各种约束没有任何问题 上面部分在UIScrollView中  

后因设置 `UIImageView.layer.masksToBounds = true` 解决  
![1](/assets/postAssets/2018/1.webp)  

原因待续...


