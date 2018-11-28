---
layout: post
title: 天下寂然
---

<div style="display:flex;justify-content:space-between;align-items:center;">
  <div>
    <h3>欢迎你来到这里!</h3>
    <p>我是<a style="display:inline-block;" href="https://github.com/harryzjm"><b>Hares</b></a>, <b>iOS软件工程师</b>, 目前正在探索前端世界...</p>
    <p>若对博客内容有疑问, 或是建议, 请联系我.</p>
    <b>邮件:<a style="display:inline-block;" href="mailto:harryzjm@live.com">harryzjm@live.com</a></b>
  </div>
  <div align="left"  style="flex:1 0;">
    <img src="/assets/photo/welcome.gif">
  </div>
</div>

### 快捷路径    

[Github Stars Manager](https://iangeli.github.io/stars)

[Shell](https://iangeli.com/2014/01/15/shell.html) | [网络地址](https://harryzjm.github.io/2018/06/12/%E7%BD%91%E7%BB%9C%E5%9C%B0%E5%9D%80.html) | [Mac本地地址](https://iangeli.com/2018/06/13/Mac%E6%9C%AC%E5%9C%B0%E5%9C%B0%E5%9D%80.html)  
-- | -- | --  
[iOS版本占有率查询](https://developer.apple.com/support/app-store/) |  |   


<h3>才艺展示</h3>
<div id="container"></div>

<script type="text/javascript">
  function preloadImages(urls, callback, param) {
    if (urls.length == 0) { callback(param); return }
    var img = new Image()
        img.src = urls[0]
        if (img.complete) {
      preloadImages(urls.slice(1), callback, param)
    } else {
        img.onload = function() {
            preloadImages(urls.slice(1), callback, param)
        }
            }
  }
  function animate(urls) {
    let container = document.getElementById('container')
    const count = (urls.length + 1) / 2
    for (let i = 0; i < count; i++) {
      let div = document.createElement('div')
            container.appendChild(div)
      for (let j = 0; j < count; j++) {
        let img = new Image()
                setTimeout(function (div) {
          img.src = urls[i+j]
          div.appendChild(img)
        }, 500 * (i+j), div)
      }
    }
  }

  const url = '/assets/photo/skill.gif'
  const pageWidth = Math.floor(document.getElementById('post__content').clientWidth / 100)
  const count = Math.max(Math.min(pageWidth, 4), 1)
  const urls = Object.keys(Array.apply(null, {length: count * 2 - 1})).map(function(item){
    return url + `?a=` + item
  })
  
  preloadImages(urls, animate, urls)
</script>




