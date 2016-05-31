Title: Pity for the outcast
Date: 2014-02-16 18:30:00.000
Category: blog
Tags: maya, gui, python, programming, mGui
Slug: _pity_for_the_outcast
Authors: Steve Theodore
Summary: A litany of complaints about Maya GUI programming, with a teensy ray of hope

I don't think it's too far over the top to say that everybody hates Maya's internal GUI system. It combines a very 1990's selection of widgets with a very 1970's coding style: it's a  1970's/1990's Frankenstein monster as horrifying as Ashton Kutcher in _That 70's Show._  

_[![](http://www.mediabistro.com/prnewser/files/2013/11/cmKUTCHER_ARTICLE_narrowweb__300x3532.jpg)](http://www.mediabistro.com/prnewser/files/2013/11/cmKUTCHER_ARTICLE_narrowweb__300x3532.jpg)_
  
Not surprisingly a lot of TA's feel like they have to turn to PyQT if they want to deliver polished tools with a modern UI.  Unfortunately this is also less than ideal - while PyQT is a very powerful framework, it's got a very distinctive idiom of its own to learn, and moreover its hard to distribute since it depends on C++ dlls.  If you want to share a tool across studios or with outsourcers on a variety of boxes, OS'es and Maya versions it can become a Dantesque journey into DLL hell.  
  
Because we do a lot of work with outsourcers, I've been looking into ways to render native Maya GUI a little less irritating. A quick review of my own pain-points in Maya GUI development showed me three main problems with the existing system    

## Icky syntax

Default Maya GUI is purely imperative; while Maya creates an in-memory object for every widget you create, you can only interact through it with via commands: In the typical idiom you create a button:    
    
    :::python
    cmds.button("big button");

  
but your can only interact with it by calling more commands:   

    :::python
    mybutton = cmds.button("big button")  
    cmds.button(mybutton, e=True, w=128)  
    cmds.button(mybutton, e=True, label = 'Red button'))  
    cmds.button(mybutton, e=True, bgc = (1,.5, .5))  
    

This gets old pretty fast.  It's particularly bad for GUI components like _formLayout_, which can easily require whopping big arguments like this:
        
    :::python  
    cmds.formLayout( form, edit=True, attachForm=[(b1, 'top', 5), (b1, 'left', 5), (b2, 'left', 5), (b2, 'bottom', 5), (b2, 'right', 5), (column, 'top', 5), (column, 'right', 5) ], attachControl=[(b1, 'bottom', 5, b2), (column, 'bottom', 5, b2)], attachPosition=[(b1, 'right', 5, 75), (column, 'left', 0, 75)], attachNone=(b2, 'top') )  
    

  
Which is, frankly, stupid.  

## Lousy event handling

Another big knock on Maya's native gui is it's lousy callback system. The python version is bolted on to the original, string based MEL version and confuses a lot of people with uncertain scoping and unclear syntax (Check out these threads on [Tech Artists.Org ](http://tech-artists.org/forum/showthread.php?3205-why-scriptJob-doesnt-work-in-case-of-attrControlGrp&highlight=callback)and  [StackOverflow ](http://stackoverflow.com/questions/21036620/executing-different-functions-based-on-options-selected)for some examples of how people get lost) .  
  
Even when default Maya GUI callbacks do fire, they don't usually indicated who fired them off. This means you need to capture any relevant information ahead of time and encode it into the callback. In lots of GUI systems, you could handle a raft of similar functions like this pseudocode:  

    
    
    :::python  
    button_codes = ['red', 'green', 'blue']  
    for code in button_codes:  
        button(code, tag = code, handler = apply_color)  
      
    def apply_color(button):  
       target.color = constants[button.tag]  
    


In Maya, on the other hand, you need to compose the callbacks with the right context when you create them using a `[functools.partial](http://docs.python.org/2/library/functools.html)` or a closure.  This makes coding up anything like dynamic model-view-controller UI into a real chore, and forces you to interleave your layout architecture and your data model in clumsy ways.  
  
Moreover, Maya GUI callbacks are single-function calls. Its common in other frameworks -- for example in C#  -- to have [multicast delegates](http://msdn.microsoft.com/en-us/library/ms173175.aspx) which can trigger multiple actions from a single callback. This makes for cleaner, more general code since you can split UI-only functionality ('highlight this button') from important stuff ('delete this model').  

## No Hierarchy

It might not be strictly fair to say that Maya GUI has 'no hierarchy'; anybody who has ever mucked around with `cmds.setParent` or `cmds.lsUI` knows that the actual widgets are composed in a strict hierarchical tree; hence UI objects with names like  
`window1|formLayout57|formLayout58|frameLayout38|columnLayout5|button5`  
The problem is that Maya doesn't manage this for you - you are responsible for capturing the pathname of every UI widget you create if you ever want to access it again, which imposes a useless maintenance tax on otherwise simple code. 

Moreover, the names aren't determninistic, thanks to Maya's rule against identical paths: that means you may want a button called 'Button', but it may decide to call itself 'Button1' or 'Button99' and there's nothing you can do about it. As if that weren't bad enough, the strongly imperative style of the Maya GUI code also requires manual management. If you declare a layout and start filling it up with widgets, you're also responsible deciding when a particular container is full. A missed `cmds.setParent` can easily screw up your visual layout or the ordering of a menus and it's possible to shoot yourself in the foot without any corresponding gain in power, productivity or even prettiness. This limitation is why Maya has to offer all those redundant command sets for multiple-column rows and grids. When a monstrosity like `cmds.rowLayout(nc=5, cw5=(100,100,50,50,80), ct5 =("left", "left", "both","both","right"))` is a _win_ for code cleanliness and legibility you know something has gone horribly wrong. 

## So What?

All of that amounts to a long-winded way of restating the obvious: nobody likes coding in standard Maya GUI.  The question is, can something be done about it?


Actually, quite a bit..  [Next time out](http://techartsurvival.blogspot.com/2014/02/rescuing-maya-gui-from-itself.html) I'll talk about some practical ways to make Maya GUI coding... well, let's not say _"fun"_, lets run with another 90's retread:

[![](http://www.kraigbrockschmidt.com/mm/images/Win95_Sucks_Less_T-Shirt.jpg)](http://www.kraigbrockschmidt.com/mm/images/Win95_Sucks_Less_T-Shirt.jpg)
  

For 'Windows 95' substitute 'Maya GUI' and you've got the idea (For the origins of this authentic 2400-baud era meme, [click here](http://blogs.msdn.com/b/oldnewthing/archive/2010/08/24/10053386.aspx).) 

