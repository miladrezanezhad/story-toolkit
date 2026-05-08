"""
Tests for NLP modules.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit.nlp.coherence_checker import CoherenceChecker
from story_toolkit.nlp.text_analyzer import TextAnalyzer


def test_coherence_checker():
    """Test CoherenceChecker functionality"""
    print("\nTesting CoherenceChecker...")
    
    checker = CoherenceChecker()
    
    # Test character consistency check
    characters = [
        {"stage": 0, "personality": "brave"},
        {"stage": 1, "personality": "brave"},
        {"stage": 2, "personality": "brave"}
    ]
    result = checker.check_character_consistency(characters)
    assert result["is_consistent"] == True
    print("  ✓ Consistent character check")
    
    # Test character inconsistency detection
    characters_bad = [
        {"stage": 0, "personality": "brave"},
        {"stage": 1, "personality": "cowardly"}
    ]
    result_bad = checker.check_character_consistency(characters_bad)
    assert result_bad["is_consistent"] == False
    print("  ✓ Inconsistent character detection")
    
    # Test timeline coherence
    events = [
        {"id": 1, "timestamp": 100},
        {"id": 2, "timestamp": 200},
        {"id": 3, "timestamp": 300}
    ]
    timeline = checker.check_timeline_coherence(events)
    assert timeline["is_coherent"] == True
    print("  ✓ Coherent timeline check")
    
    # Test timeline incoherence detection
    events_bad = [
        {"id": 1, "timestamp": 300},
        {"id": 2, "timestamp": 200}
    ]
    timeline_bad = checker.check_timeline_coherence(events_bad)
    assert timeline_bad["is_coherent"] == False
    print("  ✓ Incoherent timeline detection")
    
    # Test plot hole detection
    elements = [
        {"id": "clue1", "introduced": True, "resolved": True},
        {"id": "clue2", "introduced": True, "resolved": False}
    ]
    holes = checker.check_plot_holes(elements)
    assert len(holes) > 0
    print("  ✓ Plot hole detection")
    
    # Test full report generation
    story_data = {
        "characters": characters,
        "events": events,
        "elements": elements
    }
    report = checker.generate_coherence_report(story_data)
    assert "overall_score" in report
    assert "character_consistency" in report
    assert "timeline" in report
    assert "plot_holes" in report
    assert "recommendations" in report
    print("  ✓ Full report generation")
    
    print("✅ CoherenceChecker tests passed!")


def test_text_analyzer():
    """Test TextAnalyzer functionality"""
    print("\nTesting TextAnalyzer...")
    
    analyzer = TextAnalyzer()
    
    # Test text analysis
    sample_text = """
    The old house stood on the hill. It had been abandoned for years. 
    Strange lights flickered in the windows at night. Nobody dared to enter.
    """
    
    analysis = analyzer.analyze_text(sample_text)
    assert "word_count" in analysis
    assert analysis["word_count"] > 0
    assert "sentence_count" in analysis
    assert analysis["sentence_count"] > 0
    assert "avg_words_per_sentence" in analysis
    assert "readability_score" in analysis
    assert "reading_level" in analysis
    print("  ✓ Text analysis")
    
    # Test readability analysis
    readability = analyzer.analyze_readability(sample_text)
    assert "score" in readability
    assert "level" in readability
    assert "avg_words_per_sentence" in readability
    print("  ✓ Readability analysis")
    
    # Test dialogue analysis
    dialogue = [
        "Hero: I will stop you!",
        "Villain: You can try!",
        "Hero: For justice!",
        "Villain: Justice is an illusion!"
    ]
    
    dialogue_analysis = analyzer.analyze_dialogue(dialogue)
    assert "total_lines" in dialogue_analysis
    assert dialogue_analysis["total_lines"] == 4
    assert "speakers" in dialogue_analysis
    assert "Hero" in dialogue_analysis["speakers"]
    assert "Villain" in dialogue_analysis["speakers"]
    print("  ✓ Dialogue analysis")
    
    # Test pacing analysis
    pacing = analyzer.analyze_pacing(sample_text, chunk_size=10)
    assert "chunks_analyzed" in pacing
    assert "pacing_data" in pacing
    assert len(pacing["pacing_data"]) > 0
    print("  ✓ Pacing analysis")
    
    print("✅ TextAnalyzer tests passed!")


if __name__ == "__main__":
    print("\n🧪 STORY TOOLKIT - NLP TESTS")
    print("="*40)
    
    test_coherence_checker()
    test_text_analyzer()
    
    print(f"\n{'='*40}")
    print("✅ All NLP tests passed!")
    print(f"{'='*40}\n")
