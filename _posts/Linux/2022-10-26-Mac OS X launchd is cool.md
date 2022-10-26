---  
layout: post  
title: Mac OS X launchd is cool  
category: Linux  
tags: Linux  
keywords: Linux  
---  

__Posted by [Paul Annesley](https://paul.annesley.cc/2012/09/mac-os-x-launchd-is-cool/)__  

One of the core components of Mac OS X is [launchd](http://en.wikipedia.org/wiki/Launchd), and it turns out it can do some cool things.

I particularly like the idea of using `QueueDirectories` to monitor and act upon files dropped into a directory, without having to run any extra daemons. The files could be uploaded to S3, transcoded to a different video format, gzipped… anything.

Anyway, I recently fell into the `launchd` documentation, and came out with this write-up. [Let me know](https://twitter.com/pda) if you find it useful.

## Overview

The first thing that the Mac OS kernel runs on boot is `launchd`, which bootstraps the rest of the system by loading and managing various daemons, agents, scripts and other processes. The [launchd man page](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/launchd.8.html) clarifies the difference between a daemon and an agent:

> In the launchd lexicon, a “daemon” is, by definition, a system-wide service  
> of which there is one instance for all clients. An “agent” is a service that  
> runs on a per-user basis. Daemons should not attempt to display UI or  
> interact directly with a user’s login session. Any and all work that involves  
> interacting with a user should be done through agents.

Daemons and agents are declared and configured by creating `.plist` files in various locations of the system:

```
~/Library/LaunchAgents         Per-user agents provided by the user.
/Library/LaunchAgents          Per-user agents provided by the administrator.
/Library/LaunchDaemons         System-wide daemons provided by the administrator.
/System/Library/LaunchAgents   Per-user agents provided by OS X.
/System/Library/LaunchDaemons  System-wide daemons provided by OS X.
```

Perhaps best of all, `launchd` is open source under the [Apache License 2.0](http://en.wikipedia.org/wiki/Apache_License). You can currently find the [latest source code on the Apple Open Source site](http://www.opensource.apple.com/release/mac-os-x-1081/).

## launchd as cron

The [Mac OS crontab](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man1/crontab.1.html) man page says:

```
Although cron(8) and crontab(5) are officially supported under Darwin,
their functionality has been absorbed into launchd(8), which provides a
more flexible way of automatically executing commands.
```

Turns out `launchd` has a simple `StartInterval <integer>` property, which starts the job every N seconds. However the true cron-like power lies in `StartCalendarInterval`:

```
StartCalendarInterval <dictionary of integers or array of dictionary of integers>

This optional key causes the job to be started every calendar interval as
specified. Missing arguments are considered to be wildcard. The semantics
are much like crontab(5).  Unlike cron which skips job invocations when the
computer is asleep, launchd will start the job the next time the computer
wakes up.  If multiple intervals transpire before the computer is woken,
those events will be coalesced into one event upon wake from sleep.

     Minute <integer>
     The minute on which this job will be run.

     Hour <integer>
     The hour on which this job will be run.

     Day <integer>
     The day on which this job will be run.

     Weekday <integer>
     The weekday on which this job will be run (0 and 7 are Sunday).

     Month <integer>
     The month on which this job will be run.
```

Lets find the shortest example of this in action:

```
pda@paulbook ~ > grep -rl StartCalendarInterval \
                   /Library/Launch* /System/Library/Launch* | \
                   xargs wc -l | sort -n | head -n1 | awk '{print $2}' | xargs cat

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>Label</key>
        <string>com.apple.gkreport</string>
        <key>ProgramArguments</key>
        <array>
                <string>/usr/libexec/gkreport</string>
        </array>
        <key>StartCalendarInterval</key>
        <dict>
                <key>Minute</key><integer>52</integer>
                <key>Hour</key><integer>3</integer>
                <key>WeekDay</key><integer>5</integer>
        </dict>
</dict>
</plist>
```

Better than cron? Apart from better handling of skipped jobs after system wake, it also supports per-job environment variables, which can save writing wrapper scripts around your cron jobs:

```
EnvironmentVariables <dictionary of strings>

This optional key is used to specify additional environmental variables to
be set before running the job.
```

So, anything XML is obviously worse than `0 52 3 * 5 /path/to/command`, but `launchd` is packing more features than cron, so it can pull it off.

## launchd as a filesystem watcher

Apart from having an awesome daemon/agent manager, Mac OS X also has an excellent Mail Transport Agent called [postfix](http://en.wikipedia.org/wiki/Postfix_(software)). There’s a good chance your ISP runs the same software to handle millions of emails every day. We’ll be using it as an example of how `launchd` can start jobs based on filesystem changes.

Because your laptop isn’t, and shouldn’t be, a mail server, you don’t want postfix running all the time. But when messages are injected into it, e.g. by a script shelling out to `/usr/sbin/sendmail` or `/usr/bin/mail`, you want them to be delivered straight away.

Here’s how Mac OS X does it (`/System/Library/LaunchDaemons/org.postfix.master.plist`):

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>org.postfix.master</string>
    <key>Program</key>
    <string>/usr/libexec/postfix/master</string>
    <key>ProgramArguments</key>
    <array>
        <string>master</string>
        <string>-e</string>
        <string>60</string>
    </array>
    <key>QueueDirectories</key>
    <array>
        <string>/var/spool/postfix/maildrop</string>
    </array>
    <key>AbandonProcessGroup</key>
    <true/>
</dict>
</plist>
```

We’ll start with the simple part. `ProgramArguments` passes `-e 60` to postfix, [described thusly](http://www.postfix.org/master.8.html):

```
-e exit_time
              Terminate the master process after exit_time seconds.
              Child processes terminate at their convenience.
```

So postfix is told to exit after running for 60 seconds. The mystery (to me, earlier today, at least) is how it gets started. It could be on a cron-like schedule, but (a) it isn’t, (b) that would suck, and © it would result in delayed mail delivery. It turns out the magic lies in `QueueDirectory`, which I initially overlooked thinking it was a postfix option. The [launchd.plist](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html) man page says:

```
WatchPaths <array of strings>
This optional key causes the job to be started if any one of the listed
paths are modified.

QueueDirectories <array of strings>
Much like the WatchPaths option, this key will watch the paths for
modifications. The difference being that the job will only be started if
the path is a directory and the directory is not empty.
```

The [Launchd Wikipedia page](http://en.wikipedia.org/wiki/Launchd) actually goes into more detail:

```
QueueDirectories
Watch a directory for new files. The directory must be empty to begin with,
and must be returned to an empty state before QueueDirectories will launch
its task again.
```

So `launchd` can monitor a directory for new files, and then trigger an agent/daemon to consume them. In this case, the [postfix sendmail(1) man page](http://www.postfix.org/sendmail.1.html) tells us that “Postfix sendmail(1) relies on the postdrop(1) command to create a queue file in the maildrop directory”, and the [man page for postdrop(1)](http://www.postfix.org/postdrop.1.html) tells us that `/var/spool/postfix/maildrop` is the maildrop queue. `launchd` sees new mail there, fires up postfix, and then stops it after 60 seconds. This might cause deferred mail to stay deferred for quite some time, but again; your laptop isn’t a mail server.

## launchd as inetd

Tranditionally the [inetd](http://en.wikipedia.org/wiki/Inetd) and later [xinetd](http://en.wikipedia.org/wiki/Xinetd) “super-server daemon” were used to listen on various ports (e.g. FTP, telnet, …) and launch daemons on-demand to handle in-bound connection, keeping them out of memory at other times. Sounds like something `launchd` could do…

Lets create a simple inetd-style server at `~/Library/LaunchAgents/my.greeter.plist`:

```
<plist version="1.0">
<dict>
  <key>Label</key><string>my.greeter</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/ruby</string>
    <string>-e</string>
    <string>puts "Hi #{gets.match(/(\w+)\W*\z/)[1]}, happy #{Time.now.strftime("%A")}!"</string>
  </array>
  <key>inetdCompatibility</key><dict><key>Wait</key><false/></dict>
  <key>Sockets</key>
  <dict>
    <key>Listeners</key>
    <dict>
      <key>SockServiceName</key><string>13117</string>
    </dict>
  </dict>
</dict>
</plist>
```

Load it up and give it a shot:

```
pda@paulbook ~ > launchctl load ~/Library/LaunchAgents/my.greeter.plist
pda@paulbook ~ > echo "My name is Paul." | nc localhost 13117
Hi Paul, happy Friday!
```

## launchd as [god](http://godrb.com/)!

You can use `launchd` to ensure a process stays alive forever using `<key>KeepAlive</key><true/>`, or stays alive under the following conditions.

*   `SuccessfulExit` — the previous run exited successfully (or if false, unsuccessful exit).  
    
*   `NetworkState` — network (other than localhost) is up (or if false, down).  
    
*   `PathState` — list of file paths exists (or if false, do not exist).  
    
*   `OtherJobEnabled` — the other named job is enabled (or if false, disabled).  
      
    

These can be combined with various other properties, for example:

*   `WorkingDirectory`  
    
*   `EnvironmentVariables`  
    
*   `Umask`  
    
*   `ThrottleInterval`  
    
*   `StartOnMount`  
    
*   `StandardInPath`  
    
*   `StandardOutPath`  
    
*   `StandardErrorPath`  
    
*   `SoftResourceLimits` and `HardResourceLimits`  
    
*   `Nice`  
      
      
    

## More?

There’s some more [information at developer.apple.com](http://developer.apple.com/library/mac/#documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html), and the [launchd](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/launchd.8.html) and [launchd.plist](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html) man pages are worth reading.

Let me know if you find any of this useful… I’m [@pda](https://twitter.com/pda) on Twitter.

You can leave comments on [Hacker News](http://news.ycombinator.com/item?id=4581125) if that’s more your thing.