Title: Maya Bug Watch: API2 and GetPoints()
Date: 2015-03-27 21:20:00.001
Category: blog
Tags: , , , 
Slug: Maya-Bug-Watch:-API2-and-GetPoints()
Authors: Steve Theodore
Summary: pending

In general I’m more or less a [fan of Maya Python API
2.0](http://techartsurvival.blogspot.com/2014/12/all-we-are-saying-is-give-
api-20-chance.html). It’s more pythonic and feels faster than the old version.
However, it’s not without its quirks and I just found one that really bit me
in the behind.  
If you want to get the vertices of an object in the api, the usual formula is:  

  1. Get the dagPath of the object
  2. make an [MFnMesh](http://help.autodesk.com/view/MAYAUL/2015/ENU/?guid=__py_ref_class_open_maya_1_1_m_fn_mesh_html)
  3. call the ‘GetPoints’ method of your mesh
  4. party on.

Something like this, which returns a list of [MPoint](http://help.autodesk.com
/view/MAYAUL/2015/ENU/?guid=__py_ref_class_open_maya_1_1_m_point_html) objects
for the verts in the mesh  

    
    
    import maya.api.OpenMaya as api  
      
    def get_verts(mesh):  
        mobj = api.MGlobal.getSelectionListByName(mesh).getDagPath(0)  
        # that's lazy, it assumes that the first child is the mesh shape.  
        # in practice you need to be more careful...  
        mfn_mesh =  api.MFnMesh(mobj)  
        vert_array = mfn_mesh.getPoints()  
        return [i for i in vert_array]  
    

This works fine and dandy… except:  
_**If the mesh has 256 or more verts, the first vertex comes back as
garbage**_  
Here’s an example, using the same function:  

    
    
    mesh, _ = cmds.polyCube(sw = 1, sh= 1, sd = 1)  
    print get_verts(mesh)[:4]  
    #> [maya.api.OpenMaya.MPoint(-0.50000000000009082, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(0.5, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.5, 0.5, 0.5, 1), maya.api.OpenMaya.MPoint(0.5, 0.5, 0.5, 1)]  
      
    # this looks good... Here's the same thing for a 226 vert cube:  
    mesh, _ = cmds.polyCube(sw = 8, sh= 8, sd = 3)  
    print get_verts(mesh)[:4]  
    #> [maya.api.OpenMaya.MPoint(-0.50000000000005185, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.375, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.25, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.125, -0.5, 0.5, 1)]  
      
    # but up the vert count to 258:  
    mesh, _ = cmds.polyCube(sw = 8, sh= 8, sd = 4)  
    print get_verts(mesh)[:4]  
    #> [maya.api.OpenMaya.MPoint(5.0277956463997711e-315, 5.0313386899592279e-315, 0.5, 1), maya.api.OpenMaya.MPoint(-0.375, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.25, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.125, -0.5, 0.5, 1)]  
      
    # that first point is gibberish: python can't go to the -315th power!  
    

I’ll leave it to wiser heads to figure out _why_ it works out like this. My
guess is that something is borked in pointer math going on inside the wrapper
around `MfnMesh`, but I don’t know. Luckily, there’s a workaround: if you
create _new_ MPoints out of the items coming back from the `GetPoints()` call,
you get good data. I’m not sure why but this should be so but it appears to be
reliable on my machine (Windows 7, 64 bit maya 2015). Here’s the workaround:  

    
    
    def safe_get_verts(mesh):  
        mobj = api.MGlobal.getSelectionListByName(mesh).getDagPath(0)  
        mfn_mesh =  api.MFnMesh(mobj)  
        vert_array = mfn_mesh.getPoints()  
        return [api.MPoint(i) for i in vert_array]  # creating new MPoints fixes the issue  
      
    mesh, _ = cmds.polyCube(sw = 10, sh= 10, sd = 10)  
    print safe_get_verts(mesh)[:4]  
    #> [maya.api.OpenMaya.MPoint(-0.5, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.40000000596046448, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.30000001192092896, -0.5, 0.5, 1), maya.api.OpenMaya.MPoint(-0.20000001788139343, -0.5, 0.5, 1)]  
    


