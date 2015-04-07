# TXT2PYNB

TXT2PYNB is a Sublime Text 2 package that takes a Python (or Julia) file with inline block-commented markdown blocks and turns it into an [iPython](http://ipython.org/notebook.html) (or [iJulia](https://github.com/JuliaLang/IJulia.jl)) notebook (`.ipynb`). Please view the "Tags" section below or the `Examples` folder for examples of scripts. The package will output a notebook of the same name as the script in the same directory where the script is saved. (e.g. `my_script.py` will output `my_script.ipynb` in the same directory)

### Download

This package can be dowloaded from [package control](https://packagecontrol.io/) in Sublime Text 2. Search for "TXT2PYNB" after installing package control and searching for it within the 'install packages' option.

### Building Notebook

Once installed in Sublime Text 2, TXT2PYNB can be called as a build-system by pressing `C + b` where `C` is the `command` key on Apple computers and `ctrl` on others. For some users, the TXT2PYNB build system will be called by default with `.py` or `.jl` scripts, but others might need to select it from `Tools->Build System->TXT2PYNB`.

Alternatively, TXT2PYNB can be searched and called using the Command Palette (`cmd + shift + p`). This is particularly useful if a user regularly uses other build systems for Python or Julia scripts. The default call to the TXT2PYNB build system can be turned off by removing the `TXT2PYNB.sublime-build` file in this package's folder.

### Script Execution (For use outside of Sublime Text 2)

Example execution of code for a python script, Julia works similarly. The command-line-executable script txt2pynb.py is in the `txt2pynb` folder. 

    python /path/to/txt2pynb.py /path/to/example_script.py

### Tags

The beginning and ending tags for code and markdown follow a typical html-like format. It is recommended that the entire markdown blocks be commented out and also the code tags be commented out (as below) in order to preserve the script's capability to be ran as a Python file.

    #<code>
    # This is a comment inside of a code block
    #</code>
    
    '''<md>
    This is markdown!
    </md>'''

### Space Delimiting

Having no code or markdown tags will result in the script being parsed with double space delimiting. Please view example number 2 to see this demonstrated. The markdown blocks must be in block comment format such as '''markdown'''  (or """markdown""" for Julia) in order to be correctly parsed. Also, markdown blocks can be squished on top of code blocks to allow for a markdown and code block in one double space-delimited block, as seen in Example_2 in the `Examples` folder. 

### Examples

View `Examples` folder for sample code and output.

### Common Issues

* `C+b` doesn't output anything.
  * If a build system is already assigned by default for `.py` or `.jl` files, it may be necessary to manually change the build system while the script is open by going to `Tools > Build System` and selecting `TXT2PYNB`. Likewise, if a different build system is desired for an open `.py` or `.jl` file, switch it back using the same procedure.

To Do
-----
1. ~~Turn into sublime text package~~
2. ~~Fix json output into pynb to make it look more pretty (also use JSON module)~~
3. ~~Remove dependencies~~
4. ~~Change so the infile is only called once (ie validate the already imported script)~~
5. ~~Fix indentation error~~
6. Incorporate test suite (nose)
7. ~~Validate double space delimited script~~
8. ~~Improve flow by making the script more modular (condense stripping functions as well)~~
9. ~~Fix spacing issue in code stripping function~~
10. Address compatability issues (test and make sure it works on Windows)
11. Add ability to 'pull back' code from edited notebook
12. Add ST 3 compatability 
