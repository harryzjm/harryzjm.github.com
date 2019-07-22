---  
layout: post  
title: Shell与plist  
category: Command  
tags: Shell  
keywords: Shell  
description: 
---  

__Posted by [极乐鸟](http://jileniao.net/mac-shell-PlistBuddy.html)__  

iOS工程下的`Info.plist`文件中有个`CFBundleVersion`的键，从1开始累加的方式给`CFBundleVersion`设置值

### 读取`CFBundleVersion`
plist操作还是用PlistBuddy， 位置在/usr/libexec/PlistBuddy。  
读属性值是用Print命令，单纯读出来在终端打印的话很简单  

	/usr/libexec/PlistBuddy -c "Print CFBundleVersion" ~/xxx/Info.plist

但要赋值给变量，就要稍微加工一下了。  

	BUILD_CODE=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" ~/xxx/Info.plist)

这样再echo $BUILD_CODE 就能输出plist文件中的内部版本号了  

### 执行`CFBundleVersion`加1
Mac下shell中的计算和其他语言稍有不同。加减乘除的话写+-*/是会被当做为字符串的，想让shell知道你是个表达式计算的话，需要`expr`处理。  

	BUILD_CODE=`expr $BUILD_CODE + 1`

注意：expr 中运算符前后必须要有一个空格，我最初忽略掉空格， 结果是死活不出来想要的加法结果。  

### 给CFBundleVersion写入新加1后的值
这个就简单了，一个PlistBuddy的Set命令搞定  

    /usr/libexec/PlistBuddy -c "Set CFBundleVersion $BUILD_CODE" ~/xxx/Info.plist

### 分享自动编译打包ipa的shell文件  
```shell  
#!/bin/bash
#Author Jileniao.Net
SCHEMENAME='JILENIAO'
DATE=`date +%Y%m%d_%H%M`
SOURCEPATH=$( cd "$( dirname $0 )" && pwd)
IPAPATH=$SOURCEPATH
DISNAME=$SCHEMENAME"_"$DATE
ARCHNAME=$DISNAME.xcarchive
IPANAME=$DISNAME
ExportOptions='ExportOptions.plist'
INFOPLIST=$SCHEMENAME/Info.plist
BUNDLE_ID='net.jileniao.iosblog'
DISPLAY_NAME='极乐鸟'
VERSION_NAME='1.0.5'
#BUILD_CODE='153'
PROVISION_PROFILE='jileniao-dis'
# 测试版APP
if [ -n "$1" ]; then
  # extra parameter 1
fi
rm -rf ./build
rm main.jsbundle
rm main.jsbundle.meta
rm -rf ./Build
rm -rf ./ModuleCache
rm -rf ./Logs
xcodebuild clean
CURR=`pwd`
cd .. && react-native bundle --entry-file index.js --platform ios --dev false --bundle-output ios/main.jsbundle --assets-dest ios/
cd $CURR
# 先读取之前的BUILD_CODE，加1得到新的BUILD_CODE
BUILD_CODE=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" $INFOPLIST)
BUILD_CODE=`expr $BUILD_CODE + 1`
# 设置编译参数
/usr/libexec/PlistBuddy -c "Set CFBundleDisplayName $DISPLAY_NAME" $INFOPLIST
/usr/libexec/PlistBuddy -c "Set CFBundleShortVersionString $VERSION_NAME" $INFOPLIST
/usr/libexec/PlistBuddy -c "Set CFBundleVersion $BUILD_CODE" $INFOPLIST
/usr/libexec/PlistBuddy -c "Set CFBundleIdentifier $BUNDLE_ID" $INFOPLIST
/usr/libexec/PlistBuddy -c "Delete provisioningProfiles" $ExportOptions
/usr/libexec/PlistBuddy -c "Add provisioningProfiles dict" $ExportOptions
/usr/libexec/PlistBuddy -c "Add provisioningProfiles:$BUNDLE_ID string $PROVISION_PROFILE" $ExportOptions
# 构建
xcodebuild archive \
 -project JILENIAO.xcodeproj \
 -scheme $SCHEMENAME \
 -configuration Release \
 -archivePath $ARCHNAME \
 clean \
 build \
 -derivedDataPath ./
if [ -e $ARCHNAME ]; then
  echo "xcodebuild archive Successful"
else
  echo "xcodebuild archive Failed"
  exit 1
fi
# 导出ipa
xcodebuild -exportArchive \
 -archivePath $ARCHNAME \
 -exportPath $IPANAME \
 -exportOptionsPlist $ExportOptions
if [ -e $IPANAME ]; then
  echo "Export ipa Successful"
  open $IPAPATH
else
  echo "Export ipa Failed"
  exit 1
fi
#删除临时文件
rm -rf $ARCHNAME
rm -rf ./Build
rm -rf ./ModuleCache
rm -rf ./Logs
```  