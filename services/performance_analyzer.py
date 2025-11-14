import asyncio
from models.schemas import LLMRequest, PerformanceComparison, SequentialResponse, ParallelResponse
from services.sequential_generator import sequential_generator
from services.parallel_generator import parallel_generator
from datetime import datetime

class PerformanceAnalyzer:
    def __init__(self):
        pass

    async def run_performance_comparison(self, question: str) -> PerformanceComparison:
        """Run both sequential and parallel approaches and compare performance"""
        
        # Run both approaches concurrently to ensure fair comparison
        sequential_task = sequential_generator.generate_sequential_response(question)
        parallel_task = parallel_generator.generate_parallel_response(question)
        
        sequential_response, parallel_response = await asyncio.gather(
            sequential_task, 
            parallel_task
        )
        
        # Calculate performance metrics
        speedup_factor = sequential_response.generation_time_ms / parallel_response.total_generation_time_ms
        time_saved_ms = sequential_response.generation_time_ms - parallel_response.total_generation_time_ms
        
        return PerformanceComparison(
            question=question,
            sequential_response=sequential_response,
            parallel_response=parallel_response,
            speedup_factor=speedup_factor,
            time_saved_ms=time_saved_ms,
            timestamp=datetime.now()
        )

    def analyze_performance_metrics(self, comparison: PerformanceComparison) -> dict:
        """Generate detailed performance analysis"""
        return {
            "summary": {
                "speedup_factor": round(comparison.speedup_factor, 2),
                "time_saved_ms": round(comparison.time_saved_ms, 2),
                "time_saved_seconds": round(comparison.time_saved_ms / 1000, 2),
                "performance_improvement_percentage": round(
                    (comparison.time_saved_ms / comparison.sequential_response.generation_time_ms) * 100, 2
                )
            },
            "timing_breakdown": {
                "sequential_total_ms": comparison.sequential_response.generation_time_ms,
                "parallel_total_ms": comparison.parallel_response.total_generation_time_ms,
                "section_identification_ms": comparison.parallel_response.section_identification_time_ms,
                "parallel_generation_ms": comparison.parallel_response.parallel_generation_time_ms,
                "section_count": len(comparison.parallel_response.sections)
            },
            "content_metrics": {
                "sequential_words": comparison.sequential_response.word_count,
                "parallel_words": comparison.parallel_response.word_count,
                "word_difference": comparison.parallel_response.word_count - comparison.sequential_response.word_count,
                "words_per_second_sequential": round(
                    comparison.sequential_response.word_count / (comparison.sequential_response.generation_time_ms / 1000), 2
                ),
                "words_per_second_parallel": round(
                    comparison.parallel_response.word_count / (comparison.parallel_response.total_generation_time_ms / 1000), 2
                )
            },
            "section_performance": [
                {
                    "heading": section.heading,
                    "words": section.word_count,
                    "generation_time_ms": section.generation_time_ms,
                    "words_per_second": round(section.word_count / (section.generation_time_ms / 1000), 2)
                }
                for section in comparison.parallel_response.sections
            ]
        }

# Global instance
performance_analyzer = PerformanceAnalyzer()