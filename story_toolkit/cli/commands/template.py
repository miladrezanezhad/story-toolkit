"""
Template commands for CLI.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from story_toolkit import StoryToolkit


def cmd_list_templates(args):
    """List all available templates"""
    toolkit = StoryToolkit()
    templates = toolkit.list_templates()
    
    print(f"\n📚 Available templates ({len(templates)}):")
    for t in templates:
        print(f"\n   📋 {t['name']}")
        print(f"      Genre: {t['genre']}")
        print(f"      Stages: {t['stage_count']}")
        print(f"      Description: {t['description'][:80]}...")
    
    return templates


def cmd_use_template(args):
    """Create story from template"""
    try:
        toolkit = StoryToolkit()
        
        story = toolkit.use_template(
            template_name=args.template,
            genre=getattr(args, 'genre', None),
            theme=getattr(args, 'theme', 'adventure')
        )
        
        print(f"✅ Template '{args.template}' applied")
        print(f"📖 Genre: {story['metadata']['genre']}")
        print(f"📖 Theme: {story['metadata']['theme']}")
        print(f"📖 Stages: {len(story['plot']['main_plot'])}")
        
        # Save to file if output specified
        if hasattr(args, 'output') and args.output:
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(story, f, indent=2, ensure_ascii=False)
            print(f"   📁 Saved to {args.output}")
        
        return story
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def add_template_parser(subparsers):
    """Add template subcommands to parser"""
    
    # template list
    parser_list = subparsers.add_parser('list', help='List all templates')
    parser_list.set_defaults(func=cmd_list_templates)
    
    # template use
    parser_use = subparsers.add_parser('use', help='Use a template')
    parser_use.add_argument('template', 
                            choices=['hero_journey', 'three_act', 'mystery_clues', 'romance_beat', 'horror_cycle'],
                            help='Template name')
    parser_use.add_argument('--genre', '-g', help='Story genre (optional)')
    parser_use.add_argument('--theme', '-t', default='adventure', help='Story theme')
    parser_use.add_argument('--output', '-o', help='Save story to JSON file')
    parser_use.set_defaults(func=cmd_use_template)
