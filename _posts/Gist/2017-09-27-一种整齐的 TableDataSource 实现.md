---  
layout: post  
title: 一种整齐的 TableDataSource 实现  
category: Gist  
tags: Gist  
keywords: Gist  
description: 
---  

```swift  
// Swift 3.2  
func configArtist(_ cell: ArtistTableCell, index: IndexPath) {  
}  

func configVideo(_ cell: RelatedVideoTableCell, index: IndexPath) {  
}  

func configComment(_ cell: CommentCell, index: IndexPath) {  
}  

func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {  
    switch indexPath.section {  
    case 0: return tableView.config(indexPath, block: configArtist)  
    case 1: return  tableView.config(indexPath, block: configVideo)  
    default: return tableView.config(indexPath, block: configComment)  
    }  
}  
```  

key code:  
```swift  
extension UITableView {  
    func config<T: UITableViewCell>(_ index: IndexPath,  
                                    block: (T, IndexPath) -> Void) -> UITableViewCell {  
        let sCell = dequeueReusableCell(withIdentifier: T.description(), for: index)  
        guard let cell = sCell as? T else { return sCell }  
        block(cell, index)  
        return cell  
    }  
}  
```  

随手所写 出乎意料的整齐 Swift果然有点意思  

