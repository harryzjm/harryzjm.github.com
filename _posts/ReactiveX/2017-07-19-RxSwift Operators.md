---  
layout: post  
title: RxSwift Operators  
category: ReactiveX  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

# SwitchLatest  
```swift  
let 👦🏻 = BehaviorSubject<CustomStringConvertible>(value: 0)  
let 👧🏼 = BehaviorSubject<CustomStringConvertible>(value: "A")  

let player = Variable(👦🏻)  

player.asObservable()  
    .switchLatest()  
    .subscribe(onNext: { print($0, terminator: "\t") })  
    .disposed(bag)  

👦🏻.onNext(1)  

player.value = 👧🏼  

👧🏼.onNext("B")  
👦🏻.onNext(2)  
👧🏼.onNext("C")  
👦🏻.onNext(3)  

// 0	1	A	B	C  
```  
注: 与**flatMapLatest**区别  
.flatMapLatest(func) == .map(func).switchLatest()  

# Merge(maxConcurrent:)  
```swift  
let subject1 = PublishSubject<Int>()  
let subject2 = PublishSubject<Int>()  
let subject3 = PublishSubject<Int>()  

_ = Observable.of(subject1, subject2, subject3)  
    .merge(maxConcurrent: 1)  
    .subscribe {  
        print($0)  
}  
subject1.on(.next(111))  
subject2.on(.next(222))  
subject3.on(.next(333))  
subject1.onCompleted()  
print("Subject1 Completed")  
subject2.on(.next(222))  
subject3.on(.next(333))  

// next(111)  
// Subject1 Completed  
// next(222)  
```  
merge中可并行的序列  
因为PublishSubject序列 故之前的不补发  

