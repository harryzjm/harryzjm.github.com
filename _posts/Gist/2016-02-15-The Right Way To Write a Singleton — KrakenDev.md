---  
layout: post  
title: The Right Way To Write a Singleton  
category: Gist  
tags: Swift  
keywords: Jekyll,Github  
description: 
---  

__Posted by [Hector Matos](http://krakendev.io/?author=5592eaffe4b08369d0205792)__  

Even though I've written about the woes of managing state in my previous post, sometimes there's just no way we can avoid it. One example of managing state is something we're all quite acquainted with - The Singleton. The problem we find in Swift is that there are SEVERAL ways of implementing them. But which way is the right way? In this post I'm going to show you the history of the singleton and then show you the right way to implement the singleton in Swift.  

If you want to see the right way to implement the singleton pattern in Swift along with proof of it's "right-ness", you can scroll to the bottom of the post and see it there. :)  

* * *  

# A Trip Down Memory Lane  

Swift is a natural evolution of Objective-C. In Objective-C, this is how we implemented the singleton:  

    @interface Kraken : NSObject  
    @end  

    @implementation Kraken  

    + (instancetype)sharedInstance {  
        static Kraken *sharedInstance = nil;  
        static dispatch_once_t onceToken;  

        dispatch_once(&amp;onceToken, ^{  
            sharedInstance = [[Kraken alloc] init];  
        });  
        return sharedInstance;  
    }  

    @end  

Now that we have that out of the way and we can see the basic structure of a singleton, let's lay out some rules so we understand what we're looking at:  

# Da Rules of Da Singleton, Mahn  

There are essentially three things to remember about the Singleton:  

* A singleton has to be **_unique_**. This is why it's called a **_single_**ton. There can only be one instance for the lifetime of the application it exists in. Singletons exist to give us singular global state. Such examples are `NSNotificationCenter`, `UIApplication`, and `NSUserDefaults`.  
* To maintain a singleton's _unique-ness_, the initializer of a singleton needs to be private. This helps to prevent other objects from creating instances of your singeton class themselves. Thank you to all who pointed that out to me :)  
* Because of rule #1, in order to have only one instance throughout the lifetime of the application, that means it needs to be **_thread-safe_**. Concurrency really sucks when you think about it, but simply put, if a singleton is built incorrectly in code, you can have two threads try to initialize a singleton at the same time which can potentially give you two separate instances of a singleton. This means that it's possible for it to not be unique unless we make it **_thread-safe_**. This means we want to wrap the initialization in a `dispatch_once` GCD block to make sure the initialization code only runs once at runtime.  

Being unique and initializing in one place in an app is easy. The important thing to remember for the rest of this post is that a singleton fulfill the much-harder-to-see `dispatch_once` rule.  

# Da Swift Singleton  

Since Swift 1.0, there have been several ways to create a singleton. These have been covered very extensively [here][7], [here][8], and [here][9]. But who likes clicking on links? SPOILER ALERT; There are four variations. Allow me to count the ways:  

## The Ugliest Way (A.K.A. The "Why Are You Still Coding In Swift If You're Just Going To Do This" Way)  

    class TheOneAndOnlyKraken {  
        class var sharedInstance: TheOneAndOnlyKraken {  
            struct Static {  
                static var onceToken: dispatch_once_t = 0  
                static var instance: TheOneAndOnlyKraken? = nil  
            }  
            dispatch_once(&amp;Static.onceToken) {  
                Static.instance = TheOneAndOnlyKraken()  
            }  
            return Static.instance!  
        }  
    }  

This way is a straight port of Objective-C's singleton implementation over to Swift. Ugly in my opinion because Swift was meant to be terse and expressive. Be better than the port guys. Be better. :P  

## The Struct Way (A.K.A. The "Old But Strangely Still Popular" Way)  

    class TheOneAndOnlyKraken {  
        class var sharedInstance: TheOneAndOnlyKraken {  
            struct Static {  
                static let instance = TheOneAndOnlyKraken()  
            }  
            return Static.instance  
        }  
    }  

This way was how we had to do it in Swift 1.0 since classes still didn't support static class variables back then. Structs, however, did support them! Because of these restrictions on static variables, we were forced into a model that looked like this. It's better than the straight Objective-C port but still not good enough. Funnily enough, I still see this method of writing singletons several months after the release of Swift 1.2. But more on that later.  

## The Global Variable Way (A.K.A. The "One Line Singleton")  

    private let sharedKraken = TheOneAndOnlyKraken()  
    class TheOneAndOnlyKraken {  
        class var sharedInstance: TheOneAndOnlyKraken {  
            return sharedKraken  
        }  
    }  

As of Swift 1.2, we gained **_access control specifiers_** and the ability to have **_static class members_**. This meant that we didn't have to have a global variable clutter the global namespace and we could now prevent namespace collisions. This version is a lot Swiftier in my opinion.  

Now at this point, you may be asking why we don't see `dispatch_once` in our struct or global variable implementations. Well according to Apple, both of these methods fulfills the `dispatch_once` clause I outlined above. Here's a quote straight from their [Swift Blog][9] that proves that they are wrapped in `dispatch_once` blocks behind the scenes:  

&gt; The lazy initializer for a global variable (also for static members of structs and enums) is run the first time that global is accessed, and is launched as `dispatch_once` to make sure that the initialization is atomic. This enables a cool way to use `dispatch_once` in your code: just declare a global variable with an initializer and mark it private.  

— Apple's Swift Blog  

That's all Apple gave us as far as official documentation goes. But this meant that all we had proof for was **_global_** variables and static members of structs/enums! At that point, the only 100% safe bet backed by Apple docs was using a global variable to lazily wrap singleton initialization in a `dispatch_once` block. BUT WHAT ABOUT OUR STATIC **_CLASS_** VARIABLES?!?!?!?  

This very question brings us to this next exciting section:  

## The Right Way A.K.A. "The One Line Singleton (Now With Proof!")  

    class TheOneAndOnlyKraken {  
        static let sharedInstance = TheOneAndOnlyKraken()  
    }  

So I've done a fair amount of research for this post. In fact, this post was inspired by a conversation we had at Capital One today due to the review of a PR that aimed at achieving proper singleton consistency in Swift across our app. We knew about this "right" method of writing singletons, but we had no proof to back up our reasoning other than postulation. Trying to back this method up without sufficient documentation was useless. It was my word against a lack of information on the internet/blogosphere. And everyone knows that if it isn't on the Internet it isn't true. This made me sad.  

I navigated to the far ends of the internets (AKA the 10th page of Google Search Results) and came up empty handed. Had no one posted proof of the one line singleton yet?! Maybe they have, but it was hard to find.  

So I decided to do something about it and wrote up every way of initializing a singleton and inspected them at runtime using breakpoints. After analyzing each stack trace for any similarities I came across something interesting - PROOF!  

Check it out, yo (Oh, and yay for class emojis!):  

![Using the Global Singleton][13]  

Using the Global Singleton  

![Using the One Line Singleton][14]  

Using the One Line Singleton  

The first image shows the stack trace of a global let instantiation. Outlined in red is the thing of interest here. Before the actual initialization of the Kraken singleton is a call trace labeled `swift_once` followed by a `swift_once_block_invoke` call. Since Apple said they lazily instantiate global variables in a `dispatch_once` block, we can safely assume this is what they meant.  

Using this knowledge, I inspected the stack trace of our shiny &amp; pretty one-line-singleton. As you can see with our second image, it's exactly the same! So there you have it! Proof that our one line singleton is proper. All is now right with the world. Also, now that this post is on the Internet, that MUST mean it's true!  

_wink wink_  

# Don't Forget the Private Init!  

As [@davedelong][15], Frameworks Evangelist at Apple, graciously pointed out to me, you have to make sure that your inits are **_private_**. This makes sure your singletons are truly unique and prevents outside objects from creating their own instances of your class through virtue of access control. Since all objects come with a default public initializer in Swift, you need to override your init and make it private. This isn't too hard to do and still ensures our one line singleton is nice and pretty:  

    class TheOneAndOnlyKraken {  
        static let sharedInstance = TheOneAndOnlyKraken()  
        private init() {} //This prevents others from using the default '()' initializer for this class.  
    }  

Doing this will makes sure that the compiler throws this error when any class attempts to initialize `TheOneAndOnlyKraken` using the `()` initializer:  

![][16]  

And there you have it! The perfect, one-line singleton.  

# Conclusion  

Echoing [jtbandes'][17] excellent comment on the [top rated answer to swift singletons on Stack Overflow][18], I simply could not find documentation anywhere that proved thread-safety by "virtue of let". I actually remember something of the sort said when I was at WWDC last year, but you can't expect readers or quick Googlers to stumble across that when trying to make sure this is the right way to write a singleton in Swift. Hopefully, this post can help someone out there understand why the one-line singleton in Swift is the way to go.  

Happy coding fellow nerds!  

## Get Notified!  

Sign up with your email address to get notified when I post something new. Go on. Go ahead. You know you wanna. All the cool kids are doing it.  

Email Address  

Do It!  

I respect your privacy and will NEVER share your data with anyone. You can count on me.  

You, my friend, are awesome. And you've made my day. Thank you for making my day. Here's an awesome quote:  

I am Inigo Montoya. You killed my father. Prepare to die.  

[6]: /assets/postAssets/2016/791010.jpg  
[7]: https://github.com/hpique/SwiftSingleton  
[8]: http://stackoverflow.com/questions/24024549/dispatch-once-singleton-model-in-swift  
[9]: https://developer.apple.com/swift/blog/?id=7  
[10]: http://static1.squarespace.com/static/5592eb03e4b051859f0b377f/t/55a8b9a0e4b0581b80a3f4ae/1437120930876/  
[11]: http://static1.squarespace.com/static/5592eb03e4b051859f0b377f/t/55a8b8e5e4b0671daf047783/1437120742426/  
[12]: http://static1.squarespace.com/static/5592eb03e4b051859f0b377f/t/55a8b8bfe4b0671daf04772e/1437120704789/  
[13]: /assets/postAssets/2016/1437120566797.webp  
[14]: /assets/postAssets/2016/1437120615798.webp  
[15]: https://twitter.com/davedelong  
[16]: /assets/postAssets/2016/1437493975886.webp  
[17]: http://stackoverflow.com/users/23649/jtbandes  
[18]: http://stackoverflow.com/a/24147830  
[19]: http://static1.squarespace.com/static/5592eb03e4b051859f0b377f/t/55a8b7e7e4b0c3b7c348cc5e/1437120488261/  

