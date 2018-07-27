---  
layout: post  
title: iOS证书  
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [Superdanny](http://superdanny.link/)__  

## Certificates 证书  

* 我们从[开发者中心][2]了解到，开发者证书分为两种类型：`Development Certificate`(**开发证书**)和`Production Certificate`(**发布证书**)。两种证书都有对应的附属证书，包括推送证书、Apple Pay证书、Pass Type ID证书等等一系列附属证书。  
* 需要注意的是，当我们发布应用到 AppStore 时，发布的电脑必须具备两个条件：  

    * 安装了创建这个发布证书的电脑导出的p12文件  
    * 从`开发者账号`下载了发布证书  

![证书分类][3]  

### 证书的作用  

当某台电脑安装开发者证书后，这台电脑是如何拥有这种能力的呢？  

* 苹果在此运用了代码签名技术。代码签名验证允许我们的操作系统来判断是谁(**你或者信任的团队成员**)对App进行了签名。  
* Xcode会在项目编译期间使用你的代码签名验证，这个验证由一个由Apple认证过的**`公钥-私钥对`**组成，存储在你的`Keychain`(下简称**钥匙串**)中，公钥包含在证书(**Certificates**)中，`公钥证书`在**本地钥匙串**和**开发者账号**都有存储。  
* 另外，还有一个我们可以叫做`媒介证书`(**Intermediate Certificate**)的证书来确保我们的证书(Certificates)是经过授权而发布的。当安装好Xcode时，`媒介证书`就已经安装到我们的`钥匙串`中去了。如果你不小心删除了你的`媒介证书`，不用担心。你可以重新[下载][4]它。  
* 通过在`开发者账号`（**Developer Account**）和本地（**Mac**）都经过验证的证书（**Certificate**）我们就可以利用合法的证书进行App的测试和发布了。  

### 创建CSR文件及证书制作  

**1\. 打开电脑中的`钥匙串访问`**  

![钥匙串][5]  

**2\. 选择菜单`钥匙串访问`-`证书助理`-`从证书颁发机构请求证书`**  

![请求证书][6]  

**3\. 输入你的Email地址和名字，确保Email地址和名字与你注册为iOS开发者时登记的相一致**  

![输入Email、名字][7]  

**4\. 选择保存到磁盘(Saves to Disk)，建议保存到桌面，方便查找**  

![保存到磁盘][8]  

**5\. 打开[开发者中心][9]，登录开发者账号**  

![登录界面][10]  

**6\. 选择`Certificates, Identifiers &amp; Profiles`进入，然后选择`Certificates`**  

![Certificates, Identifiers &amp; Profiles][11]  

![Certificates][12]  

**7\. 选择`Certificates`，在右侧选择添加按钮添加**  

![添加证书][13]  

**8\. 选择`iOS App Development`，用于真机调试的`Certificates`文件，点击`Continue`。然后接下来会让你创建CSR文件(Create a CSR file)，点击`Continue`进入下一步上传CSR文件**  

![选择真机调试证书][14]  

**9\. 点击`Choose File`选择刚刚存储在桌面的SCR文件，然后点击`Generate`。一会就生成我们想要的证书啦！**  

![Choose File][15]  

![上传SCR文件][16]  

**10\. 我们可以将刚刚生成的证书点击`Download`下载到本地使用**  

![下载证书][17]  

* * *  

### 证书的使用  

如果开发者B，登录`开发者账号`，下载证书（cer文件）运行，只有证书没有私钥，是不能正常使用的。所以如果有新同事加入到开发组的时候，应该从本地钥匙串中选择证书，**一定要记得展开证书那一条显示出私钥并将两行都选中**，右键导出2项，输入密码之后就生成p12文件（**包含证书和私钥**）给同事。  

另外可以给同事一份[描述文件][18](**Provisioning Profiles**)，用于本地开发识别测试设备。  

需要强调一点，证书和项目关系其实并不大，证书一般有效期只有一年，当证书过期后，只需要重新生成一份证书，上传到`开发者账号`就行，同时因为原有证书过期，需要重新生成`Provisioning Profiles`文件。然后给同事们最新的p12文件和Provisioning Profiles文件就行  

所以`开发者账号`中的证书，配置文件是可以放心操作的（比如误删了，或者找不到证书私钥了）  

![][19]  

### 证书过期/即将过期  

网上很多说法，但是讲的对我来说还不够完善，所以这里统一一下，也方便自己查阅。  

**疑问一：证书过期了，会影响到 AppStore 上面的应用吗？**  

答：证书过期不会影响已上架 AppStore 应用，但是推送会出问题，更新推送证书也不用下架重新发布，可以重新生成，只要保证 developer.apple.com 中那个 APP ID 的推送证书和推送服务器上的一致即可。但是账号欠费的话应用会被下架。  

**疑问二：证书过期了/即将过期怎么办？**  

答：首先，打开密钥中心，生成一个CSR（证书请求）。然后，到Apple Center把证书revoke，然后新建一个，新建的将会默认是刚刚revoke的证书的所有设置的。把下载回来的证书导出一份p12格式的保存起来（因为如果其他人需要的时候，只能跟你拿了，在Apple Center下载的用不了的。原因是还需要你电脑的密钥）然后去provision profile edit 一下，从新下载，替换掉原来的。你就可以继续开发了。不需要提交新 App 到 AppStore。  

## Provisioning Profiles 描述文件  

在这里，我引用别人的一段话，因为觉得写得很喜感，但又很实在。  

![][20]  

我想这个界面一弹出来的时候，蛋蛋忧伤迎面扑来。然后怒点 Fix issue，然后你们团队负责管理证书的基友突然发现证书中心多了好多好乱的证书以及描述文件，然后他爆了一句：what the fuck！删掉了带有Xcode *的证书以及描述文件，然后自己又暴力的点了一发Fix issue，然后你突然调试不了了，再暴击Fix issue键，最后整个团队都只有通过Fix issue来真机调试了…  

所以慎点Fix issue，如果点击这个选项，聪明的(<del>蠢哭的</del>)Xcode就会自己管理描述文件，然后各种莫名其妙的带有Xcode *的证书以及描述文件…  

其实只要坚信一点，证书、设备ID、AppID、描述文件都弄对了就绝逼不会出问题的！  

### 描述文件过期  

苹果官方文档写明，企业证书有效期是3年，而描述文件只有1年有效期。所以当你的描述文件过期(**expire**)时。不用慌张，我看到网上好多朋友说删除重新生成，其实不用这么麻烦，只需要3步完成：`点击过期的描述文件展开详情界面`-`点击Edit按钮`-`点击Generate按钮`  

* * *  

[2]: https://developer.apple.com/ios/manage/overview/index.action  
[4]: http://www.apple.com/certificateauthority  
[9]: https://developer.apple.com/membercenter/  
[18]: /2015/09/25/iOS-production-certificate-and-use/#provisioning-profiles-描述文件  
[3]: /assets/postAssets/2016/81f8a509gw1ezq93sjmnbj20pq0k4god.webp  
[5]: /assets/postAssets/2016/81f8a509gw1ewe0hqvgt1j206q062q2z.webp  
[6]: /assets/postAssets/2016/81f8a509gw1ewe0hon5joj20uq0foadz.webp  
[7]: /assets/postAssets/2016/81f8a509jw9ezl2jtqobzj20y80o877n.webp  
[8]: /assets/postAssets/2016/81f8a509gw1ewe0hluv88j20y80o8ack.webp  
[10]: /assets/postAssets/2016/81f8a509gw1ewe0hh9nbzj20qq0igt9v.webp  
[11]: /assets/postAssets/2016/81f8a509gw1ewe0hfwupuj21kw0hg41q.webp  
[12]: /assets/postAssets/2016/81f8a509gw1ewe0hdhtxyj21k60uidlt.webp  
[13]: /assets/postAssets/2016/81f8a509gw1ewe0h9aq38j21k60hw0wd.webp  
[14]: /assets/postAssets/2016/81f8a509gw1ewe0h8deitj21ii0w8afm.webp  
[15]: /assets/postAssets/2016/81f8a509gw1ewe0h42rmzj213e0asgmb.webp  
[16]: /assets/postAssets/2016/81f8a509gw1ewe0h39trgj213k0ow7al.webp  
[17]: /assets/postAssets/2016/81f8a509gw1ewe0gwmrp4j21300syq6q.webp  
[19]: /assets/postAssets/2016/81f8a509gw1ezqda52mmej20uk08s76e.webp  
[20]: /assets/postAssets/2016/81f8a509gw1ezqetrs90nj20m80afq4r.webp  

