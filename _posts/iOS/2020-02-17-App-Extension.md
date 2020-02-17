---  
layout: post  
title: App Extension 
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [小东邪](https://xiaodongxie1024.github.io/2018/10/24/appExtension/)__  

## 一. 基本知识

#### 1\. 定义

简单的说,App Extension 可以让开发者们拓展自定义的功能和内容到应用程序之外,并在用户与其他应用程序或系统交互时提供给用户。

#### 2\. 用途

你可以创建一个app extension通过打开一个特殊的开关。例如

* Share extension: 让用户从浏览器分享至其他社交软件中。
* Today widget:为了让用户赶上去看喜欢的比赛你可以再通知中心中提供一个小部件显示比赛时间提醒等信息。
* 甚至可以创建一个app extension 提供定制的键盘让用户可以使用它来代替系统的键盘。

<div style="display:flex;align-items:center;">
  <div>
    <img src="/assets/postAssets/2019/15819146956032.jpg">
  </div>
  <div>
    <img src="/assets/postAssets/2019/15819147108130.jpg">
  </div>
</div>

#### 3\. 类型

[Extension point](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/index.html) : 启用扩展的区域称为扩展点,也就是每一个具有特定功能具体的extension。

> 每个扩展点提供了使用说明和API为开发者去创建一个app extension.

下表是苹果官方提供的所有Extension point列表

![](/assets/postAssets/2019/15819177348293.jpg)

#### 4.本质

每一个extension都是一个独立的二进制文件,它独立于用于发布它的应用程序。我们必须使用一个app去包含并且发布你的extension。

## 二. 主要概念区别

* **App**: 就是我们正常手机里的每个应用程序,即Xcode运行后生成的程序。一个app可以包含一个或多个target,每个target将产生一个product.
* **App extension**: 为了扩展特定app的功能并且依赖于一个特定的app的一条进程。
* **Containing app**: 一个app包含一个或多个extension称为containing app。
* **Target**: 在项目中新建一个target来创建app extension.任意一个target指定了应用程序中构建product的设置信息和文件。
* **Host app**: 包含 app extension 并且能从中打开它(并不一定非要从此app内部打开, 可以是app内部也可以是例如 Today Widget 外部控件)。我们可以把它理解为宿主的App, 能够调起 extension 的 app 被称为 host app, 比如 Safari app 里面网页分享到微信, Safari 就是 host app; widget 的 host app 就是 Today。

[Xcode Target](https://developer.apple.com/library/content/featuredarticles/XcodeConcepts/Concept-Targets.html#//apple_ref/doc/uid/TP40009328-CH4) 介绍

* 我们通过Xcode新建一个target,Xcode会为每一种extension point提供一个模板,每种模板里会提供特定的源文件(源文件中会包含一些示例代码)和设置信息,build这个target将会生成一个指定的二进制文件被添加到app’s bundle中。

* 当我们要发布的APP中包含app extension,开发者需要提交a containg app到 App Store. 当用户安装了这个containg app, extensions也会被随之安装。如果要开启app extension功能,需要用户手动去触发它,触发的地方可能是containing app 内部也可能是外部,例如Today widget 这个extension 需要用户在通知中心点击编辑按钮去添加,还有比如需要在偏好设置中去管理的extensions等等.

## 三. App Extension 工作原理

#### 1\. 本质

app extension不是一个app, 它是为了实现了一个特定的的任务,不同的extension point定义了不同的任务。

#### 2\. 生命周期

因为app extension不是一个app,它的生命周期和app是不同的,在大多情况下,当用户从app的UI上或者其他活动视图控制器中选择开启extension功能的选项时将会开始执行。

* 开始:A host app 定义了上下文提供给extension, 当它发送一个请求并且用户正确相应后开启extension的生命周期。

* 结束:通常会在完成host app收到的请求后立即终止。

> 例如,当用户从Host app 中选择一张图片然后长按图片点击分享按钮,用户可以从可分享的列表中进行选择,选择后将会完成分享的动作,此时分享的extension将会结束。

![](/assets/postAssets/2019/15819181790939.jpg)


## 四. App Extension 如何和 App 通讯

#### 1\. 简单交互

![](/assets/postAssets/2019/15819181868798.jpg)

* app extension 和 containing app 将不能够直接交互,典型的,containing app可能还没有开始运行然而它包含的app extension已经在运行了。（例如,一个天气的app,当你还没有打开它时,你可以在Today Widget中看到今天天气的信息）

* 在一个典型的请求响应事务中,系统代表的host app打开app extension, 通过host提供的extension上下文(context)传递数据, 这个extension通过界面的展示来执行一些任务,如果适用于extension的目的,返回数据给host.

* 上图的虚线代表了app extension 和 containing app之间有限的交互。例如Today widget(只有 Today Extension 才支持通过调用其他不可以) 通过调用 NSExtensionContext类中`openURL:completionHandler:`方法来要求系统去打开它的containing app.

#### 2\. 具体交互

正如下图的读写箭头所示,任意一个app extension和它的containing app能够在一个私有的shared container中分享数据。下图展示了containing app , app extension 和 host app之间完整的交互方式。

![](/assets/postAssets/2019/15819182092013.jpg)

> 注意:系统使用进程间通信来确保host app和app extension可以一起工作从而实现一个完整的体验。在你的代码中,你不必考虑它们之间潜在的通信规则,因为你使用了extension point 和 系统提供的上层API。

## 五. App Extensions 不可用的API

App extension不能够像containing app一样直接进行一些动作,它包括如下:

* 不能使用 sharedApplication 对象及其其中的方法。
* 使用NS_EXTENSION_UNAVAILABLE 宏在头文件中标记的任意API或类似的不可用的宏或API在一个不可用的框架中。例如,在iOS 8.0中,the HealthKit framework and EventKit UI framework 将不能使用app extension.
* 不能在iOS设备中使用相机和麦克风(不像其他app extensions,iMessage app可以访问这些资源,只有它正确的配置 NSCameraUsageDescription and NSMicrophoneUsageDescription Info.plist 文件中的Key)。
* 不能长期运行后台任务,该限制的具体细节因平台而异。(一个app extension能够使用NSURLSession对象启动一个上传或下载并将这些操作的结果返回给containing app)
* 不能使用Air Drop接收数据(一个app extension能够像一个正常的app一样通过UIActivityViewController class去使用AirDrop发送数据)

## 六. 创建App Extension

#### 1\. 选择Extension Point

每个extension point都针对一个特定的用户场景。你的第一步是选择支持你计划交付功能的extension point.这个选择将决定你你能够使用哪些API以及在特定情景下API的使用方式。

> 在iOS 和 OS X 中支持extension points, NSExtensionPointIdentifier中描述了它们的info.plist 中extension point中标识符的key.

#### 2\. 在Xcode项目中新建target

为你需要使用的app extension 选择一个合适的extension point, 之后需要添加一个新的target在你的containing app中。使用Xcode template是最简单的方式来添加一个app extension为你的extension point提供预先配置好的target。

![](/assets/postAssets/2019/15819182636450.jpg)

![](/assets/postAssets/2019/15819182734738.jpg)

#### 3\. 具体步骤

* 在Xcode项目设置信息的Capabilities中打开某些extension point必需的开关,注意部分需要在apple developer后台中将app id中权限放开。
* 打开Xcode,上方工具栏选择File->New->Target.
* 在新弹出的对话框中选择Application Extension中你需要的extension point.
* 完成后将自动添加一个target在你的项目中,并且包含一些示例代码。
* 当你build一个extension模板时,如果成功将生成一个以.appex结尾的extension bundle文件。

#### 4\. 注意:

* app extension target 在项目配置build setttings的Architectures选项下必须包含arm64(iOS) 或x86_64(OS X)架构,否则发布时将被App Store拒绝。一般来说,当你新建一个app extension target 时Xcode将包含适合的64位带有“Standard architectures” 的architecture。
* 如果containing app target链接时嵌入一个framework,那么必须包含64位 architecture否则发布也将被拒。
* 你可以在[About 64-Bit Cocoa Touch Apps](https://developer.apple.com/library/content/documentation/General/Conceptual/CocoaTouch64BitGuide/Introduction/Introduction.html#//apple_ref/doc/uid/TP40013501)这篇文章中你将能够了解更多依靠你的target平台有关64位development信息。

## 七. 检查App extension默认模板

#### 1\. 模板结构

每个app extension模板都包含一些配置文件如Info.plist,一个view controller class和一个默认的user interface,所有的这些将都由extension point定义。默认的view controller class可以包含你要实现的extension point方法。

#### 2\. Info.plist介绍

app extension target的Info.plist文件可以标识extension point,并制定extension的详细信息。这个文件至少要包含NSExtension这个key和这个extension point指定的含有键值对的字典。例如,NSExtensionPointIdentifier key将需要一个值来展示extension point反向DNS的名字,例如com.apple.widget-extension。下面列举了一些在NSExtension字典中的键值对。

* NSExtensionAttributes:extension point特定的一些属性,如Photo Editing extension中的PHSupportedMediaTypes
* NSExtensionPrincipalClass: 模板创建的view controller class的名字(例如SharingViewController),当一个host app调用extension,这个extension point将实例化这个类。
* NSExtensionMainStoryboard: the extension默认的storyboard文件,通常被命名为MainInterface。

#### 3\. 其他设置

除了plist文件中的设置,默认情况下,模板可能会设置一些功能。每个extension point能够定义capabilities使extension point支持的任务类型变得有意义。例如,iOS 文档Provider extension包含com.apple.security.application-groups entitlement.

OS X app extension 所有的模板将默认包含App Sandbox 和 com.apple.security.files.user-selected.read-only entitlements。如果需要去做一些其他事情例如访问网络或者访问照片,联系人等信息时你需要定义额外的capabilities对于extension。

## 八. 响应 Host App 的请求

#### 1\. 触发

在用户接受一个带有host app请求的app extension时app extension将被打开。app extension在收到请求后会打开帮助用户执行特定任务,具体是完成或者取消任务取决于用户在UI界面上的动作。例如,Share Extension收到一个host app请求之后通过弹出一个分享的view作为响应。用户将可以通过这个View上选择分享的目标或者是取消本次分享。

当一个host app发送一个请求给app extension,它将指定一个extension context.对于大部分extensions,context最重要的部分是在extension中设置用户想要的items工作。例如,OS X Share extension 的 context可能包含一个用户想要发送的文本选择信息。

#### 2\. 步骤

* 发请求

一旦Host app 发出请求(通常调用`beginRequestWithExtensionContext:`方法),app extension可以使用 extensionContext属性在主view controller中获取这个context.子view controllers也能通过链接访问该属性。

* 获取Context

你可以使用 NSExtensionContext类去检查这个context并且得到它的items。它可以很好地在视图控制器的loadView方法中后去这个context和Items以便在你的视图中展示需要的信息。代码如下 `NSExtensionContext *myExtensionContext = self.extensionContext;`

* 获取Items

context 对象的inputItems属性中包含了extension 需要使用的所有items。 `NSArray *inputItems = myExtensionContext.inputItems;`

每个NSExtensionItem对象包含了该tiem各方面的很多属性,例如它的title, content text, attachments, and user info.

> 注意: attachments属性包含了与item关联的media data数组。例如,在关联sharing request的item中,attachments 属性包含了用户想要去分享网页的信息。

* 完成或取消任务

app extension给用户一个选择去完成或取消此次任务。我们可以通过`completeRequestReturningItems:completionHandler:`方法来选择返回NSExtensionItem对象给host app,或者`cancelRequestWithError:`方法,返回一个错误代码

> 注意: 如果app extension调用`completeRequestReturningItems:completionHandler:`方法将提供一个completionHandler回调,系统要求你至少应该暂停app extension。

#### 3.注意

在iOS系统中,app extension 可能需要更多时间来完成一个潜在的耗时任务。例如上传一个网页的内容。在这种情况下,你可以使用NSURLSession class在后台进行传输。因为后台传输使用一个独立的进程,传输会继续,作为一个低优先级的任务,extension 的进程在完成host app请求后应该被终止。

尽管我们可以在后台完成上传或下载的任务,但是其他后台任务例如支持VOIP或者后台播放音乐等在extensions中不能被实现。如果app extension的Info.plist文件中包含UIBackgroundModes,发布时将会被拒。

## 九. 性能优化

#### 1\. 设计简洁的UI

用户感觉灵活轻便。设计您的extension,以便在一秒钟内完成目标。启动速度过慢的扩展由系统终止。

原则: 简单,集中完成一个单一的任务。

> 注意: extension 的图标要与app保持一致。

#### 2\. 内存

运行extension的内存限制远小于前台应用程序的内存限制。在这两个平台上,系统可能会主动终止extension,因为用户希望返回主机应用程序中的host app。某些extension可能比其他extension的内存限制更低,例如widgets必须特别高效,因为用户可能同时打开多个widgets。

#### 3\. 运行

app extension 一旦开启后是一条独立的进程,不在containing app 主运行循环中,如果extension的回调在主运行循环,它可能有一个较差的用户体验在另一个extension或app.

> 注意:app才是系统资源的主要使用者,extension只是辅助。

## 十. iOS App extension 测试

#### 1\. Debug, Profile, and Test Your App Extension

* 你必须为containing app 和 它的app extensions提供各自签名信息(即创建不同的apple id但extension的app id 是app的子id).

* 使用Xcode去debug一个app extension就像去degbug其他进程一样,不同的是,在extension scheme 运行阶段,你要指定一个host app作为可执行文件。指定完成后,Xcode调试器将附加到该extension。

* 当你将Xcode运行的target选择到你的extension时,在运行时将会弹出选择一个app去运行,如果你想要每次都选用一个指定的,你需要进行一下的操作

* 编辑scheme,在弹出菜单中选择Run,在右侧的Info信息中将Executable选择到我们的host app.

#### 2.注意

* 在你build或run app extension之前,确保选择了正确的extension’s scheme去调试。如果你直接去调试containing app scheme,Xcode不会将你的app extension附加上去除非你从containing app 中调用它。

* 在Xcode debug控制台的日志中,app extension的二进制文件可能与CFBundleIdentifier属性的值相关联,而不是CFBundleDisplayName属性的值。

* 如果直接运行containing app在控制台Log信息中看不到extension 文件中打印的信息。

## 十一. 过审须知

* 1\. 发布App时为了过审,containing app必须提供基本功能给用户,同时不能只有app extensions.

* 2.为了过审,无论你为containing app选择哪种目标设备系列,都必须为您的应用扩展程序指定“iPhone / iPad”（有时称为universal）作为目标设备系列。

## 十二. 处理常见场景

#### 1\. 打包包含extension代码Framework

我们可以创建一个framework在containing app 和app extension之间共享代码。

* 我们需要在包含extension的Target build setting中将“Require Only App-Extension-Safe API”设置为YES。如果你不这么设置,Xcode会提醒你“linking against dylib not safe for use in application extensions”.

* 为了确保你的framework不包含app extensions不可用的API,如果您有一个包含此类API的自定义框架,您可以从containing app中安全地链接到该框架,但不能与该应用程序包含的extensions共享该代码。

当配置Xcode的project时,在Copy Files build phase中你必须选择“Frameworks”作为destination在你的framework中。

[Deploying a Containing App to Older Versions of iOS](https://developer.apple.com/library/content/documentation/General/Conceptual/ExtensibilityPG/ExtensionScenarios.html#//apple_ref/doc/uid/TP40014214-CH21-SW3)

[Building Modern Frameworks](https://developer.apple.com/videos/wwdc2014/#416)

#### 2\. Containing App中分享数据

##### 关系

app extension 和 containing app 之间不能直接访问彼此的存储数据的容器。

但我们可以共享数据。

> 注意:app extension 的target工程不可以直接访问应用程序沙盒。

##### 共享数据

为了使用数据共享功能,我们需要在当前Target设置中的Capabilities中,打开App Group开关,并且在apple developer中创建APP Group,并向我们当前target和containing app的app id中打开并配置app group功能。
[Adding an App to an App Group](https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/EnablingAppSandbox.html#//apple_ref/doc/uid/TP40011195-CH4-SW19)

* APP group : 允许单个开发团队生成的多个app共享对一个特定的group container访问。这个容器不适合面向用户,例如共享缓存或数据库。

配置成功后,app extension和containing app可以使用 NSUserDefaults API共享一个容器来同步需要交互的数据。我们可以使用下面的API

```swift  
// Create and share access to an NSUserDefaults object
NSUserDefaults *mySharedDefaults = [[NSUserDefaults alloc] initWithSuiteName: @"com.example.domain.MyShareExtension"];

// Use the shared user defaults object to update the user account
[mySharedDefaults setObject:@"Hello World!" forKey:@"小东邪"];

[shared synchronize];
```  

可以通过下面的方法从shared container中读取存入的数据。

```swift  
- (NSString *)readDataFromNSUserDefaults { 
    NSUserDefaults *shared = [[NSUserDefaults alloc] initWithSuiteName:@"group.wangzz"]; 
    NSString *value = [shared valueForKey:@"小东邪"]; 
    return value; 
}
```  

下图展示了containing app , extension 与shared container之间的关系。

![](/assets/postAssets/2019/15819186189031.jpg)

> 注意:当我们建立好一个共享容器时,containing app 和 每个app extension 都具有对容器读写的权限,所以我们必须要考虑数据同步的问题。

- 保存数据的时候必须指明group id；

- 而且要注意NSUserDefaults能够处理的数据只能是可plist化的对象,详情见Property List Programming Guide。

- 为了防止出现数据同步问题,不要忘记调用[shared synchronize];

#### 3\. 访问网页

在Share extension 和 Action extension(仅iOS)中,可以让用户访问web内容通过请求Safari运行JavaScript文件并将结果返回到扩展名。

#### 4\. 执行上传和下载

#### 5\. 声明支持的数据类型

#### 6\. 将Containing app 部署到老版本的应用中

> 3-6的具体步骤可参考[苹果官方文档](https://developer.apple.com/library/content/documentation/General/Conceptual/ExtensibilityPG/)

#### 总结  

本文是我在阅读APP官方文档后将官方文档中不易理解的一些东西图形化并针对例如app,extension,host app, containing app等混淆概念统一对比,更易于理解,在做每一种具体的extension中肯定会遇到不同的问题,所以整体先了解extension的工作原理及注意点还是十分必要的,关于更多内容请参考[苹果官方文档](https://developer.apple.com/library/content/documentation/General/Conceptual/ExtensibilityPG/)