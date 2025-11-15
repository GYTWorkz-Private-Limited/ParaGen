import asyncio
import time
from typing import List
from models.schemas import SectionInfo, GeneratedSection, ParallelResponse
from services.openai_client import get_openai_client
from services.section_identifier import section_identifier
from prompts.advanced_prompts import get_section_prompt
from datetime import datetime

class ParallelGenerator:
    def __init__(self):
        pass

    async def generate_section_content(
        self, 
        main_question: str, 
        section: SectionInfo
    ) -> GeneratedSection:
        """Generate content for a single section"""
        start_time = time.time()
        
        # Use advanced prompt selection based on section type
        prompt = get_section_prompt(
            section_heading=section.section_heading,
            question=main_question,
            target_words=section.section_content_size_in_words
        )
        
        try:
            content = await get_openai_client().generate_completion(
                prompt=prompt,
                max_tokens=min(section.section_content_size_in_words * 2, 1500),
                temperature=0.7
            )
            
            end_time = time.time()
            generation_time = (end_time - start_time) * 1000
            word_count = len(content.split())
            
            return GeneratedSection(
                heading=section.section_heading,
                content=content.strip(),
                word_count=word_count,
                generation_time_ms=generation_time
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate section '{section.section_heading}': {str(e)}")

    async def generate_parallel_response(self, question: str) -> ParallelResponse:
        """Generate a complete response using parallel section generation"""
        overall_start_time = time.time()
        
        # Step 1: Identify sections
        section_response, identification_time = await section_identifier.identify_sections(question)
        sections_info = section_response.sections
        
        # Step 2: Generate all sections in parallel
        parallel_start_time = time.time()
        
        # Create tasks for parallel execution
        tasks = [
            self.generate_section_content(question, section_info)
            for section_info in sections_info
        ]
        
        # Execute all tasks in parallel
        generated_sections = await asyncio.gather(*tasks)
        
        parallel_end_time = time.time()
        parallel_generation_time = (parallel_end_time - parallel_start_time) * 1000
        
        # Step 3: Assemble the final response
        assembled_answer = self._assemble_response(generated_sections)
        
        overall_end_time = time.time()
        total_time = (overall_end_time - overall_start_time) * 1000
        
        total_word_count = sum(section.word_count for section in generated_sections)
        
        return ParallelResponse(
            answer=assembled_answer,
            sections=generated_sections,
            total_generation_time_ms=total_time,
            section_identification_time_ms=identification_time,
            parallel_generation_time_ms=parallel_generation_time,
            word_count=total_word_count,
            timestamp=datetime.now()
        )

    def _assemble_response(self, sections: List[GeneratedSection]) -> str:
        """Assemble the final response from generated sections"""
        assembled_parts = []
        
        for i, section in enumerate(sections, 1):
            assembled_parts.append(f"{i}. {section.heading}")
            assembled_parts.append(section.content)
            assembled_parts.append("")  # Add spacing between sections
        
        return "\n".join(assembled_parts).strip()

# Global instance
parallel_generator = ParallelGenerator()