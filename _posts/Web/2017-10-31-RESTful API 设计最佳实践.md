---  
layout: post  
title: RESTful API 设计最佳实践  
category: Web  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__[Philipp Hauer](https://blog.philipphauer.de/restful-api-design-best-practices/)__  
__[SlaneYang译](http://www.zcfy.cc/article/restful-api-design-best-practices-in-a-nutshell-4388.html)__  

项目资源的URL应该如何设计？用名词复数还是用名词单数？一个资源需要多少个URL？用哪种HTTP方法来创建一个新的资源？可选参数应该放在哪里？那些不涉及资源操作的URL呢？实现分页和版本控制的最好方法是什么？因为有太多的疑问，设计RESTful API变得很棘手。在这篇文章中，我们来看一下RESTful API设计，并给出一个最佳实践方案。  

### 每个资源使用两个URL  

资源集合用一个URL，具体某个资源用一个URL：  
```swift  
/employees           #资源集合的URL  
/employees/56      #具体某个资源的URL  
```  

### 用名词代替动词表示资源  

这让你的API更简洁，URL数目更少。不要这么设计：  
```swift  
/getAllEmployees  
/getAllExternalEmployees  
/createEmployee  
/updateEmployee  
```  
 更好的设计：  
```swift  
GET /employees  
GET /employees?state=external  
POST /employees  
PUT /employees/56  
```  

### 用HTTP方法操作资源  

使用URL指定你要用的资源。使用HTTP方法来指定怎么处理这个资源。  
* **GET (获取)**：GET请求不改变资源的状态。只读,无副作用。可用于缓存。  
* **POST (创建)**：创建新的资源。  
* **PUT (更新)**：更新现有资源。  
* **DELETE (删除)**：删除现有资源。  

2个URL乘以4个HTTP方法就是一组很好的功能。看看这个表格：  

||POST（创建）|GET（读取）|PUT（更新）|DELETE（删除）|  
| --- | --- | --- | --- | --- |  
| /employees | 创建一个新员工 | 列出所有员工 | 批量更新员工信息 | 删除所有员工 |  
| /employees/56 | （错误） | 获取56号员工的信息 | 更新56号员工的信息 | 删除56号员工 |  

### 对资源集合的URL使用POST方法，创建新资源  

创建一个新资源的时，客户端与服务器是怎么交互的呢？![](/assets/postAssets/2017/1508163502633713.webp)  
在资源集合URL上使用POST来创建新的资源过程  
1. 客户端向资源集合URL`/employees`发送POST请求。HTTP body 包含新资源的属性 “Albert Stark”。  
2. RESTful Web服务器为新员工生成ID，在其内部模型中创建员工，并向客户端发送响应。这个响应的HTTP头部包含一个Location字段，指示创建资源可访问的URL。  

### 对具体资源的URL使用PUT方法，来更新资源  

![](/assets/postAssets/2017/1508163502242435.webp)  

使用PUT更新已有资源  
1. 客户端向具体资源的URL发送PUT请求`/employee/21`。请求的HTTP body中包含要更新的属性值（21号员工的新名称“Bruce Wayne”）。  
2. REST服务器更新ID为21的员工名称，并使用HTTP状态码200表示更改成功。  

### 推荐用复数名词  

推荐：  
```swift  
/employees  
/employees/21  
```  
 不推荐：  
```swift  
/employee  
/employee/21  
```  
 事实上，这是个人爱好问题，但复数形式更为常见。此外，在资源集合URL上用GET方法，它更直观，特别是`GET /employees?state=external`、`POST /employees`、`PUT /employees/56`。但最重要的是：避免复数和单数名词混合使用，这显得非常混乱且容易出错。  

### 对可选的、复杂的参数，使用查询字符串（？）。  

不推荐做法：  
```swift  
GET /employees  
GET /externalEmployees  
GET /internalEmployees  
GET /internalAndSeniorEmployees  
```  
 为了让你的URL更小、更简洁。为资源设置一个基本URL，将可选的、复杂的参数用查询字符串表示。  
```swift  
GET /employees?state=internal&maturity=senior  
```  

### 使用HTTP状态码  

RESTful Web服务应使用合适的HTTP状态码来响应客户端请求  
* 2xx – 成功 – 一切都很好  
* 4xx – 客户端错误 – 如果客户端发生错误（例如客户端发送无效请求或未被授权）  
* 5xx – 服务器错误 – 如果服务器发生错误（例如，尝试处理请求时出错） 参考[维基百科上的HTTP状态代码](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes)。但是，其中的大部分HTTP状态码都不会被用到，只会用其中的一小部分。通常会用到一下几个：  

|2xx：成功|3xx：重定向|4xx：客户端错误|5xx：服务器错误|  
| --- | --- | --- | --- |  
| 200 成功 | 301 永久重定向 | 400 错误请求 | 500 内部服务器错误 |  
| 201 创建 | 304 资源未修改 | 401未授权 |   |  
|   |   | 403 禁止 |   |  
|   |   | 404 未找到 |   |  

### 返回有用的错误提示  

除了合适的状态码之外，还应该在HTTP响应正文中提供有用的错误提示和详细的描述。这是一个例子。 请求：  
```swift  
GET /employees?state=super  
```  
响应：  
```swift  
// 400 Bad Request  
{  
	    "message": "You submitted an invalid state. Valid state values are 'internal' or 'external'",  
    "errorCode": 352,  
    "additionalInformation" :  
    "http://www.domain.com/rest/errorcode/352"  
}  
```  

### 使用小驼峰命名法  

使用小驼峰命名法作为属性标识符。  
```swift  
{  "yearOfBirth": 1982  }  
```  
 不要使用下划线（`year_of_birth`）或大驼峰命名法（`YearOfBirth`）。通常，RESTful Web服务将被JavaScript编写的客户端使用。客户端会将JSON响应转换为JavaScript对象（通过调用`var person = JSON.parse(response)`），然后调用其属性。因此，最好遵循JavaScript代码通用规范。  
对比：  
```swift  
person.year_of_birth  // 不推荐，违反JavaScript代码通用规范  
person.YearOfBirth  // 不推荐，JavaScript构造方法命名  
person.yearOfBirth  // 推荐  
```  

### 在URL中强制加入版本号  

从始至终，都使用版本号发布您的RESTful API。将版本号放在URL中以是必需的。如果您有不兼容和破坏性的更改，版本号将让你能更容易的发布API。发布新API时，只需在增加版本号中的数字。这样的话，客户端可以自如的迁移到新API，不会因调用完全不同的新API而陷入困境。  
使用直观的 “v” 前缀来表示后面的数字是版本号。  
```swift  
/v1/employees  
```  
 你不需要使用次级版本号（“v1.2”），因为你不应该频繁的去发布API版本。  

### 提供分页信息  

一次性返回数据库所有资源不是一个好主意。因此，需要提供分页机制。通常使用数据库中众所周知的参数offset和limit。  
```swift  
/employees?offset=30&limit=15 #返回30 到 45的员工  
```  
 如果客户端没有传这些参数，则应使用默认值。通常默认值是`offset = 0`和`limit = 10`。如果数据库检索很慢，应当减小`limit`值。  
```swift  
/employees #返回0 到 10的员工  
```  
 此外，如果您使用分页，客户端需要知道资源总数。例： 请求：  
```swift  
GET /employees  
```  
 响应：  
```swift  
{  
    "offset": 0, 
    "limit": 10, 
    "total": 3465, 
    "employees": [ ]  
     //...  
}  
```  

### 非资源请求用动词  

有时API调用并不涉及资源（如计算，翻译或转换）。例：  
```swift  
GET /translate?from=de_DE&to=en_US&text=Hallo  
GET /calculate?para2=23&para2=432  
```  
 在这种情况下，API响应不会返回任何资源。而是执行一个操作并将结果返回给客户端。因此，您应该在URL中使用动词而不是名词，来清楚的区分资源请求和非资源请求。  

### 考虑特定资源搜索和跨资源搜索  

提供对特定资源的搜索很容易。只需使用相应的资源集合URL，并将搜索字符串附加到查询参数中即可。  
```swift  
GET /employees?query=Paul  
```  
 如果要对所有资源提供全局搜索，则需要用其他方法。前文提到，对于非资源请求URL，使用动词而不是名词。因此，您的搜索网址可能如下所示：  
```swift  
GET /search?query=Paul //返回 employees, customers, suppliers 等等.  
```  

### 在响应参数中添加浏览其它API的链接  

理想情况下，不会让客户端自己构造使用REST API的URL。让我们思考一个例子。 客户端想要访问员工的薪酬表。为此，他必须知道他可以通过在员工URL（例如`/employees/21/salaryStatements`）中附加字符串“salaryStatements”来访问薪酬表。这个字符串连接很容易出错，且难以维护。如果你更改了访问薪水表的REST API的方式（例如变成了`/employees/21/salary-statement`或`/employees/21/paySlips`），所有客户端都将中断。 更好的方案是在响应参数中添加一个`links`字段，让客户端可以自动变更。  
请求：  
```swift  
GET /employees/  
```  
 响应：  
```swift  
//...  
{  
    "id": 1, 
    "name": "Paul", 
    "links": [  
        {  
            "rel": "salary", 
            "href": "/employees/1/salaryStatements"  
        }  
    ]  
}  
 //...  
```  
 如果客户端完全依靠`links`中的字段获得薪资表，你更改了API，客户端将始终获得一个有效的URL（只要你更改了`link`字段，请求的URL会自动更改），不会中断。另一个好处是，你的API变得可以自我描述，需要写的文档更少。  
在分页时，您还可以添加获取下一页或上一页的链接示例。只需提供适当的偏移和限制的链接示例。  
```swift  
GET /employees?offset=20&limit=10  
```  
```swift  
{  
    "offset": 20, 
    "limit": 10, 
    "total": 3465, 
    "employees": [ ], 
    "links": [  
        {  
            "rel": "nextPage", 
            "href": "/employees?offset=30&limit=10"  
        }, 
        {  
            "rel": "previousPage", 
            "href": "/employees?offset=10&limit=10"  
        }  
    ]  
}  
```  

### 相关阅读  

* 作者写的一篇关于在[Java中测试RESTful服务的最佳实践](https://blog.philipphauer.de/testing-restful-services-java-best-practices/)的文章。  
* 作者强烈推荐一本书[Brain Mulloy’s nice paper](https://pages.apigee.com/rs/apigee/images/api-design-ebook-2012-03.pdf)，作为这篇文章的基础。  

