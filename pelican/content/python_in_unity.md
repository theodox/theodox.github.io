Title: Embedding IronPython in Unity = Tech-art hog heaven
Date: 2013-12-21 11:14:00.001
Category: blog
Tags: unity, python, programming, techart
Slug: _python_in_unity
Authors: Steve Theodore
Summary: How to embed an IronPython intepreter into Unity editor tools.

_Update 6/2/2015_ If you are relatively new to Unity, and you're here because you're looking for ways to work in Python rather than C#, you may also want to check out [this 2015 post](http://techartsurvival.blogspot.com/2015/05/boo-who.html) about Boo - the very obscure, but very Python-like language in Mono that lets you write Unity games with fast, compiled code by almost-Python syntax.

You don't work long in games without griping about your engine, and I've got my share of complaints about Unity. But I have to admit that it's the best toy in the world for a classic tech-art geek personality. Unlike bigger, more powerful AAA engines, Unity lets you get in under the hood really quickly. The editor environment is extremely extensible - you can add not just dialogs and buttons but 3d widgets and [diegetic UI ](http://www.thewanderlust.net/blog/2010/03/29/user-interface-design-in-video-games/).   
  
When I first got my hands on Unity I was a bit disappointed to note that, unlike Maya, it doesn't include a built in interactive console environment. The console is a wonderful thing for a TA - it's great for printing out data, lightweight automation of the "find everything in the scene named 'foo' and rename it to 'bar'" variety. So, I thought, is there some way to get this into Unity?  The fact that one could even ask it is a tribute to how flexible Unity is - and as it turned out it was not only possible, it wasn't too hard.  

## You got Python in my Unity!

To start with a console needs some kind of scripting language. Not surprisingly, I wanted to see I could do it in Python. Fortunately, this is ridiculously easy thanks to [IronPython](http://ironpython.codeplex.com/), the dotnet flavor of Python.  IronPython  runs on dotnet, and so does Unity - so it's not tough to plug IronPython into Unity directly.  Here's how:  


1. You need a verstion of IronPython that will run on Unity's version of [Mono ](http://www.mono-project.com/Main_Page), which as of this writing (Unity 4.22 , late 2013) is version 2.6.  By a happy coincidence of naming, that points you at [IronPython 2.6.2](http://ironpython.codeplex.com/downloads/get/159511).  (I've tried later versions but without much luck).
2. Locate the IronPython dlls and the IronPython stdlib in the zip file. You will need  
    _
        - IronPython.dll
        - IronPython.Modules.dll
        - Microsoft.Scripting.Core.dll
        - Microsoft.Scripting.dll
        - Microsoft.Scripting.Debugging.dll
        - Microsoft.Scripting.ExtensionAttribute.dll
        - Microsoft.Dynamic.dll
