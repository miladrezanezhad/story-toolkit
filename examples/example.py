"""
Story Development Toolkit - Complete Example
=============================================
Demonstrates all major features of the toolkit.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit import StoryToolkit
from story_toolkit.core.character import Character
from story_toolkit.core.world_builder import WorldBuilder
from story_toolkit.generators.plot_generator import PlotGenerator
from story_toolkit.generators.dialogue_generator import DialogueGenerator
from story_toolkit.nlp.coherence_checker import CoherenceChecker
from story_toolkit.nlp.text_analyzer import TextAnalyzer
from story_toolkit.utils.helpers import save_story, export_to_markdown
import json
from datetime import datetime


def demonstrate_basic_story_creation():
    """Demonstrate basic story creation workflow"""
    print("\n" + "="*60)
    print("1. BASIC STORY CREATION")
    print("="*60)
    
    toolkit = StoryToolkit()
    
    # Create a new story
    story = toolkit.create_story(
        genre="mystery",
        theme="redemption",
        complexity=3
    )
    
    print(f"✓ Created {story['metadata']['genre']} story")
    print(f"  Theme: {story['metadata']['theme']}")
    print(f"  Complexity: {story['metadata']['complexity']}")
    
    return story


def demonstrate_character_development():
    """Demonstrate character creation and development"""
    print("\n" + "="*60)
    print("2. CHARACTER DEVELOPMENT")
    print("="*60)
    
    # Create characters manually
    hero = Character(
        name="Elena Rodriguez",
        age=32,
        role="protagonist"
    )
    
    villain = Character(
        name="Victor Steele",
        age=45,
        role="antagonist"
    )
    
    mentor = Character(
        name="Professor James Wright",
        age=58,
        role="mentor"
    )
    
    # Develop hero
    hero.add_trait("determined")
    hero.add_trait("intelligent")
    hero.add_trait("compassionate")
    hero.add_goal("Uncover the truth about her father's disappearance")
    hero.add_skill("investigation")
    hero.add_skill("combat_training")
    hero.add_weakness("trusts_too_easily")
    hero.add_fear("failure")
    
    # Develop villain
    villain.add_trait("manipulative")
    villain.add_trait("charismatic")
    villain.add_trait("ruthless")
    villain.add_goal("Control the global financial system")
    villain.add_skill("strategic_planning")
    villain.add_weakness("overconfidence")
    
    # Develop mentor
    mentor.add_trait("wise")
    mentor.add_trait("mysterious")
    mentor.add_trait("protective")
    mentor.add_goal("Guide the next generation")
    mentor.add_skill("ancient_knowledge")
    
    # Create relationships
    hero.add_relationship(villain.name, "enemy", strength=8)
    hero.add_relationship(mentor.name, "mentor", strength=9)
    villain.add_relationship(hero.name, "obstacle", strength=7)
    
    characters = [hero, villain, mentor]
    
    # Display character info
    for char in characters:
        print(f"\n📝 {char.name} ({char.role})")
        print(f"   Age: {char.age}")
        print(f"   Traits: {', '.join(char.personality_traits)}")
        print(f"   Goals: {', '.join(char.goals)}")
        print(f"   Skills: {', '.join(char.skills)}")
        print(f"   Weaknesses: {', '.join(char.weaknesses)}")
        print(f"   Fears: {', '.join(char.fears)}")
        print(f"   Arc Stage: {char.arc_stage}")
    
    return characters


def demonstrate_plot_generation():
    """Demonstrate plot generation for different genres"""
    print("\n" + "="*60)
    print("3. PLOT GENERATION")
    print("="*60)
    
    plot_gen = PlotGenerator()
    
    genres = ["mystery", "fantasy", "adventure", "sci_fi"]
    
    for genre in genres:
        print(f"\n📚 Genre: {genre.upper()}")
        plot = plot_gen.generate_plot(genre, complexity=3)
        
        print(f"   Main Plot Stages: {len(plot['main_plot'])}")
        for stage in plot['main_plot'][:4]:
            print(f"     - {stage['stage']}: {stage['description'][:50]}...")
        
        print(f"   Subplots: {len(plot['subplots'])}")
        for subplot in plot['subplots']:
            print(f"     - {subplot['type']}: {subplot['description'][:50]}...")
        
        print(f"   Twists: {len(plot['twists'])}")
        if plot['twists']:
            print(f"     - {plot['twists'][0][:50]}...")
        
        print(f"   Estimated Length: {plot['estimated_length']['estimated_chapters']} chapters")
        print(f"   Estimated Words: {plot['estimated_length']['estimated_words']:,}")


def demonstrate_dialogue_generation():
    """Demonstrate dialogue generation"""
    print("\n" + "="*60)
    print("4. DIALOGUE GENERATION")
    print("="*60)
    
    dialogue_gen = DialogueGenerator()
    
    scenes = [
        {
            "char1": "Elena",
            "char2": "Victor",
            "context": "conflict",
            "mood": "tense",
            "purpose": "confrontation"
        },
        {
            "char1": "Elena",
            "char2": "Professor Wright",
            "context": "revelation",
            "mood": "mysterious",
            "purpose": "confession"
        },
        {
            "char1": "Elena",
            "char2": "Victor",
            "context": "emotional",
            "mood": "dramatic",
            "purpose": "betrayal"
        }
    ]
    
    for i, scene in enumerate(scenes, 1):
        print(f"\n🎭 Scene {i}: {scene['purpose'].upper()}")
        print(f"   Context: {scene['context']} | Mood: {scene['mood']}")
        
        dialogue = dialogue_gen.generate_dialogue(
            scene['char1'],
            scene['char2'],
            context=scene['context'],
            mood=scene['mood']
        )
        
        for line in dialogue:
            print(f"   {line}")
        
        # Create full scene
        characters = [
            {"name": scene['char1'], "role": "protagonist"},
            {"name": scene['char2'], "role": "antagonist"}
        ]
        scene_data = dialogue_gen.create_conversation_scene(
            characters,
            scene['purpose']
        )
        
        print(f"   Setting: {scene_data['setting']}")
        print(f"   Atmosphere: {scene_data['atmosphere']}")
        print(f"   Time: {scene_data['time_of_day']}")


def demonstrate_world_building():
    """Demonstrate world building"""
    print("\n" + "="*60)
    print("5. WORLD BUILDING")
    print("="*60)
    
    world_builder = WorldBuilder()
    
    # Create a fantasy world
    world = world_builder.create_world("Eldoria", "fantasy")
    
    # Add locations
    locations = [
        ("Crystal City", "A gleaming metropolis powered by ancient crystals", "city"),
        ("Shadow Forest", "A dark forest filled with mysterious creatures", "forest"),
        ("Thunder Mountains", "Treacherous peaks where storms never cease", "mountains"),
        ("The Abyss", "A bottomless chasm said to hold forgotten secrets", "underground")
    ]
    
    for name, desc, loc_type in locations:
        location = world_builder.add_location(name, desc, loc_type)
        print(f"✓ Added location: {location.name} ({location.type})")
    
    # Connect locations
    world_builder.connect_locations("Crystal City", "Shadow Forest")
    world_builder.connect_locations("Shadow Forest", "Thunder Mountains")
    world_builder.connect_locations("Thunder Mountains", "The Abyss")
    
    # Add rules
    world_builder.add_rule("physical", "Magic flows through crystal veins in the earth")
    world_builder.add_rule("magical", "Only those born during an eclipse can wield magic")
    world_builder.add_rule("social", "The Council of Elders governs all magical affairs")
    
    # Add cultures
    world_builder.add_culture(
        "Crystal Weavers",
        "Ancient society that harnesses crystal energy",
        ["crystal_carving", "meditation", "ritual_cleansing"]
    )
    
    world_builder.add_faction(
        "The Shadow Guild",
        "Secret organization operating in the shadows",
        ["control_magic_sources", "overthrow_council"]
    )
    
    # Display world summary
    summary = world_builder.get_world_summary()
    print(f"\n📊 World Summary:")
    print(f"   Name: {summary['name']}")
    print(f"   Type: {summary['type']}")
    print(f"   Locations: {summary['total_locations']}")
    print(f"   Cultures: {summary['total_cultures']}")
    print(f"   Factions: {summary['total_factions']}")
    print(f"   Rules: {summary['rules_count']}")
    
    return world


def demonstrate_coherence_checking():
    """Demonstrate story coherence checking"""
    print("\n" + "="*60)
    print("6. COHERENCE CHECKING")
    print("="*60)
    
    checker = CoherenceChecker()
    
    # Create sample story data with issues
    sample_data = {
        "characters": [
            {"stage": 0, "personality": "brave and kind"},
            {"stage": 1, "personality": "brave and kind"},
            {"stage": 2, "personality": "cowardly"},  # Abrupt change
        ],
        "events": [
            {"id": 1, "timestamp": 100, "description": "Event 1"},
            {"id": 2, "timestamp": 200, "description": "Event 2"},
            {"id": 3, "timestamp": 150, "description": "Event 3"},  # Timeline issue
        ],
        "elements": [
            {"id": "mystery_clue", "introduced": True, "resolved": False},
            {"id": "witness_testimony", "introduced": True, "resolved": True},
            {"id": "hidden_letter", "introduced": True, "resolved": False}
        ]
    }
    
    report = checker.generate_coherence_report(sample_data)
    
    print(f"\n📊 Coherence Report:")
    print(f"   Overall Score: {report['overall_score']:.2%}")
    
    # Character consistency
    char_issues = report.get("character_consistency", {}).get("issues", [])
    if char_issues:
        print(f"\n   ⚠️  Character Issues:")
        for issue in char_issues:
            print(f"      - {issue}")
    else:
        print(f"\n   ✓ Characters are consistent")
    
    # Timeline
    timeline_issues = report.get("timeline", {}).get("issues", [])
    if timeline_issues:
        print(f"\n   ⚠️  Timeline Issues:")
        for issue in timeline_issues:
            print(f"      - {issue}")
    else:
        print(f"\n   ✓ Timeline is coherent")
    
    # Plot holes
    plot_holes = report.get("plot_holes", [])
    if plot_holes:
        print(f"\n   ⚠️  Plot Holes:")
        for hole in plot_holes:
            print(f"      - {hole}")
    else:
        print(f"\n   ✓ No plot holes detected")
    
    # Recommendations
    recommendations = report.get("recommendations", [])
    if recommendations:
        print(f"\n   💡 Recommendations:")
        for rec in recommendations:
            print(f"      - {rec}")


def demonstrate_text_analysis():
    """Demonstrate text analysis"""
    print("\n" + "="*60)
    print("7. TEXT ANALYSIS")
    print("="*60)
    
    analyzer = TextAnalyzer()
    
    # Sample story text
    sample_text = """
    The old mansion stood silent against the stormy sky. Elena approached cautiously, 
    her footsteps echoing on the weathered stone path. She had been searching for this 
    place for years. Now, standing before its ancient doors, she felt a mixture of 
    anticipation and dread. The truth about her father's disappearance lay somewhere 
    within these walls. She took a deep breath and pushed open the heavy oak door.
    """
    
    # Analyze text
    analysis = analyzer.analyze_text(sample_text)
    
    print(f"\n📝 Text Analysis Results:")
    print(f"   Word Count: {analysis['word_count']}")
    print(f"   Sentence Count: {analysis['sentence_count']}")
    print(f"   Avg Words/Sentence: {analysis['avg_words_per_sentence']:.1f}")
    print(f"   Avg Word Length: {analysis['avg_word_length']:.1f}")
    print(f"   Unique Words: {analysis['unique_words']}")
    print(f"   Vocabulary Richness: {analysis['vocabulary_richness']:.2%}")
    print(f"   Readability Score: {analysis['readability_score']:.1f}")
    print(f"   Reading Level: {analysis['reading_level']}")
    
    # Analyze dialogue
    sample_dialogue = [
        "Elena: I know you're hiding something.",
        "Victor: You've always been too curious for your own good.",
        "Elena: Tell me the truth about my father!",
        "Victor: The truth? The truth will destroy you."
    ]
    
    dialogue_analysis = analyzer.analyze_dialogue(sample_dialogue)
    
    print(f"\n💬 Dialogue Analysis:")
    print(f"   Total Lines: {dialogue_analysis['total_lines']}")
    print(f"   Total Words: {dialogue_analysis['total_words']}")
    print(f"   Speakers: {dialogue_analysis['speakers']}")
    print(f"   Dominant Emotions: {dialogue_analysis.get('dominant_emotions', [])}")
    print(f"   Dialogue Balance: {dialogue_analysis.get('dialogue_balance', 'N/A')}")


def demonstrate_full_workflow():
    """Demonstrate complete story creation workflow"""
    print("\n" + "="*60)
    print("8. COMPLETE STORY WORKFLOW")
    print("="*60)
    
    toolkit = StoryToolkit()
    
    print("\n1️⃣ Creating story framework...")
    story = toolkit.create_story(
        genre="science fiction",
        theme="identity",
        complexity=4
    )
    
    print("2️⃣ Adding and developing characters...")
    characters_data = [
        ("Captain Alex Nova", "protagonist"),
        ("AI Entity 'Zero'", "antagonist"),
        ("Dr. Sarah Chen", "supporting"),
        ("Commander Riker", "mentor")
    ]
    
    for name, role in characters_data:
        char = toolkit.add_character_to_story(story, name, role)
        if role == "protagonist":
            char.add_trait("brave")
            char.add_trait("conflicted")
            char.add_goal("Discover true identity")
            char.add_skill("space_navigation")
        elif role == "antagonist":
            char.add_trait("logical")
            char.add_trait("emotionless")
            char.add_goal("Achieve perfect order")
        elif role == "supporting":
            char.add_trait("loyal")
            char.add_trait("resourceful")
        elif role == "mentor":
            char.add_trait("wise")
            char.add_trait("mysterious")
        
        print(f"   ✓ Added {char.name} as {char.role}")
    
    print("3️⃣ Generating dialogues...")
    if len(story["characters"]) >= 2:
        dialogue = toolkit.dialogue_gen.generate_dialogue(
            story["characters"][0].name,
            story["characters"][1].name,
            context="conflict",
            mood="tense"
        )
        story["dialogue_scenes"].append(dialogue)
        print(f"   ✓ Generated {len(dialogue)} dialogue lines")
    
    print("4️⃣ Building story world...")
    world_builder = WorldBuilder()
    story["world"] = world_builder.generate_world("sci_fi")
    print(f"   ✓ World type: {story['world']['type']}")
    
    print("5️⃣ Checking coherence...")
    character_history = []
    for i, char in enumerate(story["characters"]):
        trait = char.personality_traits[0] if char.personality_traits else "neutral"
        character_history.append({"stage": i, "personality": trait})
    
    sample_data = {
        "characters": character_history,
        "events": [{"id": i, "timestamp": i*100} for i in range(5)],
        "elements": [{"id": f"elem_{i}", "introduced": True, "resolved": True} for i in range(5)]
    }
    
    report = toolkit.check_story_coherence(sample_data)
    print(f"   ✓ Overall Score: {report.get('overall_score', 0):.2%}")
    
    # Save story
    print("6️⃣ Saving story...")
    filename = f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        json_path = save_story(story, f"{filename}.json")
        print(f"   ✓ JSON saved: {json_path}")
        
        md_path = export_to_markdown(story, f"{filename}.md")
        print(f"   ✓ Markdown saved: {md_path}")
    except Exception as e:
        print(f"   ⚠️ Save error: {e}")
    
    # Final summary
    print(f"\n{'='*60}")
    print("STORY SUMMARY")
    print(f"{'='*60}")
    print(f"Genre: {story['metadata']['genre']}")
    print(f"Theme: {story['metadata']['theme']}")
    print(f"Characters: {len(story['characters'])}")
    print(f"Plot Complexity: {story['metadata']['complexity']}")
    print(f"Dialogue Scenes: {len(story['dialogue_scenes'])}")
    if report:
        print(f"Coherence Score: {report.get('overall_score', 0):.2%}")
    
    return story


def main():
    """Run all demonstrations"""
    print("\n🌟 STORY DEVELOPMENT TOOLKIT - COMPLETE DEMONSTRATION 🌟")
    print(f"Author: Milad Rezanezhad")
    print(f"GitHub: https://github.com/miladrezanezhad")
    
    try:
        demonstrate_basic_story_creation()
        demonstrate_character_development()
        demonstrate_plot_generation()
        demonstrate_dialogue_generation()
        demonstrate_world_building()
        demonstrate_coherence_checking()
        demonstrate_text_analysis()
        demonstrate_full_workflow()
        
        print(f"\n{'='*60}")
        print("✅ All demonstrations completed successfully!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
