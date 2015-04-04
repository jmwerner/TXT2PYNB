import sublime_plugin
import sublime

if sublime.version() >= '3000':
    from .txt2pynb import txt2pynb
else:
    from txt2pynb import txt2pynb


class txt2pynbCommand(sublime_plugin.WindowCommand):
    def run(self):

        view = self.window.active_view()
        input_file_path = view.file_name()

        if input_file_path is None or view.is_dirty():
            sublime.error_message(
                "ERROR: Current buffer must be saved prior to building "
                "iPython notebook with TXT2PYNB"
            )
            return

        outfile_split = input_file_path.split('.')
        output_file_path = outfile_split[0] + '.ipynb'
        txt2pynb(input_file_path, output_file_path)
        sublime.status_message("TXT2PYNB Complete")
