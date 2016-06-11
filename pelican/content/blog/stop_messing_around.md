Title: Goddamit, stop messing around
Date: 2015-04-26 11:38:00.000
Category: blog
Tags: programming, console
Slug: stop_messing_around
Authors: Steve Theodore
Summary: A module for simple colored printing in a python terminal

It was inevitable, after I started noodling around with [terminal colors in ConEmu](eyeballs.html), that I’d waste an afternoon cooking up a way to color my Maya terminal sessions automatically.  

The actual code is [up on GitHub](https://github.com/theodox/conemu) (under the usual MIT Open License - enjoy!).   
  
As implemented, its a module you can activate simply by importing `conemu`. Ordinarily I don't like modules that 'do things' on import, but this one is such a special case that it seems justifiable. Importing the module will replace `sys.stdout`, `sys.stdin`, and `sys.display_hook` with ConEmu-specific classes that do a little color formatting to make it easier to work in `mayapy`.  If for some reason you want to disable it, calling `conemu.unset_terminal()` will restore the default terminal.  
  
Here are the main features:  


####Colored prompts and printouts

[![](http://3.bp.blogspot.com/-AvNLhOBExmw/VT0sX69KZ2I/AAAAAAABLvo/Znt5WQHspns/s1600/conemu_2_1.jpg)](http://3.bp.blogspot.com/-AvNLhOBExmw/VT0sX69KZ2I/AAAAAAABLvo/Znt5WQHspns/s1600/conemu_2_1.jpg)

This helps de-emphasize the prompt, which is the least interesting but item on screen, and to emphasize command results or printouts

####Unicode objects highlighted

[![](http://4.bp.blogspot.com/-ciIg7fGJIGw/VT0sxi0-F-I/AAAAAAABLvw/hlbGzLSFB5w/s1600/conemu_2_2.jpg)](http://4.bp.blogspot.com/-ciIg7fGJIGw/VT0sxi0-F-I/AAAAAAABLvw/hlbGzLSFB5w/s1600/conemu_2_2.jpg)

Since all Maya objects returned by commands are printed as unicode string (like `u'pCube1'`, the terminal highlights unicode strings in a different color to make it easy to pick out Maya objects in return values. The annoying little `u` is also suppressed.  


####Code objects highlighted

[![](http://1.bp.blogspot.com/--6vJNm-EdE8/VT0s-3SVHuI/AAAAAAABLv4/SRVJ-2ZCWMQ/s1600/conemu_2_3.jpg)](http://1.bp.blogspot.com/--6vJNm-EdE8/VT0s-3SVHuI/AAAAAAABLv4/SRVJ-2ZCWMQ/s1600/conemu_2_3.jpg)
  
Code objects (classes, functions and so on) are highlighted separately  


####Comment colors

[![](http://1.bp.blogspot.com/-hUxg4Dc96vc/VT0tN5TF79I/AAAAAAABLwA/vUtHyrpuaXo/s1600/conemu_2_4.jpg)](http://1.bp.blogspot.com/-hUxg4Dc96vc/VT0tN5TF79I/AAAAAAABLwA/vUtHyrpuaXo/s1600/conemu_2_4.jpg)
 

Lines beginning with a `#` or a `/` will be highlighted differently, allowing you separate out ordinary command results from warnings and infos. **In this version I have not isolated the path used by `cmds.warning`, which makes this less useful. Does anybody out there know which pipe that uses? It appears to bypass `sys.stdout.write()` and sys.stderr.write()**   


#### Automatic prettyprint

[![](http://4.bp.blogspot.com/-ua1kHl9PyQA/VT0txVSoYJI/AAAAAAABLwI/gL5CZb0MMjk/s1600/conemu_2_5.jpg)](http://4.bp.blogspot.com/-ua1kHl9PyQA/VT0txVSoYJI/AAAAAAABLwI/gL5CZb0MMjk/s1600/conemu_2_5.jpg)

If the result of a command is anything other than a string, it will be run through [`prettyprint` ](https://docs.python.org/2/library/pprint.html)so that it will be formatted in a slightly more legible manner. This is particularly handy for commands like `ls` or `listAttr` which produce a lot of results: `pprint` will arrange these vertically if they result would otherwise be wider than 80 characters.  

## Utilities submodule

The module contains some helper classes if you want to make your own display more elaborate, or to mess with it interactively during a console session.  

#### Terminal class

The _`Terminal`_ class makes it less cumbersome to control the display. The main use is to color or highlight text. The 16 terminal colors are available as `Terminal.color[0]` through `Terminal.color[15]`, and you can highlight a piece of text like so:  

    :::python
    print "this is " + Terminal.color[10]("colored text")  
    

The background colors are `Terminal.bg[0]` through `terminal.bg[5]` and work the same way:  
    
    :::python
    print Terminal.bg[2]("backgound text")  
    

`Terminal` also has a helper for setting, coloring, and unsetting prompt strings.  


#### Conemu: console control

The _`Conemu`_ class includes some limited access to the more elaborate functions offered by ConEmu (The methods in `Terminal` might work in other ANSI terminals – I haven’t tried ! – but the ConEmu ones specific to ConEmu). The key methods are:  

#####`ConEmu.alert(message)`
Pops up a GUI confirm dialog with ‘message’ in it.

#####`ConEmu.set_tab(message)`
Sets the name of the current ConEmu tab to ‘message’.

#####`ConEmu.set_title(message)`
Sets the name of the current ConEmu window to ‘message’.

#####`ConEmu.progress(active, progress)`
if `active` is True, draw a progress indicator in the window task bar at `progress` percent. For example `ConEmu.progress(True, 50)` overlays a 50% progress bar on the ConEmu task bar icon. If `active` is false, the progress bar is hidden. This can be handy for long running batch items

