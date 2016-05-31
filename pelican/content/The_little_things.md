Title: The little things
Date: 2016-02-18 19:27:00.001
Category: blog
Tags: , , , 
Slug: _the_little_things
Authors: Steve Theodore
Summary: pending

It’s the little things that really matter in life.  


[![](http://www.tshirtbordello.com/images/rule-32-enjoy-little-things-s3.jpg)](http://www.tshirtbordello.com/images/rule-32-enjoy-little-things-s3.jpg)

  
If you’ve ever spent any time wrestling with Maya distribution, you’ve probably noticed that `userSetup.py` executes in an odd fashion: it’s not a module that gets imported, it’s basically a series of statements that get executed when Maya fires up. Unfortunately that also means that most of the usual strategies you’d use in python to find out _where_, exactly, you are running from is problematic. The usual python tricks like `__file__` don’t work; and most of the time asking for `os.getcwd()` will point at your Maya program directory. Usually you end up running around looking at all the directories where Maya might be stashing a `userSetup` and trying to figure out which one is the one you are in`. It’s ugly.  
However today, I _**actually found one which works**_. At least, I haven’t figured out how to break it yet.  

    
    
    import os, inspect  
    USER_SETUP_PATH = os.path.dirname(inspect.currentframe().f_code.co_filename)  
    

Since I’ve tried to figure this one out on at least a hundred previous occasions, I am feeling unduly smug about this one.   
PS, if you’re wondering why I care: this makes it really easy to do a simple install/uninstall of a [`userSetup.py` / `userSetup.zip` combo](http://techartsurvival.blogspot.com/2014/07/save-environment-2-i-am-egg-man.html) with no environment variables or special rules.   
PPS: Take that, Maya!

