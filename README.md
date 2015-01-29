# txt2pynb

The `txt2pynb.py` script will take a Python (or Julia) file with inline block-commented markdown blocks and turn it into an [iPython](http://ipython.org/notebook.html) (or [iJulia](https://github.com/JuliaLang/IJulia.jl)) notebook (`.ipynb`). Currently, the script requires two command line arguments. The first is a path to the `txt2pynb.py` script (in a clone of this repo or wherever else) and the second is a path to your python script that is to be converted into a notebook. View the example input script and example execution below. Don't hesitate to contact the author with any inuiries or bugs, the code is still in its early stages.

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

Example execution of code for a python script. Julia works similarly

`python /path/to/txt2pynb.py /path/to/example_script.py`


To Do
-----
1. Turn into sublime text package