3. If you want access to the Python stdlib, you'll also need to grab a copy of the python 2.6 /Lib folder -- this is [not distributed with IronPython 2.6](http://techartsurvival.blogspot.com/2013/12/python-in-unity-minor-correction.html).  I unzipped the Python26.zip file from my Maya bin directory into the /Lib folder, taking care to leave the handful of IronPython files already there
4. Copy all of the above into an **Editor/Plugins/Resources** folder in Unity. If you're not sure what that means:
    - Naming a folder _Editor_ tells Unity it only runs in the editor, not at runtime (IronPython _won't_ run inside Unity on IOS devices, since those never run editor code). 
    - Naming it a folder _Plugins_ tells Unity to load dlls from it
    - Naming a folder _Resources_ makes sure it loads before scripts are compiled
    For our application we need all three, hence "Editor/Plugins/Resources/..."  You can stick that whole thing into a top level folder for cleanliness if you want. Note the path names in this example:  
    [![](http://3.bp.blogspot.com/-uHVdPvrDduM/Uq_uSf5ZxNI/AAAAAAAABO0/H0PMXUJlFso/s640/layout.png)](http://3.bp.blogspot.com/-uHVdPvrDduM/Uq_uSf5ZxNI/AAAAAAAABO0/H0PMXUJlFso/s1600/layout.png)
5. Restart Unity and open up MonoDevelop. If you check the Assembly-CSharp Editor info in the Solution panel you should see all of your IronPython DLL's are referenced therein:  
    [![](http://3.bp.blogspot.com/-A_kG1rnuiuY/Uq_vrq1bXhI/AAAAAAAABPA/b9v7p3wxpfw/s400/assembl.png)](http://3.bp.blogspot.com/-A_kG1rnuiuY/Uq_vrq1bXhI/AAAAAAAABPA/b9v7p3wxpfw/s1600/assembl.png)


Once you've verified that the DLL's are in place, its time to test them.  Hosting an IronPython session in another app is much simpler than it sounds. The best resource for how it works is [Michael Foord's Voidspace site](http://www.voidspace.org.uk/ironpython/embedding.shtml) (his [book on IronPython](http://www.manning.com/foord/) is a great resource if you plan on going far with this , btw) . However in overview the process is pretty simple:

  1. Create a [`Microsoft.Hosting.ScriptEngine`]((https://github.com/IronLanguages/main/blob/master/Runtime/Microsoft.Scripting/Hosting/ScriptEngine.cs). This is the actual Python interpreter.
  2. Create a  [`Microsoft.Hosting.ScriptScope`](https://github.com/IronLanguages/main/blob/master/Runtime/Microsoft.Scripting/Hosting/ScriptScope.cs) This corresponds to the global namespace of your interpreter - much like the interpeter namespace in Maya
  3. Create  a [`Microsoft.Hosting.ScriptSource`](https://github.com/IronLanguages/main/blob/master/Runtime/Microsoft.Scripting/Hosting/ScriptSource.cs) using some text you've entered or composed.
  4. Execute the script
  5. Rinse & Repeat. You are in business!


## Script hosting in practice

  
Here's an example .cs script that demostrates the process. Put it in an editor folder so that it can access the Unity Editor assembly (it's probably a good idea to keep it in the editor folder where you have your plugins/resources folder for cleanliness).   
    
     using UnityEngine;    
     using UnityEditor;    
     using IronPython;    
     using IronPython.Modules;    
     using System.Text;    
     // derive from EditorWindow for convenience, but this is just a fire-n-forget script    
     public class ScriptExample : EditorWindow {    
         [MenuItem("Python/HelloWorld")]    
         public static void ScriptTest()    
         {    
             // create the engine    
             var ScriptEngine = IronPython.Hosting.Python.CreateEngine();    
             // and the scope (ie, the python namespace)    
             var ScriptScope = ScriptEngine.CreateScope();    
             // execute a string in the interpreter and grab the variable    
             string example = "output = 'hello world'";    
             var ScriptSource = ScriptEngine.CreateScriptSourceFromString(example);    
             ScriptSource.Execute(ScriptScope);    
             string came_from_script = ScriptScope.GetVariable<string>("output");    
             // Should be what we put into 'output' in the script.    
             Debug.Log(came_from_script);                
         }    
     }    
  
  
When it compiles you'll get a menu items that activates the script.  When you hit it you should get a debug printout in your console like so.  

[![](http://4.bp.blogspot.com/-OHCa77GIxGA/UrEnF442YzI/AAAAAAAABPQ/nYBOKL4W1ZI/s1600/hello+world.jpg)](http://4.bp.blogspot.com/-OHCa77GIxGA/UrEnF442YzI/AAAAAAAABPQ/nYBOKL4W1ZI/s1600/hello+world.jpg)

  
Like the Maya python interpreter, you need to import the appropriate names so that you can get to them in scripts (it's always rather boggled my mind that Maya's own interpreter requires you to import cmds or pymel _every single freakin' time_.  IronPython lets you import dotnet assemblies as if they were python modules, and since Unity and the Unity Editor are dotnet assemblies you can get access to the entire Unity environment just by importing them into your interpreter.   
  
First, we need to load the assemblies to make them available to the intpereter itself.  In dotnet land that's done by loading an assembly.  Once an assembly is loaded, it can be imported using typical Python syntax  
  
    
     [MenuItem("Python/HelloWorldRuntime")]    
     public static void UnityScriptTest()    
     {    
         // create the engine like last time    
         var ScriptEngine = IronPython.Hosting.Python.CreateEngine();    
         var ScriptScope = ScriptEngine.CreateScope();    
         // load the assemblies for unity, using the types of GameObject    
         // and Editor so we don't have to hardcoded paths    
         ScriptEngine.Runtime.LoadAssembly(typeof(GameObject).Assembly);    
         ScriptEngine.Runtime.LoadAssembly(typeof(Editor).Assembly);    
         StringBuilder example = new StringBuilder();    
         example.AppendLine("import UnityEngine as unity");    
         example.AppendLine("import UnityEditor as editor");    
         example.AppendLine("unity.Debug.Log(\"hello from inside the editor\")");    
         var ScriptSource = ScriptEngine.CreateScriptSourceFromString(example.ToString());    
         ScriptSource.Execute(ScriptScope);    
     }    
    

Running that one generates another console message - but this time from inside the script!  

[![](http://3.bp.blogspot.com/-S6g8MqlQ4gg/UrEub33XuBI/AAAAAAAABPg/kJmAVPdZtAI/s1600/hello+2.png)](http://3.bp.blogspot.com/-S6g8MqlQ4gg/UrEub33XuBI/AAAAAAAABPg/kJmAVPdZtAI/s1600/hello+2.png)

## Next time: building a console
  
That may not seem like much, but in reality it's a big deal. You've got a working script interpreter running in Unity now, with all the power of Python and access to the innards of the Unity environment.  What remains is to build a decent interactive environment. 

If you're content with something barebones, you can whip up a simple UI to allow you to type code into a text field and see the results in another text block.  That may be enough for some purposes (hell, half the 3d packages on the market do little more than that).  However a more featured editor is a little tougher and involves a  little hacking to work around the limitations of Unity's GUI text handling, which makes it a bit involved for a single post. I'll save that one for next time  
  

