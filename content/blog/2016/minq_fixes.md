Title: Moar Minq!
Date: 2016-10-16
Category: blog
Tags: maya, python, minq
Slug: minq_fixes
Authors: Steve Theodore
Summary: Some updates and improvements for [minq](https://github.com/theodox/minq/blob/master/readme.MD)
header_cover: http://media.jrn.com/images/mink-mink-2-of-hoffman.jpg

After the recent updates to [mGui](/2016/mgui2_live), I've just pushed a few changes to [minq](https://github.com/theodox/minq/blob/master/readme.MD).  After a couple of months away I solved a couple of nagging issues with that had me stumped earlier.  
>Oh man, after a month of C++ it feels so nice to do somey Python, even if it's just playing hooky...

Fabulous Fancy Filters
======================

The big change is to the way you do attribute filters.  In the first release, you had to choose between a nice clean way of writing an attribute filter and a limited set of features.  The `where()` operator on a query let you pass in a filter function , so you could -- for example -- find all the transforms above the zero line like this:

```python
    upper = Transforms().where(lambda p: cmds.getAttr(p + '.ty') > 0)
```

Under the hood that would look more or less like:

```python
	for each_node in cmds.ls(type='transform')
		if cmds.getAttr(each_node + ".ty") > 50:
			yield each_node
```

Which works fine. However for a big list it involves a potentially large number of independent `getAttr` calls, which aren't too fast.  So we also added the option to format a special bulk query that would issue the same `getAttr` on all of the items in your query at once, for a big speed boost. Those accelerated queries looked like this:

```python
   upper = Transforms().where(item.ty > 50)
```

This exploits an interesting behavior in Maya: if you select a whole bunch of items at once and do a `getAttr` from the listener you'll get a whole list of answers, not just one -- and the cost of the query is correspondingly lower.  Unfortunately, it doesn't work for _custom_ attributes: it only works for Maya's built-in attributes.

So in the old version of minq you had to choose between a clean, fast bulk query or a wordy, slower but more flexible version using a lambda.  To de-couple the style from the speed, I've added two new variants on the query syntax:  `native` will generate a fast bulk attribute query for built-in attributes, and `custom` uses the same syntax but uses the slower-but-flexible approach instead. Thus

```python
    upper  = Transforms().where(native.ty > 50)  # a fast bulk query
    customized = Shapes().where(custom.example == 1)  # a slower general query
```

There's also an option for tweaking the custom queries so they will or will not raise exceptions if the custom attribute isn't found.  The default behavior for missing attributes is simply not to pass the filter, but in some situations you may want to know for sure if your stream has items that are missing the attributes you expect.

Proud, Pleasing Positions
=========================

Another longstanding gripe that is partially cleaned up in this pass is bulk queries for object positions.  It's always been easy to get _local_ positions with a simple query like

```python
    Selected().get(Transforms).get(AttribValues, "translate")
```
However there was no easy way to get _world_ positions. This release adds the `WorldPositions` and `LocalPositions` classes which will return the positions:

```python
    camera_positions = Cameras().get(WorldPositions)
```

Under the hood these are extracted from the `matrix` and `worldMatrix` attributes so they work as speedy bulk queries.  The main limitation is that the results will always come back in native Maya units (ie, in centimeters) so you may need to transform them if you're working in another unit.  Should you need to do that, here's a handy hack using `api.OpenMaya.MVector`:

```python
	in_meters = lambda p: MVector(p) / 100
	Selected().get(Parents).get(WorldPositions).foreach(in_meters)
```

Along with `LocalPositions` and `WorldPositions`, access to the matrices also made it easy to add a `LocalAxis` query. This will return the local X, Y or Z axis of a transform in either world or local space:

```python
    forwards = Meshes().get(Parents).get(LocalAxis, 'x') 
```

By default the axis vectors will be returned in world space, but you can get local space instead:

```python
    lcl_forwards = Meshes().get(Parents).get(LocalAxis, 'x', local=True)
```

These vectors are extracted directly from the matrices, so you may need to renormalize them depending on what you want them for. 

Dauntless Documentation
=======================

While we're on the subject, I've cleaned up the [minq wiki](https://github.com/theodox/minq/wiki).  After a long month of slogging through the Unreal Engine codebase in search of what-the-heck-is-going-on-here?, I've tried to atone for my past sins in terms of under-documenting.  Please give me a shout out or update the wiki yourself if you see something wrong or unclear on the docs!






