Title: No soup for you, userSetup.py
Subtitle: How to turn of Maya's userSetup
Date: 2014-05-13 12:30:00.001
Category: blog
Tags: maya, python, tools
Slug: no_soup_for_you
Authors: Steve Theodore
Summary: How to bypass `userSetup.py` (or `userSetup.mel`, if you're really old school)
header_cover: http://4.bp.blogspot.com/_U3jHsmZuyeg/TLr6UM2AS-I/AAAAAAAADg0/1BFasu5yW70/s1600/obama_poster_soup_nazi.gif

When I start working on [isolating maya environments,](multiple_mayapy_management_mania) I came across a nice bit of trivia I didn't know about.  
  
If you ever want to run a Maya without its _userSetup.py_ and without having to move or rename files, it turns out you can suppress userSetups by setting an environment variable called `MAYA_SKIP_USERSETUP_PY` to any value that evaluates as `True`.  This is handy for testing and isolating path management problems - if you've got a rogue path and you're not sure where it's coming from, this is an easy way to make sure it's not being added in by the userSetup.  
  
PS: If you're using a [MayaPyManager](multiple_mayapy_management_mania) to run mayapy instances, you can set this variable like so:  
    
    :::python  
    from mayaPyManager import MayaPyManager  
    import os   
    
    env = os.environ.copy()  
    env['MAYA_SKIP_USERSETUP_PY'] = '1'  
    mgr = MayaPyManager('path/to/mayapy.exe', env, 'path/to/maya/scripts')  
    # this manager will use only the user provided path  
    # and won't run the userSetup.py on startup  

[![](http://4.bp.blogspot.com/_U3jHsmZuyeg/TLr6UM2AS-I/AAAAAAAADg0/1BFasu5yW70/s1600/obama_poster_soup_nazi.gif)](http://4.bp.blogspot.com/_U3jHsmZuyeg/TLr6UM2AS-I/AAAAAAAADg0/1BFasu5yW70/s1600/obama_poster_soup_nazi.gif)
    
