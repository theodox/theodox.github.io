Title: The right profile
Date: 2015-04-18 22:16:00.000
Category: blog
Tags: python, programming, maya 
Slug: _the_right_profile
Authors: Steve Theodore
Summary: A brief, gentle introduction to the uses and abuses of profiling in Maya Python

Lately I was working in one of those relatively rare TA tasks where performance really mattered. I had to do a lot of geometry processing and the whole thing was as slow as molasses, despite all my best guesses about clever little tricks to speed things up. 

To break the logjam, I resorted to actual profiling, something I tend to avoid except in emergencies. 

Now, you might wonder why I say I avoid profiling. If you skip ahead and see the trick I used here, and all the fiddly little bits of detailed performance data it provides, you may be particularly curious why anybody would want to pass up on all this cool, authoritative data. The reason, however, is really simple: Good profiling is so powerful that it can be overly seductive. Once you can see right down to the millisecond how tiny tweaks affect your code, the temptation to start re-working everything to shave a little bit off here and there is hard to escape.

If you're working on a game engine, constant reference to the profiler might make sense. In regular TA work, however, milliseconds rarely matter: all that counts is the user's perception of responsiveness. Your users will care about the difference between a .1 second tool and a 1 second tool, or that between a 1 second tool and a 10 second tool. They are unlikely to care about - or even notice - the difference between a 1.3 second tool and a 1.1 second tool. The time you spend grinding out those extra fractions of a second may just not be worth it. As Donald Knuth, one of the great-grandaddies of all programming put it:

> We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. 

So a word of warning before we proceed. Optimize late, only after you've got the problem solved and after you've got what seems like solid, working code that's just too slow. Stay focused on clarity, reliability and ease of maintenance first; only reach for the profiler in code where the perf has really become an issue. 

## Cheap-ass profiling

Python includes some excellent native profiling tools. The easiest one to use (and the one that's most handy for people working in Maya) is the [`cProfile`](https://docs.python.org/2/library/profile.html) module. It allows you to extract very detailed timing and call-count information from a run of a function. 

Here's a basic example of profile in action. We'll start of with a couple of simple functions. 
    
    
    import time  
    import cProfile  
      
      
    def some_math(n):  
        return n ** n  
      
    def slow():  
        time.sleep(.01)  
      
    def do():  
        counter = 0  
        for i in range(200):  
            counter += 1  
            some_math(counter)  
            slow()  
    

Then we'll call them using `cProfile.run()`. The run function takes a string which it will use `eval` to execute. So in our case:
    
    
    cProfile.run('do()')  
    

That will print out the following report, or something pretty like it:
    
    
         604 function calls in 2.096 seconds  
      
    Ordered by: standard name  
      
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)  
        1    0.002    0.002    2.096    2.096 <maya console>:12(do)  
      200    0.003    0.000    0.003    0.000 <maya console>:6(some_math)  
      200    0.002    0.000    2.091    0.010 <maya console>:9(slow)  
        1    0.000    0.000    2.096    2.096 <string>:1(<module>)  
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}  
        1    0.000    0.000    0.000    0.000 {range}  
      200    2.089    0.010    2.089    0.010 {time.sleep}  
    

The first line in the report prints out the total time, in this case a shade over 2 seconds. Each line in the report that follows lists the following information for a single function call (including nested calls)

ncalls
    The number of times a given function was called during this run. If the function is recursive, this number may show up as two numbers separated by a a slash, where the first is the true number of total calls and second the number of direct, non-recursive calls. As you can see here `do()` itself was called only once, but the sub-functions `some_math()` and `slow()` were each called 200 times; `time.sleep()` was called 200 times as well since it was called by every iteration of `slow()`
tottime
    the total amount of time spent executing this function for the entire run. As you can see the call to `time.sleep` occupies the bulk of the time in this run. Not that this is the time it takes to process the function - _not_ the real-world time it takes to run! So our `do()` function in the first line shows a `tottime` of .002 seconds even though it clearly took more than two seconds to run. 
percall
    The _average_ time spent executing the function on this line, if it was executed multiple times. Like `tottime`, this measures processor time only and does not include things like network delays or (as in this case) thread sleeps.
