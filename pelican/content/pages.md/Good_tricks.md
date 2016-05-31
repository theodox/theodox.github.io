Title: Good tricks
Date: 2014-10-29 19:12:00.000
Category: Tips and tricks
Tags: programming, techart, maya
Slug: Good-tricks
Authors: Steve Theodore
Summary: This page is a collection of little bits of useful info that are too small to merit their own blog posts

This page is a collection of little bits of useful info that are too small to merit their own blog posts.  They aren't in any particular order but they can be very useful.

---

## itertools is your friend
The itertools module is a bit of Python arcana that many people overlook.  For an in-depth look , [Doug Hellman's PyMOTW article](http://pymotw.com/2/itertools/index.html) is a great overview.. Here are some of the highlights:


**itertools.chain** is a fast way to string a list of iterables together. For example, you might have a list of lists - say, a bunch of component selections in Maya - and want to combine them into a single list.  It creates a generator that you can run through one item at a time or convert to a list with a list comprehension   
    
    import itertools  
    cube_verts =  ['pCube1.vtx[1]', 'pCube1.vtx[2]', 'pCube1.vtx[4]', 'pCube1.vtx[5]']  
    sphere_verts = ['pSphere1.vtx[10]', 'pSphere1.vtx[11]', 'pSphere1.vtx[12]', 'pSphere1.vtx[99]']  
    plane_verts = ['pPlane1.vtx[2]', 'pPlane1.vtx[20]', 'pPlane1.vtx[200]', 'pPlane1.vtx[202]']  
      
    for item in itertools.chain(cube_verts, sphere_verts, plane_verts):  
        print item  
      
    #pCube1.vtx[1]  
    #pCube1.vtx[2]  
    #pCube1.vtx[4]  
    #pCube1.vtx[5]  
    #pSphere1.vtx[10]  
    #pSphere1.vtx[11]  
    #pSphere1.vtx[12]  
    #pSphere1.vtx[99]  
    #pPlane1.vtx[2]  
    #pPlane1.vtx[20]  
    #pPlane1.vtx[200]  
    #pPlane1.vtx[202]

**itertools.product** will give you a generator that produces all the combinations of multiple iterable items. For example:  
    
    axes = ('x', 'y', 'z')  
    dimensions = (-1, 0, 1)  
    print [i for i in itertools.product(axes, dimensions)]  
    # [('x', -1), ('x', 0), ('x', 1), ('y', -1), ('y', 0), ('y', 1), ('z', -1), ('z', 0), ('z', 1)]  
    
---

## regex testers
Regular aexpressions are powerful.  They are also ridiculous artifacts of the dark ages when superstitious programmers seemed to believe that every keystroke incurred the displeasure of the computing gods.  Figuring out a regex from scratch is all to often a frustrating exercise, so it's great to have an interactive tool to let you experiment in a nice, safe environment instead of trying to write your regexes and your actual tools st the same time.

For Pythonista's, try [Pythex](https://pythex.org/).

C# / dotnet programmers can use [Regex Storm](http://regexstorm.net/tester) 

---

## **Maya list returns**

Before maya 2014, cmds had several commands with an annoying, anti-pythonic behaviour: if you ask a question that usually returns a list but get no results, Maya will return _None_ instead of an empty list. The most common example is a call to _cmds.ls_ which returns nothing:  
    
    
    good_stuff = cmds.ls(type='mesh')  
    for item in good_stuff:  
        do_something(item)  
    # ERROR: NoneType is not iterable  
    

Luckily, Python has a handy language feature that makes it easy to avoid this trap without an extra if test. If you change the ls like so:   
    
    good_stuff = cmds.ls(type='mesh') or []  
    for item in good_stuff:  
        do_something(item)  
    


The `or []` will pass a list result with something in it unchanged; but if the result is None, the or will substitute the empty list. Everything downstream from there can rely on the presence of a real list, even if it's empty   

---

## Maya-like selection-or-list behavior

If you want to make a function that behaves like the default maya commands -- that is, it works on arguments you pass or on selected objects -- you can combine the *args variable input and the or [] trick to make a nice one liner :
    
    def mayalike(*args):  
         my_objects = args or cmds.ls(sl=True) or []  
         for item in my_objects:  
               #do stuff  
  
This will use `args` if provided and the result of `cmds.ls(sl=True)` if not. Since the `or []` is at the end you can always iterate on it regardless of the arguments or the state of the Maya selection.


---
## Python multiple assignment

Python has a handy trick of unpacking iterables in a single assigment call.  This lets you write things like:

    rotation = [ 0, 90, 0 ]
    rx, ry, rz = rotation

 which saves some annoying boilderplate.  It can be especially useful when dealing with functions that produce tuple or list results:

    filename, extension = os.splitext(completefilename)

which is much more elegant than

    results = os.splitext(completefilename)
    filename = results[0]
    extension = results[1]


It's a good idea, though, to resist the temptation to overdo it: if you find yourself unpacking long tuples a lot:

    name, address, state, zip, phone = customer
 
that's a good sign that customer should be a dictionary, a class, or -- best of all -- a [`namedtuple`](http://pymotw.com/2/collections/namedtuple.html)so you can parse it reliably. 

---

### Learn to love Mayapy

If you're doing a lot of work that involves restarting and reloading maya - particularly if you're iterating on one script that involves a bunch of setup work -- the common trick is to keep all of your steps in a python tab in your listener.  It's better than nothing, but it's still pretty slow, since you need to start up Maya and wait for the gui to finish loading which takes several seconds at best. 
  
If what you're working on does not require GUI access, you can use MayaPy.exe and the `-c` and `-i` flags to get into your script quickly. The `-c` flag launches mayapy and runs a command, and the `-i` flag keeps the  interpreter running. So you can boot mayapy directly into a running, headless copy of maya python like this:  
  
    path/to/maya.py.exe -i -c "import maya.standalone; maya.standalone.initialize()"  
  
Obviously you could put your test setup in a separate module and import that after standalone. I've found this saves me a _huge_ amount of time when I'm iterating on something that doesn't need GUI.  I stick this into a button in my IDE or make a shell alias / bat script to do it.  
  
---

##  <http://lesterbanks.com/2014/01/maya-using-transfer-attributes-as-a-shrink-wrap-deformer/>

