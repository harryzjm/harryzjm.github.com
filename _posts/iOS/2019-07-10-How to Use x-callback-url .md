---  
layout: post  
title: How to Use x-callback-url 
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

![](/assets/postAssets/2019/15627256600441.jpg)


```js  
// in JSBox
let baseURL = $context.query["x-success"]
if (baseURL != undefined && baseURL.length > 0) {
	// X-Callback value 为 { "hello" : "world", "foo" : "bar" }
  let url1 = baseURL + "?hello=world&foo=bar"
  // X-Callback value 为 world
  let url2 = baseURL + "?result=world"
  $app.openURL(url2)
}
```  