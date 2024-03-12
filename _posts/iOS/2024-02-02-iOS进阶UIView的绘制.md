---  
layout: post  
title: iOS进阶UIView的绘制  
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [iOS猿_员](https://www.jianshu.com/p/a120d6c64d88)__  

# 前言

如果要研究OpenGL ES相关和 GPU 相关，这篇文章很具有参考的入门价值.

### 理解 UIView 的绘制, UIView 是如何显示到 Screen 上的?

首先要从`Runloop`开始说,iOS 的`MainRunloop` 是一个60fps 的回调,也就是说16.7ms(毫秒)会绘制一次屏幕,这个时间段内要完成:

*   `view`的缓冲区创建
*   `view`内容的绘制(如果重写了 drawRect)

这些 `CPU`的工作.

然后将这个缓冲区交给`GPU`渲染, 这个过程又包含:

*   多个`view`的拼接(compositing)
*   纹理的渲染(Texture)等.

最终现实在屏幕上.因此,如果在16.7ms 内完不成这些操作, eg: CPU做了太多的工作, 或者`view`层次过于多,图片过于大,导致`GPU`压力太大,就会导致"卡"的现象,也就是 **丢帧**,**掉帧**.

苹果官方给出的最佳帧率是:**60fps**(60Hz),也就是一帧不丢, 当然这是理想中的绝佳体验.

### 这个`60fps`该怎么理解呢？

一般来说如果帧率达到 `60+fps`(fps >= 60帧以上,如果帧率fps > 50,人眼就基本感觉不到卡顿了,因此,如果你能让你的 iOS 程序**稳定**保持在`60fps`已经很不错了, 注释,是"稳定"在60fps,而不是, `10fps`,`40fps`,`20fps`这样的跳动,如果帧频不稳就会有卡的感觉,`60fps`真的很难达到, 尤其是在 iPhone 4/4s等 32bit 位机上,不过现在苹果已经全面放弃32位,支持最低64位会好很多.

> fps 代表的是刷新频率,单位赫兹Hz,因为电子工程中考虑到能耗和视觉以及其它方面,60Hz是一个比较理想的刷新频率,所以家用电器也经常会出现60Hz的字样. 视频中帧率FPS >= 25 才不会人眼察觉有卡顿,因为视频中视频模糊视频中的i p b帧能够给予前后帧一些需要的像素信息方便GPU的离屏渲染,GPU的索引可以节省很多性能.

总的来说, UIView从绘制到Render的过程有如下几步：

*   每一个`UIView`都有一个`layer`
*   每一个`layer`都有个`content`,这个`content`指向的是一块缓存,叫做**`backing store`**.

`UIView`的绘制和渲染是两个过程:

*   当`UIView`被绘制时,CPU执行`drawRect`，通过`context`将数据写入**`backing store`**
    
*   当**`backing store`**写完后，通过render server交给GPU去渲染，将backing store中的bitmap数据显示在屏幕上.
    

上面提到的从`CPU`到`GPU`的过程可用下图表示:

![](/assets/postAssets/2023/17068682283588.jpg)

下面具体来讨论下这个过程

*   CPU bound:

假设我们创建一个 UILabel

```objectivec
UILabel* label = [[UILabel alloc]initWithFrame:CGRectMake(10, 50, 300, 14)];
label.backgroundColor = [UIColor whiteColor];
label.font = [UIFont systemFontOfSize:14.0f];
label.text = @"test";
[self.view addSubview:label];
```

这个时候不会发生任何操作, 由于 UILabel 重写了`drawRect`方法,因此,这个 `View`会被 `marked as "dirty"`:

类似这个样子:

![](/assets/postAssets/2023/17068682519976.jpg)


然后一个新的`Runloop`到来，上面说道在这个`Runloop`中需要将界面渲染上去，对于`UIKit`的渲染，Apple用的是它的`Core Animation`。 做法是在Runloop开始的时候调用：

```json
[CATransaction begin]
```

在`Runloop`结束的时候调用

```json
[CATransaction commit]
```

在`begin`和`commit`之间做的事情是将`view`增加到`view hierarchy`中，这个时候也不会发生任何绘制的操作。 当`[CATransaction commit]`执行完后，`CPU`开始绘制这个`view`:


![](/assets/postAssets/2023/17068712537764.jpg)

首先`CPU`会为`layer`分配一块内存用来绘制`bitmap`，叫做**`backing store`**  
创建指向这块`bitmap`缓冲区的指针，叫做`CGContextRef`  
通过`Core Graphic`的`api`，也叫`Quartz2D`，绘制`bitmap`  
将`layer`的`content`指向生成的`bitmap`  
清空`dirty flag`标记  
这样`CPU`的绘制基本上就完成了.  
通过`time profiler`可以完整的看到个过程：

```css
Running Time Self Symbol Name
2.0ms 1.2% 0.0 +[CATransaction flush]
2.0ms 1.2% 0.0 CA::Transaction::commit()
2.0ms 1.2% 0.0 CA::Context::commit_transaction(CA::Transaction*)
1.0ms 0.6% 0.0 CA::Layer::layout_and_display_if_needed(CA::Transaction*)
1.0ms 0.6% 0.0 CA::Layer::display_if_needed(CA::Transaction*)
1.0ms 0.6% 0.0 -[CALayer display]
1.0ms 0.6% 0.0 CA::Layer::display()
1.0ms 0.6% 0.0 -[CALayer _display]
1.0ms 0.6% 0.0 CA::Layer::display_()
1.0ms 0.6% 0.0 CABackingStoreUpdate_
1.0ms 0.6% 0.0 backing_callback(CGContext*, void*)
1.0ms 0.6% 0.0 -[CALayer drawInContext:]
1.0ms 0.6% 0.0 -[UIView(CALayerDelegate) drawLayer:inContext:]
1.0ms 0.6% 0.0 -[UILabel drawRect:]
1.0ms 0.6% 0.0 -[UILabel drawTextInRect:]
```

假如某个时刻修改了`label`的`text`:

```bash
label.text = @"hello world";
```

由于内容变了,`layer`的`content`的`bitmap`的尺寸也要变化，因此这个时候当新的`Runloop`到来时，`CPU`要为`layer`重新创建一个`backing store`，重新绘制`bitmap`.  
`CPU`这一块最耗时的地方往往在`Core Graphic`的绘制上，关于`Core Graphic`的性能优化是另一个话题了，又会牵扯到很多东西，就不在这里讨论了.

GPU bound：

`CPU`完成了它的任务：将`view`变成了`bitmap`，然后就是`GPU`的工作了，`GPU`处理的单位是`Texture`.  
基本上我们控制`GPU`都是通过`OpenGL`来完成的，但是从`bitmap`到`Texture`之间需要一座桥梁，`Core Animation`正好充当了这个角色：  
`Core Animation`对`OpenGL`的`api`有一层封装，当我们要渲染的`layer`已经有了`bitmap content`的时候，这个`content`一般来说是一个`CGImageRef`，`CoreAnimation`会创建一个`OpenGL`的`Texture`并将`CGImageRef（bitmap）`和这个`Texture`绑定，通过`TextureID`来标识。  
这个对应关系建立起来之后，剩下的任务就是`GPU`如何将`Texture`渲染到屏幕上了。 `GPU`大致的工作模式如下：

![](/assets/postAssets/2023/17068712715489.jpg)


整个过程也就是一件事：

`CPU`将准备好的`bitmap`放到`RAM`里，`GPU`去搬这快内存到`VRAM`中处理。 而这个过程`GPU`所能承受的极限大概在16.7ms完成一帧的处理，所以最开始提到的60fps其实就是GPU能处理的最高频率.  
因此，`GPU`的挑战有两个：

*   将数据从`RAM`搬到`VRAM`中
*   将`Texture`渲染到屏幕上

这两个中瓶颈基本在第二点上。渲染`Texture`基本要处理这么几个问题：

*   Compositing:

`Compositing`是指将多个纹理拼到一起的过程，对应`UIKit`，是指处理多个`view`合到一起的情况，如:

```csharp
[self.view addsubview : subview]。
```

如果`view`之间没有叠加，那么`GPU`只需要做普通渲染即可.  
如果多个`view`之间有叠加部分，`GPU`需要做`blending`.

加入两个`view`大小相同，一个叠加在另一个上面，那么计算公式如下：

`R` = `S`+`D`\*(`1`\-`Sa`)

> `R`: 为最终的像素值  
> `S`: 代表 上面的Texture（Top Texture）  
> `D`: 代表下面的Texture(lower Texture)

其中`S`,`D`都已经`pre-multiplied`各自的`alpha`值。  
`Sa`代表`Texture`的`alpha`值。

假如`Top Texture`（上层`view`）的`alpha`值为`1`，即不透明。那么它会遮住下层的`Texture`.  
即,`R` = `S`。是合理的。

假如`Top Texture`（上层`view`）的`alpha`值为`0.5`，  
`S`为`(1,0,0)`，乘以`alpha`后为`(0.5,0,0）`。  
`D`为`(0，0，1)`。  
得到的`R`为`（0.5，0，0.5）`。

基本上每个像素点都需要这么计算一次。

因此，`view`的层级很复杂，或者`view`都是半透明的（`alpha`值不为`1`）都会带来`GPU`额外的计算工作。

*   Size

这个问题，主要是处理`image`带来的，假如内存里有一张`400x400`的图片，要放到`100x100`的`imageview`里，如果不做任何处理，直接丢进去，问题就大了，这意味着，`GPU`需要对大图进行缩放到小的区域显示，需要做像素点的`sampling`，这种`smapling`的代价很高，又需要兼顾`pixel alignment`。 计算量会飙升。

*   Offscreen Rendering And Mask

如果我们对`layer`做这样的操作：

```objectivec
label.layer.cornerRadius = 5.0f;
label.layer.masksToBounds = YES;
```

会产生`offscreen rendering`,它带来的最大的问题是，当渲染这样的`layer`的时候，需要额外开辟内存，绘制好`radius，mask`，然后再将绘制好的`bitmap`重新赋值给`layer`。  
因此继续性能的考虑，`Quartz`提供了优化的`api`：

```objectivec
label.layer.cornerRadius = 5.0f;
label.layer.masksToBounds = YES;
label.layer.shouldRasterize = YES;
label.layer.rasterizationScale = label.layer.contentsScale;
```

简单的说，这是一种`cache`机制。  
同样`GPU`的性能也可以通过`instrument`去衡量：

![](/assets/postAssets/2023/17068712886640.jpg)


红色代表`GPU`需要做额外的工作来渲染`View`，绿色代表`GPU`无需做额外的工作来处理`bitmap`。

全文完

# 文末推荐

*   **更多：[iOS面试题大全-（附答案）](https://www.jianshu.com/p/e709fde38de3)**
*   **更多：《BAT面试答案文集.PDF》，获取可加iOS技术交流圈：[937 194 184](https://links.jianshu.com/go?to=https%3A%2F%2Fjq.qq.com%2F%3F_wv%3D1027%26k%3D5PARXCI)。**

收录：[原文地址](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.sunyazhou.com%2F2017%2F10%2F16%2F20171016UIViewRendering%2F)

  
  
作者：iOS猿\_员  
链接：https://www.jianshu.com/p/a120d6c64d88  
来源：简书  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。