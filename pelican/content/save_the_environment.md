Title: Save the environment!
Date: 2014-06-03 10:30:00.000
Category: blog
Tags: maya, python, distribution, programming
Slug: _save_the_environment
Authors: Steve Theodore
Summary: A grumpy look at the state of python tools distribution

[+Rob Galanakis](https://plus.google.com/112207898076601628221)  posted this on Google+, and as I started to reply I realized this would be a useful thing to put out to a wider audience.  Or maybe useful isn't the right word - it's just something that bugs me so I want to bloviate about it.  

> Hey +Cory Mogk , +Brad Clark, +Steve Theodore , and whoever else in #techart . Has anyone figured out a viable model for reusing Python libraries in Maya, like other Python applications with pip/virtualenv/requirements.txt do? Is there a conversation anywhere?﻿

The short answer to Rob's question is : I've tried to go this route, but I couldn't get a virtualenv-based approach to match for my needs.   For the long answer, read on...  


## If You're Not Outraged, You're Not Paying Attention

Like [a lot of people](http://lucumr.pocoo.org/2014/1/27/python-on-wheels/), I'm pretty unhappy about [the state of python environment management](http://www.simplistix.co.uk/presentations/python_package_management_08/python_package_management_08.pdf).   
  

[![](http://www.faithvillage.com/files/galleries/acf1e1575cba5c2dcbb9966017bab1622c3bfee9-7aaec91bedc07579a475225ff6467f07/thumbs/acf1e1575cba5c2dcbb9966017bab1622c3bfee9-7aaec91bedc07579a475225ff6467f07-hero_image-resize-260-620-fill.jpg)](http://www.faithvillage.com/files/galleries/acf1e1575cba5c2dcbb9966017bab1622c3bfee9-7aaec91bedc07579a475225ff6467f07/thumbs/acf1e1575cba5c2dcbb9966017bab1622c3bfee9-7aaec91bedc07579a475225ff6467f07-hero_image-resize-260-620-fill.jpg)

  
  
There's no dependable, low-maintenance way for people to distribute things -- or to cleanly install things that depend on other things. Even the best tools are wonky, jacked up scaffolding on layers of older, crummier code.  
  
The boundaries of any particular piece of Python are porous to begin with, both because of cross imports and also python's magical morphing and monkey patching abilities - but the messy state of the distribution ecosystem makes things far worse than they should be. Figuring out how to correctly set up a new module in this ambiguous environment is treacherous. It's not for nothing that the "easy" installation tools, pip and easy_install between them have 17,000+ questions on StackOverflow!  
  
The typical [easy_install / pip route](http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows) is tolerable, more or less, if you're coder, and you live in a *nixy everybody-is-a-coder and everybody-has-a-compiler environment. When you're busy experimenting with different frameworks and shiny new toys that show up on [the cheeseshop](https://pypi.python.org/pypi), it's great to get all that cool free stuff with just a a few keystrokes.  But this is "easy" only in the sense that hand editing config files to set up a web server is "easy": if you're technically confident, willing to debug anomalies, and have enough background knowledge to sort of the hiccups you'll be fine. But that's not "easy" for 99% of humanity, that's easy for hardcore nerds.   
  
The Python distribution ecosystem just isn't... well... Pythonic.  It embarrassingly fails the [pythonic principle](http://legacy.python.org/dev/peps/pep-0020/)  
    
    There should be one-- and preferably only one --obvious way to do it.
  
since there are [at least 4 big toolsets](http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2) (setuptoools, distutils, distribute and distribute 2) and none of them is perfect. All rely on a mixture of static data and scripts that react to the state of your local machine, so installing stuff can provide different results from different orders of operation or different environment settings.  It also fails both  
    
        Simple is better than complex.

and     
    
        Complex is better than complicated.

Since the operations you need to perform are often obscure and obscurely interdependent.  Even on a mac, which (being *nixy) should be a much friendlier environment for the live-install approach, I've had serious nightmares -- [trying to set up Django was like a &amp;!*^#&amp;^$ Kafka novel.](http://techartsurvival.blogspot.com/2013/12/and-i-thought-we-had-it-bad.html)  To some degree my bad luck there reflects failure to live up to  
  
  
        In the face of ambiguity, refuse the temptation to guess.  
    

because many of the problems come from a welter of competing installation scripts and tools that are constantly trying to make things "easy" for one application in ways that make them harder for others.  
  
To be fair, the Python universe is so diverse that it's almost beyond the possibility of rational management : a big product like [Plone ](http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-4.2-to-4.3/updating-package-dependencies)can involve literally hundreds of dependencies including a mix of python and compiled code that has to run on dozens of platforms.  Even if 99% of them install flawlessly, the remainders still add up to (at best ) a long, frustrating afternoon of  head-scratching, doc-reading forensics.  It's DLL hell all over again.  
  
It's enough to make you long for a blankety-blank InstallShield wizard.   
  
On the receiving end, things are just as confusing and intimidating.  Because Python is so multi-platform, lots of packages expect you to be able to compile your own binaries, which is rarely a trivial undertaking even for coders (at least, for people who don't do much non-python programming) and is petrifying for end users. More dangerous, though, is the fact that not everybody does a great job of tracking their own dependencies or knowing their own requirements.  If package X will works with version 2.1 of package Y, but not with 2.2  upgrading Y to 2.35 will break X.  And  of course Y 2.35 might have come along after the author of package X has moved on to other projects.  And Y 2.2 may be required by package Z, and get upgraded automatically when you grab Z to check it out.  
  
All of this puts us in the rotten position where installing something new has the potential to break existing code. The user is the one who has to figure that out and work around it, and the fix is often "you can't do this and that in the same install unless you write a patch yourself."   
  
[pip](https://pip.readthedocs.org/en/1.0.1/) and [buildout](http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2) do a heroic job of trying to organize all this chaos. However the underlying problem is _extremely _hard, because the foundations are shaky. You've got decades' worth of code, full of shadowy, hard-to-track dependencies, made by hundreds of different hands with widely varying levels of care and forethought.  The  requirements for packages may not even be clear to their authors: do you know every nuance of the version differences in the packages you rely on? Do you always know when you're exploiting a behavior that the developers don't like and want to change?   
  
Hell, I cannot honestly say that for my _own_ code all the time.  
  
The short version of all this: being able to install stuff is not the same as maintaining a healthy environment.  Just ask all your older relatives whose machines sport seventeen different internet toolbars.  


## Habitat Crisis!

If that all sounds bad... well, in the technical art / Maya context, it's _worse_.  For a couple of reasons:  


[![](http://rlv.zcache.com/habitat_for_two_manatees_bumper_sticker-r4dabf424d562476183df7d3644afd8f8_v9wht_8byvr_512.jpg)](http://rlv.zcache.com/habitat_for_two_manatees_bumper_sticker-r4dabf424d562476183df7d3644afd8f8_v9wht_8byvr_512.jpg)

  
First, and most importantly, artist users are aren't going to accept a "real" command-line-and-text-file based system on their own, even if we had one. That means the TAs have to do it ~~automagically~~ remotely, which is a non-trivial tech challenge.  All too often 'remote installation' translates to 'send some poor sucker running around typing stuff for the artists while they everybody stands around waiting to get back to work.'   And wait till the next big update happens when somebody's on vacation; suddenly they're out of sync with the rest of the team and generating weird issues that are hard to debug. A first class ticket to 'It works on my machine' land!  
  
All tech support is made more difficult by a diversity of environments: that's why console games are easier to make than PC games even though the underlying tech is the same.  Asking your artists to maintain their own Python ecosystem is like asking your teenage kids to clean their rooms: if they do it at all, it won't be done that well enough to justify the arguing you need to get it done at all. It's hard enough to get a big art team to stay in sync with simple stuff like 'always get latest in perforce' or 'set this environment variable'.   So... managing a complex programming environment?  
  
In a shell window?  
  
_Seriously?_  
  
To some degree this is a moot point: no matter your preferences, you might not have the kind of access you need to use python's admin level tools anyway.  If you have to work with outsourcers, as I do,  you don't have the option of ~~forcing your users at gunpoint~~ empowering your users to manage their own setups. In a lot of places (China especially) you can't count on the end user having admin privileges (thus, no writing into the Maya directory) or always-on internet access (thus, no pip/easy_install).   
  
Even if you have the rights, it might not be a good idea.  Outsource teams don't like having to reconfigure their whole workspace to accommodate a client who is here today and gone tomorrow. They want a clean, disposable, drop-in setup that they can turn on and off quickly.  A nice discrete footprint removes a lot of hassle from the relationship.  Done properly, it also saves a lot of remote support time and money.  Simplicity pays.  
  
That's true even for pure in-house development: any company that supports multiple teams needs the same flexibility to swap out toolsets easily without going deep into machine- or user-level configuration. At work I have people hopping between two or three distinct toolsets during an ordinary day, and it's vital that they can do this without wasting time or thought on how things like setting setting all sorts of environment variables or remembering to launch Maya from the right command line.  

## Save the Endangered Pythons!


[![](http://www.kingsnake.com/blog/uploads/zombie.JPG)](http://www.kingsnake.com/blog/uploads/zombie.JPG)
  
All this adds up to a some pretty stark requirements for Maya python tools:  
  


  1. You want a Python environment that's uniform for all your users
  2. You want to be able to have more than one environment side by side
  3. You want your environments to be easy to distribute - and easy to delete 

  
In the wider Python world, this would automatically make you think [virtualenv](https://pypi.python.org/pypi/virtualenv)_._  
  
[virtualenv](https://pypi.python.org/pypi/virtualenv) is the most popular solution to the messy round-robin of versioning, dependency management, and distribution.  While it's all sorts of sophisticated under the hood (here's some [details here](http://blip.tv/pycon-us-videos-2009-2010-2011/pycon-2011-reverse-engineering-ian-bicking-s-brain-inside-pip-and-virtualenv-4899496)) it's conceptually very simple: cut all the crap and just make a separate Python for every project, containing exactly what we need!  Throw in [pip ](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)\- the best-of-a-bad-lot installer tool that makes installing new modules as good as it's likely to get - and you can quickly create and populate lots of clean environments and populate them. Or use [buildout ](http://www.buildout.org/en/latest/)to create precisely controlled setups that have exactly what you need this time.  It's brilliant, Gordian-knot-cutting solution that replaces the incredible complexity of package management tools --  albeit at the cost of lots of duplicated code on disk. Disk space, however, is far cheaper than debugging time and tech-support hand holding.  
  
Unfortunately, I've never been able to figure out how to get a running Maya to use a virtualenv at runtime. The Maya application appears to be it's own python interpreter (you can verify this by checking _sys.executable _in your command window, or just by renaming mayapy.exe and noting that Maya still works fine).  Which means that virtualenv's main trick -- recursing up from the physical location of the python executable -- isn't going to work correctly.  We don't want to try copying Maya itself and all of it's zillions of dependencies  \-- a hefty half-gigabyte or so --for every new project.  And even if we do, the licensing engine does actually care if you're running from the default install directory (at least, it's never let me get away with copying maya to a new location even on a licensed machine).  
  
Effectively, Maya already _is_ it's own virtualenv . That's why you can have other versions of Maya running independently of other Pythons installed on your machine.  Which is nice and all  -- but no help for the problem of creating a cleanly isolated toolsets for your Maya users.  

[![](http://rlv.zcache.com/our_product_use_sustainable_buzzwords_bumper_sticker-r2e739ef8d9874e7f90d354212bf488aa_v9wht_8byvr_324.jpg)](http://rlv.zcache.com/our_product_use_sustainable_buzzwords_bumper_sticker-r2e739ef8d9874e7f90d354212bf488aa_v9wht_8byvr_324.jpg)

After banging my head against this for a while - I'm [not the only one who's tried it](http://stackoverflow.com/questions/16678334/virtualenv-and-maya) \- I've switched to a tactic that has most of the same properties as the virtualenv but is more Maya-friendly.  I try to replicate the same level of isolation with a rather higher level of uniformity (OK, let's be honest here: I mean _fascistic control_) over what my users get.  
  
While I'm not convinced its the distribution system to end all systems, I'm fairly happy with it - it's definitely been the least troublesome, lowest maintenance setup I've administered over the years, and it's worked pretty reliably for me both in and out of house.  I'll describe it a soon-to-be-completed followup post.  
  
In the meantime, allow me to say that looking at lots of bumper stickers while seeking funny graphics for your blog is a speedy way to dim your faith in humanity. _Not recommended._  

[![](http://rlv.zcache.com/im_not_cynical_im_just_experienced_bumper_sticker-rf1ba55c5e6df4016859176f200d32d0f_v9wht_8byvr_324.jpg)](http://rlv.zcache.com/im_not_cynical_im_just_experienced_bumper_sticker-rf1ba55c5e6df4016859176f200d32d0f_v9wht_8byvr_324.jpg)

  


