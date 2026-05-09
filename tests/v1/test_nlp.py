"""
Tests for v1.0.0 - NLP Tools (CoherenceChecker, TextAnalyzer)

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from story_toolkit.nlp.coherence_checker import CoherenceChecker
from story_toolkit.nlp.text_analyzer import TextAnalyzer


def create_test_story_data():
    """Create sample story data for testing"""
    return {
        "characters": [
            {"stage": 0, "personality": "brave and kind"},
            {"stage": 1, "personality": "brave and kind"},
            {"stage": 2, "personality": "brave and kind"}
        ],
        "events": [
            {"id": 1, "timestamp": 100},
            {"id": 2, "timestamp": 200},
            {"id": 3, "timestamp": 300}
        ],
        "elements": [
            {"id": "clue_1", "introduced": True, "resolved": True},
            {"id": "clue_2", "introduced": True, "resolved": False}
        ]
    }


def test_coherence_checker():
    """Test CoherenceChecker class"""
    print("\n🔍 Testing CoherenceChecker (v1)...")
    
    checker = CoherenceChecker()
    
    # Test generate report
    story_data = create_test_story_data()
    report = checker.generate_coherence_report(story_data)
    
    assert report is not None
    assert "overall_score" in report
    assert isinstance(report["overall_score"], float)
    
    # Test quick check
    is_coherent = checker.quick_check(story_data)
    assert isinstance(is_coherent, bool)
    
    # Test detailed issues
    details = checker.get_detailed_issues(story_data)
    assert details is not None
    
    print("   ✅ CoherenceChecker tests passed")
    return True


def test_text_analyzer():
    """Test TextAnalyzer class"""
    print("\n📊 Testing TextAnalyzer (v1)...")
    
    analyzer = TextAnalyzer()
    
    # Test analyze text
    text = "The old house stood on the hill. It had been abandoned for many years."
    analysis = analyzer.analyze_text(text)
    
    assert analysis is not None
    assert "word_count" in analysis
    assert "readability_score" in analysis
    
    # Test analyze readability
    readability = analyzer.analyze_readability(text)
    assert isinstance(readability, dict)
    
    # Test analyze dialogue
    dialogue = [
        "Hero: I will defeat you!",
        "Villain: You can try!",
        "Hero: For justice!"
    ]
    dialogue_analysis = analyzer.analyze_dialogue(dialogue)
    assert dialogue_analysis is not None
    
    print("   ✅ TextAnalyzer tests passed")
    return True


def run_all():
    """Run all v1 NLP tests"""
    print("\n" + "="*60)
    print("🧪 V1.0.0 - NLP TESTS")
    print("="*60)
    
    results = []
    results.append(("CoherenceChecker", test_coherence_checker()))
    results.append(("TextAnalyzer", test_text_analyzer()))
    
    print("\n" + "-"*40)
    for name, status in results:
        print(f"  {'✅' if status else '❌'} {name}")
    print("-"*40)
    
    all_passed = all(status for _, status in results)
    print(f"\n📊 V1 NLP Tests: {sum(1 for _, s in results if s)}/{len(results)} passed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)