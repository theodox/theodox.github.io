Title: mGui updates
Date: 2014-06-24 22:10:00.000
Category: blog
Tags: mGui, Maya
Slug: mGui-updates
Authors: Steve Theodore
Summary: Some new features for [mGui](https://github.com/theodox/mGui), including progress bars, menu loading from YAML files and scriptJobs

For anybody whos been following the mGui Maya GUI construction kit posts, I've added a few fixes and tweaks to the GitHub project in the last couple of weeks:

#### [mGui.progress](https://github.com/theodox/mGui/blob/master/mGui/progress.py)

The progress module wraps Maya's `progressBar` command for mGui style coding of progress bars.   
  
There are two classes in the module;  **ProgressBar ** is the generic version and **MainProgressBar** always points at Maya's main progress bar.  Both classes have `start()`, `update()` and `end()` methods instead of Maya's clunky `cmds.progressBar(name, e=True, beginProgress=1)` and so on.  They also both have an `iter()` method, which will loop over a generator expression and update the progress bar for each yield then pass along the value. This allows simple idioms like:  
  
  
    from mGui.progress import MainProgressBar  
    import os  
      
    def list_files(dir):  
        # pretend this is as long, slow function...  
        for item in os.listdir(dir):  
            yield item  
      
    pb = MainProgressBar()  
    for each_file in pb.iter(list_files()):  
        print each_file.upper()  
        # here's where you do something with the results  
    
  
So you can update the progress bar without unduly intertwining the GUI update and the program logic.  

#### [mGui.menu_loader](https://github.com/theodox/mGui/blob/master/mGui/menu_loader.py)

The menu_loader module will create menus from a [YAML](http://pyyaml.org/wiki/PyYAMLDocumentation) data file.  It does a little bit of introspection to figure out how to create the items and attach their handlers to functions. This makes it easy to set up a menu with several items from a single setup routine.

The menu data is a text-based YAML file that looks like this:  
  
    
    !MMenu  
        key:   UndeadLabs  
        label: Undead Labs  
        items:  
            - !MMenuItem  
                key: About  
                label: About Undead Labs...  
                annotation: "About this UndeadLabs tool setup"  
                command: tools.common.aboutDialog.open  
      
            - !MMenuItem  
                key: RemoteDebugger  
                label:  Remote Debugger  
                annotation: Start / Stop remote python debugger  
                command: tools.common.remoteDebug.remote_debugger_dialog  
    

And loading the menu is as simple as:  
    
    import mGui.menu_loader as loader  
    loader.load_menu('path/to/undeadlabs.YAML')  

#### [mGui.scriptJobs](https://github.com/theodox/mGui/blob/master/mGui/scriptJobs.py)

The scriptJobs module adapts the event model for use with scriptJobs. A ScriptJobEvent is a derivative of Event which allows you to hook multiple handlers to a single scriptjob (in the same way that the other Event classes allow for multicast delegates):  
  
    
    from mGui.scriptJobs import *  
      
    def print_selected (*args, **kwargs):  
        print cmds.ls(sl=True) or []  
      
    sj = ScriptJobEvent("e", "SelectionChanged")  
    sj += print_selected  
    

  
As with all the mGui Event classes, you can add multiple handlers to  single event:  
  

    sj += some_other_function()  
    
  
The module also includes named subclasses to simplify setup. That way you can do things like:  

    
    closing_sj = RecentCommandChanged()  
    closing_sj += close_handler  
    

  
which is a bit nicer and less typo prone if you use an autocompleting IDE.  
