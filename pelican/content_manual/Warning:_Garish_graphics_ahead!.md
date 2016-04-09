Title: Warning: Garish graphics ahead!
Date: 2014-04-12 17:59:00.002
Category: blog
Tags: , , , 
Slug: Warning:-Garish-graphics-ahead!
Authors: Steve Theodore
Summary: pending

If you're tired of boring old light-grey-on-dark-grey text, you'l'l be pleased
to know that the Maya text widget actually supports a surprising amount of
HTML markup. Which means that instead of this:  
  

[![](http://2.bp.blogspot.com/-9X5_YoY6aCo/U0nRf9WRIXI/AAAAAAABICg/l_tl1f_kKd4
/s1600/boring.png)](http://2.bp.blogspot.com/-9X5_YoY6aCo/U0nRf9WRIXI/AAAAAAAB
ICg/l_tl1f_kKd4/s1600/boring.png)

  
  
You set peoples eyeballs on fire like this:  
  
[![](http://2.bp.blogspot.com/-Eb4ElNfethw/U0nQ3Ses5aI/AAAAAAABICY/THb9sHzqWZ0
/s1600/maya+gui+text.png)](http://2.bp.blogspot.com/-Eb4ElNfethw/U0nQ3Ses5aI/A
AAAAAABICY/THb9sHzqWZ0/s1600/maya+gui+text.png)  
---  
This is a single cmds.text object  with it's  label property set to an HTML
string.  
  
  
It turns out that cmds.text is actually a fairly full-featured HTML4 renderer!
That means that you can create pretty complex layouts using many -- though not
all -- of the same tools you'd use for laying out a web page.  You can style
your text with different [fonts](http://www.w3schools.com/css/css_font.asp),
sizes, colors, alignments and so on - you can even us CSS style sheets for
consistency and flexibility.  
  
More than that you can also include images, tables and layout divisions, which
are great for formatting complex information.  No more printing out reports
into dull old textScrollFields!  
  
Best of all, it's trivial to do.  
  
All you need to do is set the _label _property of a cmds.text object to a
striing of valid HTML. By default your object inherits the standard maya
background and foreground colors but you can override these in your HTML  You
can even just compose your text in an HTML editor like DreamWeaver or
Expression Blend; that how I did the example in the graphic above..  
  
There are some limitations you need to be aware of.  The big ones seem to be:  
  

  * HTML/CSS controls for positioning text or divs don't seem to work. _Align _tags inside a span element do work, but [float ](http://www.w3schools.com/cssref/pr_class_float.asp)and [positions](http://www.w3schools.com/css/css_positioning.asp) apparently do not.
  * The renderer won't fetch images or other resources from a URL or relative paths.
  * No JavaScripts - so no blinking texts or animated gifs.  I'm not sure that's a loss.
  * No inputs such as buttons, checkboxes or text fields.
  * Fonts seem to render smaller inside the Maya text than they do in a conventional browser. You can't specify text size in ems or percentages; pixel sizes seem to work fine, however.
  * It looks like text is the only control that supports this styling right now ( tested in Maya 2014).

I'd assume that these limitation reflect the behavior of underlying QWidgets
inside of Maya - if anybody has the real dope to supplement my guesswork,
please chime in.  

  

In the mean time, here's to the inevitable avalanche of eye-ripping garishness
that is sure to result from this revelation. As for me, I'm off to go convert
my whole toolset to [Comic Sans!](http://bancomicsans.com/main/)

  

  

  


