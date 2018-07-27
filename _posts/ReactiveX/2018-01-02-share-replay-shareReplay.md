---  
layout: post  
title: share & replay & shareReplay  
category: ReactiveX  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__[Posted by AloneMonkey](http://www.alonemonkey.com/2017/04/02/rxswift-part-eleven/)__  

__[Posted by Andy Chou](https://medium.com/@_achou/rxswift-share-vs-replay-vs-sharereplay-bea99ac42168)__  

### 问题  
每次订阅都会导致`observable`重新执行链式调用。  
如下:  

```swift  
let results = query.rx.text  
    .flatMapLatest { query in  
        networkRequestAPI(query)  
    }  
results.subscribe(...)   // a network request  
results.subscribe(...)   // another network request  
```  

### 解决方案如下  
[![image](/assets/postAssets/2018/script_1491368007455.webp)  

1 表示重播最多`bufferSize`个事件  
2 表示当订阅者的引用计数大于0时，重播一个事件  
**共享订阅者:**多个订阅者订共享一个订阅者对象  
**可连接:**可连接序列只有调用`connect`后才会开始发射值，可以等多个订阅者订阅后再连接。  
**引用计数:**返回的`observable`记录了订阅者的数量，当订阅者数量从0变成1，订阅源序列，当订阅者数量从1变成0，  取消订阅并重置源序列。  
每次订阅者数量从0变成1源序列将会重新被订阅。  
**重播事件:**重播已经发射的事件给订阅者。  
`replay(bufferSize)`和`shareReplay(bufferSize)`最多重播`bufferSize`个，而`shareReplayLatestWhileConnected`最多一个，当订阅者的引用计数变成0，`buffer`会被清空，所以引用计数从0变成1，订阅者不会受到重播事件。  
### publish  
以下例子使用`interval`模拟用户输入文本，并进行搜索:  

```swift  
var results = Observable.interval(1, scheduler: MainScheduler.instance)  
            .map{ "\($0)" }  
            .flatMapLatest{ query in  
                self.request(query)  
```  

然后去订阅结果:  
`publish`原来讲到过，只有`connect`之后才会发射值。  

```swift  
func publish(){  
    let results = self.results.publish()  
    results.subscribe{  
            print("订阅者 one: \($0)")  
        }.disposed(by: disposeBag)  
    results.subscribe{  
            print("订阅者 two: \($0)")  
        }.disposed(by: disposeBag)  

    _ = results.connect()  
    delay(4){  
        print("three 订阅")  
        results.subscribe{  
            print("订阅者 three: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
订阅者 two: next(3 请求成功!)  
three 订阅                        //没有重播事件  
搜索 4  发送网络请求  
订阅者 one: next(4 请求成功!)  
订阅者 two: next(4 请求成功!)  
订阅者 three: next(4 请求成功!)  
```  

### replayAll  
重播所有事件:  

```swift  
func replayAll(){  
    let results = self.results.replayAll()  
    results.subscribe{  
        print("订阅者 one: \($0)")  
        }.disposed(by: disposeBag)  
    results.subscribe{  
        print("订阅者 two: \($0)")  
        }.disposed(by: disposeBag)  
    _ = results.connect()  
    delay(4){  
        print("three 订阅")  
        results.subscribe{  
            print("订阅者 three: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
订阅者 two: next(3 请求成功!)  
three 订阅  
订阅者 three: next(0 请求成功!)     //订阅后，受到重播的所有事件  
订阅者 three: next(1 请求成功!)  
订阅者 three: next(2 请求成功!)  
订阅者 three: next(3 请求成功!)  
搜索 4  发送网络请求  
订阅者 one: next(4 请求成功!)  
订阅者 two: next(4 请求成功!)  
订阅者 three: next(4 请求成功!)  
```  

### replay  
`replay(bufferSize)`重播指定个数的事件:  

```swift  
func replay(){  
    let results = self.results.replay(2)  
    results.subscribe{  
        print("订阅者 one: \($0)")  
        }.disposed(by: disposeBag)  
    results.subscribe{  
        print("订阅者 two: \($0)")  
        }.disposed(by: disposeBag)  
    _ = results.connect()  
    delay(4){  
        print("three 订阅")  
        results.subscribe{  
            print("订阅者 three: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
订阅者 two: next(3 请求成功!)  
three 订阅                        //重播最后2个事件  
订阅者 three: next(2 请求成功!)  
订阅者 three: next(3 请求成功!)  
搜索 4  发送网络请求  
订阅者 one: next(4 请求成功!)  
订阅者 two: next(4 请求成功!)  
订阅者 three: next(4 请求成功!)  
```  

### share  
订阅者从1变成0重置序列:  

```swift  
func share(){  
    let results = self.results.share()  
    let sub = results.subscribe{  
        print("订阅者 one: \($0)")  
    }  
    delay(4){  
        //订阅者从1变成0  
        //可被观察序列重新发射  
        print("订阅者 one被销毁")  
        sub.dispose()  
        results.subscribe{  
            print("订阅者 two: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
订阅者 one被销毁  
搜索 0  发送网络请求                //从0开始重新发射  
订阅者 two: next(0 请求成功!)  
```  

### shareReplay(bufferSize)  
在`share`的基础重播`bufferSize`个值。  

```swift  
func shareReplay(){  
    let results = self.results.shareReplay(2)  
    let sub1 = results.subscribe{  
        print("订阅者 one: \($0)")  
    }  
    let sub2 = results.subscribe{  
        print("订阅者 two: \($0)")  
    }  
    delay(4){  
        sub1.dispose()  
        sub2.dispose()  
        print("three 订阅")  
        results.subscribe{  
            print("订阅者 three: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
订阅者 two: next(3 请求成功!)  
three 订阅  
订阅者 three: next(2 请求成功!)         //虽然订阅者都被销毁，但是仍收到最后两个值  
订阅者 three: next(3 请求成功!)  
搜索 0  发送网络请求  
订阅者 three: next(0 请求成功!)  
```  

### shareReplayLatestWhileConnected  
订阅者从1变成0，缓存区被清空:  

```swift  
func shareReplayLatestWhileConnected(){  
    let results = self.results.shareReplayLatestWhileConnected() // test  shareReplay(1)  
    let sub = results.subscribe{  
        print("订阅者 one: \($0)")  
    }  
    delay(4){  
        sub.dispose()  
        //订阅者从1变成0， 缓存的一个值被清掉了，所以不会收到最后一个值  
        print("two 订阅")  
        results.subscribe{  
            print("订阅者 two: \($0)")  
        }.disposed(by: self.disposeBag)  
    }  
}  
output:  
搜索 3  发送网络请求  
订阅者 one: next(3 请求成功!)  
two 订阅  
搜索 0  发送网络请求  
订阅者 two: next(0 请求成功!)  
搜索 1  发送网络请求  
订阅者 two: next(1 请求成功!)  
```  

试试改成`shareReplay(1)`，或者不销毁`sub`。  
### 总结  
可以结合上面的例子，在实际运用中选择合适的接口。  
代码见github:  
[RxSwiftShareOrReplay](https://github.com/AloneMonkey/RxSwiftStudy)  

