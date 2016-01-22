---
layout: post
title: iOS应用上架到AppStore
category: iOS
tags: iOS
keywords: iOS
description: 
---


__Posted by [Superdanny](http://superdanny.link/)__  


# iOS应用上架到AppStore


## 上架前准备工作

### 1、注册App ID(**应用ID**)

`App ID`是识别不同应用程序的唯一标示符。每个App都需要一个`App ID`或者App标识。目前有两种类型的App标识：一个是精确的`App ID`(**explicit App ID**)，一个是通配符`App ID`(**wildcard App ID**)。 使用通配符的`App ID`可以用来构建和安装多个程序。尽管通配符`App ID`非常方便，但是一个精确的`App ID`也是需要的，尤其是当App使用**iCloud**或者使用其他iOS功能的时候，比如**Game Center**、**Push Notifications**或者**IAP**。关于如何创建`App ID`，苹果官方有相关的文档说明👉[注册App IDs][3]

### 2、创建Distribution Certificate(**发布证书**)

发布证书，也是根证书。它是所有应用发布的基础，当你创建过一次根证书之后，就不需再创建。创建的过程我以前的文章有提及过开发证书的创建，发布证书的创建过程类似。👉[iOS开发者证书的那些事][2]

### 3、创建商店Provisioning Profile(**商店描述文件**)

和开发期间使用的开发描述文件类似，我们 App 上架到 AppStore 的时候也需要创建一个对应的描述文件，不过有一点不同的是，该类型的描述文件不需要选择任何设备就能创建。创建过程也非常简单，可参考开发描述文件的创建过程。

### 4、Build Settings(**生成设置**)

我们需要在工程中进行相应的配置，才能提交到 AppStore。对`Code Signing`中的`Code Signing Identity`和`Provisioning Profile`两项进行配置。  
![Build Settings][4]

### 5、Deployment Target(**部署目标**)

非常有必要说下deployment target，Xcode中每个target都有一个deployment target，它指出app可以运行的最低操作系统。不过，一旦应用在App Store中生效，再去修改deployment target，你要考虑到一定后果。如果你在更新app的时候提高了deployment target，但是已经购买应用的用户并没有遇到新的deployment target，那么应用就不能在用户的移动设备上运行。如果用户通过iTunes(不是设备)下载了一个更新过的app，然后替代了设备上原先的版本，最后却发现新版本不能在设备上运行，这确实是个问题。

对此有两个方法：

1. 当你决定提高现有app的deployment target时，要在新版本的版本注释中进行说明。如果你提前告知用户，那么至少有一点，你已经尽力阻止问题的发生了。

2. 对于一款新app，我经常会把deployment target设置为最近发布的系统版本。因为新iOS版本发布后，渗透率的增长速度是令人难以置信的。很多人认为提高deployment target会失去大部分市场，这个说法并不准确，比如iOS 6，iOS 6发布后一个月，超过60%的设备已经进行了更新。但对Android而言，就是另外一回事了，Android用户并不会像iOS用户那样热衷于更新操作系统版本。

## iTunes Connect

1. 在提交App之前，我们需要进入到[iTunes Connect][5]里面创建我们的App记录。

![选择iTunes Connect][6]

2. 然后点击界面左上角的**`+`**号，选择新建App

![新建App][7]

3. 填写应用相关信息-`Metadata`(**元数据**)

![应用信息][8]  
其中`SKU Number`是一个**唯一标识你的app的特殊字符串。应用发布之后就不能修改**，可以使用app的`Bundle ID`。

之后的操作就不用介绍了，因为都是一些基本的信息设置。你只需要按提示一步一步完成设置即可。添加成功之后，应用的状态会显示`Prepare for Upload`(**准备提交**)。

接下来，在`构建版本`栏目下，我们看到苹果提示我们使用Xcode或者`Application Loader`提交我们的构建版本。此时我们就可以进行[上传二进制文件][9]了。上传之后在该栏目下就会有我们上传的二进制文件供选择，选择对应的文件之后就可以点击右上角的**`提交以供审核`**按钮，此时应用的状态会变成`Waiting For Review`(**等待审核**)

![构建版本][10]

## 上传二进制文件

苹果提供两种方式进行提交，一种是直接通过Xcode打包提交，另一种是通过Xcode自带工具`Application Loader`进行提交。我比较喜欢第二种，因为可以看到上传进度。更加人性化。关于上传方式，我这边不做展开，提供给大家一个学习资料。有任何疑问欢迎留言提出😊

### 方式一：使用 Xcode 上传

我在[iOS开发企业版ipa分发(In-House模式)记录][11]一文中有讲到使用Xcode打包步骤，不过里面的少许步骤不一样而已。这里就不做详细说明。如果有什么不懂可以参阅👉[上传你的App][12]。

### 方式二：使用 Application Loader 上传

有关详细信息，请参阅👉[Using Application Loader][13]。

## 知识扩展

1、我们在进行版本更新的时候，App图标、名字、描述、新版本描述、关键词、支持URL、截图、联系方式、Review Notes(**审核备注**)均可以更改

![元数据相关信息][14]

2、Review Notes(**审核备注**)中，包括如下信息：

* 名字、姓氏、电子邮件地址、电话号码(**都是必需**)

在 app 审核团队有任何疑问或需要了解其他信息时应联系的您组织中人员的联系人信息。

有助于审核团队实施审核过程的 app 其他信息。添加测试 app 可能需要的信息，如 app 专用设置、测试注册或帐户详细信息。"Review Notes"（审核备注）字段的大小上限为 4000 字节，并可本地化为任何语言版本。如果您的 app 通过蜂窝数据网络传输流媒体视频，则在"Review Notes"（审核备注）中输入测试视频流 URL。此文本仅对 Apple 审核团队可见。

拥有完整访问权限的演示帐户的用户名。此帐户在 app 审核过程中使用，不能是过期帐户。应在"Review Notes"（审核备注）字段中添加其他帐户的详细信息。

拥有完整访问权限的演示帐户的密码。

## 关于 app 状态

无论 app 版本列于 iTunes Connect 中的哪个位置，您都可以看到版本的状态（如`Waiting For Upload`（正在等待上传）或`Ready for Sale`（可以销售））或状态指示器（如 ![green][17]， ![yellow][18] 或 ![red][19] ）。状态会立即告知您是否需要关注您的 app：

* 红色状态指示器表示您需要先执行某个操作，然后您的 app 才能在商店中提供。
* 黄色状态指示器表示正在进行某个进程（由您或 Apple 控制）。
* 绿色状态指示器表示 app 已在商店中提供。

| 状态            | 状态名称                                          | 说明                                                                                                                                                     |
| ------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ![yellow][18] | Prepare for Submission(准备上传)                  | 已为 app 创建了 iTunes Connect 记录，但是未准备好上传二进制文件。您可能仍要配置元数据、屏幕快照、价格、In-App Purchase、Game Center、iAd App Network 设置等等。                                        |
| ![yellow][18] | Waiting For Review(正在等待审核)                    | 您已提交新的 app 或更新后的版本，而且 Apple 已收到，但是尚未开始审核该 app。在 app 正在等待审核时，您可以：1、拒绝您的二进制文件，以将其从 Apple 审核队列中移除。请参阅 拒绝您的二进制文件。2、编辑某些 app 信息。                            |
| ![yellow][18] | In Review(审核中)                                | Apple 正在审核您的 app。由于提交的每个 app 都不相同，因此没有固定的审核时间。您可以通过拒绝二进制文件将您的二进制文件从审核队列中移除。请参阅 拒绝您的二进制文件。                                                              |
| ![yellow][18] | Pending Contract(合同挂起)                        | 您的 app 已通过审核，并可以销售，但是您的合同尚未生效。在“Contracts, Tax &amp; Banking”（合同、税务和银行）模块中检查合同进度。请参阅 查看合同和合同状态。                                                            |
| ![yellow][18] | Waiting For Export Compliance(等待出口合规)         | 您的 app 已通过审核，并可以销售，但正在审核您的 CCATS 文件的出口合规。                                                                                                              |
| ![yellow][18] | Pending Developer Release(等待开发者发布)            | 您的 app 版本已获得 Apple 批准，正在等待您进行发布。您可以选择手动控制发布或将发布日期定于将来的某个日期。当一切准备就绪时，将 app 版本发布到商店。请参阅 指定应用程序版本发布时间。                                                    |
| ![yellow][18] | Processing for App Store(正在针对 App Store 进行处理) | 正在处理您的二进制文件，并且可在 24 小时内准备销售。                                                                                                                           |
| ![yellow][18] | Pending Apple Release(等待 Apple 发布)            | Apple 保留您的 app 版本，直到相应的 Apple iOS 或 OS 版本公开发布。如果您认为 app 应在现有的 iOS 或 OS 版本上进行发布，则检查在您的 app 二进制文件中设置的部署目标。如果您使用不同的部署目标重建 app 二进制文件，则拒绝此版本的二进制文件，并提交新的版本。 |
| ![green][17]  | Ready for Sale(可以销售)                          | Apple 已经批准该 app 版本，并将其发布到商店。在此状态下可进行的更改是：1、从商店中移除 app。请参阅 在商店中取消[ app 销售的步骤][20]。2、使用新版本更新 app。请参阅 将您的[ app 替换为新版本][21]。                               |
| ![red][19]    | Rejected(已拒绝)                                 | Apple 拒绝了二进制文件。具有管理员或技术人员角色的 iTunes Connect 用户会收到包含拒绝原因的通知。请参阅 使用解决方案中心。                                                                               |
| ![red][19]    | Metadata Rejected(已拒绝元数据)                     | 元数据项目（除您的二进制文件外）未通过审核。请参阅 使用解决方案中心。要解决该问题，请编辑 iTunes Connect 中的元数据。当你解决这个问题,再次提交审查的程序。                                                                 |
| ![red][19]    | Removed From Sale(已取消销售)                      | 您的 app 已从商店中移除。如果您的 app 存在从商店中移除的风险，则 Apple 会与您联系，以尽量在移除您的 app 前解决相关问题。                                                                                |
| ![red][19]    | Developer Rejected(开发者已拒绝)                    | 您已拒绝审核流程中的二进制文件，并将其从审核队列中移除。当您准备就绪时，重新提交您的二进制文件或提交新的二进制文件。请参阅 拒绝您的二进制文件。                                                                               |
| ![red][19]    | Developer Removed From Sale(开发者已取消销售)         | 您已从商店中移除 app。请参阅 重新销售[ app 的步骤][20]。                                                                                                                   |
| ![red][19]    | Invalid Binary(无效的二进制文件)                      | Apple 拒绝了您的二进制文件，因为它没有满足所有上传要求。解决二进制文件中的所有问题后，在 **构建版本** 模块中删除不符合的二进制文件，选择一个新的文件，然后保存提交审核。                                                             |

## 查看状态历史

1. 进入[iTunes Connect][21]
2. 选择某一个app进入详情界面
3. 依次选择`App Store Versions`(**App Store版本**) — `Activity`(**活动**)

![iOS App Store版本][22]

* * *


[1]: /2015/09/24/iOS-about-certification-guide
[2]: /2015/09/25/iOS-production-certificate-and-use/
[3]: https://developer.apple.com/library/ios/documentation/IDEs/Conceptual/AppDistributionGuide/MaintainingProfiles/MaintainingProfiles.html#//apple_ref/doc/uid/TP40012582-CH30-SW991
[5]: https://itunesconnect.apple.com/
[9]: /2016/01/13/iOS-iTunes_Connect_1-Uploading-APP-to-Appstore/#上传二进制文件
[11]: /2015/10/10/iOS-recording-In-House/
[12]: https://developer.apple.com/library/ios/documentation/IDEs/Conceptual/AppDistributionGuide/UploadingYourApptoiTunesConnect/UploadingYourApptoiTunesConnect.html#//apple_ref/doc/uid/TP40012582-CH36-SW9
[13]: https://itunesconnect.apple.com/docs/UsingApplicationLoader.pdf
[15]: http://weibo.com/2180556041
[16]: http://SuperDannyBlog.farbox.com
[20]: https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnect_Guide/Chapters/ChangingAppStatus.html#//apple_ref/doc/uid/TP40011225-CH30-SW17
[21]: https://itunesconnect.apple.com/  
[4]: /assets/postAssets/2016/81f8a509gw1ezzbb19csxj21kw0yc12o.webp
[6]: /assets/postAssets/2016/81f8a509gw1ezzd0fwjiej21kw0mcwj5.webp
[7]: /assets/postAssets/2016/81f8a509jw9ezzcyi6n8zj21kw0titig.webp
[8]: /assets/postAssets/2016/81f8a509gw1ezzd096nlmj20p80w0aca.webp
[10]: /assets/postAssets/2016/81f8a509jw9ezzyqfk8o9j21kw0mjae3.webp
[14]: /assets/postAssets/2016/81f8a509gw1ezzzrilpe6j20u00x5tiq.webp
[17]: /assets/postAssets/2016/81f8a509gw1f0043w60y6j200a00aq2s.webp
[18]: /assets/postAssets/2016/81f8a509gw1f0043y5prsj200a00aq2s.webp
[19]: /assets/postAssets/2016/81f8a509gw1f0043wf07bj200a00aq2s.webp
[22]: /assets/postAssets/2016/81f8a509jw9f006vqjzynj217x0ijdif.webp
  


