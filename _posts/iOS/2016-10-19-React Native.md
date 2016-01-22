---  
layout: post
title: React Native
category: iOS
tags: Swift Define
keywords: Jekyll,Github
description: 
---  


__Posted by [talisk](http://blog.talisk.cn/blog/2016/08/13/RN-Learning-path-for-iOS-developer/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io/)__  


## 名词解释

首先列举几个关键词：

* React：近几年Web前端领域非常火热的一个开发框架React.JS，其核心思想是将视图组件化，通过更新组件的state来渲染出组件。
* Native：这个词从字面理解就够了，就是指原生的。前几年有个非常火热的跨平台开发框架PhoneGap（现称Cordova），那就不是原生的开发方式。原生就要使用对应平台的特定语言和框架进行开发，比如使用Objective-C或Swift开发的iOS应用。
* React Native：结合了这两个词，我们可以简单地得到结论：使用React框架进行原生方式的开发。

## 实现原理

我们都知道在iOS平台上，苹果提供了一个JavaScriptCore的framework，可以进行JavaScript语言的解析，React Native通过多次封装定义，最终实现了在JavaScript语言中调用Objective-C的类和方法。具体的原理我们现在还不必深究，后文的学习路线中会有提到。

所以既然是调用Objective-C的类和方法，性能上当然是不差的（但也不完美），所以这也是React Native相比其他跨平台开发方式的一大优势。

## 评价

* 跨平台：目前React Native官方已经支持iOS、Android两个平台的移动设备，民间也有一些大牛在做macOS、tvOS，甚至UWP平台的适配。但由于不同平台特性不同，并不能一份代码在所有平台上直接运行，React Native的思想是「Learn once, write anywhere」，我们需要针对不同平台的特性写出不同的代码，尽量保持组件的高可复用性。
* 性能：官方宣称性能堪比Native，实际使用中我们会发现几个问题，比如复杂视图渲染出View层级过多、ListView（等同于iOS上的UITableView）无重用机制、有些组件存在内存泄露。这就会导致在部分低端Android机型上的性能过差，复杂的、大型的应用会有明显性能问题。
* 热更新：由于App Store应用商店发版迭代效率问题，热更新成为了iOS平台非常渴求的功能，可喜的是React Native的热更新能力非常好，通过将JavaScript代码部署到服务器中，运行过程中即可重新reload整个界面。
* 学习成本：对于iOS开发者来讲，要了解相当数量的Web前端开发知识才可以进行开发，对于Web前端开发者来讲，对于原生性能调优则需要原生开发知识和经验，所以说学习成本略高。
* 开发效率：Android和iOS平台可复用很多组件，仅部分代码需要各自平台分别维护，所以比开发两个平台原生应用效率要高得多。加上本身可动态渲染的能力，不用重新编译，Command⌘+R即可重新渲染界面，开发效率更是惊人地快。


## 开发环境配置

你的电脑若未安装Homebrew、Node.js、WatchMan等工具，请参照：

* [配置React Native的开发环境 - CSDN](http://blog.csdn.net/github_26672553/article/details/52159868)

若已安装Homebrew、Node.js、WatchMan，请直接：

* [搭建开发环境 - react native 中文网](http://reactnative.cn/docs/0.30/getting-started.html)

对于IDE/Editor的选择，目前可以有Sublime Text、VSCode、WebStorm、Atom+Nuclide、Deco选择。我个人比较推荐的是VSCode和WebStorm。以下提供两篇关于IDE的设置。

* WebStorm - [WebStorm开发工具设置React Native智能提示 - CSDN](http://blog.csdn.net/xiangzhihong8/article/details/52224527)
* VSCode - [VSCode IDE超强开发插件介绍 - 江清清的技术专栏](http://www.lcode.org/vscode-react-native-tools/)

## JavaScript

首先是最基础的JavaScript教程，快速过一遍即可。

* [JavaScript 高级教程 - W3School](http://www.w3school.com.cn/js/index_pro.asp)
* [不再彷徨：完全弄懂JavaScript中的this（译文总结） - Segmentfault](https://segmentfault.com/a/1190000006076637)

### ES6

ES6也称ES2015，是JavaScipt语言的较新的一种标准，在React Native开发时，我们建议使用这种标准。

* [ECMAScript 2015 简易教程 - 颜海镜](http://yanhaijing.com/javascript/2015/09/11/learn-es2015/)
* [ECMAScript 6 入门 - 阮一峰](http://es6.ruanyifeng.com/)
* [关于Promise：你可能不知道的6件事 - dwqs/blog](https://github.com/dwqs/blog/issues/1)

### 语法规范

JavaScript本身变化很快，这份由Airbnb维护的语法规范是使用较为广泛、全面的，很有参考性。

* [Airbnb React/JSX Style Guide](https://github.com/airbnb/javascript/tree/master/react)

## React Native

### 快速入门

* [快速入门实例 - react native 中文网](http://reactnative.cn/docs/0.31/sample-application-movies.html)

由于会有一些开源项目和开源组件使用ES5标准进行开发，所以应该看得懂ES5代码。

* [React/React Native 的ES5 ES6写法对照表 - react native 中文网](http://bbs.reactnative.cn/topic/15/react-react-native-%E7%9A%84es5-es6%E5%86%99%E6%B3%95%E5%AF%B9%E7%85%A7%E8%A1%A8)

### 布局

* [布局 FlexBox布局 - 简书](http://www.jianshu.com/p/31248003f375)

### 组件

* [React-Native从入门到深入–组件生命周期 - 简书](http://www.jianshu.com/p/78ce267658de)
* [React Native 的 Navigator 组件使用方式 - Mystra](http://www.wangchenlong.org/2016/04/19/1604/191-rn-navigator/)
* [React-Native组件用法详解之ListView - 简书](http://www.jianshu.com/p/1293bb8ac969)
* 更多组件学习请参考：[React Native专题 - 江清清的技术专栏](http://www.lcode.org/react-native/)

### React with Redux

* [Redux 简明教程 - GitHub](https://github.com/kenberkeley/redux-simple-tutorial)
* [Redux 状态管理方法与实例 - Segmentfault](https://segmentfault.com/a/1190000005933397)
* [【译】Redux和命令模式 - Jimmylv](http://blog.jimmylv.info/2016-04-19-Redux-and-The-Command-Pattern/)
* [Redux 中文文档 - Redux](http://cn.redux.js.org/)
* [React + Redux 组件化方案 - IMWeb](http://imweb.io/topic/57c531bc6227a4f55a8872c2)
* [React-Native with Redux - Lifecycle](http://richardcao.me/2016/01/12/React-Native-With-Redux/)

### 热更新

* [CodePush 热更新流程（iOS） - talisk’s Wiki](http://wiki.talisk.cn/ReactNative/CodePush.html)
* [React Native热更新部署/热更新-CodePush最新集成总结 - 简书](http://www.jianshu.com/p/9e3b4a133bcc)

### 原理

* [React Native 通信机制详解 - bang’s blog](http://blog.cnbang.net/tech/2698/)

## 推荐资源

* [awesome-react-native - GitHub](https://github.com/jondot/awesome-react-native)
* [React Native 中文网](http://reactnative.cn/)
* [江清清的技术专栏](http://www.lcode.org/)

