import sublime_plugin, sublime, os
 
class Txt2pynbCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        run_string = 'python ' + "'" + sublime.packages_path() + "'" + '/txt2pynb/txt2pynb.py'+ ' ' + "'" + self.view.file_name() + "'"
        os.system(run_string)
