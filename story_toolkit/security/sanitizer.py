"""
Security sanitizers for Story Toolkit

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import html
import re
import os


class SecuritySanitizer:
    """Sanitize inputs to prevent security issues"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML special characters"""
        if not isinstance(text, str):
            text = str(text)
        return html.escape(text, quote=True)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove dangerous characters from filename"""
        # Remove path traversal
        filename = filename.replace('..', '')
        filename = filename.replace('/', '')
        filename = filename.replace('\\', '')
        filename = filename.replace('\x00', '')
        
        # Keep only safe characters
        safe_pattern = r'[^a-zA-Z0-9_.-]'
        return re.sub(safe_pattern, '_', filename)
    
    @staticmethod
    def sanitize_path(filepath: str, base_dir: str = None) -> str:
        """Ensure path is within base directory"""
        if base_dir is None:
            base_dir = os.getcwd()
        
        # Resolve to absolute path
        abs_path = os.path.abspath(os.path.join(base_dir, filepath))
        abs_base = os.path.abspath(base_dir)
        
        # Check if inside base directory
        if not abs_path.startswith(abs_base):
            raise ValueError(f"Path traversal attempt: {filepath}")
        
        return abs_path
    
    @staticmethod
    def sanitize_sql(value: str) -> str:
        """Basic SQL sanitization (though we use parameters)"""
        # Remove dangerous SQL patterns
        dangerous = [';', 'DROP', 'DELETE', 'INSERT', 'UPDATE', '--', "/*", "*/"]
        for pattern in dangerous:
            if pattern.lower() in value.lower():
                value = value.replace(pattern, '')
        return value
    
    @staticmethod
    def sanitize_command_arg(arg: str) -> str:
        """Sanitize command line arguments"""
        # Remove shell metacharacters
        dangerous = ['&', '|', ';', '$', '`', '>', '<', '\n', '\r']
        for char in dangerous:
            arg = arg.replace(char, '')
        return arg


# Shortcut functions for convenience
def sanitize_html(text: str) -> str:
    """Escape HTML special characters"""
    return SecuritySanitizer.sanitize_html(text)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename"""
    return SecuritySanitizer.sanitize_filename(filename)


def sanitize_path(filepath: str) -> str:
    """Sanitize file path"""
    return SecuritySanitizer.sanitize_path(filepath)


def sanitize_sql(value: str) -> str:
    """Sanitize SQL input"""
    return SecuritySanitizer.sanitize_sql(value)


def sanitize_command_arg(arg: str) -> str:
    """Sanitize command argument"""
    return SecuritySanitizer.sanitize_command_arg(arg)