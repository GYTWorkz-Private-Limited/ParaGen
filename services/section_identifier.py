import csv
import io
import time
from models.schemas import SectionInfo, SectionIdentificationResponse
from services.azure_client import azure_client
from prompts.section_prompts import SECTION_IDENTIFICATION_PROMPT

class SectionIdentifier:
    def __init__(self):
        pass

    async def identify_sections(self, question: str) -> SectionIdentificationResponse:
        """
        Identify logical sections for the given question using LLM
        """
        start_time = time.time()
        
        prompt = SECTION_IDENTIFICATION_PROMPT.format(question=question)
        
        try:
            response = await azure_client.generate_completion(
                prompt=prompt,
                max_tokens=800,
                temperature=0.3
            )
            
            # Parse CSV response
            csv_data = response.strip()
            sections = []
            
            # Use StringIO to read CSV from string
            csv_reader = csv.reader(io.StringIO(csv_data))
            
            for row in csv_reader:
                if len(row) >= 2:  # Ensure we have both heading and word count
                    try:
                        section_heading = row[0].strip()
                        word_count = int(row[1].strip())
                        
                        sections.append(SectionInfo(
                            section_heading=section_heading,
                            section_content_size_in_words=word_count
                        ))
                    except (ValueError, IndexError) as e:
                        # Skip malformed rows
                        continue
            
            if not sections:
                raise Exception("No valid sections found in CSV response")
            
            end_time = time.time()
            identification_time = (end_time - start_time) * 1000
            
            return SectionIdentificationResponse(sections=sections), identification_time
            
        except Exception as e:
            raise Exception(f"Section identification failed: {str(e)}")

# Global instance
section_identifier = SectionIdentifier()