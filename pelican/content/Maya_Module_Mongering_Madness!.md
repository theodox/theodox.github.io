Title: Maya Module Mongering Madness!
Date: 2014-01-21 19:48:00.000
Category: blog
Tags: 
Slug: Maya-Module-Mongering-Madness!
Authors: Steve Theodore
Summary: pending

When I covered Maya modules a while back, I pointed out that Maya modules are not, by themselves, a complete one-step way to distribute tools.  They stick some extra paths onto your Mel, Python and plugin search paths but they don't actually load tools or set up your environment is any other way.  
  
This time out I want to talk a bit about some of the ways you can do startups cleanly and reliably with mininal fuss.  
  


### Boots on the ground

Booting up your environment should not be a huge deal - but it frequently is.  Lots of studios - particularly ones where the toolset has evolved over long stretches of time and passed through many sets of hands - start their Maya the ways bees fly: in defiance of the laws of physics or even of common sense.  One company I consulted for had a very messy set of imports and initializations that was causing problems. Trying to make sense out of it all I wrote some code to analyze the way modules were imported by other modules dump it out to a big graph using GraphViz.  The resulting graphs were so huge and complex that we could only see them at wall chart size. It was cool in a 1964 NASA engineer sort of way, this huge paper thing -- but the underlying reality was nasty, error prone and generally crazy-making.   
  
And, of course, even when things are relatively sane - when the modules are laid out logically and imported sanely - things still go wrong.  Missing resources, dlls and mlls all over the place,  and most pernicious of all leftover .pyc files that execute the wrong code can all get in the way of the _real_ work - in other words, these things are distractions from  debugging your own stupid mistakes.  
  
The weird part is that this is not really a hard problem.  If your maya toolset is laid out in a simple, logical way these problems generally don't arise, and when they do they are fairly easy to fix.  The nice side benefit is that a well laid out set of modules also makes your life easier when it comes time to distribute your tools to the team.  
  


## Tough as an old boot. Not.

  
You don't need to do a ton of studying to get to a happy place. Good module layout follows the same rules as good code layout: Modules should  do one thing well, inside clear boundaries. They should be grouped into namespaces (for clarity and easier finding things) and have as few cross links as possible.  It's pretty common for code to grow as the problem set it works on fhanv  
  
  
It's simpler if you mentally divide your modules into three  categories:  
  


### Libraries

Libraries makeup the bulk of your code. Ideally they are more or less orthogonal to each other, because you want to minimize the length of import chains.  A good library module relies primarily on the python standard library and as few other modules as possible.  
  
Simple libraries can be individual modules. For example, a module that you use whenever you need to save debug information to a specially formatted text file might be a library module, with functions and classes for formatting the data and writing out the text files.  One important note, though :  good library makes the fewest possible assumptions about context. So, for example, you don't want  your _debugText.py _module to pop up a dialog box prompting for a file location - you don't want it to fail if you run it in a headless Maya batch session!   Library code is UI-less, or at the very least its UI is easily avoided.  
  
Since your problem set is probably very large, you'll eventually want your libraries to have some hierarchy.  Luckily python packages map neatly onto hierarchical folder arrangements....  
  
The problem really should not be that hard. Python's module importing mechanism is elegant and simple (if you don't believe it, try writing solid, modular, reusable code in MaxScript!).  Importing the same module into lots of different places imposes little cost. If the module is well designed -- in particular, if it's done properly so that importing causes no unexpected side effects -- reimporting is a great way to keep code nicely organized and maintainable.  It cuts down on cut-and-pasted code reuse, encourages predictability (it's a lot nicer if when all the code for working with file paths or  
  
For people trying to maintain a big codebase is manag  
  
Big sources of problems:  
  
* Leftover pycs.  These get read in preference to the py files, and you can easily get the wrong code.  Fix: zip files!  
* Version conflicts.  Hard to avoid if you don't lock down the user's env.  Fix: for artists? Zip files. For devs? VirtualEnv  
* name conflicts: http://programmingrealizations.blogspot.com/2010/10/python-import-search-orderprecedence.html   fix: more relative imports, and more explict imports. No star imports! No  
&lt;&gt;  
  
Example:  
  
Create a module hierarchy like this.  Add a print statement to the __init__.py's that print's their path, such as "foo", "foo-bar", and "foo-bar-foo"  
  
highlevel.py and lowlevel.py each start with "import foo"  
  
  


[![](http://1.bp.blogspot.com/-cOARgT1x_X8/Ut4UxvDjqlI/AAAAAAABH6U/_0tHG8lAZRg/s1600/files.png)](http://1.bp.blogspot.com/-cOARgT1x_X8/Ut4UxvDjqlI/AAAAAAABH6U/_0tHG8lAZRg/s1600/files.png)

  
now, try importing the modules!  
  


[![](http://4.bp.blogspot.com/-IzAkmzrw0L8/Ut4UxWT0r5I/AAAAAAABH6Y/-xLV905QtSI/s1600/results.png)](http://4.bp.blogspot.com/-IzAkmzrw0L8/Ut4UxWT0r5I/AAAAAAABH6Y/-xLV905QtSI/s1600/results.png)

  
This is an expected behavior, if an annoying one in this case. The main lesson here is to be careful about reusing names in a hierarchy. It's also another reason why modules should be groomed!  
  
[Python docs about import order](http://docs.python.org/2/tutorial/modules.html#the-module-search-path)  
Nick Coghlan's detailed notes at the [I-wish-I-had-that-domain-named boredomAndLaziness.org](http://python-notes.boredomandlaziness.org/en/latest/python_concepts/import_traps.html)

