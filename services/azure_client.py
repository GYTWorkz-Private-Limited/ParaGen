import os
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import asyncio
from typing import Optional

load_dotenv()

class AzureOpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not all([self.api_key, self.endpoint, self.api_version, self.deployment_name]):
            raise ValueError("Missing required Azure OpenAI configuration")
        
        self.client = AsyncAzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = 1500,
        temperature: float = 0.7
    ) -> str:
        """Generate a completion using Azure OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Azure OpenAI API error: {str(e)}")
    
    async def generate_multiple_completions(
        self, 
        prompts: list[str], 
        max_tokens: Optional[int] = 1500,
        temperature: float = 0.7
    ) -> list[str]:
        """Generate multiple completions in parallel"""
        tasks = [
            self.generate_completion(prompt, max_tokens, temperature) 
            for prompt in prompts
        ]
        return await asyncio.gather(*tasks)

# Global client instance
azure_client = AzureOpenAIClient()