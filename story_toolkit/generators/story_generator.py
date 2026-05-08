"""
Story Generator - Generate complete novels using LLM

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import random

from ..llm import BaseLLMBackend


class StoryGenerator:
    """Generate complete stories and novels using LLM"""
    
    def __init__(self, llm_backend: Optional[BaseLLMBackend] = None):
        self.llm_backend = llm_backend
        self.use_llm = llm_backend is not None
    
    def generate_novel(self, genre: str, theme: str, 
                       num_chapters: int = 5,
                       words_per_chapter: int = 500,
                       protagonist_name: str = None,
                       antagonist_name: str = None,
                       use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate a complete novel
        
        Args:
            genre: Story genre (fantasy, sci-fi, mystery, romance, adventure)
            theme: Story theme (courage, love, redemption, survival)
            num_chapters: Number of chapters (default: 5)
            words_per_chapter: Words per chapter (default: 500)
            protagonist_name: Hero's name (auto-generated if None)
            antagonist_name: Villain's name (auto-generated if None)
            use_llm: Use LLM for generation (fallback to templates if False)
        
        Returns:
            Dictionary with complete novel
        """
        # Generate names if not provided
        if not protagonist_name:
            protagonist_name = self._generate_name()
        if not antagonist_name:
            antagonist_name = self._generate_name()
        
        # Generate chapter outlines
        chapters = self._generate_chapter_outlines(
            genre, theme, num_chapters, protagonist_name, antagonist_name
        )
        
        # Generate content for each chapter
        if self.use_llm and use_llm:
            novel_content = self._generate_chapters_with_llm(
                genre, theme, chapters, protagonist_name, antagonist_name, words_per_chapter
            )
        else:
            novel_content = self._generate_chapters_with_templates(
                chapters, words_per_chapter
            )
        
        # Create novel structure
        novel = {
            "title": self._generate_title(genre, theme),
            "genre": genre,
            "theme": theme,
            "protagonist": protagonist_name,
            "antagonist": antagonist_name,
            "num_chapters": num_chapters,
            "chapters": novel_content,
            "created_at": datetime.now().isoformat()
        }
        
        return novel
    
    def _generate_name(self) -> str:
        """Generate a random name"""
        first_names = ["Kai", "Zara", "Liam", "Nova", "Asher", "Luna", "Eli", "Iris", "Leo", "Aria"]
        last_names = ["Storm", "Shadow", "Bright", "Stone", "Wind", "Fire", "Water", "Star"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_title(self, genre: str, theme: str) -> str:
        """Generate a title based on genre and theme"""
        templates = {
            "fantasy": [f"The {theme.capitalize()} Quest", f"Tales of {theme.capitalize()}", 
                       f"The {theme.capitalize()} Blade", f"Realm of {theme.capitalize()}"],
            "mystery": [f"The {theme.capitalize()} Secret", f"Case of {theme.capitalize()}",
                       f"Shadow of {theme.capitalize()}"],
            "romance": [f"A {theme.capitalize()} Heart", f"Love and {theme.capitalize()}",
                       f"The {theme.capitalize()} Promise"],
            "adventure": [f"The Great {theme.capitalize()}", f"Quest of {theme.capitalize()}",
                         f"Journey to {theme.capitalize()}"],
            "sci_fi": [f"The {theme.capitalize()} Protocol", f"Galactic {theme.capitalize()}",
                      f"Stars of {theme.capitalize()}"]
        }
        return random.choice(templates.get(genre, [f"The {theme.capitalize()} Story"]))
    
    def _generate_chapter_outlines(self, genre: str, theme: str, 
                                   num_chapters: int, protagonist: str, 
                                   antagonist: str) -> List[Dict]:
        """Generate chapter outlines based on genre"""
        outlines = []
        
        # Standard 3-act structure
        act1_chapters = max(1, num_chapters // 4)
        act2_chapters = num_chapters - act1_chapters - 1
        act3_chapters = 1
        
        chapter_num = 1
        
        # Act 1: Setup
        for i in range(act1_chapters):
            if i == 0:
                title = f"The Beginning"
                summary = f"{protagonist} lives an ordinary life until {antagonist} appears."
            else:
                title = f"The Call"
                summary = f"{protagonist} decides to face {antagonist}."
            outlines.append({"number": chapter_num, "title": title, "summary": summary})
            chapter_num += 1
        
        # Act 2: Confrontation
        for i in range(act2_chapters):
            titles = ["The Journey", "Trials", "Allies", "The Darkest Hour", "Preparation"]
            title = titles[i % len(titles)]
            summary = f"{protagonist} faces challenges and grows stronger."
            outlines.append({"number": chapter_num, "title": title, "summary": summary})
            chapter_num += 1
        
        # Act 3: Resolution
        title = "The Final Battle"
        summary = f"{protagonist} confronts {antagonist} in an epic showdown."
        outlines.append({"number": chapter_num, "title": title, "summary": summary})
        
        return outlines[:num_chapters]
    
    def _generate_chapters_with_llm(self, genre: str, theme: str,
                                    outlines: List[Dict], protagonist: str,
                                    antagonist: str, words_per_chapter: int) -> List[Dict]:
        """Generate chapter content using LLM"""
        chapters = []
        
        for outline in outlines:
            prompt = f"""Write chapter {outline['number']} of a {genre} story about {theme}.

Title: {outline['title']}
Summary: {outline['summary']}
Protagonist: {protagonist}
Antagonist: {antagonist}

Write approximately {words_per_chapter} words. Make it engaging and dramatic.
Include dialogue and vivid descriptions.

Chapter {outline['number']}: {outline['title']}

"""
            try:
                response = self.llm_backend.generate(prompt, max_tokens=words_per_chapter * 2)
                content = response
            except Exception as e:
                content = f"[Error generating content: {e}]\n\n{outline['summary']}"
            
            chapters.append({
                "number": outline['number'],
                "title": outline['title'],
                "content": content
            })
        
        return chapters
    
    def _generate_chapters_with_templates(self, outlines: List[Dict], 
                                          words_per_chapter: int) -> List[Dict]:
        """Generate chapter content using templates (fallback)"""
        chapters = []
        
        template = """
It was a dark and stormy night. The hero stood at the crossroads of destiny.
Before them lay the path to adventure. Behind them, the comfort of home.
"I must go forward," they whispered to themselves.

The journey was long and treacherous. They faced many challenges and met strange allies.
Each step brought them closer to their goal. Each victory made them stronger.

Finally, they reached the final confrontation. The battle was fierce.
But in the end, courage and determination won the day.

And so, the hero returned home, forever changed by their adventure.
"""
        
        for outline in outlines:
            # Repeat template to reach word count
            repeat_count = max(1, words_per_chapter // len(template))
            content = (template * repeat_count)[:words_per_chapter * 5]
            
            chapters.append({
                "number": outline['number'],
                "title": outline['title'],
                "content": content
            })
        
        return chapters
