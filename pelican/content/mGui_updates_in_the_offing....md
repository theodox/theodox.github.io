Title: mGui updates in the offing...
Date: 2016-03-26 15:34:00.000
Category: blog
Tags: mGui
Slug: mGui-updates-2
Authors: Steve Theodore
Summary: A sneek peek at some changes in the 2.0 version of [mGui](https://github.com/theodox/mGui)

For those of you who've been using [mGui](https://github.com/theodox/mGui) to speed up and simplify your Maya gui coding, there are some interesting changes on the horizon. Although I'm not entirely ready to release the changes I have in mind they are mostly sitting in [their own branch in the Github repo](https://github.com/theodox/mGui/tree/remove_keys). 

The upcoming version introduces some new idioms - in particular, it gets rid of the need for explicitly setting keys on new controls to get access to nested properties. In the first version of mGui you'd write something like this:
    
    
    :::python
    with gui.Window('window', title = 'fred') as example_window:  
        with VerticalForm('main') as main:  
            Text(None, label = "Items without vertex colors")  
            lists.VerticalList('lister' ).Collection < bind() < bound    
            with HorizontalStretchForm('buttons'):  
                Button('refresh', l='Refresh')  
                Button('close', l='Close')  

With the new refactor that looks like this:
    
    :::python
    with gui.Window('window', title = 'fred') as example_window:  
        with VerticalForm() as main:  
            Text(label = "Items without vertex colors")  
            lister = lists.VerticalList()  
            lister.collection < bind() < bound    
            with HorizontalStretchForm() as button_row:  
                refresh = Button( label='Refresh')  
                close = Button(label='Close')  


The big advantage here is that those local variables are not scoped exclusively to the layout context managers where they live, which makes it easy to control when and where you hook up your event handlers: In the above example you could defer all the bindings and event handlers to the end of the script like this:
    
    
    :::python
    with gui.Window('window', title = 'fred') as example_window:  
        with VerticalForm() as main:  
            Text(label = "Items without vertex colors")  
            lister = lists.VerticalList()  
            with HorizontalStretchForm() as button_row:  
                refresh = Button( label='Refresh')  
                close = Button(label='Close')  
    lister.collection < bind() < bound  
    refresh.command += refresh_def  
    close.command += close_def  
    

So far I'm really liking the new idiom, particularly eliminating the extra quotes and redundant `None` keys. However this is a minorly breaking change: in some cases, old code which relied on the key value to name and also label a control at the same time will when the keys become redundant. Moreover I bit the bullet and started to refactor the entire mGui module to use correct pep-8 naming conventions - in particular, member variables are _no longer capitalized_. So if you have code outside of mGui this will introduce some issues. When I converted my own code, most of the changes could be done with a regular expression but there were a few danglers.

I think the changes are worth the effort, but I'd be really interested in hearing from users before trying to bring the new mGui branch back into the main line. It should actually be possible to write a script that fixes most existing code automatically, that's something we could refine collaboratively.Please let me know in the comments or by opening an issue on the GitHub site if you have comments or plans. 

As always, bug fixes and pull requests always entertained!

