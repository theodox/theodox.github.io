Title: Maya's (mildy) Magical Modules
Date: 2014-01-12 17:45:00.000
Category: blog
Tags: Maya, python, modules, programming
Slug: _maya-magical-modules
Authors: Steve Theodore
Summary: An introduction to Maya's module system, a handy method for bundling and distributing tools non-invasively

If you're doing tools work in Maya, you've probably seen a lot of ways of distributing scripts and tools. The most common, alas, is also the wonkiest - dumping a bunch of scripts into the users's script folder or maybe fiddling with Maya.env to point at a shared drive on the local network.     
  
Eventually, you'll rum into situations where you can't just litter files all over your user's machine. Maybe you're supporting multiple projects in the studio and you need to have users hopping back and forth between toolsets. Maybe you're dealing with multiple versions of Maya and your tools have been forked into different environments. Maybe you're dealing with outsources who don't want to permanently alter their own environment just to get your tools for one project. Whatever the reason, someday you'll run into a situation where you want to be able to drop in a whole Maya toolset as a unit and to remove or disable it the same way.   
  
Maya has always a had a facility called **modules**, can be useful for this purpose. It used to be used for things like  cloth sim or hair that were tacked on to the main package (back when hair was a $9,000 add-on!) .  Since then it's largely fallen out of favor, but it's never gone away -- and it has some useful properties that are great for tools distribution.  
  
A module is really a sort of virtual file system.  Maya's most important folders are those for scripts, plugins, icons, and presets -- the same ones you typically see in your Maya user directory.  If you place a special text file in your module path, you can add to extra paths for Maya to search for scripts, plugins, icons and presets.   
  
The big advantage of modules is the ability to manage complete set of files at once - scripts, plugins and so on can all be included (or excluded) from your Maya in a single place _Note to Autodesk - it would be very nice to give users a UI for this.  The 'Modules' setting in the preferences, confusingly, does not refer to _these _modules!_  Parts of a module can be kept independent of the user's private stock of scripts and tools. For outsourcers and contractors, in particular, the ability to completely uninstall a toolset you don't need anymore is a godsend.   
  
Another handy feature of modules is that they can point Maya at shared network paths as well as paths on disk. This makes it far easier to keep a whole team on a common tool set by pointing a module script directory at a shared drive.  I'm not personally a big fan of the shared drive as a distribution method (more on that some other time) but it's fairly common and this makes it easy to establish and manage.  
  
Finally modules do a little bit of automatic versioning. A module can specify different paths for different Maya versions, OS'es and processors.  This means a tool author can produce a single distribution for all customers and give them identical installation instructions without worrying too much about the details of the individual workstations on the receiving end.  You can pack up all of your distributions into a single zip file, and users merely unzip it into the modules folder of their local settings and the installation is done .  

### Basic Setup

Modules are defined by a simple text file with a ".mod" extension.  Maya will look for module files in all the directories in the Maya_MODULE_PATH environment variable if you have it set, or in the modules directory of your Maya user directory (for example, in My Documents\Maya\modules). Here are the default locations where modules can be placed:  

#### Default for Windows

    <user>/My Documents/Maya/modules  
    C:/Program Files/Common Files/Autodesk Shared/Modules/Maya/  
    C:/Program Files/Common Files/Autodesk Shared/Modules/Maya/modules/   

#### Default for Mac OS X, Linux

    $Maya_APP_DIR/Maya//modules  
    $Maya_APP_DIR/Maya/modules  
    /usr/autodesk/modules/Maya/  
    /usr   

