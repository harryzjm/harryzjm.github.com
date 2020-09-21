---  
layout: post  
title: CocoaPods的资源管理和Asset Catalog优化  
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [小猪](https://dreampiggy.com/2018/11/26/CocoaPods%E7%9A%84%E8%B5%84%E6%BA%90%E7%AE%A1%E7%90%86%E5%92%8CAsset%20Catalog%E4%BC%98%E5%8C%96/)__  

## Asset Catalog和App Thinning

Asset Catalog，是Xcode提供的一项图片资源管理方式。每个Asset表示一个图片资源，但是可以对应一个或者多个实际PNG图，比如可以提供`@1x`, `@2x`, `@3x`多张尺寸的图以适配；在macOS上，还可以通过指定日间和夜间不同Appearances的两套图片。

这种资源，在编译时会被压缩，然后在App运行时，可以通过API动态根据设备scale factor（Mac上日夜间设置）来选择对应的真实的图片渲染。

[App Thinning](https://help.apple.com/xcode/mac/current/#/devbbdc5ce4f)，是苹果平台（iOS/tvOS/watchOS）上的一个用于优化App包下载资源大小的方案。在App包提交上传到App Store后，苹果后台服务器，会对不同的设备，根据设备的scale factor，重新把App包进行精简，这样不同设备从App Store下载需要的容量不同，3x设备不需要同时下载1x和2x的图。

但是，这套机制直接基于Asset Catalog，换言之，只有在Asset Catalog中引入的图片，才可以利用这套App Thinning。直接拷贝到App Bundle中的散落图片，所有设备还是都会全部下载。因此如何尽量提升Asset Catalog利用率，是一个很大的包大小优化点。

## CocoaPods的资源管理

CocoaPods是一个构建工具，它完全基于Pods的spec文件规则，在Podfile引入后，生成对应构建Xcode Target。也就是它是一个声明式构建工具（区别于Makefile这种过程式的构建工具）。对于资源的管理，目前有两个方式进行声明并引入，即`resources`和`resource_bundles`，参考[podspec syntax](https://guides.cocoapods.org/syntax/podspec.html)

虽然Podspec中包含所有待构建库的声明，但于CocoaPods也会根据Podfile的配置，动态调整最终的Xcode工程的配置，根据是否开启`use_framework!`，以下的资源声明最终的行为有所不同，这里分开介绍。

### 不使用use_framework!

当不使用use_framework!时，最终对Pod库，会创建单独的静态链接库`.a`的Target，然后CocoaPods会对主工程App Target增加自己写的脚本来帮助我们拷贝Pod的资源。

* `resources`字段

对应参数是一个数组，里面可以使用类似`A/*.png`通配符匹配。所有匹配到的资源，如图片。

在`pod install`完成后，CocoaPods会插入一个生成的脚本[CP] Copy Bundle Resource（注意，这并非Xcode本身构建过程），拷贝到编译完成后的App Main Bundle的根路径下。

也就是说，如果匹配到了一个`A/1.png`和`A/2.plist`，这个`1.png`和`2.plist`，最终会出现在ipa包的展开根路径中。

```  
| Info.plist
| 1.png
| 2.plist
| News
| xxx
```  

优点：

1. 最简单暴力，而且由于固定了资源的路径在根路径上，如果先前在主工程目录中使用的代码，不需要更改一行即可继续使用（原因是主工程的你拖一个图片文件夹，Xcode的构建过程默认就是把资源放到App Main Bundle的根路径上的）。

缺点：

1. 严重的命名冲突问题，由于通配符会拷贝所有文件到根路径，因此如果出现如下 `A/1.png, B/1.png`两个文件同时匹配（B是另一个库的文件夹），将会出现冲突，CocoaPods采取的方式是暴力合并，会有一个被替换掉。因此，这要求所有资源文件命名本身，加入特定的前缀以避免冲突。类似的不止是图片，所有资源如`bundle`, `js`, `css`都可能存在这个问题，难以排查。而且由于这种拷贝到根路径的机制，这个问题不可从根源避免。
2. 无法享用任何Xcode的优化，Xcode对于所有内建的Copy Bundle Resource中添加的PNG/JPEG图片，会进行一次压缩减少大小（注意，这和App Thinning不一样）。而CocoaPods这种使用自己的Shell脚本暴力拷贝，源文件和Bundle的文件是完全一样的。

* `resource_bundles`字段

对应参数是一个字典，里面的Key表示你所希望的一组资源的资源名，常见值是`库名+Resource`，Value是一个数组，里面和`resources`一样允许通配符匹配资源。

当`pod install`完成后，CocoaPods会对所有的Pods中声明了`resource_bundles`资源，以Key为名称建立一个单独的Bundle Target，然后根据Value匹配的值，把这些图片资源全部加到这个Target的Xcode内建Copy Bundle Resource过程中。然后通过一个Shell脚本添加到App Main Bundle中。假设我们这样写 `'DemoLibResource' => [A/1.png, 'A/2.plist']`匹配到了一个`1.png`和`2.plist`，会是以这个Target建立一个Bundle父文件夹。然后这些Bundle父文件夹，拷贝到App Main Bundle根路径下，最后得到这样一个ipa结构。

```  
| Info.plist
| DemoLibResource.bundle
|- 1.png
|- 2.plist
| News
| xxx
```  

优点：

1. 解决了命名冲突问题，由于使用了一级的Key值，作为一个单独的父文件夹隔离，不同的Pods库不太可能出现命名冲突（遵守`库名+Resource`，则库之间不会不出现同样的Key值）。
2. 能利用Xcode本身的优化过程，由于单独构建了一个Target，使用Xcode原生的Copy Bundle Resource过程，PNG图片等会自动享受压缩

缺点：

1. 由于最终资源产物增加了一级Resource Key的父文件夹，如果有先前依赖Main Bundle路径位置的加载代码，需要进行更新。典型的用法如`NSBundle.mainBundle pathForResource:ofType:`取本地Bundle中一个文件路径，这时候需要更新为`[NSBundle bundleWithPath:] pathForResource:ofType:`的代码调用。对于`UIImage imageNamed:`方法，它也支持Bundle，看情况需要更新。

举例子说明，原来使用方式为:

```swift  
// 直接访问路径
NSString *plistPath = [NSBundle.mainBundle pathForResource:@"test" ofType:@"plist"];
// 获取Bundle中的UIImage，只是示例，推荐使用Asset Catalog替代这种裸的图片引用
UIImage *image = [UIImage imageNamed:@"1"];
```  

现在需要更新为：

```swift  
// 路径变化，这步骤可以封装库级别的工具方法，或者宏，Static对象，都行
// 由于采取了Static Library而没有使用use_framework!，因此此时[NSBundle bundleForClass:]和mainBundle是相同的，原因是类其实在mainBundle的二进制中，而不是Framework中。但是为了代码统一，建议都使用bundleForClass:（后面讲）

// NSString *bundlePath = [NSBundle.mainBundle.resourcePath stringByAppendingPathComponent:@"DemoLibResource.bunbdle"]; // 虽然也能Work，为了统一代码（开启use_framework!）用下面的更好
NSString *bundlePath = [[NSBundle bundleForClass:DemoLib.class].resourcePath stringByAppendingPathComponent:@"DemoLibResource.bunbdle"];
NSBundle *bundle = [NSBundle bundleWithPath:bundlePath];
// 直接访问路径
NSString *plistPath = [bundle pathForResource:@"test" ofType:@"plist"];
// 获取Bundle中的UIImage，只是示例，推荐使用Asset Catalog替代这种裸的图片引用
UIImage *image = [UIImage imageNamed:@"1" inBundle:bundle compatibleWithTraitCollection:nil];
```  

总体来说，结合优缺点，大部分的组件库，对于通用资源的引用，应当避免使用`resources`，而转为使用`resource_bundles`声明。能够从源头上避免冲突。改动成本也不算大，封装个库内部的工具方法/宏替换下即可。

Tips：如果在使用`resource_bundles`的情况下，我还想避免Xcode的图片优化策略（如无损的图片等），这时候可以采取将图片放入一个自己建立的Bundle文件夹中，然后`resource_bundles`引入这个Bundle本身，注意路径需要再加一层。

## 使用use_framework!

当使用了use_framework!之后，CocoaPods会对每个Pod单独建立一个动态链接库的Target，每个Pod最后会直接以Framework集成到App中。而资源方面，由于Framework本身就能承载资源，所有的资源都会被拷贝到Framework文件夹中而不再使用单独的脚本处理。

* `resources`

在使用`resources`声明时，同不使用use_framework!相比，改动的点在于这些Pod库资源的路径。此时，这些Pod库资源会被拷贝到Pod库自己的Fraemwork根路径下，而不在App Main Bundle的根路径下。

```  
| Info.plist
| Frameworks
|- DemoLib.framework
|-- 1.png
|-- 2.plist
| News
| xxx
```  

优点：

1. 虽然在不使用use_framework!的情况下，这种声明会造成命名冲突。但是在使用use_framework!的情况下，由于资源本身被拷贝到Framework中，已经能最大程度减少冲突，因此这时候一般不需要考虑名称冲突问题

缺点：

1. 在use_framework!的情况下，能够保证代码一行不改，但是使用use_framework!后就不行了。原因在于此时Bundle资源路径已经发生变化，到Framework自身的文件夹中而不是App Main Bundle中，需要进行更新。这个更新的路径和`resource_bundles`不同，不需要额外拼接一层Key值的名称。直接使用bundleForClass即可，比较简单

```swift  
// 使用bundleforClass替代mainBundle即可
NSBundle *bundle = [NSBundle bundleForClass:DemoLib.class];
// 直接访问路径
NSString *plistPath = [bundle pathForResource:@"test" ofType:@"plist"];
// 获取Bundle中的UIImage，只是示例，推荐使用Asset Catalog替代这种裸的图片引用
UIImage *image = [UIImage imageNamed:@"1" inBundle:bundle compatibleWithTraitCollection:nil];
```  

* `resource_bundles`

在使用`resource_bundles`声明时，同不使用use_framework!相比，改动的点在于对应这些Key生成的Bundle的位置。此时，这些生成的Bundle父文件夹，会放入Pod库自己的Framework的根路径下。而每个Pod库Framework本身，在App Main Bundle的`Frameworks`文件夹下。

```  
| Info.plist
| Frameworks
|- DemoLib.framework
|-- DemoLibResource.bundle
|--- 1.png
|--- 2.plist
| News
| xxx
```  

优点：同上
缺点：同上。但有点区别，在于Bundle的路径变化。此时，`NSBundle bundleForClass:`不再等价于mainBundle了，因此对应代码更新示例里面，一定不能用mainBundle而要用bundleForClass替代。传入的Class是哪一个Pod库的Class，就会取到对应Pod库Framework里面的Bundle文件夹。

```swift  
// 再抄一遍，害怕忘记了，此时不能用mainBundle的resourcePath去拼接
NSString *bundlePath = [[NSBundle bundleForClass:DemoLib.class].resourcePath stringByAppendingPathComponent:@"DemoLibResource.bunbdle"];
NSBundle *bundle = [NSBundle bundleWithPath:bundlePath];
```  

## CocoaPods与Asset Catalog图片资源

前面花了大篇章说了关于CocoaPods处理通用的资源引用的方式，是为了业务库作者能有清晰认识到，在从主工程沉库代码后，需要怎么样更改来处理资源。

现在回到正题说一下Pod库中的Assets Catalog需要怎么样处理以利用App Thinning。Assets Catalog的好处都有啥已经说过了，因此我们需要尽量保证大部分情况下优先使用Assets Catalog而非将图片拷贝至App Bunlde中（虽然Xcode会压缩优化，但是这种方式无论如何都无法利用App Thinning）。

Assets Catalog本身的文件夹`xcassets`一定不会出现在最终的App包中，它在编译时会产生一个二进制产物`Assets.car`，而这个二进制目前只能由UIKit的方法，去读取产生一个UIImage内存对象，其他代码无法直接访问原始的图片文件路径和ImageData。同时，按照官方文档的说明，[UIImage imageNamed:inBundle:compatibleWithTraitCollection:](https://developer.apple.com/documentation/uikit/uiimage/1624154-imagenamed?language=objc) 实际上，会优先去查找指定Bundle（`UIImage imageNamed:`即为mainBundle）的路径下的`Assets.car`文件并展开，然后找不到再去寻找Bundle路径下同名的图片文件。所以，从API使用上来看，一个图片具体是在散落在Bundle根路径下，还是在被编译到Bundle路径下的`Assets.car`中，代码应该是一致的。

值得说明的是，CocoaPods不会自动根据你在Spec中的声明，创建Asset Catalog，你必须通过Xcode手动创建，添加，然后在Spec中引入它。类似这样。

```  
spec.resources = ['A/DemoLib.xcassets']
```  

有了这些知识，我们就结合前面的CocoaPods资源处理策略，以及UIKit的行为，再来回顾上述这些声明的行为，以及我们应该怎么样从代码上去使用。

下面的例子统一都以上面这个示例举例子，假设这个Asset Catalog中含有`1.png`, [`1@2x.png](mailto:%601@2x.png)`,`[1@3x.png](mailto:1@3x.png)`.

### 不使用use_framework!

* `resources`

不同于普通资源那种暴力拷贝的方式，CocoaPods这下没法暴力拷贝这个编译产物的`Assets.car`到根路径了，因为它会直接覆盖掉App本身的编译产物。所以，CocoaPods采取的方案，是合并Asset Catalog。首先会编译得到工程App的`Assets.car`，然后通过便利所有Pod的`resources`引入的`xcassets`，使用atool工具进行多个Asset Catalog合并，最后输出到App Main Bundle根路径下的`Asset.car`里。

```  
| Info.plist
| Assets.car (编译进去了1.png）
| News
| xxx
```  

优点：

1. 继承了普通资源的处理方式，由于采取了Asset Catalog合并，原来主工程代码不需要更改一行可继续使用。相当于库的Assets Catalog资源直接添加到主工程Assets Catalog中

缺点：

1. 一贯的命名冲突问题，由于Asset Catalog还会和主工程以及其他Pod库进行合并，一旦出现了重名的资源，最终编译产物`Assets.car`会根据合并顺序替换掉之前的。因此还是得每个Asset Catalog中资源名也得添加前缀

* `resource_bundles`

类似对于普通资源的处理，如果使用`resource_bundles`，对于每个Key生成的Bundle父文件夹，会把生成的`Assets.car`拷贝到这个Bundle父文件夹中。如果当前Pod库引用了多个xcasset文件，对引用的这几个做合并。

```  
| Info.plist
| DemoLibResource.bundle
|- Assets.car（含有1.png）
| News
| xxx
```  

优点：同普通资源
缺点：同普通资源。代码使用方面，由于之前提到的UIImage API，对于同路径下的`Assets.car`编译产物，和散落的普通图片名，代码使用方式是一致的，因此这里也没有额外的变化。

### 使用use_framework!

* `resources`

在使用use_framework!的情况下，对应编译产物`Assets.car`会被拷贝到Pod库Framework的根路径下，其他的行为类似。

```  
| Info.plist
| Frameworks
|- DemoLib.framework
|-- Assets.car
| News
| xxx
```  

优点：同普通资源
缺点：同普通资源，代码使用方面也同普通资源的情形

* `resource_bundles`

在使用use_framework!的情况下，也会创建Key为名称的父Bundle文件夹，拷贝到Pod库Framework根路径下，然后对应编译产物`Assets.car`放到了这个自动生成Bundle文件夹下，其他行为类似。

```  
| Info.plist
| Frameworks
|- DemoLib.framework
|-- DemoLibResource.bundle
|--- Assets.car
| News
| xxx
```  

优点：同普通资源
缺点：同普通资源，代码使用方面也同普通资源的情形

## 最佳实践和总结

可以看出，CocoaPods，对待普通资源和Asset Catalog都支持，唯一的行为不同的点，在于普通资源如果发生重名，不会进行合并而是直接替换。但是Asset Catalog如果出现多个引用，会进行合并。

虽然表面看起来，我们分析了总共会有 **使用resource还是resource_bundle** ***是否使用use_framework!** ***普通资源还是Asset Catalog**，8种情形。但是实际上从世纪代码使用上，由于Asset Catalog和普通图片API可以统一，同时动态/静态的Bundle位置也可以统一处理，实际上只有两种Case：

### 使用resource_bundle：推荐，避免命名冲突

推荐做法，对于每个需要引入资源的库，以`库名+Resource`为Key（不强制，推荐），然后引入资源，Asset Catalog。代码必须更新，以使用对应的Bundle名来获取。参考上面的代码：

```swift  
NSString *bundlePath = [[NSBundle bundleForClass:DemoLib.class].resourcePath stringByAppendingPathComponent:@"DemoLibResource.bunbdle"];
NSBundle *bundle = [NSBundle bundleWithPath:bundlePath];
```  

### 使用resource：不推荐，因为会导致命名冲突。

除非你能保证分所有资源都已加入前缀，而且目前代码不好更改的情况下，可以保持继续使用主工程的直接访问mainBundle的代码；其他的任何情况，使用`NSBundle bundleForClass:`来获取Bundle，然后加载路径，或者使用`UIImage imageNamed:inBundle:compatibleWithTraitCollection`加载图片。

```swift  
NSBundle *bundle = [NSBundle bundleForClass:DemoLib.class];
```  

对于Pod库开发者，需要尽量使用`resource_bundle`来处理资源，同时，Pod自身代码可能需要更新，以使用正确的方式加载图片或者其他Bundle资源。并且，对于图片资源，如果无特殊用处，建议都建立Asset Catalog以利用App Thinning。