Title: The Dog Ate My Homework
Date: 2014-10-30 09:55:00.001
Category: blog
Tags: , , , , 
Slug: _the_dog_ate_my_homework
Authors: Steve Theodore
Summary: pending

I had an interesting issue at work the other day. While the details are unit-test specific, I learned a useful general idea that’s worth sharing.  
  
We run all of our various Maya tools through a single build system which runs unit tests and compiles code for our different targets (currently Maya 2011 and 2015). Ordinarily, since I’m very allergic to using binaries when I don’t have to, this multi-maya setup doesn’t cause us a lot of headaches. I have a little extractor routine which unzips the few binaries we do distribute in the right places, and all the rest of the code is blissfully unaware of which Maya version it’s running (with the exception of the nasty [ls bug I mentioned a few weeks ago](http://techartsurvival.blogspot.com/2014/09/2015-bug-watch-ls.html).)  
  


[![](http://rs1img.memecdn.com/how-many-times-have-you-heard-amp-quot-my-dog-ate-my-homework-amp-quot_fb_2216011.jpg)](http://rs1img.memecdn.com/how-many-times-have-you-heard-amp-quot-my-dog-ate-my-homework-amp-quot_fb_2216011.jpg)

  


  
Last week, however, we added a new tool and accompanying test suite to the toolkit. It works fine in 2015 (where we do all of our actual development right now), but crashes in 2011. After a bit of head-scratching we eventually realized that this one was absurdly simple: the test uses a saved Maya so that it can work with known, valid data. Of course the file was saved from Maya 2015, so when the Maya 2011 version of the tests tries to run boot up, it falls over because 2011 won’t read a 2015 file.  
Or, as the checkin comment has it, “Doh!”  
  


## Test cancelled!

  
The obvious fix is just to skip the test in Maya 2011 - a test that can never pass is hardly generating much useful information, and the likelihood that our small pool of 2011 customers actually need this tool is low anyway. Skipping a test is easy enough if you’re running the tests manually in an IDE – but a lot more complex if you’re got a build server that’s trying to auto-detect the tests. Plus, designing a system that makes it _too_ easy to skip tests is a Bad Thingtm; - you generally want all of your tests running all the time, since “I’ll re-enable that test after I deal with this problem” is right up there with “the check is in the mail” and “it’s not you, it’s me” in the probity department.   
So, the goal is to allow us to conditionally disable tests based on a hard constraint - in this case, when they are running on an inappropriate version of Maya - without compromising the tests as a whole . Secondarily it would be nice to do this without any kind of central registry file - we’d really just like the tests to just run, except when they _can’t_.  
  


[![](http://i1.wp.com/lotsofhumor.com/wp-content/uploads/2013/04/didnt-study-for-test-test-cancelled.jpg)](http://i1.wp.com/lotsofhumor.com/wp-content/uploads/2013/04/didnt-study-for-test-test-cancelled.jpg)

  


  
Now, typically a test runner will detect tests by looking for classes that derive from [unittest.TestCase](https://docs.python.org/2/library/unittest.html). The easiest way to skip the test, therefore, is simply not to define it at all - if the test runner doesn’t see the class when it imports your test modules, we’ll be fine. _Note: this strategy won’t work if you have some kind of hand-rolled test harness that finds tests by string parsing file contents or something like that! However, you probably want to be doing the standard thing anyway… As they say in Python land, [“There should be one– and preferably only one –obvious way to do it.”](http://legacy.python.org/dev/peps/pep-0020/)_  
  
In C++ or C# you could do this with a “preprocessor directive”, aka a “#define” - a conditional check that runs at compile time to include or exclude certain parts of a file.   
  
In Python we don’t even need that: you can just inline the check in your file and it will execute when the module is imported. Here’s a simple example which conditionally use Raymond Hettinger’s [ordereddict module](https://pypi.python.org/pypi/ordereddict) in Python 2.6 and the equivalent built-in version in Python 2.7:  
  
    :::python
    import sys  
      
    if sys.version_info.major == 7:  
        from collections import OrderedDict  
    else:  
        from ordereddict import OrderedDict  
    

  
_(If you are total #IFDEF addict there is also the [pypredef module](http://stackoverflow.com/questions/482014/how-would-you-do-the-equivalent-of-preprocessor-directives-in-python). Not my cup of tea, but the author does make some good points about the utility of his approach). _  
  
The inline approach works fine in small amounts, but it’s aesthetically unappealing - it forces a bunch of module-level definitions away from the left margin, visually demoting them from important names to generic code blocks. More importantly, it’s easy to mess up: a misplaced indentation can radically change the contents of your file, and even though I’m a big fan of indentations over cur lies, I miss my indents with depressing regularity.  
  
Fortunately, Python has an elegantly succinct way of annotating code for higher-level purposes without messing up the visual cleanliness and logical flow: [decorators](http://www.artima.com/weblogs/viewpost.jsp?thread=240808). Decorators are handy here for two reasons: first off, they express your intent very clearly by telling future readers something unambiguous about the structure of your code. Secondly, they can execute code (even fairly complex code, though frankly it’s a bad idea for what I’m describing here!) without compromising the layout and readability of your module.  
The particularly nice thing about decorators in this case is that the way decorators work in any case is a natural match for the problem we have.   


## The substitute teacher

A decorator is just a function (or a callable class) which takes another function or class as an argument. When Python finds a decorated function or class, it calls the decorator function and passes the target – that is, the decorated bit of code – as an argument Whatever comes out of the decorator function is then swapped in for the original code.   
Here’s a simple example, using functions for simplicity:  
 
    :::python   
    def decorated(original_func):  
            def replacement_func(arg):  
            # this function replaces the original  
            # it only knows what the original does  
            # because that was passed in when the  
            # decorator was called....  
            print "calling original"  
            result = original_func(arg)  
            print "original says : ", result  
            return result  
        return replacement_func   
        # return our new replacement function  
        # but bind it to the name of the original  
      
    @decorated  
    def size(arg):  
       return len(arg)  
      
    example = size( [1,2,3])  
    # calling original  
    # original says : 3  
    print example:  
    # 3  

The decorator can completely replace the original code if it wants to:  
  

    :::python    
    def override(original_func):  
       def completely_different():  
           return "and now for something completely different"  
      
    @override  
    def parrot():  
        return "I’d like to make a complaint about a parrot"  
      
    print parrot()  
    # and now for something completely different  
    

  
Or, it could leave it untouched too:  

    :::python    
    def untouched(original_func):  
        return original_func  
      
    @untouched  
    def spam():  
        return "spam!"  
      
    print spam()  
    #spam!  
    

  
The essential thing here is that the decorator sort of like one of those elves who swap out children for changelings. Officially nothing has changed - the name you defined in the un-decorated code is right there - but under the hood it may be different.  


[![](http://bartsblackboard.com/files/2009/11/The-Simpsons-05x11-Homer-The-Vigilante.jpg)](http://bartsblackboard.com/files/2009/11/The-Simpsons-05x11-Homer-The-Vigilante.jpg)



## Mandatory testing

Once you understand the decorator-as-changeling idea, it becomes pretty easy to see how the decorator can allow code swaps based on some condition. You might, for example, try to patch around a function which returns an empty list in Maya 2014, but [crashes in Maya 2015](https://www.blogger.com/blogger.g?blogID=3596910715538761404)(link):  
  
    
    :::python  
    def safe_2015(original_func):  
            if '2015' in cmds.about(v=True):  
            # wrap it for safety in 2015  
            def safe\_ls(*args, **kwargs):  
                try:  
                    return original_func(*args, **kwargs)  
                except RuntimeError:  
                    return []()  
            return safe_ls  
        else:  
            # send it back unchanged in non-2015  
            return original_func  
      
    @safe_2015    
    def do_something():  
       \#....  
    

  
> Disclaimer: I wouldn’t use this code in practice! It’s a good example of the principle, but not a wise way to patch around the 2015 ls bug.  
  
Returning at long last to the problem of suppressing tests: we just need to harness the power of decorators to replace the class definition of our test classes with something else that won’t get run by our test suite. And, luckily, that’s really easy to do since we don’t have to return anything:  
  
    :::python    
    def Only2015(original):  
        if '2015' in cmds.about(v=True):  
                return original # untouched!  
            else:  
                return object # the decorated class is now just object  
    

  
So if your do something like this in your tests:  
  

    :::python    
    from unittest import TestCase  
    import maya.standalone  
    try:  
        maya.standalone.initialize()  
    except:  
        pass  
      
      
    @Only2015  
    class Test2015Only(TestCase):  
        def test_its_2015(self):  
            assert '2015' in cmds.about(v=True)  
      
    class TestOtherVersions(TestCase):  
        def test_any_version(self):  
            assert '20' in cmds.about(v=True)  
    

  
As you’d expect, both of these test will run and pass when run on a Maya 2015 python. However, under any other version of Maya the file really looks like this:  
  

    :::python    
    from unittest import TestCase  
        import maya.standalone  
        try:  
            maya.standalone.initialize()  
        except:  
            pass  
      
    # in 2014 <, this TestCase class has been replaced by a dumb object() class  
    class Test2015Only(object):  
        pass  
      
      
    class TestOtherVersions(TestCase):  
        def test\_any\_version(self):  
            assert '20' in cmds.about(v=True)  
    

  
Because `Test2015Only()` is now an `object()` instead of a `TestCase()`, the test runner doesn’t even see it and doesn’t try to run it.  


## Makeup work

This is a lovely example of why Python can be so much fun. The language has the magical ability to extend itself on the fly - in this case, change the meaning of whole blocks of otherwise conventional code - but at the same time it offers simple, conservative mechanisms that keep that process for degenerating into mere anarchy (or, worse, into _[JavaScript](http://qph.is.quoracdn.net/main-qimg-eb6eb210fd4116ef10fee083428ed482?convert_to_webp=true)_).  
  
This particular gimmick was a great way to clean up our messy test set. Predictably, about 30 seconds I verified that it worked I was starting to brainstorm all sorts of cool new uses for this tactic.   
  
A few more minutes of reflection, however, brought me to see that this kind of trick should be reserved for special occasions. The ability to swap the contents of a name based on runtime condition is definitely cool - but it’s hardly a good practice for readability and maintenance down the road. It happens to be a nice fit for this problem because a test is never going to be used by anything other than the test suite. Trying the same thing with, say, a geometry library that gets imported all over the place would be a nightmare to debug.  
  
Magic is wonderful but, best used _sparingly_.  

[![](http://pad2.whstatic.com/images/thumb/f/f5/Get-out-of-Class-Step-6.jpg/670px-Get-out-of-Class-Step-6.jpg)](http://pad2.whstatic.com/images/thumb/f/f5/Get-out-of-Class-Step-6.jpg/670px-Get-out-of-Class-Step-6.jpg)

  


