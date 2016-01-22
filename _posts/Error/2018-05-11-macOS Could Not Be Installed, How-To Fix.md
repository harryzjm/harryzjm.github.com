---  
layout: post
title: macOS Could Not Be Installed, How-To Fix
category: Error
tags: Swift Define
keywords: Jekyll,Github
description: 
---  

__[Posted by SK](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/)__


Updating your MacBook or iMac should be free of headaches and drama. Apple even coined a marketing phrase “it just works!” But recently, a lot of readers and Mac users are finding the opposite–it just doesn’t work! Several users have recently had issues updating their MacBook with the latest version of macOS. Unfortunately, this appears to be a fairly common problem for some when updating to the latest macOS High Sierra update.


The update gets stuck with a message “mac os could not be installed on your computer an error occurred installing macOS.” Some folks report seeing this message as well “the path /System/Installation/Packages/OSInstall.mpkg appears to be missing or damaged.” ![macOS Could Not Be Installed, How-To Fix](/assets/postAssets/2018/macOS-could-not-be-installed-on-this-computer-error-message-540x390.webp)


Then your Mac prompts you to quit the installer and restart your computer. ***Well, Apple, whatever happened to it just works???***



Contents  

* [1 Quick Tips ](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Quick_Tips)
    * [1.1 RELATED ARTICLES](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#RELATED_ARTICLES)
* [2 Getting macOS could not be installed on your computer?](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#GettingmacOS_could_not_be_installed_on_your_computer)
    * [2.1 Check Storage](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Check_Storage)
    * [2.2 Beyond the Basics](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Beyond_the_Basics)
* [3 How-To Fix macOS could not be installed issue](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#How-To_Fix_macOS_could_not_be_installed_issue)
    * [3.1 Fixing the Install issue using Safe Mode on your Macbook](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Fixing_the_Install_issue_using_Safe_Mode_on_your_Macbook)
    * [3.2 Fixing macOS Install Problem in Recovery Mode](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Fixing_macOS_Install_Problem_in_Recovery_Mode)
* [4 Removing Third Party KEXT Files](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Removing_Third_Party_KEXT_Files)
* [5 Problems? Try Single User Mode](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Problems_Try_Single_User_Mode)
* [6 Reader Tips ](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Reader_Tips)
    * [6.1 Related Posts:](https://appletoolbox.com/2017/12/macos-could-not-be-installed-how-to-fix/#Related_Posts)



## Quick Tips  
![](/assets/postAssets/2018/ATB-Quick-Tips-540x262.webp)

* Check that your Mac’s Date&Time are on Set Automatically
* Reset your Mac’s NVRAM or PRAM
* Free up some internal hard drive storage
* Restart in Safe Mode and run Disk Utility’s First Aid
* Try Recovery Mode
* Use Terminal to identify and remove non-Apple KEXTs
* Restart in Single User Mode to remove problematic files

### RELATED ARTICLES

* [macOS High Sierra Update, What You Should Know](https://appletoolbox.com/2017/09/upgrading-to-macos-high-sierra-know/)
* [macOS Needs to Update Your Library, How-To Fix](https://appletoolbox.com/2017/11/macos-high-sierra-needs-to-repair-library-fix/)
* [MacBook Slow after macOS Upgrade, Tips to Consider](https://appletoolbox.com/2017/02/macbook-slow-after-macos-upgrade-tips-consider/)



## Getting macOS could not be installed on your computer?

If you are experiencing this issue with your update, here are a few tips that you can use to address this issue. Before proceeding with the steps below, we suggest that you ensure your Mac’s clock is correct. If your Mac’s Date&Time do not match your current timezone or date, macOS often won’t install. Go to **System Preferences > Date & Time. **Apple prefers if you choose the option to Set Automatically.

Next, let’s try out the basic NVRAM reset (or PRAM for older Macs) on your computer.

#### Follow these steps if you are not sure about how to do the NVRAM reset

1. Shut down your Mac
2. Turn it on and immediately press and hold these four keys together: Option, Command, P, and R ![macOS Could Not Be Installed, How-To Fix](/assets/postAssets/2018/NVRAM-Reset-Mac-macOS-and-Mac-OS-X-540x129.webp)
3. Release the keys after about 20 seconds, during which your Mac might appear to restart
4. Open System Preferences and check (and adjust, if necessary) any settings that reset, like volume, display resolution, startup disk selection, or time zone


### Check Storage

The other thing is to make sure that your MacBook/Mac has enough space available to complete the update. If you are running low on space, [Apple provides some guidelines](https://support.apple.com/en-us/HT206996) that can help you recover some space on your Mac.

### Beyond the Basics

Now, that we have taken care of the basics, we suggest that you try each of the processes below until your macOS install problem is fixed. We arranged the how-to-fix steps in three separate categories.

The first of the troubleshooting steps walk you through Safe mode options and then we suggest the Recovery mode. The last of the options shows you how to remove third-party KEXT files using simple terminal commands and then try the install process.

## **How-To Fix macOS could not be installed issue**

### Fixing the Install issue using Safe Mode on your Macbook

* One of the best practices around updating is to make sure that you have taken a backup of the system before doing any troubleshooting. Better Safe than Sorry. We are assuming that you have already backed up your machine before you proceed with any of the steps below
* The first thing to try is to get your Mac/MacBook into Safe mode. When you hold the ‘Shift’ key during startup, your computer will launch into Safe mode
* Safe mode essentially forces the initiated process to ignore all third party launch daemons and startup items. Once you are in the Safe mode, the next course of action is to get into Disk Utility. Once your MacBook has entered safe mode, you will see it indicated in the top right-hand corner of your screen

![macOS Install Could not Be Completed](/assets/postAssets/2018/Safe-Mode.webp)

* Log in using your credentials and then go to your macOS Utilities folder. Here you will need to start up the Disk Utility Program. Once in the program, Click First Aid on the top and choose the volume (Your main HDD) and start the repair process

![macOS Install Could Not Be Completed., How To Fix](/assets/postAssets/2018/macOS-Update-Problems-How-To-Fix.webp)


* Once the Repair has completed, you will be notified of the status. At this point, you would want to rerun the macOS Update program and see if it works for you without giving you the error message

If you tried the steps above in Safe mode and did not find success, the next course of action is to try the Recovery mode.

### Fixing macOS Install Problem in Recovery Mode

* To get to recovery mode on your Mac or MacBook, you will need to press and hold Command + R keys together when booting up your computer  ![](/assets/postAssets/2018/osx_recovery_command-540x166.webp)
* Once you are in the Recovery mode, click on the Apple logo on the top left corner of the screen and make sure that your startup disk is pointing to the Mac Boot disk
* Now find the macOS update program and run the update

Sometimes, when you are facing install/upgrade issues, a workaround that works for many users is to create an external bootable installer and try to run the install program using it. Apple provides a detailed white paper on this process. You can create the [bootable installer on a USB](https://support.apple.com/en-us/HT201372) and then try it to update the macOS.

## Removing Third Party KEXT Files

If you are still reading and have already tried the series of fixes in both Safe mode and Recovery mode to no avail, you may have to roll up your sleeves and do a little more digging into the root cause of the issue. Sometimes it’s the third party KEXT extensions that cause a lot of heartache during update/install of macOS.

These KEXT Files get added to your Mac/MacBook when you are using third-party devices. If you are not sure about it, your best bet is to look and see what third-party extensions are currently there on your machine.


To do so, Open up terminal from your utilities and type in the following to see the non-Apple KEXTs.

**Kextstat | grep –v com.apple**

This command should show you all the third party extensions. Now you can remove them one by one or remove the one that you think may be the suspect. Using terminal, you can unload the kext my using the following command.

**sudo kextunload /System/Library/Extensions/NAMEOFTHEKEXT.kext**



Here ‘NAMEOFTHEKEXT’ needs to be replaced with the appropriate suspect KEXT file that you found above. Once you have unloaded the KEXT, you can go back and check to make sure that it has indeed been removed by using the kextstat command.

Once you have removed all the third party KEXT files and have made sure that you have enough space on your machine for the macOS update, please try and relaunch the install process.



## Problems? Try Single User Mode

If your install process is failing because of a particular problematic file, you can also try to log in using the single user mode and delete that specific file and then try resuming the install. Sometimes you find these problematic ones off files in the Installer log files. To access these log files, open up the Console app in utilities and click on ***‘/var/log’*** on the left-hand column and then choose ***‘instal.log’* **in the next column.![macOS Could Not Be Installed, How-To Fix](/assets/postAssets/2018/MacBook-Console-for-Install-logs.webp)

We are hoping that you were able to fix the macOS Install issue using some of these tips. If you have tried everything without any success, your best bet is to reach out to Apple Support folks so that they can help out. Please let us know how your install worked by using the comments below.

## Reader Tips  
![](/assets/postAssets/2018/Reader-Tips-540x183.webp)

* Try restarting in recovery mode and install macOS High Sierra or Sierra from a bootable USB drive disk. If necessary, reformat your SSD to Mac OS Extended (Journaled), not APFS
* Try setting up another admin user account to see if the same problem continues
* Boot up your Mac using Cmd + R to access the recovery partition. Immediately, go the Apple menu choose Startup Disk. Select your HD. Unlocked it if necessary by entering your admin password. Reboot and see if it starts up normally
* Update your system’s clock by using Terminal. Open **Applications > Utilities >Terminal** and type the command **date. **If the date listed is incorrect, type this command **ntpdate -u “time.apple.com”** then press return. If you live outside of the Americas, type in Apple’s time server nearest you, such as **time.asia.apple.com** or **time.euro.apple.com **inside the parenthesis
* I created an ISO image of macOS High Sierra on a USB and installation was a breeze after that
* Shut down your Mac and wait 30 seconds. After 30 seconds, press the power button and immediately hold down Command + R and keep pressing these keys until the apple logo appears. You should see a screen asking you to choose a language, select your language of choice, and navigate to your macOS Utilities. Check the WiFi button at the top right to make sure you’re connected to the internet. Then select reinstall the latest version of macOS, click continue, agree and allow it to download and restart on its own (just leave the Mac alone–really!) After macOS reinstalls, it should restart and end up at the login screen
* I booted up while holding the Option key and chose my regular MacinstoshHD (**not an update volume**). Then I booted normally (not with safe mode) and tried again to reinstall the update. Took several reboots but in the end, it worked!
* Oftentimes, this error means your Mac is trying to boot from a different HD partition, sometimes even the recovery partition. To fix it, restart in startup manager (holding option key) and select your regular HD to reboot from. Once successful, go to **System Preferences > Startup Disk** > Select your normal HD startup. That should fix the problem

