import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
from typing import Optional, List

load_dotenv()

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.endpoint = os.getenv("OPENAI_ENDPOINT")
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4.1-mini")
        
        if not self.api_key:
            raise ValueError("Missing required OpenAI API key. Please set OPENAI_API_KEY environment variable.")
        
        if not self.endpoint:
            raise ValueError("Missing required OpenAI endpoint. Please set OPENAI_ENDPOINT environment variable.")
        
        # Configure client for Azure OpenAI using standard OpenAI SDK interface
        base_url = f"{self.endpoint.rstrip('/')}/openai/v1/"
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = 1500,
        temperature: float = 0.7
    ) -> str:
        """Generate a completion using OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_multiple_completions(
        self, 
        prompts: List[str], 
        max_tokens: Optional[int] = 1500,
        temperature: float = 0.7
    ) -> List[str]:
        """Generate multiple completions in parallel"""
        tasks = [
            self.generate_completion(prompt, max_tokens, temperature) 
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)

# Global client instance - will be instantiated when needed
openai_client = None

def get_openai_client():
    global openai_client
    if openai_client is None:
        openai_client = OpenAIClient()
    return openai_client