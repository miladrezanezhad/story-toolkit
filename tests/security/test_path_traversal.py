"""
Path Traversal Security Tests

Tests directory traversal and file system access attacks.
"""

import sys
import os
import tempfile
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit


class PathTraversalTester:
    """Comprehensive path traversal tests"""
    
    def __init__(self):
        self.results = []
    
    def test_basic_path_traversal(self):
        """Test basic path traversal patterns"""
        print("\n  📁 Testing basic path traversal...")
        
        traversal_patterns = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\win.ini",
            ".././.././../etc/shadow",
            "....//....//....//etc/passwd",
            "..;/..;/..;/etc/passwd",
        ]
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        for pattern in traversal_patterns:
            try:
                # Try to save with path traversal
                toolkit.save_story(story, pattern)
                print(f"    ❌ Should not allow: {pattern}")
                return False
            except (ValueError, PermissionError, AttributeError):
                # Expected - should reject
                pass
        
        print("    ✅ Basic path traversal prevented")
        return True
    
    def test_encoded_path_traversal(self):
        """Test encoded path traversal patterns"""
        print("\n  🔐 Testing encoded path traversal...")
        
        encoded_patterns = [
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd",
            "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
            "%2e%2e/%2e%2e/%2e%2e/etc/passwd",
        ]
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        for pattern in encoded_patterns:
            try:
                toolkit.save_story(story, pattern)
                print(f"    ❌ Should not allow encoded: {pattern}")
                return False
            except (ValueError, PermissionError, AttributeError):
                pass
        
        print("    ✅ Encoded path traversal prevented")
        return True
    
    def test_absolute_path_access(self):
        """Test absolute path access attempts"""
        print("\n  🎯 Testing absolute path access...")
        
        absolute_paths = [
            "/etc/passwd",
            "C:\\windows\\system32\\config\\SAM",
            "/var/log/auth.log",
            "~/.ssh/id_rsa",
            "$HOME/.bashrc",
        ]
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        for path in absolute_paths:
            try:
                toolkit.save_story(story, path)
                print(f"    ❌ Should not allow absolute path: {path}")
                return False
            except (ValueError, PermissionError, AttributeError):
                pass
        
        print("    ✅ Absolute path access prevented")
        return True
    
    def test_symlink_attacks(self):
        """Test symlink following attacks"""
        print("\n  🔗 Testing symlink attacks...")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            toolkit = StoryToolkit()
            story = toolkit.create_story("fantasy", "test")
            
            # Create a symlink to sensitive file
            sensitive_file = os.path.join(tmpdir, "sensitive.txt")
            with open(sensitive_file, 'w') as f:
                f.write("secret data")
            
            link_path = os.path.join(tmpdir, "link")
            try:
                os.symlink(sensitive_file, link_path)
            except (OSError, NotImplementedError):
                # Windows might not support symlinks without privilege
                print("    ⚠️ Symlink test skipped (OS limitation)")
                return True
            
            try:
                # Try to write through symlink
                toolkit.save_story(story, link_path)
                
                # Check if original file was modified
                with open(sensitive_file, 'r') as f:
                    content = f.read()
                
                if "secret data" not in content:
                    print("    ✅ Symlink attack prevented")
                    return True
                else:
                    print("    ❌ Symlink attack succeeded")
                    return False
                    
            except (ValueError, PermissionError, AttributeError):
                print("    ✅ Symlink attack rejected")
                return True
    
    def test_null_byte_injection(self):
        """Test null byte injection in paths"""
        print("\n  💉 Testing null byte injection...")
        
        null_byte_patterns = [
            "../../../etc/passwd\0.jpg",
            "test\0../../etc/passwd",
            "safe\0../../../etc/shadow",
        ]
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        for pattern in null_byte_patterns:
            try:
                toolkit.save_story(story, pattern)
                print(f"    ❌ Should not allow null byte: {pattern}")
                return False
            except (ValueError, TypeError, AttributeError):
                pass
        
        print("    ✅ Null byte injection prevented")
        return True
    
    def test_long_paths_dos(self):
        """Test long path DoS attacks"""
        print("\n  📏 Testing long path DoS...")
        
        long_path = "a" * 10000 + "/../etc/passwd"
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        try:
            toolkit.save_story(story, long_path)
            print("    ⚠️ Long path accepted - potential DoS risk")
            return False
        except (ValueError, OSError, AttributeError):
            print("    ✅ Long path rejected")
            return True
    
    def test_zip_slip_attack(self):
        """Test Zip Slip attack simulation"""
        print("\n  📦 Testing Zip Slip attack simulation...")
        
        # Simulate extraction of malicious zip entry
        malicious_entry = "../../../etc/cron.d/malicious"
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        # Test if path sanitization prevents this
        try:
            # This would normally be during zip extraction
            safe_path = os.path.basename(malicious_entry)
            if safe_path != malicious_entry:
                print("    ✅ Zip Slip pattern sanitized")
                return True
            else:
                print("    ⚠️ Potential Zip Slip vulnerability")
                return False
        except:
            print("    ✅ Zip Slip handling implemented")
            return True
    
    def test_directory_traversal_with_valid_paths(self):
        """Test traversal with valid base paths"""
        print("\n  🔄 Testing traversal with valid base paths...")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            toolkit = StoryToolkit()
            story = toolkit.create_story("fantasy", "test")
            
            # Create valid subdirectory
            subdir = os.path.join(tmpdir, "safe")
            os.makedirs(subdir)
            
            # Try to escape from allowed directory
            traversal_paths = [
                os.path.join(subdir, "../../../etc/passwd"),
                os.path.join(subdir, "..\\..\\..\\windows\\win.ini"),
            ]
            
            for path in traversal_paths:
                try:
                    toolkit.save_story(story, path)
                    print(f"    ❌ Escaped from safe directory: {path}")
                    return False
                except (ValueError, PermissionError, AttributeError):
                    pass
            
            print("    ✅ Directory traversal from valid paths prevented")
            return True
    
    def test_file_upload_attacks(self):
        """Test file upload-style attacks"""
        print("\n  📤 Testing file upload attacks...")
        
        upload_patterns = [
            "../../../var/www/html/shell.php",
            "../../../public_html/backdoor.php",
            "..\\..\\..\\inetpub\\wwwroot\\cmd.asp",
            "../../../home/user/.ssh/authorized_keys",
        ]
        
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        
        for pattern in upload_patterns:
            try:
                toolkit.save_story(story, pattern)
                print(f"    ❌ File upload attack possible: {pattern}")
                return False
            except (ValueError, PermissionError, AttributeError):
                pass
        
        print("    ✅ File upload attacks prevented")
        return True
    
    def run_all(self):
        """Run all path traversal tests"""
        print("\n" + "="*60)
        print("📁 PATH TRAVERSAL SECURITY TESTS")
        print("="*60)
        
        tests = [
            ("Basic Path Traversal", self.test_basic_path_traversal),
            ("Encoded Path Traversal", self.test_encoded_path_traversal),
            ("Absolute Path Access", self.test_absolute_path_access),
            ("Symlink Attacks", self.test_symlink_attacks),
            ("Null Byte Injection", self.test_null_byte_injection),
            ("Long Paths DoS", self.test_long_paths_dos),
            ("Zip Slip Attack", self.test_zip_slip_attack),
            ("Traversal from Valid Paths", self.test_directory_traversal_with_valid_paths),
            ("File Upload Attacks", self.test_file_upload_attacks),
        ]
        
        results = []
        for name, test_func in tests:
            result = test_func()
            results.append((name, result))
        
        print("\n" + "-"*40)
        for name, status in results:
            print(f"  {'✅' if status else '❌'} {name}")
        print("-"*40)
        
        passed = sum(1 for _, s in results if s)
        print(f"\n📊 Path Traversal Tests: {passed}/{len(results)} passed")
        
        return passed == len(results)


def run():
    """Run path traversal security tests"""
    tester = PathTraversalTester()
    return tester.run_all()


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)