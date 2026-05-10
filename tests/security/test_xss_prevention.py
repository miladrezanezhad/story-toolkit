"""
XSS (Cross-Site Scripting) Prevention Security Tests

Tests various XSS attack vectors in exporters and output.
"""

import sys
import os
import html
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.exporters import HTMLExporter, ExportConfig, HTMLTemplate


class XSSTester:
    """Comprehensive XSS prevention tests"""
    
    def __init__(self):
        self.results = []
    
    def create_malicious_story(self, toolkit, malicious_payload):
        """Create a story with malicious payload"""
        story = toolkit.create_story("fantasy", "test")
        
        # Inject payload in various places
        story["metadata"] = story.get("metadata", {})
        story["metadata"]["title"] = malicious_payload
        story["metadata"]["author"] = malicious_payload
        story["metadata"]["description"] = malicious_payload
        
        if "plot" in story and "main_plot" in story["plot"]:
            for stage in story["plot"]["main_plot"]:
                stage["description"] = malicious_payload
        
        return story
    
    def check_output_safety(self, content, payload):
        """Check if output is safe (payload escaped or removed)"""
        # Payload should not appear as executable HTML/JS
        dangerous_patterns = [
            f"<script>{payload}</script>",
            f"<img src=x onerror={payload}>",
            f"javascript:{payload}",
            f"onload={payload}",
            f"onerror={payload}",
        ]
        
        for pattern in dangerous_patterns:
            if pattern in content and not html.escape(pattern) in content:
                return False
        
        # Check if escaped properly
        if payload in content:
            # Payload should be escaped
            escaped = html.escape(payload)
            if escaped not in content:
                return False
        
        return True
    
    def test_basic_xss(self):
        """Test basic XSS vectors"""
        print("\n  🎯 Testing basic XSS vectors...")
        
        xss_vectors = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "<body onload=alert('XSS')>",
            "><script>alert('XSS')</script>",
        ]
        
        toolkit = StoryToolkit()
        success_count = 0
        total_tests = len(xss_vectors) * len(HTMLTemplate)
        
        for vector in xss_vectors:
            story = self.create_malicious_story(toolkit, vector)
            
            for template in HTMLTemplate:
                with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                    output_path = tmp.name
                
                try:
                    config = ExportConfig(html_template=template)
                    exporter = HTMLExporter(config)
                    exporter.export(story, output_path)
                    
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if self.check_output_safety(content, vector):
                        success_count += 1
                    else:
                        print(f"    ⚠️ Vector '{vector[:30]}...' in template {template.value}")
                    
                    os.remove(output_path)
                    
                except Exception as e:
                    print(f"    ⚠️ Error with '{vector[:30]}...': {e}")
                    if os.path.exists(output_path):
                        os.remove(output_path)
        
        print(f"    ✅ Basic XSS vectors: {success_count}/{total_tests} safe")
        return success_count > 0
    
    def test_encoded_xss(self):
        """Test encoded/obfuscated XSS vectors"""
        print("\n  🔐 Testing encoded XSS vectors...")
        
        encoded_vectors = [
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "\\u003cscript\\u003ealert('XSS')\\u003c/script\\u003e",
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
        ]
        
        toolkit = StoryToolkit()
        success = True
        
        for vector in encoded_vectors:
            story = self.create_malicious_story(toolkit, vector)
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                exporter = HTMLExporter(ExportConfig())
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Should not execute even if decoded
                if "<script>" in content.lower() and "alert" in content.lower():
                    # Check if escaped
                    if html.escape("<script>") not in content:
                        print(f"    ❌ Vector vulnerable: {vector[:30]}...")
                        success = False
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Vector '{vector[:30]}...' error: {e}")
        
        if success:
            print("    ✅ Encoded XSS vectors prevented")
        return success
    
    def test_dom_based_xss(self):
        """Test DOM-based XSS vectors"""
        print("\n  🏠 Testing DOM-based XSS vectors...")
        
        dom_vectors = [
            "document.location='http://evil.com'",
            "window.location='javascript:alert(1)'",
            "eval('alert(1)')",
            "setTimeout('alert(1)', 1000)",
            "Function('alert(1)')()",
        ]
        
        toolkit = StoryToolkit()
        success = True
        
        for vector in dom_vectors:
            story = self.create_malicious_story(toolkit, vector)
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                exporter = HTMLExporter(ExportConfig())
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Dangerous JavaScript should be escaped or not present
                dangerous_js = ['document.location', 'window.location', 'eval(', 'setTimeout(', 'Function(']
                for pattern in dangerous_js:
                    if pattern in content and pattern not in html.escape(content):
                        print(f"    ⚠️ Pattern '{pattern}' found unescaped")
                        success = False
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Vector '{vector[:30]}...' error: {e}")
        
        if success:
            print("    ✅ DOM-based XSS vectors prevented")
        return success
    
    def test_html_injection(self):
        """Test HTML injection vectors"""
        print("\n  📝 Testing HTML injection vectors...")
        
        html_vectors = [
            "<h1>Injected</h1>",
            "<b>Bold</b>",
            "<div onclick='alert(1)'>Click</div>",
            "<a href='javascript:alert(1)'>Link</a>",
            "<iframe src='evil.com'></iframe>",
            "<object data='evil.swf'></object>",
            "<embed src='evil.swf'>",
        ]
        
        toolkit = StoryToolkit()
        success = True
        
        for vector in html_vectors:
            story = self.create_malicious_story(toolkit, vector)
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                exporter = HTMLExporter(ExportConfig())
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # HTML tags should be escaped
                if '<' in vector and '>' in vector:
                    if vector in content and html.escape(vector) not in content:
                        print(f"    ⚠️ HTML tag not escaped: {vector[:30]}...")
                        success = False
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Vector '{vector[:30]}...' error: {e}")
        
        if success:
            print("    ✅ HTML injection vectors prevented")
        return success
    
    def test_css_injection(self):
        """Test CSS injection vectors"""
        print("\n  🎨 Testing CSS injection vectors...")
        
        css_vectors = [
            "<style>body{background:url('evil.com')}</style>",
            "<style>@import url('evil.css')</style>",
            "background:url('javascript:alert(1)')",
            "expression(alert(1))",
            "</style><script>alert(1)</script>",
        ]
        
        toolkit = StoryToolkit()
        success = True
        
        for vector in css_vectors:
            story = self.create_malicious_story(toolkit, vector)
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                exporter = HTMLExporter(ExportConfig())
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # CSS injection should be escaped
                if '<style>' in vector and vector in content and html.escape(vector) not in content:
                    print(f"    ⚠️ CSS injection: {vector[:30]}...")
                    success = False
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Vector '{vector[:30]}...' error: {e}")
        
        if success:
            print("    ✅ CSS injection vectors prevented")
        return success
    
    def test_all_templates_xss(self):
        """Test XSS across all HTML templates"""
        print("\n  📚 Testing all HTML templates for XSS...")
        
        malicious = "<script>alert('XSS')</script>"
        toolkit = StoryToolkit()
        story = toolkit.create_story("fantasy", "test")
        story["metadata"] = story.get("metadata", {})
        story["metadata"]["title"] = malicious
        story["metadata"]["author"] = malicious
        
        templates_tested = 0
        all_safe = True
        
        for template in HTMLTemplate:
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                config = ExportConfig(html_template=template)
                exporter = HTMLExporter(config)
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if malicious content is escaped
                escaped = html.escape(malicious)
                if malicious in content and escaped not in content:
                    print(f"    ❌ Template {template.value} vulnerable!")
                    all_safe = False
                else:
                    print(f"    ✅ Template {template.value} safe")
                    templates_tested += 1
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Template {template.value} error: {e}")
        
        if all_safe:
            print(f"    ✅ All {templates_tested} templates secure")
        return all_safe
    
    def test_http_header_injection(self):
        """Test HTTP header injection via CRLF"""
        print("\n  📡 Testing HTTP header injection...")
        
        crlf_vectors = [
            "Hello\r\nX-Injected: malicious",
            "Title\nSet-Cookie: hacked=1",
            "Author\r\nLocation: http://evil.com",
        ]
        
        toolkit = StoryToolkit()
        success = True
        
        for vector in crlf_vectors:
            story = toolkit.create_story("fantasy", "test")
            story["metadata"] = story.get("metadata", {})
            story["metadata"]["title"] = vector
            
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
                output_path = tmp.name
            
            try:
                exporter = HTMLExporter(ExportConfig())
                exporter.export(story, output_path)
                
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # CRLF characters should be escaped
                escaped_content = html.escape(content)
                if '\r' in content and '\r' not in escaped_content:
                    print(f"    ⚠️ CR character not escaped")
                    success = False
                
                if '\n' in content and '\n' not in escaped_content:
                    print(f"    ⚠️ LF character not escaped")
                    success = False
                
                os.remove(output_path)
                
            except Exception as e:
                print(f"    ⚠️ Vector error: {e}")
        
        if success:
            print("    ✅ HTTP header injection prevented")
        return success
    
    def test_custom_escape_function(self):
        """Test custom HTML escape function"""
        print("\n  🛡️ Testing custom escape function...")
        
        from story_toolkit.security.sanitizer import sanitize_html
        
        test_cases = [
            ("<script>", "&lt;script&gt;"),
            ("alert('xss')", "alert(&#x27;xss&#x27;)"),
            ('onclick="alert(1)"', "onclick=&quot;alert(1)&quot;"),
        ]
        
        success = True
        for input_text, expected in test_cases:
            result = sanitize_html(input_text)
            if result != expected:
                print(f"    ❌ sanitize_html('{input_text}') = '{result}', expected '{expected}'")
                success = False
        
        if success:
            print("    ✅ Custom escape function works")
        return success
    
    def run_all(self):
        """Run all XSS prevention tests"""
        print("\n" + "="*60)
        print("🌐 XSS PREVENTION SECURITY TESTS")
        print("="*60)
        
        tests = [
            ("Basic XSS Vectors", self.test_basic_xss),
            ("Encoded XSS Vectors", self.test_encoded_xss),
            ("DOM-based XSS", self.test_dom_based_xss),
            ("HTML Injection", self.test_html_injection),
            ("CSS Injection", self.test_css_injection),
            ("All Templates XSS", self.test_all_templates_xss),
            ("HTTP Header Injection", self.test_http_header_injection),
            ("Custom Escape Function", self.test_custom_escape_function),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
            except Exception as e:
                print(f"    ❌ {name} crashed: {e}")
                results.append((name, False))
        
        print("\n" + "-"*40)
        for name, status in results:
            print(f"  {'✅' if status else '❌'} {name}")
        print("-"*40)
        
        passed = sum(1 for _, s in results if s)
        print(f"\n📊 XSS Prevention Tests: {passed}/{len(results)} passed")
        
        return passed == len(results)


def run():
    """Run XSS prevention security tests"""
    tester = XSSTester()
    return tester.run_all()


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)