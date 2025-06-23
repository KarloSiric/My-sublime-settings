# -*- coding: utf-8 -*-
# @Author: karlosiric
# @Date:   2025-02-18 10:47:48
# @Last Modified by:   karlosiric
# @Last Modified time: 2025-02-18 18:43:23

import sublime
import sublime_plugin
import logging
import os
from typing import Optional, Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# File type to icon mapping
FILE_ICONS = {
    # Programming Languages
    '.py': '🐍',
    '.js': '📜',
    '.html': '🌐',
    '.css': '🎨',
    '.json': '📋',
    # Documents
    '.pdf': '📄',
    '.doc': '📝',
    '.docx': '📝',
    '.txt': '📃',
    # Images
    '.jpg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    # Folders
    'folder': '📁',
    'folder_open': '📂',
    # Default
    'default': '📄'
}

class FileViewManager:
    """Manages file browser view operations"""
    
    @staticmethod
    def get_file_browser_view(window) -> Optional[sublime.View]:
        """Find the file browser view if it exists"""
        return next(
            (view for view in window.views() 
             if "FileBrowser" in view.settings().get("syntax", "")),
            None
        )

    @staticmethod
    def get_icon_for_path(path: str) -> str:
        """Get the appropriate icon for a file path"""
        if os.path.isdir(path):
            return FILE_ICONS['folder']
        
        ext = os.path.splitext(path)[1].lower()
        return FILE_ICONS.get(ext, FILE_ICONS['default'])

    @staticmethod
    def create_file_browser(window, settings: Dict = None):
        """Create a new file browser with specified settings"""
        default_settings = {
            "immediate": True,
            "single_pane": True,
            "other_group": "left"
        }
        settings = settings or default_settings
        window.run_command("dired", settings)

class ToggleDiredSidebarCommand(sublime_plugin.WindowCommand):
    def run(self):
        logger.debug("Starting ToggleDiredSidebarCommand")
        
        try:
            # Store current view
            current_view = self.window.active_view()
            
            # Get or close file browser
            file_browser_view = FileViewManager.get_file_browser_view(self.window)
            
            if file_browser_view:
                logger.debug("Closing existing FileBrowser")
                file_browser_view.close()
            else:
                logger.debug("Creating new FileBrowser")
                FileViewManager.create_file_browser(self.window)
            
            # Restore focus with delay
            if current_view and current_view.is_valid():
                sublime.set_timeout(
                    lambda: self.window.focus_view(current_view), 
                    10
                )
                
        except Exception as e:
            logger.error(f"Error in ToggleDiredSidebarCommand: {str(e)}")
            sublime.error_message(f"Error toggling sidebar: {str(e)}")

class FocusFileBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        logger.debug("Starting FocusFileBrowserCommand")
        
        try:
            file_browser_view = FileViewManager.get_file_browser_view(self.window)
            
            if file_browser_view:
                logger.debug("Focusing existing FileBrowser")
                self.window.focus_view(file_browser_view)
            else:
                logger.debug("Creating new FileBrowser")
                FileViewManager.create_file_browser(self.window)
                
        except Exception as e:
            logger.error(f"Error in FocusFileBrowserCommand: {str(e)}")
            sublime.error_message(f"Error focusing file browser: {str(e)}")

class CustomizeFileBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Command to customize file browser appearance"""
        try:
            file_browser_view = FileViewManager.get_file_browser_view(self.window)
            if file_browser_view:
                # Apply custom styling
                settings = file_browser_view.settings()
                settings.set("line_padding_top", 2)
                settings.set("line_padding_bottom", 2)
                settings.set("margin", 8)
                
                # Refresh the view
                file_browser_view.run_command("refresh")
                
        except Exception as e:
            logger.error(f"Error customizing file browser: {str(e)}")
            sublime.error_message(f"Error customizing file browser: {str(e)}") 
