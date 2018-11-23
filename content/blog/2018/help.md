Title: Help!
Category: blog
Tags: python, maya, programming
Slug: help
Date: 2018-05-10
Authors: Steve Theodore
Summary: Something that's always driven me crazy in Maya is the fact that `maya.cmds` does not really support Python's built-in `help()` function.  But after suffering for years on that account, it finally occurred to me today that it's fixable.

![](http://4.bp.blogspot.com/-sImC61f6sxw/Vbk7c-gxPhI/AAAAAAACqFU/28rnJSRnOuo/s1600/the-beatles-help-movie-poster_5896.jpg)

<!--jump-->

If (like I often dow) you've forgotten the countless different flags that go with a particularly involved Maya command, it's a pain to have to hop over to google just to remember the cryptic codes for the different options.  Consider a monster like, say, `file`  which has somewhere north of 50(!) flags you have to keep track of.  Most aren't complicated, but apart from the most common ones you'll never remember them all.

In MEL you can type

```
    help file;
```

from the command line, which prints a nicely formatted list of the whole shebang:

```
    Synopsis: file [flags] [String]
    Flags:
       -e -edit
       -q -query
       -a -activate                        
     -add -                                
     -amf -anyModified                     
      -ap -activeProxy                     
      -at -applyTo                          String
     -bls -buildLoadSettings               
       -c -command                          String String
      -ch -constructionHistory              on|off
     -chn -channels                         on|off
     -cmp -compress                        
     -cnl -copyNumberList                  
     -con -constraints                      on|off
      -cr -cleanReference                   String
      -de -defaultExtensions                on|off
     -dns -defaultNamespace                
      -dr -deferReference                   on|off
      -ea -exportAll                       
     -ean -exportAnim                      
     -ear -exportAnimFromReference         
     -eas -exportSelectedAnim              
      -ec -editCommand                      String
      -er -exportAsReference               
     -err -errorStatus                     
      -es -exportSelected                  
     -esa -exportSelectedAnimFromReference 
     -esn -executeScriptNodes               on|off
     -esr -exportSelectedNoReference       
     -ess -exportSelectedStrict            
     -eur -exportUnloadedReferences        
      -ex -exists                          
     -exn -expandName                      
     -exp -expressions                      on|off
     -exs -exportAsSegment                 
       -f -force                           
     -fmd -fileMetaData                    
      -fr -flushReference                   String
      -gl -groupLocator                    
      -gn -groupName                        String
      -gr -groupReference                  
       -i -import                          
     -ifr -importFrameRate                  on|off
      -ir -importReference                 
     -itr -importTimeRange                  String
      -iv -ignoreVersion                   
       -l -list                            
     -lad -loadAllDeferred                  on|off
     -lar -loadAllReferences               
     -lck -lockReference                   
     -lcu -lockContainerUnpublished         on|off
      -lf -lockFile                         on|off
     -lfo -lastFileOption                  
     -lnr -loadNoReferences                
     -loc -location                        
      -lr -loadReference                    String
     -lrd -loadReferenceDepth               String
     -lrp -loadReferencePreview             String
      -ls -loadSettings                     String
     -ltf -lastTempFile                    
      -mf -modified                         on|off
     -mnc -mergeNamespacesOnClash           on|off
     -mnp -mergeNamespaceWithParent        
     -mnr -mergeNamespaceWithRoot          
     -mns -mapPlaceHolderNamespace          String String (multi-use)
      -ms -moveSelected                    
     -new -newFile                         
      -ns -namespace                        String
       -o -open                            
      -op -options                          String
      -pm -proxyManager                     String
     -pmt -prompt                           on|off
      -pn -preserveName                    
     -pns -parentNamespace                 
     -pos -postSaveScript                   String
      -pr -preserveReferences              
     -prs -preSaveScript                    String
      -pt -proxyTag                         String
      -pu -preserveUndo                     on|off
      -pv -preview                         
       -r -reference                       
      -ra -renameAll                        on|off
     -rdi -referenceDepthInfo               UnsignedInt
     -rdn -removeDuplicateNetworks         
     -rep -replaceName                      String String (multi-use)
     -rer -resetError                      
     -rfn -referenceNode                    String (Query Arg Optional)
      -rn -rename                           String
     -rnn -returnNewNodes                  
     -rns -relativeNamespace                String
     -rpl -renamingPrefixList              
     -rpr -renamingPrefix                   String
      -rr -removeReference                 
     -rts -renameToSave                     on|off
       -s -save                            
      -sa -selectAll                       
     -sdc -saveDiskCache                    String
     -seg -segment                          String
      -sh -shader                           on|off
     -shd -sharedNodes                      String (multi-use)
     -shn -shortName                       
      -sn -sceneName                       
     -sns -swapNamespace                    String String (multi-use)
      -sr -saveReference                   
     -srf -sharedReferenceFile             
     -sru -saveReferencesUnloaded          
     -str -strict                           on|off
     -stx -saveTextures                     String
     -typ -type                             String
      -uc -uiConfiguration                  on|off
      -un -unresolvedName                  
     -uns -usingNamespaces                 
      -ur -unloadReference                  String
       -w -writable                        
     -wcn -withoutCopyNumber  
```



`maya.cmds`, alas, does not support this directly.  Python's built-in `help()` function is very handy for remembering options and syntax but it works off of docstrings, and `cmds` does not include useful ones.  If you try 

```
    help(file)
```

in the listener you get the supremely useless


```
    Help on built-in function file in module maya.cmds:
    
    file(...)
```


I've been annoyed by that one for years -- but it finally struck me today that there's an easy workaround.   A little function like this will let you hide the built-in help function in the listener so you can use the MEL help and Python `help()` interchangeably:


```
    import maya.cmds as cmds
    import maya.mel as mel
    
    if __name__ == '__main__':
        _original_help = help
        
        
        def maya_help(obj):
            if obj.__module__ == cmds.__name__:
                mel.eval( "help {}".format(obj.__name__))
            else:
                _original_help(obj)
                
        globals()['help'] = maya_help           
```


If you toss that into your `userSetup.py` or some other code that runs at startup you should be able to type things like `help (cmds.file)` and get the relevant info in your listener.

It only took a _decade_ of Maya Python for that one to occur to me.  

Doh.

    
    



