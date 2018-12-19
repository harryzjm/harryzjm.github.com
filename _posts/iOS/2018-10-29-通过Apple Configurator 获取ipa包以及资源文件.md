---  
layout: post  
title: 通过Apple Configurator 获取ipa包以及资源文件 
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [Anchoriter](https://www.jianshu.com/p/fdb50d303ad6)__  


### 1. App Store下载Apple Configurator 2。
### 2. 然后把iphone连接上Mac，点击Apple Configurator 2 菜单中->账户->登陆（用连接设备的Apple ID）

![](/assets/postAssets/2018/15407924464180.webp)

### 3. 所有设备->选中当前iPhone->添加->应用，找到您想要ipa的那个应用->添加

![](/assets/postAssets/2018/15407924786014.webp)

![](/assets/postAssets/2018/15407925129379.webp)

### 4. 因为你手机中已经存在了当前应用，所以会提示，该应用已经存在， 是否需要替换？
    此时，不要点任何按钮！不要点任何按钮！不要点任何按钮！
  
![](/assets/postAssets/2018/15407925219827.webp)

### 5. 不要操作Apple Configurator 2，让它保持上图的状态，然后打开Finder前往文件夹，或者直接快捷键`command+shift+G`
    并输入下面路径
    `~/Library/Group Containers/K36BKF7T3D.group.com.apple.configurator/Library/Caches/Assets/TemporaryItems/MobileApps/`

点击前往，打开ipa包所在文件。将ipa文件copy出来。

这时候别忘了点击Apple Configurator 2窗口中的停止，你会发现刚才目录下的文件也消失了

拿到ipa文件后，你可以将后缀`.ipa`改为`.zip`,然后解压

就可以看到Payload下的包，显示包内容可以看到部分APP的资源以及Assets.car。

如果你要解压Assets.car， 可以使用github上的工具[https://github.com/pcjbird/AssetsExtractor](https://link.jianshu.com/?t=https%3A%2F%2Fgithub.com%2Fpcjbird%2FAssetsExtractor)

最后，提取出来的资源文件，大家要注意版权，仅供参考，不要直接拿来商业使用。

