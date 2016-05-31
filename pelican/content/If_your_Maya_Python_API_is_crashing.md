Title: If your Maya Python API is crashing
Date: 2014-03-18 00:38:00.001
Category: blog
Tags: maya, python, api
Slug: _maya-python-api-crash
Authors: Steve Theodore
Summary: A useful tidbit from Autodesk on how to avoid a common crash scenario in Maya python api 1.0

Check out [this useful post from Cyril Fauvelle](http://around-the-corner.typepad.com/adn/2013/03/possible-misuse-of-mscriptutil-in-maya.html#) on the ins and outs of the dreaded [**MScriptUtil**](http://www.chadvernon.com/blog/resources/maya-api-programming/mscriptutil/).  
  
This kind of stuff is why I reserve API programming for only the knottiest of tasks.  maya.cmds won't clean-exit your Maya session if you reverse two lines by accident.  However, sometimes there's no alternative...  Here's hoping API 2.0 matures quickly and we can all forget all of this pointless distraction.  
  


