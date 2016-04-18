Title: Markdown Wrapup
Date: 2015-03-17 23:47:00.000
Category: blog
Tags: blogging, markdown
Slug: Markdown-Wrapup
Authors: Steve Theodore
Summary: An experiment with plain-text blogging in markdown.

> Since this was written I've moved the whole blog to a [Pelican]() based static site generated entirely from Markdown. It's a vastly nicer way to work than the old Blogger editor!  I've left this along for historical reasons but as of 'today' (spring 2016) I'm all Pelican, all the time.

A [while back](http://techartsurvival.blogspot.com/2014/11/wyg-wys.html) I blogged about how much I longed for a good [Markdown](http://daringfireball.net/projects/markdown/syntax) based blogging platform. Since a couple of people inquired about how that’s gone, I thought I’d mention my (meager) findings since then.  
  
## The options
  
There are several different ways you could get Markdown-based onto a blog:   

### Static site generators

I looked at a number of static generators, like [Gollum](https://github.com/gollum/gollum/wiki) from github and [Nikola](http://getnikola.com/blog/). Both of these were conceptually appealing, but suffered from similar issues, most notably the usual run of configuration and install issues the come with any web-world endeavor these days. I had a hell of time getting either one working install on the macbook I use for most of my writing and eventually decided that I wasn’t that interested in wrestling with those kind of things into the future. More importantly, I’m too busy to really admin my own server - I want a hosted service. If you’re more into running your own server – and you don’t mind sleuthing out things like getting the right Ruby package manager setup running – they could both work fine. 


#### Markdown-based blogs
There are a few markdown based blogging hosts out there. The one I looked at most carefully was [Silvrback](https://www.silvrback.com/), and I enjoyed it a good deal. The writing was clean and simple and it came with a built-in syntax highlighting: the biggest damn hassle about all these posts has been getting the code samples into a reasonable format without hopping around between multiple sites and pasting a lot of esoteric formatting codes in HTML by hand. So, I had a good experience with Silvrback and I seriously considered switching. If you’re just getting started it’s definitely worth a look, particulary for technical blogs like this one.
![silverback](http://knolzone.com/wp-content/uploads/2014/03/silvrback.jpg)  

#### Custom markdown
    
The last option would be trying to take control of the markdown to HTML conversion process and spit out a minimal set of HTML that would play nice with Blogger but need no hand-work to make it pretty (you’ll recall that I bitched about my earlier efforts getting bogged down in `<p/>` vs `<br/>` and other HTML nonsense I don’t want to think about. There are lots of Markdown generators out there at varying levels of sophistication, but I also don’t want to think too much about micromanaging those.

After a few bouts of intense googling, I ended deciding to stick with Blogger for two reasons. First, I didn’t see an obvious way to port my old stuff – more than a hundred posts with all sorts of special formatting and so on – and I felt it would be bad for the site to be split across two hosts. Also, I worried about losing readers if I switched URLs (if I do this again, I’m going to set up a custom domain early so people know the site by a redirect I can switch at will!). I will admit that I also wondered if using Google for hosting has anything to do with search results - I’ve noticed that a significant portion of traffic comes through Google searches and I wonder if other hosts are quite as well covered by whatever magic algorithm Google uses.  
Sticking with Blogger for hosting means figuring out to reconcile my markdown text and Blogger’s style sheets. Luckily, it turns out that [Sublime Text](http://www.sublimetext.com/) has a nicely configurable [Markdown preview plugin](https://github.com/revolunet/sublimetext-markdown-preview). I love Sublime anyway – it’s my go-to text editor for everything except heavy-duty C# and Python **(VS and [PyCharm](https://www.jetbrains.com/pycharm/), respectively, btw)**.   

In ordinary use, MarkdownPreview “bakes” your Markdown info nicely formatted HTML with all sorts of swanky CSS formatting – which is precisely what makes things hard for Blogger. With a little extra work, however, you can get it to produce a stripped-down HTML with the right tags and links but without all the extra CSS that conflicts with the Blogger template.   
It took a bunch of fiddling to figure out how it works, but once I got over the n00bishness it turns out to be very simple. Here’s a step-by-step to setting it up for yourself.  

---

###  1. Install the MarkdownEditing and MarkdownPreview packages for Sublime Text.

This is pretty simple using Sublime’s excellent Package Manager, so I’ll skip the details **([here’s some help](http://www.granneman.com/webdev/editors/sublime-text/packages/how-to-install-and-use-package-control/) if you need it.)**  

###  2\. Create a simplified HTML template

You want to make a simple HTML template that Sublime can render Markdown into. You can add some customisations if you like but the main business of the template is to prevent MarkdownPreview from filling in all of it’s own CSS styles.   

Luckily, it’s easy to do this: if you don’t add a placeholder for the HTML `<head>` tag, MardownPreview can’t stick all the styles in there. This means you can force Sublime to give you a stripped-down output that won’t override your Blogger template.  

If all you want to do is get uncluttered HTML, you can just use   

    {{ Body }}  
    

as your template. That will let you past your Markdown HTML into blogger while keeping your Blogger theme intact.  

Since I do a lot of code samnples in this blog, I opted to include a little bit of custom CSS to pretty it up. MarkdownPreview uses [Pygments](http://pygments.org/) to generate highlighted code. Pygments marks up the html with a bunch of custom HTML classes for different language parts, and you just need to provide some CSS that will decorate those guys. There are plenty of examples that work with Pygments which you can cut-and-paste like [this set from Rich Leland](https://github.com/richleland/pygments-css).   

For myself, I grabbed a free one that looked a lot like the highlighting style on Github – to keep my template simple I put it in a public folder on DropBox and used an HTML link to include it in the blog. **Feel free to use it if you’d like, but don’t link to it: I may keep fiddling with it and you don’t want my changes!. You can also get it [here](https://gist.github.com/theodox/4fefeb539f1d8ec341b0)**  

    
    
    <head>  
    <link rel="stylesheet" title="github" href="https://dl.dropboxusercontent.com/u/2977490/github.css">  
    </head>  
    {{ BODY }}  
    

The dropbox files contains the CSS styles for highlighting code, but none of the zillions of other styles that usually come out of the Markdown &gt; HTML translation. This way, my Blogger template will control the appearance of everything and keep the general style of the blog – but the code coming out of Markdown will be highlighted. Plus, I can tweak old entries by just changing the shared file. **One caution: Blogger is finicky about which links it will allow in the head tag: I would rather have linked to the Gists or a CSS file on github, but wasn’t able to get that to work.**  

### 3\. Customize the MarkdownPreview package.

Open up the user settings for MarkdownPreview (**Package Settings &gt; Markdown Preview &gt; Settings – User**). This will be a blank file the first time you open it, but like all Sublime settings files it’s a JSON file. We just need to tell the MarkdownPreview plugin to use our template:  

    
    
    {  
        "enable_highlight" : true,  
        "enable_pygments" : true,  
        "html_template" : "C:/path/to/blog_template.html",  
        "skip_default_stylesheet": true  
    }  
    

The key thing values here are the `html_template`, which is the path to the template file from step 2, and `skip_default_stylesheet`, which tells MarkdownPreview not to insert all those other styles.   

### 4\. Build your blog!

With the template and settings in place, create some Markdown. In Sublime, generating the HTML uses the same ‘build’ model as compiling code. So you first set the build system to Markdown (**Tools &gt; Build System &gt; Markdown**). Then you build it (**CMD + B or Tools &gt; Build**), which by default will create an HTML file alongside your markdown file. You can view the results in a browser directly or just open the HTML file in Sublime.   
What you should have at this point is nicely formed HTML without tons of extra CSS (and, if you added code-highlight styles, some colorful highlited text as well). You can just cut the HTML and paste it straight into the HTML view in Blogger and you should have a perfect, Blogger friendly but Markdown-clean and easy blog entry. Once you’ve done the setup steps once, your only job is a single cut-and-paste (you can even configure MarkdownPreview to copy the HTML to the clipboard instead of writing to a file!).   

---

## Wrapup

This is not the perfect blogging system, by a long shot – but it’s a whole lot better than Blogger’s slow GUI, and it offers flexible code highlighting for all of the languages that Pygments supports. Once all the spadework is done, posting is as simple as writing in Markdown, hitting the build button, then pasting into Blogger. So far I’m finding it a huge improvement.   

But of course, TA’s are _never_ satisfied so I bet this will come up again some other time…

