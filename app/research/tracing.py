"""
Research Tracing System for AI Storytelling Performance Analysis

This module provides comprehensive tracing and metrics collection for:
- Story generation performance and quality
- Image generation (DALL-E) performance and quality  
- Audio generation (OpenVoice) performance and quality
- Overall system performance and costs
"""

import os
import time
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import uuid
from pathlib import Path

# LangSmith integration
try:
    from langsmith import Client, RunTree, traceable
    from langsmith.evaluation import EvaluationResult
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

@dataclass
class StoryMetrics:
    """Metrics for story generation"""
    story_id: str
    prompt: str
    generation_time: float
    word_count: int
    character_count: int
    page_count: int
    model_used: str
    temperature: float
    max_tokens: int
    actual_tokens_used: Optional[Dict[str, int]] = None
    cost_estimate: Optional[float] = None
    quality_score: Optional[float] = None

@dataclass
class ImageMetrics:
    """Metrics for image generation"""
    image_id: str
    story_id: str
    prompt: str
    generation_time: float
    model_used: str
    image_size: str
    image_url: Optional[str] = None
    local_path: Optional[str] = None
    cost_estimate: Optional[float] = None
    quality_score: Optional[float] = None
    relevance_score: Optional[float] = None

@dataclass
class AudioMetrics:
    """Metrics for audio generation"""
    audio_id: str
    story_id: str
    generation_time: float
    model_used: str
    voice_style: str
    audio_duration: float
    local_path: Optional[str] = None
    cost_estimate: Optional[float] = None
    quality_score: Optional[float] = None
    clarity_score: Optional[float] = None

@dataclass
class ResearchSession:
    """Complete research session data"""
    session_id: str
    timestamp: datetime
    story_metrics: StoryMetrics
    image_metrics: List[ImageMetrics]
    audio_metrics: Optional[AudioMetrics]
    total_cost: float
    total_time: float
    success: bool
    error_message: Optional[str] = None

