
import re, sys

# args are parser file name [0] and path to python file to parse [1]
args = sys.argv

input_file_name = args[1]

outfile_split = args[1].split('.')
output_file_name = outfile_split[0] + '.ipynb'


if outfile_split[1] == 'py':
	lang = 'python'
else:
	lang = 'julia'

# Ensures that all tags are opened and closed. Returns ordering of code and md blocks
def validation(file):
	codeFlag = False
	mdFlag = False
	order = []
	for line in infile:
		if codeFlag:
			if re.search(code_end, line) != None:
				codeFlag = False
				order.append('code')
		else:
			if re.search(code_start, line) != None:
				codeFlag = True
		if mdFlag:
			if re.search(md_end, line) != None:
				mdFlag = False
				order.append('md')
		else:
			if re.search(md_start, line) != None:
				mdFlag = True
	if codeFlag or mdFlag:
		print 'ERROR: Code or md tags not closed in script'
	return order;

def content_strip(line, output_file):
	# Remove garbage from string
	outline = ''.join(line)
	outline = re.sub('\n#$', '', outline)
	outline = re.sub('(^\n*)', '', outline)
	all_lines = outline.split('\n')
	iter = 0
	strip_one_tab = False
	lines_length = len(all_lines) 
	while iter < lines_length:
		if re.search('^\t', all_lines[iter]) != None and iter == 0:
			strip_one_tab = True
		if strip_one_tab:
			final_out = re.sub('^\t', '', all_lines[iter])
		else:
			final_out = all_lines[iter]
		# Escape any backslashes or tabs
		final_out = re.sub('\\\\', '\\\\\\\\', final_out)
		# Excape any other string literals
		final_out = re.sub(r'\t', '\\\\t', final_out)
		final_out = re.sub(r'\"', '\\\"', final_out)
		output_file.write('\"' + final_out)
		iter += 1
		if iter != lines_length:
			output_file.write('\\n\",\n')
		else:
			output_file.write('\"')
	return None;

def start_code(file):
	file.write('\t\t\t{\n \t\t\t "cell_type\": \"code\", \n\t\t\t \"collapsed\": false, \n\t\t\t \"input\": [ \n')
	return None;

def end_code(file):
	file.write('\n\t\t\t],\n \t\t\t\"language\": \"' + lang + '\",\n\t\t\t\"metadata\": {},\n\t\t\t\"outputs\": [] \n\t\t\t}')
	return None;

def start_md(file):
	file.write('\t\t\t{\n \t\t\t "cell_type\": \"markdown\", \n\t\t\t\"metadata\": {},\n\t\t\t\"source\": [ \n')
	return None;

def end_md(file):
	file.write('\n\t\t\t] \n\t\t\t}')
	return None;

def start_notebook(file):
	file.write('{\n\t\"metadata\": {\n \t\t\"name\": \"\"\n\t}, \n\t\"nbformat\": 3,\n\t\"nbformat_minor\": 0,\n\t\"worksheets\": [\n\t\t{\n\t\t\t\"cells\": [\n')
 	return None;

def end_notebook(file):
	file.write('\t\t\t],\n\t\t\"metadata\": {} \n\t} \n\t]\n}')
	return None;


outfile = open(output_file_name, "w")

infile = open(input_file_name, "r")
script = infile.read()
infile.close()

flag_start = '<flags>'
flag_end = '</flags>'


flag_tags_regex = '(?s)(?<=' + flag_start +')(.*?)(?=' + flag_end + ')'
md_block_regex = '(?s)(?<=(\'\'\'|\"\"\"))(.*?)(?=(\'\'\'|\"\"\"))'
flag_block = re.findall(flag_tags_regex, script)
if len(flag_block) > 0:
	if flag_block[0] == 'double_space_delimiter':
		flag_strip = re.search('(?s)(?<=' + flag_end + ')(.*)', script)
		newscript = flag_strip.group()
		code_blocks = []
		md_blocks = []
		block_order = []
		# Splits on two or more \n
		splits = re.split(r'[\n]{3,}', newscript)
		for block in range(0, len(splits)):
			if splits[block] != '':
				str_tester = re.search(md_block_regex, splits[block])
				if str_tester:
					content = str_tester.group()
					md_blocks.append(content)
					block_order.append('md')
				else:
					code_blocks.append(splits[block])
					block_order.append('code')
else:
	code_start = '<code>'
	code_end = '</code>'
	md_start = '<md>'
	md_end = '</md>'
	# Generate regexs for eventual extraction between tags
	# (?s) - to match over multiple lines - the rest is to match code between code tags
	code_tags_regex = '(?s)(?<=' + code_start +')(.*?)(?=' + code_end + ')'
	md_tags_regex = '(?s)(?<=' + md_start +')(.*?)(?=' + md_end + ')'
	code_blocks = re.findall(code_tags_regex, script)
	md_blocks = re.findall(md_tags_regex, script)
	infile = open(input_file_name, "r")
	block_order = validation(infile)
	infile.close()


## ADD VALIDATION FOR SPACE DELIMITED SCRIPTS




start_notebook(outfile)

code_index = 0
md_index = 0
for block in range(0,len(block_order)):
	if block_order[block] == 'code':
		start_code(outfile)
		content_strip(code_blocks[code_index], outfile)
		end_code(outfile)
		if code_index + md_index < (len(block_order)-1):
			outfile.write(',\n')
		else:
			outfile.write('\n')
		code_index += 1
	else:
		start_md(outfile)
		content_strip(md_blocks[md_index], outfile)
		end_md(outfile)
		if code_index + md_index < (len(block_order)-1):
			outfile.write(',\n')
		else:
			outfile.write('\n')
		md_index += 1

end_notebook(outfile)


outfile.close()









