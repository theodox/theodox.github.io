Title: Didn't need those eyeballs anyway!
Date: 2015-04-12 10:21:00.000
Category: blog
Tags: , , , 
Slug: Didn't-need-those-eyeballs-anyway!
Authors: Steve Theodore
Summary: pending

OK, I admit this one is pretty much useless. But it’s still kind of cool :)  
[Just the other day](http://techartsurvival.blogspot.com/2015/04/blockquote-
background-f9f9f9-border.html) I discussed setting up
[ConEmu](http://conemu.github.io/) for use as a direct maya terminal. This is
fun, but once you’ve got the console virus the next thing that happens is you
start getting obsessed with stupid terminal formatting tricks. It’s almost as
if going text modes sends you past the furthest apogee of spartan simplicity
and starts you orbiting inevitably back towards GUI bells and whistles.  
At least, I know that about 15 minutes after I posted that last one, I was
trying to figure out how to get colored text into my maya terminal window.  
It turns out it’s pretty easy. ConEmu supports [ANSI escape codes](http://wiki
.bash-hackers.org/scripting/terminalcodes), those crazy 1970’s throwbacks that
all the VIM kiddies use on their linux machines to make ugly termina color
schemes:  
![](http://i.stack.imgur.com/79YI2.png)  
---  
all this beauty... in _your_ hands!  
This means any string that gets printed to ConEmu’s screen, if it contains
color codes, will be in color! You can change background colors, foreground
colors, even add bold, dim or (God help us) _blinking_ text to your printouts.  
Here’s a quick way to test this out:  
Start up a maya command shell in ConEmu (instructions
[here](http://techartsurvival.blogspot.com/2015/04/blockquote-background-
f9f9f9-border.html) if you missed them last time).  
In your maya session, try this:  
  

    
    
    import sys  
    sys.ps1 = "Maya> "  
    

  
This swaps in the custom prompt `Maya>` for the generic `>>>`.  
![console_prompt](http://3.bp.blogspot.com/-mBMHF410Wy0/VSqmy2QJCEI/AAAAAAABLn
w/qu1P2pz15Do/s1600/color_1.png)  
Now, let’s try to make it a bit cooler: try setting `sys.sp1` to this:  

    
    
    sys.ps1 = "\033[38;5;2mMaya>\033[0m "  
    

  
![color_console](http://2.bp.blogspot.com/-2J0dLUc78MI/VSqmyxXLdsI/AAAAAAABLn0
/4ERl34IdqTI/s1600/color_0.png)  
Whoa!  
Here’s what the gobbledygook means:  
**`\033` **is the ascii code for ‘escape’, which terminals use to indicate a non-printable character. The square bracket - number - m sequences are displayc ommands which will affect the output. In this case we said “set the text mode to color index 2’ (probably green on your system), type out ‘Maya&gt; ‘, then revert to the default color”.  
Here’s a few of the formatting codes that ConEmu supports:  

  * `**\033[0m**` resets all escapes and reverts to plain text.
  * `**\033[1m**` and `**\033[2m**` start or end _bold_ text
  * `**\033[4m**` turns on ‘inverse’ mode, with foreground and background colors reversed
  * `**\033[2J**` clears the terminal screen and sets the prompt and cursor back to the top. You probably don’t want to use this as your prompt, since it clears the screen after every key press! However it can be useful for paging through long results, Unix-`more` style.
  * `**033[38;5;<index>m**` sets the text color to the color `<index>`. Colors are defined in the ConEmu settings dialog (_Features &gt; Colors_). There are 16 color; here you identify them by index number (Color #0 is the default background, color #15 is the default foreground) This allows you to swap schemes – several well known codiing color schemes such as Zeburn and Solarized are included in ConEmu.
  * **`033[48;5;<index>m` **sets the background color to the color `<index>`. The background colors are a bit hard to spot: if you check the colors dialog you’ll see a few items have two numbers next to them (such as ‘1/4’ or ‘3/5’). The second number is the background index. **Yes, it’s wierd – it was the 70’s. What do you expect?**
  * `**\033[39m**` resets any color settings.

  
These codes work sort of like HTML tags; if you “open” one and don’t “close”
it you’ll find it stays on, so while you’re experimenting you’ll probably
experience a few odd color moments.  
But still… how cool is that? Now if we could only get it to syntax highlight…
or recognize maya objects in return values… hmm. Things to think about :)  
The Full list of escape codes supported by ConEmu is
[here](http://conemu.github.io/en/AnsiEscapeCodes.html)


