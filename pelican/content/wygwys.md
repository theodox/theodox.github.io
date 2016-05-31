Title: WYG > WYS
Date: 2014-11-01 11:00:00.000
Category: blog
Tags: blogging, markdown
Slug: wygwys
Authors: Steve Theodore
Summary: The first step on the long road to a streamlined, markdown based blogging platform...

> Update 4/4/2015:  I've got a much improved pipeline for markdown blogging using Sublime Text, as detailed [here](markdown-wrapup.html).  I'm also having a lot of luck with [MDWiki ](http://dynalon.github.io/mdwiki/#!index.md)for static sites on [github.io](http://github.io/)  
> Update 5/1/2016:  If you're reading this, I've finally transitioned over to all-markdown, all-the-time using [Pelican](http://docs.getpelican.com/en/3.6.3/index.html)

First off, a confession. I’ve become a plaintext nazi. 30 years since I first hit _Ctrl+I_ to italicise a piece of text, I’ve pretty much abandoned fancy-pants text edtors for the hardcore geek chic of plain text and [Markdown](http://daringfireball.net/projects/markdown/syntax).  

To be honest, this makes me uncomfortable, because plain-text-chauvinism is the techie equivalent of skinny jeans and ironical facial hair; it’s definitely a thing for the Cool Kids<sup>tm</sup>, a demographic which is not really my native habitat.  

But I’m willing to be cool if that’s what it takes.  
  
  
[Markdown](http://daringfireball.net/projects/markdown/syntax) is just a great tool for writing web or wiki content. If you spend a lot of time typing - particularly if you’re a TA who spends a lot of typing Python! – it becomes natural really quickly.  
The great thing about markdown is that it’s not dependent on the vagaries of a particular editor or application. There’s no need to worry about the layout of the menus or the mnemonics of the hotkeys - you just type. You just tap away without taking your hands off the keyboard to hit special key combinations for formatting (eg **bold**, _italic_), so you go a lot faster.   
In markdown, the emphasis is on the structure of what you’re writing instead of the presentation. You don’t format, you ‘mark up’ - that is you indicate what the job of a particular bit of text, is but you don’t describe it’s appearance. You can create headings, lists, block quotes, and even code snippets just using some simple conventions. Moreover the conventions are pretty readable in plain text. For example, you this little snippet of text  

    
    heading  
    ========  
    This is some plain text  
      
    ### subheading  
        * list item  
        * other list item  
    

Produces this formatted output:  


# heading

text goes here  


### subheading

  * list item
  * other list item

The actual look of the output is going to be controlled down stream something else. Most markdown is processed into HTML using CSS to control things like fonts, line-spacing, and alignment.   

I’ve found that markdown makes me a lot more productive than traditional WYSWIG editing. In part that’s because I can write markdown in a very stripped-down editor like [Sublime Text](http://www.sublimetext.com/) on the PC or [Ulysses](http://www.ulyssesapp.com/) on the Mac. These stripped-down editors are really qick and responsive, since they do so much next to nothing in the realm of document layout. Most important for me, they include far fewer distractions than Word or even Google Docs, so I can focus on the job at hand instead of fiddling around with styles and formatting.   

In cases where the layout actually matters I can take the finished text and export it via HTML or PDF to a traditional layout program, but nowadays that almost never happens: I literally cannot remember the last time I worried about the layout of words and images on a printed page (which is a pretty odd reflection for me, since I only got into computers because of [desktop publishing](http://www.opticentre.net/FAQ/Desktop-publishing-%28DTP%29/History-of-Desktop-publishing/), back when that was a thing.). Some flavors of markdown include the ability to inline html directly in the text for special purposes - for example, I got the superscript after Cool Kids tm by typing  
    
    Cool Kids <sup>tm</sup>   
    

99 times out of 100, however, this level of specificity isn’t important until the real work of writing is done and I’m just polishing up - I’m much happier focusing on the actual content and tweaking the visuals at the very last minute. That’s what a lifetime of game devlopment does to a person. 

Nowadays I do all my writing in plain text and markdown, with two exceptions. The wiki we use at work, [Confluence](https://www.atlassian.com/software/confluence?_mid=2c4fae43fb6d045f4fbe6afdba94a6fe&gclid=Cj0KEQjwt7KiBRD9lOePpe_BhrgBEiQAHaS_19HAtXBp54afa2VUzVBDBXsvpGSZWav3m92wizJ8DZsaAtPB8P8HAQ), doesn’t support markdown and to be perfectly frank it drives me nuts: The editor feels sluggish and the workflow constantly distracts me from what I’m supposed to be actually writing. And, unfotunately, Blogger doesn’t support md either. Blogger is at least not quite as sluggish as Confluence, but it definitely feels like wearing a deep-sea diver suit compared to blazing away in a plain text editor with markdown.  

Luckily I’ve found an option that at least looks pretty good. This post was written entirely in [StackEdit](https://stackedit.io/), a free online markdown editor which also allows publishing directly to Blogger. I followed [these instructions](http://www.g14n.info/2013/12/how-to-use-markdown-to-edit-blogger.html) by Gianluca Casati which seem to work pretty well.   

On the upside, this feels a lot more productive and focused than the usual Blogger writing process. In particular, it’s way easier to include short bits of code in markdown. Including code snippets into blogger, on the other hand, is a huge pain in the patootie; In the past I’ve used [Gists](https://help.github.com/articles/about-gists/), which are not to hard to embed and produce nicely highlighted code in lots of languages. For long format code it’s still a great tool. However it’s not ideal for small snippets of a few lines - there’s a lot of hopping around between editors and it’s very disjointed, which tends to get in the way of good flow when writing. For short jobs I will often just hand-edit the HTML produced by Blogger, which works but is, frankly, BS.   

One the downside, the StackEdit &gt; markdown &gt; html &gt; Blogger pipeline is precisely the sort of jury-rigged song and dance that drives me crazy in my day job. Translations are rarely perfect in any case, and inserting three of them along the way to do a single job offends my sense of Pipeline Fu. I have yet to figure out how to tweak the final results to stay in line with the established style of the blog, and it’s particularly tough to tweak the final results directly in Blogger if I need to make a tweak. The last straw is blogger's maddening habit of replacing &lt;p&gt; tags with &lt;br/&gt; tags, even if you paste HTML right into the HTML editor.  It all feels a lot like a complex MEL pipeline. It works... but it feels wrong.  

So, apologies for any wierd fomatting here - this is a very beta version of a new process. I’m still not satisfied that this is the ‘right’ way to write for the web (Santa, if you’re reading this, I’d _kill_ for a good markdown blogging platform that also did Python syntax highlighting!).

