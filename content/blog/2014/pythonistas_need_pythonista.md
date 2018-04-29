Title: Pythonistas need Pythonista!
Date: 2014-07-27 13:07:00.000
Category: blog
Tags: python, web
Slug: pythonista
Authors: Steve Theodore
Summary: [Pythonista](http://omz-software.com/pythonista/), a remarkably slick Python interpreter for iOS

If you consider yourself a Pythonista, you've probably been frustrated by the difficulty involved in getting to work in Python on iOS devices.  I just stumbled upon a really cool answer to your prayers in the form of [Pythonista](http://omz-software.com/pythonista/). It's not brand new - it looks like it came out last year - but I just found out about it and flipped my proverbial wig.  

Pythonista is a sandboxed Python 2.7 development environment for iOS.  It borrows a page from the playbook of earlier sandboxes like [Codea](http://twolivesleft.com/Codea/). and manages to skirt Apple's rules for what you can do on the device while still allowing plenty of power.  It includes a script editor (a pretty slick one for iOS, by the way) ,an interactive environment, and a bunch of libraries to make development really useful.  Among the 'batteries' included are heavy hitters like `pil`,`numpy` and `matplotlib`, along with a few cool little things like a text-to-speech module and tools for dealing with the iOS console.

The most impressive inclusions are the `scene` and `ui` modules: custom modules devoted to iOS drawing and UI.  Ironically, it's easier to develop a GUI application on your iPad using Pythonista than it is to do it on a desktop machine - the app even comes with a UI builder tool similar to QT's interface builder (not nearly as deep or complex, of course, but iOS UI is less complex than desktop). You can read multiple touches.  You can even do hardware accelerate drawing - nice for things like a finger-sketching program.  Since Pythonista includes `pil`, you can even do stuff like image processing:  

[![](http://a1.mzstatic.com/us/r30/Purple2/v4/11/f3/e5/11f3e59b-90f9-68e2-fc61-c6f440bfccf7/screen568x568.jpeg)](http://a1.mzstatic.com/us/r30/Purple2/v4/11/f3/e5/11f3e59b-90f9-68e2-fc61-c6f440bfccf7/screen568x568.jpeg)
   
Pythonista's main limitation is that it's not possible to add external modules to the library in the usual ways: `setuptools` and `pip` aren't available.  You can manually install pure-python modules by copy-paste-save, and there are few installation tools floating around on the web such as [pipista](https://gist.github.com/pudquick/4116558) and [Pypi](https://gist.github.com/anonymous/5243199).  (As an aside: here's a [handy collection of Pythonista snippets and links](http://randomfoo.net/2013/12/08/pythonista-and-ios-automation)).  Modules with binary dependencies -- such as the perforce api -- are off-limits; I'm not sure it it would be possible to use .pyd's that were properly compiled for iOS or if the security sandbox won't allow arbitrary binary code at all.  
  
All in all, it's pretty cool stuff for any Pythonerd.  My big project right now is a touch based inteface on the iPad to control a [BrickPi](http://www.dexterindustries.com/BrickPi/) Mindstorms robot, but at some point I think an asset-database / issue tracker client on the iPad would be a handy tool for our production team .  

All in all, pretty cool for $6.99!

