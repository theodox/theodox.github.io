Title: Be cross
Date: 2015-01-16 19:11:00.000
Category: blog
Tags: math, unpublished
Slug: Be-cross
Authors: Steve Theodore
Summary: The vector cross product

We've talked a lot about the dot product in this series, because in an very
important way it's the foundation of linear algebra.  However we've neglected
the dot product's less famous little brother, the cross product, which is an
extremely useful tool for TA's. So let's remedy that injustice.  

  

The cross product, also known as the _vector product_, is a vector operation
like the dot product.  However it has two really important differences.

  

The first one is why it gets the alias _vector_ product. The dot is a _scalar
_product, because dotting two vectors gives you back a single number, a.k.a a
"scalar" value.  The cross product is the _vector _product because it returns
a new vector.  And, as it happens, that vector is very handy for anybody doing
3-d math because it's the normal of the plane defined by the original two
vectors:  
  

[![](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/images
/crossproduct.jpg)](http://help.adobe.com/en_US/FlashPlatform/reference/action
script/3/images/crossproduct.jpg)

  
  
The is obviously going to be useful, but it's a little trickier to explain
exactly _how_ the cross product does its thing.  The dot-product based
derivations that we've provided for matrices, for example, aren't too hard to
follow once you get the whole bagels-and-coffee derivation.  Cross products...
well, lets see if we can make a little sense of them.  As always, you _can_
just skate on, knowing that calling vectorA.cross(vectorB) will give you a
vector at right angles to the vectorA and vectorB, but it's always a good idea
to get under the hood and see how these little miracles operate instead of
just taking them purely on faith.  
  
  


