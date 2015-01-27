# iPython_Parser

This script will (eventually) parse a hybrid markdown/python script (saved as a .py file, see example below) and turn it into an iPython notebook. Once working properly, the functionality will be placed into a Sublime Text package and ported to iJulia as well. 

Example script:
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
