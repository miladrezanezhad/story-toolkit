"""
Text Analyzer Module
====================
Analyzes text characteristics for story development.

Author: Milad Rezanezhad
GitHub: https://github.com/miladrezanezhad
"""

import re
from typing import Dict, List, Tuple
from collections import Counter

class TextAnalyzer:
    """Analyzes text properties and readability"""
    
    def __init__(self):
        self.readability_thresholds = {
            "easy": 80,
            "moderate": 60,
            "challenging": 40,
            "difficult": 0
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        analysis = {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": self._calculate_avg_words(words, sentences),
            "avg_word_length": self._calculate_avg_word_length(words),
            "unique_words": len(set(words)),
            "vocabulary_richness": self._calculate_vocabulary_richness(words),
            "readability_score": self._calculate_readability(text),
            "reading_level": self._determine_reading_level(text),
            "common_words": self._get_common_words(words, 10),
            "sentence_variety": self._analyze_sentence_variety(sentences)
        }
        
        return analysis
    
    def analyze_readability(self, text: str) -> Dict:
        """
        Analyze text readability.
        
        Args:
            text: Text to analyze
            
        Returns:
            Readability metrics
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        avg_words = len(words) / max(len(sentences), 1)
        avg_word_len = sum(len(word) for word in words) / max(len(words), 1)
        
        # Simple readability score (higher = easier to read)
        score = 100 - (avg_words * 2 + avg_word_len * 10)
        score = max(0, min(100, score))
        
        return {
            "score": round(score, 1),
            "level": self._determine_reading_level(text),
            "avg_words_per_sentence": round(avg_words, 1),
            "avg_word_length": round(avg_word_len, 1)
        }
    
    def analyze_dialogue(self, dialogue_lines: List[str]) -> Dict:
        """
        Analyze dialogue characteristics.
        
        Args:
            dialogue_lines: List of dialogue lines
            
        Returns:
            Dialogue analysis
        """
        if not dialogue_lines:
            return {}
        
        total_words = 0
        speaker_counts = Counter()
        emotions_detected = []
        
        for line in dialogue_lines:
            # Extract speaker and text
            match = re.match(r'^([^:]+):\s*(.+)', line)
            if match:
                speaker = match.group(1)
                text = match.group(2)
                
                speaker_counts[speaker] += 1
                words = text.split()
                total_words += len(words)
                
                # Simple emotion detection
                emotions = self._detect_emotions(text)
                emotions_detected.extend(emotions)
        
        return {
            "total_lines": len(dialogue_lines),
            "total_words": total_words,
            "avg_words_per_line": total_words / max(len(dialogue_lines), 1),
            "speakers": dict(speaker_counts),
            "dominant_emotions": Counter(emotions_detected).most_common(3),
            "dialogue_balance": self._calculate_dialogue_balance(speaker_counts)
        }
    
    def analyze_pacing(self, text: str, chunk_size: int = 100) -> Dict:
        """
        Analyze story pacing by examining text chunks.
        
        Args:
            text: Full text to analyze
            chunk_size: Size of text chunks in words
            
        Returns:
            Pacing analysis
        """
        words = text.split()
        chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]
        
        pacing_data = []
        for i, chunk in enumerate(chunks):
            chunk_text = ' '.join(chunk)
            sentences = re.split(r'[.!?]+', chunk_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            pacing_data.append({
                "chunk": i + 1,
                "word_count": len(chunk),
                "sentence_count": len(sentences),
                "avg_sentence_length": len(chunk) / max(len(sentences), 1),
                "action_words": self._count_action_words(chunk_text),
                "descriptive_words": self._count_descriptive_words(chunk_text)
            })
        
        return {
            "chunks_analyzed": len(chunks),
            "pacing_data": pacing_data,
            "pacing_variance": self._calculate_pacing_variance(pacing_data)
        }
    
    def _calculate_avg_words(self, words: List[str], sentences: List[str]) -> float:
        """Calculate average words per sentence"""
        return len(words) / max(len(sentences), 1)
    
    def _calculate_avg_word_length(self, words: List[str]) -> float:
        """Calculate average word length"""
        return sum(len(word) for word in words) / max(len(words), 1)
    
    def _calculate_vocabulary_richness(self, words: List[str]) -> float:
        """Calculate vocabulary richness (unique words ratio)"""
        return len(set(words)) / max(len(words), 1)
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        avg_words = len(words) / max(len(sentences), 1)
        avg_word_len = sum(len(word) for word in words) / max(len(words), 1)
        
        score = 100 - (avg_words * 2 + avg_word_len * 10)
        return max(0, min(100, score))
    
    def _determine_reading_level(self, text: str) -> str:
        """Determine the reading level of the text"""
        score = self._calculate_readability(text)
        
        if score >= self.readability_thresholds["easy"]:
            return "easy"
        elif score >= self.readability_thresholds["moderate"]:
            return "moderate"
        elif score >= self.readability_thresholds["challenging"]:
            return "challenging"
        else:
            return "difficult"
    
    def _get_common_words(self, words: List[str], n: int = 10) -> List[Tuple[str, int]]:
        """Get most common words"""
        # Filter out short/common words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", 
                     "to", "for", "of", "with", "by", "from", "is", "was", "are"}
        filtered_words = [w.lower() for w in words if w.lower() not in stop_words and len(w) > 2]
        return Counter(filtered_words).most_common(n)
    
    def _analyze_sentence_variety(self, sentences: List[str]) -> Dict:
        """Analyze sentence structure variety"""
        lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if not lengths:
            return {"variety": "no sentences found"}
        
        return {
            "shortest": min(lengths) if lengths else 0,
            "longest": max(lengths) if lengths else 0,
            "average": sum(lengths) / len(lengths) if lengths else 0,
            "variety_score": "high" if max(lengths) - min(lengths) > 15 else "low"
        }
    
    def _detect_emotions(self, text: str) -> List[str]:
        """Simple emotion detection in text"""
        emotion_keywords = {
            "angry": ["angry", "furious", "mad", "rage", "hate"],
            "sad": ["sad", "sorrow", "cry", "tears", "grief"],
            "happy": ["happy", "joy", "wonderful", "great", "love"],
            "fearful": ["scared", "afraid", "fear", "terrified", "horror"],
            "surprised": ["surprised", "shocked", "amazed", "unexpected"]
        }
        
        detected = []
        text_lower = text.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected.append(emotion)
        
        return detected
    
    def _calculate_dialogue_balance(self, speaker_counts: Counter) -> str:
        """Calculate balance between speakers"""
        if len(speaker_counts) < 2:
            return "single_speaker"
        
        values = list(speaker_counts.values())
        ratio = min(values) / max(values) if max(values) > 0 else 0
        
        if ratio > 0.7:
            return "balanced"
        elif ratio > 0.4:
            return "moderately_balanced"
        else:
            return "unbalanced"
    
    def _count_action_words(self, text: str) -> int:
        """Count action-oriented words"""
        action_verbs = ["run", "jump", "fight", "strike", "chase", "shoot", 
                       "throw", "break", "crash", "explode", "race", "battle"]
        return sum(1 for word in text.lower().split() if word in action_verbs)
    
    def _count_descriptive_words(self, text: str) -> int:
        """Count descriptive adjectives"""
        common_adjectives = ["beautiful", "dark", "bright", "cold", "hot", 
                           "ancient", "massive", "tiny", "strange", "familiar"]
        return sum(1 for word in text.lower().split() if word in common_adjectives)
    
    def _calculate_pacing_variance(self, pacing_data: List[Dict]) -> float:
        """Calculate variance in pacing across chunks"""
        if len(pacing_data) < 2:
            return 0.0
        
        lengths = [chunk["avg_sentence_length"] for chunk in pacing_data]
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        
        return round(variance, 2)
    
    def __str__(self) -> str:
        return "TextAnalyzer()"
