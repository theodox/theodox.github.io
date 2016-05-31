Title: First module of the year!
Date: 2016-01-13 23:35:00.000
Category: blog
Tags: maya, python, shaders, techart
Slug: sfx_module
Authors: Steve Theodore
Summary: Introducing SFX -- a python module for scripting Maya shaderFX shaders.

It's been a busy few months at work, and the blogging has been pretty light. But I promised some folks on the Tech-Artists.org slack that I'd share some code for dealing with Mays's ShaderFX system: a very useful toolkit but not the best documented or automatable part of Maya. Since it's New Years' Resolution time, I thought I'd kill two birds with one stone and put up some notes to go with the code  

All of shaderfx in maya is organized by a single, undocumented command. Which is pretty lame.   

However, it’s not as bad as it seems once you figure out the standard command form, which is always some variant of this form:  

        shaderfx -sfxnode <shader node> -command <command> <node id>  
    

The `sfxnode` argument tells maya which sfx shader to work on. The `command` flag indiciates an action and the `node id` specifies an node in the network. Nodes are assigned an id in order of creation, with the firstnode after the root ordinarily being number 2 and so on – however the ids are not recycled so a network which has been edited extensively can have what look like random ids and there is no guarantee that the nodes will form a neat, continuous order.   
Many commands take additional arguments as well. Those extra always follow the main command; thus   

    
        shaderfx -n "StingrayPBS1" -edit_int 19 "uiorder" 1;  
    

sets the value of the `uiorder` field on node 19 to a value of 1.   
The `shaderfx` command can also return a value: to query the `uiorder` field in the example above you’d issue   
  
    
    
        shaderfx -n "StingrayPBS1" -getPropertyValue 19 "uiorder";  
        // Result: 1 //   
    

  
So, the good news is that the `shaderfx` command is actually pretty capable: so far, at least, I have not found anything I really needed to do that the command did not support. For some reason the help documentation on the mel command is pretty sparse but the python version of the help text is actually quite verbose and useful.  
Still, it’s kind of a wonky API: a single command for everything, and no way to really reason over a network as a whole. Worse, the different types of nodes are identified only by cryptic (and undocumented) numeric codes: for example a `Cosine` node is 20205 – but the only way to find that out is to use the `getNodeTypeByClassName` command (and, by the way, the node type names are case and space sensitive).  


##Cleanup crew

With all that baggage I was pretty discouraged about actually getting any work done using shaderfx programmatically. However a little poking around produced what I hope is a somewhat more logical API, which I’m [sharing on github](https://github.com/theodox/sfx).  
The `sfx` module is a plain python module - you can drop it into whatever location you use to story your Maya python scripts. It exposes two main classes:  
**`SFXNetwork`** represents a single shader network – it is a wrapper around the Maya shader ball. The `SFXNetwork` contains an indexed list of all the nodes in the network and also exposes methods for adding, deleting, finding and connecting the nodes in the network.  
**`SFXNode`** represets a single node inside the network. It exposes the properties of the node so they can be accessed and edited using python dot-style syntax. 

The module also includes to submodules, `sfxnodes` and `pbsnodes`. These make it easier to work with the zillions of custom node ids: Instead of remembering that a `Cosine` node is type 20205, you reference `sfxnodes.Cosine`. I’ll be using the `StingrayPBSNetwork` class and the `pbsnodes` submodule in my examples, since most of my actual use-case involves the Stingray PBS shader. The syntax and usage, however, are the same for the vanilla `SFXNetwork` and `sfxnodes` – only the array of node types and their properties.  
Here’s a bit of the basic network functionality.   


###Create a network

To create a new shaderfx network, use the `create()` classmethod:  
    
    :::python  
    from sfx import StingrayPBSNetwork  
    import sfx.pbsnodes as pbsnodes  
      
    network = StingrayPBSNetwork.create('new_shader')  
    

That creates a new shaderball (note that it won’t be connected to a shadingEngine by default – that’s up to you).  


### Listing nodes

An SFXNetwork contains a dictionary of id and nodes in the field `nodes`. This represents all of the graph nodes in the network. _Note I’ve used a different shader than the default one in this example to make things easier to read._  
    
    :::python
    print network.nodes  
    # { 1 : <sfxNode UnlitBase (1)>, 2: <sfxNode 'MaterialVariable' (2)> }  
      
    print network.nodes[2]:  
    # <sfxNode 'MaterialVariable' (2)>  
    

The keys of the dictionary are the node ids. As already noted, these are not guaranteed to be in a continuous order depending on what you do to the network - however they are stable and they will always match the id numbers shown in the shaderfx ui when you activate the `show node IDs` toggle in the ShaderFX window.  

The values of the node dictionary are `SFXNode` objects.  


###Adding new nodes

To add a node to the network use its `add()` method and pass a class from either the `sfxnodes` or `pbsnodes` submodule to indicate the type.   

    
    :::python
    if_node = network.add(pbsnodes.If)  
    # creates an If node and adds it to the network  
      
    var_node = network.add(pbsnodes.MaterialVariable)  
    # creates a MaterialVariable node and adds it to the network  
    

###Connecting nodes

Connecting nodes in shaderfx requires specifying the source node the source plug, the target node and the target plug. Unforunately the plugs are indentifited by zero-based index numbers: the only way to know them by default is to count the slots in the actual shaderfx UI. Output plugs are usually (not always) going to be index zero but the target plugs can be all over the map.  
To make this cleaner, each `SFXNode` object exposes two fields called `inputs` and `outputs`, which have named members for the available plugs. So to connect the ‘result’ output of the `var_node` object to the input named ‘B’ on the `if_node`:  

    
    :::python
    network.connect(var_node.outputs.result, if_node.inputs.b)  
    

If the connection can’t be made for some reason, a `MayaCommandError` will be raised.  

In any shader system it's common to have to ‘swizzle’ the connections: to connect the x and z channels of a 3-pronged output to channels of an input, for example. Mismatched swizzles are a common cause of those `MayaCommandErrors`. You can set the swizzle along with the connection by passing the swizzle you need as a string  

    
    :::python
    network.connect(var_node.outputs.result, if_node.inputs.b, 'z')  
    # connects the 'x' output of var_node  to the b channel of the input  
    

###Setting node properties

Nodes often have editable properties. There are a lot of different ones so it is often necessary to inspect a node and find out what properties it has and what type of values those properties accept. Every `SFXNode` object has a read-only member `properties`, which is a dictionary of names and property types. Thus:


    :::python
    print node.properties  
    # { 'min': 'float', 'max': 'float', 'method': 'stringlist' }  

If you know that a property exists on an object you can query it or set it using typical python dot syntax:  

    
    
    :::python
    node = network.properties[5]   
    # get the node at index 5 in this network  
      
    print node.properties:  
    # { 'min': 'float', 'max': 'float', 'method': 'stringlist' }  
      
    print node.min  
    # 1.0  
    # getting a named property returns its value.  
      
    node.min = 2.0  
    # sets the node value  
      
    print node.min  
    # 2.0  
    

If you try to access a property that doesnt exist, an error will be raised:  

    :::python    
    print node.i_dont_exist  
    # AttributeError: no attribute named i_dont_exist  
      
    node.i_dont_exist = 99  
    # MayaCommandError  
    

##Help wanted!

So, there’s the basics. This module is pretty simple but I’ve found it _extremely_ helpful in workign with SFX nodes. It will be much easier to work with, of course, if you already know your way around ShaderFX. Please let me know how it works for you – and as always bug reports and pull requests are very welcome! 