A module file is a plain text file. The official documentation for the format is [here](http://docs.autodesk.com/MayaUL/2013/ENU/Maya-API-Documentation/index.html?url=files/GUID-9E096E39-AD0D-4E40-9B2A-9127A2CAD54B.htm,topicNumber=d30e30995) _(the 2012 version is [here](http://download.autodesk.com/global/docs/Mayasdk2012/en_us/index.html).  There are some pretty significant differences between 2012 and 2013+)!_.

For the simple case a module file just looks like this:
    
      
    + moduleName 1.0 c:\path\to\moduleName  
    

  
The module name is what shows up in the Maya UI, the 1.0 is a version number, and the path points Maya to the location of the module folder.  This example would point to a folder called "ModuleName". If that's all that goes in there, then Maya will look for scripts in  
  
    c:\path\to\moduleName\scripts
  
icons in  
  
    c:\path\to\moduleName\icons

and plugins in  
  
    c:\path\to\moduleName\plug-ins  
  
You can test this out by making the folder `c:\path\to\moduleName\scripts` and popping a `userSetup.py` ( or a `userSetup.mel`, if you're feeling old school) into it containing something like a `print("hello world")`. When you restart your Maya, you should see it printout in the Maya output window as Maya loads. It's the output window for Python because the script will execute _before_ the Maya UI has loaded (something to keep in mind in your startup scripts!).  
  
You can avoid hard coding the paths by using an alternate syntax in the mode file.  You have a can, for example, include an environment variable using `${variable}` in place of an absolute path. For example  
    
    
    + moduleName 1.0 ${PROJECT_LOC}\Mayatools  
    
  
will point look for your module folder in the location defined by the environment variable named **project_loc**.  One side effect of this is that uou can put your modules into the modules folder (alongside your mod files) without having to hard-code paths:  
    
    
    + moduleName 1.0 ${Maya_MODULE_PATH}\moduleName 

You can even point your modules at a network share:  
  
    
    + moduleName 1.0 \\net\shared\modules\moduleName

### Fancy stuff in 2013+ 

Sometimes setup requirements are more complex than dropping in a single folder (not a good idea if you can avoid it - but you know how it is...).  **In 2013 and later,**  you can use the module file to override particular paths and do some more flexible setup.  
  
For example, in 2013+, you can also define the path relative to the module file location:  

      
    + moduleName 1.0 ..\moduleName

  
should point at a folder _above_ the directory where the module file is located. **But  remember: 2013+ only!** If you've looked at, for example, [Cyrille Fauvel's post on modules](http://around-the-corner.typepad.com/adn/2012/07/distributing-files-on-Maya-Maya-modules.html) you'll see a bunch of advice that only works for 2013+.  Be aware :)  

The other neat addition in 2013 is the ability to override specific sub-paths of the module. Thus  
      
    
    + moduleName 1.0 ${Maya_MODULE_PATH}\moduleName 
    scripts: //network/share/scripts
 

would point the scripts at the shared network scripts  drive, while leaving the plugins and icons folders in the module location.  
  
 2013+ also offers the ability to set environment variables from inside a module  

    
    
    + moduleName 1.0 ${Maya_MODULE_PATH}\moduleName 
    HAS_FANCY_2013_FEATURES=YES

Will set the environment variable `HAS_FANCY_2013_FEATURES` to 'yes' inside your Maya session. 2013 even has some funky syntax allowing you to append to existing variables and so on . There's no point in recapitulating it here, the [description in the docs](http://docs.autodesk.com/MayaUL/2013/ENU/Maya-API-Documentation/index.html?url=files/GUID-9E096E39-AD0D-4E40-9B2A-9127A2CAD54B.htm,topicNumber=d30e30995) is a concise as I could do. My only commentary would be: _seriously, people? It's 2014 and still with the funky syntax crap?  I'm supposed to recognize that  _PATH += and PATH +:= bin _are different?_  
  
Adding to paths can be extremely handy for some things, but unfortunately this won't solve a particularly thorny problem for tools teams, which is making sure that the OS can find binary dlls: if you have DLL dependencies in a binary plugin, its 'too late' to fix it by appending the DLL locations to the system path once Maya has loaded. Which stinks -- and is another reason to avoid binary plugins like the plague they are if at all possible.

###  One stop tool distribution... or not

For any busy TA, the business of distributing and maintaining toolsets on lots of other people's computers is a constant headache.  Modules can offer some significant assistance with this, since they allow you some control over Maya's search paths without requiring your to write code. It's a simple solution to the chicken-and-egg problem of getting Maya to do what you want before you've got tools loaded up to tell Maya what to do.  
  
Modules, on their own, are not a complete solution to that problem.  But they are a help.  
  
Modules basically just tell Maya to look in a few extra places for things like scripts or plugins - they don't automatically run startup code or do initialization, and they don't have much in the way of smarts -- they can't for example, allow you to quickly switch between two project-specific versions of your Maya tool set. You can install modules for toolsetA and toolsetB, but something smarter than a module file has to decide which one to pick on a given occasion (I'm going to talk about that problem in another post, but for now  However they do allow you to mix and match install locations, which is a big start; they also allow you to install outside the user's script folders, which is a key element in the good-fences-make-good-neighbors relationship between TA tools and the user's private Maya preferences.  Plus, they are explicit: you can look at the file and tell what its trying to do, which beats any number of magic naming and location rules.  
  
At some point in the near future I'll try to post something on the second half of the distribution puzzle: running startup code cleanly and intelligently.  
  
  

