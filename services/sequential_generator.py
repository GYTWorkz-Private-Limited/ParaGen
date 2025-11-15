import time
from models.schemas import SequentialResponse
from services.openai_client import get_openai_client
from prompts.section_prompts import SEQUENTIAL_GENERATION_PROMPT
from datetime import datetime

class SequentialGenerator:
    def __init__(self):
        pass

    async def generate_sequential_response(self, question: str) -> SequentialResponse:
        """Generate a complete response using traditional sequential approach"""
        start_time = time.time()
        
        prompt = SEQUENTIAL_GENERATION_PROMPT.format(question=question)
        
        try:
            content = await get_openai_client().generate_completion(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            end_time = time.time()
            generation_time = (end_time - start_time) * 1000
            word_count = len(content.split())
            
            return SequentialResponse(
                answer=content.strip(),
                generation_time_ms=generation_time,
                word_count=word_count,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            raise Exception(f"Sequential generation failed: {str(e)}")

# Global instance
sequential_generator = SequentialGenerator()