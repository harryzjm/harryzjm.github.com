---  
layout: post  
title: 通用链接（Universal Links）  
category: Foundation  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [小松哥](https://www.jianshu.com/p/734c3eff8feb)__  

#### 什么是Universal Links?  

在iOS9之前，对于从各种从浏览器、Safari中唤醒APP的需求，我们通常只能使用scheme。但是这种方式需要提前判断系统中是否安装了能够响应此scheme的app，并且这种方式在微信中是被禁用了的。  

Universal Links是iOS9推出的一项功能，使你的应用可以通过传统的HTTP链接来启动APP(如果iOS设备上已经安装了你的app，不管在微信里还是在哪里)， 或者打开网页(iOS设备上没有安装你的app)。  

下面简单说下怎么使用Universal Links，具体的可以看[官方的说明文档](https://link.jianshu.com?t=https://developer.apple.com/library/ios/documentation/General/Conceptual/AppSearch/UniversalLinks.html)  

#### 怎么使用Universal Links  

1.先决条件：你必须有一个域名,且这个域名需要支持https。  

2.需要在开发者中心做配置：找到对应的App ID，在Application Services列表里有Associated Domains一条，把它变为Enabled就可以了。  

![](/assets/postAssets/2018/15192698791323.webp)  

配置App ID支持Associated Domains  

3.打开工程配置中的Associated Domains，在其中的Domains中填入你想支持的域名，必须以**applinks:**为前缀。  

![](/assets/postAssets/2018/15192698875448.webp)  

配置项目中的Associated Domains  

4.创建一个内容为json格式的文件，苹果将会在合适的时候，从我们在项目中填入的域名请求这个文件。这个文件名必须为**apple-app-site-association**，没有后缀名，文件内容大概是这样子：  

```  
{  
    "applinks": {  
        "apps": [],  
        "details": [  
            {  
                "appID": "9JA89QQLNQ.com.apple.wwdc",  
                "paths": [ "/wwdc/news/", "/videos/wwdc/2015/*"]  
            },  
            {  
                "appID": "ABCD1234.com.apple.wwdc",  
                "paths": [ "*" ]  
            }  
        ]  
    }  
}  
```  

说明：  

> appID：组成方式是 teamId.yourapp’s bundle identifier。如上面的 9JA89QQLNQ就是teamId。登陆开发者中心，在Account - Membership里面可以找到Team ID。  

> paths：设定你的app支持的路径列表，只有这些指定的路径的链接，才能被app所处理。星号的写法代表了可识别域名下所有链接。  

[这篇博客](https://link.jianshu.com?t=http://www.jackivers.me/blog/2015/9/17/list-of-universal-link-ios-9-apps)里有很多其他公司的例子，可以参考一下。也有可能有的公司的已经不再适用，可以换换其他公司的。  

5.上传该文件到你的域名所对应的根目录或者`.well-known`目录下，这是为了苹果能获取到你上传的文件。上传完后,自己先访问一下,看看是否能够获取到，当你在浏览器中输入这个文件链接后，应该是直接下载apple-app-site-association文件。  

#### 验证  

在iOS设备中的备忘录中输入App能识别的链接，然后直接点击此链接，就会直接跳转到你的app了。或是长按，在出现的弹出菜单中第二项是`在’XXX’中打开`，这也代表着成功：  

![](/assets/postAssets/2018/15192699034652.webp)  

出现菜单  

或是你将要测试的网址在safari中打开，在出现的网页上方下滑，可以看到有`在”XX”应用中打开`：  

![](/assets/postAssets/2018/15192699133580.webp)  

出现菜单  

在微信的网页浏览器中也是可以的，虽然微信屏蔽了所有的scheme方式跳转到其它app，但是Universal Links是由系统直接处理的，微信屏蔽不了，这也就实现了从微信跳转到我们的app。  

苹果为了方便开发者，提供了一个网页来验证我们编写的这个apple-app-site-association是否合法有效，进入[验证网址](https://link.jianshu.com?t=https://search.developer.apple.com/appsearch-validation-tool/)进行验证：  

![](/assets/postAssets/2018/15192699240855.webp)  

验证链接  

#### 进入app后的处理  

现在用户点击某个链接，直接可以进我们的app了，但是我们的目的是要能够获取到用户进来的链接，根据链接来展示给用户相应的内容。  
我们需要在工程里的 AppDelegate 里实现方法  

```  
- (BOOL)application:(UIApplication *)application continueUserActivity:(NSUserActivity *)userActivity restorationHandler:(void (^)(NSArray * _Nullable))restorationHandler  
{  
    if ([userActivity.activityType isEqualToString:NSUserActivityTypeBrowsingWeb])  
    {  
        NSURL *url = userActivity.webpageURL;  
        if (url是我们希望处理的)  
        {  
            //进行我们的处理  
        }  
        else  
        {  
            [[UIApplication sharedApplication] openURL:url];  
        }  
    }  

    return YES;  
}  
```  

#### 注意  

前端开发经常面临跨域问题，必须要求跨域，如果不跨域，就不行。  
只有当前webview的url域名，与跳转目标url域名不一致时，Universal Link 才生效。  

好了先说到这里，如果遇到什么问题可以详细看[官方的说明文档](https://link.jianshu.com?t=https://developer.apple.com/library/ios/documentation/General/Conceptual/AppSearch/UniversalLinks.html)。  

