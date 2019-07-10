---  
layout: post  
title: How to Use x-callback-url 
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

![](/assets/postAssets/2019/15627256600441.jpg)


```swift  
// in iOS
let params = URLScheme.allParameters()
let baseURL = params["x-success"]
let url = baseURL + "?hello=world&foo=bar"
Safari.open(url)
```  

```js  
// in JSBox
let baseURL = $context.query["x-success"]
if (baseURL != undefined && baseURL.length > 0) {
	let url = baseURL + "?hello=world&foo=bar"
	$app.openURL(url)
}
```  