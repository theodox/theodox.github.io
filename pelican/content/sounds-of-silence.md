Title: The sounds of (Python) Silence
Date: 2014-01-02 10:45:00.000
Category: blog
Tags: programming, maya, python
Slug: sounds-of-silence
Authors: Steve Theodore
Summary: pending

After a long vacation with my children, I've been meditating on the virtues of silence.  
  
Python is a glorious toybox bursting with fun gadgets to delight TA's near and far.  You can easily use it to stuff anything from database access to a serial port controller into your copy of Maya, which is a always fun (and occasionally useful).  However the [plethora](http://www.youtube.com/watch?v=-mTUmczVdik) of Python libraries out there does bring with it a minor annoyance - if you grab something cool off [the cheeseshop](https://pypi.python.org/pypi) you don't know exactly how the author wants to communicate with users.  All too often you incorporate something useful into your Maya and suddenly your users have endless reams of debug printouts in their script listener -- info that might make sense to a coder or a sysadmin but which is just noise (or worse, slightly scary) for your artists.  


  
If you're suffering from overly verbose external modules, you can get a little peace and quiet with this little snippet. The Silencer class is just a simple [context manager](http://docs.python.org/2.7/reference/datamodel.html#context-managers) that hijacks _sys.stdout_ and _sys.stderr_ into a pair of StringIO's that will just silently swallow any printouts that would otherwise go to the listener.   


  
  


If you actually need to look at the spew you can just look at the contents of the _out_ and _error_ fields of the Silencer.   More commonly though you'll just want to wrap a particularly verbose bit of code in a _with... as_ block to shut it up.  You'll also get the standard context manager behavior: an automatic restore in the event of an exception, etc.  
  
  


  


