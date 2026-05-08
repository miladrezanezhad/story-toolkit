"""
Dialogue prompt templates for LLM

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

DIALOGUE_PROMPTS = {
    "conflict": """
Generate a tense conflict dialogue between {speaker} and {listener}.
The conversation should show rising tension and emotional stakes.
Style: {style}
Number of lines: {num_lines}
""",
    "friendship": """
Generate a warm friendship dialogue between {speaker} and {listener}.
The conversation should show trust and mutual respect.
Style: {style}
Number of lines: {num_lines}
""",
    "love": """
Generate a romantic dialogue between {speaker} and {listener}.
The conversation should be heartfelt and emotional.
Style: {style}
Number of lines: {num_lines}
""",
    "betrayal": """
Generate a dramatic betrayal dialogue between {speaker} and {listener}.
One character reveals a shocking truth to the other.
Style: {style}
Number of lines: {num_lines}
"""
}

CHARACTER_PROMPTS = {
    "protagonist": "Create a heroic protagonist with a tragic backstory.",
    "antagonist": "Create a compelling villain with understandable motivations.",
    "mentor": "Create a wise mentor figure with mysterious knowledge.",
    "supporting": "Create a loyal supporting character with unique skills."
}

PLOT_PROMPTS = {
    "fantasy": "Create a fantasy plot about a hero's journey.",
    "mystery": "Create a mystery plot with unexpected twists.",
    "romance": "Create a romance plot with emotional obstacles."
}