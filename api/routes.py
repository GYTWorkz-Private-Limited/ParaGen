from fastapi import APIRouter, HTTPException
from models.schemas import (
    LLMRequest, 
    SequentialResponse, 
    ParallelResponse, 
    SectionIdentificationResponse
)
from services.sequential_generator import sequential_generator
from services.parallel_generator import parallel_generator
from services.performance_analyzer import performance_analyzer
from services.section_identifier import section_identifier
from services.query_classifier import query_classifier, QueryType
from services.simple_responder import simple_responder

router = APIRouter()

@router.post("/generate/sequential", response_model=SequentialResponse)
async def generate_sequential_response(request: LLMRequest):
    """Generate response using traditional sequential approach"""
    try:
        # Check if this is a simple query that can be handled without LLM
        query_type, reasoning = query_classifier.classify_query(request.question)
        
        if simple_responder.should_bypass_llm(request.question, query_type):
            if query_type == QueryType.SIMPLE_GREETING:
                return simple_responder.generate_greeting_response()
            else:
                return simple_responder.generate_simple_response(request.question)
        
        # Use normal sequential generation for complex queries
        response = await sequential_generator.generate_sequential_response(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate/parallel", response_model=ParallelResponse)
async def generate_parallel_response(request: LLMRequest):
    """Generate response using parallel section-based approach"""
    try:
        # Always use parallel generation when this endpoint is called
        # This is the core feature of ParaGen - let users decide when to use it
        response = await parallel_generator.generate_parallel_response(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/sections", response_model=SectionIdentificationResponse)
async def analyze_sections(request: LLMRequest):
    """Identify sections for a given question"""
    try:
        response, _ = await section_identifier.identify_sections(request.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare/performance")
async def compare_performance(request: LLMRequest):
    """Run performance comparison between sequential and parallel approaches"""
    try:
        # Check if this query is worth comparing
        query_type, reasoning = query_classifier.classify_query(request.question)
        
        if query_type != QueryType.COMPLEX_QUERY:
            return {
                "message": "Simple query detected - parallel generation not beneficial",
                "query_type": query_type.value,
                "reasoning": reasoning,
                "recommendation": "Use sequential generation for simple queries like this",
                "estimated_sections": query_classifier.estimate_sections_needed(request.question),
                "simple_response": simple_responder.generate_simple_response(request.question) if query_type == QueryType.SIMPLE_QUESTION else simple_responder.generate_greeting_response()
            }
        
        # Run full comparison for complex queries
        comparison = await performance_analyzer.run_performance_comparison(request.question)
        analysis = performance_analyzer.analyze_performance_metrics(comparison)
        
        return {
            "comparison": comparison,
            "analysis": analysis,
            "query_classification": {
                "type": query_type.value,
                "reasoning": reasoning,
                "estimated_sections": query_classifier.estimate_sections_needed(request.question)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Parallel LLM API is running"}

@router.post("/classify/query")
async def classify_query(request: LLMRequest):
    """Classify query complexity and recommend approach"""
    try:
        query_type, reasoning = query_classifier.classify_query(request.question)
        estimated_sections = query_classifier.estimate_sections_needed(request.question)
        should_parallel = query_classifier.should_use_parallel_generation(request.question)
        
        return {
            "question": request.question,
            "classification": {
                "type": query_type.value,
                "reasoning": reasoning,
                "should_use_parallel": should_parallel,
                "estimated_sections": estimated_sections
            },
            "recommendations": {
                "best_approach": "parallel" if should_parallel else "sequential",
                "expected_speedup": "2-5x" if should_parallel else "N/A (simple query)",
                "bypass_llm": simple_responder.should_bypass_llm(request.question, query_type)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get API statistics and capabilities"""
    return {
        "api_version": "1.0.0",
        "features": {
            "sequential_generation": True,
            "parallel_generation": True,
            "section_identification": True,
            "performance_comparison": True,
            "query_classification": True,
            "intelligent_routing": True
        },
        "llm_provider": "Azure OpenAI",
        "supported_operations": [
            "/generate/sequential",
            "/generate/parallel", 
            "/analyze/sections",
            "/compare/performance",
            "/classify/query"
        ],
        "intelligence": {
            "simple_greeting_detection": True,
            "complexity_analysis": True,
            "automatic_optimization": True
        }
    }