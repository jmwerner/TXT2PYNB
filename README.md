# txt2pynb

The `txt2pynb.py` script will take a Python (or Julia) file with inline block-commented markdown blocks and turn it into an [iPython](http://ipython.org/notebook.html) (or [iJulia](https://github.com/JuliaLang/IJulia.jl)) notebook (`.ipynb`). Currently, the script requires two command line arguments. The first is a path to the `txt2pynb.py` script (in a clone of this repo or wherever else) and the second is a path to your python script that is to be converted into a notebook. View the example input script and example execution below. Don't hesitate to contact the author with any inuiries or bugs, the code is still in its early stages. It should also be noted that the script will output a notebook of the same name as the script. (e.g. `my_script.py` will output `my_script.ipynb`)

Example input script:
```
#<code>
a = 5
#</code>

#<code>
	b = 10
	print b * 20
#</code>
#<code>
	a = b * 25
#</code>

'''<md>
This here is markdown

This is line two of markdown. Isn't it beautiful?

This is line three of markdown

#Markdown header! 
</md>'''
```

### Execution 
Example execution of code for a python script. Julia works similarly

`python /path/to/txt2pynb.py /path/to/example_script.py`

### Using Flags
Currently, placing a ```double_space_delimiter``` flag in the python script to be parsed will also allow blocks to be delimited by two or more spaces. 

    <flags>double_space_delimiter</flags>

Example of corresponding script. The markdown blocks must be in block comment format such as '''markdown'''  (or """markdown""" for Julia) 

```
<flags>double_space_delimiter</flags>

	# can I have a comment here?
	import re
	a = 5
	print re.search('a', "helalo") != None
	print re.search('a', "hallo") != None




a = 30 * 25
for i in range(0,5):
	print i


'''

This is a sigma $\sigma$ symbol in markdown and a forall $\forall$ symbol too!

Here's some mathematics $ 1 + 2 - 3 * 5 / 15$ and "quoted" information

And an integral for good measure $\int_{5}^{10}f(x)dx$

#Markdown header! 
'''
```

To Do
-----
1. Turn into sublime text package
2. Fix json output into pynb to make it look more pretty
3. ~~Remove dependencies~~
4. Change so the infile is only called once (ie validate the already imported script) 
