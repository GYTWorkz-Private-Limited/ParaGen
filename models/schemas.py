from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class SectionInfo(BaseModel):
    section_heading: str = Field(..., description="The heading of the section")
    section_content_size_in_words: int = Field(..., description="Estimated number of words for this section")

class SectionIdentificationResponse(BaseModel):
    sections: List[SectionInfo] = Field(..., description="List of identified sections")

class GeneratedSection(BaseModel):
    heading: str
    content: str
    word_count: int
    generation_time_ms: float

class LLMRequest(BaseModel):
    question: str = Field(..., description="The user's question to be answered")

class SequentialResponse(BaseModel):
    answer: str
    generation_time_ms: float
    word_count: int
    timestamp: datetime

class ParallelResponse(BaseModel):
    answer: str
    sections: List[GeneratedSection]
    total_generation_time_ms: float
    section_identification_time_ms: float
    parallel_generation_time_ms: float
    word_count: int
    timestamp: datetime

class PerformanceComparison(BaseModel):
    question: str
    sequential_response: SequentialResponse
    parallel_response: ParallelResponse
    speedup_factor: float
    time_saved_ms: float
    timestamp: datetime