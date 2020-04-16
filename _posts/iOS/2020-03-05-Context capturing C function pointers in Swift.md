---  
layout: post  
title: Context capturing C function pointers in Swift 
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [vmanot](https://vmanot.com/context-capturing-c-function-pointers-in-swift)__  

Take the following code:

```swift  
func foo() {
    let bar = NSObject()

    let f: (@convention(c) () -> ()) = {
        print(bar)
    }
}

```

This will not compile. You will instead be presented with the following error:

```bash  
error: a C function pointer cannot be formed from a closure that captures context

```

While you are unlikely to ever encounter this error in typical iOS development, it may arise as the result of, say, an attempt to interface with a low-level C library/framework. In my case, I was trying to construct a parameter for a low-level POSIX function (`pthread_create`), which only accepted a C function pointer.

There is a (dirty) workaround:

```swift  
import ObjectiveC
import Swift

func cFunction(_ block: (@escaping @convention(block) () -> ()))
    -> (@convention(c) () -> ()) {
    return unsafeBitCast(
        imp_implementationWithBlock(block),
        to: (@convention(c) () -> ()).self
    )
}

```

This effectively allows you to write:

```swift  
func foo() {
    let bar = NSObject()

    let f: (@convention(c) () -> ()) = cFunction {
        print(bar)
    }
}

```

Which is, in fact, valid Swift code.

So… what does `cFunction` do? It:

* Takes an Objective-C block pointer (specified using the attribute `@convention(block)`).
* Uses [`imp_implementationWithBlock`](https://developer.apple.com/documentation/objectivec/1418587-imp_implementationwithblock) to construct a C function pointer from aforementioned block.
* Uses [`unsafeBitCast`](https://developer.apple.com/documentation/swift/1641250-unsafebitcast) to cast said function pointer to the appropriate Swift representation (another attributed function type, this time with [`@convention(c)`](https://developer.apple.com/documentation/swift/imported_c_and_objective-c_apis/using_imported_c_functions_in_swift))

While this works, there are a few points to note:

* It relies on the Objective-C runtime, using a function that is typical reserved for converting C function pointers with arguments usually in the format of `id, SEL, ...`.
* In the example code, `bar` will be retained indefinitely. That is because C function pointers are not deallocated like Objective-C block pointers once they go out of scope. You must manually deallocate `bar` once you are done using it. This may be done by way of a flag, or based on some information derived from maybe an argument passed to the callback.