cumtime
    this is the real world time needed to complete the call, or more precisely the total real world time spent on all of the calls (as you can see, it's the sleep call and `do()` which each take up about two seconds)
percall
    the second percall column is the amount of average amount of real-world time spent executing the function on this line.
filename
    this identifies the function and if possible the origin of the file where the function came from. Functions that originate in C or other extension modules will show up in curly braces.

As you can see this is _incredibly_ powerful right out of the box: it lets you see the relative importance of different functions to your overall perfomance and it effortlessly includes useful back-tracking information so you can find the offenders.

## Record Keeping

If you want to keep a longer term record, you can dump the results of `cProfile.run()` to disk. In this form:
    
    
    cProfile.run('do()', "C:/do_stats.prf")  
    

You'll get a dump of the performance data to disk instead of an on-screen printout. A minor irritant is the fact that the dumped stats are not the plain-text version of what you see when running the stats interactively: they are the pickled version of a `Stats` object: just opened in a text editor they are gibberish.

To read them you need to import the `pstats` module and create a new `Stats` from the saved file. It's easy:
    
    
    import pstats  
    disk_stats = pstats.Stats("C:/do_stats.prf")  
    

Calling the `print_stats` method of your new `Stats` object will print out the familiar report. You can also use the `sort_stats` method on the object to reorganize the results (by call count, say, or cumulative time). 

The details on the `Stats` object are [in the docs](https://docs.python.org/2/library/profile.html#pstats.Stats)

## Caveats

I've already said that this kind of information can tempt you to cruise past to point of diminishing returns right on to squeezing-blood-from-a-stone-land. That said it's also worth noting that there is also bit of the Heisenberg uncertainty principle at work here: profiling slightly changes the performance characteristics of your code Game engine programmers or people who do embedded systems for guided missiles will care about that: you probably don't need to.

In any case, approaching this kind of profiling with the wrong mindset will drive you crazy as you chase micro-second scale will-o-the-wisps. The numbers give a good general insight into the way your code is working, but don't accord them any larger importance just because they seem seem so official and computer-y. They are guidelines, not gospel.

## Using the data

When you actually do start optimizing, what do you want to do with all those swanky numbers? The art of optimizing code is _waaaay_ too deep to cover in a few paragraphs but there are a couple of rules of thumb that are handy to think about while learning how to read the profile results:

### Call Counts Count

The first thing to look at is _not_ the times: it's the call counts. 

If they seem wildly out of line, you may have inadvertently done something like call a more than you intended. If you have a script that does something to 500-vertex object but a particular vertex-oriented function shows up 2000 or 4000 times, that may mean you're approaching the data in an inefficient way. If it becomes something huge - like 250,000 calls - it sounds like you're doing an "all against all" or "n-squared" check: an algorithm that has to consider not just every vert, but every vertex-to-vertex relationship. These are generally something to avoid where possible, and the call count totals are a good way to spot cases where you've let one slip in by accident. 

**The evils of 'n-squared' and so on are illustrated nicely [here](http://rob-bell.net/2009/06/a-beginners-guide-to-big-o-notation/). You might also want to check out [Python Algorithms](http://astore.amazon.com/tecsurgui-20/detail/1430232374) if you're really getting in to waters where this kind of thing matters!**

### Look for fat loops

The second thing too look at is the balance of times and call counts. The most performant code is a mix of infrequent big calls and high-frequency cheap ones. If your stats show a high call count and a high `cumtime` on the same line, that's a big red flag saying "investigate me!" As you can see in the report above, the real villains (`slow()` and in turn `time.sleep()`) are easily spotted by the combination of high call counts and high cumtime numbers.

### Use builtins where possible

Next, you want to check the balance between your own code and built-ins or Maya API code, as indicated by the curly brackets around the function names in the last column. In general, API or built-in calls are going to be faster than anything you write yourself: doing things like a deriving the distance between two 3-D points will usually run about 8x faster in the API than it would in pure python. So, you'd like to see lots of those kinds of calls, particularly inside loops with high call counts. 

### High cumtimes

Only after you've sorted through the high call counts, and high call/cumtime combinations, and aggressive use of builtins do you want to start looking at high cumtimes on their own. Of course, you won't have a good idea when those high times are _justified_ if you don't know how the code actually works, which is why you want to do your optimizing passes on code that is already legible and well organized. 

## Wrap

Naturally, these few notes just scratch the surface of how you optimize - this post is really about _profiling_ rather than optimizing. I'm sure we'll hit that topinc some other day. In the meantime, it's worth spending some time mastering the slightly retro, programmer-esque interface of the cProfile module. Doug Hellman's [_Python Module Of the Week_ article](http://pymotw.com/2/profile/) on profiling is a good if you want to get beyond the basic report i'm using here. There's also a nice lightweight intro at [Mouse vs Python](http://www.blog.pythonlibrary.org/2014/03/20/python-102-how-to-profile-your-code/). The [docs](https://docs.python.org/2/library/profile.html#) could be more friendly but they are authoritative.

In the meantime, readers of a certain age will certainly remember who _really_ had the right profile

  


