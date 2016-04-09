Title: Your weekly moment of Python-is-awesome
Date: 2014-05-27 22:58:00.001
Category: blog
Tags: 
Slug: Your-weekly-moment-of-Python-is-awesome
Authors: Steve Theodore
Summary: pending

I stumbled across a cool little idea while working on a refactor of my python tools build system, and although it is not really ready for prime-time it's fun enough I had to share.  With a little bit of work you can _load Python modules directly over the web via http!_  How cool is that?  
  
Details  &amp; code after the jump  
  
  
  
In the past I've always gave users a userSetup.py which automatically downloads a zip file containing all the rest of my code from a net share. While this works quite well, the userSetup file itself is a bit of a weak link. Although it changed pretty rarely, it was a bit more complex than I liked. In an ideal world, the user setup would be just a couple of lines, highly resistant to breakage and easy to leave untouched for months or years.  All the changeable stuff should happen off in the ether, so users always get the latest hotness.  
  
While pondering how to improve this, I was trolling Doug Hellman's invaluable [Python Module of the Week](http://pymotw.com/2/) site and stumbled onto his discussion of [custom Python module finders](http://pymotw.com/2/sys/imports.html). Basically, a module finder is a class which you can register with python to tell it how to look for modules. The key word there is 'how', not where' -- a module finder can do anything it wants to find or create a module, as long as it has returns an object with a load_module method that python can use to actually pop the code into sys.modules. It's particularly cool because the process is _completely transparent_ to the calling code: if you call  
  
`import XXX`  
  
you'll get XXX, even if your custom finder/loader had to generate it by consulting the _I Ching _and waiting for the right phase of the moon.  
  
That sounds like fun (jeez, my sense of fun has gotten pretty esoteric). So, I hacked up a highly experimental example of a module loader that will look on the web for a python module being served up via http and import it as if it were local.  
  
 Here's the first bit, the module finder which is in charge of looking for the code when somebody says 'import xxx':  
  

    
    
      
    '''  
    web_shim.py  
      
    Exposes a custom module loader and importer which allow for download, cache and  
    load of python modules stored on an HTTP server  
      
    To activate, add the class to sys.path_hooks:  
      
        sys.path_hooks.append(WebFinder)  
    '''  
      
    import imp  
    import sys  
    import urllib2  
    import binascii  
    import os  
    import tempfile  
      
      
    class WebFinder(object):  
        '''  
        A custom module finder (background: http://pymotw.com/2/sys/imports.html)  
        that will find and load modules via http connections, as long as the  
        module file's parent http path is on the system path  
      
        The module file is downloaded to the users temp directory. When it changes, it  
        will be replaced with the latest version from the server. Returns a WebLoader  
        for the cached file.  
        '''  
        CACHE_DIR = tempfile.gettempdir()  
      
        def __init__(self, path_entry):  
            if not "http" in path_entry:  
                raise ImportError()  
            self.url = path_entry  
            self.cache = os.path.normpath(self.CACHE_DIR)  
            return  
      
        def find_module(self, fullname, path=None):  
            expanded = os.path.normpath(os.path.join(self.cache, fullname + ".py"))  
            try:  
                target_url = (self.url + "/" + fullname + ".py")  
                self.target_url = target_url  
                dl = urllib2.urlopen(target_url).read()  
                crc = binascii.crc32(dl) & 0xffffffff  
                old = 0xffffffff  
                try:  
                    handle = open(expanded, 'rt')  
                    disk_date = handle.read()  
                    handle.close()  
                    old = binascii.crc32(disk_date) & 0xffffffff  
                except:  
                    old = 0xffffffff  
                if crc != old:  
                    handle = open(expanded, 'wt')  
                    handle.writelines(dl)  
                    handle.close()  
                return WebLoader(self.target_url, expanded, fullname)  
            except:  
                if (os.path.exists(expanded)):  
                    return WebLoader(self.target_url, expanded, fullname)  
      
    

  
 The module finder's job is to be pointed at a path (in this case, 'self.url') If the path is not something this finder knows how to handle, it raises an ImportError. Otherwise, it sticks around until Python calls find_module with a module name, at which point it will return a module loader object (see below) or None if it doesn't know what to do.  
  
In this case, we do everything as simply as possible. The finder only works on a path with 'http' in it (note that's not really the right way to check for a url! It's enough for proof of concept, though). The finder just fills out the path with the name of the module (plus ".py") and tries to download it into the user's temp directory. The business with the hex numbers is just a crc check to make sure that the downloaded module is the latest version. If this is the first time you've grabbed the file -- or if the code on the server has changed  \-- the cached copy will be refreshed.  
  
The second half of the operation is the WebLoader, which loads the cached module:  
  

    
    
      
    # usess the same imports as WebFinder.py  
      
    class WebLoader(object):  
        '''  
        Import loader (see http://pymotw.com/2/sys/imports.html for background)  
        which loads modules cached by a WebFinder using imp.load_source  
        '''  
        def __init__(self, url, filepath, name):  
            self.url = url  
            self.name = name  
            self.file = filepath  
            return  
      
        def load_module(self, fullname):  
            if fullname in sys.modules:  
                mod = sys.modules[fullname]  
                return mod  
                # bail now so we don't mislead users  
                # if mod was found somewhere else!  
            else:  
                mod = sys.modules.setdefault(fullname, imp.load_source(fullname, self.file))  
                mod.__file__ = self.file  
                mod.__name__ = fullname  
                mod.__path__ = [self.url]  
                mod.__loader__ = self  
                mod.__package__ = '.'.join(fullname.split('.')[:-1])  
                return mod  
    

  
A moduleloader can do all sorts of fancy things (the test code on PyMOTW, for example, loads a module from a python shelf database) but in this case I'm doing the simplest thing possible, which is to use imp.load_source on our cached python file. imp, if you're not familiar with it, is a super useful built-in module which provides access to most of the internals of python's import process). Actually using the code is the cool part. All you need to do is to register the finder with sys.path_hooks and then add the web server with your modules on in to your path:   
  

    
    
      
    sys.path_hooks.append(WebFinder)  
    sys.path.append("http://www.inference.phy.cam.ac.uk/mackay/python/compression/huffman")  
      
    # with the url on the path, just use import  
    import Example  
    print Example.__path__  
    #['http://www.inference.phy.cam.ac.uk/mackay/python/compression/huffman/Example.py']  
      
    # the module's __path__ will point at the url, but __file__ points at the cached  
    # file on disk  
    

  
This isn't really something I'd be comfortable using in production without more work.  There's no security and no authentication, so not only is your code up on the web for anybody to see, you're also executing code off the web with no idea what it will do. It would be OK for an intranet if you were pretty sure none of your coworkers fancies him/herself a master prankster, but I'd slather on the security before trying this over long distances!  
  
Another obvious improvement would be to figure out a how to diff the local version of the file against the version on the http server without actually downloading the whole thing; that would be simple if the server could be asked for the CRC directly, but it would mean a tighter coupling between the finder and the server (which might be a good thing, security wise).  Another improvement might be to hack the loader so it force reloaded the module if the server version had changed, although that could have unintended side effects if the --   
 The point, however -- assuming there is one --  is how freaking awesome python's infrastructure is. Live loading of code over the net, transparent to all your other code, in about 50 lines?  Hat's off to Guido.   


[![](http://www.wired.com/wp-content/uploads/blogs/wiredenterprise/wp-content/uploads/2012/06/beard-programmers-final-two.png)](http://www.wired.com/wp-content/uploads/blogs/wiredenterprise/wp-content/uploads/2012/06/beard-programmers-final-two.png)

