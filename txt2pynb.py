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

def strip_one(block_in):
    # Strip leading and trailing '\n' and '#' characters
    block_out = block_in.rstrip('#')
    block_out = block_out.strip('\n')
    # Remove extra tabs (for people who indent within the raw code blocks) 
    #  while preserving the appropriate amount of tabs within loops and other constructs
    tab_match = re.match('\t+', block_out)
    if tab_match is not None:
        block_out = block_out.strip(tab_match.group(0))
        block_out = re.sub('\n' + tab_match.group(0), '\n', block_out)
    return block_out;

with open(input_file_name, 'r') as infile:
    script = infile.read()

flag_start = '<flags>'
flag_end = '</flags>'

# Coded dynamically to change later if needed
code_start = '<code>'
code_end = '</code>'
md_start = '<md>'
md_end = '</md>'


block_order = []
all_blocks = []

flag_tags_regex = '(?s)(?<=' + flag_start +')(.*?)(?=' + flag_end + ')'
md_block_regex = '(?s)(?<=(\'\'\'|\"\"\"))(.*?)(?=(\'\'\'|\"\"\"))'
flag_block = re.findall(flag_tags_regex, script)
if len(flag_block) > 0:
    if flag_block[0] == 'double_space_delimiter':
        flag_strip = re.search('(?s)(?<=' + flag_end + ')(.*)', script)
        newscript = flag_strip.group()
        # Splits on two or more \n
        splits = re.split(r'[\n]{3,}', newscript)
        for block in range(0, len(splits)):
            if splits[block] != '':
                str_tester = re.search(md_block_regex, splits[block])
                if str_tester:
                    content = str_tester.group()
                    all_blocks.append(content)
                    block_order.append('md')
                else:
                    all_blocks.append(splits[block])
                    block_order.append('code')
else:
    script_splits = re.split('(' + code_start + '|' + md_start + '|' + code_end + '|' + md_end + ')', script)
    for chunk in range(0, len(script_splits)):
        if script_splits[chunk] == code_start and script_splits[chunk + 2] == code_end:
            block_order.append('code')
            all_blocks.append(script_splits[chunk + 1])
        if script_splits[chunk] == md_start and script_splits[chunk + 2] == md_end:
            block_order.append('md')
            all_blocks.append(script_splits[chunk + 1])


cell_array = []
for block in range(0,len(block_order)):
    if block_order[block] == 'code':
        one_code_cell = {'cell_type': 'code', 'collapsed': False, 'language': lang,'metadata': {},'outputs': [] }
        stripped_cell = strip_one(all_blocks[block])
        one_code_cell.update({'input':stripped_cell})
        cell_array.append(one_code_cell)
        # code_index += 1
    else:
        one_md_cell = {'cell_type': 'markdown', 'metadata': {}}
        stripped_cell = strip_one(all_blocks[block])
        one_md_cell.update({'source':stripped_cell})
        cell_array.append(one_md_cell)
        # md_index += 1


obj = {'metadata': {'name': ''}, 'nbformat': 3,'nbformat_minor': 0,'worksheets': [{"cells": cell_array}]}

outfile = open(output_file_name, "w")

outfile.write(json.dumps(obj, indent = 4))

outfile.close()
