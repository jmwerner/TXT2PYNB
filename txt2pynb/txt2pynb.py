import re
import sys
import json
import codecs

code_start = '<code>'
code_end = '</code>'
md_start = '<md>'
md_end = '</md>'


def space_or_not(script_in):
    return not ((code_start in script_in) or (md_start in script_in))


def strip_one_block(block_in, celltype):
    if celltype == 'code':
        # Strip tailing '#' character(s)
        block_out = block_in.rstrip('#')
        # Strip tailing tab or spaces to ensure '\n' gets stripped next
        block_out = block_out.rstrip('[\t| ]')
        # Strip leading and tailing '\n'
        block_out = block_out.strip('\n')
    else:
        block_out = block_in.strip('\n')
    # Remove extra tabs (for people who indent within the raw code blocks)
    #  while preserving the appropriate amount of tabs within loops and other constructs. Also
    #  sees 4 spaces as tabs in accordance with the pep8 style guide
    tab_match = re.match('[\t|    ]+', block_out)
    if tab_match is not None:
        block_out = block_out.strip(tab_match.group(0))
        block_out = re.sub('\n' + tab_match.group(0), '\n', block_out)
    return block_out


def create_cell_array(all, order, lang):
    output = []
    for block in range(0, len(order)):
        if order[block] == 'code':
            one_code_cell = {
                'cell_type': 'code',
                'collapsed': False,
                'language': lang,
                'metadata': {},
                'outputs': []
            }
            stripped_cell = strip_one_block(all[block], 'code')
            one_code_cell.update({'input': stripped_cell})
            output.append(one_code_cell)
        else:
            one_md_cell = {'cell_type': 'markdown', 'metadata': {}}
            stripped_cell = strip_one_block(all[block], 'md')
            one_md_cell.update({'source': stripped_cell})
            output.append(one_md_cell)
    return output


def split_function(spaces, script):
    block_order = []
    all_blocks = []
    if spaces:
        # Splits on two or more \n
        splits = re.split(r'[\n]{3,}', script)
        for block in range(0, len(splits)):
            if splits[block] != '':
                str_tester = re.search('(?s)(?<=(\'\'\'|\"\"\"))(.*?)(?=(\'\'\'|\"\"\"))',
                                       splits[block])
                if str_tester:
                    content = str_tester.group()
                    all_blocks.append(content)
                    block_order.append('md')
                    # Remove leading and trailing whitespace, then split on ''' or """
                    # to find if md and code block are fused together
                    str_split_compressed_blocks = re.split('(\'\'\'|\"\"\")', splits[block].strip())
                    last_chunk = str_split_compressed_blocks[-1]
                    if last_chunk != '':
                        last_chunk = re.sub('^[ ]{1}', '', last_chunk)
                        all_blocks.append(last_chunk)
                        block_order.append('code')
                else:
                    all_blocks.append(splits[block])
                    block_order.append('code')
    else:
        script_splits = re.split(
            '(' + code_start + '|' + md_start + '|' + code_end + '|' + md_end + ')',
            script
        )
        for chunk in range(0, len(script_splits)):
            if script_splits[chunk] == code_start and script_splits[chunk + 2] == code_end:
                block_order.append('code')
                all_blocks.append(script_splits[chunk + 1])
            if script_splits[chunk] == md_start and script_splits[chunk + 2] == md_end:
                block_order.append('md')
                all_blocks.append(script_splits[chunk + 1])
    return all_blocks, block_order


def txt2pynb(input_file_name, output_file_name):

    if input_file_name.endswith('py'):
        lang = 'python'
    else:
        lang = 'julia'

    with codecs.open(input_file_name, 'r', encoding="utf8") as infile:
        full_script = infile.read()

    space_flag = space_or_not(full_script)

    parsed_blocks, parsed_order = split_function(space_flag, full_script)

    cell_array = create_cell_array(parsed_blocks, parsed_order, lang)

    obj = {
        'metadata': {'name': ''},
        'nbformat': 3,
        'nbformat_minor': 0,
        'worksheets': [{"cells": cell_array}]
    }

    outfile = codecs.open(output_file_name, "w", encoding="utf-8")
    outfile.write(json.dumps(obj, indent=4, ensure_ascii=False))
    outfile.close()


if __name__ == "__main__":

    # args are parser file name [0] and path to python file to parse [1]
    args = sys.argv

    input_file_name = args[1]
    outfile_split = args[1].split('.')
    output_file_name = outfile_split[0] + '.ipynb'
    txt2pynb(input_file_name, output_file_name)
