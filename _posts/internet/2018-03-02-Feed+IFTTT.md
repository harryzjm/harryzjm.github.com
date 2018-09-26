---  
layout: post  
title: Feed+IFTTT  
category: internet  
tags: Feed IFTTT  
keywords: Feed,IFTTT  
description: 
---  

**► 制作Feed**  

**1\. 进入网页**，[FEED43](http://www.feed43.com/)无需注册，点击Create your own feed直接使用。  

![](/assets/postAssets/2018/v2-b5da0b08f632376fad3925a779e373b4_hd.webp)  

**2\. 选定RSS网页**，将目标网址添入Step1\. Specify source page address (URL)，将输入的源代码复制到txt文档中（方便之后写抓取规则）  

![](/assets/postAssets/2018/v2-1b687a5b1c325ba6d04fbdcc13b95668_hd.webp)  

**3\. 定制RSS抓取规则**。Global Search Pattern是选择你要搜索的范围。可以不填，这样会搜索整个页面，一般新手都选择整个页面，即空白。Item (repeatable) Search Pattern这部分最重要，是我们要抓取的内容。  

![](/assets/postAssets/2018/v2-b1fa90c59739bddc0c27134cd36ba6bc_hd.webp)  

仔细查看Step1中的源代码，找到区需要抓取的部分，输入到Item (repeatable) Search Pattern。  

测试网址：[http://news.163.com/special/0001386F/rank_whole.html](http://news.163.com/special/0001386F/rank_whole.html)  

**需要抓取的源代码**：  

```swift  
<tr>  
<td class="red"><span>2</span><a href="更时尚更运动 车展实拍解析红旗H5">更时尚更运动 车展实拍解析红旗H5</a></td>  
<td class="cBlue">11211615</td>  
</tr>  
```  

![](/assets/postAssets/2018/v2-cf6dbf2c09189f7517ec63abdc80c50d_hd.webp)  

点击Extract，进行抓取  

![](/assets/postAssets/2018/v2-e9486741a6229ab258a95147f584571b_hd.webp)  

**4\. 整理rss输入格式**- Define output format，一般情况下前面三个会已经写好，后三个就将前面得出的item里面的元素填入即可，我这里1对应的是链接所以填入 Link，2对于标题就填入Title, 这里支持HTML, 可输入HTML变更显示内容  

![](/assets/postAssets/2018/v2-b4614f5c46090f2eb762aac87d604350_hd.webp)  

然后点击preview，完成制作，同时出现预览  

![](/assets/postAssets/2018/v2-498bf1f1c0b14da172498b58f59e39b9_hd.webp)  

如果注册了FEED43的账号，可以修改rss地址，但不能改为中文，否则会rss出错。   

**5\. 获取RSS地址**，点击Fedd URL 可得rss地址，我这里是[http://www.feed43.com/6212020573370533.xml](http://www.feed43.com/6212020573370533.xml)  

![](/assets/postAssets/2018/v2-f3b00e876d8df136f7d354b4fc22f900_hd.webp)  

在RSS reader中展示为  

![](/assets/postAssets/2018/v2-6d8f503ff3da16eb985ca1d3ae2de98f_hd.webp)  

**6\. 全文抓取：**feed43导出的条目必须点击链接才能看到内容。在rss展示全文，需要通过FeedEx再转一次。  

FeedEx：[https://feedex.net/](https://feedex.net/)  

![](/assets/postAssets/2018/v2-213e5f4ac7f1734b9d4e60cb465908cd_hd.webp)  

—————————  

