title: python_in_unity
category: Blog
tags: blog
date: 2014-01-01


- importing Unity
 - you need to use clr.AddReferenceToFile, not clr.AddReference
 - the path to Unity/editor/data/managed needs to be in your python system path
 - then import UnityEngine

* Compiling:
- use pyc.py in ipy/tools/scripts
- /target:dll
- reference http://dbaportal.eu/2009/12/21/ironpython-how-to-compile-exe/

* Don't work
- evidently it's broken if you have dotnet 4.5 on your machine...
- unity is dotnet 3.5/4 and key pieces were moved in 4.5
- if 4.5 has been installed it breaks back compatibility
- pyc.py can't pick which version to target
	
