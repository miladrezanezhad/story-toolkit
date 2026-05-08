"""
Story Development Toolkit - Advanced Example
=============================================
Demonstrates advanced features and custom configurations.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from story_toolkit import (
    StoryToolkit,
    Character,
    Plot,
    WorldBuilder,
    CharacterGenerator,
    PlotGenerator,
    DialogueGenerator,
    CoherenceChecker,
    TextAnalyzer,
    save_story,
    load_story,
    export_to_markdown
)
from datetime import datetime
import json


def advanced_character_creation():
    """Advanced character creation with custom attributes"""
    print("\n" + "="*60)
    print("ADVANCED CHARACTER CREATION")
    print("="*60)
    
    # Custom character with full attributes
    protagonist = Character(
        name="Kai Stormrider",
        age=28,
        role="protagonist"
    )
    
    # Add complex personality
    protagonist.add_trait("brave")
    protagonist.add_trait("impulsive")
    protagonist.add_trait("loyal")
    protagonist.add_trait("reckless")
    
    # Multiple goals
    protagonist.add_goal("Master the ancient arts")
    protagonist.add_goal("Avenge his fallen master")
    protagonist.add_goal("Protect the innocent")
    
    # Detailed skills
    skills = ["sword_mastery", "elemental_control", "stealth", "survival"]
    for skill in skills:
        protagonist.add_skill(skill)
    
    # Weaknesses and fears
    protagonist.add_weakness("overconfidence")
    protagonist.add_weakness("impatience")
    protagonist.add_fear("losing_control")
    protagonist.add_fear("fire")
    
    # Add motivations
    protagonist.add_motivation("honor")
    protagonist.add_motivation("justice")
    protagonist.add_motivation("redemption")
    
    # Detailed background
    protagonist.background = """
    Kai was born during a great storm that destroyed his village. 
    Taken in by a wandering master, he trained for 15 years in the 
    ancient arts. When his master was murdered by the Shadow Council, 
    Kai swore vengeance. Now he walks the path between light and darkness,
    seeking justice while battling his own inner demons.
    """
    
    # Create relationships
    protagonist.add_relationship("Master Yuki", "mentor", strength=10)
    protagonist.add_relationship("Shadow Council", "enemy", strength=9)
    protagonist.add_relationship("Luna Nightshade", "ally", strength=7)
    
    # Display full character profile
    print(f"\n🎭 Character Profile: {protagonist.name}")
    print(f"{'─'*40}")
    print(f"Role: {protagonist.role}")
    print(f"Age: {protagonist.age}")
    print(f"Arc Stage: {protagonist.arc_stage}")
    
    print(f"\n📋 Personality Traits:")
    for trait in protagonist.personality_traits:
        print(f"   • {trait}")
    
    print(f"\n🎯 Goals:")
    for goal in protagonist.goals:
        print(f"   • {goal}")
    
    print(f"\n⚔️ Skills:")
    for skill in protagonist.skills:
        print(f"   • {skill}")
    
    print(f"\n⚠️ Weaknesses:")
    for weakness in protagonist.weaknesses:
        print(f"   • {weakness}")
    
    print(f"\n😨 Fears:")
    for fear in protagonist.fears:
        print(f"   • {fear}")
    
    print(f"\n💪 Motivations:")
    for motivation in protagonist.motivations:
        print(f"   • {motivation}")
    
    print(f"\n👥 Relationships:")
    for name, details in protagonist.relationships.items():
        print(f"   • {name}: {details['type']} (Strength: {details['strength']}/10)")
    
    print(f"\n📖 Background:")
    print(f"{protagonist.background.strip()}")
    
    # Get strengths and weaknesses analysis
    analysis = protagonist.get_strengths_weaknesses()
    print(f"\n📊 Character Analysis:")
    print(f"   Strengths: {len(analysis['strengths']['skills'])} skills, "
          f"{len(analysis['strengths']['positive_traits'])} positive traits")
    print(f"   Support System: {analysis['strengths']['support_system']} relationships")
    print(f"   Weaknesses: {len(analysis['weaknesses']['personal'])} personal, "
          f"{len(analysis['weaknesses']['fears'])} fears")
    
    return protagonist


def advanced_world_building():
    """Advanced world building with complex structures"""
    print("\n" + "="*60)
    print("ADVANCED WORLD BUILDING")
    print("="*60)
    
    world = WorldBuilder()
    
    # Create complex fantasy world
    world.create_world("Aethoria", "fantasy")
    
    # Add multiple interconnected locations
    locations_data = [
        {
            "name": "Crystal Spire",
            "desc": "Towering citadel made of living crystal, home to the Mage Council",
            "type": "city",
            "climate": "eternal_spring",
            "population": "50,000",
            "features": ["floating_gardens", "crystal_libraries", "portal_network"],
            "significance": 10
        },
        {
            "name": "Verdant Depths",
            "desc": "Ancient forest where trees touch the clouds and magic is wild",
            "type": "forest",
            "climate": "temperate_rainforest",
            "population": "scattered_tribes",
            "features": ["elder_trees", "fey_circles", "hidden_groves"],
            "significance": 8
        },
        {
            "name": "Ironforge Stronghold",
            "desc": "Mountain fortress of the Dwarven clans",
            "type": "city",
            "climate": "alpine",
            "population": "30,000",
            "features": ["great_forge", "underground_city", "rune_halls"],
            "significance": 9
        },
        {
            "name": "The Ashen Wastes",
            "desc": "Desolate wasteland created by ancient magical catastrophe",
            "type": "wasteland",
            "climate": "arid",
            "population": "nomadic_survivors",
            "features": ["magic_scars", "floating_islands", "time_rifts"],
            "significance": 7
        },
        {
            "name": "Shadowmere",
            "desc": "Sunken city beneath the great lake, domain of the Merfolk",
            "type": "underwater_city",
            "climate": "aquatic",
            "population": "25,000",
            "features": ["coral_palaces", "bioluminescent_gardens", "abyss_gates"],
            "significance": 8
        }
    ]
    
    for loc_data in locations_data:
        location = world.add_location(
            loc_data["name"],
            loc_data["desc"],
            loc_data["type"]
        )
        # Add extra attributes
        location.climate = loc_data["climate"]
        location.population = loc_data["population"]
        location.key_features = loc_data["features"]
        location.significance = loc_data["significance"]
        print(f"✓ Created: {location.name} ({location.type})")
    
    # Create complex connections
    connections = [
        ("Crystal Spire", "Verdant Depths"),
        ("Crystal Spire", "Ironforge Stronghold"),
        ("Verdant Depths", "Shadowmere"),
        ("Ironforge Stronghold", "The Ashen Wastes"),
        ("Shadowmere", "The Ashen Wastes"),
        ("Verdant Depths", "The Ashen Wastes")
    ]
    
    for loc1, loc2 in connections:
        world.connect_locations(loc1, loc2)
    
    print(f"\n✓ Created {len(connections)} location connections")
    
    # Add complex rules system
    world.add_rule("physical", "Magic is channeled through crystalline structures")
    world.add_rule("physical", "The world has two moons that affect magical tides")
    world.add_rule("magical", "Magic users must bond with a familiar to access powers")
    world.add_rule("magical", "Forbidden magic causes corruption of the soul")
    world.add_rule("magical", "Each element requires a different casting method")
    world.add_rule("social", "The Council of Seven governs all magical affairs")
    world.add_rule("social", "Non-magic users are second-class citizens")
    world.add_rule("technological", "Steam technology exists alongside magic")
    world.add_rule("technological", "Crystal-powered airships are common transport")
    
    # Add cultures
    cultures = [
        {
            "name": "Mageborn",
            "desc": "Noble caste of magic users who rule from Crystal Spire",
            "customs": ["ritual_binding", "elemental_trials", "spire_ascension"]
        },
        {
            "name": "Dwarven Clans",
            "desc": "Underground dwellers who master rune magic and metallurgy",
            "customs": ["forge_blessing", "ancestor_worship", "rune_carving"]
        },
        {
            "name": "Wild Elves",
            "desc": "Forest dwellers who commune with nature spirits",
            "customs": ["moon_dances", "tree_singing", "spirit_walks"]
        }
    ]
    
    for culture_data in cultures:
        world.add_culture(
            culture_data["name"],
            culture_data["desc"],
            culture_data["customs"]
        )
    
    # Add factions
    factions = [
        {
            "name": "The Obsidian Order",
            "desc": "Secret society seeking to control all magic",
            "goals": ["monopolize_crystal_magic", "eliminate_muggle_rights", "awaken_ancient_power"]
        },
        {
            "name": "Freedom Alliance",
            "desc": "Rebel group fighting for equality between magic and non-magic users",
            "goals": ["equal_rights", "free_magic_access", "overthrow_council"]
        }
    ]
    
    for faction_data in factions:
        world.add_faction(
            faction_data["name"],
            faction_data["desc"],
            faction_data["goals"]
        )
    
    # World summary
    summary = world.get_world_summary()
    print(f"\n📊 World Summary:")
    print(f"   Name: {summary['name']}")
    print(f"   Type: {summary['type']}")
    print(f"   Locations: {summary['total_locations']}")
    print(f"   Cultures: {summary['total_cultures']}")
    print(f"   Factions: {summary['total_factions']}")
    print(f"   Total Rules: {summary['rules_count']}")
    
    # Validate world
    issues = world.validate_world()
    if issues:
        print(f"\n⚠️ World Building Issues:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print(f"\n✓ World building is complete")
    
    return world


def advanced_plot_development():
    """Advanced plot development with custom configurations"""
    print("\n" + "="*60)
    print("ADVANCED PLOT DEVELOPMENT")
    print("="*60)
    
    plot_gen = PlotGenerator()
    plot = Plot()
    
    # Generate multiple genre plots
    print("\nGenerating complex plot structure...")
    
    # Main plot
    main_plot = plot_gen.generate_plot("fantasy", complexity=5)
    print(f"✓ Main Plot: {len(main_plot['main_plot'])} stages")
    
    # Add custom plot points
    plot_points = [
        ("The Awakening", "Kai discovers his hidden powers during a crisis", 1, 10),
        ("The Betrayal", "A trusted ally reveals their true allegiance", 5, 9),
        ("The Reckoning", "Final confrontation with the Shadow Council", 15, 10),
        ("The Sacrifice", "Kai must choose between power and love", 18, 8),
        ("The Rebirth", "Rising from the ashes, transformed", 20, 9)
    ]
    
    for title, desc, chapter, importance in plot_points:
        point = plot.add_plot_point(title, desc, chapter, importance)
    
    # Connect plot points
    plot.connect_plot_points(plot.plot_points[0].id, plot.plot_points[1].id)
    plot.connect_plot_points(plot.plot_points[1].id, plot.plot_points[2].id)
    plot.connect_plot_points(plot.plot_points[2].id, plot.plot_points[3].id)
    plot.connect_plot_points(plot.plot_points[3].id, plot.plot_points[4].id)
    
    # Add subplots
    plot.add_subplot(
        "The Lost Legacy",
        "Kai uncovers secrets about his true heritage",
        ["Kai", "Master Yuki"]
    )
    plot.add_subplot(
        "Forbidden Love",
        "Romance blossoms between Kai and an enemy's daughter",
        ["Kai", "Luna"]
    )
    plot.add_subplot(
        "The Resistance",
        "Underground movement fights against the Shadow Council",
        ["Freedom Alliance", "Supporting Characters"]
    )
    
    # Display plot timeline
    print(f"\n📊 Plot Summary:")
    summary = plot.get_plot_summary()
    print(f"   Total Points: {summary['total_points']}")
    print(f"   Subplots: {summary['subplots']}")
    print(f"   Structure Complete: {summary['structure_completion']:.1f}%")
    print(f"   Current Act: {summary['current_act']}")
    print(f"   Key Points: {len(summary['key_points'])}")
    
    # Display timeline
    print(f"\n⏱️ Plot Timeline:")
    for event in plot.get_plot_timeline():
        stars = "★" * event['importance'] + "☆" * (10 - event['importance'])
        print(f"   Ch.{event['chapter']:2d} [{stars}] {event['title']}: {event['description'][:40]}...")
    
    # Validate plot
    issues = plot.validate_plot()
    if issues:
        print(f"\n⚠️ Plot Issues:")
        for issue in issues:
            print(f"   - {issue}")
    
    return plot


def advanced_story_generation():
    """Advanced story generation with all features combined"""
    print("\n" + "="*60)
    print("ADVANCED STORY GENERATION")
    print("="*60)
    
    toolkit = StoryToolkit()
    
    print("\n🎬 Generating complete story with all elements...")
    
    # Generate full story automatically
    story = toolkit.generate_full_story(
        genre="fantasy",
        theme="sacrifice",
        num_characters=5
    )
    
    # Display results
    print(f"\n{'='*60}")
    print("GENERATED STORY OVERVIEW")
    print(f"{'='*60}")
    
    # Metadata
    metadata = story["metadata"]
    print(f"\n📋 Metadata:")
    print(f"   Genre: {metadata['genre']}")
    print(f"   Theme: {metadata['theme']}")
    print(f"   Complexity: {metadata['complexity']}")
    print(f"   Created: {metadata.get('created_at', 'N/A')}")
    
    # Characters
    print(f"\n👥 Characters ({len(story['characters'])}):")
    for char in story['characters']:
        print(f"   • {char.name} - {char.role}")
        print(f"     Traits: {', '.join(char.personality_traits[:3])}")
    
    # Plot
    plot = story.get("plot", {})
    print(f"\n📚 Plot:")
    print(f"   Main Plot Stages: {len(plot.get('main_plot', []))}")
    print(f"   Subplots: {len(plot.get('subplots', []))}")
    print(f"   Twists: {plot.get('twists', [])}")
    
    # World
    world = story.get("world", {})
    print(f"\n🌍 World:")
    print(f"   Type: {world.get('type', 'N/A')}")
    print(f"   Key Locations: {len(world.get('key_locations', []))}")
    
    # Dialogue
    print(f"\n💬 Dialogue Scenes: {len(story.get('dialogue_scenes', []))}")
    
    # Coherence
    report = story.get("coherence_report", {})
    print(f"\n🔍 Coherence Report:")
    print(f"   Overall Score: {report.get('overall_score', 0):.2%}")
    
    recommendations = report.get("recommendations", [])
    if recommendations:
        print(f"   Recommendations:")
        for rec in recommendations:
            print(f"     - {rec}")
    
    # Save story
    print(f"\n💾 Saving story...")
    filename = f"advanced_story_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        json_path = save_story(story, f"{filename}.json")
        print(f"   ✓ JSON: {json_path}")
        
        md_path = export_to_markdown(story, f"{filename}.md")
        print(f"   ✓ Markdown: {md_path}")
    except Exception as e:
        print(f"   ⚠️ Save error: {e}")
    
    return story


def main():
    """Run advanced demonstrations"""
    print("\n🔥 STORY DEVELOPMENT TOOLKIT - ADVANCED FEATURES 🔥")
    print(f"Author: Milad Rezanezhad")
    print(f"GitHub: https://github.com/miladrezanezhad")
    
    try:
        advanced_character_creation()
        advanced_world_building()
        advanced_plot_development()
        advanced_story_generation()
        
        print(f"\n{'='*60}")
        print("✅ All advanced demonstrations completed!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
