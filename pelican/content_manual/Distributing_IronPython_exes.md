Title: Distributing IronPython exes
Date: 2014-09-01 21:41:00.000
Category: blog
Tags: 
Slug: Distributing-IronPython-exes
Authors: Steve Theodore
Summary: pending

Inside c# exe  

  1. zip up the standard lib
  2. Include it as embedded resource
  3. Put it on on sys.metapath with a ResourceMetaPathImporter
    1. http://blog.ironpython.net/2012/07/whats-new-in-ironpython-273.html
  4. Create a C# app with included Ironython script engine
    1. Same as the Unity blog post
  5. Build!
    1. whole thing is pretty small - mine compiled to under 4 mb

IPy exe

  

http://stackoverflow.com/questions/6195781/ironpython-exe-compiled-using-pyc-
py-cannot-import-module-os

  

Essentially: compile an Ipy stdlib dll using the pyc compiler

  

    
    
    clr.AddReference('StdLib')


