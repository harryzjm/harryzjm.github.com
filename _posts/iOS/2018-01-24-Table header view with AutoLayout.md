---
layout: post
title: Table header view with AutoLayout
category: iOS
tags: CocoaPods
keywords: CocoaPods
---  
 
__Posted by [aunnnn](https://medium.com/@aunnnn/table-header-view-with-autolayout-13de4cfc4343)__  


[*Just give me the code!*](https://github.com/aunnnn/TableHeaderViewWithAutoLayout)

I’d been searching for how to use AutoLayout with a table header view. Setting a table view’s tableHeaderView feels like throwing a view in a dark hole. We don’t know how it’s related with other views in the hierarchy.

Finally, I found a solution that works well for me *without *explicit frame calculations.

*Note: I use UIViewController with UITableView as a subview, not UITableViewController.*

**The gist:** 1) set table header view, 2) pin the header view’s centerX, width and top anchors to the table view, *3)* call `layoutIfNeeded` on table header view to update its size, 4) *set table view header again.

### **Steps**

In `viewDidLoad()` :

1. Make a container view. Add everything here. Make sure to set constraints properly to let it grows as needed.
2. Set tableHeaderView to the container
3. Add* *centerX, width and top anchors of the container (which is now tableHeaderView) to the table view.
4. Update the header view frame first time by calling `layoutIfNeeded()` then setting the table header view again.

That’s it 🎉.

```swift  

// ...In viewDidLoad()

// 1.
let containerView = UIView()
containerView.translatesAutoresizingMaskIntoConstraints = false

// headerView is your actual content.
containerView.addSubview(headerView)


// 2.
self.tableView.tableHeaderView = containerView

// 3.
containerView.centerXAnchor.constraint(equalTo: self.tableView.centerXAnchor).isActive = true

containerView.widthAnchor.constraint(equalTo: self.tableView.widthAnchor).isActive = true

containerView.topAnchor.constraint(equalTo: self.tableView.topAnchor).isActive = true

// 4.
self.tableView.tableHeaderView?.layoutIfNeeded()
self.tableView.tableHeaderView = self.tableView.tableHeaderView

```

### To update the header frame on device rotation

Just do step 4\. again in viewWillTransitionToSize, but do it in the next draw loop (by wrapping with Dispatch.main.async), since `layoutIfNeed()` needs to know the correct parent frame first:

```swift  

override func viewWillTransition(to size: CGSize, with coordinator: UIViewControllerTransitionCoordinator) {

  super.viewWillTransition(to: size, with: coordinator)

  DispatchQueue.main.async {
    self.tableView.tableHeaderView?.layoutIfNeeded()
    self.tableView.tableHeaderView = self.tableView.tableHeaderView
  }
}

```  

### Github Repo

The repo below has a UITableView’s extension for these 4 steps. It also contains working examples, including both UITableView and UITableViewController.

[**aunnnn/TableHeaderViewWithAutoLayout**
*TableHeaderViewWithAutoLayout - Example of how to use AutoLayout with table header view.*github.com](https://github.com/aunnnn/TableHeaderViewWithAutoLayout "https://github.com/aunnnn/TableHeaderViewWithAutoLayout")[](https://github.com/aunnnn/TableHeaderViewWithAutoLayout)

If you’re interested, I’m developing a framework that handles this kind of gotchas in UITableView for you. So you can get started with using AutoLayout with table header view, section header/footer view and table view cell immediately. You need to know how to use AutoLayout though.

It’s not finished yet, but you can checkout examples. Any helps/suggestions are welcomed.

[**aunnnn/ViewElements**
*ViewElements - A framework to manage and reuse UIViews in iOS apps.*github.com](https://github.com/aunnnn/ViewElements "https://github.com/aunnnn/ViewElements")[](https://github.com/aunnnn/ViewElements)

*If this is helpful, please tap* 💚 *for me* 😍.





