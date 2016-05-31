Title: Size is the enemy: an oldie but a goodie
Date: 2014-09-01 22:39:00.000
Category: blog
Tags: , , 
Slug: _size-is-the-enemy_-an-oldie-but-a-goodie
Authors: Steve Theodore
Summary: pending

While googling my way around some strategy issues lately I rediscovered [this 2007 post from Jeff Atwood](http://blog.codinghorror.com/size-is-the-enemy/) which neatly sums up a few important things that have been factoring very large in my thinking lately:  Plus, I've spent the last 4 days in the madness that is Pax (shout out to all the great folks who came by the booths, by the way!) so I'm a little grumpy.  
  
The reasons why are enumerated after the jump....  (Update 9/3) see below  
  
  


## #1: Maintain &gt; Build

Maintaining any codebase is way harder than making it. Waaaaaay harder.  
  
I've been presiding over a rewrite of my own toolset - one that is only 2.5 years or so of my own work - and I'm amazed and appalled at how crufty it is. Lots of important things are held together with spit and bailing wire. Lots of trivial things are massively over-engineered. And -- though I pride myself on being good about code reuse, _there's-only-one-way-to-do-it, _and extending earlier solutions instead of reinventing things -- it's full of pointless duplication.   
  
And even though it's 90% my own work it's full of conflicting style choices and paradigms.  I guess it shows I'm still learning, so I haven't gotten totally stale yet.  
  


## #2: Dynamic &gt; Static

I've been looking a lot at possible language alternatives to Python for future tools. I love Python. I mean, in a totally unhealthy, creepy, even stalker-y way. But I don't like being to beholden to any one tech or approach. I'd love to get beyond Python's erratic distribution mechanisms, and Id' _really_ like to get my hands on a decent GUI toolkit that didn't make me program C++ indirectly ( [Python Shoes](http://shoesrb.com/), where are you?)  
  
So, while tinkering with [Boo](http://boo.codehaus.org/), [Cobra](http://cobra-language.com/), [Nimrod ](http://nimrod-lang.org/documentation.html)and a few other options I've been revisiting the old theological debate about dynamic vs static languages; working on [Moonrise ](http://moonrise-game.com/) (in Unity) has made me realise that C# was designed with the express intention of driving me insane. It seems routinely true that I write 4 times as many lines of C# as I do in Python. I'm sure I'm saving a few bugs because of all the clunky type management stuff, but I think I'd rather just fix the bugs than suffer through the oceans of boilerplate that C# induces.   
  
To be fair, it's a little worse in Unity than in the rest of the world: you can do a lot to make C# suck less using attributes and reflection and other meta-techniques, but those are tougher to do in Unity's special flavor of C#.   
  
Still, I think I've finally made up my mind on this one: I'd rather take the risks that come with dynamic code over the sheer, mind-numbing boredom that comes with obsessive type safety.  Especially in a world where overhauling and updating and refactoring code is the _real_ work: building it is just the first chapter.  
  


## #3 I hate curly braces.

I'm not even trying to deny it anymore. I hate the little bastards.  What a waste of space.  
  


## #4  I'm Screwed 

The interesting problem - if I end up just getting cozy with my prejudices and preferences - is now how to pick a decent dynamic environment for tools development while (A) not having the code base degenerate into mush and  (B) having decent GUI options.   And if at all possible, (C), no goddam curly brackets.  


  


For most of my work - managing files, talking to databases, and dealing with data on disk performance is not really the most important problem: I tend to deal in minute-scale problems not hour-scale problems, so cutting them down by a factor of 5 is a nice plus rather than a live-or-die necessity.  While this means a bit more freedom, it also removes a sorting criterion from the problem.  
  
The stinky part is that, for the given problem set there really is **no obvious winner**.  
  


  * I could imagine that the combination of [Ruby ](https://www.ruby-lang.org/en/)and [Shoes](http://shoesrb.com/) would be super productive, even though the Shoes GUI is pretty limited compared to QT or WPF.  I could probably tolerate those block ending markers in Ruby, and there is a good set of standard library code out there. The perf is not great but that's my least important problem. I don't think it's much easier to distribute Ruby apps to users than it is to do with Python, however.
  * Nimrod looks like a cool little language, but has no equivalent of the Python standardlib.
  * Boo and Cobra both use the same CLR as C#, so theoretically you can use them to drive GUI apps with WPF or winforms, but that puts you right back into programming a clunky language through the medium of a nicer one: if I wanted that I'd stick with PyQT.  
   
  * Javascript is actually super powerful, in the sense that has the same kind of high level fluidity that Python does. It's also got the best (or at least the most broadly available and flexible) GUI out there in the form of  HTML \+ CSS. Unfortunately it's got the security sandbox so you need a special infrastructure to do even really mundane stuff like trolling the files on a hard disk -- to say nothing of it's famously bad issues with local vs global variables and scoping.  [CoffeeScript](http://coffeescript.org/) can eleminate a lot of the worst syntactic pain (and the blankety-blank curly brackets) but it's hard to maintain code which is written in one language but actually _run_ in another: "compiles to Javascript" is pretty cool until you have to actually debug something which is only genetically related to the code you actually _wrote.  
_
  * (update 9/3) You can do an HTML front end for a python app with the [Chromium Embedded Framework for python](https://code.google.com/p/cefpython/). That actually works pretty well, and lets you keep JS for the light weight UI manipulation while passing the heavy lifting off to Python fairly transparently. The only caveat: the day after I discovered this I went to work, installed the Maya 2015 trial -- and promptly found that _their_ shiny new HTML gui front end had a Javascript error and did not work, thereby preventing me from logging iu to the trial. It's the new thing altight, but it's not quite there.  And It's still a 2-language solution, albeit a nice one.  

  * (update 9/3):  For completeness sake I should mention the combination of Jytron and AWT or Swing. This works right out of the box - if you have Jython, you have a complete GUI toolkit with no downloads, installs or DLLs to manage. You can also [compiile Jython to executables](http://stackoverflow.com/questions/16701979/packaging-a-jython-program-in-an-executable-jar), buit it's not a completely transparent process and it seems a bit fiddly. Still, could be an optiom....  

  * (ipdate 9/3)::  I've also been experimenting a lot with compiling IronPython to exes using the IL compiler that comes with IronPython. So far it actually looks pretty good: the exes are smaller than similar Py2Exes or PyInstaller projects and they seem to be less prone to obscure compilation problems too.... maybe some light at the end of the tunnel?



_**TLDR: ** _There really is nothing that fills the niche of a powerful, flexible language with good GUI and distribution options right now.  Sigh.  
  
Please, prove me wrong !

