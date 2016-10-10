Title: Maya GUI II: All Your Base Classes Are Belong To Us
Date: 2014-03-28 09:30:00.000
Category: blog
Tags: Maya, python, GUI, programming, mGui
Slug: all_your_base
Authors: Steve Theodore
Summary: Introducing `mGui`, a module for making Maya GUI coding more pythonic and less infuriating.

> I've left this article mostly intact, but some elements of the syntax have changed in mGui 2.0.  The big changes, generally speaking, are under the hood -- but the 2.0 version uses pep-8 style naming so the capital letters for properties have been replaced with lower-case ones. See the [mGui updates](mGui_updates_2) post for a more up-to-date view of the current mGui syntax. mGui 2 will be the main line in GitHub after 10-10-2016.


In [Rescuing Maya GUI From Itself](rescuing_maya_gui_from_itself.html) I talked in some detail about how to use descriptors and metaclasses to create a wrapper for the Maya GUI toolkit that, er, sucks less than the default implementation. I also strove mightily to include a lot of more or less irrelevant references to [Thunderbirds](http://www.youtube.com/watch?v=BfIAKj3Gl1E). This time out I want to detail what a working implementation of the ideas I sketched out there looks like.  
![](http://fc06.deviantart.net/fs70/f/2010/282/6/a/all_your_base_by_ultimathegod-d30fu0f.jpg)  

I think this time the irrelevant thematic gloss will come from [All Your Base Are Belong To Us](http://knowyourmeme.com/memes/all-your-base-are-belong-to-us) jokes. Because (a), we’re talking about base classes, (b) what could be more retro and 90’s than Maya’s GUI system, and (c) **For Great Justice, Make All Zig!**  

I’ve put my current stab at a comprehensive implementation up on Github, in the form of the [mGUI project](https://github.com/theodox/mGUI) , where you can poke at it to your heart’s content. The whole project is there, and it’s all free to use under the MIT, [_‘do-what-thou-wilt-but-keep-the-copyright-notice’_](http://opensource.org/licenses/MIT) license. Enjoy! I should warn you, though, that this is still W.I.P code, and is evolving all the time! Use it at your own risk – things may change a lot before its really ‘ready’.   

## All Your Properties Are Belong To Our Base Class

![](http://fc00.deviantart.net/fs30/f/2008/064/8/0/All_your_base_are_belong_to_us_by_Sky_roxorz_815.png) 

What we’re shooting for is a library that provides all of Maya;’s GUI widgets in a clean, pythonic way without making anybody learn too much new stuff. If all goes well, the result is a cleaned up and more efficient version of things most of us already know. You can also treat this an template for how you might want to to wrap other aspects of Maya – say, rendering or rigging – in cleaner code.  

From last time, we know we can wrap a Maya GUI component in a class which uses [descriptors](http://nbviewer.ipython.org/urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb) to make conventional property access work. The main thing we’re going to be delivering in this installment is a slew of classes that have the right property descriptors to replicate the Maya GUI toolkit. We’ll be using the metaclass system we showed earlier to populate the classes (if none of this makes sense, you probably want to [hop back to the previous blog entry](rescuing_maya_gui_from_itself.html) before following along).  
To keep things simple and minimize the boilerplate, we’ll want to derive all of our concrete classes – the widgets and layouts and so on – from a single base. This helps the code simple and ensure that the features we add work the same way for the whole library. We’ll add a second class later to handle some details specific to layouts, but that will derive from the base class.  
Before we look at the details of the base class, we should think a little more about the properties. In the last installment, we treated all properties the same way - as generic wrappers around Maya.cmds. In a production setting, though, we want to distinGUIsh between 3 types of properties:  

#### Regular properties
These are just wrapped accesses to commands, like we demonstrated last week. They use the same ControlProperty class as we used last time to call commands on our GUI widgets.

#### Read-only properties
A small number of Maya GUI commands are read-only. It would be nice and more pythonic to make sure that these behave appropriately. So, ControlProperty has been tweaked with a flag that allows it to operate as a read-only property; otherwise it’s just the same descriptor we talked about last time out. ]

#### Callbacks
This one is a bit more involved. I’ve already complained about the weaknesses of the event model in Maya GUI. Cleaning it up starts with knowing which properties are callback properties and treating them accordingly. 
To differentiate between these three types of properties, we need to tweak our old metaclass so that it can distinGUIsh between regular properties, read-only properties, and event properties. Luckily the necessary changes are super simple - basically, we’ll take out the hard-coded list of properties we used before and allow every incoming class to declare a list of properties, a list of read-onlies, and a list of callbacks. (if you want to compare, the version from last time is [here](https://gist.github.com/theodox/9106311)):  

## Somebody Set Us Up The Bomb!

Before getting into the nitty-gritty of our overall widget class, I want to make a side noted about the special properties used for the callbacks. These CallbackProperty descriptors are slightly different from the familiar ControlProperty. Their job is to de-couple the Maya GUI widget from the commands it fires. They create special delegate objects which will intercept callbacks fired by our GUI objects.  

If you have experimented a little with last time’s code, you may already have seen that it works just as well for callbacks and commands as for other properties. So you may wonder why we should bother to treat callbacks differently. What’s the point?  

There are two main reasons this is a useful complication.  
First, and most usefully, event delegates make it easier to add your callbacks after you lay out your GUI, rather than forcing you to interleave your code logic with the process of building forms and layouts. De-coupling the functional code form the graphic display makes for more readable and more maintainable code. It also makes it possible for you to reuse fairly generic layouts with different back ends. In pseudo-code:  

    Layout  
       Layout  
         ButtonA  
         ButtonB  
       Layout  
         ButtonC  
         ListA  
      
    ButtonA deletes selected item from ListA  
    ButtonB renames selected item from ListA  
    ButtonC adds new item to ListA  
    
  
as opposed to  

    
    Layout  
       Layout   
         ButtonA.   
            I'm going to delete something from the list when it gets made  
         ButtonB  
            I'm going to rename something in the list when it gets made  
       Layout  
         ButtonC  
            I'm going to add something to the list when it gets made  
         ListA  
    
Keeping the functional bits separate makes it easy to, say, split the purely visual layout details into a separate file, but more importantly makes it clear whats an administrative detail and what’s actual functionality.  
On a second, more tactical level the proxies also allow you to attach more than one function to a callback. It’s pretty common, for example, that you the act of want selecting an item in a list to select object in the Maya scene, but also to enable some relevant controls and maybe check with a database or talk to source control. Using an event proxy lets you handle those different tasks in three separate functions instead of one big monster that mixes up lots of UI feedback and other concerns.  

![](https://images-blogger-opensocial.googleusercontent.com/gadgets/proxy?url=http%3A%2F%2F3.bp.blogspot.com%2F-OFyQFgarV3I%2FUmU6BLY68jI%2FAAAAAAAAA6g%2FHSk55Z2R5Io%2Fs1600%2FPantallazo-1.png&container=blogger&gadget=a&rewriteMime=image%2F*)  

If you’re familiar with QT you’ll rexognize that event delegates are basically QT “Signals”  

So that’s why the extra complexity is worth it.  

The actual workings of the proxy class are documented in the [events.py file in the Github project](https://github.com/theodox/mGUI/blob/master/mGUI/events.py); I’ll get back to how those work in a future post. Details aside, they key takeaway for right now is that this setup helps us move towards GUI code that’s more declarative. That’s the other reason why `button.label = “Reset”` is better than `cmds.Button(self.activeButton, e=True, l="Reset"`– it’s not just less typing. The real value comes from treating the GUI layout as **data** rather than **code**. That means you can concentrate on the actual work of your tools rather than the fiddly details of highlighting buttons or whatever.  
Last but not least - by standardizing on the event mechanism we have an easy way to standardize the information that comes with the callback events for very little extra works. So, for example, all of the callbacks include a dictionary of keyword arguments when they fire - and the dictionary includes a reference to the widget that fired the event. That way it’s easy to write a generic event handler and not have to manually bind the firing control to a callback function.  

> While we’re on the topic of de-coupling: Wouldn’t it be nice to separate out the details of the visuals (“what color is that button?”) from the structure of the forms and layouts?. Spoiler alert! This is a topic for a future post – but the curious might want to check out [styles.py in the GitHub](https://github.com/theodox/mGUI/blob/master/mGUI/styles.py)

## Think ahead

![](http://www.geekytattoos.com/wp-content/uploads/2009/04/all-your-base-tattoo.jpg)  
> How the hell are you going to explain THAT to your grandchildren?  
The obvious lession is THINK AHEAD  
  
---

So, we’ve covered our improved property descriptors, and now it’s time to set up our base class.  

This is a great opportunity to do some plumbing for more efficient coding. However it’s also a temptation – when the desire to sneak everything under the sun into your base classes is a recipe for monster code and untraceable bugs. This design should be as simple as we can make it.  

Still, there are a couple of things that it would be nice to put into the base class - they are all very general (as befits base-class functions) and they are all common to any GUI tasks.  

### Tags

In most GUI systems, you can attach any arbitrary data you want to a widget. For example, you might want to have an array of buttons that all did the same thing with slightly different values, say moving an object by different amounts.  In vanilla Maya, you have to encapsulate the data into your command call: With a tag attached to the buttons, on the other hand, you can write a script that just says "move the target by the amount in this button’s tag", which is much easier to maintain and more flexible. And as we just pointed out, the event mechanism always sends a reference to the control which owns an event when it fires, so it’s easy to get to the right tag when you want it.  

###  A real name

Having explicit names for your pieces is very handy, particularly in large, deeply nested systems like a GUI..  

In conventional Maya coding the names are critical, since they are your only way of contacting the GUI after it’s built. They are also unpredictable, because of Maya’s habit of renaming items to give them unique path names. Luckily for us we don’t need to rely on the widget names from Maya, since we’re managing the GUI items under the hood inside our wrappers. This gets us off the hook for creating and managing variables to capture the results of every GUI command under the sun.  

That said, names are still useful in a big complex system. So, to make it really clear how to find one of our wrappers inside a GUI layout it makes sense to ask for an explicit name passed in as the first argument - that way it’s totally clear what the control is intended to be. 

> Note: This system changes slightly in mGui 2.0 (spring, 2016).  The newer syntax allows you to auto-assign keys using local variable names, which involves less redundancy than the original way. Explicit keys still work, however.

There are, of course, plenty of controls you don’t really care about once they’re made: help text, spaces, separators and so on. To avoid making users have to invent names for those guys, we should let users pass in 0 or False or None as a succinct way of saying “I don’t care about the name of this thing”.  

> Minor note: I used `Key` as the name of the property so my IDE did not bug me for using in the Python reserved word ‘id’. Little things matter :) However in mGui 2.0, you generally don't need to specify kees.

Speaking of little things: there are some great tools in the Python language to make classes more efficient to work with. The so called ‘magic methods’ allow you to customize the behavior of your classes, both to make them feel more Pythonic and to express your intentions more clearly. Here are a couple of the things we can do with the magic methods in our base class:  

### \_\_nonzero\_\_

Speaking of that pass-in-zero-to-skip-names gimmick, one simple but super-useful thing we can do is to implement the `__nonzero__` method. That’s what Python calls when you try the familiar  
    
    :::python
    if something:  
        doSomething()  
    

test. In our case, we know that all Maya GUI control commands have the `exist` flag, and therefore all of our GUI classes will too. So, if our `__nonzero__` just returns the `exist` property of our class instances, we can elegantly check for things like dead controls with a simple, pythonic if test.  

### \_\_repr\_\_

`__repr__` is what Python calls when you need a printable representation of an object. In our case, we can pass back our underlying Maya GUI object, which is just a GUI path string. This way, you can pass one of our wrapper classes to some other python code that works on GUI objects and it will ‘just work’ – This is more or less what PyMel does for nodes, and it’s a great help when integrating a new module into an existing codebase. Like PyMel’s version there will be some odd corner cases that don’t work but it’s a handy convenience most of the time.  

As a minor tweak, the `__repr__` is also tweaked to display differently when the GUI widget inside a wrapper class has been deleted. This won’t prevent errors if you try to use the widget, but it is a big help in parsing error messages or stack traces.  

### \_\_iter\_\_

The next magic method we want to add is `__iter__`. It is the what python calls when you try to loop over a list or a tuple.  

Now, a single GUI object obviously is not iterable. A layout like columnLayout, on the other hand, can be iterated since it has child controls. By implementing `__iter__` here and then over-riding it when we tackle layouts, we can iterate over both layouts and their children in a single call. This makes it easy to look for layout children :  
    
    :::python
    for child in mainlayout:  
        if child.Key == 'cancel': #.... etc  
    

So with all those methods added the base Control class looks like this:  

    :::python    
    class Control(Styled, BindableObject):  
        '''  
        Base class for all mGUI controls.  Provides the necessary frameworks for CtlProperty and CallbackProperty access to the underlying widget.  
      
        NOTE this is not exactly identical to the code on github - more advanced stuff is removed to make the progression clearer  
        '''  
        
        # what command do I call?
        CMD = cmds.control  
        
        # these will be re-written by the metaclass as property descriptors 
        _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag',  'enable', 'enableBackground', 'exists', 'fullPathName', 'height',  'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']  
        _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']  
        _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus']  
        
        # Activate the metaclass!
        __metaclass__ = ControlMeta  
      
        def __init__(self, key, *args, **kwargs):  
      
            self.Key = key  
            self.Widget = self.CMD(*args, **_style)  
            '''  
            Widget is the GUI element in the scene  
            '''  
            self.Callbacks = {}  
            '''  
            A dictionary of Event objects  
            '''  
            Layout.add_current(self)  
      
      
        def register_callback(self, callbackName, event):  
            '''  
            when a callback property is first accessed this creates an Event for the specified callback and hooks it to the GUI widget's callback function  
            '''  
            kwargs = {'e':True, callbackName:event}  
            self.CMD(self.Widget, **kwargs)  
      
        def __nonzero__(self):  
            return self.exists  
      
        def __repr__(self):  
            if self:  
                return self.Widget  
            else:  
                return "<deleted UI element %s>" % self.__class__  
      
        def __str__(self):  
            return self.Widget  
      
        def __iter__(self):  
            yield self  
    

You’ll notice that it is inheriting from two classes we have not touched on, `Styled` and `BindableObject`. Those don’t interact with what we’re doing here - they’ll come up in a later post. You can pretend it just says ‘object’. If you’re reading the code carefully you’ll probably spot a little bit of code I haven’t described. `register_callback` is there to support event proxies – we’ll talk about the details when we get to [event proxies](http://techartsurvival.blogspot.com/2014/04/the-main-event-event-oriented.html) in the future.  

Despite my rather verbose way of describing it all, this is not a lot of code. Which is what exactly you want in a base class: simple, common functionality, not rocket science. Hopefully, though, adding those pythonic behaviors will save a lot of waste verbiage in production work.  

![](http://3.bp.blogspot.com/-9goyxbxMoA8/Uy5eUMQ1DxI/AAAAAAABIBI/McpZ1Vp2SIQ/s1600/yeoldeayb+\(2)  

> Damn, the internet has a lot of time on its hands   
  

## All Your Children Are Belong To Parent Layout

There’s one little bit of plumbing in Control that is worth calling out:  

    :::python
    Layout.add_current(self)  
    

That’s way of making sure that we can store references to our control wrappers in our layout wrappers - that is, when you create a wrapped button inside a wrapped columnLayout, the columnLayout has a handle to the wrapper class for the button. Which brings us around neatly to the wrapper class for layouts - called… wait for it… Layout.  

To support nesting, we want our Layout wrapper class to be a context manager. The idea is that you when you start a Layout, it declares itself the active layer and all GUI controls that get created add themselves to it; when you’re done with it control is return to whatever Layout was active before. As Doctor Who says of bow ties, “Context Managers are cool.”  

If you’ve done a lot of Maya GUI you know it’s also nice to have the same functionality for menus as well. So, to avoid repeating ourselves let’s start by creating a generic version of Control that works as a context manager so we can get identical functionality in windows, layouts and menus. Then we can inherit it into a wrapper class for layouts and another for windows and voila, they are all context managers without cutting and pasting. Here’s the abstract base class for all ‘nested’ classes: menus, windows, layouts etc:  
    
    :::python  
    class Nested(Control):  
        '''  
        Base class for all the nested context-manager classes which automatically parent themselves  
        '''  
        ACTIVE_LAYOUT = None  
      
        def __init__(self, key, *args, **kwargs):  
            self.Controls = []  
            super(Nested, self).__init__(key, *args, **kwargs)  
      
        def __enter__(self):  
            self.__cache_layout = Nested.ACTIVE_LAYOUT  
            Nested.ACTIVE_LAYOUT = self  
            return self  
      
        def __exit__(self, typ, value, traceback):  
            self.layout()  
            Nested.ACTIVE_LAYOUT = self.__cache_layout  
            self.__cache_layout = None  
            cmds.setParent("..")  
      
        def layout(self):  
            '''  
            this is called at the end of a context, it can be used to (for example) perform attachments  
            in a formLayout.  Override in derived classes for different behaviors.  
            '''  
            return len(self.Controls)  
      
        def add(self, control):  
            path_difference = control.Widget[len(self.Widget):].count('|') - 1  
            if not path_difference:  
                self.Controls.append(control)  
      
            if control.Key and not control.Key[0] == "_":  
                if control.Key in self.__dict__:  
                    raise RuntimeError('Children of a layout must have unique IDs')  
                self.__dict__[control.Key] = control  
      
        def remove(self, control):  
            self.Controls.remove(control)  
            k = [k for k, v in self.__dict__.items() if v == control]  
            if k:  
                del self.__dict__[k[0]]  
      
        def __iter__(self):  
            for item in self.Controls:  
                for sub in item:  
                    yield sub  
            yield self  
      
        @classmethod  
        def add_current(cls, control):  
            if cls.ACTIVE_LAYOUT:  
                Nested.ACTIVE_LAYOUT.add(control)  
    

All that really does is pop the current `Nested` onto a stack and make it possible for other controls to add themselves to the instance on top of the stack.  

Here’s the concrete implementation for actual Layout classes:  

    :::python   
    class Layout(Nested):  
      
        CMD = cmds.layout  
        _ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag', 'dragCallback', 'dropCallback', 'enable', 'enableBackground', 'exists', 'fullPathName', 'height', 'manage', 'noBackground', 'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride', 'useTemplate', 'visible', 'visibleChangeCommand', 'width']  
        _CALLBACKS = ['dragCallback', 'dropCallback', 'visibleChangeCommand']  
        _READ_ONLY = ['isObscured', 'popupMenuArray', 'numberOfPopupMenus', 'childArray', 'numberOfChildren']  
    

This is just a regular mGUI class (it gets all of the metaclass behavior from `Control`, via `Nested`) with added properties for common layout properties like `numberOfChildren`.  

While we’re messing with contexts, this is also a great opportunity to do what PyMel already does and make all layouts automatically manage UI parenting. This gets rid of all those irritating calls to setParent(“..”), and lets us write GUI code that looks like real Python and not a plate of spaghetti. Compare this wordy cmds example:  
    
    :::python    
    win = window('main window', title="Ugly version")  
    columnLayout('GUI', width = 256)  
    frameLayout("t_buttons", label = "buttons column")  
    columnLayout("col")  
    sphere_1 = button('mkSphere', label = "Make Sphere", c = make_sphere)  
    cone_1 = button('mkCone', label ="Make Cone", c = make_cone)  
    cube_1 = button('mkCube', label ="Make Cube", c = make_cube)  
    setParen("..")  
    setParent("..")  
    frameLayout("r_buttons", label = "buttons row")  
    rowLayout ("row", numberOfColumns=3)  
    sphere_2 = button('mkSphere', label = "Make Sphere", c = make_sphere)  
    cone_2 = button('mkCone', label ="Make Cone", c = make_cone)  
    cube_2 = utton('mkCube', label ="Make Cube", c = make_cube)  
    setParen("..")  
    setParent("..")  
    frameLayout("g_buttons", label = "buttons grid")  
    gridLayout("grid", numberOfColumns = 2):  
    sphere_3 = button('mkSphere', label = "Make Sphere", c = make_sphere )  
    cone_3 = button('mkCone', label ="Make Cone", c = make_cone)  
    cube_3 = button('mkCube', label ="Make Cube", c = make_cube)  
    circle_btn = button('mkCircle', label = "Make Circle", c = make_circle)  
    setParen("..")  
    setParent("..")  
    setParent("..")  
    showWindow(win)  
    

To this version using context manager layouts:  

> **Historical note:** This uses 'mGui 1' syntax; in mGui 2 the explicit keys would not be needed

    :::python
    from mGUI.GUI import *  
    # note the caps: all of these are wrapper objects, not Maya.cmds!  
      
    window = Window('main window', title="How's this")    
    with ColumnLayout('GUI', width = 256) as GUI:  
        with FrameLayout("t_buttons", label = "buttons column"):  
            with ColumnLayout("col"):  
                Button('mkSphere', label = "Make Sphere")  
                Button('mkCone', label ="Make Cone")  
                Button('mkCube', label ="Make Cube")  
      
        with FrameLayout("r_buttons", label = "buttons row"):  
            with RowLayout ("row", numberOfColumns=3):  
                Button('mkSphere', label = "Make Sphere")  
                Button('mkCone', label ="Make Cone")  
                Button('mkCube', label ="Make Cube")  
      
        with FrameLayout("g_buttons", label = "buttons grid"):  
            with GridLayout("grid", numberOfColumns = 2):  
                Button('mkSphere', label = "Make Sphere")  
                Button('mkCone', label ="Make Cone")  
                Button('mkCube', label ="Make Cube")  
                Button('mkCircle', label = "Make Circle")  
    

That example also includes one other neat way to leverage contexts too. If you double check the `add` method in `Nested` you’ll see that it adds child wrapper objects to it’s own `__dict__`. That makes them accessible without having to explicitly store them. In this example, you could get to the last sphere-making button in this example as `GUI.g_buttons.grid.mk_sphere` without having to manually capture the name of the underlying widgets they way the first example must. Since Maya GUI is always a single-rooted hierarchy, as long as you know the first parent of a window or panel you can always get to any of its the child layouts or controls. This saves a lot of the boring boilerplate you would otherwise need to do just keeping track of bits and pieces.  

There’s one little extra bit of magic in there to let the add method discriminate between children you care about and those you don’t. If your child controls have no key set, they won’t be added to the `__dict__`. On a related note, you can also be tricksy and add a control which is not a direct child of the layout - for example, if you had a layout with a list of widgets in a scrollLayout, you don’t usually don’t care about the scrollbar - it’s just along for the ride. So you can add the widgets directly to the ‘real’ parent layout and keep the paths nice and trim. The goal, after all, is to make the GUI layout a logical tree you can work with efficiently. There’s a practical example of this trick in the [lists.py](https://github.com/theodox/mGUI/blob/master/mGUI/lists.py) file on Github.

Here’s a snippet tacked on to the end of that last sample showing how you can use the iterability of the layouts to set properties in bulk. You can see how the work of turning command-style access into property style access, combined with the extra clarity we get from context managers, really pays off:  
    
    :::python
    # using the iterability of the layout to set widths   
      
    for item in GUI.t_buttons:  
        item.width = 256  
      
    for item in GUI.r_buttons.row:  
        item.width = 85  
    item.width = 256  # the last item is GUI.r_buttons.row itself  
    item.columnWidth3 = (85,85,85)  # ditto  
      
    for item in GUI.g_buttons.grid:  
        item.width = 128  
    item.width = 256  # now the last item is the grid  
    item.cellWidth = 128     
      
    cmds.showWindow(window)  

  
![](http://1.bp.blogspot.com/-YbhMcGSYTpg/Uy58bLV2nlI/AAAAAAABIBo/4q3TtCRPosI/s1600/example.png)  

I don’t even want to think about the equivalent code in `cmds`!  
One parting note about the naming scheme, It does have one, inevitable drawback: it means that the child wrappers have unique names inside a given context. Not much we can do about that. They can, however, have the same name under different parents - the example above has , `GUI.t_buttons.grid`.`mk_sphere`, and `GUI.g_buttons.grid.mk_sphere` Thats a useful thing to exploit if you want to, say, find all of the ‘Select’ buttons on a form and disable them or something off that sort.  

## Make All Zig!

Hopefully, the combination of some syntax sugar in our wrappers and turning layouts into context managers will make Maya GUI layout less of a pain in the butt. However, we still need to actually crank out all the wrappers for all those scores of classes in the Maya GUI library. Descriptors and metaclasses are powerful tools, but few of us have the intestinal fortitude to plow through the dozens of classes in the Maya GUI library getting every flag and command correct.  

In an ideal world we’d have a way of reflecting over some kind of assembly information and extracting all of the Maya GUI commands with their flags and options. Of course, in an ideal world we would not have to do this in the first place, since the native GUI system would not be the unfortunate SNES-era mishmash that it is.  

![](http://www.rogerwendell.com/images/allyourbase/allyourbase_clip.gif)  
> Mass production is a pain in the ass.  

Luckily, the TA spirit cannot be kept down by adversity. In this case we don’t have a nice clean api but we do have MEL.... poor, neglected, wallflower MEL. Well, here’s a chance for the wallflower to save the party: MEL’s help command can list all of the commands and all of the flags in Maya. So, what we need to do is to run through all of the Mel commands in help, find the ones that look like GUI commands, and capture their command - flag combinations as raw material for our metaclass control factory.  

See? This was getting all programmery, but now we’re back in familiar TA spit-and-bailing-wire territory. Comfier?  

The actual code to build the wrappers isn’t particularly interesting (its [here](https://github.com/theodox/mGUI/blob/master/mGUI/helpers/tools.py) if you want to see it). In two sentences: Use the mel `help *` command to find all of the commands in Maya which share flags with cmds.control or cmds.layout. Then collect their flags to make the list of class attributes that the metaclass uses to create property descriptors. The final output will be a big ol’ string of class definitions like this:  

    :::python    
    class FloatSlider(Control):  
        '''sample output from mGUI.helpers.tools.generate_commands()'''  
        CMD = cmds.floatSlider  
        _ATTRIBS = ['horizontal','step','maxValue','value','minValue']  
        _CALLBACKS = ['changeCommand','dragCommand']  
    

We generate two files, one for controls and one for layouts (that’s an arbitrary design call on my part, you could of course have one file). Now they’re just sitting on disk as if we’d written them by hand. We can import our newly generated modules and away we go, with nice pythonic properties and our new functions.  

There is one judgement call here that is worth mentioning in passing.  
The logic in the helper modules which generate this is all deterministic, it doesn’t need human intervention so it could actually be run at module load time rather than being run and dumped out to a file. For what I want to do, I felt that physical files were a better choice, because they allow the option of hand tailoring the wrapper classes as the project evolves. Plus, the startup cost of trolling through every MEL command, while it’s not very big, is real and it seems good to avoid it. I’ve have heard enough grumbling over the years about PyMel’s startup speed that I thought it wisest to opt for speed and clarity over fewer files on disk.  

One nice side effect of generating our wrappers this way: we’ve added some functionality through our base classes but fundamentally we’ve kept the same names and options we already know from plain old Maya.cmds. The only changes are the mandatory names and the fact that I’ve capitalized the class names to make them more pep-8-friendly.  

Hopefully, keeps the learning curve short for new user. Its hard enough to pick up a new style, making you memorize hundreds of new property names seem like a big tax on users.  

In the version up on Github (and in this example) I opted to use only the long name for the properties. This is definitely a matter of taste; I’m sure that many TAs out there are sufficiently familiar with the old Maya command flags that a howler like `cmds.rowLayout(nc=2, cw2=(50,100), ct2=('both', 5), bgc = (.8,.6,.6), cl2=("left", "right")` makes its meaning clear. for my part, though, the long names clarify the intent of the code enormously if you make a fairly small upfront investment in typing.   

If you are of the opposite opinion, though, you can call the `generate_helpers` and `generate_controls` functions in mGUI.helpers.tools with `includeShortNames` set to true make your own wrappers with the short flags too.  
## What You Say!!!

Now we’ve got a complete library of all the widgets. You can see the results in [controls.py](https://github.com/theodox/mGUI/blob/master/mGUI/core/controls.py) and [layouts.py](https://github.com/theodox/mGUI/blob/master/mGUI/core/layouts.py) on GitHub. (The base classes are also up there for your perusal in [the root of the core module](https://github.com/theodox/mGUI/blob/master/mGUI/core/__init__.py)). If all you want is to stop writing long commands every time you touch a GUI item, you’re done. You can write crisper layout code, tweak your properties, and so on with what we’ve covered so far. If you’re interested in making practical use of this setup – remember that WIP warning! – you should read the docs in the events.py module to make sure you know how to hook up callback events. I’ll cover that in more detail in the future.  
However… Simpler syntax is just scratching the surface of what we can get up to now that we have a proper class library for our widgets. Next time out we’ll look at the event mechanism in more detail and talk about how to cleanly separate your functional code, GUI layouts, and the display styles of your widgets.  

[Until next time....](http://www.youtube.com/watch?v=8fvTxv46ano)

