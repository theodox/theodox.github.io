Title: Maya callbacks cheat sheet
Date: 2014-04-23 13:53:00.001
Category: blog
Tags: Maya, GUI, python, programming 
Slug: _maya-callbacks-cheat-sheet
Authors: Steve Theodore
Summary: An overiew of how Maya GUI callbacks work, along with some recommendations for how to set them up neatly.

_Update 5/7/14: Added a note on closures and lambdas_  
  
In [All Your Base Classes](http://techartsurvival.blogspot.com/2014/03/Maya-GUI-ii-all-your-base-classes-are.html),  I suggested that we can do better than the standard callback mechanism for doing Maya event handling.  The limitations of the default method are something I've [complained about before](http://techartsurvival.blogspot.com/2014/02/pity-for-outcast.html), and if you follow these things on [TAO](http://tech-artists.org/forum/showthread.php?3292-Maya-python-UI-acessing-controls-from-external-functions) or CGTalk or [StackOverflow](http://stackoverflow.com/questions/3435128/creating-a-ui-in-Maya-using-python-scripting) it seems pretty clear that a lot of other people have problems with the standard Maya code flow too.  
  
I was planning on devoting the next big post to the event mechanism in [mGUI ](https://github.com/theodox/mGUI). However as I did the spadework for this post I decided it was better to split it up into two parts, since a lot of folks seem to be confused about the right way to manage basic Maya callbacks. Before moving fancy stuff, it's a good idea to make sure the basics are clear. Most vets will already know most of what I'm going over here, but I found the  time spent laying it out for myself a useful exercise  so I figured it would be worth sharing even if it's not revolutionary.  

## Unsolved Mysteries of the Maya.

  
So, let's start by clearing up something that even a lot of old-school Maya coders find a bit mysterious when building GUIs.  
  

[![](http://epGUIdes.com/UnsolvedMysteries/cast.jpg)](http://epGUIdes.com/UnsolvedMysteries/cast.jpg)

  
In vanilla Maya, GUI components fire callbacks - that is to say that when Maya recognizes a user action like a button press or a text entry, it calls a function you've provided. There are two ways you can set this up.  The old-school MEL way is to use a string:  
    
    
    my_button = cmds.button('hello', command = 'print "hello"')  
    
  
In the bad old days of MEL, this was usually fine since most procedures were declared as globals and so they were available everywhere.  
  
Unfortunately, Python's stricter rules about scoping mean that you constantly run into problems with this strategy if you're not careful. For example, this straight python conversion of the Mel paradigm works fine:  
    
      
        def print_hello(_):  
            print "hello"  
      
        my_w = cmds.window()  
        my_col = cmds.columnLayout()  
        my_button = cmds.button('hello', command = "print_hello()")  
        cmds.showWindow(my_w)  
    

  
But try this:  

      
        def show_test_window():  
            def print_hello_again(_):  
                print "hello"  
          
            my_w = cmds.window()  
            my_col = cmds.columnLayout()  
            my_button = cmds.button('hello', command = "print_hello_again()")  
            cmds.showWindow(my_w)  
          
        show_test_window()  
    

When you hit the button you'll be told  

    # Error: NameError: name 'print_hello_again' is not defined #
  

That's because `print_hello_again` is defined in the scope of the _function_, not the scope of the Maya interpreter -- when the callback actually fires, the name is buried away inside of _show_test_window _and can't be found by Maya, at least not using the simple string name.

>That "_" in the functions, by the way, is the standard python symbol for "I have to have a variable here but I intend to ignore it" - it shows up in a lot of these GUI examples because many, though not all, Maya callbacks fire off an argument when they activate.   

This happens all the time to people trying to port old MEL code to Python - snippets that work in the interpreter don't work when converted to functions or split between modules because the string callbacks only execute in the global scope. Luckily, once you realize that the "where is my function" problem is just basic scoping, it's easy to fix. You can forcibly capture the functions you want by just passing them directly to your GUI callbacks instead of using strings, thanks to the magic of python's [first class functions](http://python-history.blogspot.com/2009/02/first-class-everything.html).  You just need to pass the function itself - not a quoted string that looks like the function - to the callback, Thus the previous example becomes
    
    :::python     
    def show_test_window():  
        def print_hello_again(_):  
            print "hello"  
      
        my_w = cmds.window()  
        my_col = cmds.columnLayout()  
        my_button = cmds.button('hello', command = print_hello_again)  
        # note: no quotes and no parens. 
        # You're passing the function as an object!  
        cmds.showWindow(my_w)  
      
    show_test_window()  
    
  
Since you've got the callback in scope when you create the GUI, you're certain to have it when you need it (if by some accident it was out of scope at creation time you'd get an obvious error that you'd have to fix before moving on).  
  
Clear, predictable scoping is why it's almost always the right decision to wrap your GUIs in classes. The class defines a predictable scope so you don't  have to worry about what's loaded or try to cram import statements into your callback functions.   Plus, classes include data storage, so you can keep your data nicely independent of your code. Suppose, for example, you needed to display a different set of greetings beyond the standard "hello world."  With a class you can defer the problem up to the moment of the actual button press with no fancy footwork or complex lambda management:  

      
    :::python
    class Greeter(object):  
        def __init__(self, greeting):  
            self.greeting = greeting  
            self.window = cmds.window()  
            cmds.columnLayout()  
            cmds.button('hello', command = self.greet)  
      
        def show(self):  
                cmds.showWindow(self.window)  
      
            def greet(self, _):  
                print self.greeting  
    

Whatever is stuffed into the Greeter's _greeting_ field will be printed out when the button get's pressed.  
  
## Lambda Lambda Lambda  
  
Of course, sometimes you don't need a full blown class for your callback functions; often you just want to do something simple that doesn't deserve a full function of it's own.  In cases like this, python provides a handy construct called a _lambda_, which is basically a one-line function.  A lambda looks like this:  
    
    :::python      
    multiply = lambda x, y : x * y  
    

  
which is exactly equivalent to:  

    
    :::python     
    def multiply (x, y):  
        return x * y  
    

  
In this example 'multiply' is just a plain old variable name. x and y are the input variables, and the expression to the right of the colon is what the lambda returns.  Lambdas can have any number of arguments, but they don't use the *args / **kwargs variable argument syntax.   
  
The main difference between  lambdas and functions  is that the body of a lambda is a single expression : you can't put flow control (such as loops) or statements which are not evaluable (such as 'print' ) into a lambda.  You can, however, call functions - even functions that return None.  
  
Lambdas are a great way to  cook up throwaway functions. For example:  
    
      
    :::python
    w = cmds.window()  
    cmds.columnLayout()  
    cmd.button('cube', command = lambda x: cmds.polyCube(name = 'new_cube'))  
    cmds.showWindow(w)  
    
  
creates a window with a button which creates a cube when the button is pressed.  You'll probably note that in this case the argument to the lambda is ignored - that's because buttons always fire their callbacks with one argument so the lambda needs to accept one.

> In other examples, you'll recall, I use  a python convention of a single underscore as the 'ignore me' argument.
  
The one thing that makes lambdas interesting (sometimes the '_may you live in interesting times_' sort of interesting) is that they are inside the scope of your functions - which means they can use [closures](http://www.shutupandship.com/2012/01/python-closures-explained.html) to capture variables _before_ they fire.  This can be useful if you want to set up a simple relationship without building a full-on class. This example sets the text of a text widget based on a value you pass it at startup, showing the way closures capture names:  
    
    :::python
    def closure_example_window(value)  
        w = cmds.window()  
        c = cmds.columnLayout()  
        t = cmds.text(label = 'press the button')  
        cmd.button('cube',  c= lambda _: cmds.text(t, e=True, label = value))  
        # captures the name of the text and the value passed in by the user  
        cmds.showWindow(w)  
    
  
However, closures are automatically created by Python when a given scope is closed up - in this example, that would be at the end of the function. The values that are 'closed over' are determined when the function finishes.  Which is usually what you want... unless you're in the habit of re-using variable names:  

    :::python     
    def closure_example_surprise(value)  
        w = cmds.window()  
        c = cmds.columnLayout()  
        t = cmds.text(label = 'press the button')  
        cmd.button('cube', c = lambda _: cmds.text(t, e=True, label = value))  
        value = 'gotcha!'  
        cmds.showWindow(w)  
    

  
When you run this one, the button ignores your value and prints `gotcha` instead of whatever value you passed in! That's because the closure will get its value when the function finishes in line 7, NOT when you first assign it in line 5. This little gotcha is usually a curiosity, but it makes life difficult if you want to, say, assign commands inside a loop. In a case like that you should use functions or callable objects (see below) in preference to lambdas. 
  
## Arguments for the prosecution
  
So, the "where the hell is my function" problem which tends to plague beginners is easy to solve once you look at it the right way.   
  
However, right after you're comfortable with passing functions directly, you immediately realize that's not enough.  It's very common to have multiple GUI controls that do more or less the same thing with different settings such a set of buttons which make different sized objects.    

Alas, while this is easy to understand, it's also kinda ugly to code.  
  
For starters, you might try making lots of little functions:  

    :::python
    def Boxes():  
        def make_big_box(_):  
            cmds.polyCube(h = 10, d=10, w=10)  
      
        def make_med_box(_):  
            cmds.polyCube(h = 5, d=5, w=5)  
     
        def make_sm_box(_):  
            cmds.polyCube(h = 2, d=2, w=2)  
     
        my_w = cmds.window()  
        cmds.columnLayout()  
        cmds.button("small box", c = make_sm_box)  
        cmds.button("medium box", c = make_med_box)  
        cmds.button("large box", c = make_big_box)  
        cmds.showWindow(my_w)  
    

  
Or you could do basically the same thing using lambdas to create temporary functions, which saves on the extra defs but tends to be illegible and tough to debug for complex commands :  

    
      
        def BoxLambdas():  
            my_w = cmds.window()  
            cmds.columnLayout()  
            cmds.button("small box", c = lambda _: cmds.polyCube(d =2, w= 2 , h=2) )  
            cmds.button("medium box",  c = lambda _: cmds.polyCube(d = 10 , w = 5 , h = 5) )  
            cmds.button("large box", c = lambda _: cmds.polyCube(d = 10 , w = 10 , h = 10) )  
            cmds.showWindow(my_w)

_BTW There's that underscore again, in the lambdas, doing the same job: ignoring the callback argument from the buttons_.

  

A third method is to use the Python built-in module `functools`. Functools offsers the [`partial` object](https://docs.python.org/2/library/functools.html#functools.partial), which "freezes" a command and a set of arguments into a callable package.   
    
      
    :::python
    from functools import partial  
    def FuncBoxes():  
    
        # note the comma - the command is an argument to partial!   
        small_box = partial( cmds.polyCube,   d =2, w = 2 , h = 2 )  
        med_box = partial( cmds.polyCube,  d = 5, w = 5 , h = 5 )  
        big_box = partial( cmds.polyCube,  d = 10, w = 10 , h = 10 )  
    
        my_w = cmds.window()  
        cmds.columnLayout()  
        cmds.button("small box", c = lambda _ : small_box())  
        cmds.button("medium box",  c = lambda _ : med_box() )  
        cmds.button("large box", c = lambda _ : big_box()  )  
        cmds.showWindow(my_w)  

  
Partials are handy for cleaning up the messes you'd get from trying to format a complex commands in-line in the middle of your GUI code. This example is a sort of worst case scenario, since Maya buttons always fire with a single argument and cmds.polyCube doesn't like that.  Here I used lambdas  to swallow the arguments (note the telltale underscores). More often you'll be calling your own functions and the syntax is much cleaner and easier to parse:
    
    :::python

    from functools import partial  
    def FuncBoxesClean():  
        def make_box(_, **kwargs):    
           # swallow the argument but keep the keywords...
           cmds.polyCube(**kwargs)  

        small_box = partial( make_box,   d =2, w = 2 , h = 2 )  
        med_box = partial( make_box,  d = 5, w = 5 , h = 5 )  
        big_box = partial( make_box,  d = 10, w = 10 , h = 10 )  

        my_w = cmds.window()  
        cmds.columnLayout()  
        cmds.button("small box", c =  small_box)  
        cmds.button("medium box",  c = med_box )  
        cmds.button("large box", c = big_box  )  
        cmds.showWindow(my_w)  
        

That's far easier on the eyes and less of a nasty tax on future readers, but it requires a knowledge of how partials work.

## Final Summation

So, here's a cheatsheet of the rules for hooking Maya event callbacks:  

  1. Don't use strings for python calls. 
    1. If you're calling MEL, OK: but don't use MEL anyway :)
  2. Pass functions to your callback directly. No quotes, no parens.
    1. If you have a scope problem, you'll see it when you create the GUI; usually you can solve it with an import
  3. If you need to pass arguments to your function in the callback, you have options:
    1. custom mini-functions are clear, but extra work
    2. lambdas are ugly, but workable
    3. partials - especially on top of your own functions - are clean 

  
Now, even if you follow these rules,  its easy for your functional code and your GUI to get in each other's ways.  Creating a lot of throwaway functions is busywork, but formatting commands in-line inside GUI code is error prone and hard to read. Partials are nice for separating data from layout code, but usually come with annoying extra syntax to hide the callback arguments.  
  

### Next Episode...

  
Of course if you've been following the [mGUI](https://github.com/theodox/mGUI)series you'll know where I'm going. (If you haven't, you might want to check [here](http://techartsurvival.blogspot.com/2014/02/pity-for-outcast.html), [here ](http://techartsurvival.blogspot.com/2014/02/rescuing-Maya-GUI-from-itself.html)and [here](http://techartsurvival.blogspot.com/2014/03/Maya-GUI-ii-all-your-base-classes-are.html) before continuing).  Next time out I'lll take a look at how you could get to a cleaner separation of concerns like this:  
    
    
    :::python
    import mGUI.GUI as mg

    def make_box(*args, **kwargs):  
        H,W,D = kwargs['sender'].Tag  
        cmds.polyCube(h = H, d = D, w = W)  
          
    def mGUIBoxes():  
        with mg.Window("boxes") as window:  
            with mg.ColumnLayout("col"):  
                mg.Button("sm", label = "small boxes", tag = (2,2,2) )  
                mg.Button("med", label = "medium boxes", tag = (5,5,5) )  
                mg.Button("lrg", label = "large boxes", tag = (10,10,10) )  
          
        for b in window.col.Controls:  
            b.command += make_box  
        window.show()  
    

  
  
  

