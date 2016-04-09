Title: Adventures in the 4th dimension
Date: 2014-12-15 23:35:00.000
Category: blog
Tags: , , 
Slug: Adventures-in-the-4th-dimension
Authors: Steve Theodore
Summary: pending

In [our last discussion of 3d math](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html), we started to plumb the mysteries of the matrix. Along the way we discovered two important facts: First, that it’s possible to write an article about matrices with only the merest smidge of a Keanu Reeves mention and second (almost as important), that **matrices are just a convention for applying dot products in series.** We walked through the derivation of matrices for a series of dot products and shows how hat simple operation allows you to do rotations in two and three dimensions.  
  
Naturally, any TA reading this will be knows there's more. We all know that the matrices we’re most familiar with — the transform matrices that drive animation and modeling — do more than rotate. So this this time out we’re going talk about how **translation** — spatial offsets — can be packed into matrices.  And we're going to do it in a truly brain bending way.  Sort of.  


> _If none of this sounds familiar, you may want to return to the [previous post in the series](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html) before continuing._

  
After all of the time we’ve spent with dot products in this series, one thing we should remember is that dots are **additive** — if you dot two vectors, you sum up all of the products. “Additive” is a nice quality to have if we’re thinking about adding translations to our matrices  It suggests that maybe we can use the additive-ness of dot products to teach our matrices how to do translations as well as rotations.  
  
Multiplying a vector against a matrix, [you’ll recall](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html), is nothing more than stringing together a set of dot products between the vector and the columns of the matrix. So, putting together the fact that dots are additive and the fact that matrix multiplication uses dots, it seems logical that we can just stick our translation right onto the bottom of the matrix.  By dropping it down at the end of the matrix columns, we'll add it add it to our results. One important side effect that we’ll have to worry about is that this will break the pretty symmetry we noted last time whereby every matrix row is an axis in the matrix's local coordinate system.  However we’ll deal with that after we know it works.  
  
To keep things simple, let’s start with a rotate matrix that doesn’t do any, you know, _rotating_ — a matrix that works but leaves incoming data unchanged. That'll make it easier to see when our translations kick in. The correct math moniker for this do-nothing matrix is an _identity_ matrix (as in the otherwise-inexplicable _MakeIdentity_ command in Maya) and it’s just a set of rows that match the default XYZ axes:  
  
1| 0| 0  
---|---|---  
0| 1| 0  
0| 0| 1  
  
I won’t bother with the math here, but if your work it out for yourself you’ll quickly see that dotting the columns of this matrix in turn against any vector returns the original vector unchanged.   
  
