---  
layout: post  
title: Huginn实现自动通过slack推送豆瓣高分电影  
category: internet  
tags: internet  
keywords: internet  
description: 
---  

__Posted by [WANG JIE](https://blog.wangjiegulu.com/2018/04/03/huginn_douban_high_score_movies_and_slack)__  

想象下以下场景：每当有正在上映的电影在豆瓣上的评分超过7.8分，则 huginn 自动编辑一条信息并通过 [`Slack`](https://slack.com/) （当然也可以用 telegram 等app）通知到我电脑或者手机上。收到信息后，点击不喜欢忽略，或者点击购票按钮直接进入到购票页面。甚至 Huginn 可以结合 `Google Calendar` 查询你这几天的行程安排，推送高分电影信息的同时给你选择一个比较合适观看电影的时间点，购买好电影票后，huginn 又自动帮你把日程事件写入到 `Google Calendar` 中，并设置提醒。是不是很酷？！

Huginn 就如你的贴心管家，按照你的意愿自动帮你完成很多事情。

我们先来实现 `每当有正在上映的电影在豆瓣上的评分超过7.8分，则给我推送 Slack 信息` 这一部分需求。

最后达到的效果如下：  

![](/assets/postAssets/2018/38308823-d6afbb92-384a-11e8-8db6-4f6def8ff371.webp)

### 创建 Agents

首先进入 Huginn 首页（默认`localhost:3000`），左上角进入 `Scenarios`：


![](/assets/postAssets/2018/38248922-84a7d57e-377c-11e8-8073-443bd59fd2f1.webp)


我的理解：**Scenario** 代表一种场景，一般会包含多个 **agent**，一个 agent 表示进行一次事件的处理或者变换。拿我们现在的例子来说，**自动通过slack推送豆瓣高分电影** 这一整个就是一个 `Scenario`，但是这个 `Scenario` 会有很多的 `agent`s 组成，比如：

* 有一个 agent 是用来从豆瓣网页获取当前上映中的所有电影和它们的分数等信息；
* 一个 agent 是用来从第一个 agent 里面拿到的所有电影进行过滤，过滤的标准就是 `score > 7.8`，
* 还有一个 agent 是用来把过滤后的电影通过 slack 推送到我们手机上。

看着跟 `RxJava` 的观察者模式是不是很像？第一个从豆瓣页面拉取数据的过程就像是 `Observable`，然后其它的 agent 就像很多的 `operator` 用来把数据进行转换和变化，最终通知到 `subscriber`，这里的 `subscriber` 就是我们自己。我们通过 huginn 订阅了 `豆瓣高分电影`，就是这么简单。

点击左下角的 `New Scenario` 创建一个名为 `douban_high_score_movie` 的 Scenario。

### 创建获取数据 agent

> 第一个 agent 用来从豆瓣官网获取所有正在上映的电影

在 `douban_high_score_movie` 的 Scenario 中点击 `+ New Agent` 来创建第一个 Agent。


![](/assets/postAssets/2018/38249853-b1eac0d4-377f-11e8-8242-022b28113653.webp)


如上图，你需要去决定你要创建的 agent 的类型（[这里](https://github.com/huginn/huginn/wiki/Agent-Types-&-Descriptions)是目前 Huginn 支持的所有的类型）。

我们通过输入 “web” 来进行过滤选择 `Website Agent`。


![](/assets/postAssets/2018/38283656-c5dc2f5a-37e9-11e8-8f3c-bd7d8d8d7c5e.webp)


上图，左边是我们需要去配置的地方；右边是每个设置对应的说明。

* **Name：**给这个 agent 取个名字，我们这里取名为 `step1_get_douban_playing_movies`，表示这个 agent 是 `douban_high_score_movie` 这个 Scenario 的第一步，是用来从豆瓣获取当前正在上映的所有电影。
* **Schedule：**表示调度周期，表示在什么时候自动执行这个 agent，比如 `Every 1d` 表示每一天执行一次、`Every 2h` 表示每2小时执行一次、`8pm` 表示每天下午8点执行等等；这里我们选择 `3pm`，每天下午3点执行一次。
* **Keep events：**表示事件保留的时间；比如我们从豆瓣上获取到所有上映的电影，每一部电影信息都是一个 event，Huginn会把这些 event 保留在本地，你可以通过这个参数来设置这些 events 在本地保留多少时间，超过这个时间，Huginn会把数据清除。我们这里设置1小时（为什么只设置为1小时，[下面我们会再讨论](https://blog.wangjiegulu.com/2018/04/03/huginn_douban_high_score_movies_and_slack/#keep_useless)）。
* **Sources：**表示这个 agent 处理的数据来源是哪个 agent。我们现在创建的 agent 是第一个 agent，是从豆瓣网站上获取正在上映的所有电影，所以不需要从其他 agent 传递数据（也就是上面说的 events）过来，所以这个留空。
* **Receivers：**表示这个 agent 处理完数据之后把这些数据传入到哪个 agent。还是用 `RxJava` 做类比，因为每个 agnet 都有可能只是整个观察者模式中的一个操作符，用来转化数据，数据转化完之后，可能还需要其他 agent 把这些数据做进一步的转化。
* **Scenarios：**表示这个 agent 是数据哪个 Scenario 的。
* **Options：**这个非常关键，就是通过这个配置文件（JSON）来进行网络请求和豆瓣电影数据解析相关的操作的，这个我们重点讲下。

> **注意：**以上没提到的配置可以留空

#### Options 配置

Options 配置其实就是一个 JSON 文件。Website Agent 的 Options 主要的元素有如下：

![](/assets/postAssets/2018/38284371-684365f8-37ed-11e8-8125-b94a2a35e12b.webp)


* **url：**网站地址，表示我需要从哪个网站获取数据，现在我们是从豆瓣，所以需要输入豆瓣正在上映的网址，这里我们输入 `https://movie.douban.com/cinema/nowplaying/hangzhou/`，当然最后一个地点可以根据你的常驻地点做相应的修改。
* **type：**数据解析的类型，支持的类型有 `xml`、`html`、`json`、`text` 四种，当前豆瓣网址返回的当然是 html 了，所以这里我们填写 `html`。如果其他场景，比如 调用第三方开放的 api，返回的类型可能就是 `json` 或者 `xml`了。
* **mode：**表示获取数据的模式，我们这里选择 `on_change`。
    * on_change：在数据有更改时才会获取作为 events。
    * merge：把新数据和输入的数据进行合并。
    * all：获取所有数据。
* **extract：**用来配置（JSON）从这个网站解析出真正我们想要的数据。如果 `type` 是 `html`，则每个数据通过 `css` 选择器或者 `xpath` 来解析出真正的数据。

> **注意：** `on_change` 这个设置在我们现在的场景下其实用处不大，这个[下面我们会再讨论](https://blog.wangjiegulu.com/2018/04/03/huginn_douban_high_score_movies_and_slack/#keep_useless)。

最后的 options 如下：

```json  
{
 "expected_update_period_in_days": "2",
 "url": "https://movie.douban.com/cinema/nowplaying/hangzhou/",
 "type": "html",
 "mode": "on_change",
 "extract": {
 "title": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-title"
 },
 "score": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-score"
 },
 "star": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-star"
 },
 "release": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-release"
 },
 "region": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-region"
 },
 "actors": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-actors"
 },
 "director": {
 "css": "li[@data-category='nowplaying']",
 "value": "@data-director"
 },
 "detail_url": {
 "css": "li[@data-category='nowplaying']/ul/li/a[@data-psource='poster']",
 "value": "@href"
 },
 "image_url": {
 "css": "li[@data-category='nowplaying']/ul/li/a[@data-psource='poster']/img",
 "value": "@src"
 }
 }
}
```  

以上可以看出，我们从豆瓣的每部电影中获取了以下信息：

* title：电影名字
* score：电影分数，满分10分
* star：电影分数，满分50分
* release：上映日期
* region：地区
* actors：演员
* director：导演
* detail_url：详细 url
* image_url：电影封面

> **注意：**获取具体 xpath 比较简单的方法：通过 chrome 右键的 `inspect` 来复制拿到。

以上配置完毕后，点击下面的 `Dry Run`，应该就会出现以下页面


![](/assets/postAssets/2018/38285255-f7211d02-37f1-11e8-84ee-c6b74401094e.webp)


最后进行保存。第一个 agent 就创建完毕了。

同时，这个 agent 在运行的过程中会生成以下 events：


![](/assets/postAssets/2018/38285762-5520c52c-37f4-11e8-9db5-ffa0f1116924.webp)


### 创建过滤 agnet

`step1_get_douban_playing_movies` 把所有正在上映的电影数据从豆瓣上拉取下来并解析好，生成一个个 events。然后我们第二个 agent 就需要从这些 events 里面进行过滤筛选出所有分数大于 `7.8`（具体的标准可以自己定） 的电影。相当于 RxJava 的 filter 操作符吧。

同样创建 agent，选择为 `TriggerAgent`，名字为 `step2_pick_high_score_movies`。这是把 **Sources** 填写为第一个 agent 的名字，即 `step1_get_douban_playing_movies`，表示我要创建的 agent 处理的数据（events）是从 `step1_get_douban_playing_movies` 来的。

然后重点还是在 Options 中

* **keep_event：**表示是否把我从 `step1_get_douban_playing_movies` 这个 agent 收到的 events 原封不动地再传给下一个 agent（下一个 agent 我们还没创建），我们设置为 true。因为下一个 agent 我们是用来把数据通过 slack 发送到给我们自己的，那肯定需要第一个 agent 中获取到的例如电影名字、分数等信息。
* **rules：**表示我们过滤的规则，可以多个，具体下面说。
* **must_match：**表示 rules 中我必须要满足几个规则，如果是1，则意味着 rules 中所有的规则是或关系（只要满足 rules 中的1个规则即可）；默认不填写的话是**必须要满足 rules 中所有的规则。**，因为我们这里只需要满足一个分数大于7.8就可以，所以可以不填写。

最后 Options 的配置如下：

```json  
{
 "expected_receive_period_in_days": "2",
 "keep_event": "true",
 "rules": [
 {
 "type": "field>=value",
 "value": "7.8",
 "path": "$.score"
 }
 ],
 "message": "Looks like your pattern matched in '{{value}}'!"
}
```  

如上，在 **rules** 中添加一个规则，**type** 表示匹配规则，`field>=value`：

* **field**: 通过下面 path 从 events 匹配出来的数据，这里是 `$.score`，所以表示的是电影的分数；
* **value**：表示下面 json 的 `value` 字段的值，这里为 `7.8`。

通过简单的表达式 `field>=value` 来设定匹配规则：电影分数 >= 7.8分。

至此，第二个 agent 创建完毕。

你同样可以通过下面的 `Dry Run` 来进行测试，测试时因为有 `Sources`，需要你构造一些假数据作为输入来运行。

### 创建去重 agnet

`step2_pick_high_score_movies`用来把 `step1_get_douban_playing_movies` 中从豆瓣官网获取的电影信息进行高分的过滤（分数>=7.8）。

我们还需要创建一个去重的 agent，来避免重复给我们自己推送高分电影（因为我们现在获取的频率是每天进行获取检测，但是电影总不可能是每部电影只上映一天吧，第二天获取的时候肯定有第一天获取的数据）。

这里大家可能会有个问题，因为我们在配置第一个 agent 的时候，已经把 `mode` 已经设置为 `on_change`了，为什么还是会有重复数据呢？因为这里的电影信息中，有诸如 `分数` 这类的数据，这些数据是随时可能会有变化的，虽然是同一个电影，但是分数从 `8.1` 上升到 `8.2`，那 Huginn 也会认为满足了 `on_change` 条件，所以会造成重复推送。所以，我们还需要单独做去重处理。

> **注意：** 之前提到过 `on_change` 等设置在第一个 agent 其实用处不大，同样也是由于上面说的原因，我们也不知道同样的电影什么时候分数会发生变化，就算用了 `on_change`，也可能会把之前获取过的数据拿到。所以第一个 agent 的 keep_event 设置的时间比较短，因为这些 events 提供给 `on_change` 匹配意义不大，所以还是节省空间，设置短一点。

创建 agent，type 选择 `DeDuplicationAgent`，名字取为 `step2_1_deduplication_high_score_movies`，**Sources** 填写为上一个 agent 的名字，即 `step2_pick_high_score_movies`。

> **注意：**这里 **keep_event** 设置了90天，因为一旦经过我们这个 agent 去重后，events 假设保留1小时，那下一天我再去获取所有上映的电影并高分过滤后，因为昨天的数据（events）已经被清空了，所以就没办法做比较去重了，所以会导致重复数据。所以这里保存时间应该要>=电影上映的时长，所以这里设置为90天，即3个月左右。

DeDuplicationAgent 的 Options 填写就比较简单了

![](/assets/postAssets/2018/38286554-8fa7b166-37f8-11e8-9d8b-601bf37c895e.webp)


* **Property：**填写你要去重依据的字段，我们这里根据电影名字来去重，也就是 `title`。
* **Lookback：**表示去重的时候跟之前的多少条历史 events 做比较，同一时期一起上映的电影应该不会超过100部，所以设置为100了。

### 创建 slack 通知的 agent

Huginn 自带有一个 `SlackAgent`，用来发送 slack 消息。


![](/assets/postAssets/2018/38287159-d1b96f10-37fb-11e8-835f-0b9e620ab075.webp)


它使用了 [incoming-webhooks](https://api.slack.com/incoming-webhooks) 来实现消息的发送。

但是为了有更多的可玩性，我们这里选择，自己创建一个 `slack app`，然后通过它的 open api 实现。

因此，我们需要创建一个 `PostAgent`。但是在此之前我们先来配置好 Slack 环境。

#### 配置 Slack 环境

安装 Slack：[https://slack.com](https://slack.com/)

* Google Play for Android：[https://play.google.com/store/apps/details?id=com.Slack](https://play.google.com/store/apps/details?id=com.Slack)

创建自己的 workspace（单独创建一个自己私有的，注意不要使用公司、团队的 workspace），比如我的是 `https://wangjie.slack.com`。

在自己私有的 workspace 中创建一个私有的 channel：`#huginn-movie`


![](/assets/postAssets/2018/38288443-62b02016-3803-11e8-8733-ded2ac3b535b.webp)


这个 channel 就是用来接收高分电影的数据了，当然你也可以使用 `#general`。

然后我们创建一个自己的 app，用来发送电影信息。进入 [https://api.slack.com/](https://api.slack.com/)


![](/assets/postAssets/2018/38288591-4f2cf702-3804-11e8-9b96-fe8561c21e9c.webp)


点击 `Start Building`，


![](/assets/postAssets/2018/38288667-a0cc323a-3804-11e8-9a7d-6da84babc266.webp)


* **App Name：**可以随意填写
* **Development Slack Workspace：**选择你刚刚创建的私有的 workspace

在 `Add features and functionality` 中点击 `Permissions` 进入权限配置。

在 `Scope` 中添加如下权限：


![](/assets/postAssets/2018/38288837-a0438740-3805-11e8-821e-5e91a1bf401e.webp)


添加完以上所有权限后，点击保存，然后重新打开 `Permissions`，点击下面按钮安装我们的这个 app 到 slack。


![](/assets/postAssets/2018/38288942-31655e06-3806-11e8-92af-63c67f778570.webp)



安装完毕之后，再次进入 `Permissions`，拷贝 `OAuth Access Token`：


![](/assets/postAssets/2018/38289144-4ad7c56c-3807-11e8-9599-4e64dd704258.webp)


然后，我们就可以使用我们的 token 来访问 slack 的 open api 了，具体文档在这里：[https://api.slack.com/web](https://api.slack.com/web)。

我们需要的发送消息到 `#huginn-movie` channel 的接口文档：
[https://api.slack.com/methods/chat.postMessage](https://api.slack.com/methods/chat.postMessage)

有了 api 文档，有了 token，一切就好办了。


![](/assets/postAssets/2018/38289564-69cd36bc-3809-11e8-820f-8f7cddaf64cb.webp)


由上述文档，我们可以通过 post 请求，把我们要发送的电影信息封装到 `attachments` 参数中执行请求即可。

而且 `attachments` 参数可以参考文档 [https://api.slack.com/docs/message-attachments](https://api.slack.com/docs/message-attachments) 来封装信息。

Slack 环境一切就绪，接下来，回到 Huginn。

#### 创建 Agent 发送 Slack 消息

创建 `PostAgent`（注意，不是 `SlackAgent`），取名为 `step3_high_score_movies_to_slack_post`。**Sources** 填写为 `step2_1_deduplication_high_score_movies`，因为这个 agent 需要把去重后的电影信息通过 slack 发送给我们。

最终的 Options 配置如下：

```json  
{
  "post_url": "{% raw %}{% credentials slack_huginn_url_post_message %}{% endraw %}", 
  "expected_receive_period_in_days": "1", 
  "content_type": "json", 
  "method": "post", 
  "payload": {
    "channel": "huginn-movie", 
    "username": "Douban Movie", 
    "icon_url": "https://img3.doubanio.com/pics/douban-icons/favicon_48x48.png", 
    "attachments": [
      {
        "fallback": "Required plain-text summary of the attachment.", 
        "mrkdwn_in": [
          "text", 
          "pretext"
        ], 
        "color": "#36a64f", 
        "pretext": "Hi~ , There is *high score* movie.", 
        "author_name": "{{director}}", 
        "author_link": "{{detail_url}}", 
        "author_icon": "", 
        "title": "《{{title}}》", 
        "title_link": "{{detail_url}}", 
        "text": "*Actors*: {{actors}}", 
        "fields": [
          {
            "title": "Score", 
            "value": "{{score}}", 
            "short": true
          }, 
          {
            "title": "Star", 
            "value": "{{star}}", 
            "short": true
          }, 
          {
            "title": "Region", 
            "value": "{{region}}", 
            "short": true
          }, 
          {
            "title": "Release", 
            "value": "{{release}}", 
            "short": true
          }
        ], 
        "image_url": "", 
        "thumb_url": "{{image_url}}", 
        "footer": "Slack", 
        "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png", 
        "ts": "{{'now' | date: '%s'}}"
      }
    ]
  }, 
  "headers": {
    "Content-Type": "application/json", 
    "Authorization": "{% raw %}{% credentials slack_huginn_token %}{% endraw %}"
  }, 
  "emit_events": "false", 
  "no_merge": "false", 
  "output_mode": "clean"
}
```  

需要注意的是：

* `{\% credentials slack_huginn_url_post_message %\}`：此类的表达式为 [Liquid-interpolated](https://github.com/huginn/huginn/wiki/Formatting-Events-using-Liquid)，具体的值配置在 `Credentials` 中，可以理解为全局定义，在 `Credentials` 中配置好 `key-value` 之后，可以在其它地方以诸如 `{\% credentials key \%}` 的方式来使用，这里不做过多介绍了。

* 在消息中使用Slack 中的 `@` 某人的功能时，需要拿到对应用户的 ID，可以的获取方式可以通过在 slack 中选中名字然后 `Copy link` 的方式拿到用户链接，用户连接的最后就是 ID。


![](/assets/postAssets/2018/38290017-c49db6c8-380b-11e8-817c-bbd1aa25396e.webp)


保存该 Agent，至此，所需的所有的 Agent 都已经创建完毕了。

## 总结

整个 Scenario 的事件流程图如下：


![](/assets/postAssets/2018/38290316-44ee5e12-380d-11e8-9da2-d6d995fb3e1a.webp)


Huginn 还支持公开你创建的 Scenario，提供给其它人使用，以上的代码也已经公开：

[http://h.wangjiegulu.com/scenarios/8/export.json](http://h.wangjiegulu.com/scenarios/8/export.json)

大家可以直接下载使用，不过需要在 `Credentials` 中配置如下参数：

* **slack_huginn_token：**你创建的 Slack App 的 OAuth Access Token，具体方式可以参考[这里](https://blog.wangjiegulu.com/2018/04/03/huginn_douban_high_score_movies_and_slack/#slack_token)
* **slack_at_user_id：**你需要 @ 的 slack 用户 ID，填写你自己的，拿到你 ID 的方式可以参考[这里](https://blog.wangjiegulu.com/2018/04/03/huginn_douban_high_score_movies_and_slack/#slack_at_anyone)
* **slack_huginn_url_post_message：**填写 `https://slack.com/api/chat.postMessage` 即可。

除了以上例子，Huginn 还可以完成更多奇思妙想，限制你的只有你的想象力。

