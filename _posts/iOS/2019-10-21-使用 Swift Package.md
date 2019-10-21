---  
layout: post  
title: Swift Package 极简指南  
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [Kevin Zhow](https://tips.producter.io/swift-package-ji-jian-zhi-nan/)__  



在 iOS 开发中共享代码，以往的方案是 [CocoaPods](https://cocoapods.org/) 或者 [Carthage](https://github.com/Carthage/Carthage). 但自从 Xcode 11 发布后，Swift Package 也正式成为了一种代码共享的可选方案。

# 使用 Swift Package

Swift Package 的使用要比 Cocoapods 和 Carthage 都简单的多，只需要找到对应的 Git 代码仓库的 URL，然后在 Xcode 找到 `File -> Swift Packages -> Add package Dependency` 即可快速添加。

![Screen-Shot-2019-10-13-at-03.06.36](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.06.36.png)

除此之外，本地的 Swift Package 也可以直接把 Package 文件夹拖到 Xcode 里引用。

这种去中心化，优雅的代码共享方案非常清新，本文将分享如何创建自己的 Swift Package.

# 创建 Swift Package

在 Xcode 中找到 `File -> New -> Swift Package` 即可进入创建流程。
![Screen-Shot-2019-10-13-at-03.11.30](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.11.30.png)

Apple 的[官方文档](https://github.com/apple/swift-package-manager/blob/master/Documentation/Usage.md)也详细说明了如何用命令行创建 Swift Package.

```
$ mkdir swift_package_demo
$ cd swift_package_demo
$ swift package init # or swift package init --type library
$ swift build
$ swift test

```

![Screen-Shot-2019-10-13-at-03.22.31](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.22.31.png)
通过命令行创建后得到的是这样一个目录结构
![Screen-Shot-2019-10-13-at-03.24.41](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.24.41.png)
这个目录没有 iOS 开发者以往熟悉的`.xcodeproj`文件，事实上只要用 Xcode 选择`File -> Open` 直接打开这个 Package 的根目录，就会根据 `Package.swift` 自动生成 Target.
![Screen-Shot-2019-10-13-at-03.26.59](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.26.59.png)

# 了解 Package.swift

Package.swift 只需要知道两部分，就可以用起来了。

## 例子

```
import PackageDescription

let package = Package(
    name: "swift_package_demo",
    products: [
        .library(
            name: "swift_package_demo",
            targets: ["swift_package_demo"]),
    ],
    dependencies: [
    ],
    targets: [
        .target(
            name: "swift_package_demo",
            dependencies: []),
        .testTarget(
            name: "swift_package_demoTests",
            dependencies: ["swift_package_demo"]),
    ]
)

```

一个是对内的 `targets` 以上面配置文件 `.target("swift_package_demo")` 为例，程序会自动到 Source 文件夹里寻找名为 `swift_package_demo` 的文件夹，并把里面所有 public 属性作为接口开放出来。

而对外的 `products` 中，`.library("swift_package_demo")` 则配置了当第三方 App 引用时，需要 import 的 module 名。

`products` 的名称可以随意改成自己希望的样子，比如 `.library("demoPackage")` 那么在其他 App 中添加了这个 Package 后，使用 `import demoPackage` 即可。

![Screen-Shot-2019-10-13-at-03.45.04](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.45.04.png)

# UI 库判断宏

Swift Package 中的代码，使用

```
#if
#endif

```

这种宏代码去判断系统环境，如果我们的 Package 是 UI 相关的，那么需要用

```
#if canImport(UIKit)
public class CustomView: UIView {
}
...
#endif

```

去包裹整个类。

# 发布到 Github

完成后的代码，可以发布到 Github 上，需要保证 Package.swift 是在代码的根目录里，也就是最好遵循下面这基本结构。

![Screen-Shot-2019-10-13-at-03.49.30](/assets/postAssets/2019/Screen-Shot-2019-10-13-at-03.49.30.png)

如果真的需要更改 Sources 文件夹的位置，那么也 Package.swift 要对应的修改

```
.target(
    name: "swift_package_demo",
    dependencies: [],
    path: "./SourceMoved/Sources"),

```

更多的配置项目，可以参考 Apple 的[官方文档](https://developer.apple.com/documentation/swift_packages/target)




