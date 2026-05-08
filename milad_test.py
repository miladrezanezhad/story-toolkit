# auto_story_generator.py
"""
Auto Story Generator - Generates a complete story and saves as PDF

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from story_toolkit import StoryToolkit
from story_toolkit.llm import LLMFactory, LLMProvider
from story_toolkit.exporters import PDFExporter, ExportConfig, PDFStyle
import os
import json

print("="*710)
print("📖 AUTO STORY GENERATOR")
print("="*701)

# ============================================================
# STEP 1: Create Toolkit with LLM
# ============================================================
print("\n1️⃣ Initializing Story Toolkit...")

# Using Mock LLM (no API key needed)
# For real stories, use:
# llm = LLMFactory.create_backend(provider=LLMProvider.OPENAI, api_key="sk-...")
llm = LLMFactory.create_backend(provider=LLMProvider.MOCK)
toolkit = StoryToolkit(llm_backend=llm)
print("   ✅ Toolkit ready")

# ============================================================
# STEP 2: Generate Story Structure
# ============================================================
print("\n2️⃣ Generating story structure...")

story_config = {
    "title": "The Crystal of Destiny",
    "genre": "fantasy",
    "theme": "redemption",
    "author": "Story Toolkit AI",
    "chapters": 4
}

print(f"   📖 Title: {story_config['title']}")
print(f"   🎭 Genre: {story_config['genre']}")
print(f"   ❤️ Theme: {story_config['theme']}")
print(f"   📚 Chapters: {story_config['chapters']}")

# ============================================================
# STEP 3: Generate Chapter Content
# ============================================================
print("\n3️⃣ Generating chapter content...")

# Define chapter outlines
chapters = [
    {
        "number": 1,
        "title": "The Awakening",
        "summary": "In the village of Oakhaven, a young hero discovers a mysterious crystal that glows with ancient power. Little do they know, this crystal holds the key to saving the kingdom from a dark curse."
    },
    {
        "number": 2,
        "title": "The Journey Begins",
        "summary": "The hero leaves home, venturing into the Whispering Woods. Along the way, they meet strange creatures and face their first challenges. An old friend joins the quest."
    },
    {
        "number": 3,
        "title": "Trials and Truths",
        "summary": "The hero faces three trials that test their courage, wisdom, and heart. They learn the truth about the crystal and the sacrifice required to save the kingdom."
    },
    {
        "number": 4,
        "title": "The Final Choice",
        "summary": "The hero confronts the dark lord at the Crystal Spire. A choice must be made that will determine the fate of everyone they love. Sacrifice or victory?"
    }
]

# Generate actual content for each chapter
story_content = []
for chapter in chapters:
    print(f"   📝 Writing Chapter {chapter['number']}: {chapter['title']}...")
    
    # Build prompt for LLM
    prompt = f"""Write a short chapter for a fantasy story.

Genre: Fantasy
Theme: Redemption
Chapter {chapter['number']}: {chapter['title']}
Summary: {chapter['summary']}

Write approximately 2500 words. Make it engaging with dialogue and vivid descriptions.
The hero should face challenges and grow throughout the chapter.

Chapter {chapter['number']}: {chapter['title']}

"""
    
    # Generate content using LLM
    try:
        content = llm.generate(prompt, max_tokens=800)
    except:
        # Fallback content if LLM fails
        content = f"""
CHAPTER {chapter['number']}: {chapter['title']}

{chapter['summary']}

The journey was long and treacherous, but the hero pressed forward. Each step brought them closer to their destiny. The wind whispered secrets of ancient times, and the stars guided their path.

"The crystal chose you for a reason," a voice echoed in their mind. "Trust yourself."

With renewed determination, the hero continued. The final battle awaited, but they were no longer afraid. They had come too far to turn back now.

To be continued...
"""
    
    story_content.append({
        "number": chapter["number"],
        "title": chapter["title"],
        "content": content
    })

print("   ✅ All chapters generated")

# ============================================================
# STEP 4: Create Story Data Structure for PDF
# ============================================================
print("\n4️⃣ Creating story data structure...")

# Build story dictionary for PDF export
story_data = {
    "metadata": {
        "title": story_config["title"],
        "author": story_config["author"],
        "genre": story_config["genre"],
        "theme": story_config["theme"]
    },
    "plot": {
        "main_plot": []
    }
}

# Add chapters to story data
for chapter in story_content:
    story_data["plot"]["main_plot"].append({
        "stage": chapter["title"],
        "description": chapter["content"][:200] + "...",
        "content": chapter["content"]
    })

print("   ✅ Story data ready")

# ============================================================
# STEP 5: Export to PDF
# ============================================================
print("\n5️⃣ Exporting to PDF...")

# Configure PDF
config = ExportConfig(
    title=story_config["title"],
    author=story_config["author"],
    pdf_style=PDFStyle.PRINT
)

# Create PDF exporter
exporter = PDFExporter(config)

# Generate PDF filename
pdf_filename = f"{story_config['title'].replace(' ', '_')}.pdf"
exporter.export(story_data, pdf_filename)

file_size = os.path.getsize(pdf_filename)
print(f"   ✅ PDF created: {pdf_filename}")
print(f"   📄 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

# ============================================================
# STEP 6: Display Story Preview
# ============================================================
print("\n" + "="*70)
print("📖 STORY PREVIEW")
print("="*70)

for chapter in story_content:
    print(f"\n{'='*60}")
    print(f"📚 {chapter['title']}")
    print(f"{'='*60}")
    # Show first 500 characters of each chapter
    preview = chapter['content'][:500]
    print(preview)
    if len(chapter['content']) > 500:
        print("\n... (continued in PDF)")
    print()

# ============================================================
# STEP 7: Save as JSON backup
# ============================================================
json_filename = f"{story_config['title'].replace(' ', '_')}.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(story_data, f, indent=2, ensure_ascii=False)
print(f"\n💾 Story saved as JSON: {json_filename}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*70)
print("🎉 STORY GENERATION COMPLETE!")
print("="*70)
print(f"""
📖 Story: {story_config['title']}
🎭 Genre: {story_config['genre']}
❤️ Theme: {story_config['theme']}
📚 Chapters: {len(story_content)}
📄 PDF File: {pdf_filename}
💾 JSON File: {json_filename}

✨ The story has been automatically generated and saved as PDF!
""")

# ============================================================
# STEP 8: Open PDF
# ============================================================
try:
    os.startfile(pdf_filename)
    print("📖 PDF opened automatically!")
except:
    print(f"📖 Please open {pdf_filename} manually.")