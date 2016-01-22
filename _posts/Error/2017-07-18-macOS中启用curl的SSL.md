---  
layout: post
title: macOS中启用curl的SSL
category: Error
tags: Swift Define
keywords: Jekyll,Github
description: 
---  

RN中编译遇到:  
curl: Protocol "https" not supported or disabled in libcurl  

如下解:  
[https://curl.haxx.se/download.html](https://curl.haxx.se/download.html)下载最新包  
```shell  
cd curl-x.xx.x  
./configure --with-darwinssl  
make  
sudo make install  
```  


