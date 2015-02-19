# txt2pynb

The `txt2pynb.py` script will take a Python (or Julia) file with inline block-commented markdown blocks and turn it into an [iPython](http://ipython.org/notebook.html) (or [iJulia](https://github.com/JuliaLang/IJulia.jl)) notebook (`.ipynb`). Currently, the script requires two command line arguments. The first is a path to the `txt2pynb.py` script (in a clone of this repo or wherever else) and the second is a path to your python script that is to be converted into a notebook. View the example input script and example execution below. Don't hesitate to contact the author with any inquiries or bugs, the code is still in its early stages. It should also be noted that the script will output a notebook of the same name as the script. (e.g. `my_script.py` will output `my_script.ipynb`)


### Execution 
Example execution of code for a python script. Julia works similarly.

    python /path/to/txt2pynb.py /path/to/example_script.py


### Examples
View `Examples` folder for sample code and output.


### Using Flags
Adding a number `1` flag as the third command line argument will allow for space delimited parsing. Please view example number 2 to see this demonstrated.

    python /path/to/txt2pynb.py /path/to/example_script_with_space_delimiting.py 1

The markdown blocks must be in block comment format such as '''markdown'''  (or """markdown""" for Julia) in order to be correctly parsed. Also, markdown blocks can be squished on top of code blocks to allow for a markdown and code block in one double space-delimited block.


To Do
-----
1. Turn into sublime text package
2. ~~Fix json output into pynb to make it look more pretty (also use JSON module)~~
3. ~~Remove dependencies~~
4. ~~Change so the infile is only called once (ie validate the already imported script)~~
5. ~~Fix indentation error~~
6. Incorporate test suite (nose)
7. ~~Validate double space delimited script~~
8. Improve flow by making the script more modular (condense stripping functions as well)
9. Fix spacing issue in code stripping function