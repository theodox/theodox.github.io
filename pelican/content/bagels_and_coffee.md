Title: Bagels and Coffee, or, the vector dot product and you
Date: 2014-11-22 11:46:00.004
Category: blog
Tags: math
Slug: bagels_and_coffee
Authors: Steve Theodore
Summary: An introduction to the vector dot product, and how it's used in computer graphics.

I’ve been boning up on my math lately.   

Like most TA’s I’ve cobbled together a bag of tricks from different situations I’ve dealt with over the years, but I’ve never really gone back to shore up my shaky high school trigonometry and pre-calculus. It’s certainly possible (at least, I hope it is!) to be a good TA with only seat-of-the-pants math skills — after all, we have parenting and scaling and all the other cool tricks in our apps to do the heavy lifting for us. Still, I’ve been finding that paying more attention to the math fundamentals is helping me solve problems more efficiently and elegantly than my patented hack-and-slash techniques did.  
So, I’m starting an occasional series on some basic math concepts that I hope will be useful to other TA’s. I know it’s been helpful to me - there’s nothing that concentrates the mind like putting something out there on the internet for public commentary - it’s really forces you to think things through… _At least, as long as you’re not on Twitter_.  
  
  
To kick off the series, I want to start off with a simple operation that I use all the time, the humble [dot product](http://en.wikipedia.org/wiki/Dot_product). Also known as the 'scalar' product, the dot is an operation for turning lists of numbers into a single number. It’s also astonishingly useful for graphics. I’ve used it for years, but only recently did I try to see how and _why_ it works instead of just relying on the second-hand assurance _that_ it works.  

The dot is all about combining operations on lists. We always run into it in the context of geometric vectors, but in the pure math world vector is just another way of saying “list of similar numbers.” If you go to the coffee shop every day and buy a $5 latte, its obviously going to cost $25 a week (Tote that up over 48 work weeks a year - it's a lot of money! I bring instant. But I digress). If you buy a $2 bagel on monday and a $3 cookie on Wednesday and Friday, how much will it cost?:  

    
    
    5 * 5 = $25 for coffee  
    2 * 1 = $2 for bagel  
    3 * 2 = $6 for cookies  
    

This makes $33 total a week (you really should bring in your snacks from home. You'll save a ton!)   

Besides helping you save money on lunch, this is a classic (though non-3-d related) example of the dot product in action. Dots are nothing more than a structured way of multiplying two lists of numbers. In this case we have list of prices:  

    
    
    [5, 2, 3]  
    

and a list of quantities:  

    
    
    [5, 1, 2]  
    

The dot operation merely multiplies the numbers in the same position in the list and adds them together. As you can see, this is trivial math:  

    
    
    (5 * 5) +  (2 * 1) + (3 * 2)  
      
    

Despite it's humble origins, however, this trick -- multiplying ordered pairs of numbers and adding them up - is absolutely basic in 3-D graphics. The lists of prices and quantities become vectors (in fact, general purpose algebra calls any list a 'vector') and with a simple convention the dot product takes on a very interesting and useful set of properties for TA’s to exploit.  
The most famous example of the dot product in graphics is [the original Lambert shading equation](http://en.wikipedia.org/wiki/Lambertian_reflectance):  
    
    N dot L  
    

Where N is a surface normal and L is the angle of the incident light.   
  
  
[![](http://upload.wikimedia.org/wikipedia/commons/thumb/0/03/VisualPhotometry_Fig2_from_Lambert'sPhotometria.jpg/2880px-VisualPhotometry_Fig2_from_Lambert'sPhotometria.jpg)](http://upload.wikimedia.org/wikipedia/commons/thumb/0/03/VisualPhotometry_Fig2_from_Lambert'sPhotometria.jpg/2880px-VisualPhotometry_Fig2_from_Lambert'sPhotometria.jpg)  
  
> The 'Lambert shader' is based on this math textbook from 1760. How cool is that?  
  
Lambertian shading is probably the single most common operation in computer graphics, but it’s the same math as figuring out your coffee budget. Here’s how the magical translation from bagels and coffee to shaded pixels works:  
Imagine a sphere being lit by a directional light from straight above, in classic CG fashion. The vector to the light would be   

    
    
    [0, 0, 1]  
    

On top of the sphere, the normal vector would point the same way - it too would point up towards  

    
    
    [0, 0, 1]  
    

The dot of these two is:  

    
    
    (0 * 0) + (0 * 0) + (1 * 1)   
    

in other words, 1. This makes sense: our light is directly overhead, so the sample point on top of the sphere receives the full incoming light. Compare this to a point halfway down the sphere. A a normal point 45 degrees from the vertical might be   

    
    
    [.707, 0, .707]  
    

And the dot would be  

    
    
    (0 *.707) + (0 * 0) + (1 * .707)  
    

or .707. That means this sample point is getting about 70% of the incoming light. At the horizon of the sphere the dot will be `[0,0,1] dot [1, 0, 0]`. This dots out to   

    
    
    (1 * 0) + (0 * 0) + (0 * 1)   
    

or 0. This makes sense - at the horizon of the sphere the light is parallel to the surface and imparts no light.  
Or, in pretty picture form:  


[![](http://www.upvector.com/pages/Tutorials/Intro%20to%20Shaders/images/lambert1.gif)](http://www.upvector.com/pages/Tutorials/Intro%20to%20Shaders/images/lambert1.gif)

  


## Wherefore art thou cos(theta)?

So, it appears of this fancy-pants rendering is coming from the same bagels-and-coffee trick. How come? Lambert’s law isn’t some simple interpolation - it’s based on cosines, which give it the characteristic soft falloff around the horizon. How does this work?  
The sharp-eyed reader might notice that all of the vectors in this example are _normalized_, that is to say the length of all of the vectors in this example are 1. That’s is the special convention that turns a plain-vanilla dot product into a geometric proposition. As long as the vectors are normalized -- but **only** if they are normalized -- the dot product of the light vector and the normal vector is the cosine of the angle between the two vectors. That’s what makes the nice soft falloff on a Lambert-lit object, but it has lots of other properties as well.  
To understand how this bagels-and-coffee math turns into trigonometry, remember that ‘normalizing’ a vector just means setting its length to one. Visualize what happens if you sweep a 1-unit long line segment around in a circle, starting from the horizontal. As the segment rotates, you can draw a right triangle from it’s end point up or down to the horizontal axis, as in the example below:  
  


[![](http://www.mathsisfun.com/geometry/images/circle-unit-sct.gif)](http://www.mathsisfun.com/geometry/images/circle-unit-sct.gif)

  
If you recall your high-school trigonometry you’ll remember that the cosine of an angle in a right triangle is the ratio between the side of a right triangle next to the angle and the hypotenuse of the same triangle _(the “CAH” in “[SOHCAHTOA](http://www.mathwords.com/s/sohcahtoa.htm),” if you learned it the way I did)_. In this case, our hypotenuse is always 1 (it’s a unit line). so  the cosine is just the width of our right triangle. All of this works as described _only_ if the vectors are normalized,however - when your dots give you wonky results, non-normalized vectors are always the first thing to look for.  
_[This video from Khan Academy](https://www.youtube.com/watch?v=ZffZvSH285c) gives you a more in-depth derivation if this description isn’t clear._  
Once you grasp the unit-circle-cosine setup, it’s easy to see how dotting unit vectors creates cosine values rather than lunch budgets. See what happens when you dot a random vector against `[1,0,0]`:  

    
    
    example = [.866, .5, 0]  
    reference = [1, 0, 0]  
    example dot reference = (.866 * 1) + (.5 * 0) + (0 * 0) = .866  
    

As you can see the X component of the example vector has been preserved, but the other two are zeroed out. (This illustrates the meaning of the dot project - it’s the _projection_ of one vector on to another. We’ll touch on that more in the next post).   

In this case, projecting that 60 degree line segment onto the vector `[1,0,0]`creates a line segment from `[0,0,0]`to `[.866,0,0]` and the same kind of right triangle we described above. The ratio of the hypotenuse vector to this new ‘adjacent’ vector is .866 / 1, that is, plain old .866 — which we we know from the unit circle is the cosine of 60 degrees and the answer we were looking for.   

This is how the dot of two normalized (!) vectors is alway the cosine of the angle between them.  


## Dot's all, folks

So that's the basic theory of the dot product. Of course what the ruthlessly practical TA will want to know about is uses, not theory. Some of the applications will be obvious but there is a [plethora](https://www.youtube.com/watch?v=-mTUmczVdik) of less obvious ways the dot product can make your life eaiser. I’ll hit those in my next post.  In the meantime, bring instant coffee instead of paying for that venti tripple mocchachino every day. That stuff’ll totally blow your budget.  
  


##  Posts in this series

  * [Bagels and Coffee (intro to dot products)](bagels_and_coffee.html)
  * [Dots All Folks (dot product uses)](dots_all_folks.html)
  * [Dot Matrix (intro to matrices)](dot_matrix.html)
  * [Adventures in the 4th Dimension (translation matrices)](adventures-in-4th-dimension.html)
  * [To Scale! (scale matrices)](to-scale.html)

  


