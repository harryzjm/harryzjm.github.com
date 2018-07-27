---  
layout: post  
title: magic mouse 卡顿  
category: Error  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

1. 电量过低  
2. 网络环境  
> 外层网络频段干扰  
> macos 在share wifi  改为 share bluetooth  

配置bluetooth:  
1. share中配置为share bluetooth  
2. bluetooth connect mac  
3. Go to System Preferences -> Network -> Bluetooth Pan (you might have to create this one)  
4. Press Advanced..  
5. Pick "Using DHCP with manual address" for "Configure IPv4"  
6. Enter an address under "IPv4 Address" (192.168.1.14 worked for me)  
Hit ok, hit apply.  

