Title: State of Decay 2
Category: blog
Tags: games, industry
Slug: sod2
Date: 2018-04-29
Authors: Steve Theodore
Summary: After a long, long, _long_ dev cycle, [State of Decay 2](https://www.stateofdecay.com/) is finally about done.

![SOD 2 box](https://news.xbox.com/en-us/wp-content/uploads/thumb_610D2555B6F4417F9CDEDA14369E8419.jpg)

It's no accident that there have not been a lot of blog entries in the last several months, but hopefully life will be returning to normal soon.  I took the time to clean up my [site generator](2016/new_blog) and simplify the site theme, though I expect I'll probably waste a bunch of time fiddling around over the summer.

In any event, the game is looking good -- although I've got one **HUGE** bug I must squish before we go out the door! -- and it's been a real blast to bask in some of the reactions from people who've seen the game.  

The last couple of years have been kind of a wild ride, professionally -- I certainly never thought I'd spend more time staring at C++ than anything else ! --  but at least, now that the dust is settling, there should be time for blogging again.  With all the crazy stuff I've had to learn I'm sure there will be lots to chew over, too.

In any event, the press embargo will lift on May 1st, and opening day will be May 22d.  In the meantime, here's a little video teaser from the company stream with a special shout out to my colleague Jeff Sult, who helped me ferret out a truly insidious bug in the Xbox shader compiler.

<iframe width="560" height="315" src="https://www.youtube.com/embed/fSFqoZ3YlUI" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

> PS If you're wondering... sometimes the Xbox decides to 'optimize' exponent operators to use a logarithm instead of a multiply... Which is very nice unless your exponent somehow goes _negative_, in which case the result is a NAN which can really mess up your PBR G-buffers.  Sigh...

