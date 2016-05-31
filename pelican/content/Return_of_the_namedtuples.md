Title: Return of the namedtuples
Date: 2015-08-02 17:59:00.000
Category: blog
Tags: maya, python, programming
Slug: _return_of_the_namedtuples
Authors: Steve Theodore
Summary: A quick review of the Python `namedtuple` -- a great way to return complex data from your functions without needing complex custom classes.

I’m sure you’ve read or written code that looks like this:  

    :::python
    results = some_function()  
    for item in results:  
        cmds.setAttr(item[0] + "." + item[1], item[2])  
    

Here `some_function` must be using one of Python’s handiest features, the ability to return lists or tuples of different types in a single function. Python’s ability to return ‘whatever’ - a list, a tuple, or a single object – makes it easy to assemble a stream of data in one place and consume it in others wihout worrying about type declarations or creating a custom class to hold the results. Trying to create a similarly flexible system in, say, C# involves a lot of type-mongering. So it’s nice.  
At least, it’s nice _at first_. Unfortunately it’s got some serious drawbacks that will become apparent after a while – outside the context of a single script or function, relying entirely on indices to keep things straight is dangerous. As so often in Pythonia, freedom and flexibility can come at the cost of chaos downstream if you’re not careful.  
  

[![](https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRd4-Lzu45urv3dmdng5DMjdlO-ILlLVxoa-HeHMZ8uczP4fLWC)](https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRd4-Lzu45urv3dmdng5DMjdlO-ILlLVxoa-HeHMZ8uczP4fLWC)

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#i-have-a-bad-feeling-about-this)I have a bad feeling about this…

Everything will be hunky-dory as long as `some_function` continues to pack its output the same way. In this example `some_function` is probably doing something like:  
  
    :::python
    # imagine some actual code here ...  
    results = []  
    for node in object_list  
        for attrib in attrib_list:  
            settable = is_attrib_settable(node, attrib)  
            if settable:  
               new_value = dict_of_defaults[attrib]  
               results.append ([node, attrib, new_value])  
    return results  
    

  
Inevitably, though, something will come along that causes the order of the results to change. In a Maya example like this, for example, the likely cause would be some other user of this function finding out that the code needs to set defaults on an unusual value type. `setAttr` needs to be told what type of data to expect if things are unusual.  

That being the case, your teammate extends `some_function` to output the data type needed. If you’re lucky, the results look like `[node, attribute, value, type]` and your existing code works fine. But if it changes to `[node, attribute, type, value]` your existing code will break in wierd ways. Moreover if you haven’t written a lot of comments, the person fixing the bugs will have to sit down and deduce what `item[0]`, `item[1]` and `item[2]` were supposed to be.   

This example is a perfect illustration unit tests are such a nice thing to have in Python-land: a unit test would probably catch the change in signature right away, alerting your helpful co-worker to the can of worms they have opened up by changing the output of the function. But the real moral of the story is how dangerous it is to rely on implicit knowledge of structures – like the ordering of a list – instead of on explicit instructions. When somebody fails to understand the implications of that ordering, bad things will happen. When the knowledge you need to debug the problem is hidden, things will be  
even worse.  

