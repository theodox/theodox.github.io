Title: Rescuing Maya GUI from itself
Date: 2014-02-23 10:22:00.000
Category: blog
Tags: , , , , , 
Slug: Rescuing-Maya-GUI-from-itself
Authors: Steve Theodore
Summary: pending

**Update 4/11/2015: Fixed the code examples which were blown away in the current Blogger template, and also dead image links**

[Last time out](http://techartsurvival.blogspot.com/2014/02/pity-for-
outcast.htm) was devoted to a subject most TA's already know: the shortcomings
of Maya's native GUI. This time we're going to start looking at ways to rescue
Maya from itself.

![](http://www.fanderson.org.uk/news/images3/darlingpuppet.jpg)

And if you don't know what that picture is there, [go here
first](http://youtu.be/9XNWA_yZvWo") \- this tech-art stuff is not as
important as a good understanding of
[Thunderbirds!]("http://en.wikipedia.org/wiki/Thunderbirds_\(TV_series\))).

With that out of the way:

Any good rescue mission starts with objectives. The three main drawbacks to
coding in Maya GUI natively are **nasty syntax**, clunky **event handling**,
and difficult **management**. In today's thrill-packed episode, we're going
lay some foundations for tackling that old-school syntax and dragging Maya GUI
kicking and screaming into the 21st century.

# Under the surface

![](http://www.foundation3d.com/forums/attachment.php?attachmentid=74848&d=141
0941489)

Composing a Maya GUI in code is annoying because the only way to access the
properties of a Maya GUI node is via a command - there's no way to get at the
properties directly without a lot of command mongering.

Sure, the purist might say that alternatives are just [syntax
sugar](http://www.javakey.net/1-java/92b15b2251bd8f85.htm) \- but Maya GUI's
drawbacks are are (a) an obstacle to readability (and hence maintenance) and
(b) such a big turn off that people don't bother to learn what native GUI can
do. This is particularly true for formLayouts, which are the most useful and
powerful - and also the least handy and least user-friendly - way of layout of
controls in Maya. All the power is no use if you just stick with columnLayouts
and hand-typed pixel offsets because setting things up takes a whole
paragraph's worth of typing.

So, the first thing I'd like to ponder is how to cut out some of the crap. Not
only will a decent wrapper be more pleasant to read and write - at some point
in the future when we get to talk about styling controls, real property access
will be a big help in keeping things tidy. Plus, by putting a wrapper around
property access we'll have a built in hook for management and cleaning up
event handling as well, even though that's a topic for a future post.

The upshot of it all: we're stuck with the under-the-hood mechanism, but
there's no reason we can't wrap it in something prettier. Consider this simple
example:

    
    
    import maya.cmds as cmds  
      
    class ExampleButton(object):  
        CMD = cmds.button  
      
        def __init__(self, *args, **kwargs):  
            self.Widget = self.CMD (*args, **kwargs)  
      
        @property  
        def Label(self):  
            return self.CMD(self.Widget, q=True, label=True)  
      
    example = cmds.window()  
    col = cmds.columnLayout()  
    btn = ExampleButton("hello world")  
    cmds.showWindow(example)  
    print btn.Label  
    # hello world  
    

This is [plain-vanilla Python properties](http://nbviewer.ipython.org/urls/gis
t.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb) in action.
It's easy to extend it so you can set 'Label' also:

    
    
        @Label.setter  
        def Label(self, val):  
            return self.CMD(self.Widget, e=True, label=val)  
      
    # add this to the example above:  
    btn.Label = "Goodbye cruel world"  
    

![](http://1.bp.blogspot.com/-AOcq5Y6WCSA/UwLm4_AUSoI/AAAAAAABH7s/3FL8iI1r9TU/
s1600/gbcw.png)

# Rescuing the rescuers

While this is a nice trick, it doesn't take long to figure out that replacing
the whole Maya GUI library with this will take a lot of annoying, repetitive,
and typo-prone code. `cmds.button` alone has 34(!) properties to manage, and
real offenders like `rowLayout` have a lot more. Writing wrappers for all of
these is a huge waste of valuable human brainpower

Luckily, that's not the end. Property objects are really instances of [Python
descriptors](http://docs.python.org/2/howto/descriptor.html), which means they
are classes. And since they are classes, we have some more options for
creating them.

[The official docs](http://docs.python.org/2/howto/descriptor.html) on
descriptors are kind of opaque, but the link I shared above to [Chris
Beaumont's article on properties and descriptors](http://nbviewer.ipython.org/
urls/gist.github.com/ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb) does
a great job of explaining what they do: which is, in a nutshell, to provide
property like services in the form of class-level objects. (Update: here's
[great five minute
video](http://nedbatchelder.com/blog/201306/explaining_descriptors.html) too).
Instead of defining methods and decorating them as we did above, you create a
class which handles the function-to-property behavior (both getting and
setting) and stick it directly into your own class namespace, the same way you
would place a def or a constant (as an aside, this placement is why the CMD
field in the example is a class field rather than a hard code or an instance
property - it makes it easy for the descriptor to call the right cmds function
and flags. We could make a separate class for `cmds.floatField`, for example,
swapping out only the class level CMD parameter, and it would 'just work' the
same way).

The gotcha to bear in mind with descriptors is that they are separate objects
that live in the class, _not_ instance members You don't create them inside
your `__init__`, you declare them in the class namespace. They don't belong to
individual instances - that's why in the example below you'll notice that
_self_ refers to the descriptor itself, and not to the ExampleButton class
(this is how each descriptor in the example below remembers how to format it's
own call to the maya command under the hood).

The "bad" part of that is that you the descriptor is ignorant of the class
instance to which it is attached when you call it. Pyhton will pass the
instance in to the descriptor, as you'll see in the example below. The good
part, on the other hand, is that the descriptor itself can (if need be) have a
memory of its own - that's why the descriptors in the next example can
remember which flags to use when they call the underlying Maya GUI commands.

While this sounds scary, it's mostly a minor mental adjustment - once you do a
couple times it will be routine. And all the oddness is concentrated in the
definition of the descriptor objects themselves - once the descriptor is
actually declared, you access it just as if it were a conventional instance
property and all is plain-jane `foo.bar = baz`.

Here's the button example re-written with a couple of descriptors:

    
    
    class CtlProperty (object):  
        '''  
        Property descriptor.  When applied to a Control-derived class, invokes the correct Maya command under the hood to get or set values  
        '''  
      
        def __init__(self, flag, cmd):  
            assert callable(cmd), "cmd flag must be a maya command for editing gui objects"  
            self.Flag = flag  
            self.Command = cmd   
      
        def __get__(self, obj, objtype):  
            '''  
            Class instance <obj> and its type <objtype> are passed in automatically.   
            <self> is this descriptor object, NOT an owning class instance!  
            '''  
            ctrl = obj.Widget if hasattr(obj, "Widget") else str(obj)  
            return self.Command(ctrl, **{'q':True, self.Flag:True})  
      
        def __set__(self, obj, value):  
            '''  
            Again, the owning instance is passed in as <obj> automatically  
            '''  
            ctrl = obj.Widget if hasattr(obj, "Widget") else str(obj)  
            self.Command(ctrl, **{'e':True, self.Flag:value})  
      
    class ExampleButton(object):  
        CMD = cmds.button  
      
        def __init__(self, *args, **kwargs):  
            self.Widget = self.CMD (*args, **kwargs)  
      
        Label = CtlProperty('label', CMD)  
        BackgroundColor = CtlProperty('bgc', CMD)  
      
    # same example as before      
    example = cmds.window()  
    col = cmds.columnLayout()  
    btn = ExampleButton("hello world")  
    cmds.showWindow(example)  
    btn.Label = "Thunderbirds are GO!"  
    btn.BackgroundColor = (.25, 1, .25)  
    

  
![](http://2.bp.blogspot.com/-nCT8aEzquIE/UwLr8_Ct6wI/AAAAAAABH78/wVp86oOdf24/
s1600/t+are+g.png)

That's more like it - only two lines of data-driven code where we used to have
six (well, not counting CtlProperty - but thats a one time cost to be spread
out over scads of different GUI classes later). It's a lot easier to read and
understand as well, and contains far fewer opportunities for typos.

But… we're still talking 34 lines like that for `cmds.button`, and God knows
how many for `cmds.rowColumLayout`.

**Sigh.**

# Act III

![](http://www.clevescene.com/imager/thunderbirds-stiff-acting-all-
around/b/original/1504418/2808/1875857.t.jpg)

No rescue drama is complete without a false climax, and this is ours. Despite
the ominous music just before the commercial,. the situation is not really
that bad. The last example shows that the problem is not really one of _code_
any more, it's just _data_. Since descriptors are objects, you can crank them
out like any other object: provide a list of the appropriate flags for a given
class and you can crank out the correct descriptors, as they say,
"[automagically](https://www.youtube.com/watch?v=Z3qK8gT5LLg)."

**As long as you promise not to use that stupid word around me.**

Fortunately for our rescue team, Python treats classes the same way it treats
anything else: as objects that can be created and maniuplated.

If you use the Python builtin `type` on any Python class, you'll get back  
`type 'type'`. In other words, a Python class definition is itself an instance
of the class 'type'. How… _meta._

The reason this matters to us is that we can fabricate classes the same way
fabricate other kinds of Python things. You would not hesitate to crank out a
list of strings assembled in code: there's no reason you can't do the same
thing for descriptors! You could do this by hand, creating type instances and
filling them out yourself: types take three arguments: a string name, a list
of parent types, and dictionary of named fields and propertis. Thus:

    
    
    def constructor(self, name):  
        self.Name = name  
      
    example = type('Example', (), {'__init__':constructor } )  
      
    Test = example("Hello world")  
    # <__main__.Example object at 0x00000000022D6198>  
    Test.Name  
    # Hello world  
    

However this would send you down a possible rabbit hole, since the idea we're
really chasing is a way to mass produce classes to make UI coding easier and
it would not be very easy if all of the classes had to be coded up in this
clunky way. Luckily Python has an obscure but extremely powerful mechanism
designed for just this sort of problem. Because, you know, it's the language
of geniuses.

![](https://shapersofthe80s.files.wordpress.com/2011/01/thunderstampbrains.jpg
)

# "Brains, Activate the Metaclass"

The helpful MacGuffin in this case it the
_[Metaclass](http://docs.python.org/2/reference/datamodel.html#customizing-
class-creation). _Metaclasses have a reputation - not _entirely_ undeserved -
as deep voodoo. The most commonly circulated quote about them is that "If you
can solve the problem without a metaclass, you should."

However, in our case we really can't solve the problem without some form of
class factory. In particular, we need a way to bang out classes with the right
collection of Descriptors to cover all of the zillions of flags in the Maya
GUI system. So just this once we can put on the big blue glasses and lab coats
and venture into the super secret lair of the mad metaclass scientists.

The job of a metaclass is to customize the act of class creation. When a class
is first defined, python will pass the type it creates (that same object we
played with in the last example) to the metaclass for further manipulation.
The `__new__` function of the metaclass will be called on the just-defined
type, taking it name, parents and internal dictionary as arguments. The
`__new__` can fiddle with any of these as it sees fit before passing it along
for actual use.

As you can imagine, this is a good time for PythonMan's Uncle Ben to remind us
that 'with great power comes great responsibility' - it's easy to shoot
yourself in the foot with a metaclass, since you can make changes to the
runtime versions of your classes that will not be represented in your source
files. Don't just run off and meta all over everything in sight. A minimalist
approach is the best way to stay sane.

But you'd probably like to see what this really looks like in practice. Here's
an example.

    
    
    class ControlMeta(type):  
        '''  
        Metaclass which creates CtlProperty  objects for maya gui proxies  
        '''  
        CONTROL_ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate',   
                    'docTag', 'dragCallback', 'dropCallback', 'enable',   
                    'enableBackground',  'exists', 'fullPathName', 'height',    
                    'manage', 'noBackground',  'numberOfPopupMenus', 'parent',   
                    'popupMenuArray', 'preventOverride', 'useTemplate', 'visible',   
                    'visibleChangeCommand', 'width']  
      
        def __new__(cls, name, parents, kwargs):  
            '''  
            __new__ is called then classes using this meta are defined.  It will add   
            all of the items in CONTROL_ATTRIBS to the new class definition as   
            CtlProperty descriptor objects using the CMD field (a maya.cmds command)   
            provied in the outer class.  
            '''  
      
            CMD = kwargs.get('CMD', None)  
      
            if not kwargs.get('CMD'):  
                CMD = parents[0].CMD  
      
            for item in ControlMeta.CONTROL_ATTRIBS:  
                kwargs[item] = CtlProperty(item, CMD)  
      
            return super(ControlMeta, cls).__new__(cls, name, parents, kwargs)  
    

The actual code is pretty simple. It takes the type object created by the
'real' class and grabs the contents of the CMD class field (remember that from
the earlier examples?). Then it loops through its own list of command names
and inserts them all into the new class as descriptors with the correct
commands and the maya command that was stored in the command object. So our
earlier button example becomes:

    
    
    https://gist.githubusercontent.com/theodox/9106403/raw/60a06cba76748d7b157a5219349888f7b0bf0214/ButtonWithMeta.py  
    class MetaButton(object):  
        CMD = cmds.button  
        __metaclass__ = ControlMeta  
      
        def __init__(self, *args, **kwargs):  
            self.Widget = self.CMD (*args, **kwargs)  
      
      
    w = cmds.window()  
    c = cmds.columnLayout()  
    mb = MetaButton("button1")  
    cmds.showWindow(w)  
      
    print mb.exists  # We never had to add this one!  
    # True  
    print mb.visible  # or this  
    # True  
    

There is a minor problem with this very truncated example, however: there's no
label or command in the the metaclass, so the MetaButton has no button
specific properties - only the generic ones in our list (which I made by
trolling the flags for `cmds.control`, the 'base class' of all Maya control
commands).

This is easily fixed by adding properties that are specific to buttons to a
class field, and tweaking the metaclass to read and use them the same way it
already uses the CMD class field. Like CMD, these are good class-level
attributes since the collection of flags is shared by all buttons, fields or
whatever.

    
    
    class ControlMeta(type):  
        '''  
        Metaclass which creates CtlProperty  objects for Control classes  
        '''  
        CONTROL_ATTRIBS = ['annotation', 'backgroundColor', 'defineTemplate', 'docTag',   
                            'dragCallback', 'dropCallback', 'enable', 'enableBackground',   
                            'exists', 'fullPathName', 'height',  'manage', 'noBackground',   
                            'numberOfPopupMenus', 'parent', 'popupMenuArray', 'preventOverride',   
                            'useTemplate', 'visible', 'visibleChangeCommand', 'width']  
      
      
        def __new__(cls, name, parents, kwargs):  
      
            CMD = kwargs.get('CMD', None)  
            _ATTRIBS = kwargs.get('_ATTRIBS',[])  # unique props from outer class  
      
            if not kwargs.get('CMD'):  
                CMD = parents[0].CMD  
      
            for item in ControlMeta.CONTROL_ATTRIBS:  
                kwargs[item] = CtlProperty(item, CMD)  
      
            for item in _ATTRIBS:   # now add in the outer class's unique props too  
                kwargs[item] = CtlProperty(item, CMD)  
      
            return super(ControlMeta, cls).__new__(cls, name, parents, kwargs)  
      
      
    class MetaButton(object):  
        CMD = cmds.button  
        _ATTRIBS = ['label', 'command']  # button specific props  
        __metaclass__ = ControlMeta  
      
        def __init__(self, *args, **kwargs):  
            self.Widget = self.CMD (*args, **kwargs)  
      
    class MetaFloatField(object):  
        CMD = cmds.floatField  
        _ATTRIBS = ['editable','precision','value','maxValue','step',  
                    'minValue', 'changeCommand','dragCommand','enterCommand',  
                    'receiveFocusCommand']  # this one has a lot of properties  
      
        __metaclass__ = ControlMeta  
      
        def __init__(self, *args, **kwargs):  
            self.Widget = self.CMD (*args, **kwargs)  
    

As you can see, extending the automatic analysis is easy now that we know the
basic trick. Just add a semi-private class field with the class specific
attributes, and away we go!

# In our next exciting episode…

I think this pretty much demonstrates that overhauling the Maya GUI toolkit is
possible. However, in its current state it's just a down-payment.

The combination of descriptors and metaclasses is an incredibly powerful tool
and it's not hard to see what comes next (it's also easy to imagine similar
setups for other problems which suffer from ugly imperative syntax). Now that
we have a method for cranking out control widget classes by the bucketload,
filling out the class library itself is pretty simple. There are, though, a
few tricks we can use to make it better and less manual, as well as making
sure it is complete. So, in a future outing, we'll tackle a method for
replicating the whole Maya command hierarchy in a more or less automatic way.

If you want to roll your own lightwieght properties library, this should give
you enough tools to work with. If you're more interested in actually doing GUI
work without all the `cmds` crap, you should check out
[mGui](https://github.com/theodox/mGui), which is a library based on exactly
this metaclass strategy to make GUI code more declarative and less ugly.

In the mean time,as we say at International Rescue Headquarters:
[F.A.B!](http://www.funtrivia.com/askft/Question54024.html)


