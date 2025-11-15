import re
from typing import Optional, Tuple
from enum import Enum

class QueryType(Enum):
    SIMPLE_GREETING = "simple_greeting"
    SIMPLE_QUESTION = "simple_question"
    COMPLEX_QUERY = "complex_query"

class QueryClassifier:
    def __init__(self):
        # Simple greeting patterns
        self.greeting_patterns = [
            r'^(hi|hello|hey|greetings)\.?$',
            r'^(hi|hello|hey) there\.?$',
            r'^good (morning|afternoon|evening)\.?$',
            r'^how are you\??$',
            r'^what\'?s up\??$',
            r'^howdy\.?$',
            r'^(yo|sup)\.?$'
        ]
        
        # Simple question patterns (short, non-complex)
        self.simple_question_patterns = [
            r'^what is \w+\??$',
            r'^who is \w+\??$',
            r'^when is \w+\??$',
            r'^where is \w+\??$',
            r'^how do I \w+\??$',
            r'^what time is it\??$',
            r'^what\'?s the weather\??$'
        ]
        
        # Complexity indicators
        self.complexity_keywords = [
            'explain', 'analyze', 'compare', 'describe', 'discuss',
            'implementation', 'architecture', 'strategy', 'approach',
            'benefits', 'challenges', 'advantages', 'disadvantages',
            'process', 'steps', 'methodology', 'framework',
            'best practices', 'considerations', 'factors',
            'install', 'installing', 'setup', 'configure', 'guide',
            'tutorial', 'instructions', 'procedure'
        ]

    def classify_query(self, question: str) -> Tuple[QueryType, str]:
        """
        Classify the query type and return classification with reasoning
        """
        question_clean = question.strip().lower()
        
        # Check for simple greetings
        for pattern in self.greeting_patterns:
            if re.match(pattern, question_clean, re.IGNORECASE):
                return QueryType.SIMPLE_GREETING, "Detected simple greeting pattern"
        
        # Check for very short queries (likely simple)
        if len(question_clean.split()) <= 3:
            for pattern in self.simple_question_patterns:
                if re.match(pattern, question_clean, re.IGNORECASE):
                    return QueryType.SIMPLE_QUESTION, "Detected simple question pattern"
            
            # If it's very short but not a recognized pattern, still treat as simple
            if len(question_clean.split()) <= 2:
                return QueryType.SIMPLE_QUESTION, "Very short query, treating as simple"
        
        # Check for complexity indicators
        complexity_score = 0
        words = question_clean.split()
        
        for keyword in self.complexity_keywords:
            if keyword in question_clean:
                complexity_score += 1
        
        # Length-based complexity
        word_count = len(words)
        if word_count > 15:
            complexity_score += 1
        if word_count > 25:
            complexity_score += 2
        
        # Question words that suggest complexity
        complex_question_words = ['how', 'why', 'what', 'when', 'where', 'which']
        question_word_count = sum(1 for word in words if word in complex_question_words)
        if question_word_count > 1:
            complexity_score += 1
        
        # Multiple sentences suggest complexity
        if len(question.split('.')) > 2 or len(question.split('?')) > 2:
            complexity_score += 1
        
        if complexity_score >= 1:  # Lowered threshold - if any complexity indicator is found
            return QueryType.COMPLEX_QUERY, f"Complexity score: {complexity_score}"
        elif word_count > 6:  # Lowered length threshold for medium queries
            return QueryType.COMPLEX_QUERY, "Medium-length query, treating as complex"
        else:
            return QueryType.SIMPLE_QUESTION, "Short query without complexity indicators"

    def should_use_parallel_generation(self, question: str) -> bool:
        """
        Determine if parallel generation is worth using for this query
        """
        query_type, _ = self.classify_query(question)
        return query_type == QueryType.COMPLEX_QUERY

    def estimate_sections_needed(self, question: str) -> int:
        """
        Estimate how many sections a complex query might need
        """
        query_type, _ = self.classify_query(question)
        
        if query_type != QueryType.COMPLEX_QUERY:
            return 1
        
        question_lower = question.lower()
        
        # Count topic indicators
        topic_indicators = [
            'and', 'also', 'additionally', 'furthermore', 'moreover',
            'benefits', 'challenges', 'advantages', 'disadvantages',
            'implementation', 'deployment', 'architecture', 'design',
            'best practices', 'considerations', 'approaches', 'methods'
        ]
        
        topic_count = sum(1 for indicator in topic_indicators if indicator in question_lower)
        
        # Base sections + topic indicators
        estimated_sections = max(3, min(6, 3 + topic_count))
        
        return estimated_sections

# Global instance
query_classifier = QueryClassifier()