import sublime
import sublime_plugin
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ToggleDiredSidebarCommand(sublime_plugin.WindowCommand):
    def run(self):
        logger.debug("Starting ToggleDiredSidebarCommand")
        
        try:
            # Store the currently active view
            current_view = self.window.active_view()
            
            # Check if FileBrowser view exists
            file_browser_view = None
            for view in self.window.views():
                if "FileBrowser" in view.settings().get("syntax", ""):
                    file_browser_view = view
                    break
            
            if file_browser_view:
                logger.debug("Found FileBrowser view - closing it")
                file_browser_view.close()
            else:
                logger.debug("Opening new FileBrowser")
                self.window.run_command("dired", {
                    "immediate": True,
                    "single_pane": True,
                    "other_group": "left"
                })
            
            # Restore focus to the original view
            if current_view and current_view.is_valid():
                sublime.set_timeout(lambda: self.window.focus_view(current_view), 10)
                
        except Exception as e:
            logger.error(f"Error in ToggleDiredSidebarCommand: {str(e)}")

class FocusFileBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        logger.debug("Starting FocusFileBrowserCommand")
        
        try:
            # Find FileBrowser view
            file_browser_view = None
            for view in self.window.views():
                if "FileBrowser" in view.settings().get("syntax", ""):
                    file_browser_view = view
                    break
            
            if file_browser_view:
                logger.debug("Found FileBrowser view - focusing it")
                self.window.focus_view(file_browser_view)
            else:
                logger.debug("No FileBrowser view found - creating one")
                self.window.run_command("dired", {
                    "immediate": True,
                    "single_pane": True,
                    "other_group": "left"
                })
                
        except Exception as e:
            logger.error(f"Error in FocusFileBrowserCommand: {str(e)}")
