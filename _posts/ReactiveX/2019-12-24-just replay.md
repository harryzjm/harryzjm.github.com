---  
layout: post  
title: just replay  
category: ReactiveX  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

```swift  
var num = 1
let signal = Observable<TimeInterval>
    .create { (observe) -> Disposable in
        let current = num; defer { num += 1 }
        print("---------------------------new \(current)")
        observe.onNext(Date().timeIntervalSince1970)
        observe.onNext(Date().timeIntervalSince1970)
        DispatchQueue.after(.seconds(1)) {
            observe.onNext(Date().timeIntervalSince1970)
            observe.onCompleted()
            print("---------------------------done \(current)")
        }
        return Disposables.create() }
//  .replayAll()

print("----------------------1")
signal.bind { (i) in
    print("1", i)
}.disposed(by: bag)

print("----------------------2")
signal.bind { (i) in
    print("2", i)
}.disposed(by: bag)

//signal.connect().disposed(by: bag)

DispatchQueue.after(.milliseconds(500)) {
    print("----------------------3")
    signal.bind { (i) in
        print("3", i)
    }.disposed(by: self.bag)
}

DispatchQueue.after(.seconds(2)) {
    print("----------------------4")
    signal.bind { (i) in
        print("4", i)
    }.disposed(by: self.bag)
}
```  

### normal  
```bash  
----------------------1
---------------------------new 1
1 1577239519.9551091
1 1577239519.955235
----------------------2
---------------------------new 2
2 1577239519.958106
2 1577239519.958146
----------------------3
---------------------------new 3
3 1577239520.504408
3 1577239520.504589
1 1577239520.984064
---------------------------done 1
2 1577239520.984493
---------------------------done 2
3 1577239521.601649
---------------------------done 3
----------------------4
---------------------------new 4
4 1577239522.008889
4 1577239522.0091028
4 1577239523.042561
---------------------------done 4
```  
1.有订阅后即开始发送 各自生成自己的信号流  
2.信号未结束 跟进订阅: 产生新信号流  
3.信号已结束 跟进订阅: 产生新信号流  

### publish()  
即 `replay(0)`  
```bash  
----------------------1
----------------------2
---------------------------new 1
1 1577239639.52909
2 1577239639.52909
1 1577239639.529395
2 1577239639.529395
----------------------3
1 1577239640.581406
2 1577239640.581406
3 1577239640.581406
---------------------------done 1
----------------------4
```  
1.控制首发 共享  
2.信号未结束 跟进订阅: 同步等待  
3.信号已结束 跟进订阅: 无任何信号流  

### replay(1)  
```bash  
----------------------1
----------------------2
---------------------------new 1
1 1577239712.420685
2 1577239712.420685
1 1577239712.420951
2 1577239712.420951
----------------------3
3 1577239712.420951
1 1577239713.422114
2 1577239713.422114
3 1577239713.422114
---------------------------done 1
----------------------4
```  
1.控制首发 共享  
2.信号未结束 跟进订阅: 补发之前一次 同步等待  
2.信号已结束 跟进订阅: 无任何信号流  

### replayAll()  
```bash  
----------------------1
----------------------2
---------------------------new 1
1 1577239753.553278
2 1577239753.553278
1 1577239753.5535269
2 1577239753.5535269
----------------------3
3 1577239753.553278
3 1577239753.5535269
1 1577239754.597208
2 1577239754.597208
3 1577239754.597208
---------------------------done 1
----------------------4
```  
1.控制首发 共享  
2.信号未结束 跟进订阅: 补发之前所有后 同步等待  
3.信号已结束 跟进订阅: 无任何信号流  