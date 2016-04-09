Title: From the annals of bug subtlety
Date: 2014-06-20 11:39:00.000
Category: blog
Tags: , , , , 
Slug: From-the-annals-of-bug-subtlety
Authors: Steve Theodore
Summary: pending

... comes an object lesson in why it's nice to have a debugger.

  

I'm porting a biggish python codebase to support multiple OSs  and maya
versions.  As I move things around I try to use the opportunity to shore up
test coverage.  And it feels like the most boring chore imaginable, until
something like this crops up.

  

I've got an exporter framework that I share between projects and files, and
when I was moving from 2011- only to multiple version.  It's important code,
so it's tested - but the test is really dumb: it creates a test scene, imports
the test framework, and calls one function. But running the tests in 2014
never works - even though I can manually execute the exact steps in a regular
copy of maya and all is well.

  

So I threw it under the debugger -- [PyCharm FTW!
](http://www.jetbrains.com/pycharm/) \-- and started stepping through. No
dice, everything seemed OK but still the test failed: it could not find my
test objects. Finally, in desperation, I started stepping though the test and
issuing an ls() after every step... and I found that the break wasn't caused
by running code - it was caused by importing my module.  I didn't call it -
just _imported_ it.  WTF?

  

It turns out that _importing PyMel was wiping my test scene _in 2014! The
tests all run under maya.standalone, and the bug only shows up there, which is
why just doing it by hand in maya wasn't showing the same symptoms.

  

Here's my repro case:

  

import maya.cmds as cmds

cmds.polyCube()

# [u'pCube1', u'polyCube1']

cmds.ls(type='transform')

# [u'front', u'pCube1', u'persp', u'side', u'top']

import pymel.core as pm

cmds.ls(type='transform')

# [u'front', u'persp', u'side', u'top']

  

This is a 100% repro in maya.standalone - but _not_ in GUI maya, where the bug
does not occur.Is this true for everybody else ?   The workaround is to import
pymel earlier so that the destruction doesn't affect anything important.

  

But... ouch!

  


