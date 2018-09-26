---  
layout: post  
title: Shadowsocks & PAC  
category: internet  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__[Posted by yiranphp](https://www.zybuluo.com/yiranphp/note/632963")__  

### Shadowsocks  

简单来说，打开了Shadowsocks客户端软件，就设置了一个本地代理，代理类型为 socks5，地址和端口为：127.0.0.1:1080，简称为 ss 代理，无论你选择 PAC 模式还是全局模式，甚至关闭 Shadowsocks，如下图所示，ss 代理依旧在运行  
![image_1b6h1h4pt1bkbu0214qf1nmqhq9.png-76.6kB](/assets/postAssets/2017/image_1b6h1h4pt1bkbu0214qf1nmqhq9.webp)  

### PAC  

代理自动配置（Proxy auto-config，简称PAC）是一种网页浏览器技术，用于定义浏览器该如何自动选择适当的代理服务器来访问一个网址。   
一个PAC文件包含一个JavaScript形式的函数“FindProxyForURL(url, host)”。这个函数返回一个包含一个或多个访问规则的字符串。用户代理根据这些规则适用一个特定的代理其或者直接访问。当一个代理服务器无法响应的时候，多个访问规则提供了其他的后备访问方法。浏览器在访问其他页面以前，首先访问这个PAC文件。PAC文件中的URL可能是手工配置的，也可能是是通过网页的网络代理自发现协议（Web Proxy Autodiscovery Protocol）自动配置的。  

上面是从维基百科摘录的关于PAC的解释，我做了一个简单的图片解释什么是PAC：  
![此处输入图片的描述](/assets/postAssets/2017/yEvu2aF.webp)  

简单的讲，PAC就是一种配置，它能让你的浏览器智能判断哪些网站走代理，哪些不需要走代理。点击 Shadowsocks 的菜单，选择『编辑自动模式的 PAC』，如下图  
![image_1b6h31qvt1hr0rco1nh941i1nkq1h.png-66.5kB](/assets/postAssets/2017/image_1b6h31qvt1hr0rco1nh941i1nkq1h.webp)  

![image_1b6h2oer5pre1jbrjtr1oqf18ie14.png-106kB](/assets/postAssets/2017/image_1b6h2oer5pre1jbrjtr1oqf18ie14.webp)   
在上面的目录下有两个文件，一个是 gfwlist.js，还有一个是   
user-rule.txt,确保当前的模式为自动代理模式，打开系统设置-->网络，点击高级，查看代理选项卡，如下图  
![image_1b6h39qi71mb45mo74v1j4ql3p1u.png-108.1kB](/assets/postAssets/2017/image_1b6h39qi71mb45mo74v1j4ql3p1u.webp)  

在浏览器中打开 URL，下载 pac 文件，打开查看  

![image_1b6h3g4sjeopq2l8m81fl41j082b.png-96kB](/assets/postAssets/2017/image_1b6h3g4sjeopq2l8m81fl41j082b.webp)  

这三个文件的关系就是：   
最终的pac 文件是根据 gfwlist.js 和 user-rule.txt 两个文件共同生成的   
如果用户想要添加某些网站进入 PAC，最好的方式是写入 user-rule.txt 这个文件，而不是修改 gfwlist.js 这个文件，因为gfwlist.js这个文件会时不时的和 github 上做同步，可能会造成已有的修改会被覆盖掉。  

### PAC 的优势  

PAC自动代理属于智能判断模式，相比全局代理，它的优点有：   
1\. 不影响国内网站的访问速度，防止无意义的绕路   
2\. 节省Shadowsocks服务的流量，节省服务器资源   
3\. 控制方便  

### user-rule文件的语法规则  

user-rule文件中，每一行表示一个URL通配符，但是通配符语法类似。例如添加一行 ||ip138.com^   
注意末尾不要忘记 ^ 符号，意思是要么在这个符号的地方结束，要么后面跟着?,/等符号。   
自定义代理规则的设置语法与GFWlist相同，语法规则如下：   
1\. 通配符支持。比如 *.example.com/* 实际书写时可省略 * ， 如 .example.com/ ， 和 *.example.com/* 效果一样   
2\. 正则表达式支持。以 \ 开始和结束， 如 [\w]+:\/\/example.com\   
3\. 例外规则 @@ ，如 @@*.example.com/* 满足 @@ 后规则的地址不使用代理   
4\. 匹配地址开始和结尾 | ，如 |[http://example.com](http://example.com/) 、 example.com| 分别表示以 [http://example.com](http://example.com/) 开始和以 example.com 结束的地址   
5\. || 标记，如 ||example.com 则 [http://example.com](http://example.com/) 、 [https://example.com](https://example.com/) 、 [ftp://example.com](ftp://example.com/) 等地址均满足条件   
6\. 注释 ! 。 如 !我是注释  

### 转者云:  

若是想让某个应用走代理 直接用 Charles 找出该应用的连接地址或域名 添入 位于~/.ShadowsocksX-NG/user-rule.txt 即可  

