Title: mGui Maintenance
Date:  2017-1-14
Category: blog
Tags: python, mGui, maya, gui
Slug: mGui_maintenance
Authors: Steve Theodore
Summary: A new release for mGui

With special thanks to Bob White, Eric Spevacek, Logan Bender and Kartik Hariharan I'd like to announce the 2.1 point release of [mGui](https://github.com/theodox/mGui).  

This is mostly a stabilization release for the [big 2.0 update we pushed in October](/2016/mgui2_live). 

## New Feature

The main new feature in this release is the addition of `[mGui.treeView](https://github.com/theodox/mGui/blob/master/mGui/treeView.py)`, a module for wrapping Maya's `treeView` widget.  I've never been a fan of the maya treeView, which seems like it comes from another planet than the rest of the Maya widget set; it's so different that it needed a whole module of it's own to make it workable. 

The new `MTreeView()` class wraps the existing mGui `TreeView`, but provides a more idiomatic way to get at the TreeView's button commands.  You can now use the same style you use for other mGui buttons:

```python

from mGui.treeView import MTreeView
from mGui.gui import *
from mGui.forms import *

with Window() as win:
    with FillForm() as form:
        tree = MTreeView(numberOfButtons = 2, width = 256, height = 256)

tree.set_items(**{'a':'b', 'b':'a', 'c':'a'})

def btn_a(*_,**kw):
    selected = kw['tree_view'].selectItem
    print 'items', selected, 'button', kw['button_index']

def btn_b(*_,**kw):
    selected = kw['tree_view'].selectItem
    print 'items', selected, 'button', kw['button_index']
    print 'button 2 was pressed'

def double_click(*arg, **kw):
    print 'double click', arg

tree.buttons[0].pressed += btn_a
tree.buttons[1].pressed += btn_b
tree.itemDblClickCommand += double_click

win.show()
```

The `buttons` field looks like an array, and you can (as you see in the sample) use the standard mGui `+=` syntax to add a handler to the buttons as defined by the TreeViews `numberOfButtons` parameter.  


## Updated examples

The example code has been cleaned up a tad -- some of this is just part of the conversion to the new keyless idiom and some of this is just graphic polish. In particular `[mGui.examples.formExamples.py](https://github.com/theodox/mGui/blob/master/mGui/examples/formExamples.py)`, which shows the various options for FormLayouts in mGui, got a bit of cleanup to make it more understandable.  `[mgui.examples.boundCollection.py](https://github.com/theodox/mGui/blob/master/mGui/examples/boundCollection.py)` got some much-needed cleanup


## Bug fixes

### Better handling of LayoutDialogs
We discovered an odd condition where Maya would sometimes refuse to fire off the event handlers attached to an mGui widget when the widget was called through maya's `layoutDialog` command.  It seems like Maya didn't like the potentially aynchronous `MayaEvent` handlers inside of `layoutDialog`, so we added a little bit of tracking to make sure that only synchronous `Event` handlers get attached in that special case. I'd been working around that by manually re-assigning Event objects to the handlers -- but that's a silly thing to ask users to remember, so now it's all transparently handled under the hood.

###  HorizontalExpandForm
We found and fixed an issue with the `HorizontalExpandForm()`, which had somehow stopped expanding.

### List.inner_list
Fixed a condition where sometimes `List()` controls didn't correctly report their the 'inner_list' property which actually contained their visible contents.  In general you don't want to mess with the `inner_list` property in any case, but it should be available for inspection when absolutely necessary now.


## Till next time...

This was a fun release, since it had a lot more contributions from new faces. It's nice to see people running with the code and it's gratifying that it is holding up OK so far. 

It's a [ship year](http://www.xbox.com/en-US/games/state-of-decay-2), so I expect that both the blogging and hacking will be a bit... light... for a while.  But don't hesitate to chime in with questions, comments or, better yet, bug fix pull requests!  