Next, we’d like to add some extra information to this matrix to include a translation. Since we know our dots are going down the columns, if we tack on an extra row we should be getting a new value added to the output: hopefully, the translation we want. Adding an extra row for translation gives us a 4X3 matrix like this (with an example translation of `[1,2,3]` :  
1| 0| 0  
---|---|---  
0| 1| 0  
0| 0| 1  
1| 2| 3  
  


> _For future reference, matrices are usually described as ‘rows by columns’; in the last article we derived our matrix first as a 2X2 then as a 3X3 matrx. Most transformation matrices in 3d software are 4X4, for reasons that will become apparent shortly, but Max users will find this 4X3 format familiar — Maxscript makes extensive use of 4x3 matrices for object transforms._

So now we’ve got a test matrix that should offset our initial value by  `[1,2,3]`. However, we immediately run into a problem: as we try to multiply our vector against this matrix. The columns now have 4 items but our vector only has 3. How can we sum up? Dot products require that both vectors being dotted have the same number of products, as you can see here:  
  

    
    
    [1,1,1] dot [1,0,0,1] = (1 * 1) + (1 * 0) + (1 * 0) + (??? * 1)   
    

  
To make this work, we are going to need to extend our vector to grab the translation values from the new matrix row. It needs to become a 4-dimensional vector. _The fourth dimension! Trippy! Cue [theremin music](https://www.youtube.com/watch?v=4wQsWL-lMJw)...._  
We've actually dimension jumped before, while working through rotation matrices. We could borrow the same tactic we used in the last post when we moved from a 2-D matrix to a 3-D matrix by just taking on a zero to our vector. This seems like a natural idea, since we know that the 2-D vector `[X,Y]` is equivalent to the 3-D vector `[X,Y,0]`. So let’s see what happens if we do the dot products:  
  

    
    
    [1,1,1,0] dot [1,0,0,1] = (1 * 1) + (1 * 0) + (1 * 0) + (0 * 1) = 1  
    [1,1,1,0] dot [0,1,0,2] = (1 * 0) + (1 * 1) + (1 * 0) + (0 * 2) = 1  
    [1,1,1,0] dot [0,0,1,3] = (1 * 0) + (1 * 0) + (1 * 1) + (0 * 3) = 1  
    

  
Not what we were hoping for: our result is still  `[1,1,1]`. What happened?  
  
The extra zero has allowed us to __do __the dot product — but it's  also zeroing out the translation we are trying to add. Evidently zero is not what we want here (this is not just an misstep, though: we'll come back to those zeroes later).   
For now, the fix is pretty obvious, even though it’s much less obvious how to what the fix is supposed to mean. If we turn that final zero into a one, we’ll get our translation added to the original value:  
  

    
    
    1,1,1,1 dot 1,0,0,1 = (1 * 1) + (1 * 0) + (1 * 0) + (1 * 1) = 2  
    1,1,1,1 dot 0,1,0,2 = (1 * 0) + (1 * 1) + (1 * 0) + (1 * 2) = 3  
    1,1,1,1 dot 0,0,1,3 = (1 * 0) + (1 * 0) + (1 * 1) + (1 * 3) = 4  
    

  
There, at last, is the translation we are looking for; our vector `[1,1,1,1]`has become `[2,3,4]`, reflecting the offset in the last row of the matrix.  
  
Well, it’s nice to get the right result, but this still leaves us with a bit of a conundrum.  I know what [2,3,4] means. But what the heck is that last coordinate doing there? Did we just make it up?  


# X,Y,Z,WTH?

You may remember from our [original discussion of dot products](http://techartsurvival.blogspot.com/2014/11/bagels-and-coffee-or-vector-dot-product.html) that _vector_ is actually a very general term, encompassing any bundle of numbers. In tech art we’re used to thinking of vectors as XYZ bundles in 3-D space, but a vector can just as easily be something else — such as your weekly Starbucks expenditure, which is how we started down this road in the first place. 3-D points can be represented by vectors — but so could any bundle of 3 numbers which formed part of a linear equation; say, the value of the dollar, the euro and the yen on a given day. Dot products and matrices work the same way regardless of the subject matter. So, one thing we know already is that all 3-D points are vectors, so to speak, but _not _all vectors are 3-D.  
[![](http://micro.magnet.fsu.edu/optics/timeline/people/antiqueimages/euclid.jpg)](http://micro.magnet.fsu.edu/optics/timeline/people/antiqueimages/euclid.jpg)  
---  
Not only did he pioneer analytical geometry, he seems to have invented the Mall Santa look too.  
  
The vectors we use in graphics, of course are usually [Euclidean vectors](https://www.princeton.edu/~achaney/tmve/wiki100k/docs/Euclidean_vector.html): a set of 3 numbers which represent a spatial offset in the X,Y and Z spatial dimensions. The word _vector_ comes from the Latin word for _one who carries_: the vector is the spatial difference between two positions. We get misled by the fact that programming languages usually use the _algebraic_ name vector (as “bundle of numbers”) for the data type we use to hold the _geometric_ Euclidean vector. _The fact that algebraic vectors and Euclidean vectors share the same noun while meaning different things is, to put it mildly, _annoying.  _With the goofy stuff we're getting in to, I personally would be happy to skip these minor surprises._  
To understand what that weird extra number, however, we have to add in a third concept: the Euclidean **point**._ _Which is also frequently represented in code by something called "vector" but which is represents a different idea. Sigh. We will have to distinguish between two things which look similar when written down or stored as vectors in computer memory but which actually _mean _two different things. Up till now we've talked about vectors and points as if they were interchangeable, but to make the translation matrix work we need to differentiate them.  
  
The default Euclidean vector is a purely relative quantity. It represents a _**change**_ in position. That's why the vector that gets you from `[0,0,0]` to `[1,1,1]` and the vector that gets you from `[8,8,8]` to `[9,9,9]` are the same: the vector proper has no location of it's own. You can think of it as a surface normal, which tells you which way a surface is facing without telling you anything about where the surface actually _is_, or the direction of a directional light which illuminates along a direction and which doesn't actually reside anywhere in 3-D space.  
  
On the other hand a Euclidean point _is _an actual location in space. The point `[1,1,1]` is just that : the location `[1,1,1]`. it has no 'facing' or 'direction' the way a surface normal does - and it's not the same as any other 3-D point. It's an _address, _while a regular vector is an offset.  
  
That's where our fourth coordinate comes in. **Th****e fourth coordinate in our example tells us if we’re dealing with a Euclidean point or a Euclidean vector, **that is, if we are dealing with something that can be translated or not.  If the last coordinate is a **1**, the data is a **point **which can be transformed (moved, rotated and scaled). If the last coordinate is a **0**, the data is a **vector**, which can be rotated and scaled but not moved. The last number is known as the [homogeneous coordinate](http://en.wikipedia.org/wiki/Homogeneous_coordinates), although most people refer to it as the “W” component by analogy with X Y and Z.  _Although I kind of wish they had just wrapped it around back to A, or started at W, or something. XYZW? Like I said, I'd like to concentrate on the mind-warping concepts more and the annoying terminology less.  Oh well._  


# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#homegeneophobia)Homegeneophobia

  


If you’re practically minded, all you _really _need to know today is that a W of 1 is a point and a W of 0 is a direction. If you are especially literal minded, in fact, this next bit may be a bit... bizarre. You can probably skip it without missing much practical information, but try to stick it out. It will give you an appreciation of the abstract beauty the underlies matrix math.  I'm going to try to explain of the ‘meaning’ of the W coordinate but take this with a grain of salt, since this one goes a bit beyond my limited mathematical imagination.  
We've already suggested that the W component represents a 4th dimension.  While that's kind of hard to visualize, we can see the results by 'projecting' onto the XYZ space that we are used to. Got that? Just like we project a 3-D set of points onto the 2-D screen of our computers, we can project a 4-D quantity into 3 dimensions.  
Another way to think about it is that an XYZW vector is _one point along a 4-dimensional line that intersects 3-space_.  In this image, engraver/ math whiz / literal Renaissance Man [Albrecht Durer](http://www.albrecht-durer.org/) is using a perspective scrim to do his life drawing: projecting a 3-D reality on the 2-D silk screen by keeping his eye in one location and then seeing how the 3-D lady lines up with his 2-D grid.  
[![](http://relativity.net.au/gaming/java/images/DurerFrustum.png)](http://relativity.net.au/gaming/java/images/DurerFrustum.png)  
---  
A decent analogy for projecting 4-D down to 3, here a 3-D world projected  down to 2:   
  
  
In this word, each 2-D point on the scrim corresponds to a 3-D line running from Durer's eye through the plane of the scrim and beyond.  In a matrix, each 3-D point is on a similar line that runs into the fourth dimension.  While it's hard to visualize, it's mathematically consistent - which is why the mathematicians like it.  
  
How cool – or confusing – is that?    
  
The point where our mystical 4-D vector intersects our plain old 3-D space corresponds to the point where Durer's eyeline passes through the scrim.  In our case, the point is  `[X,Y,Z]` divided by `W`. One side effect of this is that there are many different 4-D points that correspond to the same 3-D point: `[1,1,1,1]`, `[2,2,2,2]` and `[-1,-1,-1,-1]` all represent the same point.  In the illustration above, you can see how each of the orange lines hits one _point _in 2-D, but that the point lies on a 3-D _line. _Going from 4-D space down to 3-D works the same way - except that the extra dimension is brain-bendingly hard to visualize.  
  
A W value of 1 represents the projection of our 4-D vector onto boring old 3-D reality, sort of like the plane of the perspective scrim in the image above.  W values less than one approach the 'eye point', while values larger than 1 extend past the scrim into the scene.  To understand how the W changes the projected value in 3-D, imagine picking a point on Durer's 2-D screen and pushing back through the screen. As the distance (the W) increases, the projected point will get closer to the center of the screen.  In fact, this is plain old 1-point perspective in action:  A W approaches infinity, any coordinate translates into the perspective vanishing point, which in this case is the center of the scrim.  
  


[![](http://www.robinurton.com/history/Renaissance/perspective.jpg)](http://www.robinurton.com/history/Renaissance/perspective.jpg)

all lines converge at W=infinity, at least according to Piero Della Francesca

  
If you’re still unable to wrap your brain around this - and I am not sure I really can, so don’t feel bad about it, you might find this YouTube from Jamie King helpful. You can relate it to the Durer image by imagining Jamie's example image is taken looking down on Durer's little perspective machine from above:  
  
_Extra points for the gratuitous Bill and Ted reference, btw._  
  
This same analogy also explains, sort of, why W=0 vectors don’t move. As W increases, the points will converge on the center of his scrim, that is, the perspective vanishing point. On the other hand as W gets smaller they move away: the effect is like a camera zooming in:  everything on the image plane moves _away_ from the vanishing point. As W reaches zero the 'zoom' is now infinite: In math, all of your 4-D points would have become _impossible to convert back to 3-D_ because you'd be dividing their XYZ positions by zero.  It's sort of the inverse of a black hole: instead of all points collapsing down into a singularity, they are instead all smeared out infinitely -- which makes them effectively the same anyway. There's no difference between `[1,1,1,0]` and `[999,999,999,0]` in position, since they are both 'located' at  `[undefined,undefined,undefined]` in 3 dimensions.  
  
Since movement has no meaning in this bizarro singularity world, translations don't do anything. But — brain bend alert —  rotations still work. Of course, we already know from our earlier experiments with W's set to zero: the dots against the first 3 rows of the 4X3 matrix haven't changed, but a W=0 input vector won't translate.  Put another way, since dot products are a way of projecting one vector on to another, projecting a any 4-D vector onto a different 4-D vector with a W of 0 will keep you right at the 'eye point' out of which all those 4-D rays are shooting, so you won't have any W-ness to project yourself out into the 3-D world.  
  
 It's simultaneously baffling and awe-inspring. Like _[Goat Simulator](http://www.goat-simulator.com/)._  
  
If you've stuck it out this far, the whole visualization actually has one imporant side benefit. It explains the _other _reason we need homogeneous coordinates: they allow us to handle perspective projections and regular geometry using the same set of rules. W coordinates that aren’t 0’s or 1’s generally crop up only when you’re working with the perspective matrix of a camera or trying to transform points from world space to screen space. However that’s a matter for another time.   
  
For now, however, I need to relax my frontal lobe.  
  


  


[![](http://www.lovingmystuff.co.uk/wp-content/uploads/2013/08/543.jpg)](http://www.lovingmystuff.co.uk/wp-content/uploads/2013/08/543.jpg)  
---  
Why did they wear those hankies on their heads, anyway?  
Turning something nice and obvious like a 3-D point into an in infinite line in a dimension where parallel lines can intersect is just the sort of thing that gives mathematicians a bad name. Thankfully we don’t really need to understand all the metaphysics: we can just rely happily on the fact that this extra abstraction lets us handle translations using the same math we use for rotations. And we should be grateful that the kind of folks who do understand the way 4-dimensional vectors are projected into our 3-D world left us the 4X4 matrix which (despite this little exercise in gimcrackery) is a remarkably elegant and handy tool for practical purposes and can still be done with junior high school math skills.  


> _Gottfried Chen’s blog also makes [an heroic attempt to explain this to mere mortals](http://deltaorange.com/2012/03/08/the-truth-behind-homogenous-coordinates). The great-grandaddy of all these discussions is Edwin Abbot’s classic novella (you read that right - it’s **fiction**) [Flatland](http://www.amazon.com/mn/search/?_encoding=UTF8&camp=1789&creative=390957&field-keywords=flatland&linkCode=ur2&tag=tecsurgui-20&url=search-alias%3Daps&linkId=AIHJQXYL5IWCSXN6)_

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#homogeneous)Homogenius!

Alright, let's get our feet back on the ground (which involves setting our Z coordinate to 0 and our W coordinate to 1).  
  
If you just skipped over the mental gymnastics above —or if you just need to be brought back down to earth — let’s remind ourselves where we are:  
We've got a nice, easy to manage system for packing spatial translations and rotations into a single operation, in the form of the 4X3 matrix. By adding a W coordinate — the ~~_mysterious_~~ homogeneous coordinate – to the end of our original vector, we have gained the ability to do translations. We've also shown how we can toggle back and forth between rotation-only vector operations and rotate-and-translate point operations by changing the W coordinate from 0 to 1.  
There is one little flaw to this nifty system, however: it’s lossy. Our 4-part vectors let us distinguish between points and pure vectors, but our 4x3 matrix is only giving us back 3 components not 4. This is fine if all we want is the points, but it’s throwing away information we might need to keep if, for example, if we wanted to multiply a point by several matrices in series.   
If we want to get a 4—way vector back from the matrix we are going to need an extra column. Luckily, we know what we want from that extra column — we just need to preserve that W value and nothing else. So how do we get there?  
We already know from [last time](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html) that the first 3 rows of our matrix are supposed to be the axes of the coordinate system which our matrix defines. By definition, an axis can’t move: it’s a direction, not a position. That suggests that it’s going turn into a vector with a W of 0 when we expand it into the next column. After all, you can’t _move_ the X axis or the Y axis: no matter how you rotate it around it is only an _axis_ if it passes through origin. The last row, on the other hand, is a _translation_: it is actually intended to enforce a change of location: In other words, it’s a _point_ with a W value of 1, rather than a vector with a W of 0.  
In other words our 4x3 matrix turns into a 4 x 4 matrix that looks like this:  
1| 0| 0| 0  
---|---|---|---  
0| 1| 0| 0  
0| 0| 1| 0  
0| 0| 0| 1  
  
The first 3 rows are the vectors defining our coordinate system and the last row is a point defining the spatial offset. Any TA should be able to visualize this as transform node — a group, a joint, a null or whatever you prefer — aligned so that it’s axes line up with the first 3 rows and it’s origin sits at the XYZ position of the fourth row.   
  
The nice bit is that, despite all the 4-dimensional mumbo-jumbo this 4X4 matrix (just like the 3X3 and 4X3 versions we’ve touched on before) is **still just a plain old set of dot products** when you clear away all the verbiage, special typography and extra dimensions. Dot your 4-D point or vector against the columns of this 4-D matrix and you’ll get back a rotated vector, just like we did when learning how matrices work. If your incoming W is set to 0, you’ll get just a rotation; if it’s set to 1, you’ll get a rotation and a translation at the same time. With plain old bagels-and-coffee math.   
Petty slick, huh?   
So, after a consciousness-expanding (and headache-inducing) journey into other dimensions, we’ve finally sort of arrived at the full 4X4 matrix that powers every graphics application under the sun. And, amazingly enough, we’ve just scratched the surface (_What is the surface of a 4-D object anyway? My brain hurts._)  
Next time out we’ll talk about how a 4x4 matrix can encode scale as well, which luckily is a little less Timothy Leary than what we’ve already gone through.  Until then here's an animated gif of a 4-dimensional cube (which in this case is a 2-D projection of the 3-D physical extrusion of the 4-D object.... piece of cake!)  
  
Me, I need a good stiff drink.  


[![](http://24.media.tumblr.com/tumblr_m3dy5zVFhq1qgnjgmo1_400.gif)](http://24.media.tumblr.com/tumblr_m3dy5zVFhq1qgnjgmo1_400.gif)

###  Posts in this series

  * [Bagels and Coffee (intro to dot products)](http://techartsurvival.blogspot.com/2014/11/bagels-and-coffee-or-vector-dot-product.html)
  * [Dots All Folks (dot product uses)](http://techartsurvival.blogspot.com/2014/11/dots-all-folks.html)
  * [Dot Matrix (intro to matrices)](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html)
  * [Adventures in the 4th Dimension (translation matrices)](http://techartsurvival.blogspot.com/2014/12/adventures-in-4th-dimension.html)
  * [To Scale! (scale matrices)](http://techartsurvival.blogspot.com/2015/01/to-scale.html)



