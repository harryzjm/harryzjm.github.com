---  
layout: post
title: Functor、Applicative 和 Monad
category: ReactiveX
tags: Swift Define
keywords: Jekyll,Github
description: 
---  


__[Posted by Aditya Bhargava](http://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html")__



你可以在 [GitHub](https://github.com/mokacoding/Swift-Functors-Applicative-Monads-In-Pictures-Playground) 找到包含本文所有代码的 playground。  


这是一个简单的值（value）：

![](/assets/postAssets/2016/6941baebgw1ev5g0orf6rj202h02y745.webp)

我们也知道如何使用函数（function）来处理值：

![](/assets/postAssets/2016/6941baebgw1ev5g0pipa6j20f203taaa.webp)

这很容易懂，那么拓展一下，任意值都能在处于特定的上下文（context）中。你可以先想象上下文就像是一个盒子，你可以把值放进去。

![](/assets/postAssets/2016/6941baebgw1ev5g0p1sv5j204g06y0sx.webp)

现在当你使用函数处理这个值，根据上下文的不同会得到不同的结果。Functors, Applicatives, Monads，Arrows等概念都是基于此。`Optional` 类型定义了两种相关的上下文:

> 注意：图上的 Maybe（Just | None）来自 Haskell，类似于 Swift 的 Optional，`.Some` 和 `.None`。

![](/assets/postAssets/2016/6941baebgw1ev5g0maov1j207u05et91.webp)
```swift  
enum  Optional  {
  case  None
  case  Some(T)
}
```  
紧接着我们将看到一个值的类型是 `.Some(T)` 或者是 `.None` 会怎样造成函数作用的不同。我们先来谈谈 Functors！

## Functors

当一个值被封装到盒子里，一个普通的函数无法作用于它：

![](/assets/postAssets/2016/6941baebgw1ev5g0o5ql5j20580483yk.webp)

这个是就是 `map` 的由来（在 Haskell 是 `fmap`）。`map` 知道如何使用函数处理数据类型。例如，你想要使用一个函数，将 `.Some(2)` 加 3。使用 `map`:
```swift  
func  plusThree(addend:  Int)  ->  Int  {

  return  addend  +  3

}

Optional.Some(2).map(plusThree)

// => .Some(5)
```  
或者用更简洁的语法，使用 Swift 的 autoclosure：
```swift  
Optional.Some(2).map  {  $0  +  3  }

// => .Some(5)
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0moduhj20jt06j753.webp)

**砰!** `map` 的作用我们看到了，但是它是怎么做到的？

## 到底什么是 Functor？

任意定义了 `map` （ Haskell 中的 `fmap`）如何作用于自己的类型都是 Functor，`map`是这样作用的：

![](/assets/postAssets/2016/6941baebgw1ev5g0n61hij20j005zwfi.webp)

所以我们可以这么做
```swift  
Optional.Some(2).map  {  $0  +  3  }
// => .Some(5)
```  
`map` 神奇地使函数起了作用，因为 `Optional` 是一个 Functor。它表明了 `map` 是如何应用 `Some` 和 `None`。
```swift  
func mapU>(f: T -> U) -> U? {
  switch  self  {
  case  .Some(let  x):  return  f(x)
  case  .None:  return  .None
}
```  
`Optional.Some(2).map { $0 + 3 }`:

这里是当我们写下 `Optional.Some(2).map { $0 + 3 }` 背后所发生的：

![](/assets/postAssets/2016/6941baebgw1ev5g0nony6j20qb07h0u9.webp)

所以我们就像在说，`map`，请将 `{ $0 + 3 }`作用与 `.None` 上？

![](/assets/postAssets/2016/6941baebgw1ev5g0kt3hgj20gn05jaag.webp)
```swift  
Optional.None.map  {  $0  +  3  }
// => .None
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0ix0wtj205k05kjrp.webp)

就像黑客帝国中的 Morpheus，`map` 知道要做什么；开始时是 `None`，结束也是 `None`！`map`是一种禅。现在你可以理解为什么 `Optional` 类型的存在。举个例子，对于没有 `Optional`类型的语言，比如 Ruby，对于一条数据库记录是这么工作的：
```swift  
let post  =  Post.findByID(1)
if  post  !=  nil  {
  return  post.title
}  else  {
  return  nil
}
```  
但是用 Swift 使用 `Optional` 仿函数：
```swift  
findPost(1).map(getPostTitle)
```  
如果 `findPost(1)` 返回 post，我们会通过 `getPostTitle` 得到 title。如果他返回 `None`，我们会返回 `None`!

我们甚至可以定义一个 infix 操作符给 `map`,`<^>` (在 Haskell 为`<$>`），然后这么做：
```swift  
infix  operator  <^>  {  associativity  left  }
func <^><T,  U>(f:  T  ->  U,  a:  T?)  ->  U?  {
  return  a.map(f)
}
getPostTitle  <^>  findPost(1)
```  
> **注意：**我们使用`<^>`，因为`<$>`不能编译通过。

这里有另一个例子：对 array 使用函数会怎么样呢？

![](/assets/postAssets/2016/6941baebgw1ev5g0kc6wuj20r80a1tac.webp)

Array 也是 functor！

好了，最后一个例子：给函数应用另外一个函数会怎么样？
```swift  
map({  $0  +  2  },  {  $0  +  3  })
// => ???
```  
这个是函数：

![](/assets/postAssets/2016/6941baebgw1ev5g0lsz47j208905v0sz.webp)

这个是一个函数应用另外一个函数：

![](/assets/postAssets/2016/6941baebgw1ev5g0jvelcj20fz089t9m.webp)

获得结果是另外一个函数！
```swift  
typealias  IntFunction  =  Int  ->  Int
func  map(f:  IntFunction,  _  g:  IntFunction)  ->  IntFunction  {
  return  {  x  in  f(g(x))  }
}
let  foo  =  map({  $0  +  2  },  {  $0  +  3  })
foo(10)
// => 15
```  
所以函数也是 Functor！当你对函数使用 fmap，你只是在做函数组装！

## Applicatives

Applicative 将提升到另一个层级。使用 applicative，我们的值被封装在一个上下文中，就像 Functor：

![](/assets/postAssets/2016/value_and_context.webp)

但是我们的函数也被封装在一个上下文中！

![](/assets/postAssets/2016/6941baebgw1ev5g0l82mhj203r048jrf.webp)

我们继续深入，applicative 不是开玩笑的。不同于 Haskell，Swift 还并没有内置处理 applicative 的方法。但是添加一个非常简单，我们可以定义一个 `apply` 函数来支持各种类型，从而支持 applicative，applicative 知道如何将一个封装在上下文之中的函数作用于封装在同样上下文之中的值：
```swift  
extension  Optional  {
  func  apply<U>(f:  (T  ->  U)?)  ->  U?  {
    switch  f  {
      case  .Some(let  someF):  return  self.map(someF)
      case  .None:  return  .None
    }
  }
}

extension  Array  {
  func  apply<U>(fs:  [Element  ->  U])  ->  [U]  {
    var  result  =  [U]()
      for  f  in  fs  {
        for  element in  self.map(f)  {
          result.append(element)
        }
      }
      return  result
    }
}
```  
如果 `self` 和函数都是 `.Some`，那么函数将被应用于解包的值，否者，`.None` 被返回。*注意因为 optional 类型是被定义为`Optional<T>`，我们只需要在 `apply` 声明处声明泛型 `U`*

我们也可以定义 `<*>`，做同样的使用：
```swift  
infix  operator  <*>  {  associativity  left  }
func  <*><T,  U>(f:  (T  ->  U)?,  a:  T?)  ->  U?  {
  return  a.apply(f)
}

func  <*><T,  U>(f:  [T  ->  U],  a:  [T])  ->  [U]  {
  return  a.apply(f)
}
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0hwefpj20pv09m0ut.webp)

例子：
```swift  
Optional.Some({  $0  +  3  })  <*>  Optional.Some(2)
// => 5
```  
使用 `<*>` 可以产生有趣的情况，比如：
```swift  
[  {  $0  +  3  },  {  $0  *  2  }  ]  <*>  [1,  2,  3]
// => [ 4, 5, 6, 2, 4, 6 ]
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0igq4lj20ni0dwgn1.webp)

> **注意:**Haskell 版的原文章展示了 applicative 比 functor 强大，它允许函数应用多个参数。而这个对于 Swift 是不可行的，但是我们可以通过使用[柯里函数 (Currying)](https://en.wikipedia.org/wiki/Currying)来定义我们想要的函数。

这里是一些可以用 applicative 而不能使用 functor 的例子。如何应用一个有两个参数的函数到两个封装好的值？
```swift  
func  curriedAddition(a:  Int)(b:  Int)  ->  Int  {
  return  a  +  b
}

curriedAddition  <^>  Optional(2)  <^>  Optional(3)
// => COMPILER ERROR: Value of optional type '(Int -> Int)? not unwrapped; did you mean to use '!' or '??'
```  
Applicatives:
```swift  
curriedAddition  <^>  Optional(2)  <*>  Optional(3)
```  
`Applicative` 把 `Functor` 推到一旁，说，“大男孩可以使用 function 处理多个参数。坐拥 `<^>` 和 `<*>`，我可以生成任意函数处理多个解包的值，然后然后将所有值打包，输出一个封装的值，哈哈哈！”
```swift  
func  curriedTimes(a:  Int)(b:  Int)  ->  Int  {
  return  a  *  b
}
curriedTimes  <^>  Optional(5)  <*>  Optional(3)
```  
## Monads

Monads 添加一种新的方式。

Functor 为封装的值应用一个函数：

![](/assets/postAssets/2016/6941baebgw1ev5g0japr3j205802r3yi.webp)

Applicatives 为封装的值应用一个封装的函数：

![](/assets/postAssets/2016/6941baebgw1ev5g0h90cej209704e0t3.webp)

Monads 为封装的值，应用一个返回封装值的函数。Monads 有个函数 `|`（在 Haskell 为 >>=）（发音为 “bind”）来处理这个。

Monads 有个函数 `flatMap`（在 Haskell 为 `liftM`）能处理这个。那我们可以给它定义一个 infix 操作符 `>>-` （在 Haskell 为`>>=`）。
```swift  
infix  operator  >>-  {  associativity  left  }
func  >>-<T,  U>(a:  T?,  f:  T  ->  U?)  ->  U?  {
  return  a.flatMap(f)
}
```  
> **注意：**不像 `<$>`, `>>=` 可以编译。我决定用 `>>-` 是由于这个库 [Runes](https://github.com/thoughtbot/Runes)，它提供在 Swift 中的 monadic 函数操作符，这很有可能在未来会成为一个标准。

![](/assets/postAssets/2016/context.webp)

只是个 monad

假定 `half` 是一个函数，只能处理基本数值类型：
```swift  
func  half(a:  Int)  ->  Int?  {
  return  a  %  2  ==  0  ?  a  /  2  :  .None
}
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0e54s4j208906574m.webp)

如果要让处理封装的值呢？

![](/assets/postAssets/2016/6941baebgw1ev5g0ej85uj204w05e0su.webp)

我们需要使用 `>>-`（在 Haskell 为 `>>=`）将封装的值强塞到这个函数里。这里是 `>>-` 的图片：

![](/assets/postAssets/2016/6941baebgw1ev5g0gui81j20bz08ct8p.webp)

这里是它如何工作：
```swift  
Optional(3)  >>-  half
// .None
Optional(4)  >>-  half
// 2
Optional.None  >>-  half
// .None
```  
内部发生了什么？让我们来看下 `>>-` 的声明：
```swift  
// For Optional
func  >>-<T,  U>(a:  T?,  f:  T  ->  U?)  ->  U?
// For Array
func  >>-<T,  U>(a:  [T],  f:  T  ->  [U])  ->  [U]
```  
![](/assets/postAssets/2016/6941baebgw1ev5g0dhmv9j20gt06u0tq.webp)

因此 `Optional` 是一个 Monad。这里是 `.Some(3)` 的处理过程！

![](/assets/postAssets/2016/6941baebgw1ev5g0ftndnj20g40jtwgq.webp)

如果你传得时 `.None`，它会更简单：

![](/assets/postAssets/2016/6941baebgw1ev5g0g9rctj20by0ed3zl.webp)

你还可以将调用连接起来：
```swift  
Optional(20)  >>-  half  >>-  half  >>-  half
// => .None
```  
![](/assets/postAssets/2016/6941baebgw1ev5gfgxyq4j20820xcwgh.webp)

> 注意：原文章描述 Haskell 的 `IO`Monad。Swift 并没有这个，所以跳过。

## 总结

1. functor 是一种实现了 `map` 的数据类型；
2. applicative 是一个种实现了 `apply` 的数据类型；
3. monad 是一种实现了 `flatMap` 的数据类型
4. `Optional` 实现了 `map` 和 `flatMap`，加上我们可以实现 `apply` 来拓展，因此它是一个 functor，applicative, 和 monad。

那么它们三者的区别是什么呢？

![](/assets/postAssets/2016/6941baebgw1ev5g0cyrgxj20og07gq4f.webp)

* **functors**:通过 `map` 对封装的值使用了函数.
* **applicatives**: 通过使用 `apply` 对封装的值使用封装了的函数，如果你定义了的话.
* **monads**: 使用一个返回封装的值的函数，放到 `flatMap` 中处理，返回一个封装后的值.

## 转者云:

其实总的来说即三点  
functor(函子)  
释义: 一个函数到一个上下文中的值, 且函数为接收一个普通值并且返回一个普通值  
applicative	(加强函子)  
释义: 一个上下文中的函数到一个上下文中的值  
monad(单子)  
释义: 一个函数到一个上下文中的值,	且函数为接收一个普通值但是返回一个在上下文中的值  




