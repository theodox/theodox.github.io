Title: The Trust Fund
Date: 2015-01-22 21:23:00.002
Category: blog
Tags: , , , , 
Slug: _the_trust_fund
Authors: Steve Theodore
Summary: pending

A recent [discussion on TAO](http://tech-artists.org/forum/showthread.php?5243-Developing-Tools-for-your-pipeline-general-question) reminded me of this old GDMag column from 2010. Tech artists always have to fight to stay focused on the relationship at the heart of our business: no amount of technical wizardry matters if your artists aren't actually benefitting from what you do.   
  
While much has changed in the last five years, a lot of this still seems like good advice (to me, anyway, but I'm biased).  I might add a couple of sentences about 'more unit tests' and 'continuous integration' and similar buzzwords but that's just fluff: taking care of your users is all that really counts.  
  
  
  
Every cloud, says the old cliche, has a silver lining.  Nobody likes the angst and insecurity of our dubious economy.  Still, in these lean times, at least we're far less likely to be dragged away from useful work for chirpy HR seminars on workplace communications or, God helps us, to don blindfolds and lean backwards into the clammy arms of that W.O.W. fanatic from IT so we can "learn to trust our teammates."  Say what you like about the dire business climate, at least it tamps down the fluff industry.  
  
Honestly, though, the gurus of the workplace have it right about one thing. Blindfolds aside, trust is a key part of any functioning workplace and it's particularly important for us. We make art in a collective medium where all of the disciplines are inextricably tied up together.  You can make a career as a rock singer with a mediocre backing band.  You can prosper as the best actor on lame sitcom.  Cranking out great models for a game that crashes on load, however, isn't going to earn you fame or fortune. Our work can easily be dragged down by a lame graphics engine or a busted pipeline (though, to be fair, we should add that a fun design or a snappy engine can also be torpedoed by inadequate artwork).   
  


[![](http://unbounce.com/photos/trust-me.png)](http://unbounce.com/photos/trust-me.png)

  


  
Put bluntly, there are no lone geniuses in game art. We depend on other people -- graphics engineers, tools coders, designers, and our fellow artists --- to do what we do.   
  
These relationships are the foundation of our work lives. This doesn't mean that you have start every whiteboard session with a group hug.  In our world, trust is more than just a warm fuzzy feeling.  A healthy respect for your teammates - or the suspicion that they don't know what they're doing -- shapes how you work in very concrete, un-emotional ways.  


## Trust Busted

  
Consider the morning ritual that greets most working artists at the beginning of the day.  Theoretically we all saunter in, fire up the box, and do a get to pull down the latest tools and most recent build of the engine.  We grab a cup of coffee while the our system assimilates yesterday's changes and by the time we're finished with [icanhascheezburger.com](http://icanhascheezburger.com/),_ (wow, that is** extremely** 2010! –ed) _we're all caught up and ready for the day's labors.  
   
  


  


[  
![](http://blog.themistrading.com/wp-content/uploads/2012/06/lucy.jpg)](http://blog.themistrading.com/wp-content/uploads/2012/06/lucy.jpg)

  
That's the theory, but it's rarely the practice.  Far too many artists will do _anything_ to avoid that daily get.  "I don't like the risk," says one, "you never know if it's going to work from one day to the next."  Another artist complains, "The tool I need broke last month so I rolled back to a working one and now I don't want to get again." There's the perennial favorite, "It takes too long, so I only do it once a month." And don't forget the oldest standby of them all: "I don't worry about that stuff, I'm just need my Max files."   
  
Sound familiar? This all-too-common story is a tangible example of a breakdown in trust, and you don't need to a special edition of Oprah to see how it undermines the studio.  If the artists don't trust the tools team, they try to bypass the tools and find workarounds. But this goes both ways: just imagine the dark mutterings coming from the engineering department every time they have to hunt down a 'bug' that's really caused by out-of-date tools or hacky workarounds.  The artists think the engineers are lost in the clouds, the tools team think the artists are big babies.  Pretty soon things bog down in recriminations and buck-passing.  
  
The damage from this kind of breakdown goes far beyond eye-rolling and sarcastic IM messages.  It's more than everyday inter-departmental wrangling, too. If you cope with tool and process problems by simply opting out, you aren't just irritating the  tools coders or TA's -- you're also leaving your fellow artists hanging.  
  
It's perfectly understandable, of course.  As an artist you're stuck with the studio toolset -- it's not like you can take your business somewhere else if you don't like the your in-house material editor or custom map tool. With deadlines looming and creative problems to solve, it's hard to gin up much enthusiasm for bird-dogging an obscure problem with a wonky exporter plugin or tracking down the exact setting that adds 11,000 warning messages to your map imports. The temptation to find a quick workaround and move on is overwhelming.  
  
But – _and here's the important part_ ! – ducking out on the problem doesn't just bypass it.  It perpetuates it, for you and for everybody else.  
  
When the culture in the art department deals with tools problems by simply ignoring them, it becomes impossible for the tools team or tech artists to build long-term solutions.  Nobody's going to fix a bug that never gets reported, and nobody's going to improve on a bad workflow if the artists don't lobby for a real improvement.  Grumbling to each other at lunch doesn't count -- unless someone actually makes it clear that there's an issue, things won't get better. _Never_ underestimate how little the other departments know about your problems.  The political hassles of scheduling and finding resources for a real fix may be a problem that has to be settled among leads — but its every line artist's responsibilty to make sure both the art leadership and the tools team know when things are broken.  
  
The old chestnut about trusting is that it leaves you vulnerable.   Working artists can relate to that, because nothing makes you feel more vulnerable than having a critical part of your pipeline break down when you've a looming deadline and the producer is breathing down your neck.  Trusting can be scary -- hell, the entire output of the Lifetime Network is devoted to that theme — but as every learn-to-love-again melodrama teaches you need to take some risks if you want to grow... or to ship good games.  
  


## Trust Building Excersize

  
Fortunately, there are some concrete things you can do to strengthen the bond of trust between the content team and the folks who are supposed to help them make the game —  and none of them requires a sit-down with Dr. Phil.  
  


### Testing

  
The most important way tools teams can build trust is to manage their releases better. Nobody would dare release a 99 cent iPhone game into the wild without testing and QA support (_really? have you been to the App Store lately? –ed._)  All too often, though, tools teams and tech artists roll out changes without doing the legwork needed to make sure the tools work as advertised.  When teams were smaller and development was less ponderous, tool writers learned to love fixing bugs and adding features with a simple checkin. It feels great to be able to drop in a one line fix into a script and tell your disgruntled customer "just get the latest version and you'll be able to work again."   
  
In a big modern studio, though, that immediacy is an expensive luxury. When you're supporting 50 or 100 artists, the costs of catching bugs late mount up quickly.  This is particularly true for tools like Max and Maya plugins, which can leave bad data inside art files long after the original bug is fixed.  No fix is fast enough to pay for the cost of dozens of angry, idled artists.  Bugs will always happen, but an aggressive testing program (complete with real, live testers, whether they're QA folks or tech artists), will go a long way toward easing the pain. Testing will certainly slow the response time for feature requests and trivial fixes.  But the benefits in terms of quality and reliability - and therefore, trust between the tools team and the content team -- are more than enough to pay for the hassle.  
  


### Regularity

  
Ship dates matter, as we all know too well. A planned release schedule for tools enhances trust, because it helps hard-working artists brace for changes. Tools that just magically appear in the daily synch are often simply ignored -- if the new skeleton editor came out while you were polishing run cycles, there's a good chance you don't even know its there (Note to tools and teacart teams everywhere: nobody reads those emails!)  When tools change their behavior or appearance without warning, artists lose faith in the stability of their environment.  And of course, if an innocent synch introduces bugs along with UI changes, the trust level will plummet and the vicious cycle of avoidance will begin.  
  
If, on the other hand, tools go out the door at well advertised times -- hopefully, coordinated with production to avoid stepping on sensitive deadlines! -- everyone can budget the time and energy needed to make sure that the new functionality is supported, new workflows are well understood, and any bugs that slip through test are squashed before they do too much damage.  Scheduled releases, accompanied by scheduled learning time, are a safer and less intimidating way to keep the artists and tools builders communicating.  
  


### Uniformity

  
Trust, as the cliche goes, is a two-way street.  If we want the tools to get better, we need to contribute something too.  The effort that goes into doing tools with adequate testing and support is hard to sustain if the production people subvert the new tools and insist on their right to opt out of changes.  Keeping an art team productive is a herculean labor.  There are a million sources of potential problems: out of date video drivers, conflicting versions of software, different OS versions — you name itg. When every artist has a completely private environment, with personally selected versions of tools and private workarounds, support is exponentially harder. Time that should go to fixing bugs in the current version of the tool will be wasted simply trying to figure out what's going on and why.  
  
Surrendering control over your personal working environment is emotionally difficult for most artists. We're slavishly devoted to customizing our hotkeys, tweaking the layout of our custom toolbars, and enhancing our personal workflows with scripts and widgets we've downloaded from the net. We want the same level of personal control over our in-house tools.  Unfortunately, the line between what's personal and what has to be shared with others can be pretty blurry.  Out of date tools may be producing data that's subtly wrong without being obviously busted, dragging down game performance or leading to crashes. Tools that are made to work together may function poorly if they aren't updated in tandem.  And working a completely private environment means you can't give meaningful feedback to the tools folks to help them do their jobs better.  The tools guys can only support one good environment at a time; it should be the one you're working on.  
  


[![](http://www.multiplestreammktg.com/blog/wp-content/uploads/2013/03/fb99-300x239.png)](http://www.multiplestreammktg.com/blog/wp-content/uploads/2013/03/fb99-300x239.png)

  


### The touchy feely stuff

  
As any Oprah devotee knows, communication is the key to building trust.  Unfortunately, tools providers and line artists don't always communicate as well as they ought to.  Technical types tend to understand the needs of computers better than they do the needs of artists. They're always tempted to  to build tools that make things easier for computers, rather than helping artists.  Artists, on the other hand, are frequently too shy to  bring their concerns to the attention of the tools team.  
  
If you don't tell people clearly what is broken in your workflow, what's preventing you from iterating, or what kind of changes would make things better, you have no right to bitch about the tools you've got.  Both sides need to explain their needs clearly and both sides need to listen attentively. Tech artists, who by nature have a foot in both worlds, are invaluable for helping these discussions along, as are producers who can provide high level guidance on the distinction between must-have and wouldn't-it-be-nice features.   
  
The bottom line is really very simple. Artists, tech artists and tools engineers all need to commit to making things better.  Good tools don't make for good games on their own — but lousy tools certainly make for lousy games. So, if you skip the meetings, don't report bugs, and try to roll your own toolset, you're making your own life and your teammates lives harder in the long run.  
  
Trust me on that.  
  


[![](http://trevinwax.com/wp-content/uploads/2011/07/1969.gif)](http://trevinwax.com/wp-content/uploads/2011/07/1969.gif)

  


  
  


  


