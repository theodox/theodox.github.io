Title: code wars
Date: 2015-08-08 12:49:00.000
Category: blog
Tags: programming
Slug: code_wars
Authors: Steve Theodore
Summary: Code Wars, yet another programming dojo -- but a pretty good one

By a certain stroke of cosmic irony, it was just after I finished shoe-horning lame _Star Wars_ jokes into my last post that I started to get obsessed with [CodeWars](http://www.codewars.com/), one of the plethora of competitive coding sites that have sprung up in the last few years.   
  

[![](http://3.bp.blogspot.com/-vc-eVNbzo1Q/VcZdEcRBhXI/AAAAAAABMag/NYI22iT0zro/s400/cw.png)](http://3.bp.blogspot.com/-vc-eVNbzo1Q/VcZdEcRBhXI/AAAAAAABMag/NYI22iT0zro/s1600/cw.png)

  
Mostly I find that sort of thing pretty annoying – it’s a genre that all too easily degenerates into macho brogrammer chest-thumping. 90 percent of the code I see on those sites is so tightly knotted – in hopes of scoring fewest-number-of-lines bragging rights – that it’s useless for learning. I’m impressed as hell by this:  

    
    f=lambda s:next((t,k)for t,k in map(lambda i:(s[:i],len(s)/i),range(1,len(s)+1))if t*k==s)  
    

but I never want to have to _interact_ with it (Bonus points if you can tell what it does! Post your answer in the comments....)  

The nice thing about Codewars is that the experience tends to push you into thinking about how to solve the problems, rather than how to maximize your score. 

I particularly like two things: first, the site includes a built-in test framework so you can do The Right Thing<sup>tm</sup> and write the tests before you write the code – not only is it a helpful touch for would-be problem solvers its very effective ‘propaganda of the deed’ for encouranging people to take tests seriously. 

Second, the site doesn’t just show you the ‘best’ solutions, it shows you all of them – and it allows you to vote both for solutions you think are clever and ones you think embody “best practices.” That snippet I posted above is extremely _clever_ but not a best practice – I wouldn’t let something like that into my codebase if I could avoid it! I’m not smart enough to unriddle such things, though I’m glad they exist.  

The other nice thing is that most of the problems are bite-sized, the sort of thing you can chew on while waiting for a longish perforce sync to complete. It’s a great way to practice you coding chops outside all the gnarly things that come with working in a particular problems set for work. I’ve had a work task which involved me in a lot of 5-minute wait times this week and I found CodeWars to be a nice chance to do keep my brains warm while waiting for Perforce.  

So, if you’re looking to sharpen up your coding skills you should definitely check out [CodeWars](http://www.codewars.com/). My username is _Theodox_ and in the goofy ninja-academy language of Codewars we can form an ‘alliance’ by following one another. We can make technical art a power in the land!  
On the practical side: codewars supports Python, Javascript, and several other languages – they just added C#. It’s great way to get familiar with new syntaxes and to see how folks who know what they are doing tackle problems natively, it’s a great tool to pick up a new language on your own. Give it a shot!  
  


