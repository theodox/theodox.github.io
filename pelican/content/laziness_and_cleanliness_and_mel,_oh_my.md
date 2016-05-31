Title: Laziness and cleanliness and MEL, Oh My.
Date: 2014-10-26 00:18:00.000
Category: blog
Tags: maya, python, programming
Slug: _maya_plugin_commands
Authors: Steve Theodore
Summary: Don't use Mel.  But if you have to, do it like this: with a pythonic wrapper to clean up your strings

The other day I was following a [thread on Tech-Artists](http://tech-artists.org/forum/showthread.php?5077-FBX-Exporting-from-Maya) which reminded me of one of those little Maya things that doesn't really matter, but which drives me bonkers: busted front ends for Maya plugins.  
  
  
When a developer makes a plugin for Maya, they can create new Mel commands as well as new nodes. The new commands will ultimately use the same basic strategy to parse their incoming arguments: Maya will give them an [MArgList](http://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/Maya-SDK/py-ref/class-open-maya-1-1-m-arg-list-html.html) object and they will have to parse out what that means. If the plugin uses an [MSyntax](http://knowledge.autodesk.com/support/maya/getting-started/caas/CloudHelp/cloudhelp/2015/ENU/Maya-SDK/py-ref/class-open-maya-1-1-m-syntax-html.html) and an [MArgParser](http://knowledge.autodesk.com/support/maya/getting-started/caas/CloudHelp/cloudhelp/2015/ENU/Maya-SDK/py-ref/class-open-maya-1-1-m-arg-parser-html.html) to pull the values out then the plugin will behave just like the functions in maya.cmds.  Flags and arguments will be checked the same way that we're used to in the rest of Maya Python.  
  
Unfortunately, there's no law that says the plugin has to do it 'correctly'.  There are more than a few plugins that don't use the standard MSyntax/MArgParser combo and just pull values out of the argument list directly.  The most notorious offender is the FBX Plugin, which generates a ton of commands which all fail to use the standard parsing mechanism.  And, of course, there are also bits of MEL lying around from other sources as well that are a bit painful to call from Python, That's why you see tons of hairy beasts like this:      
    
    import maya.mel as mel  
    mel.eval("FBXExportBakeComplexStart -v " + str(start_frames[x]))  
    mel.eval("FBXExportBakeComplexEnd -v " + str( end_frames[x]))  
    mel.eval("FBXExport -f \"" + get_export_file(x) + ".fbx\"")  
    
  
While this is workable, it's fragile: composing strings inline inside a function call is an invitation to bugs like forgetting an escaped quote (tell me you'd notice that last escape in the final line if it was borked!) or a bit of significant whitespace. It's also harder to meta-program anything that's written like this - you can't create a dictionary of options or a variable length list of arguments when you call the function. Last - but not least, at least not for lousy typists like myself - you can't rely on autocompletion in your IDE to make things quicker and less error prone.  
  
In cases like this it's handy to be able to fall back on a wrapper that will feed the plugin a correctly formatted MEL-style argument but which looks and codes like regular Maya Python. Luckily, you can usually rely on the MEL syntax, even when the plugin's argument parsing is as Python-unfriendly as the FBX plugins: If the MEL version doesn't work either, the whole thing isn't worth rescuing ! -- but if it does then you can Python-ify the front end with a little bit of Python magic to make sure the arguments are passed correctly.  
  
One thing we can do to make this a simple job is to use what's known as _MEL function syntax_.  This is a little-used MEL behavior that lets you call MEL more or less like a traditional computer function, rather than the shell-style script format you usually see. Function syntax uses parentheses and a comma-delimited list of arguments rather than white space. It means that these two calls are identical:  
  
    
    spaceLocator -p 1 2 3 -n "fred";  
    spaceLocator("-p", "1", "2",  "3",  "-n",  "fred");  
    
  
While you probably don't want to type that second one, it's a lot easier to manage if you're trying to turn a bunch of flags and arguments into a MEL command string.  What we'll be doing is creating a function that generates argument strings in the function syntax style and then passes them to MEL for you, allowing you to use the familiar cmds-style arguments and keywords instead of doing all the string assembly in-line with your other code.  
  
The rest of the relevant MEL syntax rules are pretty simple, with one exception we'll touch on later:  
  
* _Everything_ is a string!
* Flags are preceded by a dash
* Flags come first
* Non-flag arguments follow flags
* Multipart values are just a series of single values

That first one may suprise you but it's true - and in our case it's extremely useful. If you're dubious, though, try this in your MEL listener:  
    
    
    polyCube ("-name", "hello", "-width", "999");  
    
  
Implementing these rules in a function turns out to be pretty simple.   
  
    
    import maya.mel  
    def run_mel(cmd, *args, **kwargs):  
        # makes every value into a tuple or list so we can string them together easily  
        unpack = lambda v: v if hasattr(v, '__iter__') else (v,)  
        output = []  
        for k, v in kwargs.items():   
            output.append ("-%s" % k)  
            # if the flag value is True of False, skip it   
            if not v **in (**True**, **False**)**:  
                output.extend (unpack(v))  
      
        for arg in args:  
            output.append (arg)  
      
        quoted = lambda q: '"%s"' % str(q)  
      
        return maya.mel.eval("%s(%s)" % (cmd, ",".join(map(quoted, output))))  
    

  
This function will correctly format a MEL call for almost all circumstances (see the note below for the exception).  For example the irritating FBX commands above become  
    
    
    run_mel("FBXExportBakeComplexStart", v = start_frames[x])  
    run_mel("FBXExportBakeComplexEnd", v = end_frames[x])  
    run_mel("FBXExport", f = get_export_file(x) + ".fbx")  
  
That's a big improvement over all that string assembly (not leastaways because it pushes all the string nonsense into one place where it's easy to find and fix bugs!)   However it's still a bit ugly. Wouldn't it be cleaner and more readable to nudge these guys another step towards looking like real Python?  
  
