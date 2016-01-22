---
layout: post
title: GCD - dispatch_set_target_queue
category: iOS
tags: Swift Define
keywords: Jekyll,Github
description: 
---

dispatch_set_target_queue 共有两个用法

## 1.变更优先级
```swift  
dispatch_queue_t serialQueue = dispatch_queue_create("com.gcd.serialQueue", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t serialDefaultQueue = dispatch_queue_create("com.gcd.serialDefaultQueue", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t globalDefaultQueue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0);

//变更前
dispatch_async(serialQueue, ^{
    NSLog(@"1");
});
dispatch_async(serialDefaultQueue, ^{
    NSLog(@"2");
});

//变更优先级
dispatch_set_target_queue(serialQueue, globalDefaultQueue);

//变更后
dispatch_async(serialQueue, ^{
    NSLog(@"1");
});
dispatch_async(serialDefaultQueue, ^{
    NSLog(@"2");
});

// 1
// 2
// 2
// 1
```  

## 2.改变队列层次体系
当我们想让不同队列中的任务同步的执行时，可以创建一个串行队列，然后将这些队列的target指向新建的队列即可  
例: 将多个串行queue指定到目标串行queue, 以实现某任务在多个串行 queue 也是先后执行 而非并行  

```swift  
dispatch_queue_t targetQueue = dispatch_queue_create("test.target.queue", DISPATCH_QUEUE_SERIAL);

dispatch_queue_t queue1 = dispatch_queue_create("test.1", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t queue2 = dispatch_queue_create("test.2", DISPATCH_QUEUE_SERIAL);
dispatch_queue_t queue3 = dispatch_queue_create("test.3", DISPATCH_QUEUE_SERIAL);

dispatch_set_target_queue(queue1, targetQueue);
dispatch_set_target_queue(queue2, targetQueue);
dispatch_set_target_queue(queue3, targetQueue);

dispatch_async(queue1, ^{
    NSLog(@"1 in");
    [NSThread sleepForTimeInterval:3.f];
    NSLog(@"1 out");
});
dispatch_async(queue2, ^{
    NSLog(@"2 in");
    [NSThread sleepForTimeInterval:2.f];
    NSLog(@"2 out");
});
dispatch_async(queue3, ^{
    NSLog(@"3 in");
    [NSThread sleepForTimeInterval:1.f];
    NSLog(@"3 out");
});

// 1 in
// 1 out
// 2 in
// 2 out
// 3 in
// 3 out

若屏蔽
// dispatch_set_target_queue(queue1, targetQueue);
// dispatch_set_target_queue(queue2, targetQueue);
// dispatch_set_target_queue(queue3, targetQueue);
执行结果为
// 1 in
// 2 in
// 3 in
// 3 out
// 2 out
// 1 out
```  




