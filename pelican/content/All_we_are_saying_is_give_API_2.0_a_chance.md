Title: All we are saying is give API 2.0 a chance
Date: 2014-12-12 19:42:00.000
Category: blog
Tags: maya, python, programming 
Slug: api-2
Authors: Steve Theodore
Summary: Maya's api version 2.0 is finally coming of age

Doing all this math-related posting has reminded me of something I've been meaning to write up:  
  
Maya's [python API 2.0,](http://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2015/ENU/Maya-SDK/py-ref/index-html.html) first introduced in the 2013 version, got off to a rocky start. People complained about [missing functions](http://stackoverflow.com/questions/20232835/maya-python-api-2-0-has-no-mitdag-so-how-traverse-dag-graph) and [missing modules](http://jeremyyk.com/tutorials/maya-s-python-api-2-0-).  It uses (mostly) the same function and class names as the original OpenMaya Python, which is a recipe for confusion. The documentation is pretty confusing too, since it points at the original C++ docs and leaves it up to you to do much of the translation in your head.    However....  
  
  
One thing that API 2 definitely does right is to eliminate the dreaded _[MScriptUtil](http://techartsurvival.blogspot.com/2014/03/if-your-maya-python-api-is-crashing.html), _with its ugly and confusing interface and all of the opportunities for failures that it includes.  I've been busy porting over a bunch of geometry utilities to the new API and I'm routinely finding that stuff like this:  
  
  

    
    
    def APIVector( iterable, normal=False ):  
        '''  
        return an iterable as an OpenMaya MVector  
          
        if iterable is an openMaya MVector, returns untouched  
        '''  
        if isinstance( iterable, OpenMaya.MVector ):  
            o_vector = iterable  
        else:  
            assert len( iterable ) == 3, "argument to APIVector must have 3 entries"  
            v_util = OpenMaya.MScriptUtil()  
            it = list( copy( iterable ) )  
            v_util.createFromDouble( iterable[0], iterable[1], iterable[2] )  
            o_vector = OpenMaya.MVector( v_util.asDoublePtr() )  
      
        if normal:  
            o_vector = o_vector.normal ()  
        return o_vector  
    
  
Turns into to this:  

    
    
    def APIVector(*iterable, **kwargs):
    
    
        result = None  
        try:  
            result = api2.MVector(iterable)  
        except ValueError:  
            result = api2.MVector(iterable[0])  
        finally:  
            if kwargs.pop('normal', False):  
                result.normalize()  
            return result  
    

  
In other words, one reasonable line for 4 icky ones.  
  
Plus, the new versions are generally more pythonic - the API 2 version of `MVector`, for example supports both dot-access, bracket access, and iteration over the vector components (though, annoyingly, _not_ slicing).  
  
It's certainly not all perfect. You do have to be very careful about mixing API 1 and API 2 code in the same functions - even though they are both wrapping the same C++ underpinnings they are are mutually incompatible.  Some things are still cumbersome -- converting strings to MSelectionList items to MObjects to MFNs is still a waste of good brain cells -- but it's a step in the right direction. I'll post more as I know more.  
  
By the way, I spent several minutes surfing around for a funny image to wrap up on, I even did a meme-generator.com thing with The Most Interesting Man In The World saying something dismissive about MScriptUtil.  And then I thought... "What's the point."  
  
See? Progress _is_ possible.   Or maybe I'm just getting old. In Internet Years I'm already like 7,303.  
  
  
  


