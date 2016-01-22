---  
layout: post
title: retryWhen & catchError
category: ReactiveX
tags: Swift Define
keywords: Jekyll,Github
description: 
---  


## 演示  
出现错误后3次重试 且 每次等待时间加长 出现第四次错误后catch  
```swift  
let retryHandler: (Observable<Error>) -> Observable<Int> = { e in
    return e.flatMapWithIndex { (err, index) -> Observable<Int> in
        if index > 2 {
            return Observable.error("Over").observeOn(MainScheduler.instance)
        }
        print(Date(), err)
        return Observable<Int>.timer(Double(index + 1), scheduler: MainScheduler.instance).take(1)
    }
}

Observable<String>.create { (observer) -> Disposable in
    num = num + 1
    observer.onError("No. \(num)")
    return Disposables.create()
    }
    .observeOn(MainScheduler.instance)
    .retryWhen(retryHandler)
    .catchError { (err) -> Observable<String> in
        print("catch: ", err)
        return Observable.just("Go on")
    }
    .subscribe { print("------", $0) }
    .disposed(by: self.bag)

// 2017-08-30 06:17:34 +0000 No. 1
// 2017-08-30 06:17:35 +0000 No. 2
// 2017-08-30 06:17:37 +0000 No. 3
// catch:  Over
// ------ next(Go on)
// ------ completed
```  
![](/assets/postAssets/2016/15040742516141.webp)