Luckily that's quite easy to do. After all, the run_mel("command") part of this is the same except for the command names. So why not make a second function that makes functions with the right command names?  This is basically just a tweak on the way decorators work. For example:  
    
    
    def mel_cmd(cmd):  
        def wrap (*args, **kwargs):  
            return run_mel(cmd, *args, **kwargs)  
        return wrap  
    

This takes a MEL command name ("cmd") and makes a new function which calls run_mel using that command. So you can create objects which look and work like Python commands but do all the nasty mel stuff under the hood like this:  
    
    
    FBXExport = mel_cmd("FBXExport")      
    FBXExportBakeComplexStart = mel_cmd("FBXExportBakeComplexStart")  
    FBXExportBakeComplexEnd = mel_cmd("FBXExportBakeComplexEnd")  
    
And call them just like real Python:    
    
    FBXExport(f = "this_is_a_lot_nicer.fbx")  
    
 
All this might seem like a bit of extra work -- and it is, though its not much more work than all those laboriously hand-stitched string concatenations you'd have to do otherwise.

More importantly, this actually is a case where code cleanliness is next to Godliness: keeping rogue MEL from invading your python code is a big boon to long term maintenance.  String assembly is notoriously bug prone: it's way too easy to miss a closing quote, or to append something that's not a string and bring the whole rickety edifice crashing down.  Moreover, exposing all of that stringy stuff to other code makes it impossible to do clever python tricks like passing keyword arguments as dictionaries.  So in this case, a little upfront work is definitely worth it.  
  
Plus, if you're lazy like me you can import these functions in a module and they'll autocomplete. Fat Fingers FTW!   
  
So, if you find this useful, the complete code is [up on Github.](https://gist.github.com/theodox/9a2e2b92867fa82ea328)  
  
### Note

If you're a real mel-head you may have noticed one limitation in the `run_mel()`implementation above.  MEL allows multi-use flags, for commands like  

    ls -type transform -type camera  
  
However the function here doesn't try to figure format arguments that way. In part because it's a relatively rare feature in MEL, but mostly because it doesn't occur in the places I've needed to wrap MEL commands.  It would not be hard to extend the function so you could annotate some flags as being multi-use - if you give it a whirl let me know and I'll post it for others to see.  
  
### Bonus Round
The [Github also has another module](https://gist.github.com/theodox/2b83b1c47a18448d3cbf) which uses the same basic idea (but a slightly different code structure) to wrap that stupid FBX plugin.

