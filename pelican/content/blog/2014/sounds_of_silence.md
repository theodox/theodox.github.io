Title: The sounds of (Python) Silence
Date: 2014-01-02 10:45:00.000
Category: blog
Tags: programming, maya, python
Slug: sounds_of_silence
Authors: Steve Theodore
Summary: A class for managing overly chatty Python modules

After a long vacation with my children, I've been meditating on the virtues of silence.  
  
Python is a glorious toybox bursting with fun gadgets to delight TA's near and far.  You can easily use it to stuff anything from database access to a serial port controller into your copy of Maya, which is a always fun (and occasionally useful).  However the [plethora](http://www.youtube.com/watch?v=-mTUmczVdik) of Python libraries out there does bring with it a minor annoyance - if you grab something cool off [the cheeseshop](https://pypi.python.org/pypi) you don't know exactly how the author wants to communicate with users.  All too often you incorporate something useful into your Maya and suddenly your users have endless reams of debug printouts in their script listener -- info that might make sense to a coder or a sysadmin but which is just noise (or worse, slightly scary) for your artists.  

  
If you're suffering from overly verbose external modules, you can get a little peace and quiet with this little snippet. The Silencer class is just a simple [context manager](http://docs.python.org/2.7/reference/datamodel.html#context-managers) that hijacks _sys.stdout_ and _sys.stderr_ into a pair of StringIO's that will just silently swallow any printouts that would otherwise go to the listener.   

    :::python
    import sys
    from StringIO import StringIO
    
    class SilencedError ( Exception ):
        pass

    class Silencer( object ):
        '''
        suppress stdout and stderr
        
        stdout and stderr are redirected into StringIOs.  At exit their contents are dumped into the string fields 'out' and 'error'
        
        Typically use this via the with statement:
        
        For example::
            
            with Silencer() as fred:
                print stuff
            result = fred.out
            
        note that if you use a silencer to close down output from the logging module, you should call logging.shutdown() in the silencer with block
        '''

        def __init__( self, enabled=True ):
            self.oldstdout = sys.stdout
            self.oldstderr = sys.stderr
            self._outhandle = None
            self._errhandle = None
            self.out = ""
            self.err = ""
            self.enabled = enabled

        def __enter__ ( self ):
            if self.enabled:
                self.oldstdout = sys.stdout
                self.oldstderr = sys.stderr
                sys.stdout = self._outhandle = StringIO()
                sys.stderr = self._errhandle = StringIO()
                self._was_entered = True
                return self
            else:
                self._was_entered = False

        def _restore( self ):
            if self._was_entered:
                self.out = self._outhandle.getvalue()
                self.err = self._errhandle.getvalue()
                sys.stdout = self.oldstdout
                sys.stderr = self.oldstderr
                self._outhandle.close()
                self._errhandle.close()
                self._outhandle = self._errhandle = None

        def __exit__( self, type, value, tb ):
            se = None
            try:
                if type:
                    se = SilencedError( type, value, tb )
            except:
                pass
            finally:
                self._restore()
                if se: raise se
  


If you actually need to look at the spew you can just look at the contents of the _out_ and _error_ fields of the Silencer.   More commonly though you'll just want to wrap a particularly verbose bit of code in a _with... as_ block to shut it up.  You'll also get the standard context manager behavior: an automatic restore in the event of an exception, etc.  
  
  


  


