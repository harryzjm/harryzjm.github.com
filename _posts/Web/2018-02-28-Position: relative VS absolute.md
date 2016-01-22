---
layout: post
title: Position-relative VS absolute
category: Web
tags: Web
keywords: Web
description: 
---

```html  
<!DOCTYPE html>
<html>
<head>
<style>
div.relative {
    position: relative;
    width: 400px;
    height: 200px;
    border: 3px solid #73AD21;
} 

div.absolute {
    position: absolute;
    top: 0px;
    right: 0;
    width: 200px;
    height: 100px;
    border: 3px solid #73AD21;
}
</style>
</head>
<body>

<h1>Position</h1>
<h2>relative VS absolute</h2>

<p>next<br/><br/><br/><br/>show</p>


<div class="relative">relative
  <div class="absolute">absolute</div>
</div>
<div class="absolute">absolute</div>

</body>
</html>

```  

relative: 相对其正常位置
absolute: 相对于最近的定位祖先

![](/assets/postAssets/2018/15238654557878.webp)

