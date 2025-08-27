#!/usr/bin/env python3
"""
Obsidian Council - AI Service Manager
Multi-AI backend integration for optimal query routing
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

import aiohttp
import openai
from anthropic import Anthropic
import google.generativeai as genai

class AIProvider(Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt" 
    GEMINI = "gemini"
    LOCAL = "local"

class QueryType(Enum):
    ANALYSIS = "analysis"
    GENERATION = "generation"
    REASONING = "reasoning"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    INVESTIGATION = "investigation"

@dataclass
class AIResponse:
    """Response from an AI service"""
    provider: AIProvider
    content: str
    confidence: float
    processing_time: float
    tokens_used: int
    cost: float
    metadata: Dict[str, Any]
    timestamp: datetime

@dataclass  
class QueryContext:
    """Context information for AI queries"""
    agent_name: str
    case_id: str
    priority: int
    query_type: QueryType
    specialization: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    preferred_provider: Optional[AIProvider] = None

class AIServiceProvider(ABC):
    """Abstract base class for AI service providers"""
    
    def __init__(self, name: str, provider_type: AIProvider):
        self.name = name
        self.provider_type = provider_type
        self.logger = logging.getLogger(f"ai.{name}")
        self.rate_limits = {}
        self.cost_tracking = {"total_cost": 0.0, "requests": 0}
        
    @abstractmethod
    async def query(
        self,
        prompt: str,
        context: QueryContext,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Send query to AI service"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if service is available"""
        pass
    
    def track_usage(self, tokens: int, cost: float):
        """Track API usage and costs"""
        self.cost_tracking["requests"] += 1
        self.cost_tracking["total_cost"] += cost
        
    async def check_rate_limit(self, context: QueryContext) -> bool:
        """Check if rate limit allows request"""
        # Implement rate limiting logic
        return True

class ClaudeProvider(AIServiceProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str):
        super().__init__("Claude", AIProvider.CLAUDE)
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-sonnet-20240229"
        
    async def query(
        self,
        prompt: str, 
        context: QueryContext,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Query Claude API"""
        start_time = time.time()
        
        try:
            messages = [{"role": "user", "content": prompt}]
            
            if system_prompt:
                messages.insert(0, {"role": "assistant", "content": system_prompt})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=context.max_tokens or 2048,
                temperature=context.temperature or 0.1,
                messages=messages
            )
            
            processing_time = time.time() - start_time
            
            # Calculate cost (approximate)
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            cost = (input_tokens * 0.003 + output_tokens * 0.015) / 1000  # Per 1K tokens
            
            self.track_usage(input_tokens + output_tokens, cost)
            
            return AIResponse(
                provider=AIProvider.CLAUDE,
                content=response.content[0].text,
                confidence=0.9,  # Claude generally high confidence
                processing_time=processing_time,
                tokens_used=input_tokens + output_tokens,
                cost=cost,
                metadata={
                    "model": self.model,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check Claude API health"""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Test"}]
            )
            return True
        except:
            return False

