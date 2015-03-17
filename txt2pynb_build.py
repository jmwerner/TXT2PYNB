import sublime_plugin, sublime, json
import txt2pynb_functions as lib
 
class txt2pynbCommand(sublime_plugin.WindowCommand):
    def run(self, cmd="", file_regex="", path=""):
        
        view = self.window.active_view()
        root = view.file_name()

        if root is None:
            sublime.error_message("ERROR: Current buffer must be saved prior to building iPython notebook")
        else:
            base_language, output_path = lib.pre_process(root)

            with open(root, 'r') as infile:
                full_script = infile.read()

            parsed_blocks, parsed_order = lib.split_function(full_script)
            cell_array = lib.create_cell_array(parsed_blocks, parsed_order, base_language)
            obj = {'metadata': {'name': ''}, 'nbformat': 3,'nbformat_minor': 0,'worksheets': [{"cells": cell_array}]}
            
            outfile = open(output_path, "w")
            outfile.write(json.dumps(obj, indent = 4))
            outfile.close()

            sublime.status_message("TXT2PYNB Complete")