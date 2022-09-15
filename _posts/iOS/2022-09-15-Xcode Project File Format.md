---  
layout: post  
title: Xcode Project File Format  
category: iOS  
tags: iOS  
keywords: iOS  
description: 
---  

__Posted by [Monobjc](http://www.monobjc.net/xcode-project-file-format.html)__  

### Introduction

The Xcode project file is an old-style plist (Next style) based on braces to delimit the hierarchy. The file begins with an explicit encoding information, usually the UTF-8 one. This means that the file must not bear a BOM (Byte Ordering Mark) at its start or the parsing will fail.

Note: The following document is based on observations of various \*.pbxproj files and element properties have been inferred. There was not code reverse engineering involved what so ever.

### Unique Identification

Each element in the file is uniquely identified by a 96 bits identifier using a 24 hexadecimal representation. This unique identifier is unique accross the document.

The algorithm used by Xcode to generate the unique identifier seems to be based both on date, sequence and pre-defined values, but as there is no evidence that these identifiers must follow a generation convention, one can think that arbitrary identifier can be used, as long as they are unique accross the document.

The following references were useful while writing this note:

A brief look at the Xcode project format \[Cmake\] Re: CMake Apple XCode support? PBTOMAKE -- Xcode to Unix

### Elements

Here is the list of elements contained in the file format:

*   Root Element
*   PBXBuildFile
*   PBXBuildPhase
    *   PBXAppleScriptBuildPhase
    *   PBXCopyFilesBuildPhase
    *   PBXFrameworksBuildPhase
    *   PBXHeadersBuildPhase
    *   PBXResourcesBuildPhase
    *   PBXShellScriptBuildPhase
    *   PBXSourcesBuildPhase
*   PBXContainerItemProxy
*   PBXFileElement
    *   PBXFileReference
    *   PBXGroup
    *   PBXVariantGroup
*   PBXTarget
    *   PBXAggregateTarget
    *   PBXLegacyTarget
    *   PBXNativeTarget
*   PBXProject
*   PBXTargetDependency
*   XCBuildConfiguration
*   XCConfigurationList

### Root Element

The root section contains the general informations.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| archiveVersion | Number | 1 | Default value. |
| classes | List | Empty |  |
| objectVersion | Number |  | See XcodeCompatibilityVersion enumeration. |
| objects | Map | A map of element | The map is indexed by the elements identifier. |
| rootObject | Reference | An element reference | The object is a reference to a PBXProject element. |

Example:

```
// !$*UTF8*$!
{
    archiveVersion = 1;
    classes = {
    };
    objectVersion = 45;
    objects = {

    ...

    };
    rootObject = 0867D690FE84028FC02AAC07 /* Project object */;
}
```

### PBXAggregateTarget

This is the element for a build target that aggregates several others.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXAggregateTarget | Empty |  |
| buildConfigurationList | Reference | An element reference | The object is a reference to a XCConfigurationList element. |
| buildPhases | List | A list of element reference | The objects are a reference to a PBXBuildPhase element. |
| dependencies | List | A list of element reference | The objects are a reference to a PBXTargetDependency element. |
| name | String | The name of the target. |  |
| productName | String | The product name. |   |

Example:

```
4DA521A6115A00AF007C19C3 /* documentation */ = {
    isa = PBXAggregateTarget;
    buildConfigurationList = 4DA521AE115A00ED007C19C3 /* Build configuration list for PBXAggregateTarget "documentation" */;
    buildPhases = (
        4DA521A5115A00AF007C19C3 /* ShellScript */,
    );
    dependencies = (
        4DA521AA115A00BC007C19C3 /* PBXTargetDependency */,
    );
    name = documentation;
    productName = documentation;
};
```

### PBXBuildFile

This element indicate a file reference that is used in a PBXBuildPhase (either as an include or resource).

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXBuildFile | Empty |  |
| fileRef | Reference | An element reference | The object is a reference to a PBXFileReference element. |
| settings | Map |  | A map of key/value pairs for additionnal settings. |

Example:

```
4D05CA6B1193055000125045 /* xxx.c in Sources */ = {
    isa = PBXBuildFile;
    fileRef = 4D05CA411193055000125045 /* xxx.c */;
};
```

### PBXBuildPhase

This element is an abstract parent for specialized build phases.

### PBXContainerItemProxy

This is the element for to decorate a target item.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXContainerItemProxy | Empty |  |
| containerPortal | Reference | An element reference | The object is a reference to a PBXProject element. |
| proxyType | Number | 1 |  |
| remoteGlobalIDString | Reference | An element reference | A unique reference ID. |
| remoteInfo | String |   |   |

Example:

```
4D22DC0C1167C992007AF714 /* PBXContainerItemProxy */ = {
    isa = PBXContainerItemProxy;
    containerPortal = 08FB7793FE84155DC02AAC07 /* Project object */;
    proxyType = 1;
    remoteGlobalIDString = 87293EBF1153C114007AFD45;
    remoteInfo = xxx;
};
```

### PBXCopyFilesBuildPhase

This is the element for the copy file build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXCopyFilesBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| dstPath | String | The destination path |  |
| dstSubfolderSpec | Number |  |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| runOnlyForDeploymentPostprocessing | Number | 0 |   |

Example:

MISSING

### PBXFileElement

This element is an abstract parent for file and group elements.

### PBXFileReference

A PBXFileReference is used to track every external file referenced by the project: source files, resource files, libraries, generated application files, and so on.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXFileReference | Empty |  |
| fileEncoding | Number |  | See the PBXFileEncoding enumeration. |
| explicitFileType | String |  | See the PBXFileType enumeration. |
| lastKnownFileType | String |  | See the PBXFileType enumeration. |
| name | String | The filename. |  |
| path | String | The path to the filename. |  |
| sourceTree | String | See the PBXSourceTree enumeration. |   |

Example:

```
87293F901153D870007AFD45 /* monobjc.mm */ = {
    isa = PBXFileReference; 
    fileEncoding = 4; 
    lastKnownFileType = sourcecode.cpp.objcpp; 
    name = monobjc.mm; 
    path = sources/monobjc.mm; 
    sourceTree = "";
};
```

### PBXFrameworksBuildPhase

This is the element for the framewrok link build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXFrameworksBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| runOnlyForDeploymentPostprocessing | Number | 0 |   |

Example:

```
4D05CA2C119304BD00125045 /* Frameworks */ = {
    isa = PBXFrameworksBuildPhase;
    buildActionMask = 2147483647;
    files = (
    );
    runOnlyForDeploymentPostprocessing = 0;
};
```

### PBXGroup

This is the element to group files or groups.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXGroup | Empty |  |
| children | List | A list of element reference | The objects are a reference to a PBXFileElement element. |
| name | String | The filename. |  |
| sourceTree | String | See the PBXSourceTree enumeration. |   |

Example:

```
4DA521A2115A003E007C19C3 /* scripts */ = {
    isa = PBXGroup;
    children = (
    4D22DBAF116742DE007AF714 /* fix_references.sh */,
    4DA521A1115A0032007C19C3 /* generate_descriptors.sh */,
    );
    name = scripts;
    sourceTree = "";
};
```

### PBXHeadersBuildPhase

This is the element for the framewrok link build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXHeadersBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| runOnlyForDeploymentPostprocessing | Number | 0 |   |

Example:

```
87293EBC1153C114007AFD45 /* Headers */ = {
    isa = PBXHeadersBuildPhase;
    buildActionMask = 2147483647;
    files = (
    );
    runOnlyForDeploymentPostprocessing = 0;
};
```

### PBXLegacyTarget

MISSING

### PBXNativeTarget

This is the element for a build target that produces a binary content (application or library).

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXNativeTarget | Empty |  |
| buildConfigurationList | Reference | An element reference | The object is a reference to a XCConfigurationList element. |
| buildPhases | List | A list of element reference | The objects are a reference to a PBXBuildPhase element. |
| dependencies | List | A list of element reference | The objects are a reference to a PBXTargetDependency element. |
| name | String | The name of the target. |  |
| productInstallPath | String | The product install path. |  |
| productName | String | The product name. |  |
| productReference | Reference | An element reference | The object is a reference to a PBXFileReference element. |
| productType | String |  | See the PBXProductType enumeration. |

Example:

```
8D1107260486CEB800E47090 /* XXX */ = {
    isa = PBXNativeTarget;
    buildConfigurationList = C01FCF4A08A954540054247B /* Build configuration list for PBXNativeTarget "XXX" */;
    buildPhases = (
        8D1107290486CEB800E47090 /* Resources */,
        8D11072C0486CEB800E47090 /* Sources */,
        8D11072E0486CEB800E47090 /* Frameworks */,
    );
    buildRules = (
    );
    dependencies = (
    );
    name = XXX;
    productInstallPath = "$(HOME)/Applications";
    productName = TrackIt;
    productReference = 8D1107320486CEB800E47090 /* XXX.app */;
    productType = "com.apple.product-type.application";
};
```

### PBXProject

This is the element for a build target that produces a binary content (application or library).

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXProject | Empty |  |
| buildConfigurationList | Reference | An element reference | The object is a reference to a XCConfigurationList element. |
| compatibilityVersion | String | A string representation of the XcodeCompatibilityVersion. |  |
| developmentRegion | String |  | The region of development. |
| hasScannedForEncodings | Number | 0 or 1 | Whether file encodings have been scanned. |
| knownRegions | List | A list of string | The known regions for localized files. |
| mainGroup | Reference | An element reference | The object is a reference to a PBXGroup element. |
| productRefGroup | Reference | An element reference | The object is a reference to a PBXGroup element. |
| projectDirPath | String | The relative path of the project. |  |
| projectReferences | Array of map | Each map in the array contains two keys: ProductGroup and ProjectRef. |  |
| projectRoot | String | The relative root path of the project. |  |
| targets | List | A list of element reference | The objects are a reference to a PBXTarget element. |

Example:

```
29B97313FDCFA39411CA2CEA /* Project object */ = {
        isa = PBXProject;
        buildConfigurationList = C01FCF4E08A954540054247B /* Build configuration list for PBXProject "XXX" */;
        compatibilityVersion = "Xcode 2.4";
        developmentRegion = English;
        hasScannedForEncodings = 1;
        knownRegions = (
                English,
                Japanese,
                French,
                German,
                en,
        );
        mainGroup = 29B97314FDCFA39411CA2CEA /* XXX*/;
        projectDirPath = "";
        projectRoot = "";
        targets = (
             8D1107260486CEB800E47090 /* XXX*/,
        );
};
```

### PBXResourcesBuildPhase

This is the element for the resources copy build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXResourcesBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| runOnlyForDeploymentPostprocessing | Number | 0 |   |

Example:

```
8D1107290486CEB800E47090 /* Resources */ = {
        isa = PBXResourcesBuildPhase;
        buildActionMask = 2147483647;
        files = (
                535C1E1B10AB6B6300F50231 /* ReadMe.txt in Resources */,
                533B968312721D05005E617D /* Credits.rtf in Resources */,
                533B968412721D05005E617D /* InfoPlist.strings in Resources */,
                533B968512721D05005E617D /* MainMenu.nib in Resources */,
                533B968612721D05005E617D /* TableEdit.nib in Resources */,
                533B968712721D05005E617D /* TestWindow.nib in Resources */,
        );
        runOnlyForDeploymentPostprocessing = 0;
};
```

### PBXShellScriptBuildPhase

This is the element for the resources copy build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXShellScriptBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| inputPaths | List | A list of string | The input paths. |
| outputPaths | List | A list of string | The output paths. |
| runOnlyForDeploymentPostprocessing | Number | 0 |  |
| shellPath | String | The path to the shell interpreter. |  |
| shellScript | String | The content of the script shell. |   |

Example:

```
4D22DBAE11674009007AF714 /* ShellScript */ = {
        isa = PBXShellScriptBuildPhase;
        buildActionMask = 2147483647;
        files = (
        );
        inputPaths = (
        );
        outputPaths = (
        );
        runOnlyForDeploymentPostprocessing = 0;
        shellPath = /bin/sh;
        shellScript = "./fix_references.sh";
};
```

### PBXSourcesBuildPhase

This is the element for the sources compilation build phase.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXSourcesBuildPhase | Empty |  |
| buildActionMask | Number | 2^32-1 |  |
| files | List | A list of element reference | The objects are a reference to a PBXBuildFile element. |
| runOnlyForDeploymentPostprocessing | Number | 0 |   |

Example:

```
4DF8B22D1171CFBF0081C1DD /* Sources */ = {
        isa = PBXSourcesBuildPhase;
        buildActionMask = 2147483647;
        files = (
                4DF8B23E1171D0310081C1DD /* test.mm in Sources */,
        );
        runOnlyForDeploymentPostprocessing = 0;
};
```

### PBXTarget

This element is an abstract parent for specialized targets.

### PBXTargetDependency

This is the element for referencing other target through content proxies.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXTargetDependency | Empty |  |
| target | Reference | An element reference | The object is a reference to a PBXNativeTarget element. |
| targetProxy | Reference | An element reference | The object is a reference to a PBXContainerItemProxy element. |

Example:

```
4D22DC0D1167C992007AF714 /* PBXTargetDependency */ = {
        isa = PBXTargetDependency;
        target = 87293EBF1153C114007AFD45 /* libXXX */;
        targetProxy = 4D22DC0C1167C992007AF714 /* PBXContainerItemProxy */;
};
```

### PBXVariantGroup

This is the element for referencing localized resources.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | PBXVariantGroup | Empty |  |
| children | List | A list of element reference | The objects are a reference to a PBXFileElement element. |
| name | String | The filename. |  |
| sourceTree | String | See the PBXSourceTree enumeration. |   |

Example:

```
870C88031338A77600A69309 /* MainMenu.xib */ = {
        isa = PBXVariantGroup;
        children = (
                870C88041338A77600A69309 /* en */,
        );
        name = MainMenu.xib;
        sourceTree = "";
};
```

### XCBuildConfiguration

This is the element for defining build configuration.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | XCBuildConfiguration | Empty |  |
| baseConfigurationReference | String | The path to a xcconfig file |  |
| buildSettings | Map | A map of build settings. |  |
| name | String | The configuration name. |   |

Example:

```
870C88151338ABB600A69309 /* Debug */ = {
        isa = XCBuildConfiguration;
        buildSettings = {
                PRODUCT_NAME = "$(TARGET_NAME)";
        };
        name = Debug;
};
870C88161338ABB600A69309 /* Release */ = {
        isa = XCBuildConfiguration;
        buildSettings = {
                PRODUCT_NAME = "$(TARGET_NAME)";
        };
        name = Release;
};
```

### XCConfigurationList

This is the element for listing build configurations.

| Attribute | Type | Value | Comment |
| --- | --- | --- | --- |
| reference | UUID | A 96 bits identifier |  |
| isa | XCConfigurationList | Empty |  |
| buildConfigurations | List | A list of element reference | The objects are a reference to a XCBuildConfiguration element. |
| defaultConfigurationIsVisible | Number | 0 |  |
| defaultConfigurationName | String | The default configuration name. |   |

Example:

```
870C87E41338A77600A69309 /* Build configuration list for PBXProject "CocoaApp" */ = {
        isa = XCConfigurationList;
        buildConfigurations = (
                870C88061338A77600A69309 /* Debug */,
                870C88071338A77600A69309 /* Release */,
        );
        defaultConfigurationIsVisible = 0;
        defaultConfigurationName = Release;
};
```