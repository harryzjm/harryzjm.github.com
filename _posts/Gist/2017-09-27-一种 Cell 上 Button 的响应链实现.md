---  
layout: post  
title: 一种 Cell 上 Button 的响应链实现  
category: Gist  
tags: Gist  
keywords: Gist  
description: 
---  

__Posted by [lsb332](http://www.jianshu.com/p/8fef9171c322/)__  

利用 UIResponder 传递响应  

```swift  
// Swift 5  
extension UIResponder {  
    @objc func routerEvent(with name: String, userInfo: [String:Any]) {  
        next?.routerEvent(with: name, userInfo: userInfo)  
    }  
}  

// TableCell.swift  
func buttonClick(btn: UIButton) {  
    routerEvent(with: "CellButtonKey", userInfo:  ["cell": self])  
}  

// ViewController.swift  
@objc override func routerEvent(with name: String, userInfo: [String : Any]) {  
    switch name {  
    case "CellButtonKey":  
        manageButtonClick(userInfo)  
    default: break  
    }  
}  
```  

