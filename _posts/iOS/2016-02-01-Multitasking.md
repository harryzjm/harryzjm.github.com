---  
layout: post  
title: Multitasking  
category: iOS  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__Posted by [chengway](http://chengway.in//)__  

iOS 9 苹果为 iPad 带来了多任务，允许同时在一个界面上运行两个程序，本章来学习下如何在现有 App 上添加多任务环境  

现在 Multitasking 有三种模式：  

* **Slide Over 多任务模式**：打开一个 App，从 iPad Air 边缘向中心滑动，会出现一个窄边框，此时刚才打开的 App 主界面会变暗（蒙上一层灰色 mask），从边缘拉出来的空间内会出现一个 App 列表（仅限适配过的 App），你可以选择打开某个应用，此时该应用会在边缘空间显示。  
* **Split View 多任务模式**：当你继续往中心拉，屏幕会被分为两部分，左右两边的 App 会同时显示在屏幕上，也不会有任何一个 App 处于 mask 之下。  
* **Picture in Picture 模式**：也就是所谓的画中画模式，一般在播放视频时使用  

> Split View 模式仅支持 iPad Air 2，Picture in Picture 和 Slide Over 则支持 iPad Air, iPad Air 2, iPad Mini 2, 和 iPad Mini 3。  
因为 iPad Air 2 是 2 G 内存，Split View 也是最占内存的  

### Preparing your app for multitasking  

如果你的 App 是按照如下方式开发的，那么恭喜你。只要你用 iOS 9 的 SDK 重新编译下就自动支持 multitasking 了  

* 使用 size classes, adaptive layout 开发的 universal app  
* 用 SDK 9.X 编译过  
* 支持所有方向  
* 使用 launch storyboard 或 XIB  

**注意**：做到上面这几点也仅仅是支持 **multitasking** 而已，并不意味完美适配。  

### Orientation and size changes  

下面看一下本章的 Travelog （该 App 已经做到上述 4 点）在 multitasking 下的表现  

首先是单个 App 全屏运行的表现（横屏和竖屏）：  

![][1]  

**Split View 多任务模式**下竖屏的表现：  

![][2]  

**Split View 多任务模式**下横屏的表现：  

![][3]  

master view 的内容太拥挤了，并且右边的列表栏并未显示任何内容  

App 在多任务模式下，部分情况下 bounds 发生变化，**也可看做是触发了 size class 的变化**，下面是在各种多任务模式下 size class 的具体情形：  

![][4]  

> (R 代表 Regular 而 C 代表 Compact)  

幸好 UIKit 提供了一些更新 layout 的契机，我们可以在下面的方法中更新 layout：  

1. `willTransitionToTraitCollection(_:,withTransitionCoordinator:)`  
2. `viewWillTransitionToSize(_:,withTransitionCoordinator:)`  
3. `traitCollectionDidChange(_:):`  

回顾下 **Split View 多任务模式** 下竖屏的表现，再对比下上图 _33% split_ 的情形，App 的 size class 仍然为 Regular，但整体 width 变窄了，所以 master view 就会略显拥挤  

修正办法也很简单，先设置一个 `maximumPrimaryColumnWidth` 属性值  

    func updateMaximumPrimaryColumnWidthBasedOnSize(size: CGSize) {  
    // 如果是小于屏幕宽度或竖屏状况，就设置一个较小的值  
      if size.width < UIScreen.mainScreen().bounds.width  
        || size.width < size.height {  
        maximumPrimaryColumnWidth = 170.0  
      } else {  
        maximumPrimaryColumnWidth =  
          UISplitViewControllerAutomaticDimension  
      }  
    }  

在第一次载入时更新：  

    override func viewDidLoad() {  
      super.viewDidLoad()  
      updateMaximumPrimaryColumnWidthBasedOnSize(view.bounds.size)  
    }  

在 size 发生变化时更新  

    override func viewWillTransitionToSize(size: CGSize,  
      withTransitionCoordinator coordinator:  
      UIViewControllerTransitionCoordinator) {  
      super.viewWillTransitionToSize(size,  
        withTransitionCoordinator: coordinator)  
      updateMaximumPrimaryColumnWidthBasedOnSize(size)  
    }  

再次运行，好像变得更糟了  

![][5]  

似乎 table view cell 没有随 size 变化而自适应，cell 是自定义的 view，我们打开看一下（`LogCell.swift`）  

    static let widthThreshold: CGFloat = 1024.0  

    override func layoutSubviews() {  
        super.layoutSubviews()  
        let isTooNarrow = UIScreen.mainScreen().bounds.width < LogCell.widthThreshold  
        compactView.hidden = !isTooNarrow  
        regularView.hidden = isTooNarrow  
      }  

发现问题所在了吗？UIScreen 的尺寸一般是固定的，并不会响应 App size 的变化。因此我们用 UIWindow.bounds 来替代  

    static let widthThreshold: CGFloat = 180.0  

    override func layoutSubviews() {  
      super.layoutSubviews()  
      let isTooNarrow = bounds.width <= LogCell.widthThreshold  
      // some code ...  
    }  

现在就好很多  

![][6]  

> UIWindow.bounds 一直会响应 size 的变化，并且他的原点始终为 (0, 0)。在 iOS 9 你可以直接创建 UIWindow 的实例，且不需要通过 `let window = UIWindow()` 来传递一个 frame，系统会自动提供一个和应用 frame 相同的 frame  

### Adaptive presentation  

点击左上角的 **Photo Library** bar button  

![][7]  

此时将两个 App 之间的分割线继续向左拖动  

![][8]  

到了 50% 模式下，popover 没有任何过渡动作自动变成了模态显示，因为在此模式显示下，App 的 size class 由 regular 变成了 compact。但这并不是你想要的，你仅仅想让你的 App 在占屏幕 33% 的情形下才用模态展示照片库（in Slide Over 或 in 33% part）  

iOS 8 介绍了 `UIPopoverPresentationController` 管理 popover 显示的内容，你会通过 `UIModalPresentationPopover` 提供的样式来展示。  

UIPopoverPresentationControllerDelegate 提供了回调注射方法，你可以提供自定义的样式来展示 popover：  

    extension LogsViewController:  
      UIPopoverPresentationControllerDelegate {  

      func adaptivePresentationStyleForPresentationController(  
        controller: UIPresentationController,  
        traitCollection: UITraitCollection)  
        -> UIModalPresentationStyle {  
        //1 检查是否运行在 iPad 上  
        guard traitCollection.userInterfaceIdiom == .Pad else {  
          return .FullScreen  
        }  
       //2 检查是否大于 320 即 33%  
        if splitViewController?.view.bounds.width > 320 {  
          return .None  
        } else {  
          return .FullScreen  
        }  
      }  
    }  

> 只要大于 33%，一律以正常 popover 展示，只有小于或等于 33%，才会全屏模态展示  

最后修改 `presentImagePickerControllerWithSourceType(_:)` 找机会添加 `popoverPresentationController` 的 `delete` 为 `self`  

    func presentImagePickerControllerWithSourceType(sourceType:  
      UIImagePickerControllerSourceType) {  
      // some code...  
      if sourceType ==  
        UIImagePickerControllerSourceType.PhotoLibrary {  
        let presenter = controller.popoverPresentationController  
        // some code...  
        presenter?.delegate = self  
    }  
      // some code...  
    }  

最终运行，一切 OK  

![][9]  

### Other considerations  

除此之外，还应该考虑的有：  

* Keyboard：要考虑多任务模式下，键盘出来后的 layout 设置  
* Designs：设计主要考虑下面几点  
    * Be flexible 考虑在多任务模式下各种 size class 下的表现  
    * Use Auto Layout：使用 Auto Layout  
    * Use size classes：使用 Size Class 适应各种布局  
* Resources：因为多任务的引用，所以最大的情况下，iPad 在 Split View 多任务模式下可以有三个 App 在一个屏幕上同时运行（第一个 App，第二个 App 和画中画 App），因此你需要思考在多任务模式下尽量缩减 App 不必要的内存开销。  
* * *  

-EOF-  

[1]: /assets/postAssets/2016/61b207a9gw1eytpsbr92rj20m80astae.webp  
[2]: /assets/postAssets/2016/61b207a9jw1eytpybyjasj20d40hh0u3.webp  
[3]: /assets/postAssets/2016/61b207a9gw1eytq2e245fj20i90dpmz3.webp  
[4]: /assets/postAssets/2016/61b207a9jw1eytqc3ha83j20q90axdgu.webp  
[5]: /assets/postAssets/2016/61b207a9jw1eytqv187ekj20ot0bztaf.webp  
[6]: /assets/postAssets/2016/61b207a9jw1eytraubj8bj20oq0bx0v0.webp  
[7]: /assets/postAssets/2016/61b207a9jw1eytrcxxaatj20p10irwgi.webp  
[8]: /assets/postAssets/2016/61b207a9jw1eytrei2vg2j20qw0j6dhp.webp  
[9]: /assets/postAssets/2016/61b207a9jw1eytrxr6olij20os09babh.webp  