[![](http://images6.fanpop.com/image/photos/36000000/Harrison-in-Star-Wars-Empire-strikes-back-harrison-ford-36029606-3257-2231.jpg)](http://images6.fanpop.com/image/photos/36000000/Harrison-in-Star-Wars-Empire-strikes-back-harrison-ford-36029606-3257-2231.jpg)

_Sometimes things get complicated_

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#return-classes-strike-back)Return classes strike back

In most languages the way around this is to create a class that holds the results of something like `some_function`. A result class provides clear, named access to what’s going on:  

    :::python  
    class SomeFuncResult(object):  
         def __init__(self, node, attr, val):  
             self.node = node  
             self.attribute = attr  
             self.value = val  
      
     # and inside of some_function()  
    ...  
        results.append(SomeFuncResult(object, attrib, val))  
    ...  
    

This means the receiving code is much neater and easier to understand:  
    
    :::python    
    results = some_function()  
    for item in results:  
        cmds.setAttr(item.node+ "." + item.attribute, item.value)  
    

This is a better record of what you were trying to achieve in the first place, and it’s also much more survivable: as long as HelpfulCoworker01 does not actually rename the fields in the result object it can be tweaked and updated without causing problems.  

## A bit less classy

For many cases this is the right way to go. However it comes with some drawbacks of its own.   

First off – let’s be honest – there’s a lot of typing for something so dull. I always try to leave that out of the equation when I can - the time spent typing the code is such a tiny fraction of the time you’ll spend reading it that trying to save a few keystrokes is usually a Bad Idea (tm). However, typing 5 lines when you could just type a pair of bracket does feel like an imposition – particularly when the 5 lines are 100% boring boilerplate.  

The second issue is that, being a class, `SomeFuncResult` is comparatively expensive: it costs a smidge more in both memory and processor time than just a list or a tuple of values. I’m ranking this behind the typing costs deliberately, because most of the time that increment of cost doesn’t matter at all: if you’re dealing with a few hundred or even a few thousand of them, at a time the costs for spinning up new instances of `SomeFuncResult` just to hold data are going to be invisible to users. However, if you are doing something more performance-intensive the costs of creating a full mutable object can be significant in large numbers. As always, [it’s wiser not to try to optimize until things are working](http://techartsurvival.blogspot.com/2015/04/the-right-profile.html) but this is still a consideration worth recalling.  

The last issue (but probably the most important) is that `SomeFuncResult` can be changed in flight. Since it is a class, the data in a `SomeFuncResult` can be updated (for you CS types, it is _mutable_). This means some other piece of code that looks at the result object in between `some_function` and you might can decide to mess with the results. That can be a feature or a bug depending on how you want to code it – but since Python does not have a built-in mechanism for locking fields in an object, you’d have to put in extra work to make sure the results didn’t get changed by accident if keeping the data pristine was mission-critical. You can use the a property decorator to make a fake read only field:  
    
    :::python
    class SomeFuncResult(object):  
         def __init__(self, node, attr, val):  
             self._node = node  
             self._attribute = attr  
             self._value = val  
      
        @property  
        def node(self):  
            return self._node  
      
        @property  
        def attribute(self):  
            return self._attribute  
      
        @property  
        def value(self):  
            return self._value  
    

Alas, our 5 lines of boilerplate have now blossomed into 16. Our quest for clarity is getting expensive.  
  

[![](https://s-media-cache-ak0.pinimg.com/originals/ec/cf/c1/eccfc13e87cc987cbe29fadb248e3b6b.jpg)](https://s-media-cache-ak0.pinimg.com/originals/ec/cf/c1/eccfc13e87cc987cbe29fadb248e3b6b.jpg)

## [obiter dicta](https://en.wikipedia.org/wiki/Obiter_dictum)
  
One common way to get around the hassles – or at least, they typing costs –of custom return objects is simply to use dictionaries instead. If you use the [perforce Python API](http://www.perforce.com/perforce/doc.current/user/p4pythonnotes.txt) you’ll be quite familiar with this strategy; instead of creating a class, you just return dictionaries with nice descriptive names   

    :::python    
    for node in object_list  
        for attrib in attrib_list:  
            settable = is_attrib_settable(node, attrib)  
            if settable:  
               new_value = dict_of_defaults[attrib]  
               results.append ({'node':node, 'attribute':attrib, 'value':new_value})  
    return results  
    
  
Like a custom class this increases readability and clarity; it’s also future proof since you can add more fields to the dictionary without messing with existing data.   

Even better, dictionaries – unlike classes – are self-describing: in order to understand the contents of a custom result class like `SomeFuncResult` you’ll have to look at the source code, whereas you can see the contents of a result dictionary with a simple print statement. Dictionaries are slightly cheaper than classes (there is a [good workaround](http://stackoverflow.com/questions/1336791/dictionary-vs-object-which-is-more-efficient-and-why) to speed up classes, but it’s something you have to write and maintain). And, of course, dictionaries have minimal setup costs: they are boiler-plate free.  

This doesn’t mean they are ideal for all circumstances, however.   
The Achilles’ heel of using dictionaries is keys, which are likely to be strings. Unless you are very disciplined about using named constants for all your result dictionaries you’ll inevitably find that somebody somewhere has typed `attribite` with an  _i_ instead of a _u_ and suddenly perfectly valid, impeccably logical code is failing because nobody thought to look at the key names. Instead of typing lots of setup code once, you’ll be dribbling out square brackets and quotes till the end of time, with lots of little missteps and typos along the way. While that’s not an insurmoutable problem it’s another annoyance.  

[![](http://assets7.thrillist.com/v1/image/1335116/size/tl-horizontal_main_2x/amazing-1983-return-of-the-jedi-photos-you-ve-never-seen)](http://assets7.thrillist.com/v1/image/1335116/size/tl-horizontal_main_2x/amazing-1983-return-of-the-jedi-photos-you-ve-never-seen)

_Not so scary when you know the secret!_

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#return-of-the-namedtuples)Return of the namedtuples

Luckily there is yet another – and for most purposes better – way to return complex results — one that is both flexible and self-describing. [namedtuples](http://pymotw.com/2/collections/namedtuple.html) are part of the python standard library and they offer a clean, simple way to create lightweight objects that have named properties – like classes – but require almost no setup: you can create a new type of named tuple with a single line of code, and then use it like a lightweight (and immutable) class.  
A namedtuple is just a python tuple that can also use names to access it’s own fields. For example:  

    :::python    
    from collections import namedtuple  
      
    # create a namedtuple called 'SomeFuncRes' to hold nodes, attributes and values  
    SomeFuncRes = namedtuple("SomeFuncRes", "node attribute value")  
      
    # make an instance  
    example = SomeFuncRes('pCube1', 'tx', 33.0)  
    # Result: SomeFuncRes(node='pCube1', attribute='tx', value=33.0)  
    

As you can see, namedtuples are as even easier to ‘read’ than dictionaries when printed out. However, namedtuples give you dot-access to their contents.

    :::python
    print example.node  
    # pCube1  
    

This saves a few characters: `result.node` beats `result['node']` – but mopre important offers with far fewer opportunities for mistyped keys or open quotes.   
However, namedtuples can also use old-fashioned indexed access too:  

    :::python   
    print example[0]  
    # pCube1  
    

And you can even iterate over them if you need to, since a namedtuple is in the end just a slightly fancier tuple:  

    :::python    
    for item in example:  
        print item  
      
    # pCube1  
    # tx  
    # 30  
    

Namedtuples are easy to instantiate: You can create them using index ordering, names, or \*\*keyword arguments. Names tend to be better for clarity, but if you’re expanding the results of other functions like `zip()` indices and double-starred dictionaries can be very handy. Having all three options allows you to create them in the most appropriate way.  

    :::python
    print SomeFuncRes('pSphere1', 'ry', 180)  
    # SomeFuncRes(node='pSphere1', attribute='ry', value=180)  
    print SomeFuncRes(value = 1, node = 'pCube1', attribute = 'tz')  
    # SomeFuncRes(node='pCube1', attribute='tz', value=1)  
    from_dict  = {'node':'pPlane1', 'attribute':'rz', 'value':40.5}  
    SomeFuncRes(**from_dict)  
    # SomeFuncRes(node='pPlane1', attribute='rz', value=40.5)  
    

One of the great advantages of namedtuples is that (unlike classes or dictionaries) namedtuples are _immutable_; that is, they are read-only by default. This is usually a Good Thing<sup>tm</sup> for a result object, since data changing in mid-flight can lead to subtle bugs that may be very hard to reproduce. Immutability also makes them cheaper: they don’t require Python to do as much setup behind then scenes when a they are created, which can be significant in large quantities. They usually [take up less memory as well](http://blog.explainmydata.com/2012/07/expensive-lessons-in-python-performance.html).   

This combination of features is tough to beat in a cheapo data-only class. If for some reason you need to upgrade to a real class instead, you probably won’t even need to change the code which reads your namedtuples: Python doesn’t care if `result.node` is a namedtuple field or a regular object field. For all these reasons, namedtuples are a great little tool for a lot of common data-bundling jobs. No strategy fits every battle, but namedtuples are an excellent - and often overlooked! – way to manage this very common (albeit not very interesting) problem and to keep your overall toolkit cleaner, more robust and easier to maintain.  

[![](http://iruntheinternet.com/lulzdump/images/its-a-trap-pun-its-a-wrap-admiral-ackbar-star-wars-1363199217Z.jpg?id=784)](http://iruntheinternet.com/lulzdump/images/its-a-trap-pun-its-a-wrap-admiral-ackbar-star-wars-1363199217Z.jpg?id=784)

  


