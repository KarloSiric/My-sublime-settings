import sublime
import sublime_plugin
import os

# Nerd Font icon mappings
NERD_FONT_ICONS = {
    # Folders
    'folder': '',
    'folder_open': '',
    
    # Common file types
    'default_file': '',
    'py': '',
    'js': '',
    'html': '',
    'css': '',
    'json': '',
    'md': '',
    'img': '',
    'git': '',
    'archive': '',
    'pdf': '',
    'lock': '',
    'config': '',
}

# File extension mappings
FILE_TYPES = {
    # Programming
    '.py': 'py',
    '.js': 'js',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    
    # Documentation
    '.md': 'md',
    '.pdf': 'pdf',
    
    # Images
    '.png': 'img',
    '.jpg': 'img',
    '.jpeg': 'img',
    '.gif': 'img',
    
    # Git
    '.git': 'git',
    '.gitignore': 'git',
    
    # Archives
    '.zip': 'archive',
    '.tar': 'archive',
    '.gz': 'archive',
    
    # Config
    '.conf': 'config',
    '.config': 'config',
    '.yml': 'config',
    '.yaml': 'config',
}

class FileIconProvider:
    @staticmethod
    def get_icon(file_path):
        """Get the appropriate nerd font icon for a file path."""
        if os.path.isdir(file_path):
            return NERD_FONT_ICONS['folder']
            
        _, ext = os.path.splitext(file_path)
        file_type = FILE_TYPES.get(ext.lower(), 'default_file')
        return NERD_FONT_ICONS.get(file_type, NERD_FONT_ICONS['default_file'])

class FileBrowserIconCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Update the file browser view with icons."""
        view = self.view
        icon_provider = FileIconProvider()
        
        # Iterate through lines in the view
        for region in view.lines(sublime.Region(0, view.size())):
            line_text = view.substr(region)
            file_path = line_text.strip()
            
            if file_path:
                # Get icon for the file
                icon = icon_provider.get_icon(file_path)
                
                # Insert icon at the beginning of the line
                icon_point = region.begin()
                view.insert(edit, icon_point, f"{icon} ")

class FileBrowserListener(sublime_plugin.EventListener):
    def on_load(self, view):
        """Add icons when a file browser view is loaded."""
        if 'file_browser' in view.settings().get('syntax', '').lower():
            view.run_command('file_browser_icon')
