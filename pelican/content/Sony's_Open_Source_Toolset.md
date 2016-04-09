Title: Sony's Open Source Toolset
Date: 2014-09-03 23:34:00.000
Category: blog
Tags: , , 
Slug: Sony's-Open-Source-Toolset
Authors: Steve Theodore
Summary: pending

I noticed on [Gamasutra ](http://www.gamasutra.com/view/news/224682/Sony_releases_level_editor_thats_open_source_and_engineagnostic.php)(hat tip [+Jon Jones](https://plus.google.com/114297709081673565436) ) that Sony is open-sourcing its [Authoring Tools Framework](https://github.com/SonyWWS/ATF).    
  


[![](https://raw.githubusercontent.com/wiki/SonyWWS/ATF/images/LBP_PSP_2.png?raw=true)](https://raw.githubusercontent.com/wiki/SonyWWS/ATF/images/LBP_PSP_2.png?raw=true)

  
  
  
This is an interesting idea and I'm a big fan of putting this sort of thing out there - not only does it provide people a good starting point for their own projects, it also allows the curious to see what's going on even if they aren't actually using the code.  I'm sure I'll be poking around in it even if I never use a line of C#.  It's a goodwill gesture, a community service, and a nice way of asking people to fix your bugs for you for free. A win-win!  
  
I am curious as to where the tools are actually pitched. The blurb clains the ATF is used in Naughty Dog's level editor and shader editor for _The Last of Us_, a sequence editor for _Killzone_, an animation blending tool for _God of War_, and  a visual state machine editor for Quantic Dream among other things. That's a pretty broad palette for a single toolkit.  Overly-tight coupling between particular games and particular tools is one reason why game production advances in fits and starts: we have to choose between the completely generic, one-size-fits-all solutions ("Let's just make our level editor in Maya!" or "Just make the particle system UI look like Max's") and tools that can only do a very specific job for a very specific project. The middle ground between these extremes is, I think, fertile territory to explore if you're interested in game toolsets that don't suck.  
  
I'll be curious to see what's in Sony's toybox. I'm especially curious to hear from anybody who has actually worked with this code -- comment away!  
  
The project is available for cloning on [github](https://github.com/SonyWWS/ATF).

