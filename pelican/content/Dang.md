Title: Dang
Date: 2015-01-10 16:09:00.000
Category: blog
Tags: maya, bugs, techart
Slug: _dang
Authors: Steve Theodore
Summary: An irritating behavior in `cmds.ls()` that can really ruin your day.

You know the old saying, "you learn something new every day?" Well it's true. Usually, it's something like "I don't know where I left my keys," but sometimes you run into something that you realized you should have known all along and yet somehow it takes you by surprise.   


Here's a little nugget that I stumbled onto today.  If you know Maya, you probably know that cmds.ls() with no arguments gives you a list of every entity in your current maya scene.  However if you pass in a list, ls() will filter it down.  It's very common to do something like
    
    
    stuff = ['pCubeShape1', 'top', 'persp']  
    cmds.ls(stuff, type = 'camera')  
    
  
as a cheap way of filtering a list of objects by type, or
 
    
    cmds.ls(stuff, l = True)  
    

to get long names and so on.  All pretty 101.

  
Now, if you're an old Pythonista, you've probably tried it like this too:
    
    cmds.ls(*stuff, l = True)  
    
and gotten the same result.  Usually, **\*args** is a great help in writing simpler code, since you write functions that take an arbitrary number of arguments without forcing the callers to create lists or tuples. Your code can use loops or comprehensions knowing that the **\*args** will be iterable even if it's empty:   
     
    def starargs(*args):  
        for idx, item in enumerate (args):  
            print idx, '\t', item  
      
      
    starargs() # prints nothing  
      
    starargs('a')  
    # 0  a  
      
    starargs('i', 'j', 'k')  
    # 0  i  
    # 1  j  
    # 2 k  
      
    starargs(*['x','y','z'])  
    # 0    x  
    # 1    y  
    # 2    z  
    

  
Unfortunately this nice behavior can bite you if you use it with cmds.ls().  It's easy to miss the difference between
  
    
    cmds.ls(stuff)  
    
and 

  
    cmds.ls(*stuff)  
    

especially because most functions will treat these interchangeably.  
  
However (!) the _**no arguments means list everything**_ behavior means that the first one returns and empty list, but the second returns **a list of everything in Maya**.  If you were using the ls() as a filter or a long-name-converter you are likely to be very surprised by the results. I was using it as part of a cleanup routine, and I suddenly discovered I was 'cleaning' everything in my scenes.   
  
Like I said, you learn something new everyday -- in this case, new curse words!

---

You can work around this behavior  simply enough by not passing *-formatted args to ls(), or at least by not doing so without checking if the argument is valid:  
    
    
    def list_xforms (*args):  
          if not args: return []  
          return cmds.ls(*args, type='transform')  
    
  
Not an earth-shaking discovery, just another one of the many mysteries of the Maya.  


[![](http://www-tc.pbs.org/wgbh/nova/assets/img/posters/cracking-maya-code-vi.jpg)](http://www-tc.pbs.org/wgbh/nova/assets/img/posters/cracking-maya-code-vi.jpg)

  


  


  