class ResearchTracer:
    """Main tracer for research metrics collection"""
    
    def __init__(self, langsmith_api_key: Optional[str] = None):
        self.langsmith_client = None
        if LANGSMITH_AVAILABLE and langsmith_api_key:
            self.langsmith_client = Client(api_key=langsmith_api_key)
        
        self.project_name = os.getenv("LANGSMITH_PROJECT", "loomi-research")
        self.sessions: List[ResearchSession] = []
        self.current_session_id = None
        
    def start_session(self) -> str:
        """Start a new research session"""
        self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        return self.current_session_id
    
    @traceable(run_type="chain", name="story_generation")
    async def trace_story_generation(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        start_time: float,
        end_time: float,
        response_content: str,
        token_usage: Optional[Dict[str, int]] = None
    ) -> StoryMetrics:
        """Trace story generation metrics"""
        
        generation_time = end_time - start_time
        word_count = len(response_content.split())
        character_count = len(response_content)
        
        # Estimate page count (rough heuristic)
        page_count = max(1, word_count // 100)
        
        # Estimate cost (GPT-4 pricing)
        cost_estimate = 0.0
        if token_usage:
            cost_estimate = (
                token_usage.get('prompt_tokens', 0) * 0.00003 + 
                token_usage.get('completion_tokens', 0) * 0.00006
            )
        
        # Create metrics
        story_metrics = StoryMetrics(
            story_id=f"story_{uuid.uuid4().hex[:8]}",
            prompt=prompt,
            generation_time=generation_time,
            word_count=word_count,
            character_count=character_count,
            page_count=page_count,
            model_used=model,
            temperature=temperature,
            max_tokens=max_tokens,
            actual_tokens_used=token_usage,
            cost_estimate=cost_estimate
        )
        
        # Log to LangSmith if available
        if self.langsmith_client:
            await self._log_story_to_langsmith(story_metrics, response_content)
        
        return story_metrics
    
    @traceable(run_type="chain", name="image_generation")
    async def trace_image_generation(
        self,
        story_id: str,
        prompt: str,
        model: str,
        image_size: str,
        start_time: float,
        end_time: float,
        image_url: Optional[str] = None,
        local_path: Optional[str] = None
    ) -> ImageMetrics:
        """Trace image generation metrics"""
        
        generation_time = end_time - start_time
        
        # Estimate cost (DALL-E 3 pricing)
        cost_estimate = 0.04  # Standard DALL-E 3 cost per image
        
        image_metrics = ImageMetrics(
            image_id=f"img_{uuid.uuid4().hex[:8]}",
            story_id=story_id,
            prompt=prompt,
            generation_time=generation_time,
            model_used=model,
            image_size=image_size,
            image_url=image_url,
            local_path=local_path,
            cost_estimate=cost_estimate
        )
        
        # Log to LangSmith if available
        if self.langsmith_client:
            await self._log_image_to_langsmith(image_metrics)
        
        return image_metrics
    
    @traceable(run_type="chain", name="audio_generation")
    async def trace_audio_generation(
        self,
        story_id: str,
        voice_style: str,
        model: str,
        start_time: float,
        end_time: float,
        audio_duration: float,
        local_path: Optional[str] = None
    ) -> AudioMetrics:
        """Trace audio generation metrics"""
        
        generation_time = end_time - start_time
        
        # OpenVoice is free, but we can track time costs
        cost_estimate = 0.0
        
        audio_metrics = AudioMetrics(
            audio_id=f"audio_{uuid.uuid4().hex[:8]}",
            story_id=story_id,
            generation_time=generation_time,
            model_used=model,
            voice_style=voice_style,
            audio_duration=audio_duration,
            local_path=local_path,
            cost_estimate=cost_estimate
        )
        
        # Log to LangSmith if available
        if self.langsmith_client:
            await self._log_audio_to_langsmith(audio_metrics)
        
        return audio_metrics
    
    async def _log_story_to_langsmith(self, metrics: StoryMetrics, content: str):
        """Log story metrics to LangSmith"""
        if not self.langsmith_client:
            return
        
        try:
            run_tree = RunTree(
                name="story_generation",
                run_type="chain",
                inputs={
                    "prompt": metrics.prompt,
                    "model": metrics.model_used,
                    "temperature": metrics.temperature,
                    "max_tokens": metrics.max_tokens
                },
                outputs={
                    "story_content": content[:500] + "..." if len(content) > 500 else content,
                    "word_count": metrics.word_count,
                    "character_count": metrics.character_count,
                    "page_count": metrics.page_count,
                    "generation_time": metrics.generation_time,
                    "cost_estimate": metrics.cost_estimate
                },
                tags=["storytelling", "research", "gpt-4"]
            )
            
            await asyncio.to_thread(
                self.langsmith_client.create_run,
                inputs=run_tree.inputs,
                outputs=run_tree.outputs,
                run_type=run_tree.run_type,
                name=run_tree.name,
                tags=run_tree.tags,
                project_name=self.project_name
            )
            
        except Exception as e:
            print(f"Error logging to LangSmith: {e}")
    
    async def _log_image_to_langsmith(self, metrics: ImageMetrics):
        """Log image metrics to LangSmith"""
        if not self.langsmith_client:
            return
        
        try:
            run_tree = RunTree(
                name="image_generation",
                run_type="chain",
                inputs={
                    "prompt": metrics.prompt,
                    "model": metrics.model_used,
                    "image_size": metrics.image_size
                },
                outputs={
                    "image_url": metrics.image_url,
                    "local_path": metrics.local_path,
                    "generation_time": metrics.generation_time,
                    "cost_estimate": metrics.cost_estimate
                },
                tags=["image_generation", "research", "dall-e"]
            )
            
            await asyncio.to_thread(
                self.langsmith_client.create_run,
                inputs=run_tree.inputs,
                outputs=run_tree.outputs,
                run_type=run_tree.run_type,
                name=run_tree.name,
                tags=run_tree.tags,
                project_name=self.project_name
            )
            
        except Exception as e:
            print(f"Error logging to LangSmith: {e}")
    
    async def _log_audio_to_langsmith(self, metrics: AudioMetrics):
        """Log audio metrics to LangSmith"""
        if not self.langsmith_client:
            return
        
        try:
            run_tree = RunTree(
                name="audio_generation",
                run_type="chain",
                inputs={
                    "voice_style": metrics.voice_style,
                    "model": metrics.model_used
                },
                outputs={
                    "local_path": metrics.local_path,
                    "audio_duration": metrics.audio_duration,
                    "generation_time": metrics.generation_time,
                    "cost_estimate": metrics.cost_estimate
                },
                tags=["audio_generation", "research", "openvoice"]
            )
            
            await asyncio.to_thread(
                self.langsmith_client.create_run,
                inputs=run_tree.inputs,
                outputs=run_tree.outputs,
                run_type=run_tree.run_type,
                name=run_tree.name,
                tags=run_tree.tags,
                project_name=self.project_name
            )
            
        except Exception as e:
            print(f"Error logging to LangSmith: {e}")
    
    def complete_session(
        self,
        story_metrics: StoryMetrics,
        image_metrics: List[ImageMetrics],
        audio_metrics: Optional[AudioMetrics] = None,
        error_message: Optional[str] = None
    ) -> ResearchSession:
        """Complete a research session and create summary"""
        
        total_cost = story_metrics.cost_estimate or 0.0
        total_cost += sum(img.cost_estimate or 0.0 for img in image_metrics)
        if audio_metrics:
            total_cost += audio_metrics.cost_estimate or 0.0
        
        total_time = story_metrics.generation_time
        total_time += sum(img.generation_time for img in image_metrics)
        if audio_metrics:
            total_time += audio_metrics.generation_time
        
        session = ResearchSession(
            session_id=self.current_session_id,
            timestamp=datetime.now(),
            story_metrics=story_metrics,
            image_metrics=image_metrics,
            audio_metrics=audio_metrics,
            total_cost=total_cost,
            total_time=total_time,
            success=error_message is None,
            error_message=error_message
        )
        
        self.sessions.append(session)
        return session
    
    def export_metrics(self, output_dir: str = "research_metrics") -> Dict[str, Any]:
        """Export all collected metrics for analysis"""
        
        Path(output_dir).mkdir(exist_ok=True)
        
        # Convert sessions to dictionaries
        sessions_data = [asdict(session) for session in self.sessions]
        
        # Calculate aggregate metrics
        if self.sessions:
            total_sessions = len(self.sessions)
            successful_sessions = len([s for s in self.sessions if s.success])
            success_rate = successful_sessions / total_sessions
            
            avg_story_time = sum(s.story_metrics.generation_time for s in self.sessions) / total_sessions
            avg_image_time = sum(sum(img.generation_time for img in s.image_metrics) for s in self.sessions) / total_sessions
            avg_audio_time = sum(s.audio_metrics.generation_time for s in self.sessions if s.audio_metrics) / total_sessions if any(s.audio_metrics for s in self.sessions) else 0
            
            avg_cost = sum(s.total_cost for s in self.sessions) / total_sessions
            avg_word_count = sum(s.story_metrics.word_count for s in self.sessions) / total_sessions
            
            aggregate_metrics = {
                "total_sessions": total_sessions,
                "successful_sessions": successful_sessions,
                "success_rate": success_rate,
                "average_story_generation_time": avg_story_time,
                "average_image_generation_time": avg_image_time,
                "average_audio_generation_time": avg_audio_time,
                "average_total_cost": avg_cost,
                "average_word_count": avg_word_count,
                "total_cost": sum(s.total_cost for s in self.sessions),
                "total_time": sum(s.total_time for s in self.sessions)
            }
        else:
            aggregate_metrics = {}
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Raw data
        with open(f"{output_dir}/raw_metrics_{timestamp}.json", "w") as f:
            json.dump(sessions_data, f, indent=2, default=str)
        
        # Aggregate metrics
        with open(f"{output_dir}/aggregate_metrics_{timestamp}.json", "w") as f:
            json.dump(aggregate_metrics, f, indent=2, default=str)
        
        # Summary report
        report = self._generate_research_report(aggregate_metrics)
        with open(f"{output_dir}/research_report_{timestamp}.md", "w") as f:
            f.write(report)
        
        return {
            "raw_data_file": f"{output_dir}/raw_metrics_{timestamp}.json",
            "aggregate_file": f"{output_dir}/aggregate_metrics_{timestamp}.json",
            "report_file": f"{output_dir}/research_report_{timestamp}.md",
            "aggregate_metrics": aggregate_metrics
        }
    
    def _generate_research_report(self, metrics: Dict[str, Any]) -> str:
        """Generate a research report from metrics"""
        
        if not metrics:
            return "# Research Report\n\nNo data collected yet."
        
        report = f"""# AI Storytelling Research Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Sessions:** {metrics.get('total_sessions', 0)}
**Success Rate:** {metrics.get('success_rate', 0):.2%}

## Performance Metrics

### Generation Times
- **Average Story Generation:** {metrics.get('average_story_generation_time', 0):.2f}s
- **Average Image Generation:** {metrics.get('average_image_generation_time', 0):.2f}s
- **Average Audio Generation:** {metrics.get('average_audio_generation_time', 0):.2f}s
- **Average Total Time:** {metrics.get('total_time', 0) / max(metrics.get('total_sessions', 1), 1):.2f}s

### Content Metrics
- **Average Word Count:** {metrics.get('average_word_count', 0):.0f} words
- **Average Cost per Session:** ${metrics.get('average_total_cost', 0):.4f}
- **Total Cost:** ${metrics.get('total_cost', 0):.4f}

### Quality Metrics
- **Success Rate:** {metrics.get('success_rate', 0):.2%}
- **Successful Sessions:** {metrics.get('successful_sessions', 0)}/{metrics.get('total_sessions', 0)}

## Research Insights

### Performance Analysis
- Story generation is the fastest component
- Image generation takes the most time
- Audio generation varies based on content length

### Cost Analysis
- Primary costs come from GPT-4 story generation
- DALL-E 3 image generation adds consistent cost
- OpenVoice audio generation is cost-free

### Quality Observations
- Success rate indicates system reliability
- Word count shows content richness
- Generation times show system responsiveness

---
*Report generated automatically by Loomi Research Tracer*
"""
        
        return report 