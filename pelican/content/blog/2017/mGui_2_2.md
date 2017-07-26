Title: mGui 2.2 release is ready
Date: 2017-07-25
Category: blog
Tags: maya, mgui
Slug: mGui_2_2
Authors: Steve Theodore
Summary: mGui version 2.2 is here
Status: Draft

The latest next point release of the [mGui](https://github.com/theodox/mGui) module for maya gui is up on on Github, thanks in large part to [+Bob White](https://github.com/bob-white), who put in a lot of the work on this release. 

Although this is a point release, it has some exciting improvements:

# Improved Menu Support

We've added a more refined an elegant method for handling sub-menus with the `SubMenu` class.  This works like a context manager, so the structure of the menu is obvious when reading the code.  


```python

 	with Menu(label='TestMenu') as food_menu:

        # conventional menu items
        hotdog = MenuItem(label = 'Hot Dog')
        burger = MenuItem(label = 'Burger')
        taco = MenuItem(label = 'Taco')

        # a submenu
        with SubMenu(label='Pizza') as sm:
            pepperoni = CheckBoxMenuItem(label='Pepperoni')
            sausage = CheckBoxMenuItem(label='Sausage')
            pineapples = CheckBoxMenuItem(label='Pineapples')
            for each in (pepperoni, sausage, pineapples):
                each.command += pizza_selected


        MenuDivider()

        with SubMenu(label='Delivery') as sm:
            with RadioMenuItemCollection() as radio:
                eatin = RadioMenuItem('Eat In')
                takeout = RadioMenuItem('Take Out')
                delivery = RadioMenuItem('Delivery')
```

We've also enhance menus so they support the same kind of dot notation as other mGui controls.  In this example that means you could get to the 'sausage' item as

```python
	food_menu.sm.sausage
```

which is going to be both more readable and more consistent with other mGui code.  If you use the YAML menu loader, that also supports submenus:

```yaml

        - !MMenuItem
            key:  check
            label:  checkboxes
            annotation: Toggle me!
            options:
              checkBox: True
            command: mGui.examples.menu_loader.checkbox


        - !MSubMenu
            key: submenu
            label: submenus

            items:
                - !MMenuItem
                  key: sub1
                  label: Item 1

                - !MMenuItem
                  key: sub2
                  label: Item 2

```

# working with existing items

At various points we supported three different idioms (`Menu.from_existing()`, `gui.derive()` and `Control.wrap()`. for putting an mGui wrapper around existng controls.  In this release these have been collapsed into a single function, `gui.wrap()` which has some cool new features:

	* It's automatically recursive. So if you wrap an existing menu, the returned object will have nested properties for all of the menuItems in the menu.  If you wrap an existing layout, you'll have nested properties for all the layout's children.
	* It does a better job matching the underlying maya gui widgets to mGui wrapper classes than any of the previous methods.  Because of some irregularities in the way Maya relates commands to objects there are still some edge cases the new `wrap()` should get most cases.
	* For maya objects with python callbacks, you can ask `wrap()` to convert them to [multicast delegates for you. This does not support mel callbacks yet, but we may be able to expand to supporting them in the future.

The new, improved `gui.wrap()` should make it much easier to add mGui controls or layouts to menus and windows that come from regular Maya.  

For the time being, we've re-pointed `gui.derive()` at `gui.wrap()` under the hood so it won't break existing code -- it will however issue a deprecation warning so that when we remove `derive()` in 2.3 people will have had plenty of warning.


# find() method for child controls

We've added a new method to all layouts that will collect all children of a layout by mGui type.  This is handy for big complex layouts where you aren't quite sure what something should be called -- or for layouts that you've gotten from `gui.wrap()`.

# &c.

We've also cleaned up and expanded the [examples](), added more test coverage, and fixed a few minor bugs (the most obvious one will be that the `StretchForm()` classes properly respect margins.  We're also starting to put more time into the [project wiki](), including some new tutorials.  Feedback and suggestions are much appreciated! And of course if you run into any problems be sore to log them on the [project issues page].  

