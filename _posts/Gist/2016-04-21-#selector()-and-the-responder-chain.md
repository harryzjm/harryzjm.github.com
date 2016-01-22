---
layout: post
title: #selector() and the responder chain
category: Gist
tags: Swift
keywords: Jekyll,Github
description: 
---

__[Posted by Dominik Hauser](http://swiftandpainless.com/selector-and-the-responder-chain/ "Permalink to #selector() and the responder chain")__


With the new syntax for selectors in Swift 2.2 the approach I used in ["Utilize the responder chain for target action"][1] produces a warning. Let's fix that.

## Protocols for president

First we add a protocol:    
```swift  
@objc protocol DetailShowable {
  	func showDetail()
}  
```  
Then we can add an extension to  

	Selector  
	
as described in [this awesome post][2] by [Andyy Hope][3] that looks like this:    
```swift  
private extension Selector { 
  static let showDetail = #selector(DetailShowable.showDetail) 
}  
```  
Adding the action to the responder chain is then as easy as this:  
```swift  
button.addTarget(nil,
                 action: .showDetail,
                 forControlEvents: .TouchUpInside)  
```  
Then some responder object in the responder chain needs to conform to the  
	DetailShowable   
protocol.

You can find the code on [github][4].


[1]: http://swiftandpainless.com/utilize-the-responder-chain-for-target-action/
[2]: https://medium.com/swift-programming/swift-selector-syntax-sugar-81c8a8b10df3#.6gteb7p1s
[3]: https://twitter.com/AndyyHope
[4]: https://github.com/dasdom/SelectorSyntaxSugar


