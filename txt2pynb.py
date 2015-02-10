
import re, sys, json

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


with open(input_file_name, "r") as infile:
    script = infile.read()

flag_start = '<flags>'
flag_end = '</flags>'

# Coded dynamically to change later if needed
code_start = '<code>'
code_end = '</code>'
md_start = '<md>'
md_end = '</md>'


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
    # Generate regexs for eventual extraction between tags
    # (?s) - to match over multiple lines - the rest is to match code between code tags
    code_tags_regex = '(?s)(?<=' + code_start +')(.*?)(?=' + code_end + ')'
    md_tags_regex = '(?s)(?<=' + md_start +')(.*?)(?=' + md_end + ')'
    code_blocks = re.findall(code_tags_regex, script)
    md_blocks = re.findall(md_tags_regex, script)
    infile = open(input_file_name, "r")
    block_order = validation(infile)
    infile.close()


cell_array = []
code_index = 0
md_index = 0
for block in range(0,len(block_order)):
    if block_order[block] == 'code':
        one_code_cell = {'cell_type': 'code', 'collapsed': False, 'language': lang,'metadata': {},'outputs': [] }
        one_code_cell.update({'input':code_blocks[code_index]})
        cell_array.append(one_code_cell)
        code_index += 1
    else:
        one_md_cell = {'cell_type': 'markdown', 'metadata': {}}
        one_md_cell.update({'source':md_blocks[md_index]})
        cell_array.append(one_md_cell)
        md_index += 1


obj = {'metadata': {'name': ''}, 'nbformat': 3,'nbformat_minor': 0,'worksheets': [{"cells": cell_array}]}

outfile = open(output_file_name, "w")

outfile.write(json.dumps(obj, indent = 4))

outfile.close()


