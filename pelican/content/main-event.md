Title: The Main Event - event oriented programming in Maya
Date: 2014-04-29 00:14:00.001
Category: blog
Tags: maya, python, mGui, programming
Slug: _main-event
Authors: Steve Theodore
Summary: Event oriented programming for python in general and for Maya GUI in particular

The [Maya Callbacks Cheat Sheet](http://techartsurvival.blogspot.com/2014/04/maya-callbacks-cheat-sheet.html) post started out as an effort to explain the design the [event system](https://github.com/theodox/mGui/blob/master/mGui/events.py) in [mGui ](https://github.com/theodox/mGui)\- but it quickly turned into it's own thing as I realized that the vanilla Maya system remains confusing to lots of people.  With that background out of the way, I want to return to events proper, both to explain why they work the way the do in mGui and also how they can be useful for other projects as well (I use them all over the place in non-GUI contexts).  
  
...and, because it's got the word 'event' in it, I'm going to throw in a lot of irrelevant references as I can manage to **_The Crushah!_**  
  


[![](http://hot-breakfast.com/wp-content/uploads/2014/01/GHG-WB-Crusher.jpg)](http://hot-breakfast.com/wp-content/uploads/2014/01/GHG-WB-Crusher.jpg)

 

## The Reining "Champeen"

[![](http://i3.ytimg.com/vi/n0lzjNzql5Y/mqdefault.jpg)](http://i3.ytimg.com/vi/n0lzjNzql5Y/mqdefault.jpg)  
> It's a heavyweight programming paradigm!  
  
 

  
The cheat sheet post showed that Maya callbacks are reasonably functional once you understand the underlying code scope rules. However they also shows some of the limitations of the default system:  
  


#### Awkward argument handling  

In cases where you want to call a command with arguments or parameters, plain-old-Maya callbacks require you do fancy footwork with lambdas or partials to pass your arguments in correctly. It's not rocket science, but it is a pointless tax on what should be a trivial problem.  
  


#### Design time

GUI code is usually kind of fiddly to begin with, since you're often busy tweaking sizes, layouts and other graphical whatnots as you lay out the GUI (one of the big advantages of things like QT Designer is that they split this work out from the underlying code very neatly by turning all of that layout and presentation stuff into data).  You can see this particularly when you're trying to shoehorm all of the arguments and parameters for a command into the same line that also declares and styles a control: you get a long messy piece of junk with lots of nested parens that's hard to parse at a glance.   
  
On a more strategic level, creating commands at the same time you create the visual layout for your controls tends to lock you into a monolithic style of coding. If you want to add new behaviors to a control contextually, you need to manage all of the state inside some other bit of code which not only knows how to do the new job,  it also needs to know enough about the original GUI layout that it can replace existing callback commands with new ones.   This means trivial tasks like highlighting a button when something is selected from a list get intertwined with complex code that does real work -- and, alas, that the two different sets of concerns get to share bugs.  
  


#### One shot

The last big drawback of the default Maya callback system is that each callback fires only one command.  This is not a big deal for things like buttons, but when you extend it to things like scriptJobs it can get messy very fast. Either you end up creating dozens of similar scriptJobs attached to the same trigger - in which case you  have to waste a lot of energy on managing them all -- or you have to create a complex uber-handler that jams a ton of (possibly unrelated) behaviors into a giant bucket-o-code.

  


## And In Dis Corner..!

[![](http://img.rp.vhd.me/3147118_l2.jpg)](http://img.rp.vhd.me/3147118_l2.jpg)
> our plucky challenger  
  
    


The mGui event system is intended to fight these problems and to promote cleaner, less coupled and more general code.  
  
The main ideas is to create objects --[ the Event class](https://github.com/theodox/mGui/blob/master/mGui/events.py)\-- which store a list of functions (usually known as 'handlers') which they call when they are activated. Each Event can host any number of handlers, and the handlers can be added or removed from an event at any time.  The events can store information you know when they are created or pass information you only know when they fire, so you don't have to jump through hoops to provide relevant data to your handlers. Finally, the Events are smart enough not to complain when a handler disappears - if you're logging processed items to a window from a long running task and the user closes the window, the underlying code will still run without complaint.

  


If you know your OOP history, this is obviously a shameless ripoff of the standard [Observer Pattern](http://www.philipuren.com/serendipity/index.php?/archives/4-Simple-Observer-Pattern-in-Python.html), -- although the implementation here owes more to [the way events are handled in C#](http://msdn.microsoft.com/en-us/library/aa645739\(v=vs.71\).aspx).   The main difference from the canonical implementation is that -- this being Python -- the handlers don't need to be classes, much less implementations of any particular base class; instead, the Event maintains a list of callables -- which can be functions, lambdas or callable classes -- and tries to fire them when it itself is triggered. Unlike the C# version of the same idea, there's no need for an elaborate menagerie of specially-typed handlers and data passing classes; instead, any function that accept [the plain-python open-ended *args, **kwargs signature](http://freepythontips.wordpress.com/2013/08/04/args-and-kwargs-in-python-explained/) can be a handler.

Here's the important bit of the core code (the full thing, as always, is [up on github](https://github.com/theodox/mGui/blob/master/mGui/events.py)) :

    :::python
    class Event(object):

       def __init__(self, **data):
            self._Handlers = set()
            '''Set list of handlers callables. Use a set to avoid multiple calls on one handler'''
            self.Data = data
            self.Data['event'] = self

        def _add_handler(self, handler):
            """
            Add a handler callable. Raises a ValueError if the argument is not callable
            """
            if not callable(handler):
                raise ValueError("%s is not callable", handler)

            self._Handlers.add(get_weak_reference(handler))
            return self

        def _remove_handler(self, handler):
            """
            Remove a handler. Ignores handlers that are not present.
            """
            wr = get_weak_reference(handler)
            delenda = [h for h in self._Handlers if h == wr]
            self._Handlers = self._Handlers.difference(set(delenda))
            return self

        def metadata(self, kwargs):
            """
            returns the me
            """
            md = {}
            md.update(self.Data)
            md.update(kwargs)
            return md

        def _fire(self, *args, **kwargs):
            """
            Call all handlers.  Any decayed references will be purged.
            """

            delenda = []
            for handler in self._Handlers:
                try:
                    handler(*args, **self.metadata(kwargs))
                except DeadReferenceError:
                    delenda.append(handler)
            self._Handlers = self._Handlers.difference(set(delenda))

        def _handler_Count(self):
            """
            Returns the count of the _Handlers field
            """
            return len([i for i in self._Handlers])

        # hook up the instance methods to the base methods
        # doing it this way allows you to override more neatly
        # in derived classes
        __call__ = _fire
        __len__ = _handler_Count
        __iadd__ = _add_handler
        __isub__ = _remove_handler



As you can see, it's really quite simple: The handlers are maintained in set, so they can't accidentally be duplicated.  We override the `__iadd__` and  `__isub__` methods to provide a simple syntax for attaching and detaching handlers (shamelessly stolen from C#).  The core is the `__call__` method. which makes the Event object callable as if it were a function.  When the event is called, it fires all of the handlers with whatever arguments and keywords were passed in.  

>The only 'interesting' bit of code is the function WeakMethod in line 20 - it's not defined in this snippet; basically it's job is to make sure the Event object doesn't keep objects alive in memory when they should be de-referenced. [See the github](https://github.com/theodox/mGui/blob/master/mGui/events.py) for details if you're interested.
  
While the description is a bit long winded, the use case is pretty straightforward:

    :::python
    from mGui.events import Event
    test_event = Event(name='test event')

    def test_handler (*args, **kwargs):
        print args, kwargs
        
    test_event += test_handler # attach the handler

    test_event()
    #>> () {'name': 'test event', 'event': <mGui.events.Event object at 0x000000002C7FEC88>}
    test_event(1,2,3)
    #>> (1, 2, 3) {'name': 'test event', 'event': <mGui.events.Event object at 0x000000002C7FEC88>}
    test_event(msg = 'hello')
    #>> () {'msg': 'hello', 'name': 'test event', 'event': <mGui.events.Event object at 0x000000002C7FEC88>}
  
Here `test_event`  is an `Event` object and `test_handler` is a handler function. Handlers are callables of any kind: functions, object methods, lamdas, or callable objects. The only requirement is that they accept the `*args, **kwargs` form of open-ended arguments -- you can do whatever you want with the args and kwargs inside a given handler, but they will be passed so you'll need to provide the right signature in your handler functions.  
  
One of the trickiest bits of doing event-driven programming is providing the right context to your handler functions.  Different kinds of functional code will need different bits of information -- for example, you might fire an event when the user selects something in your scene.  One handler could highlight the selected item in a list, another could enable or disable some buttons, and a third could update present an appropriate dropdown list. Some of these operations will care about the selected objects, and some won't; some will care about other kinds of conditions (Is the window expanded? Is the user in 'advanced mode'?). To keep the code clean and provide handlers with the context they need to do their jobs, the Events need to be able to pass extra information; the *args, **kwargs form makes it easy to provide the data you think appropriate.  
  
[![](http://img.youtube.com/vi/msp7rGJ5l7c/0.jpg)](http://img.youtube.com/vi/msp7rGJ5l7c/0.jpg)

## Extra! Extra! Read All About It!

Most of the time, the info you want to pass with your event is dynamic - you don't know what it will be until the tool is actually running. In this case, you can just pass arguments or keywords at call time as I did in the previous example. This really helps to make the callback mechanism more flexible, since the same Event can be triggered many tines for different circumstances without new code. For example, say you've got a long running process that's looping over a bunch of objects and doing something.  
  
Sometimes, though, the data is constant. In that case you can build it into the Event object directly - in that last snippet you can see that `test_event` has been set up with a name at creation time and that name is passed along to all invocations of the event. The ability to add unique data to an event ,makes it simple to write general handlers that can deal with several types of  Events at once - for example, you might auto-generate a set of buttons each of which was tied to a particular object in your Maya scene and then pass the object names through button's Events. Something like this mGui example (though as I said at the outset, you can just use the events module without mGui if you want):  


  
Any keywords you provide when creating an Event object will be stored and then passed as keywords when the event goes off. (You'll might have noticed in the previous example that Events automatically includes a reference to themselves in their keyword arguments; this can be handy for things like one-shot handlers that want to remove themselves from an  event after they fire)  A common idiom is to add a reference to the owning GUI object, so that there's no extra work needed to figure out, say, which checkbox just toggled it's state. In this example I've added added a reference to the buttons as 'sender' manually, but if I hadn't manually created the event and had just attached a handler to the default one that comes with the mGui button I'd also have gotten that for free.  
  
One thing to point out here is that the Events can mix both styles - predefined keywords and keywords or arguments that are defined at runtime. The Events will overwrite any pre-defined keywords that are duplicated, which is a behavior to remember - it can be useful but might also cause some surprises if you're not expecting it.,  
  


## The Final Round

[![](http://i.ytimg.com/vi/M50wHftQax8/0.jpg)](http://i.ytimg.com/vi/M50wHftQax8/0.jpg)  
---  
that's gotta hurt  
  
At the risk of repeating myself, I just want to show how the Event pattern makes it easier to achieve good, clean division between GUI code and functional code.  Here's the usual way you'd go about doing something like updating a GUI to reflect a long-running process:  

    :::python
    import time
    class OverCoupled(object):
        
        def __init__(self):
            self.window  = cmds.window()
            self.col  = cmds.columnLayout()
            cmds.button('start', c= self.some_complex_function)
            self.msg =  cmds.text('...')
            self.counter = cmds.text('0')
            self._counter = 0

        def show(self):
            cmds.showWindow(self.window)
       
        
        def some_complex_function(self, _):
            # update the gui
            cmds.text(self.msg, e=True, label="doing something fancy")
            cmds.refresh(force=True)
            for item in cmds.ls(type='transform'):
               time.sleep(4)
               # redraw the label 
               self._counter +=1 
               cmds.text(self.msg, e=True, label = item )
               cmds.text(self.counter, e=True, label = str(self._counter))
               cmds.refresh(force=True)
            # closing message
            cmds.text(self.msg, e=True, label="finished fancy tasks")

    oc = OverCoupled()
    oc.show()
  
Now, you could say that doesn't look _too _bad - the class is making it easy to find the text you want to update and it's only a couple  of lines each time you do the update. But this example is trivial; imagine this was real world code where some_complex_function really was complex and had lots of branches or possible failure points.  What if you needed to hit not two, but five or six different GUI elements?  What if you wanted to add logging or email?  The maintenance would add up fast.  
  
Most of all, imagine how irritating it is to write code that simultaneously does some complex task - requiring you to mentally follow along with the ins and outs of the procedure as you write or debug it - and then adding a bunch of fiddly gui code in-line with the tool work. It only gets worse if you want to refactor or re-use parts of some_complex_function, since you'll have to work around or excise the parts specific to this GUI It's a classic violation of [Separation of Concerns](http://effectivesoftwaredesign.com/2012/02/05/separation-of-concerns/).  Here's the same code with events instead of inline GUI code:  
  
    :::python
    import mGui.gui as gui
    import maya.cmds as cmds
    import mGui.events as events

    def move_down(*args, **kwargs):
        cmds.xform(kwargs['target'], t=(0,-10,0), r=True)

    # make a window with buttons for each transform. Clicking buttons 
    # moves them down 10 units
    with gui.Window('main') as example:
        with gui.VerticalForm('form'):
            for item in cmds.ls(type='transform'):
                b = gui.Button('b_' + item, label = item)
                b.command = events.Event(sender = b, target = item)
                b.command += move_down

    example.show()

  
As you can see the event-based version lets you cleanly separate out the functions from the UI. Moreover it would be a snap to make a headless version that ran with no GUI - and you could even add  logging to the console by attaching a simple handler function to the processor's `ItemProcessed` event. Abstracting  away the actual GUI code makes it easy to keep your code tidy and also lets you evolve your display mechanism without endangering your functional code. If you decide to swap in a messageLine for the the text widget -- or for that matter, if you print a line to the listener - it's all the same to the underlying code. This flexibility is exactly what [makes the native Python logging module so powerful](http://pynash.org/2013/03/07/logging-intro.html):  logging can write to text files, update databases, send emails or print console messages -- indeed, it can do all of those at once -- and the code that calls logging doesn't need to change one iota.


## TKO!

[![](http://1.bp.blogspot.com/_4QlZmS5gO7s/SmaQEq6ewTI/AAAAAAAAARE/A5DKfeZ5Sz8/s320/BunnyHugged13.jpg)](http://1.bp.blogspot.com/_4QlZmS5gO7s/SmaQEq6ewTI/AAAAAAAAARE/A5DKfeZ5Sz8/s320/BunnyHugged13.jpg)

  
  
So, that's the basic rationale for the event system in mGui. If you [check out the file on github](https://github.com/theodox/mGui/blob/master/mGui/events.py) you'll see there's a bit more going under the hood - that's a matter for another time. Till then, keep those dukes up.  
  
  


