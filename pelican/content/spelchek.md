Title: spelchek
Date: 2015-05-16 17:45:00.000
Category: blog
Tags: , , , 
Slug: spelchek
Authors: Steve Theodore
Summary: pending

## [](https://www.blogger.com/blogger.g?blogID=3596910715538761404#spelchek)Spelchek

I’m planning one of the worst things that can happen to a TA: a big massive file move-and-rename operation. Much as I love my team, we have a poor record as a company when it comes to spelling, and it occurred to me that I’d like to at least have some degree of automatic spell checking on the names of the new files, folders and assets.  
It turns out that there’s no good spell checker for Python that doesn’t come with some kind of extension module (BTW, I’d love to be wrong about that - if you know one definitely post it in the comments). [PyEnchant](http://pythonhosted.org/pyenchant/) for example is great, but it’s got 32-bit only Windows extensions that I can’t distribute without a hassle.   


![](https://s-media-cache-ak0.pinimg.com/236x/55/2c/b5/552cb539fcc6b8addffb0eb19ec98298.jpg)

I did, however, find a very neat example of Python Power in a little post by Peter Norvig, who put together a simple spellchecker in a few dozen lines of plain, readable Python [code and great explanations here](http://norvig.com/spell-correct.html).   
I shamelessly borrowed his structure, with a couple of minor and not very creative tweaks. Peter’s original is built around Bayesian analysis: it guesses the correct word by looking at the relative frequencies with which variants show up – if ‘meet’ shows up 1000 times in your database but ‘mete’ shows up 5 times, that’s a good indication that ‘meet’ is the correct first guess.   
Since I’m in a rush, I didn’t use that functionality very much. I scrounged around for as many sources correctly scored words. Unfortunately the only free source I could rely on turned out to be the venerable ‘GSL’ or ‘General Service List’, which has great data but only for about 2000 words (I used the version found [here](http://jbauman.com/gsl.html), by [John Bauman](http://jbauman.com/index.html) as a the core of the list, and then scrounged the internet for other free sources. Since all of these were less common words than the ones in the GSL I gave them pretty arbitrary Bayes scores (4’s and 5’s for common words, 3’s for variants, plurals and participles). This is not sophisticated linguistics, but it’s close enough for horseshoes.  
The result is up on github as [spelchek](https://github.com/theodox/spelchek), which I affectionately refer to as the _cheap-ass spell checker._  
It is hardly rocket science, but it does work. You can do something like:  

    
    
       import spelchek  
       spelchek.correct('vhicle')  
        # 'vehicle'  
    

or   

    
    
        spelchek.guesses('flied')  
        # ['filed', 'flied', 'flies', 'lied']  
    

I would caution against using this for hard-core text work where perfect accuracy matters -- like database stuff, a customer-facing website, or a word processor -- since I did not go with high quality commercially or academically vetted word lists. I’m reasonably certain that there are some mis-spellings or oddballs in the 75,000 or so words I ended up with from various sources. Still, the module useful for my intended use, which is making sure that we don’t get things like ‘floder’, ‘frunishings’ and ‘vetegation’ (all of which shipped with in [State of Decay](http://www.ign.com/games/state-of-decay-year-one-survival-edition/xbox-one-20023993), I’m sorry to admit).   
As always, MIT licensed so go to town. 

