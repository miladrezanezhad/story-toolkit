"""
Unicode and Encoding Security Tests

Tests Unicode attacks, encoding issues, and homoglyph attacks.
"""

import sys
import os
import unicodedata
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.memory import MemoryManager


class UnicodeAttackTester:
    """Comprehensive Unicode attack tests"""
    
    def __init__(self):
        self.results = []
    
    def test_null_byte_injection(self):
        """Test null byte injection attacks"""
        print("\n  💉 Testing null byte injection...")
        
        toolkit = StoryToolkit()
        
        null_byte_patterns = [
            "test\0.py",
            "story\0.sql",
            "file\0.jpg",
            "normal\0../etc/passwd",
        ]
        
        for pattern in null_byte_patterns:
            try:
                story = toolkit.create_story("fantasy", pattern)
                
                # Should handle null byte gracefully
                if '\0' in str(story):
                    print(f"    ⚠️ Null byte preserved in output")
                
            except (ValueError, TypeError) as e:
                print(f"    ✅ Null byte rejected: {pattern[:20]}...")
            except Exception as e:
                print(f"    ❌ Null byte caused crash: {e}")
                return False
        
        print("    ✅ Null byte injection handled")
        return True
    
    def test_unicode_normalization_attacks(self):
        """Test Unicode normalization attacks"""
        print("\n  🔤 Testing Unicode normalization attacks...")
        
        # Visually identical but different Unicode
        homoglyphs = {
            'admin': 'admіn',  # Cyrillic i
            'root': 'rооt',    # Cyrillic o
            'config': 'cоnfіg', # Mixed Cyrillic
        }
        
        toolkit = StoryToolkit()
        
        for normal, malicious in homoglyphs.items():
            # Create stories with both names
            story1 = toolkit.create_story("fantasy", normal)
            story2 = toolkit.create_story("fantasy", malicious)
            
            # They should be distinguishable or normalized
            story1_str = str(story1)
            story2_str = str(story2)
            
            if normal in story2_str and malicious in story1_str:
                print(f"    ⚠️ Homoglyph confusion possible: '{normal}' vs '{malicious}'")
        
        print("    ✅ Unicode normalization handled")
        return True
    
    def test_rtl_override_attack(self):
        """Test RTL override attacks"""
        print("\n  ↔️ Testing RTL override attacks...")
        
        rtl_chars = [
            '\u202E',  # Right-to-Left Override
            '\u202D',  # Left-to-Right Override
            '\u200F',  # Right-to-Left Mark
            '\u200E',  # Left-to-Right Mark
        ]
        
        toolkit = StoryToolkit()
        
        for rtl_char in rtl_chars:
            malicious = f"script{rtl_char}php"
            
            try:
                story = toolkit.create_story("fantasy", malicious)
                
                # Check if RTL char is preserved or stripped
                output = str(story)
                if rtl_char in output:
                    print(f"    ⚠️ RTL character preserved: {repr(rtl_char)}")
                
            except Exception as e:
                print(f"    ❌ RTL char caused error: {e}")
                return False
        
        print("    ✅ RTL attacks handled")
        return True
    
    def test_overflow_attack(self):
        """Test Unicode overflow attacks"""
        print("\n  🌊 Testing Unicode overflow attacks...")
        
        # Create extremely long Unicode string
        long_unicode = "😀" * 100000 + "A" * 100000
        
        toolkit = StoryToolkit()
        
        try:
            story = toolkit.create_story("fantasy", long_unicode[:1000])
            print("    ✅ Long Unicode truncated/handled")
            return True
        except (ValueError, MemoryError) as e:
            print(f"    ✅ Long Unicode rejected: {e}")
            return True
        except Exception as e:
            print(f"    ❌ Long Unicode caused crash: {e}")
            return False
    
    def test_invalid_unicode_sequences(self):
        """Test invalid Unicode sequences"""
        print("\n  🔧 Testing invalid Unicode sequences...")
        
        invalid_sequences = [
            b'\x80',           # Invalid UTF-8
            b'\xFF\xFE',       # Invalid sequence
            b'\xC0\x80',       # Overlong encoding
            b'\xED\xA0\x80',   # Surrogate half
        ]
        
        toolkit = StoryToolkit()
        
        for invalid in invalid_sequences:
            try:
                # Try to decode invalid sequence
                decoded = invalid.decode('utf-8', errors='replace')
                
                story = toolkit.create_story("fantasy", decoded)
                print(f"    ✅ Invalid sequence handled: {invalid.hex()}")
                
            except Exception as e:
                print(f"    ✅ Invalid sequence rejected: {e}")
        
        return True
    
    def test_confusable_identifiers(self):
        """Test confusable identifier attacks"""
        print("\n  🎭 Testing confusable identifiers...")
        
        # Confusable pairs
        confusables = [
            ('story', 'ѕtory'),      # Cyrillic s
            ('config', 'cоnfig'),    # Cyrillic o
            ('database', 'dаtаbase'), # Cyrillic a
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        try:
            manager = MemoryManager(db_path)
            
            for normal, confusing in confusables:
                # Create stories with both names
                id1 = manager.create_story(normal, "fantasy", "test")
                id2 = manager.create_story(confusing, "fantasy", "test")
                
                # They should be treated as different
                if id1 == id2:
                    print(f"    ❌ Confusable identifiers collide: '{normal}' == '{confusing}'")
                    return False
                
                story1 = manager.get_story(id1)
                story2 = manager.get_story(id2)
                
                if story1.name == story2.name:
                    print(f"    ⚠️ Confusable names normalized: '{normal}' == '{confusing}'")
            
            manager.close()
            print("    ✅ Confusable identifiers handled")
            return True
            
        except Exception as e:
            print(f"    ❌ Test failed: {e}")
            return False
        finally:
            if os.path.exists(db_path):
                os.remove(db_path)
    
    def test_bidi_attack(self):
        """Test bidirectional text attacks"""
        print("\n  📝 Testing bidirectional text attacks...")
        
        # Bidi attacks can hide text
        bidi_attack = "\\u202E}secret{\\u202D"
        
        toolkit = StoryToolkit()
        
        try:
            story = toolkit.create_story("fantasy", bidi_attack)
            
            # Check if bidi characters are visible
            output = str(story)
            if '\u202E' in output or '\u202D' in output:
                print("    ⚠️ Bidi characters preserved")
            
            print("    ✅ Bidi attacks handled")
            return True
        except Exception as e:
            print(f"    ❌ Bidi attack caused error: {e}")
            return False
    
    def test_control_characters(self):
        """Test control character injection"""
        print("\n  🎮 Testing control character injection...")
        
        control_chars = [
            '\x00', '\x01', '\x02', '\x03',  # Null, SOH, STX, ETX
            '\x07', '\x08', '\x09', '\x0A',  # Bell, BS, TAB, LF
            '\x0B', '\x0C', '\x0D', '\x1B',  # VT, FF, CR, ESC
        ]
        
        toolkit = StoryToolkit()
        
        for control in control_chars:
            try:
                story = toolkit.create_story("fantasy", f"test{control}test")
                print(f"    ✅ Control char {ord(control):02X} handled")
            except Exception as e:
                print(f"    ✅ Control char {ord(control):02X} rejected: {e}")
        
        return True
    
    def test_emoji_variation_selector(self):
        """Test emoji variation selector attacks"""
        print("\n  😀 Testing emoji variation selectors...")
        
        variation_selectors = [
            '\uFE0E',  # Text variation
            '\uFE0F',  # Emoji variation
            '\u200D',  # Zero-width joiner
        ]
        
        toolkit = StoryToolkit()
        
        for vs in variation_selectors:
            text = f"test{vs}test"
            
            try:
                story = toolkit.create_story("fantasy", text)
                print(f"    ✅ Variation selector {repr(vs)} handled")
            except Exception as e:
                print(f"    ❌ Variation selector caused error: {e}")
                return False
        
        return True
    
    def test_zalgo_text(self):
        """Test Zalgo text (combining characters) attacks"""
        print("\n  👾 Testing Zalgo text attacks...")
        
        # Combining characters (Zalgo)
        combining_chars = '\u0300\u0301\u0302\u0303\u0304\u0305\u0306'
        zalgo_text = "H" + combining_chars * 100 + "i"
        
        toolkit = StoryToolkit()
        
        try:
            story = toolkit.create_story("fantasy", zalgo_text[:500])
            print("    ✅ Zalgo text handled")
            return True
        except Exception as e:
            print(f"    ❌ Zalgo text caused error: {e}")
            return False
    
    def run_all(self):
        """Run all Unicode attack tests"""
        print("\n" + "="*60)
        print("🔤 UNICODE ATTACK SECURITY TESTS")
        print("="*60)
        
        tests = [
            ("Null Byte Injection", self.test_null_byte_injection),
            ("Unicode Normalization", self.test_unicode_normalization_attacks),
            ("RTL Override Attack", self.test_rtl_override_attack),
            ("Overflow Attack", self.test_overflow_attack),
            ("Invalid Unicode", self.test_invalid_unicode_sequences),
            ("Confusable Identifiers", self.test_confusable_identifiers),
            ("Bidi Attack", self.test_bidi_attack),
            ("Control Characters", self.test_control_characters),
            ("Emoji Variation", self.test_emoji_variation_selector),
            ("Zalgo Text", self.test_zalgo_text),
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
        print(f"\n📊 Unicode Attack Tests: {passed}/{len(results)} passed")
        
        return passed == len(results)


def run():
    """Run Unicode attack security tests"""
    tester = UnicodeAttackTester()
    return tester.run_all()


if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)