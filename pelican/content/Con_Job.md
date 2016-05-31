Title: Con Job
Date: 2015-04-04 12:20:00.000
Category: blog
Tags: tools, programming, maya, techart
Slug: _con_job
Authors: Steve Theodore
Summary: How to be more productive with mayapy and a console program. 

  
If you do a lot of tools work in maya – particularly if you’re working one something that integrates with a whole studio toolset, instead of being a one-off script – you spend a lot of time restarting. I think I know every pixel of the last five Maya splash screens by heart at this point. A good knowledge of the python `[reload()](https://docs.python.org/2/library/functions.html#reload)` command can ease the pain a bit, but there are still a lot of times when you want to get in and out quickly and waiting for the GUI to spin up can be a real drag.  

If this drives you nuts, `mayapy` -- the python interpreter that comes with Maya -- can be a huge time saver. There are a lot of cases where you can fire off a mayapy and run a few lines of code just to validate that things are working and you don’t need to watch as all the GUI widgets draw in. This is particularly handy if you do a lot of tools work or script development, but’s also a great environment for doing quickie batch work – opening a bunch of files to troll for out of date rigs, missing textures, and similar annoyances.  
All that said, the default mayapy experience is a bit too old-school if you’re running on Windows, where the python shell runs inside the horrendous `CMD` prompt, the same one that makes using DOS so unpleasant. If you’re used to a nice IDE like [PyCharm](https://www.jetbrains.com/pycharm/) or a swanky text editor like [Sublime](http://www.sublimetext.com/3), the ugly fonts, the monochrome dullness, and above all the antediluvian lack of cut and paste are pretty offputting.  

However, it’s not too hard to put a much more pleasant face on mayapy and make it a really useful tool.  

##  Con Ed

[![](http://www.top10films.co.uk/img/conair_cage.jpg)](http://www.top10films.co.uk/img/conair_cage.jpg)  
> obligatory "con" joke here.  
  
The first thing to do is find a good _console program_. A console provides the window and display services for command-line programs; `CMD.exe` does the same thing, it just does it very _badly_. There are several good options depending on your taste (good roundup [here](http://www.nextofwindows.com/4-better-windows-console-tools-alternatives-to-windows-built-in-command-prompt/))). I’m going to walk through the setup for my favorite emulator, [ConEmu](http://conemu.github.io/), but the same ideas should adapt to the other emulators pretty simply.  
First, here’s a quick round up of what [ConEmu](http://conemu.github.io/) is going to be doing for us and mayapay:  


####Cut and paste
`Ctrl+C`, `Ctrl+V`. Worth the price of admission all by itself!

####Customizable fonts
A killer feature for those of us with old, weak eyes and/or aspirations to style

####Command history
If you’re testing out a bit of syntax, or doing something that repetitive but not worth really automating you’ll get a lot of value out of the command history: you can use the up and down arrows to scroll through your recently issued commands and repeat them. Especially when you’re testing a script over and over this takes the bite out of those two or three lines of setup you need to enter again and again.

####Startup options
We’ll want to pass a few flags and instructions to mayapy every time.

####Multiple consoles in one window
ConEmu allows you to run different shells in different tabs. This can be invaluable if you’re doing things like checking the contents of multiple folders, but it’s also a great way to compare the results of your maya scripts side-by-side in two different sessions

####Transparency
A palliative for OSX envy.

## Setup basics

>Again, these instructions are for ConEmu – if you try this with a different console, add your experience in the comments for others!

ConEmu is a great little tool, and it’s free, but it is a bit… overeager?… in its efforts to let you control everything. The interface is a bit old school, so it’s worth walking through the setup process step by step.  
First you’ll want to download and install [ConEmu](http://conemu.github.io/) (the installation instructions are down at the botton of the linked page, and the setup is basically ‘unzip into a folder’).

Once you’ve got ConEmu up and running, you’ll want to open the settings dialog and select the _Tasks_ option from the tree list at left. This will show you a dialog like this:  
  
[![](http://3.bp.blogspot.com/-w0mbodm7rfY/VSAucMI2xPI/AAAAAAABLnI/0y0424YSh94/s1600/conemu_1.jpg)](http://3.bp.blogspot.com/-w0mbodm7rfY/VSAucMI2xPI/AAAAAAABLnI/0y0424YSh94/s1600/conemu_1.jpg)  
>  Like I said, old school.

For starters going to create a startup preset that launches mayapy. ConEmu calls these ‘tasks’. To create a new one, click that `+` botton under the list of predefined tasks. That will create a blank preset with a name like “Group #”, you can rename it by typing a better name in the text box just to the left of the word “Hotkey”.  

The actual command you’ll type goes into the large text box on lower right. Just as test, enter the path to your mayapy _in quotes_, (usually it’s in `Program files\Autodesk\MayaXXXX\bin\mayapy.exe`) followed by a space and `-i`. The `-i` flag is important: it makes sure that mayaypy launches in interactive mode so you can actually use it – without the flag the application will launch and immediately quit! For maya 2015, for example, you can do:  

    
    "%ProgramFiles%/Autodesk/maya2015/bin/mayapy.exe" -i  
    

Test out this minimal version by saving the settings (the _Save Settings…_) button at lower right and making a new console using the green plus button at the upper right. Select the preset; if all goes right you’ll get a python prompt like this:  

[![](http://4.bp.blogspot.com/-6SwtLYQpf7s/VSAuvIdPHDI/AAAAAAABLnQ/gtXK892tdFs/s1600/conemu_2.jpg)](http://4.bp.blogspot.com/-6SwtLYQpf7s/VSAuvIdPHDI/AAAAAAABLnQ/gtXK892tdFs/s1600/conemu_2.jpg)

  
If it doesn’t work, go back and make sure that you surrounded the path to maypy.exe with quotes. **`<insert rant about making an operating system with spaces in the paths that doesn't support spaces by default here!>`**   


## More cowbell

With just these options, you’ve got a working python intepreter, but it’s doesn’t have any maya-specific features. To get an actual maya session you could manually start a [maya standalone](http://techartsurvival.blogspot.com/2014/04/earth-calling-mayastandalone.html) by typing  
  
    :::python  
    import maya.standalone; maya.standalone.initialize()  
    

at the prompt. This works, but it’s a bit tedious. You can automate the process in ConEmu by editing your task description: Go back to the task settings in ConEmu add this to your configuration:  
 
    "%ProgramFiles%/Autodesk/maya2015/bin/mayapy.exe" -i -c "import maya.standalone; maya.standalone.initialize()"  
    

making sure again to check your quotes.   

When you launch a new ConEmu session for your preset you’ll probably notice a pause on startup: that’s Maya starting up in the backgrdound. If your maya loads tools or scripts at startup via `userSetup.py`, you may see printouts or debug information scroll by as well. You should now be working in a standalone session, so you should be able to try something like:  


[![](http://3.bp.blogspot.com/-ncaJyLvqczY/VSAuvALxi_I/AAAAAAABLnU/64gr2WRWkdo/s1600/conemu3.jpg)](http://3.bp.blogspot.com/-ncaJyLvqczY/VSAuvALxi_I/AAAAAAABLnU/64gr2WRWkdo/s1600/conemu3.jpg)

## Avoiding userSetup.py

If your startup scripts do something dependent on the maya GUI you may get an error instead. The _Right Thing<sup>TM<sup>_ to do is to fix that: you don’t want GUI in your startup routine because it hampers your ability to do batch jobs or renders.   

However as a stopgap measure you can [suppress your userSetup.py](no-soup-for-you.html) and load a completely vanilla Maya. This requires setting an environment variable called `MAYA_SKIP_USERSETUP_PY` to 0, which unfortunately is something ConEmu can’t do for you. However, you can work around that by creating a `.BAT` file that sets the environment before launching mayapy. The bat will look like this: 
    
    set MAYA_SKIP_USERSETUP_PY  = 1  
    "%ProgramFiles%/Autodesk/maya2015/bin/mayapy.exe" -i -c "import maya.standalone; maya.standalone.initialize()"  
      
    exit  

You can point your ConEmu task at the .BAT file instead of directly at mayapy and you should get a no-userSetup session.   

This trick can also be used to launch mayapy with different environment variables – for example, I use to maintain different mayapy’s for different projects based on a set of project-specific env vars.  


##Con Air

I’ve been using mayapy in the terminal window as a key part of my work for about a year now, and I’m sure I’ve saved many, many hours of waiting when I noodle on various bits of code, one-off batch tasks, and general noodling. In addition to speedier startup, running mayaPy in the console also gives you a more customizable view and command history, so it’s also a great replacement for many things you might otherwise want to do by starting up Maya and popping open the listener.  
 
Of course, on the meta-meta-level it is a bit odd to by running a text only version of the most powerful graphics tool on the planet. But hey, that’s how we roll in techart land.

