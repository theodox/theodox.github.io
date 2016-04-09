Title: To Scale!
Date: 2015-01-04 22:08:00.004
Category: blog
Tags: , , 
Slug: To-Scale!
Authors: Steve Theodore
Summary: pending

In our [last visit to 3-d math land](http://techartsurvival.blogspot.com/2014/12/adventures-in-4th-dimension.html), we moved from the 2x2 and 3x3 matrices we used to learn how matrices function to the full 4x4 matrix that we all know and love to hate from 3d applications. This time I’d like to add support for scaling to our matrices so we can round out the ways matrices work.   
  
  


> This might be a good time to back and breeze throught the [last installment in our math series](http://techartsurvival.blogspot.com/2014/12/adventures-in-4th-dimension.html) if you’re a little fuzzy on how 4X4 matrices work, or just rusty after the holidays.

The 4x4 matrix encodes both rotations and scales very elegantly. If that matrix represented a transfrom, the first three rows of the matrix would be correspond to the local coordinates of the transform, while the fourth row is the 3-D point where the origin of the transform sits (if you’re wondering where things like the pivot offset or maya’s joint orient come from, those are actually a series of matrices that are multiplied together: the [maya docs](http://download.autodesk.com/us/maya/2009help/CommandsPython/xform.html) go into much more detail.).  
Of course, we all know that transforms can also be scaled up or down. So what does that look like in matrix form?  
Here’s our old friend the identity matrix:  
1| 0| 0| 0  
---|---|---|---  
0| 1| 0| 0  
0| 0| 1| 0  
0| 0| 0| 1  
  
and a sample point:  
1| 1| 1| 1  
---|---|---|---  
  
> If you're wondering why we need 4 points instead of three, you might want to check back after reviewing the last article in the series. 

We want to figure out what to do to this matrix so that it returns points and vectors scaled: we’d like to turn our `[1,1,1]` into `[2,2,2]`  
The natural first guess is just to scale up the whole thing by 2: in other words, we could try just changing the 1’s in our matrix to 2’s:  
2| 0| 0| 0  
---|---|---|---  
0| 2| 0| 0  
0| 0| 2| 0  
0| 0| 0| 2  
  
Easy - but let's do the math just to be sure:  
  

    
    
    [1,1,1,1] dot [2,0,0,0] = 2  
    [1,1,1,1] dot [0,2,0,0] = 2  
    [1,1,1,1] dot [0,0,2,0] = 2  
    [1,1,1,1] dot [0,0,0,2] = 2  
    

  
This looks right at first, but there’s a problem. If you cast your mind back to the [brain bending vortex](http://techartsurvival.blogspot.com/2014/12/adventures-in-4th-dimension.html) of [homogeneous coordinates](http://deltaorange.com/2012/03/08/the-truth-behind-homogenous-coordinates/), you’ll remember that the point `[2,2,2,2]` is actually quite different from `[2,2,2,1]`: in fact, it’s the same as [1,1,1,1] , since homogenous coordinates are divided by their last (W) coordinate when turned into plain old 3-D points. So, the naive approach turns out to be wrong: _we can’t just scale up every number in the matrix_!  
The culprit is that very last 2: it’s scaling up the W of the output -- which is equivalent to scaling the actual 3-D point **down**. Scaling that last W component is _negating _all of the other scales.  
  
Of course, that suggests that if we just reset that last row, we'll get the result we expected:  
  
2| 0| 0| 0  
0| 2| 0| 0  
0| 0| 2| 0  
0| 0| 0| 1  
  
  

    
    
    [1,1,1,1] dot [2,0,0,0] = 2  
    [1,1,1,1] dot [0,2,0,0] = 2  
    [1,1,1,1] dot [0,0,2,0] = 2  
    [1,1,1,1] dot [0,0,0,1] = 1  
    

  
If you take off your math hat momentarily, and resume your usual TA hat for a moment, you can we have to treat that last row differently from the others. Scaling a transform node up or down may move the children, but the origin of the transform isn’t changing. Scaling doesn’t need to touch that last matrix row, any more than the rotation does.  
  
 This is consistent with what we discovered last time while deriving the translation matrix: that last row is a slightly different beast than the others and gets handled separately. The upshot is quite simple: **scale information in your matrix is encoded only in the upper left-hand 3x3 subsection.** It doesn’t affect the last row in any way.  


## [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#uniformity)Uniformity

So, we know know how to apply a uniform scale to a matrix. If you keep that Max/Maya transform node in mind for just another moment, you can probably get a good intuition about what non-uniform scales will look like in matrix form. We know that applying a non-uniform scale to enlarges everything along the local axes of the node; we also know that the first three rows of our matrix correspond to the local axes of a transform. This suggests that we should be able to apply non-uniform scales by simply scaling those rows differently.  
Here’s a matrix that scales up by 2 in the X axis, by 3 in Y, and by 4 in Z:  
  
2| 0| 0| 0  
0| 3| 0| 0  
0| 0| 4| 0  
0| 0| 0| 1  
  
And as you can see it scales our point as we'd like:   

    
    
    [1,1,1,1] dot [2,0,0,0] = 2  
    [1,1,1,1] dot [0,2,0,0] = 3  
    [1,1,1,1] dot [0,0,2,0] = 4  
    [1,1,1,1] dot [0,0,0,1] = 1  
    

  


## Scale and rotation 

It’s probably a good idea to try this with a more complex matrix as well, just to prove out what happens when the matrix isn’t neatly lined up with the world. Here’s a matrix that rotates 45 degrees in X and 30 in Z   
.866| .5| 0| 0  
---|---|---|---  
-.353| .612| .707| 0  
.353| -.612| .707| 0  
0| 0| 0| 1  
  


> You can check back to our discussion of [rotation matrices](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html) to see the pattern behind those numbers

Our test point becomes   
  

    
    
    [1,1,1,1] dot [.866,-.353,.353,0] = .866  
    [1,1,1,1] dot [.5, .612,-.612, 0] = .5  
    [1,1,1,1] dot [0,.707,.707,0] = 1.414  
    [1,1,1,1] dot [0,0,0,1] = 1  
    

  
or `[.866, .5, .1.414]` (I’ve done a little rounding for readability).  To make this a little less abstract, heres' a unit cube in Maya with that matrix applied:  
  


[![](http://4.bp.blogspot.com/-3MHZFxXQeMY/VKohUK39ItI/AAAAAAABLgQ/VSQCT-mKkns/s1600/45_30.png)](http://4.bp.blogspot.com/-3MHZFxXQeMY/VKohUK39ItI/AAAAAAABLgQ/VSQCT-mKkns/s1600/45_30.png)

  
Since those first three rows represent the local axes of our transform, we have to multiply the whole row in order to apply a local scale. If we wanted to scale this matrix up by 2 along it’s local X, we’d get  
  
1.732| 1| 0| 0  
-.353| .612| .707| 0  
.353| -.612| .707| 0  
0| 0| 0| 1  
  
(note how both .866 and .5 are doubled). Our new dots become:  
  

    
    
    [1,1,1,1] dot [1.732,-.353,.353,0] = 1.732  
    [1,1,1,1] dot [1, .612,-.612, 0] = 1  
    [1,1,1,1] dot [0, .707, .707, 0] = 1.414  
    [1,1,1,1] dot [0,0,0,1] = 1  
    

  
You can see how the X and Y dimensions have both scaled up, since the original X axis is pointing partially into world X and world Y. Here’s the same transformation in Maya for comparison - you can see that the orientation is preserved but the unit cube is scaled double along it's local X axis.  
  


[![](http://1.bp.blogspot.com/-xQrr4BXBAI0/VKolH8cyJcI/AAAAAAABLgY/TDc1GUziqRo/s1600/scaled_and_rotated.png)](http://1.bp.blogspot.com/-xQrr4BXBAI0/VKolH8cyJcI/AAAAAAABLgY/TDc1GUziqRo/s1600/scaled_and_rotated.png)

  
  
This demonstrates how you apply non-uniform scales: by scaling the contents of your X, Y or Z rows of your matrix.  You'll notice that we had to scale the entire row to get the correct results.   
  
One important side-effect of this strategy is that not all of your row vectors will be normalized: if the matrix is scaled the vectors will have unpredictable lengths.  If you are using the matrix rows as vectors (for example, in a look-at equation) you'll have to remember to re-normalized them or you'll get wonky results.   
  
On the other hand, the length of your row vectors actually encodes the local scales of your matrix. The local X scale of your matrix is the length of the first row, the local Y is the length of the second, and the local Z scale is the length of the third row.  
  
In the examples above you can see that the rows of our (2,3,4) scale matrix are 2, 3 and 4 respectively  This is also true for the last example, despite the rotations. In case you’ve forgotten the formula, the length of a vector is the [square root of the sum of it’s squared contents](http://www.netcomuk.co.uk/~jenolive/vect5.html), or in more readable form:  
  

    
    
    def vector_length(v):  
       square_length = [i * i for i in v]  
       return math.sqrt(sum(square_length))  
    

> As you can see the vector length formula works for any length vector: Just add up the squares and take the square roots! A useful trick for many applications, though is not to bother getting square roots unless you need them: for example, if you want to sort vectors by length, you can just collect the sum of the component squares without getting the roots: the ordering is the same, but you don't have to do a bunch of expensive square roots since you only care about relative lenghts, not absolutes.

With that in mind, the lenght of the X row of our tilted-and-scaled matrix is   
  

    
    
    sqrt ( 1.732**2 + 1**2 + 0**2 )  
    

  
in other words 2, as expected (with allowance for my rounding, anyway).  This is a particularly neat trick -- as always, working through my stuff has left me in awe of the geniuses who devised this system! -- because the scales are embedded in the matrix and easily recovered even though they don't show up as single numbers.  
  
Pretty slick, huh?  But it also explains why you frequently get objects in Max and Maya reporting themselves with scale values that seem off, like 3.99999997 or the like:  that's floating point error accumulating in the calculation of the length of those row vectors.   


# Next up

Scaling, it turns out, is quite pleasantly simple after the mad 4-D adventures involved in adding translation. It remains happily parked in the upper-left-hand corner of the matrix, doing its thing in a predictable way.  
  
Next time out we’ll take a look at shears - a way to skew a matrix which usually happens by accident but which is sometimes useful to know about. In the meantime, Happy New Year and keep on dotting!  
  


###  Posts in this series

  * [Bagels and Coffee (intro to dot products)](http://techartsurvival.blogspot.com/2014/11/bagels-and-coffee-or-vector-dot-product.html)
  * [Dots All Folks (dot product uses)](http://techartsurvival.blogspot.com/2014/11/dots-all-folks.html)
  * [Dot Matrix (intro to matrices)](http://techartsurvival.blogspot.com/2014/12/dot-matrix.html)
  * [Adventures in the 4th Dimension (translation matrices)](http://techartsurvival.blogspot.com/2014/12/adventures-in-4th-dimension.html)
  * [To Scale! (scale matrices)](http://techartsurvival.blogspot.com/2015/01/to-scale.html)



