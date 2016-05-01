Title: Porting Spelchek to Boo 
Date: 2015-06-06 22:13:00.000
Category: blog
Tags: boo, spelcheck
Slug: Porting-Spelchek-to-Boo
Authors: Steve Theodore
Summary: A port of the [Spelchek](https://github.com/theodox/spelchek) spell checker to Boo, just to prove a point.


What could be more ghostly than a _post mortem?_  
  
If [my last post about Boo](http://techartsurvival.blogspot.com/2015/05/boo-who.html) piqued your interest, but you haven’t had time to do a deep dive into the language to see for yourself, I’ve posted a version of the [Spelchek](https://github.com/theodox/spelchek) Python spell checker module converted to Boo so you can see the similarities and differences between the two languages.   
The original Python version is [here](https://github.com/theodox/spelchek/issues) and the Boo port is [here](https://github.com/theodox/BooSpell). As a good indication of what I’ve been saying about the economy of Boo syntax, the Boo version comes in at almost the same size as the Python original (5.05 kb for Boo and 4.95kb for Python) and pretty much the same number of lines – I haven’t done the excersize of converting it to C# for comparison but I’d guess the C# version would come in at about half again as much typing.  
Looking at the code, significant chunks are almost identical: the logic is pretty much the same and the type annotations are the only real difference.   
Thus  

becomes   
    
    :::python
    def add(word, priority=4):  
        """  
        Adds <word> to the dictionary with the specified priority (default is 4)  
        """  
        _DICTIONARY[word.lower().strip()] = priority  
    

becomes

    :::boo
    def add(word as string, pri as int):  
    """  
    Adds <word> to the dictionary with the specified priority.   
    """  
        _DICTIONARY[word.ToLower()] = pri  
    



which is pretty much identical.  
The tricky bit of the conversion was the routine which generates possible variants of the word - it generates variants of a word by transposition and deletions. In Python:  

    :::python
    def first_order_variants(word):  
        """  
        return the obvious spelling variants of <word> with missing words, transpositions, or misplaced characters  
        """  
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]  
        deletes = [a + b[1:] for a, b in splits if b]  
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]  
        replaces = [a + c + b[1:] for a, b in splits for c in _ALPHABET if b]  
        inserts = [a + c + b for a, b in splits for c in _ALPHABET]  
        return set(deletes + transposes + replaces + inserts)  
    

As you can see the first list comprehension, `splits`, generates a lists of pairs representing places where the word could be broken up, so that ‘cat’ produces `[("c","at"), ("ca", "t")]`. The other comprehensions use that list to try inserting, deleting or transposing letters to guess what the user might have really been typing.  
In Boo, the tricky bit was getting the compiler to recognize that the `splits` list contained a pair of strings and that all the lists produced by it would also be lists of strings. Porting the python code directly wouldn’t work because Boo would see `splits` as a list of type `object` instead of deducing that it was a set of string pairs.   
Here’s the Boo version, which as you can see is recognizably the same but is clunkier than the Python, due to the need for typing,   
    
    :::boo
    def first_order_variants(word as string):  
    """  
    return the obvious spelling variants of <word> with missing words, transpositions, or misplaced characters  
    """  
        _stringList = Boo.Lang.List[of (string)]  
        _strings = Boo.Lang.List[of string]  
        pair = {w as string, i as int | (w[:i] cast string, w[i:] cast string)}  
        splits = _stringList((pair(word, i) for i in range(len(word) + 1)))  
        deletes  = _strings((a + b[1:] for a as string, b as string in splits if b))  
        transposes  = _strings((a + b[1] + b[0] + b[2:] for a as string, b as string in splits if len(b) > 1))  
        replaces  = _strings((a + c + b[1:] for a as string, b as string in splits for c in _ALPHABET if b))  
        inserts  = _strings((a + c + b for a as string, b as string in splits for c in _ALPHABET))    
      
        result = HashSet[of string]()  
        for chunk in (deletes, transposes, replaces, inserts):  
            result.UnionWith(chunk)  
      
        return result  
    

To clean it up I added two ‘aliases’ up at the top, since the Boo syntax for declaring typed containers is hard to read (‘List[of string]’): so `_stringList` is a shortcut for ‘list of string arrays’ and `_strings` is a shortcut for ‘list of strings’.  

The variable `pair` contains a lambda (ie, an inline function) using Boo’s idiosyncratic syntax: you could mentally rewrite it as  

    :::boo
    def pair(w as string, i as int) of (string):  
        return (w[:i], w(i:))  
    

or in other words “give me a string and an integer, I’ll return a pair of strings split at the index you gave me.”  

With those helpers in place the logic is identical, but it is harder to follow because of all the type-mongering. I’m pretty sure there are more elegant ways to do this withgout being so wordy, but I’m not an expert.   

# [](https://www.blogger.com/blogger.g?blogID=3596910715538761404&bpli=1&pli=1#so)So…

The point of the experiment was to see how hard the Python to Boo translation would be. This is an application where types actually matter a good deal, since all my values are strings and I need to be able to do string operations like joins on them – if all I was doing as asking questions of them things would have been more Pythonic (though probably slower as well: one of the reasons we need those types is to get the compiler to help us speed the code up).   

While this is hardly a demanding application, it is at least a proof-of-concept for the idea of prototyping in Python and then selectively porting to Boo isn’t completely nuts.