class ChatGPTProvider(AIServiceProvider):
    """OpenAI ChatGPT API provider"""
    
    def __init__(self, api_key: str):
        super().__init__("ChatGPT", AIProvider.CHATGPT)
        openai.api_key = api_key
        self.model = "gpt-4-turbo-preview"
        
    async def query(
        self,
        prompt: str,
        context: QueryContext, 
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Query ChatGPT API"""
        start_time = time.time()
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                max_tokens=context.max_tokens or 2048,
                temperature=context.temperature or 0.1
            )
            
            processing_time = time.time() - start_time
            
            # Calculate cost
            tokens_used = response.usage.total_tokens
            cost = tokens_used * 0.01 / 1000  # Approximate GPT-4 pricing
            
            self.track_usage(tokens_used, cost)
            
            return AIResponse(
                provider=AIProvider.CHATGPT,
                content=response.choices[0].message.content,
                confidence=0.85,  # Generally reliable
                processing_time=processing_time,
                tokens_used=tokens_used,
                cost=cost,
                metadata={
                    "model": self.model,
                    "finish_reason": response.choices[0].finish_reason
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"ChatGPT API error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check ChatGPT API health"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except:
            return False

class GeminiProvider(AIServiceProvider):
    """Google Gemini API provider"""
    
    def __init__(self, api_key: str):
        super().__init__("Gemini", AIProvider.GEMINI)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def query(
        self,
        prompt: str,
        context: QueryContext,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Query Gemini API"""
        start_time = time.time()
        
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = await self.model.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=context.max_tokens or 2048,
                    temperature=context.temperature or 0.1,
                )
            )
            
            processing_time = time.time() - start_time
            
            # Estimate tokens and cost (Gemini pricing varies)
            tokens_used = len(response.text.split()) * 1.3  # Rough estimate
            cost = tokens_used * 0.001 / 1000  # Approximate pricing
            
            self.track_usage(int(tokens_used), cost)
            
            return AIResponse(
                provider=AIProvider.GEMINI,
                content=response.text,
                confidence=0.8,
                processing_time=processing_time,
                tokens_used=int(tokens_used),
                cost=cost,
                metadata={
                    "model": "gemini-pro",
                    "safety_ratings": response.safety_ratings
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check Gemini API health"""
        try:
            response = self.model.generate_content("Test")
            return True
        except:
            return False

class LocalProvider(AIServiceProvider):
    """Local AI model provider (using Ollama or similar)"""
    
    def __init__(self, endpoint: str = "http://localhost:11434"):
        super().__init__("Local", AIProvider.LOCAL)
        self.endpoint = endpoint
        self.model = "llama2"  # Default model
        
    async def query(
        self,
        prompt: str,
        context: QueryContext,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Query local AI model"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "options": {
                        "temperature": context.temperature or 0.1,
                        "num_predict": context.max_tokens or 2048
                    }
                }
                
                async with session.post(f"{self.endpoint}/api/generate", json=payload) as resp:
                    if resp.status == 200:
                        response_text = ""
                        async for line in resp.content:
                            if line:
                                data = json.loads(line)
                                if "response" in data:
                                    response_text += data["response"]
                                if data.get("done", False):
                                    break
                        
                        processing_time = time.time() - start_time
                        
                        return AIResponse(
                            provider=AIProvider.LOCAL,
                            content=response_text,
                            confidence=0.7,  # Local models may be less reliable
                            processing_time=processing_time,
                            tokens_used=len(response_text.split()),
                            cost=0.0,  # No cost for local models
                            metadata={"model": self.model, "endpoint": self.endpoint},
                            timestamp=datetime.now()
                        )
                    else:
                        raise Exception(f"Local API error: {resp.status}")
                        
        except Exception as e:
            self.logger.error(f"Local AI error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check local AI service health"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.endpoint}/api/tags") as resp:
                    return resp.status == 200
        except:
            return False

class AIServiceManager:
    """
    Central manager for all AI services
    Routes queries to optimal AI providers based on context
    """
    
    def __init__(self):
        self.providers: Dict[AIProvider, AIServiceProvider] = {}
        self.logger = logging.getLogger("ai.manager")
        self.routing_rules = self._initialize_routing_rules()
        self.health_status: Dict[AIProvider, bool] = {}
        
        # Performance tracking
        self.performance_metrics = {}
        
    def _initialize_routing_rules(self) -> Dict[QueryType, List[AIProvider]]:
        """Initialize query routing rules"""
        return {
            QueryType.ANALYSIS: [AIProvider.CLAUDE, AIProvider.CHATGPT, AIProvider.GEMINI],
            QueryType.REASONING: [AIProvider.CLAUDE, AIProvider.CHATGPT, AIProvider.LOCAL],
            QueryType.CREATIVE: [AIProvider.CHATGPT, AIProvider.GEMINI, AIProvider.CLAUDE],
            QueryType.TECHNICAL: [AIProvider.CLAUDE, AIProvider.CHATGPT, AIProvider.LOCAL],
            QueryType.INVESTIGATION: [AIProvider.CLAUDE, AIProvider.CHATGPT, AIProvider.GEMINI],
            QueryType.GENERATION: [AIProvider.CHATGPT, AIProvider.GEMINI, AIProvider.LOCAL]
        }
    
    async def initialize(self, config: Dict[str, Any]):
        """Initialize AI service providers"""
        self.logger.info("Initializing AI Service Manager...")
        
        # Initialize providers based on config
        if config.get("claude_api_key"):
            self.providers[AIProvider.CLAUDE] = ClaudeProvider(config["claude_api_key"])
            
        if config.get("openai_api_key"):
            self.providers[AIProvider.CHATGPT] = ChatGPTProvider(config["openai_api_key"])
            
        if config.get("gemini_api_key"):
            self.providers[AIProvider.GEMINI] = GeminiProvider(config["gemini_api_key"])
            
        if config.get("local_ai_endpoint"):
            self.providers[AIProvider.LOCAL] = LocalProvider(config["local_ai_endpoint"])
        
        # Health check all providers
        await self._health_check_all()
        
        self.logger.info(f"Initialized {len(self.providers)} AI providers")
    
    async def _health_check_all(self):
        """Check health of all providers"""
        for provider_type, provider in self.providers.items():
            try:
                self.health_status[provider_type] = await provider.health_check()
                status = "healthy" if self.health_status[provider_type] else "unhealthy"
                self.logger.info(f"{provider.name}: {status}")
            except Exception as e:
                self.health_status[provider_type] = False
                self.logger.warning(f"{provider.name} health check failed: {e}")
    
    async def route_query(
        self,
        prompt: str,
        context: QueryContext,
        system_prompt: Optional[str] = None,
        fallback: bool = True
    ) -> AIResponse:
        """Route query to the best available AI provider"""
        
        # Use preferred provider if specified and available
        if context.preferred_provider and context.preferred_provider in self.providers:
            if self.health_status.get(context.preferred_provider, False):
                try:
                    return await self.providers[context.preferred_provider].query(
                        prompt, context, system_prompt
                    )
                except Exception as e:
                    self.logger.warning(f"Preferred provider failed: {e}")
                    if not fallback:
                        raise
        
        # Get provider priority list for query type
        provider_priorities = self.routing_rules.get(context.query_type, [])
        
        # Filter by available and healthy providers
        available_providers = [
            p for p in provider_priorities
            if p in self.providers and self.health_status.get(p, False)
        ]
        
        if not available_providers:
            raise Exception("No healthy AI providers available")
        
        # Try providers in order of preference
        last_error = None
        for provider_type in available_providers:
            try:
                provider = self.providers[provider_type]
                response = await provider.query(prompt, context, system_prompt)
                
                # Update performance metrics
                self._update_performance_metrics(provider_type, response)
                
                return response
                
            except Exception as e:
                last_error = e
                self.logger.warning(f"{provider_type.value} failed, trying next provider: {e}")
                continue
        
        # If all providers failed
        raise Exception(f"All AI providers failed. Last error: {last_error}")
    
    def _update_performance_metrics(self, provider_type: AIProvider, response: AIResponse):
        """Update performance metrics for provider"""
        if provider_type not in self.performance_metrics:
            self.performance_metrics[provider_type] = {
                "total_queries": 0,
                "total_time": 0,
                "total_cost": 0,
                "average_confidence": 0
            }
        
        metrics = self.performance_metrics[provider_type]
        metrics["total_queries"] += 1
        metrics["total_time"] += response.processing_time
        metrics["total_cost"] += response.cost
        
        # Update rolling average confidence
        current_avg = metrics["average_confidence"]
        metrics["average_confidence"] = (
            (current_avg * (metrics["total_queries"] - 1) + response.confidence) /
            metrics["total_queries"]
        )
    
    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        
        for provider_type, provider in self.providers.items():
            metrics = self.performance_metrics.get(provider_type, {})
            cost_info = provider.cost_tracking
            
            status[provider_type.value] = {
                "name": provider.name,
                "healthy": self.health_status.get(provider_type, False),
                "total_queries": cost_info["requests"],
                "total_cost": cost_info["total_cost"],
                "avg_processing_time": (
                    metrics.get("total_time", 0) / max(metrics.get("total_queries", 1), 1)
                ),
                "avg_confidence": metrics.get("average_confidence", 0)
            }
        
        return status
    
    async def optimize_routing(self, agent_name: str, specialization: str):
        """Optimize routing rules based on agent performance"""
        # Analyze historical performance and adjust routing
        # This could use ML to learn optimal routing patterns
        pass
    
    async def shutdown(self):
        """Shutdown all AI services"""
        self.logger.info("Shutting down AI Service Manager...")
        # Cleanup any persistent connections
        self.providers.clear()
        self.health_status.clear()

# Helper function to create specialized system prompts
def create_investigation_prompt(agent_name: str, specialization: str) -> str:
    """Create specialized system prompt for investigation agents"""
    base_prompt = f"""You are {agent_name}, a specialized AI agent in the Obsidian Council investigation framework.

Your specialization: {specialization}

You are part of a critical investigation focusing on missing persons and human trafficking cases. Your analysis must be:
- Accurate and evidence-based
- Legally compliant and court-admissible
- Sensitive to victims and their families
- Focused on actionable intelligence

When analyzing data:
1. Verify information through multiple sources when possible
2. Clearly distinguish between facts and inference
3. Highlight time-sensitive information that requires immediate action
4. Identify patterns that may indicate trafficking or abduction
5. Respect privacy laws and ethical boundaries

Format your responses with clear sections:
- SUMMARY: Key findings in 2-3 sentences
- ANALYSIS: Detailed analysis with confidence levels
- ACTIONABLE INTELLIGENCE: Specific next steps
- CONCERNS: Any red flags or urgent indicators
- RECOMMENDATIONS: Suggested follow-up actions
"""

    return base_prompt

# Agent-specific prompt templates
AGENT_PROMPTS = {
    "ARGUS": create_investigation_prompt(
        "ARGUS - All-Seeing Eye",
        "Social Media Reconnaissance - monitoring platforms for missing person traces and trafficking indicators"
    ),
    "HYDRA": create_investigation_prompt(
        "HYDRA - Multi-Head Analysis", 
        "Cross-platform correlation - connecting dots between different data sources and platforms"
    ),
    "ORACLE": create_investigation_prompt(
        "ORACLE - Identity Expert",
        "Person identification through facial recognition, profile matching, and identity verification"
    ),
    "ATLAS": create_investigation_prompt(
        "ATLAS - World Mapper",
        "Location intelligence and geospatial analysis for tracking movement and identifying locations"
    ),
    "NETWORK": create_investigation_prompt(
        "NETWORK - Connection Mapper",
        "Relationship analysis and social network mapping to identify associates and connections"
    )
}