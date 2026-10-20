"""
Security sanitizers for Story Toolkit

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import html
import re
import os
import urllib.parse
from pathlib import Path


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
        if not isinstance(filename, str):
            filename = str(filename)

        filename = filename.replace('\x00', '')
        filename = filename.replace('..', '')
        filename = filename.replace('/', '')
        filename = filename.replace('\\', '')

        # Keep only safe characters
        safe_pattern = r'[^a-zA-Z0-9_.-]'
        return re.sub(safe_pattern, '_', filename)

    @staticmethod
    def sanitize_path(filepath: str, base_dir: str = None) -> str:
        """Ensure path is within base directory and safe from traversal"""
        if not filepath or not isinstance(filepath, str):
            raise ValueError("Filepath must be a non-empty string")

        if '\x00' in filepath:
            raise ValueError("Null byte detected in path")

        decoded = urllib.parse.unquote(filepath)
        if '\x00' in decoded:
            raise ValueError("Null byte detected in decoded path")

        # Disallow explicit traversal patterns
        normalized_parts = decoded.replace('\\', '/').split('/')
        if '..' in normalized_parts or any(p.startswith('..') for p in normalized_parts):
            raise ValueError(f"Path traversal attempt: {filepath}")

        # Check obvious sensitive system root paths
        lower_fp = filepath.lower()
        if lower_fp.startswith(('/etc', '/var', '/root', '/usr', '~', '$', 'c:\\windows', '\\\\')):
            raise ValueError(f"Access to sensitive path blocked: {filepath}")

        if base_dir is None:
            base_dir = os.getcwd()

        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(os.path.join(base_dir, filepath))

        # Check containment via commonpath
        try:
            if os.path.commonpath([abs_base, abs_path]) != abs_base:
                raise ValueError(f"Path traversal attempt: {filepath}")
        except ValueError:
            raise ValueError(f"Path traversal attempt: {filepath}")

        return abs_path

    @staticmethod
    def sanitize_sql(value: str) -> str:
        """Basic SQL sanitization"""
        if not isinstance(value, str):
            value = str(value)

        dangerous = [';', 'DROP', 'DELETE', 'INSERT', 'UPDATE', '--', '/*', '*/']
        result = value
        for pattern in dangerous:
            result = re.sub(re.escape(pattern), '', result, flags=re.IGNORECASE)
        return result

    @staticmethod
    def sanitize_command_arg(arg: str) -> str:
        """Sanitize command line arguments"""
        if not isinstance(arg, str):
            arg = str(arg)

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


def sanitize_path(filepath: str, base_dir: str = None) -> str:
    """Sanitize file path"""
    return SecuritySanitizer.sanitize_path(filepath, base_dir)


def sanitize_sql(value: str) -> str:
    """Sanitize SQL input"""
    return SecuritySanitizer.sanitize_sql(value)


def sanitize_command_arg(arg: str) -> str:
    """Sanitize command argument"""
    return SecuritySanitizer.sanitize_command_arg(arg)
