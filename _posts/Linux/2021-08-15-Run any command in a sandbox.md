---
layout: post  
title: OS X Run any command in a sandbox  
category: Linux  
tags: Linux  
keywords: Linux  
---  

__Posted by [davd.io](https://www.davd.io/os-x-run-any-command-in-a-sandbox/)__  



Beside the pre-configured profiles, OS X’s sandbox wrapper command `sandbox-exec` provides a flexible configuration syntax that allows one to create a customized sandbox that either blacklists or whitelists specific abilities of the application executed within.

# Sandbox profile

A sandbox profile defines what a application running inside the sandbox should be able to do. The following example profile `no-network.sb` allows anything except any kind of network access. This might be useful if you want a application to keep your data private instead of sending it home:

```
(version 1)
(allow default)
(deny network*)
```

Replacing `allow` by `deny` would deny anything except networking. It’s that easy.

Other abilities include `file-read`, `signal`, `ipc-posix-shm`, `process`, `mach-lookup` etc. Some need additional parameters like file- or folder names.

The following link provides additional examples of sandbox profiles:

*   [https://github.com/pansen/macos-sandbox-profiles](https://github.com/pansen/macos-sandbox-profiles)
*   [https://github.com/s7ephen/OSX-Sandbox--Seatbelt--Profiles](https://github.com/s7ephen/OSX-Sandbox--Seatbelt--Profiles)

# Running a command sandboxed

You can run any CLI or desktop application by executing it’s Mach-O binary file through `sandbox-exec`. The following command runs VLC player without network access:

```bash
sandbox-exec -f no-network.sb /Applications/VLC.app/Contents/MacOS/VLC
```

Please note that while the sandbox mechanism is good enough for almost any use case, it still does not provide perfect security, described e.g. here: [http://www.coresecurity.com/content/apple-osx-sandbox-bypass](http://www.coresecurity.com/content/apple-osx-sandbox-bypass)

I run this site without advertisement of any kind. All information is free and my only goal is to give back something to the amazing free software development community. If you find some value in this, please [consider donating me a cup of coffee using PayPal](https://www.paypal.me/davdeu). Thank you so much!
