import time
import random
from datetime import datetime
from models.schemas import SequentialResponse
from services.query_classifier import QueryType

class SimpleResponder:
    def __init__(self):
        self.greeting_responses = [
            "Hi there! I'm ParaGen, your parallel AI assistant. How can I help you today?",
            "Hello! Welcome to ParaGen. What would you like to explore?",
            "Hey! I'm here to help with fast, comprehensive answers. What's on your mind?",
            "Greetings! I'm ParaGen - ask me anything complex and I'll break it down quickly.",
            "Hi! Ready to experience lightning-fast AI responses? What can I assist you with?"
        ]
        
        self.simple_question_responses = {
            "thank you": "You're welcome! Is there anything else I can help you with?",
            "thanks": "My pleasure! Feel free to ask me any complex questions.",
            "bye": "Goodbye! Come back anytime for fast, detailed answers.",
            "goodbye": "See you later! Remember, I'm here for comprehensive AI assistance.",
            "test": "ParaGen is working perfectly! Try asking me a complex question to see parallel generation in action.",
            "ping": "Pong! ParaGen is online and ready for complex queries.",
            "help": "I'm ParaGen, designed for fast parallel response generation. Ask me complex questions about technology, processes, explanations, or any topic that needs detailed coverage!"
        }

    def generate_greeting_response(self) -> SequentialResponse:
        """Generate a quick response for simple greetings"""
        start_time = time.time()
        
        response_text = random.choice(self.greeting_responses)
        
        end_time = time.time()
        generation_time = (end_time - start_time) * 1000
        
        return SequentialResponse(
            answer=response_text,
            generation_time_ms=generation_time,
            word_count=len(response_text.split()),
            timestamp=datetime.now()
        )

    def generate_simple_response(self, question: str) -> SequentialResponse:
        """Generate a quick response for simple questions"""
        start_time = time.time()
        
        question_lower = question.lower().strip()
        
        # Check for known simple responses
        for key, response in self.simple_question_responses.items():
            if key in question_lower:
                end_time = time.time()
                generation_time = (end_time - start_time) * 1000
                
                return SequentialResponse(
                    answer=response,
                    generation_time_ms=generation_time,
                    word_count=len(response.split()),
                    timestamp=datetime.now()
                )
        
        # Default simple response
        response_text = f"I understand you're asking about '{question}'. For simple queries like this, I can provide quick answers, but I'm optimized for complex questions that benefit from parallel processing. Try asking me something more detailed!"
        
        end_time = time.time()
        generation_time = (end_time - start_time) * 1000
        
        return SequentialResponse(
            answer=response_text,
            generation_time_ms=generation_time,
            word_count=len(response_text.split()),
            timestamp=datetime.now()
        )

    def should_bypass_llm(self, question: str, query_type: QueryType) -> bool:
        """
        Determine if we should bypass LLM entirely for very simple queries
        """
        if query_type == QueryType.SIMPLE_GREETING:
            return True
            
        question_lower = question.lower().strip()
        
        # Known simple patterns that don't need LLM
        bypass_patterns = [
            "thank you", "thanks", "bye", "goodbye", 
            "test", "ping", "help", "hello", "hi"
        ]
        
        return any(pattern in question_lower for pattern in bypass_patterns)

# Global instance
simple_responder = SimpleResponder()