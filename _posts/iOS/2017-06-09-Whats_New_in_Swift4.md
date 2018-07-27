---  
layout: post  
title: What’s New in Swift 4?  
category: iOS  
tags: Swift Define  
keywords: Jekyll,Github  
description: 
---  

__[Posted by raywenderlich](https://www.raywenderlich.com/163857/whats-new-swift-4)__  

*Note:* This tutorial uses the Swift 4 version bundled into Xcode 9 beta 1.  

[![Swift 4](/assets/postAssets/2017/WhatsNewSwift4-feature-1-250x250.webp)](https://koenig-media.raywenderlich.com/uploads/2017/WhatsNewSwift4-feature-1.webp)  

Swift 4 is the latest major release from Apple scheduled to be out of beta in the fall of 2017\. Its main focus is to provide source compatibility with Swift 3 code as well as working towards ABI stability.  

This article highlights changes to Swift that will most significantly impact your code. And with that, let’s get started!  

## Getting Started  

Swift 4 is included in Xcode 9\. You can download the latest version of Xcode 9 from Apple’s [developer portal](https://developer.apple.com/download/) (you must have an active developer account). Each Xcode beta will bundle the latest Swift 4 snapshot at the time of release.  

As you’re reading, you’ll notice links in the format of *[SE-xxxx]*. These links will take you to the relevant Swift Evolution proposal. If you’d like to learn more about any topic, make sure to check them out.  

I recommend trying each Swift 4 feature or update in a playground. This will help cement the knowledge in your head and give you the ability to dive deeper into each topic. Play around with the examples by trying to expand/break them. Have fun with it!  

*Note:* This article will be updated for each Xcode beta. If you use a different Swift snapshot, the code here is not guaranteed to work.  

## Migrating to Swift 4  

The migration from Swift 3 to 4 will be much less cumbersome than from 2.2 to 3\. In general, *most* changes are additive and shouldn’t need a ton of personal touch. Because of this, the Swift migration tool will handle the majority of changes for you.  

Xcode 9 simultaneously supports both Swift 4 as well as an intermediate version of Swift 3 in Swift 3.2\. Each target in your project can be either Swift 3.2 or Swift 4 which lets you migrate piece by piece if you need to. Converting to Swift 3.2 isn’t *entirely* free, however – you may need to update parts of your code to be compatible with new SDKs, and because Swift is not yet ABI stable you will need to recompile your dependencies with Xcode 9.  

When you’re ready to migrate to Swift 4, Xcode once again provides a migration tool to help you out. In Xcode, you can navigate to *Edit/Convert/To Current Swift Syntax…* to launch the conversion tool.  

After selecting which targets you want to convert, Xcode will prompt you for a preference on Objective-C inferencing. Select the recommended option to reduce your binary size by limiting inferencing (for more on this topic, check out the [Limiting @objc Inference](https://www.raywenderlich.com/163857/whats-new-swift-4#objc) below)  

![](/assets/postAssets/2017/Screen-Shot-2017-06-07-at-8.29.57-AM.webp)  

To better understand what changes to expect in your code, we’ll first cover API changes in Swift 4.  

## API Changes  

Before jumping right into additions introduced in Swift 4, let’s first take a look at what changes/improvements it makes to existing APIs.  

### Strings  

`String` is receiving a lot of well deserved love in Swift 4\. This proposal contains many changes, so let’s break down the biggest. [[SE-0163]](https://github.com/apple/swift-evolution/blob/master/proposals/0163-string-revision-1.md):  

In case you were feeling nostalgic, strings are once again collections like they were pre Swift 2.0\. This change removes the need for a `characters` array on `String`. You can now iterate directly over a `String`object:  

```swift  
let galaxy = "Milky Way 🐮"  
for char in galaxy {  
  print(char)  
}  
```  

![Yes!](/assets/postAssets/2017/Freddie.webp)  

Not only do you get logical iteration through `String`, you also get all the bells and whistles from `Sequence`and `Collection`:  

```swift  
galaxy.count       // 11  
galaxy.isEmpty     // false  
galaxy.dropFirst() // "ilky Way 🐮"  
String(galaxy.reversed()) // "🐮 yaW ykliM"  

// Filter out any none ASCII characters  
galaxy.filter { char in  
  let isASCII = char.unicodeScalars.reduce(true, { $0 && $1.isASCII })  
  return isASCII  
} // "Milky Way "  
```  

The ASCII example above demonstrates a small improvement to `Character`. You can now access the `UnicodeScalarView` directly from `Character`. Previously, you needed to instantiate a new `String` [[SE-0178]](https://github.com/apple/swift-evolution/blob/master/proposals/0178-character-unicode-view.md).  

Another addition is `StringProtocol`. It declares most of the functionality previously declared on `String`. The reason for this change is to improve how slices work. Swift 4 adds the `Substring` type for referencing a subsequence on `String`.  

Both `String` and `Substring` implement `StringProtocol` giving them almost identical functionality:  

```swift  
// Grab a subsequence of String  
let endIndex = galaxy.index(galaxy.startIndex, offsetBy: 3)  
var milkSubstring = galaxy[galaxy.startIndex...endIndex]   // "Milk"  
type(of: milkSubstring)   // Substring.Type  

// Concatenate a String onto a Substring  
milkSubstring += 🍼     // "Milk🍼"  

// Create a String from a Substring  
let milkString = String(milkSubstring) // "Milk🍼  
```  

Another great improvement is how `String` interprets grapheme clusters. This resolution comes from the adaptation of Unicode 9\. Previously, unicode characters made up of multiple code points resulted in a `count` greater than 1\. A common situation where this happens is an emoji with a selected skin-tone. Here are a few examples showing the before and after behavior:  

```swift  
"👩‍".count // Now: 1, Before: 2  
"👍🏽".count // Now: 1, Before: 2  
"👨‍❤️‍💋‍👨".count // Now: 1, Before, 4  
```  

This is only a subset of the changes mentioned in the [String Manifesto](https://github.com/apple/swift/blob/master/docs/StringManifesto.md). You can read all about the original motivations and proposed solutions you’d expect to see in the future.  

### Dictionary and Set  

As far as `Collection` types go, `Set` and `Dictionary` aren’t always the most intuitive. Lucky for us, the Swift team gave them some much needed love with [[SE-0165]](https://github.com/apple/swift-evolution/blob/master/proposals/0165-dict.md).  

*Sequence Based Initialization*  
First on the list is the ability to create a dictionary from a sequence of key-value pairs (tuple):  

```swift  
let nearestStarNames = ["Proxima Centauri", "Alpha Centauri A", "Alpha Centauri B", "Barnard's Star", "Wolf 359"]  
let nearestStarDistances = [4.24, 4.37, 4.37, 5.96, 7.78]  

// Dictionary from sequence of keys-values  
let starDistanceDict = Dictionary(uniqueKeysWithValues: zip(nearestStarNames, nearestStarDistances)) 
// ["Wolf 359": 7.78, "Alpha Centauri B": 4.37, "Proxima Centauri": 4.24, "Alpha Centauri A": 4.37, "Barnard's Star": 5.96]  
```  

*Duplicate Key Resolution*  
You can now handle initializing a dictionary with duplicate keys any way you’d like. This helps avoid overwriting key-value pairs without any say in the matter:  

```swift  
// Random vote of people's favorite stars  
let favoriteStarVotes = ["Alpha Centauri A", "Wolf 359", "Alpha Centauri A", "Barnard's Star"]  

// Merging keys with closure for conflicts  
let mergedKeysAndValues = Dictionary(zip(favoriteStarVotes, repeatElement(1, count: favoriteStarVotes.count)), uniquingKeysWith: +) // ["Barnard's Star": 1, "Alpha Centauri A": 2, "Wolf 359": 1]  
```  

The code above uses `zip` along with the shorthand `+` to resolve duplicate keys by adding the two conflicting values.  

*Note:* If you are not familiar with `zip`, you can quickly learn about it in Apple’s [Swift Documentation](https://developer.apple.com/documentation/swift/1541125-zip)  

*Filtering*  
Both `Dictionary` and `Set` now have the ability to filter results into a new object of the original type:  

```swift  
// Filtering results into dictionary rather than array of tuples  
let closeStars = starDistanceDict.filter { $0.value "Proxima Centauri": 4.24, "Alpha Centauri A": 4.37, "Alpha Centauri B": 4.37]  

*Dictionary Mapping*  
`Dictionary` gained a very useful method for directly mapping its values:  

// Mapping values directly resulting in a dictionary  
let mappedCloseStars = closeStars.mapValues { "\($0)" }  
mappedCloseStars // ["Proxima Centauri": "4.24", "Alpha Centauri A": "4.37", "Alpha Centauri B": "4.37"]  
```  

*Dictionary Default Values*  
A common practice when accessing a value on `Dictionary` is to use the nil coalescing operator to give a default value in case the value is `nil`. In Swift 4, this becomes much cleaner and allows you to do some awesome in line mutation:  

```swift  
// Subscript with a default value  
let siriusDistance = mappedCloseStars["Wolf 359", default: "unknown"] // "unknown"  

// Subscript with a default value used for mutating  
var starWordsCount: [String: Int] = [:]  
for starName in nearestStarNames {  
  let numWords = starName.split(separator: " ").count  
  starWordsCount[starName, default: 0] += numWords // Amazing 
}  
starWordsCount // ["Wolf 359": 2, "Alpha Centauri B": 3, "Proxima Centauri": 2, "Alpha Centauri A": 3, "Barnard's Star": 2]  
```  

Previously this type of mutation would need wrapping in a bloated `if-let` statement. In Swift 4 it's possible all in a single line!  

*Dictionary Grouping*  
Another amazingly useful addition is the ability to initialize a `Dictionary` from a `Sequence` and to group them into buckets:  

```swift  
// Grouping sequences by computed key  
let starsByFirstLetter = Dictionary(grouping: nearestStarNames) { $0.first! }  

// ["B": ["Barnard's Star"], "A": ["Alpha Centauri A", "Alpha Centauri B"], "W": ["Wolf 359"], "P": ["Proxima Centauri"]]  
```  

This comes in handy when grouping data by a specific pattern.  

*Reserving Capacity*  
Both `Sequence` and `Dictionary` now have the ability to explicitly reserve capacity.  

```swift  
// Improved Set/Dictionary capacity reservation  
starWordsCount.capacity  // 6  
starWordsCount.reserveCapacity(20) // reserves at _least_ 20 elements of capacity  
starWordsCount.capacity // 24  
```  

Reallocation can be an expensive task on these types. Using `reserveCapacity(_:)` is an easy way to improve performance when you have an idea how much data it needs to store.  

That was a ton of info, so definitely check out both types and look for ways to use these additions to spice up your code.  

### Private Access Modifier  

An element of Swift 3 some haven't been too fond of was the addition of `fileprivate`. In theory, it's great, but in practice its usage can often be confusing. The goal was to use `private` within the member itself, and to use `fileprivate` rarely in situations where you wanted to share access across members within the same file.  

The issue is that Swift encourages using extensions to break code into logical groups. Extensions are considered outside of the original member declaration scope, which results in the extensive need for `fileprivate`.  

Swift 4 realizes the original intent by sharing the same access control scope between a type and any extension on said type. This only holds true within the same source file [[SE-0169]](https://github.com/apple/swift-evolution/blob/master/proposals/0169-improve-interaction-between-private-declarations-and-extensions.md):  

```swift  
struct SpaceCraft {  
  private let warpCode: String  

  init(warpCode: String) {  
    self.warpCode = warpCode  
  }  
}  

extension SpaceCraft {  
  func goToWarpSpeed(warpCode: String) {  
    if warpCode == self.warpCode { // Error in Swift 3 unless warpCode is fileprivate  
      print("Do it Scotty!")  
    }  
  }  
}  

let enterprise = SpaceCraft(warpCode: "KirkIsCool")  
//enterprise.warpCode  // error: 'warpCode' is inaccessible due to 'private' protection level  
enterprise.goToWarpSpeed(warpCode: "KirkIsCool") // "Do it Scotty!"  
```  

This allows you to use `fileprivate` for its intended purpose rather than as a bandaid to code organization.  

## API Additions  

Now let's take a look at the new shinny features of Swift 4\. These changes *shouldn't* break your existing code as they are simply additive.  

### Archival and Serialization  

![Cereal Guy](/assets/postAssets/2017/cereal-guy-250x250.webp)  

Up to this point in Swift, to serialize and archive your custom types you'd have to jump through a number of hoops. For `class` types you'd need to subclass `NSObject`and implement the `NSCoding` protocol.  

Value types like `struct` and `enum` required a number of hacks like creating a sub object that could extend `NSObject` and `NSCoding`.  

Swift 4 solves this issue by bringing serialization to all three Swift types [[SE-0166]](https://github.com/apple/swift-evolution/blob/master/proposals/0166-swift-archival-serialization.md):  

```swift  
struct CuriosityLog: Codable {  
  enum Discovery: String, Codable {  
    case rock, water, martian  
  }  

  var sol: Int  
  var discoveries: [Discovery]  
}  

// Create a log entry for Mars sol 42  
let logSol42 = CuriosityLog(sol: 42, discoveries: [.rock, .rock, .rock, .rock])  
```  

In this example you can see that the only thing required to make a Swift type `Encodable` and `Decodable` is to implement the `Codable` protocol. If all properties are `Codable`, the protocol implementation is automatically generated by the compiler.  

To actually encode the object, you'll need to pass it to an encoder. Swift encoders are being actively implemented in Swift 4\. Each encodes your objects according to different schemes [[SE-0167]](https://github.com/apple/swift-evolution/blob/master/proposals/0167-swift-encoders.md) (*Note:* Part of this proposal is still in development):  

```swift  
let jsonEncoder = JSONEncoder() // One currently available encoder  

// Encode the data  
let jsonData = try jsonEncoder.encode(logSol42)  
// Create a String from the data  
let jsonString = String(data: jsonData, encoding: .utf8) // "{"sol":42,"discoveries":["rock","rock","rock","rock"]}"  
```  

This took an object and automatically encoded it as a JSON object. Make sure to check out the properties `JSONEncoder` exposes to customize its output.  

The last part of the process is to decode the data back into a concrete object:  

```swift  
let jsonDecoder = JSONDecoder() // Pair decoder to JSONEncoder  

// Attempt to decode the data to a CuriosityLog object  
let decodedLog = try jsonDecoder.decode(CuriosityLog.self, from: jsonData)  
decodedLog.sol         // 42  
decodedLog.discoveries // [rock, rock, rock, rock]  
```  

With Swift 4 encoding/decoding you get the type safety expected in Swift without relying on the overhead and limitations of `@objc` protocols.  

### Key-Value Coding  

Up to this point you could hold reference to functions without invoking them because functions are closures in Swift. What you couldn't do is hold reference to properties without actually accessing the underlying data held by the property.  

A very exciting addition to Swift 4 is the ability to reference key paths on types to get/set the underlying value of an instance [[SE-0161]](https://github.com/apple/swift-evolution/blob/master/proposals/0161-key-paths.md):  

```swift  
struct Lightsaber {  
  enum Color {  
    case blue, green, red  
  }  
  let color: Color  
}  

class ForceUser {  
  var name: String  
  var lightsaber: Lightsaber  
  var master: ForceUser?  

  init(name: String, lightsaber: Lightsaber, master: ForceUser? = nil) {  
    self.name = name  
    self.lightsaber = lightsaber  
    self.master = master  
  }  
}  

let sidious = ForceUser(name: "Darth Sidious", lightsaber: Lightsaber(color: .red))  
let obiwan = ForceUser(name: "Obi-Wan Kenobi", lightsaber: Lightsaber(color: .blue))  
let anakin = ForceUser(name: "Anakin Skywalker", lightsaber: Lightsaber(color: .blue), master: obiwan)  
```  

Here you're creating a few instances of force users by setting their name, lightsaber, and master. To create a key path, you simply use a back-slash followed by the property you're interested in:  

```swift  
// Create reference to the ForceUser.name key path  
let nameKeyPath = \ForceUser.name  

// Access the value from key path on instance  
let obiwanName = obiwan[keyPath: nameKeyPath]  // "Obi-Wan Kenobi"  
```  

In this instance, you're creating a key path for the `name` property of `ForceUser`. You then use this key path by passing it to the new subscript `keyPath`. This subscript is now available on every type by default.  

Here are more examples of ways to use key paths to drill down to sub objects, set properties, and build off key path references:  

```swift  
// Use keypath directly inline and to drill down to sub objects  
let anakinSaberColor = anakin[keyPath: \ForceUser.lightsaber.color]  // blue  

// Access a property on the object returned by key path  
let masterKeyPath = \ForceUser.master  
let anakinMasterName = anakin[keyPath: masterKeyPath]?.name  // "Obi-Wan Kenobi"  

// Change Anakin to the dark side using key path as a setter  
anakin[keyPath: masterKeyPath] = sidious  
anakin.master?.name // Darth Sidious  

// Note: not currently working, but works in some situations  
// Append a key path to an existing path  
//let masterNameKeyPath = masterKeyPath.appending(path: \ForceUser.name)  
//anakin[keyPath: masterKeyPath] // "Darth Sidious"  
```  

The beauty of key paths in Swift is that they are strongly typed! No more of that Objective-C string style mess!  

### Multi-line String Literals  

A very common feature to many programming languages is the ability to create a multi-line string literal. Swift 4 adds this simple but useful syntax by wrapping text within three quotes [[SE-0168]](https://github.com/apple/swift-evolution/blob/master/proposals/0168-multi-line-string-literals.md):  

```swift  
let star = "⭐️"  
let introString = """  
  A long time ago in a galaxy far,  
  far away....  

  You could write multi-lined strings  
  without "escaping" single quotes.  

  The indentation of the closing quotes  
       below deside where the text line  
  begins.  

  You can even dynamically add values  
  from properties: \(star)  
  """  
print(introString) // prints the string exactly as written above with the value of star  
```  

This is extremely useful when building XML/JSON messages or when building long formatted text to display in your UI.  

### One-Sided Ranges  

To reduce verbosity and improve readability, the standard library can now infer start and end indices using one-sided ranges [[SE-0172]](https://github.com/apple/swift-evolution/blob/master/proposals/0172-one-sided-ranges.md).  

One way this comes in handy is creating a range from an index to the start or end index of a collection:  

```swift  
// Collection Subscript  
var planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]  
let outsideAsteroidBelt = planets[4...] // Before: planets[4..  
let firstThree = planets[..4]          // Before: planets[planets.startIndex..  
```  

As you can see, one-sided ranges reduce the need to explicitly specify either the start or end index.  

*Infinite Sequence*  
They also allow you to define an infinite `Sequence` when the start index is a countable type:  

```swift  
// Infinite range: 1...infinity  
var numberedPlanets = Array(zip(1..., planets))  
print(numberedPlanets) // [(1, "Mercury"), (2, "Venus"), ..., (8, "Neptune")]  

planets.append("Pluto")  
numberedPlanets = Array(zip(1..., planets))  
print(numberedPlanets) // [(1, "Mercury"), (2, "Venus"), ..., (9, "Pluto")]  
```  

*Pattern Matching*  
Another great use for one-sided ranges is pattern matching:  

```swift  
// Pattern matching  

func temperature(planetNumber: Int) {  
  switch planetNumber {  
  case ...2: // anything less than or equal to 2  
    print("Too hot")  
  case 4...: // anything greater than or equal to 4  
    print("Too cold")  
  default:  
    print("Justtttt right")  
  }  
}  

temperature(planetNumber: 3) // Earth  
```  

### Generic Subscripts  

Subscripts are an important part of making data types accessible in an intuative way. To improve their usefulness, subscripts can now be generic [[SE-0148]](https://github.com/apple/swift-evolution/blob/master/proposals/0148-generic-subscripts.md):  

```swift  
struct GenericDictionary {  
  private var data: [Key: Value]  

  init(data: [Key: Value]) {  
    self.data = data  
  }  

  subscript(key: Key) -> T? {  
    return data[key] as? T  
  }  
}  
```  

In this example, the return type is generic. You can then use this generic subscript like so:  

```swift  
// Dictionary of type: [String: Any]  
var earthData = GenericDictionary(data: ["name": "Earth", "population": 7500000000, "moons": 1])  

// Automatically infers return type without "as? String"  
let name: String? = earthData["name"]  

// Automatically infers return type without "as? Int"  
let population: Int? = earthData["population"]  
```  

Not only can the return type be generic, but the actual subscript type can be generic as well:  

```swift  
extension GenericDictionary {  
  subscriptKeys: Sequence>(keys: Keys) -> [Value] where Keys.Iterator.Element == Key {  
    var values: [Value] = []  
    for key in keys {  
      if let value = data[key] {  
        values.append(value)  
      }  
    }  
    return values  
  }  
}  

// Array subscript value  
let nameAndMoons = earthData[["moons", "name"]]        // [1, "Earth"]  
// Set subscript value  
let nameAndMoons2 = earthData[Set(["moons", "name"])]  // [1, "Earth"]  
```  

In this example, you can see that passing in two different `Sequence` type (`Array` and `Set`) results in an array of their respective values.  

## Miscellaneous  

That handles the biggest changes in Swift 4\. Now let's go a little more rapidly through some of the smaller bits and pieces.  

### MutableCollection.swapAt(_:_:)  

`MutableCollection` now has the mutating method `swapAt(_:_:)` which does just as it sounds; swap the values at the given indices [[SE-0173]](https://github.com/apple/swift-evolution/blob/master/proposals/0173-swap-indices.md):  

```swift  
// Very basic bubble sort with an in-place swap  
func bubbleSort(_ array: [T]) -> [T] {  
  var sortedArray = array  
  for i in 0..count - 1 {  
    for j in 1..count {  
      if sortedArray[j-1] > sortedArray[j] {  
        sortedArray.swapAt(j-1, j) // New MutableCollection method  
      }  
    }  
  }  
  return sortedArray  
}  

bubbleSort([4, 3, 2, 1, 0]) // [0, 1, 2, 3, 4]  
```  

### Associated Type Constraints  

You can now constrain associated types using the `where` clause [[SE-0142]](https://github.com/apple/swift-evolution/blob/master/proposals/0142-associated-types-constraints.md):  

```swift  
protocol MyProtocol {  
  associatedtype Element  
  associatedtype SubSequence : Sequence where SubSequence.Iterator.Element == Iterator.Element  
}  
```  

Using protocol constraints, many `associatedtype` declarations could constrain their values directly without having to jump through hoops.  

### Class and Protocol Existential  

A feature that has finally made it to Swift from Objective-C is the ability to define a type that conforms to a class as well as a set of protocols [[SE-0156]](https://github.com/apple/swift-evolution/blob/master/proposals/0156-subclass-existentials.md):  

```swift  
protocol MyProtocol { }  
class View { }  
class ViewSubclass: View, MyProtocol { }  

class MyClass {  
  var delegate: (View & MyProtocol)?  
}  

let myClass = MyClass()  
//myClass.delegate = View() // error: cannot assign value of type 'View' to type '(View & MyProtocol)?'  
myClass.delegate = ViewSubclass()  
```  

### Limiting @objc Inference  

To expose or your Swift API to Objective-C, you use the `@objc` compiler attribute. In many cases the Swift compiler inferred this for you. The three main issues with mass inference are:  

1. Potential for a significant increase to your binary size  
2. Knowing when `@objc` will  

be inferred isn't obvious  

4. The increased chance of inadvertently creating an Objective-C selector collisions.  

Swift 4 takes a stab at solving this by limiting the inference of `@objc` [[SE-0160]](https://github.com/apple/swift-evolution/blob/master/proposals/0160-objc-inference.md). This means that you'll need to use `@objc` explicitly in situations where you want the full dynamic dispatch capabilities of Objective-C.  

A few examples of where you'll need to make these changes include `private` methods, `dynamic` declarations, and any methods of `NSObject` subclasses.  

### NSNumber Bridging  

There have been many funky behaviors between `NSNumber` and Swift numbers that have been haunting the language for too long. Lucky for us, Swift 4 squashes those bugs [[SE-0170]](https://github.com/apple/swift-evolution/blob/master/proposals/0170-nsnumber_bridge.md).  

Here's an example demonstrating an example of the behavior:  

```swift  
let n = NSNumber(value: 999)  
let v = n as? UInt8 // Swift 4: nil, Swift 3: 231  
```  

The weird behavior in Swift 3 shows that if the number overflows, it simply starts over from 0\. In this example, 999 % 2^8 = 231.  

Swift 4 solves the issue by forcing optional casting to return a value only if the number can be safely expressed within the containing type.  

## Swift Package Manager  

There's been a number of updates to the Swift Package Manager over the last few months. Some of the biggest changes include:  

* Sourcing dependencies from a branch or commit hash  
* More control of acceptable package versions  
* Replaces unintuitive pinning commands with a more common resolve pattern  
* Ability to define the Swift version used for compilation  
* Specify the location of source files for each target  

These are all big steps towards getting SPM where it needs to be. There's still a long road ahead for the SPM, but it's one that we can all help shape by staying active on the proposals.  

For a great overview of what proposals have been recently addressed check out the [Swift 4 Package Manager Update](https://lists.swift.org/pipermail/swift-build-dev/Week-of-Mon-20170605/001019.html).  

## Still In Progress  

At the time of writing this article, there are still 15 accepted proposals in the queue. If you want a sneak peak on what's coming down the line, check out the [Swift Evolution Proposals](https://apple.github.io/swift-evolution/) and filter by *Accepted*.  

Rather than walking through them all now, we'll keep this post updated with each new beta version of Xcode 9 .  

## 转者云:  
1.Strings变成collections, 多了些封装, 少了些真意  
2.Dictionary默认值, 对于这个 ?? 这个符号有知道这事吗  
3.Dictionary的Capacity 终于等到了这个接口  
4.Private Access我不发表意见 只唱歌:当初是你要分开, 分开就分开, 如今你又要把我哄回来...  
5.Codable又挣脱一个oc的枷锁  
6.kvc可以再牛逼点,我看好你  
7.Multi-line String据我所知,你是唯一这么搞的, 不过看起来不错  
8.One-Sided Ranges终于可以少敲几次键盘了  
9.Generic Subscripts这功能早该上了  
10.Class and Protocol Existential这个功能应该会被玩儿坏 感觉不太好  

