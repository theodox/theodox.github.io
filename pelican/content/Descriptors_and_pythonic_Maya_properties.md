Title: Descriptors and pythonic Maya properties
Date: 2014-03-11 15:15:00.000
Category: blog
Tags: maya, python, gui, techart
Slug: descriptors_and_pythonic_maya_properties
Authors: Steve Theodore
Summary: How to use descriptors for dot-style access to maya object properties instead of `cmds.getAttr()`

I'm still working on the followup to [Rescuing Maya GUI From Itself](rescuing_maya_gui_from_itself.html), but while I was at it this [StackOverflow question](http://stackoverflow.com/questions/22291337/python-re-implementing-setattr-with-super) made me realize that the same trick works for pyMel-style property access to things like position or rotation. If you're a member of the anti-pyMel brigade you might find this a useful trick for things like `pCube1.translation = (0,10,0)`. Personally I use pyMel most of the time, but this is a good supplement or alternative for haterz or for special circumstance where pymel is too heavy. 

The goal is to be able to write something like
    
    :::python
    from xform import Xform  
    example = Xform('pCube1')  
    print example.translation  
    # [0,0,0]  
    example.rotation = (0,40, 0)  
    

The process is about as simple as it can get thanks to the magic of [descriptors](rescuing_maya_gui_from_itself.html). This example spotlights one advantage of descriptors over getter/setter property functions: by inheriting the two classes (`BBoxProperty` and `WorldXformProperty`) I can get 4 distinct behaviors (world and local, read-write and read-only) with very little code and no if-checks.
    
    :::python
    '''  
    xform.py  
      
    Exposes the xform class: a simple way to set maya position, rotation and similar properties with point notation.  
      
    (c) 2014 Steve Theodore.  Distributed under the MIT License (http://opensource.org/licenses/MIT)  
    TLDR: Use, change and share, please retain this copyright notice.  
    '''  
      
    import maya.cmds as cmds  
      
    class XformProperty( object ):  
        CMD = cmds.xform  
        '''  
        Descriptor that allows for get-set access of transform properties  
        '''  
        def __init__( self, flag ):  
            self.Flag = flag  
            self._q_args = {'q':True, flag:True}  
            self._e_args = {flag: 0}  
      
      
        def __get__( self, obj, objtype ):  
            return self.CMD( obj, **self._q_args )  
      
        def __set__( self, obj, value ):  
            self._e_args[self.Flag] = value  
            self.CMD( obj, **self._e_args )  
      
      
    class WorldXformProperty( XformProperty ):  
        '''  
        Get-set property in world space  
        '''  
        def __init__( self, flag ):  
            self.Flag = flag  
            self._q_args = {'q':True, flag:True, 'ws':True}  
            self._e_args = {flag: 0, 'ws':True}  
      
    class BBoxProperty ( XformProperty ):  
        '''  
        Read only property for bounding boxes  
        '''  
        def __set__( self, obj, value ):  
            raise RuntimeError ( "bounding box is a read-only property!" )  
      
    class WorldBBoxProperty ( WorldXformProperty, BBoxProperty ):  
        '''  
        Read only property for bounding boxes  
        '''  
        pass  
      
      
    class Xform( object ):  
        '''  
        Thin wrapper providing point-notation access to transform attributes  
      
           example = Xform('pCube1')  
           # |pCube1  
           example.translation   
           # [0,0,0]  
           example.translation = [0,10,0]  
      
        For most purposes Xforms are just Maya unicode object names.  Note this does  
        NOT track name changes automatically. You can, however, use 'rename':  
           example = Xform('pCube1')  
           example.rename('fred')  
           print example.Object  
           # |fred  
      
        '''  
      
        def __init__( self, obj ):  
            self.Object = cmds.ls( obj, l=True )[0]  
      
        def __repr__( self ):  
            return unicode( self.Object )  # so that the command will work on the string name of the object  
      
        # property descriptors  These are descriptors so they live at the class level,  
        # not inside __init__!  
      
        translation = XformProperty( 'translation' )  
        rotation = XformProperty( 'rotation' )  
        scale = XformProperty( 'scale' )  
        pivots = XformProperty( 'pivots' )  
      
        world_translation = WorldXformProperty( 'translation' )  
        world_rotation = WorldXformProperty( 'rotation' )  
        world_pivots = WorldXformProperty( 'pivots' )  
        # maya does not allow 'world scale' - it's dependent on the parent scale  
      
        # always local  
        scaleTranslation = XformProperty( 'scaleTranslation' )  
        rotateTranslation = XformProperty( 'rotateTranslation' )  
      
        boundingBox = BBoxProperty( 'boundingBox' )  
        world_boundingBox = WorldBBoxProperty( 'boundingBox' )  
      
      
        def rename( self, new_name ):  
            self.Object = cmds.ls( cmds.rename( self.Object, new_name ), l=True )[0]  
      
        @classmethod  
        def ls( cls, *args, **kwargs ):  
            '''  
            Returns a list of Xforms, using the same arguments and flags as the default ls command  
            '''  
            try:  
                nodes = cmds.ls( *cmds.ls( *args, **kwargs ), type='transform' )  
                return map ( Xform, nodes )  
            except:  
                return []  
    

You may note the absence of a `__metaclass__`. In this case, with only a single class, a meta would be an unnecessary complication. Meanwhile the [code for MayaGUI itself is up on GitHub](https://github.com/theodox/mGui). Comments and/or contributions welcome!

