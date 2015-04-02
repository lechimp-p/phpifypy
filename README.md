#PHPify.py
[![Build Status](http://img.shields.io/travis/lechimp-p/phpifypy/master.svg)](https://travis-ci.org/lechimp-p/phpifypy)

### Your pythonic PHP experience.

Uses the state-of-the-art error suppressor [FuckIt.py](https://github.com/ajalt/fuckitpy)
to bring the joy of programming PHP to Python.

### Run broken code

PHPify.py lets you run broken code by using the amazing capabilities of 
[FuckIt.py](https://github.com/ajalt/fuckitpy). Never mind code of newby programmers
anymore. Just take any bit of code you see on the internet and run it without mercy.
It won't always produce what you expect, but hey, who knows anyway?

### Amazing error logging

PHPify.py tells you about all errors it finds and even tags a severity
on them by using state-of-the-art language models. It will even tell you
the time an error occured, so you can just log all errors away and examine
them later. 

### API

The API inherited from [FuckIt.py](https://github.com/ajalt/fuckitpy) is simple
to use and lets you PHPify single functions or classes as well as complete
modules:

Add `import phpify` to the top of your script, then use phpify in any of the following ways:
 
### As a replacement for import
Use phpify to replace an import when you want to run a module with the amazing
capabilities of PHPify.py. 

```python
import phpify 
#import some_shitty_module
phpify('some_shitty_module')
some_shitty_module.some_function()
```

It's still not running and no errors a logged? We need more of PHPs superpower:

```python
import phpify 
phpify(phpify('some_shitty_module'))
# This is definitely going to run now.
some_shitty_module.some_function()
```

### As a decorator
Use phpify as a function decorator when you only want the force in a single function
(you should not want that). 

```python
@phpify
def func():
    problem_solved  
```

You can use phpify as a class decorator, too.

```python
@phpify
class C(object):
    def __init__(self):
        everything_works_now
```

##License
                    DO WHAT YOU WANT TO PUBLIC LICENSE
                       Version 2, December 2004

	Copyright (C) 2014
	
	Everyone is permitted to copy and distribute verbatim or modified
	copies of this license document, and changing it is allowed as long
	as the name is changed.

                    DO WHAT YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 	0. You just DO WHAT YOU WANT TO.
 
## Attribution

This module is a fork of AJ Alts [FuckIt.py](https://github.com/ajalt/fuckitpy)
