---  
layout: post  
title: Publish & Connect & RefCount & Share  
category: ReactiveX  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

## .publish().connect()  
![](/assets/postAssets/2017/15014813930719.webp) 

```swift  
print("Starting at 0 seconds")  
let signal = Observable<Int>.interval(1, scheduler: MainScheduler.instance)  
            .publish().connect()  

let subscription1 = signal.subscribe(onNext: {  
    lError("Next: \($0)")  
})  

DispatchQueue.after(3) {  
    lError("Disposing at 3 seconds")  
    subscription1.dispose()  
}  

DispatchQueue.after(6) {  
    lError("Subscribing again at 6 seconds")  
    signal.subscribe(onNext: {  
        lError("Next: \($0)")  
    })  
}  

// Starting at 0 seconds  
// 11:08:33~$>  Next: 0 
// 11:08:34~$>  Next: 1 
// 11:08:35~$>  Next: 2 
// 11:08:35~$>  Disposing at 3 seconds 
// 11:08:38~$>  Subscribing again at 6 seconds 
// 11:08:39~$>  Next: 6 
// 11:08:40~$>  Next: 7 
```  
类似热信号  
.connect()之后变开始发送 不受subscription影响  

## .publish().refCount() / share()  
![](/assets/postAssets/2017/15014813513821.webp)  

```swift  
print("Starting at 0 seconds")  
let signal = Observable<Int>.interval(1, scheduler: MainScheduler.instance)  
    .publish().refCount()  

let subscription1 = signal.subscribe(onNext: {  
    lError("Next: \($0)")  
})  

// signal.subscribe(onNext: {  
//     lError("---------- \($0)")  
// }).disposed(by: bag)  

DispatchQueue.after(3) {  
    lError("Disposing at 3 seconds")  
    subscription1.dispose()  
}  

DispatchQueue.after(6) {  
    lError("Subscribing again at 6 seconds")  
    signal.subscribe(onNext: {  
        lError("Next: \($0)")  
    })  
}  
```  

有注释:  
```swift  
// Starting at 0 seconds  
// 11:15:26~$>  Next: 0 
// 11:15:27~$>  Next: 1 
// 11:15:28~$>  Next: 2 
// 11:15:28~$>  Disposing at 3 seconds 
// 11:15:32~$>  Subscribing again at 6 seconds 
// 11:15:33~$>  Next: 0 
// 11:15:34~$>  Next: 1 
// 11:15:35~$>  Next: 2 
```  

取消注释:  
```swift  
// Starting at 0 seconds  
// 13:48:49~$>  Next: 0 
// 13:48:49~$>  ---------- 0 
// 13:48:50~$>  Next: 1 
// 13:48:50~$>  ---------- 1 
// 13:48:51~$>  Next: 2 
// 13:48:51~$>  ---------- 2 
// 13:48:51~$>  Disposing at 3 seconds 
// 13:48:52~$>  ---------- 3 
// 13:48:53~$>  ---------- 4 
// 13:48:54~$>  ---------- 5 
// 13:48:55~$>  Subscribing again at 6 seconds 
// 13:48:55~$>  Next: 6 
// 13:48:55~$>  ---------- 6 
// 13:48:56~$>  Next: 7 
// 13:48:56~$>  ---------- 7 
```  

.publish().refCount() == .share()  
接收新subscription时, 检测之前是否还有subscription未dispose, 若有继续现在的, 若无重新开始  

