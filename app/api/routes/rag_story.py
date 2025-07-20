"""
RAG-Enhanced Story Generation API
Provides endpoints for RAG-enhanced story generation with research metrics
"""

import os
import time
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.api.models.chat import ChatRequest, ChatResponse
from app.config.settings import get_configuration, get_generation_kwargs
from app.services.rag.story_generator import RAGStoryGenerator
from app.research.rag_metrics import RAGMetricsCollector
import openai

router = APIRouter(prefix="/api/v1/rag", tags=["rag-story"])

# Get configuration
config = get_configuration()
gen_kwargs = get_generation_kwargs()

# Initialize the OpenAI async client
client = openai.AsyncClient(
    api_key=config["api_key"], 
    base_url=config["endpoint_url"]
)

# Initialize RAG components
rag_generator = RAGStoryGenerator(client)
metrics_collector = RAGMetricsCollector()

class RAGStoryRequest(BaseModel):
    """Request model for RAG story generation"""
    user_request: str
    use_rag: bool = True
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 5000
    n_retrieved_stories: int = 3

class RAGStoryResponse(BaseModel):
    """Response model for RAG story generation"""
    story_content: str
    rag_enabled: bool
    generation_time: float
    word_count: int
    retrieved_stories_count: int
    retrieved_themes: List[str]
    retrieved_characters: List[str]
    similarity_scores: List[float]
    educational_value_score: Optional[float] = None
    engagement_score: Optional[float] = None
    coherence_score: Optional[float] = None
    moral_lesson_present: bool = False

class RAGComparisonRequest(BaseModel):
    """Request model for RAG comparison"""
    user_request: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 5000

class RAGComparisonResponse(BaseModel):
    """Response model for RAG comparison"""
    user_request: str
    stories: Dict[str, Dict[str, Any]]
    comparison: Dict[str, Any]

@router.post("/generate", response_model=RAGStoryResponse)
async def generate_rag_story(request: RAGStoryRequest):
    """
    Generate a story with optional RAG enhancement.
    
    Args:
        request: RAG story generation request
        
    Returns:
        RAG story response with metrics
    """
    try:
        start_time = time.time()
        
        # Generate story with quality analysis
        result = await rag_generator.generate_story_with_quality_analysis(
            user_request=request.user_request,
            use_rag=request.use_rag,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        total_time = time.time() - start_time
        
        # Extract metrics
        metrics = result["metrics"]
        quality = result["quality_analysis"]
        
        return RAGStoryResponse(
            story_content=result["story_content"],
            rag_enabled=result["rag_enabled"],
            generation_time=metrics.generation_time,
            word_count=metrics.word_count,
            retrieved_stories_count=metrics.retrieved_stories_count,
            retrieved_themes=metrics.retrieved_themes,
            retrieved_characters=metrics.retrieved_characters,
            similarity_scores=metrics.similarity_scores,
            educational_value_score=quality["educational_value_score"],
            engagement_score=quality["engagement_score"],
            coherence_score=quality["coherence_score"],
            moral_lesson_present=quality["moral_lesson_present"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

@router.post("/compare", response_model=RAGComparisonResponse)
async def compare_rag_stories(request: RAGComparisonRequest):
    """
    Generate both RAG and non-RAG stories for comparison.
    
    Args:
        request: RAG comparison request
        
    Returns:
        Comparison response with both stories and metrics
    """
    try:
        start_time = time.time()
        
        # Generate comparison stories
        comparison = await rag_generator.generate_comparison_stories(
            user_request=request.user_request,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        total_time = time.time() - start_time
        
        # Record session for research
        session_id = metrics_collector.start_session()
        session = metrics_collector.record_comparison_session(
            user_request=request.user_request,
            story_without_rag=comparison["stories"]["without_rag"]["content"],
            story_with_rag=comparison["stories"]["with_rag"]["content"],
            metrics_without_rag=comparison["stories"]["without_rag"]["metrics"],
            metrics_with_rag=comparison["stories"]["with_rag"]["metrics"],
            total_time=total_time
        )
        
        return RAGComparisonResponse(
            user_request=comparison["user_request"],
            stories=comparison["stories"],
            comparison=comparison["comparison"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@router.get("/metrics/summary")
async def get_rag_metrics_summary():
    """
    Get summary of RAG research metrics.
    
    Returns:
        Summary of collected RAG metrics
    """
    try:
        summary = metrics_collector.generate_research_summary()
        return {
            "total_sessions": summary.total_sessions,
            "success_rate": summary.success_rate,
            "avg_generation_time_without_rag": summary.avg_generation_time_without_rag,
            "avg_generation_time_with_rag": summary.avg_generation_time_with_rag,
            "avg_rag_overhead": summary.avg_rag_overhead,
            "avg_quality_improvement": summary.avg_quality_improvement,
            "most_common_themes": summary.most_common_themes,
            "most_common_characters": summary.most_common_characters,
            "avg_similarity_score": summary.avg_similarity_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

@router.post("/metrics/export")
async def export_rag_metrics():
    """
    Export RAG research metrics to files.
    
    Returns:
        File paths of exported metrics
    """
    try:
        export_result = metrics_collector.export_metrics()
        return {
            "message": "Metrics exported successfully",
            "files": export_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/retrieve")
async def retrieve_relevant_stories(
    query: str = Query(..., description="Search query"),
    n_results: int = Query(3, description="Number of results to retrieve")
):
    """
    Retrieve relevant stories from the vector store.
    
    Args:
        query: Search query
        n_results: Number of results to retrieve
        
    Returns:
        Retrieved stories with similarity scores
    """
    try:
        from app.services.rag.retriever import RAGRetriever
        retriever = RAGRetriever()
        
        result = retriever.smart_retrieve(query, n_results=n_results)
        
        return {
            "query": query,
            "stories": [
                {
                    "title": story.title,
                    "content": story.content,
                    "moral": story.moral,
                    "similarity_score": story.similarity_score,
                    "themes": story.themes,
                    "characters": story.characters,
                    "age_group": story.age_group
                }
                for story in result.get("stories", [])
            ],
            "context": result.get("context", {}),
            "prompt_addition": result.get("prompt_addition", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

@router.get("/health")
async def rag_health_check():
    """
    Health check for RAG system.
    
    Returns:
        Health status of RAG components
    """
    try:
        # Check if vector store exists
        vector_store_exists = os.path.exists("chroma_db")
        
        # Check if retriever works
        from app.services.rag.retriever import RAGRetriever
        retriever = RAGRetriever()
        test_result = retriever.smart_retrieve("test", n_results=1)
        retriever_works = len(test_result.get("stories", [])) > 0
        
        return {
            "status": "healthy",
            "vector_store_exists": vector_store_exists,
            "retriever_works": retriever_works,
            "total_sessions": len(metrics_collector.sessions)
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "vector_store_exists": os.path.exists("chroma_db"),
            "retriever_works": False,
            "total_sessions": len(metrics_collector.sessions)
        } 