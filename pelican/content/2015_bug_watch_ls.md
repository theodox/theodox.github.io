Title: 2015 Bug watch: ls()
Date: 2014-09-04 12:15:00.001
Category: blog
Tags: maya, programming, bugs
Slug: _2015-bug-ls
Authors: Steve Theodore
Summary: A nasty little changed in maya's `ls()` command for 2015

For people switching to Maya 2015 here's an irritating bug in the 2015 Maya python layer.  
  
In all Mayas before 2015 (as far as I can check, anyway), calling cmds.ls() with a string that was not a valid Maya object name was allowed. You could for example, call  
    
    
    
    :::python  
    cmds.ls("@")  
    

  
and you'd get back an empty array. In 2015, however, it looks like they have changed the way maya.cmds is converting the string into a dag node reference; it you call the same thing in 2015 you'll get this instead:  
  
    :::python  
    # Error: Syntax error: unexpected end @ at position 1 while parsing:  
    # ; ; @  
    # ; ; ^  
    # : @  
    # Traceback (most recent call last):  
    # ; File "", line 1, in   
    # RuntimeError: Syntax error: unexpected end @ at position 1 while parsing:  
    # ; ; @  
    # ; ; ^  
    # : @ #  
    

  
  
This is a bit more serious than it seems at first glance, because ls is such a common command. Any ls operation which includes a string that starts with anything other than a letter or a number with raise an exception, so there are a lot of places which used to just chug along silently that are going to start raising exceptions.  
  
My workaround is to patch cmds.ls on startup so that it safely renames any bad string before passing them to Maya.  I do this in my bootstrap routine so I don't have to chase down every occurrence of ls anywhere in my code  (1,001 of them, or so PyCharm tells me...).  
  
    
    :::python
    import re  
    import maya.cmds as cmds  
      
    VALID_OBJECT = re.compile("""^[|]?([^a-zA-Z_\?\*\:\|])|([^a-zA-Z0-9_\?\*\:\|\.\[\]])""")  
    as_u = lambda p: p if not hasattr(p, 'addPrefix') else unicode(p)  
      
    def safe_ls(*args, **kwargs):  
        '''  
        Patches maya 2015 cmds.ls so that it does not except when passed illegal name characters.  
        '''  
        if not len(args):  
            return _BASE_LS(**kwargs)  
        if len(args) == 1 and hasattr(args[0], '__iter__'):  
           args = args[0]  
        test_args = [VALID_OBJECT.sub('_', as_u(i)) for i in args]  
        return _BASE_LS(test_args, **kwargs)gs)  
      
    cmds.ls = safe_ls  
    

  
This makes sure that existing code works as it did before and I don't _think_ it will break anything, since the invalid character strings were never going to be ls'ed into anything anyway.  Ordinarily I'm not a big fan of magical behind the scenes fixes but this is a pretty serious change to the behavior of ls which doesn't seem like an intentional upgrade so much as an oversight on Autodesk's part. So, at least until the old behavior comes back I'm gonna try it.  
  
_**Update:** Hat tip to +Robert White for pointing out that the original regex I posted did not handle namespaces. Code above includes the fix.  Never would have figured it out without [Pythex!](https://pythex.org/)_  
  
_**Update 2:** Updated the `safe_ls` procedure to handle more of the allowable syntax in older mayas_  
  


