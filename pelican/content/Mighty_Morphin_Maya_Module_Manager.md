Title: Mighty Morphin Maya Module Manager
Date: 2014-01-16 01:17:00.001
Category: blog
Tags: Maya, modules, 
Slug: Mighty-Morphin-Maya-Module-Manager
Authors: Steve Theodore
Summary: A GUI for managing Maya modules

For folks who are interested in [fiddling with Maya modules](http://techartsurvival.blogspot.com/2014/01/mayas-mildy-magical-modules.html) as per the last post, I've tossed [a quickie class to manage Maya modules ](https://gist.github.com/theodox/8414494)onto [my Gist account](https://gist.github.com/theodox).  
  
This is a bare bones bit of code. The main class is the `ModuleManager`, which can find any `.mod` files on the MAYA_MODULE_PATH of the current Maya environment. It's primary use is to find and list all the modules; secondarily it can be used to toggle them on and off (by changing the leading + which Maya uses to id a module to a -, or vice-versa). It's pretty dumb (no accounting for file permissions, incorrectly formatted .mod files, etc) but it's handy for quickly testing out configs.  
  
 Also included is a GUI class, `ModuleManagerDialog`, which finds provides a simple GUI for listing, enabling, and disabling .mod files. Again, pretty simple stuff, but people may find it useful.  

[![](http://4.bp.blogspot.com/-WyKmQOSze2g/Uted0a8FJFI/AAAAAAAA_xo/4pP_U9LJPJ8/s400/modmgr.png)](http://4.bp.blogspot.com/-WyKmQOSze2g/Uted0a8FJFI/AAAAAAAA_xo/4pP_U9LJPJ8/s1600/modmgr.png)


As will all code I put up here, it's MIT licensed. Use away with attribution - and if you have any bug fixes, let me know and we'll fix the Gist version.  
  
**PS**, hat tip to the gang at [TAO ](http://tech-artists.org/) for the idea of using a context manager to get out of all those stupid _setParent("..")_ calls in Maya GUI work. I could not find the original post where somebody mentioned it - but whoever you are, sir or madam, thank you ever so much.  
  


