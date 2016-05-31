Title: Boo Who?
Date: 2015-05-31 22:02:00.000
Category: blog
Tags: programming, boo
Slug: _boo-who
Authors: Steve Theodore
Summary: A quick introduction to Boo, a python-like language for the CLR

##Boo!

Did I scare you?

[![](http://1.bp.blogspot.com/-OFk47U8-b9E/VWvmUwg7gII/AAAAAAABL6E/61gYBKYRRN4/s400/medium.png)](http://1.bp.blogspot.com/-OFk47U8-b9E/VWvmUwg7gII/AAAAAAABL6E/61gYBKYRRN4/s1600/medium.png)

Evidently somebody's scared: the [Boo language](https://github.com/bamboo/boo/wiki), which has been a part of Unity for several years, is going to be removed from the Unity documentation in favor of C#. 

The reason is pretty simple, as this graph explains:

![](http://blogs.unity3d.com/wp-content/uploads/2014/09/graph3.png)

For a lot of Unity developers (99.56% of them, apparently) this is non-news; Boo never really garnered much of a following in the Unity community. For new developers and recent grads, C# is an easy and very well documented option; for former web debs moving to mobile apps, UnityScript feels JavaScript-y enough to ease into a new environment. Boo, on the other hand, never got much traction: it's got a small but passionate community but it never garnered enough momentum to break out of its niche. 

##Boo Hoo

Now, I'm kind of a sucker for hopeless causes, so almost inevitably this news inclined me to revisit Boo, which I've toyed with a few times but never really tried to learn. I had to write a lot of C# for [Moonrise](http://store.steampowered.com/app/351040/) and it made me long for the clarity and concision of Python. Even though C# is a perfectly capable language with lots of modern features (closures, firest class functions, etc) it's still very chatty. The tantalizing promise of Boo - not completely fulfilled, but pretty close, is that it combines both: the performance, runtime type safety, and intimate access to Unity that C# offers in a language not deformed by punctuation and rendered ridiculous by overly wordy syntax.

Here's the aesthetic differences in a nutshell:

##Boo
    
    
    import UnityEngine  
      
    class JumpingMovementController(MonoBehaviour):   
      
     _HORIZ = 'Horizontal'  
     _VERT = 'Vertical'  
     _JUMP = 'Jump'  
     _Momentum = 0.0  
     _Gravity = 2.0  
     public _Speed = 1.0  
     public _JumpSpeed = 1.5  
      
     def Update():   
      frame_speed = _Speed * Time.deltaTime   
      
      if transform.position.y == 0 :  
       _Momentum += Input.GetAxis(_JUMP) * _JumpSpeed  
      
      up =  _Momentum * Time.deltaTime  
      left_right = Input.GetAxis(_HORIZ) * frame_speed  
      forward_back = Input.GetAxis(_VERT) * frame_speed  
      transform.Translate(Vector3(left_right, up, forward_back), Space.Self)  
      
     def LateUpdate():  
      if transform.position.y > 0:  
       _Momentum -= _Gravity * Time.deltaTime;  
      else:  
       _Momentum = 0;  
       vp = Vector3(transform.position.x, 0, transform.position.z)  
       transform.position = vp  
    

##C\#
    
    
    using UnityEngine;  
    using System;  
      
    public class JumpingMovementController(MonoBehaviour)  
    {   
      
        const static string _HORIZ = "Horizontal";  
        const static string _VERT = "Vertical";  
        const static string _JUMP = "Jump";  
        var _Momentum = 0.0f;  
        var _Gravity = 2.0f;  
        public var _Speed = 1.0f;  
        public var _JumpSpeed = 1.5f;  
      
      
        void Update()  
        {  
            var frame_speed = _Speed * Time.deltaTime   
      
            if (transform.position.y == 0)   
            {  
                _Momentum += Input.GetAxis(_JUMP) * _JumpSpeed;  
            }  
      
            var up =  _Momentum * Time.deltaTime;  
            var left_right = Input.GetAxis(_HORIZ) * frame_speed;  
            var forward_back = Input.GetAxis(_VERT) * frame_speed;  
            transform.Translate(new (Vector3(left_right, up, forward_back)), Space.Self);  
        }  
      
        void LateUpdate()  
        {  
            if (transform.position.y > 0)   
            {  
                _Momentum -= _Gravity * Time.deltaTime;  
            }  
            else   
            {  
                _Momentum = 0;  
                vp = new Vector3(transform.position.x, 0, transform.position.z);  
                transform.position = vp;  
            }  
        }  
    }  
    

I just can't shake the feeling that the first code is something I don't mind reading and writing while the latter is a chore. It's also a whopping 45% more typing for the same result. And that delta only gets bigger if you want to try something a little more complicated: Boo supports offers the same list comprehension syntax as Python, so you can write:
    
    
        addresses = [(x,y) for x in range(3) for y in range(3)]  
    

where in C# you'd either get 6 lines of for-loops and nested brackets, or you'd have to use Linq. Even in the most compact form I can manage it's still much wordier:
    
    
            var xs = Enumerable.Range(0, 3).ToList();  
            var ys = Enumerable.Range(0, 3).ToList();  
            var addresses = (from x in xs  
                             from y in ys  
                             select new Tuple<int,int>(x, y)).ToList();        
    

to get to the same place. 

## Why Boother?

A hardcore programmer might object that this is "all just syntax". That's true - but since my everyday experience of working with a language is about 90% syntax I don't feel like it's fair to dismiss that concern as if it were irrelevant. That said, it can't be denied that modern C# 4 includes many language constructs that earlier versions of the language lacked: things like `var` inferred variables, lambdas, closures, and named default arguments. These things all help make the code less chatty and more legilble: If you're a _good_ C# programmer you can write very terse, expressive code that's not absurdly wordy. 

Apart from those stupid curly brackets.

On the other hand, the "culture" of the language was set in place before those kinds of features were added. The C# ethos definitely prefers the verbose to the understated, the extremely explicit to the implied.This isn't a terrible decision - like Java, it's a language designed to be used by huge teams of enterprise programmers working on titanic projects where only a few people see the whole project scope and most coders are locked away in cubicles on the 18th floor working on isolated modules to be used by other coders they will never meet.That's why C#'s obssession with visibility management and highly-specified behavior makes sense.C# is a language that's all about apportioning blame: it forces everything to be very explicit so you know which of the 6000 drones working on your enterprise app to bleame when things go wrong.

In the context of a small game or a solo project, though, the Pythonic ethic of "we're all adults here" seems more natural and productive.Besides, for hobby projects and one offs fun is a totally legitimate concern: making minigames is something that gets crammed into nooks and crannies left over by work, kids and keeping the house from falling down around my ears.So fun is a totally legit criterion for selecting a language.

And Boo is definitely more _fun_ than C#. 

## Boo Who?

Like many Pythoneers, I've always nursed a secret hunger for the magical button that would take all my tight, laconic Python code and magically make it perform like a "real" language. Boo is not the magic button, but it's a pretty good preview of what that might look like. As you can see from the code samples above, it looks and feels a lot like Python but under the hood is has similar performance and compile-time constraints to C#: in other words, Boo code can run as much as 20X faster than Python.

That's what makes Boo so tantalizing. It is _almost_ Python, but you can write Unity games, Winforms apps, or even cross-platform DLLS with it. Plus, since Boo runs on the same dotnet CLR as C#, it runs on any platform with the DotNet framework or Mono installed, so a compiled Boo program can run on Windows, Macs, or Linux boxes. There's even an interactice shell so you can do one-offs and experiment, just like Python. But - unlike Python - you get the performance gains that come from a compiled, statically typed language.

Typing and the compiler are the key difference between Boo and Python. The a compiler makes sure that all of your variables, return values and method signatures line up and uses that knowledge to optimize the final runtime code for you. You can do this in Python:
    
    
    fred = 1   
    fred = fred +  1  
    print fred  
    # 2  
    fred = "fred"  
    fred = fred + " flintstone"  
    print fred  
    # fred flintstone  
    

In Boo, however, you'll get an error when you try to change `fred` from an integer value to a string:
    
    
    fred = 1  
    fred = fred +1   
    fred = "fred"  
    #------^  
    #ERROR: Cannot convert `string` to `int`  
    

In old-school C#, this was made obvious that all variables and to declare a type:
    
    
    int fred = 1;  
    

In more modern C# you can use the `var` keyword to make the compiler guess what type you want based on the initial input: when you give it
    
    
    var fred = 1;  
    

it sees that fred has an integer in it, and treats fred as an integer from then on. If you assign the variable with the result of a method call or another variable, C# uses the expected type of that return value to set the variable type. Boo does more or less the same thing: it uses the assignment value to guess the type of a variable. You can specify it explicitly if you prefer by using the `as` keyword: 
    
    
    barney as string  
    barney = "barney"   #OK  
    

The same syntax is used to specify inputs in methods and returns:
    
    
    def bedrock (name as string) as string:  
        return name + "rock"  
      
    def inferred_return_type(name as string):  
        return name + "inferred"  
        # if the compiler can guess the output type  
        # you don't need to 'as' it  
    

Once you get out of the habit of re-using variables with different types, this is usually not too bad: 95% of the time the inference "just works" and you can write code that focuses on logic and good design instead of worrying about the types. The other 5% of the time, however, is often very frustrating. It's particularly tough when Boo's Python-like, but not _exactly_ Python behavior trips you up. Consider this little puzzle:
    
    
    def sum (values as (int)) # expect an integer tuple  
        result = 0  
        for v in values:  
            result += v  
        return v  
      
    # works as expected for this case:  
    example = (1,2,3)  
    sum(example)  
    # 6  
    

However it can be broken if your input list isn't all of the same type:
    
    
    example2 = (1,2,3,"X")   
    sum(example2)  
    # ERROR: the best overload to the method sum((int)) is not compatible with the argument list '((object))'  
    

That's not entirely shocking: the compiler saw a mixed list in example2 and return and array of type `object` (as in C#, `object` is the base class of all types). So it is right to reject that as an argument for an int-specific function. Here's where it gets odd:
    
    
    #reassign  
    example2 = (1,2,3,4)  
    sum (example2)  
    # 10  
    

This time the compiler "helpfully" casts that array to an array of ints because it can. This is not a crazy behavior, but it's definitely going to raise some issues where test code works fine but production code contans bad values. The only way to be sure that things are what they seem is to force them into the right types at declaration time:
    
    
    example3 as (int) == (1,2,3,4,5)  
    sum(example3)  
    # 15  
      
    example3 = (1,2,3,"one hundred")  
    #----------^  
    # ERROR: Cannot convert `(object)` to `(int)`  
    

This example highlights both the usefulness and the limitations of type inference: If you want a statically typed language (and all the compiler tricks that make it speedier than Python) you do have to think about how to manage your types. There's no way around it. If you've got enough C# experience, you can look at Boo as a neat way of writing speedy, statically typed code with less typing and more syntactic freedom - but if you're looking at it from the standpoint of loosey-goosey Pythonista it can seem like a lot of hurdles to jump. 

My (unscientific) impression is that a lot of people from the Python world come over to Boo and the familiar look of the code gives them a false sense of security. It's easy to write simple bits of code until the subtleties of type management bite you in the behind, and then to give up in frustration when things seem to get cluttered and uptight.

It is, however, part of the territory: lots of other tools for speeding up Python such as [Cython](http://cython.org/) expect the same kind of attention to variable types: here's a sample from Cython
    
    
    def f(double x):  
        return x**2-x  
      
    def integrate_f(double a, double b, int N):  
        cdef int i  
        cdef double s, dx  
        s = 0  
        dx = (b-a)/N  
        for i in range(N):  
            s += f(a+i*dx)  
        return s * dx  
    

which is just as finicky as C# or Boo.

For me, at any rate, spending more than a year doing C# as a regular part of work made fiddling around with Boo much easier and more productive. The type management hassles strike me as inevitable, or even natural, after a year of typing verbose C# variable types. On the other hand the cleanliness of the layout, the lack of extraneous punctuation, and the clealiness of list comprehensions and Python style loops never gets old.

While there are plenty of minor gotchas, and a few important high-level rules that can't be forgotten, Boo development flows in with an almost Pythonic fluency. If you put in the time to figure out the type inference behavior and add the annotations, you can get code thats _almost_ as flexible as Python and _almost_ as performant as C# - which, for my kind of pet projects is a great compromise. 

## Boo-ty is in the eye of the beholder

TL;DR: I've gotten pretty fond of Boo. Above all, it serves me well for noodling around in Unity where the API is mostly identical but the logic is cleaner, shorter and easier to read than the same code in C#. Translating the docs is rarely more than trivial, and the very narrow scope of a typical Unity code chunk keeps me from any of Boo's rough edges.

Another hurdle for many Pythonistas, though one which does not matter in the the context of Unity games, is the lack of the Python standard library. About 70% of what you can do with the 'batteries included' in Python can, however, be replicated using the [dotnet Base Class Library](https://msdn.microsoft.com/en-us/library/hfa3fa08%28v=vs.110%29.aspx) if you're running Boo on a Windows box (on Linux or OSX the percentage is lower: Mono has its own base class library but it's not a complete replica of the one from Microsoft). For many tools tasks and projects, this is more than enough: you'll be able to read and write XML, to decrypt JSON, to talk to an http server and so on although the function names and APIs will vary. I have to admit I prefer the Python toolkit to the dotnet one, which reflects the same bureaucratic mindset that I dislike in C#'s design, but it's still a big, robust set of tools. You can also use anything that's available as a dotnet DLL. Almost anything advertised as a usable with C# will work with Boo.

All that said, I'd definitely think twice before basing a commercial Unity project or a critical pipeline component on Boo. There does seem to be a small but measurable perfromance penalty compared to C# (the performance is, however, pretty much on par with that of UnityScript). More importantly, the Boo's biggest weakness is documentation: with a small community and (from now on) no docs on the Unity site, finding your way around in the language at first is pretty awkward. The [documentation](https://github.com/bamboo/boo/wiki) is a sporadic, volunteer effort with some glaring holes - it doesn't help that Google still sends you to the moribund Boo site on [codehaus](http://boo.codehaus.org/) instead of the current docs, which are in a [Github Wiki](https://github.com/bamboo/boo/wiki). The language is officially at version 0.9.4.9 and hasn't incremented in a long time: it's still getting commits from the original author and few other devs but it's a much smaller project than, say, IronPython. In short, it's a cool language that has not found it's audience yet, and unless it does it will remain a niche player. 

Still, it's pretty cool too. If, after those caveats, it still sounds interesting, you'll be relieved to know that Boo is not really 'going away': For the forseeable future, the language will still work in Unity, Boo, like C# and UnityScript, runs on [Mono](http://www.mono-project.com/), much as Java runs on the JVM. Unity doesn't distinguish between the source of Mono assemblies: you can still use Boo, and even more exotic dotnet languages such as F# (though not, alas, IronPython!) in Unity today. The only practical result of Unity's decision to sunset Boo support is the disappearance of the Boo documentation from the Unity website - which , to be honest was rarely adequate - and the lack of a 'create Boo script' menu item. Dropping a boo script into your assets folder, however still creates runnable code, and it should continue to do so for the forseeable future. 

There's some question about how Unity's new cross-platform compiler technology, [IL2CPP](http://blogs.unity3d.com/2014/05/20/the-future-of-scripting-in-unity/) will handle Boo. In principle, since it compiles the byte code produced by Mono rather than the original source, it too should work with any CLR language, be it Boo or F# or what have you. I've been able to compile Boo code to Unity WebGL games, which use IL2CPP, without obvious problems although I haven't done anything like a scientific test. It's not beyond belief that bugs which occur only in non-C#, non-UnityScript IL code may go unfixed. And, of course, it's impossible to say what will happen after Unity 5 - technology, particularly in games, moves too fast for confident future predictions. However, It seems pretty clear Boo will be working in Unity for a while to come even though it is being demoted from "officially supported" status to the same kind of l33t hacker underworld as functional languages. 

## Boo-Curious?

If you've got Unity installed already, you've already got everything you need to play with Boo. Just create a text file with a ".boo" extension inside a Unity project and you can write Unity components in Boo. If you don't have Unity, You can also [download Mono directly](http://www.mono-project.com/download/), which installs MonoDevelop and Boo automatically. 

If you're not fond of MonoDevelop - an editor for which I have… mixed… feelings - You can write Boo using [Sublime Text](http://www.sublimetext.com/), which has a Boo syntax higlighting package and can run Boo compiles for you. 

If you're curious but don't want to take the plunge, you can see the language for yourself and play with it online, using this [interactive repl](http://tryboo.pollinimini.net/)

The documentation - which (be warned!) is incomplete and not always up to date - is in the [Boo Project GitHub wiki](https://github.com/bamboo/boo/wiki). There's an older site at [boo.codehaus.org](http://boo.codehaus.org/) which is tends to show up on the Google results but has _mostly_ been ported to the github. In cases of conflicting information, the GitGub wiki is likelier to be right. There's also a [Google Group](https://groups.google.com/forum/#!forum/boolang) and a small pool of questions on [StackOverflow](http://stackoverflow.com/questions/tagged/boo)

If you're a hardcore type, you can also download and rebuild [the source for the entire Boo language](https://github.com/bamboo/boo) yourself from GitHub. Lastly, you might want to check out [BooJS](https://github.com/drslump/BooJS), a project which aims to compile Boo into JavaScript.

