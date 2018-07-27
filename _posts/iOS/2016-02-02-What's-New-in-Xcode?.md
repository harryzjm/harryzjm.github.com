---  
layout: post  
title: What's New in Xcode?  
category: iOS  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__Posted by [chengway](http://chengway.in//)__  

## Getting started  

本章 demo 叫做 **Local Weather**，是一个基于你的地理位置显示天气的 APP。你可以在真机上运行一下，下面让我们来探索 Xcode 的新特性。  

![][1]  

> 想要看到 energy gauge 只能在真机上运行  

### Free provisioning  

Xcode 7 最大的变化是允许你免费真机调试了，也就是说不用每年交 99 美金也可以在你的手机上运行你写的程序了，但如果提交上架还是需要加入开发者计划。  

使用免费的 Provisioning 在真机上运行看[这里][2]  

> 本章天气的 API 来自于 [openweathermap.org][3]  

## Energy impact gauge  

我们来研究一下 **Energy Impact**  

![][4]  

**Energy Impact** 显示了你 App 的耗电情况  

![][5]  

Utilization 部分显示了当前时刻的 **energy impact**，右边的 average 是平均值  

在底部，有四行分别代表 CPU、网络、位置和后台。每个小方格代表 1 秒的状态，如果这 1 秒钟状态是活跃的，则小方格会被灰色填满。  

注意，CPU 和 位置状态始终是活跃状态，而网络活跃一段时间会停 4 ~ 5 秒钟，后台状态则是完全不活跃状态。  

按下 Home 键将 App 退到后台，此时将会中止网络和位置状态，而后台状态变成活跃，CPU 始终是活跃状态。  

![][6]  

观察一下 console，log 表明所有的后台程序将在 10.79 秒后结束，但是后台 energy graph 不会中止  

![][7]  

## Code browsing features  

新版 Xcode 允许我们接手一个新项目时，能够快速熟悉整个 App 结构  

### Interface of Swift classes  

Swift 和 Objective-C 的一个显著区别就是没有头文件了，但头文件让我们可以快速熟悉一个类的用途，真的是很方便。Xcode 7 终于让 Swift 也能显示头文件了  

随便打开一个 swift 文件 `WeatherViewController.swift` ，打开 **assistant editor** 点击 assistant editor 菜单，选择 **Counterparts (1) ▶ WeatherViewController.swift (Interface)**  

![][8]  

> 你也可以选择 Generated Interface  

![][9]  

私有变量和方法并不会显示出来，还注意到头文件中的注释了吗？只有在源文件中使用 `///` 或 `/**` 才会在 Interface 中显示注释  

![][10]  

你也可以为 Objective-C 的头文件生成 Swift 接口。我们找一对用 Objective-C 写的类文件：`RWHTTPManager.h` 和 `RWHTTPManager.m`，`RWHTTPManager` 类用 OC 语法封装了 `NSURLSession`  

![][11]  

现在用同样的方法转成 Swift 接口：  

![][12]  

是不是很奇幻，用 Swift 生成的新接口貌似更加通俗易懂  

这里有两个小 issue，可能是 OC 转 Swift 时编译器还不那么完美：  

1.注意转换后 `baseURL` 作为属性是 optional，而作为参数是 non-optional 的。但是 baseURL 显示是必须的。我们在 OC 文件中修正一下，用 `_Nonnull` 替换 `_Nullable`  

    @property (nonatomic, strong) NSURL * _Nonnull baseURL;  

保存，再生成一次 Swift 接口，现在 baseURL 变成 non-optional 的了  

    var baseURL: NSURL  

2.另外一个 issue 是在 `fetchJSONAtPath` 方法中注意参数 `relativePath`，在 Swift 接口中也变成可选的了，但是通过文档我们知道这个参数不能为 nil，同样的方法，用 `_Nonnull` 替换 `_Nullable`  

### New documentation features  

现在 Xcode 7 中的注释支持 markdown 语法了，NSHipster 有篇文章很棒，看[这里][13]  

### Find call hierarchy  

现在查找指定方法在哪里被调用也很方便，选中方法右键或 Control 单击，弹出菜单选择 Find Call Hierarchy 即可  

![][14]  

## Decreasing energy impact  

回到我们的 App 上来，现在有点费电，下面来修复一下。在开始前，先回顾下整个 App 的工作流程：  

1. 请求用户当前位置  
2. 一旦获取到用户位置，使用 Http 请求抓取当地天气  
3. 收到天气数据后，更新 UI 并且定时 15 秒后再次发送更新请求  
4. countdownLabel 显示倒计时，距下次发送请求还有多少时间。计时间隔为 0.1 秒  

我们可以搜索 **// Step**，查看详细的步骤：  

![][15]  

回想一下之前在 **energy impact** 中网络的活跃状态，活跃 10 ~ 11 秒后跟随 3 ~ 5 秒的非活跃状态，这是因为只要发出网络请求，他会持续 10 秒钟，即使已经完成了请求  

这会导致每次网络请求都会很耗电，你可能认为 15 秒只发一次请求，只占 7%，对资源消耗并不严重，但这只是理想状态，真实的情况是每 15 秒发一次请求，网络请求会持续 11 秒，时间占用达到了 73%  

这是我们第一个要修复的问题  

### Reducing network energy impact  

天气虽然变化很快，但 15 秒更新一次的频率显然有点太快了。我们让他再每次启动时更新一次就够了，因为这也符合用户习惯，打开看一眼就关掉了。  

注释掉 Step 6 每隔 15 秒更新的代码  

    // Step 6: Set a timer to fetch the weather again in 15 seconds  
    // networkFetchTimer = NSTimer  
    //  .scheduledTimerWithTimeInterval(15, ...  

运行，**Energy Impact** 结果好了很多  

![][16]  

### Reducing CPU energy impact  

每隔 0.1 秒更新一次 view 的倒计时动画是消耗 CPU 的罪魁祸首，让我们停掉他  

    // Step 7: Update the countdown label every 0.1 seconds using a timer  
    // countdownUpdateTimer = NSTimer.scheduledTimerWithTimeInterval(0.1 ...  

同时也不需要 `countdownLabelStackView` 显示了  

    // countdownLabelStackView.hidden = false  

现在又好了很多，不是吗？  

![][17]  

### Reducing location energy impact  

我们获取到用户地理位置就不该再继续请求了，iOS 9 提供了新的请求方法 `requestLocation()` 他成功请求一次用户位置就会停止继续请求  

    // Step 2: Request the location  
    locationManager.requestLocation()  

![][18]  

### Reducing background energy impact  

进入后台，我们通过控制台发现 11 秒后，后台任务已经完成了，但后台线程依然在消耗电池资源。这是因为调用 `beginBackgroundTaskWithExpirationHandler(_:)` 执行后台任务完成后，我们并没有调用 `endBackgroundTask(_:)` 告知系统你的任务已经结束了。  

在 `performBackgroundWork()` 方法末尾手动补上就行了  

    print("Background work completed in: (formattedElapsedTime) " +  
      "sec")  
    UIApplication.sharedApplication().endBackgroundTask(  
      backgroundTaskIdentifier)  

至此，你已经修复了所有的耗电问题  

![][19]  

### Core Location instrument  

如果你想深挖一下用户位置是如何获取的，iOS 9 的新 **Core Location instrument** 很可能适合你。运行 App，去 **energy gauge** 界面，点击 **Location** 按钮  

![][20]  

![][21]  

**Instruments** 将会打开运行 **Core Location instrument**  

![][22]  

注意第二行 "CLLocationManager changed accuracy to kCLLocationAccuracyBest"，获取到这种精度的位置信息花费了 892.03 ms，天气 App 显然不需要这么细的精度，改成 `kCLLocationAccuracyKilometer` 就足够了  

    locationManager.desiredAccuracy = kCLLocationAccuracyKilometer  

这次精度调低，获取地理位置的时间也加快了上百倍  

![][23]  

## Playground improvements  

天气 App 优化到此结束，我们下面来玩一下 Playground，Xcode 7 还是增加了很多新特性  

### Rich playground authoring  

现在 playground 支持 Markdown 语法了，你可以用 Markdown 语法写完，然后开启 Render Documentation 渲染  

![][24]  

开启渲染  

![][25]  

单行注释用 `///` 或 `/**`，多行用 `/*`: 和 `*/`，更多 Markup 格式看[这里][26]  

### Playground pages  

现在你可以在 playground 里添加多个页面了，回到 **project navigator**，点击左下角加号按钮，选择 **New Page**  

![][27]  

添加完毕，将第一个命名为 Home  

![][28]  

选中 Page Two，会发现 Previous 和 Next 两个链接（需要关闭 `Render Documentation` 才能看见）  

    //: [Previous](@previous)  

    import Foundation  

    var str = "Hello, playground"  

    //: [Next](@next)  

@next 和 @previous 代表特殊符号，用来链接前后的页面，如果要链接到指定页面，需要提供 page name，如果名字中间有空格用 **%20** 代替  

可以在 Page Two 页面的任意位置添加下面的链接（跳转到 Home）  

    //: [Jump to Home](Home)  

在 Home 页面添加跳转 Page Two 的链接  

    //: [Jump to Page Two](Page%20Two)  

### Inline results  

**Inline results** 允许你在 playground 里直接看运行结果，比如我们写个 view，在右边的 sidebar 里点击 **Show Result**，可以直接查看渲染好的 view  

![][29]  

在 view 变量下面直接可以看到渲染结果  

![][30]  

改变 view layer 的 borderWidth 到 40，渲染结果也跟着更新  

![][31]  

### Sources and resources  

现在你可以在 playground 里添加辅助的源文件和资源文件了（分别放在 **Sources** 文件夹和 **Resources** 文件夹）将这些支持文件放到相关文件夹里，可以使结构更清晰  

![][32]  

每一个 playground page 都有自己的 sources 和 resources 文件夹，且优先于使用自己的支援文件夹里的内容  

### Manually run playgrounds  

不想每次在 playground 上做点修改都自动编译运行，机器还卡成狗，现在你可以手动控制允许了  

![][33]  

## Other improvements  

**Storyboards** 和 **Interface Builder** 还有几个改进：  
* Control-dragging 从 View 到另一个 View 加约束的时候，按住 Option 键，将会看到可添加的 constants  
* 现在可以设置一个 view 的 `layout margins` 和为约束（constraint）设置一个标识（identifier），这样出现在 document outline 中的 constraint 有了更好的可读性。  

还有很多新特性需要你自己去挖掘  

### Address sanitizer  

Xcode 推出了一个新的工具，会帮助捕获在使用 Objective-C 或 C 时，可能出现的内存损坏错误  

你可以去 **Product Scheme Edit Scheme** 中开启：**Enable Address Sanitizer**  

![][34]  

> 开启后，Xcode 将添加额外的 instrumentation 来构建你的应用程序，以便于更好地找出内存错误  

### Right-to-left support  

iOS 9 的一个重大更新是开始支持从右到左的语言，如果你使用了 Auto Layout，那么几乎不需要你做什么工作就能正常在这种语言环境下使用  

Xcode 提供了一个不需要更改语言环境就能测试 view 在**从右到左**环境下的特性  
，编辑你的 scheme，在 Options 界面下，展开 **Application Language**，这里有个 **Right to Left Pseudolanguage** 选项，勾上就能开心地测试了~  

![][35]  

iOS 9 by Tutorials 全书到此结束，终于写完了，呼呼~  

* * *  

-EOF-  

[1]: /assets/postAssets/2016/61b207a9jw1ezhis0pvp5j208l0ezmyz.webp  
[2]: https://developer.apple.com/library/ios/documentation/IDEs/Conceptual/AppDistributionGuide/LaunchingYourApponDevices/LaunchingYourApponDevices.html  
[3]: openweathermap.org  
[4]: /assets/postAssets/2016/61b207a9jw1ezhj14wuwfj209k096gmk.webp  
[5]: /assets/postAssets/2016/61b207a9jw1ezhj2qanxnj20pw0a0dhr.webp  
[6]: /assets/postAssets/2016/61b207a9jw1ezhje5ydpvj20pw0aiwga.webp  
[7]: /assets/postAssets/2016/61b207a9gw1ezhjnv9do2j20g8063n0o.webp  
[8]: /assets/postAssets/2016/61b207a9jw1ezhk0lhfg1j20h7030aag.webp  
[9]: /assets/postAssets/2016/61b207a9jw1ezhksrsg2uj20tk0ektdf.webp  
[10]: /assets/postAssets/2016/61b207a9jw1ezhkx4h00fj20tq07a0uz.webp  
[11]: /assets/postAssets/2016/61b207a9jw1ezhl2w8nbqj20jw04gwfs.webp  
[12]: /assets/postAssets/2016/61b207a9jw1ezhl3mt2nzj20jt03lt9j.webp  
[13]: http://nshipster.com/swift-documentation/  
[14]: /assets/postAssets/2016/61b207a9jw1ezhllczroij20dk04fwf3.webp  
[15]: /assets/postAssets/2016/61b207a9jw1ezhprybddbj20fr09l0up.webp  
[16]: /assets/postAssets/2016/61b207a9gw1ezhq7kue4bj20la07bgmo.webp  
[17]: /assets/postAssets/2016/61b207a9jw1ezhqj5jey2j20l0079dgx.webp  
[18]: /assets/postAssets/2016/61b207a9jw1ezhqnahfexj20l907f0ti.webp  
[19]: /assets/postAssets/2016/61b207a9jw1ezhqv3jkryj20kz07fmy2.webp  
[20]: /assets/postAssets/2016/61b207a9jw1ezhqzgmpgqj20kw03kq3e.webp  
[21]: /assets/postAssets/2016/61b207a9jw1ezhr8ulueuj20ba0450t9.webp  
[22]: /assets/postAssets/2016/61b207a9jw1ezhrahfjncj20q5079mz3.webp  
[23]: /assets/postAssets/2016/61b207a9jw1ezhre06f21j20q4075mz0.webp  
[24]: /assets/postAssets/2016/61b207a9jw1ezhrkntm9sj20pv02c74p.webp  
[25]: /assets/postAssets/2016/61b207a9jw1ezhrldtb09j20pu07dq3o.webp  
[26]: https://developer.apple.com/library/ios/documentation/Xcode/Reference/xcode_markup_formatting_ref/index.html#//apple_ref/doc/uid/TP40016497  
[27]: /assets/postAssets/2016/61b207a9jw1ezhrrvkvu3j206a055glp.webp  
[28]: /assets/postAssets/2016/61b207a9jw1ezhrsrm5p6j208b03tq2v.webp  
[29]: /assets/postAssets/2016/61b207a9jw1ezhs3gg4kyj20nq04d3z9.webp  
[30]: /assets/postAssets/2016/61b207a9jw1ezhs4hbfzwj20am056gm5.webp  
[31]: /assets/postAssets/2016/61b207a9jw1ezhs5tg2sbj20al057aa3.webp  
[32]: /assets/postAssets/2016/61b207a9jw1ezhs83cniij207f06874f.webp  
[33]: /assets/postAssets/2016/61b207a9jw1ezhsdx0wvfj207g02ijrc.webp  
[34]: /assets/postAssets/2016/61b207a9gw1ezhsqulqpsj20tb07a0ud.webp  
[35]: /assets/postAssets/2016/61b207a9jw1ezhsxdraz4j20ia05mwff.webp  

