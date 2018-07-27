---  
layout: post  
title: Xcode Unable to boot device  
category: Error  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

删除Simulator文件夹后报错:  
```  
Xcode Unable to boot device because it cannot be located on disk  

Use the device manager in Xcode or the simctl command line tool to either delete the device properly or erase contents and settings.  
```  

如下解:  
打开Xcode -> Open Developer Tool -> iOS simulator  

Hardware -> Device -> Manage Devices  
删除旧Simulator  重新添加Simulator  

