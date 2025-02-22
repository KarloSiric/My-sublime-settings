import sublime
import sublime_plugin

class SuppressSaveMessageListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        sublime.status_message("")