Title: Mighty Morphin Module Manager Made Moreso
Date: 2014-04-08 09:11:00.000
Category: blog
Tags: maya, modules, mGui 
Slug: _mighty_morphin_module_manager_made_moreso
Authors: Steve Theodore
Summary: An mGui port of the [Maya Module Manager]()

I've added a [port ](https://github.com/theodox/mhttps://github.com/theodox/mGui/blob/master/mGui/examples/modMgr.pyGui/blob/master/mGui/examples/modMgr.py)of the [Maya Module Manager I posted a while](http://techartsurvival.blogspot.com/2014/01/mighty-morphin-maya-module-manager.html) back to the examples included with the [mGui maya GUI library. ](https://github.com/theodox/mGui) This was an exercise to see how much the neater and more concise I could make it using the library.  
  

[![](http://1.bp.blogspot.com/-40t7CxBPtPo/Uz-BSayB96I/AAAAAAABICI/IW5w86cjuTA/s1600/modmgr.png)](http://1.bp.blogspot.com/-40t7CxBPtPo/Uz-BSayB96I/AAAAAAABICI/IW5w86cjuTA/s1600/modmgr.png)

  
Here's some interesting stats:  
  
The original version was **237** lines of code, not counting the header comments. The mGui version was **178** without the header, so about **25%** shorter overall.  There are about 80 lines of unchanged, purely behind-the-scenes code which didn't change between versions, so the real savings is more like **45%.**  Plus, the original sample included some functions for formLayout wrangling  so real savings might be a little higher for more old-fashioned code.  
  
Like I said [last time](http://techartsurvival.blogspot.com/2014/03/maya-gui-ii-all-your-base-classes-are.html), the mGui package is still evolving so it's still very much in a "use at your own risk" state right now... That said, I'd love to get comments, feedback and suggestions.  
  
  


