---  
layout: post  
title: 解除 Telegram iOS 群组频道封禁限制
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [Frederic Chan](https://dev.tail0r.com/remove-telegram-channel-restriction/)__  

因为 App Store 的内容审核政策，Telegram iOS 很多群组（尤其 NSFW 群组）都无法进入，部分正常的群也遭到屏蔽，而安卓和 PC/Mac 端不受影响，这还是带来了一些不方便。鉴于 telegram 的代码是开源的，于是我尝试通过修改代码的方式来绕过限制。

Telegram X 是官方使用 Swift 语言写的新的 Telegram 客户端，相比于原版更加丝滑流畅。由于原版的 Telegram iOS 已经六个月没有更新代码了，而 Telegram X 正在保持稳定的开发步伐，从长远来看我们还是修改新出的 Telegram X 比较好。

## 下载代码

首先我们从 GitHub 下载代码，项目地址是 [https://github.com/peter-iakovlev/Telegram-iOS](https://github.com/peter-iakovlev/Telegram-iOS)。

然后进入目录，下载 git 子模块：`git submodule update --init --recursive`。
然后打开 XCode 的 workspace。

## 申请 API Key

你需要在 [https://my.telegram.org/auth](https://my.telegram.org/auth) 申请一个 API Key 以和服务器进行通讯。

## 运行代码

在开始修改之前，我们先尝试运行一下。首先选择 target 为 Telegram-iOS-Fork。

![](/assets/postAssets/2019/qq20190427-105011-2x.png)

修改 target



### 替换 API Key

然后来到 Telegram-IOS/Supporting Files/BuildConfig.m，将 275 到 331 行的代码替换为如下代码：

```
_apiId = 123456;
_apiHash = @"aaaabbbbccccddddeeeeffffededeeee";
_hockeyAppId = nil;

```

其中，apiId 和 apiHash 为上一步官网申请时获得的。

其实单看提示来看是缺了一个 APP_CONFIG_DATA，它是包含了 apiId、apiHash 和 hockeyAppId 的一个 hex，但是并不知道如何将这三个值变成一个 hex。所以暂时只能替换代码。[GitHub 上有关于这个的讨论](https://github.com/peter-iakovlev/Telegram-iOS/issues/28)。

![](/assets/postAssets/2019/qq20190427-110324-2x.png)

修改前



![](/assets/postAssets/2019/qq20190427-110743-2x.png)

修改后



### XCode 10.2 兼容性问题

如果你是用的 XCode 版本是 10.2，你可能会遇到这个问题，否则你可以跳过这个步骤。在 XCode 10.2 中，会出现 Swift 3 到 Swift 4 的兼容性问题，具体表现是 ManagedAudioSession.swift 中有一个 Expression type 'Bool' is ambiguous without more context 的警告。GitHub 上也有[对应的 issue](https://github.com/peter-iakovlev/Telegram-iOS/issues/27)。目前只能把那一行注释掉来解决问题。

![](/assets/postAssets/2019/qq20190427-111256-2x.png)

注释代码



### 运行

完成以上步骤后，我们就可以点击左上角的播放按钮来编译运行了。不出意外你可以看到编译成功并弹出 iOS 模拟器窗口。登录后你会发现此时频道屏蔽依然有效。

## 修改代码

在自己开始上手之前，我曾经在群里问过有没有人尝试过。有一个人说自己尝试过并且成功了，不过他使用的是原版的 Telegram 客户端。根据他的描述，原版客户端的代码逻辑比较易读，只需要修改以下几个地方即可：







![](/assets/postAssets/2019/image-2019-04-27-10-32-02.jpg)

![](/assets/postAssets/2019/image-2019-04-27-10-32-14.jpg)





![](/assets/postAssets/2019/image-2019-04-27-10-32-39.jpg)

![](/assets/postAssets/2019/image-2019-04-27-10-32-52.jpg)







可以看到业务逻辑非常清晰易读，只需要去掉 `hasExplicitContent` 的判断即可。不过在 Telegram X 中似乎没有这么幸运，这段代码在 Telegram X 中并不存在，因此我被迫寻找别的出路。

经过不断地调试，我最后在 API 调用的反序列化步骤中加入了代码，通过位运算修改了服务器返回的群组的属性实现了频道解禁。

修改的位置在 TelegramCore/Network/Api1.swift 的 `parse_channel` 函数中，我们在读取流的操作之后（1733行）加入位运算代码，将从右数的第九位和第十八位置零，并清空 `_9` 和 `_12` 的内容：

```
_1 = _1! & ~(1 << 9) & ~(1 << 18)
_9 = nil
_12 = nil

```

![](/assets/postAssets/2019/qq20190427-112008-2x.png)

这时候我们再编译运行，可以看到 channel 屏蔽已经解除。

## 真机调试

到这里其实我们只完成了一半：现在只能在模拟器里运行，而由于苹果的限制，真机运行非常麻烦。**如果你没有苹果开发者账号（99刀一年），你会无法使用包括通知推送在内的许多功能**。在进行下面的步骤之前，你需要先在 XCode 中登录自己的 Apple ID。

### 取消没有权限的 capabilities

对于我们的免费证书，很多功能都不能使用。为了通过编译，我们需要把这些“能力”关掉。在左侧列表中点击“Telegram-iOS”、在右边的 target 列表中选择 “Telegram-iOS”，然后在 Capabilities 选项卡中关掉 Associated Domains、iCloud、Push notifications、Siri。

![](/assets/postAssets/2019/qq20190427-114704-2x.png)

关闭后



另外，还需要通过修改代码关闭 Siri 的授权申请，否则运行时会白屏卡住。具体的做法是将 AppDelegate.swift 中的 Siri 授权逻辑部分由判断逻辑直接改成拒绝状态。

![](/assets/postAssets/2019/qq20190427-194551-2x.png)

修改前



![](/assets/postAssets/2019/qq20190427-194527-2x.png)

修改后



### 使用自己的证书对 App 签名

对于**所有的 targets**，在 signing 区块中勾选 Automatically manage signing。

![](/assets/postAssets/2019/qq20190427-114940-2x.png)

然后在每一个 targets 的 Build settings 中的 signing 区块中清空 Code Signing Entitlements。

![](/assets/postAssets/2019/qq20190427-120028-2x.png)

清空 Code Signing Entitlements



### 自定义 Bundle Identifier

把每一个 target 的 bundle identifier 都改掉。除了 Telegram-iOS 之外，其他的 target 的 bundle identifier 应该以 Telegram-iOS 的 bundle identifier 为前缀。比如如果 Telegram-iOS 的新 bundle identifier 是“pro.admirable.telegram”，则 Share 的新 bundle identifier 应该设置为“pro.admirable.telegram.Share”。

![](/assets/postAssets/2019/qq20190427-121619-2x.png)

除此之外，还需要去每一个 target 里的 build settings 选项卡中，修改 User-defined 下的 APP_BUNDLE_ID 为 Telegram-iOS 的 bundle identifier：

![](/assets/postAssets/2019/qq20190427-123802-2x.png)

修改 APP_BUNDLE_ID



### 自定义 App Group

在 Target “Telegram-iOS”的 capabilities -> App Groups 中新建一个 App Groups，名字自己起（**疑似必须与“Telegram-iOS”的 Bundle identifier 保持一致，否则运行时会黑屏出现 Error 2 错误，不确定是否为 XCode 的 bug**。这个问题坑了我好几个小时。）。然后关闭 App Groups 功能再重新打开，然后选择你刚刚新建的项目。接下来的每一个 target 都需要**先关闭 App Groups 功能再重新打开，然后选择你刚刚新建的项目**。

![](/assets/postAssets/2019/qq20190427-122702-2x.png)

除此之外，你还需要前往每一个 target 的 build settings，然后将 User-defined -> Provisioning profile 清空。否则 App Groups 列表下面会有警告。

![](/assets/postAssets/2019/qq20190427-124112-2x.png)

清空 Provisioning profile



### 运行

在完成了以上步骤之后，我们就可以运行了。点击播放图标。经过编译的过程后，telegram 就安装到了你的手机上。为了运行你签名的应用程序，你需要在 iPhone 上前往设置->通用->描述文件，然后信任你自己的开发者证书。

## 后记

对于我这个后端，使用 XCode 修改 iOS 项目还是有点难度的。经过了很多个小时的斗（keng）争，终于实现了频道（channel）屏蔽的解除。不确定对于群组（group）是否有效，欢迎在评论区留言讨论。