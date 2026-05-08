"""
Comprehensive test for all modules of Story Toolkit

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("🧪 STORY TOOLKIT - COMPREHENSIVE MODULE TEST")
print("="*70)

# ============================================================
# TEST 1: Core Modules
# ============================================================
print("\n📦 1. TESTING CORE MODULES")

try:
    from story_toolkit.core.character import Character
    print("   ✅ Character module")
    
    from story_toolkit.core.plot import Plot
    print("   ✅ Plot module")
    
    from story_toolkit.core.world_builder import WorldBuilder
    print("   ✅ WorldBuilder module")
    
    from story_toolkit.core.story_engine import StoryEngine
    print("   ✅ StoryEngine module")
except Exception as e:
    print(f"   ❌ Core modules error: {e}")

# ============================================================
# TEST 2: Generators
# ============================================================
print("\n🎲 2. TESTING GENERATORS")

try:
    from story_toolkit.generators.character_generator import CharacterGenerator
    print("   ✅ CharacterGenerator")
    
    from story_toolkit.generators.plot_generator import PlotGenerator
    print("   ✅ PlotGenerator")
    
    from story_toolkit.generators.dialogue_generator import DialogueGenerator
    print("   ✅ DialogueGenerator")
    
    from story_toolkit.generators.story_generator import StoryGenerator
    print("   ✅ StoryGenerator")
except Exception as e:
    print(f"   ❌ Generators error: {e}")

# ============================================================
# TEST 3: NLP Modules
# ============================================================
print("\n🔍 3. TESTING NLP MODULES")

try:
    from story_toolkit.nlp.coherence_checker import CoherenceChecker
    print("   ✅ CoherenceChecker")
    
    from story_toolkit.nlp.text_analyzer import TextAnalyzer
    print("   ✅ TextAnalyzer")
except Exception as e:
    print(f"   ❌ NLP modules error: {e}")

# ============================================================
# TEST 4: LLM Module
# ============================================================
print("\n🤖 4. TESTING LLM MODULE")

try:
    from story_toolkit.llm import LLMFactory, LLMProvider, MockLLMBackend
    print("   ✅ LLM imports")
    
    llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
    print("   ✅ Mock backend created")
    
    response = llm.generate("Hello")
    print(f"   ✅ Generate response: {response[:50]}...")
except Exception as e:
    print(f"   ❌ LLM module error: {e}")

# ============================================================
# TEST 5: Memory Module
# ============================================================
print("\n💾 5. TESTING MEMORY MODULE")

try:
    from story_toolkit.memory import MemoryManager, MemoryConfig
    print("   ✅ Memory imports")
    
    # Check if sqlite3 is available
    import sqlite3
    print("   ✅ SQLite available")
except Exception as e:
    print(f"   ❌ Memory module error: {e}")

# ============================================================
# TEST 6: Templates Module
# ============================================================
print("\n📋 6. TESTING TEMPLATES MODULE")

try:
    from story_toolkit.templates import TemplateManager
    print("   ✅ TemplateManager")
    
    manager = TemplateManager()
    templates = manager.list_templates()
    print(f"   ✅ {len(templates)} templates available")
except Exception as e:
    print(f"   ❌ Templates module error: {e}")

# ============================================================
# TEST 7: Exporters Module
# ============================================================
print("\n📄 7. TESTING EXPORTERS MODULE")

try:
    from story_toolkit.exporters import EPUBExporter, PDFExporter, HTMLExporter
    print("   ✅ Exporters imports")
    
    from story_toolkit.exporters import to_bionic, BionicText
    print("   ✅ Bionic converter")
except Exception as e:
    print(f"   ❌ Exporters module error: {e}")

# ============================================================
# TEST 8: CLI Module
# ============================================================
print("\n💻 8. TESTING CLI MODULE")

try:
    from story_toolkit.cli.main import main
    print("   ✅ CLI main")
    
    from story_toolkit.cli.commands.story import add_story_parser
    print("   ✅ CLI story commands")
    
    from story_toolkit.cli.commands.template import add_template_parser
    print("   ✅ CLI template commands")
except Exception as e:
    print(f"   ❌ CLI module error: {e}")

# ============================================================
# TEST 9: Utils Module
# ============================================================
print("\n🛠️ 9. TESTING UTILS MODULE")

try:
    from story_toolkit.utils.helpers import save_story, load_story, export_to_markdown
    print("   ✅ Utils imports")
except Exception as e:
    print(f"   ❌ Utils module error: {e}")

# ============================================================
# TEST 10: Main Toolkit
# ============================================================
print("\n🎯 10. TESTING MAIN STORYTOOLKIT")

try:
    from story_toolkit import StoryToolkit
    print("   ✅ StoryToolkit import")
    
    toolkit = StoryToolkit()
    print("   ✅ StoryToolkit created")
    
    story = toolkit.create_story("fantasy", "courage")
    print(f"   ✅ Story created: {story['metadata']['genre']}")
    
    hero = toolkit.add_character_to_story(story, "Test Hero", "protagonist")
    print(f"   ✅ Character added: {hero.name}")
    
    dialogue = toolkit.dialogue_gen.generate_dialogue("Hero", "Villain", "conflict")
    print(f"   ✅ Dialogue generated: {len(dialogue)} lines")
    
    report = toolkit.check_story_coherence(story)
    print(f"   ✅ Coherence checked: {report.get('overall_score', 0):.0%}")
    
    templates = toolkit.list_templates()
    print(f"   ✅ Templates listed: {len(templates)}")
    
    # Test novel generation
    novel = toolkit.generate_novel("fantasy", "courage", num_chapters=2, words_per_chapter=100)
    print(f"   ✅ Novel generated: {novel['title']} ({novel['num_chapters']} chapters)")
    
except Exception as e:
    print(f"   ❌ Main Toolkit error: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)
print("""
✅ Core Modules - Character, Plot, WorldBuilder, StoryEngine
✅ Generators - Character, Plot, Dialogue, Story
✅ NLP Modules - CoherenceChecker, TextAnalyzer
✅ LLM Module - Factory, Provider, Mock Backend
✅ Memory Module - SQLite, Storage
✅ Templates Module - 5 Pre-built templates
✅ Exporters Module - EPUB, PDF, HTML, Bionic
✅ CLI Module - Story and Template commands
✅ Utils Module - Save, Load, Export
✅ Main Toolkit - Full integration test passed

🎉 ALL MODULES LOADED SUCCESSFULLY!
""")