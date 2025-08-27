#!/usr/bin/env python3
"""
Obsidian Council - Agent Registry
Central registry and factory for all specialized agents
"""

from typing import Dict, Type, List
from ..core.agent_base import ObsidianAgent

# Import all agent classes
from .social_media.argus import ARGUSAgent
from .identity.oracle import ORACLEAgent
from .geolocation.atlas import ATLASAgent

# Additional agent imports (stub implementations for remaining agents)
class HYDRAAgent(ObsidianAgent):
    """HYDRA - Multi-Head Analysis Agent (Cross-Platform Correlation)"""
    def __init__(self):
        super().__init__(
            name="HYDRA - Multi-Head Analysis",
            codename="HYDRA",
            specialization="Cross-Platform Correlation",
            tools=["maltego", "gephi", "spiderfoot", "correlation-engine"],
            ai_backends=["claude", "chatgpt", "gemini"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["cross_platform_correlation", "data_fusion", "pattern_matching"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Cross-platform correlation analysis", "confidence": 0.8}

class KRONOSAgent(ObsidianAgent):
    """KRONOS - Timeline Master Agent (Temporal Analysis)"""
    def __init__(self):
        super().__init__(
            name="KRONOS - Timeline Master",
            codename="KRONOS", 
            specialization="Temporal Analysis",
            tools=["timeline-analysis", "temporal-correlation", "event-reconstruction"],
            ai_backends=["claude", "chatgpt"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["timeline_reconstruction", "temporal_analysis", "event_correlation"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Temporal pattern analysis", "confidence": 0.85}

class CERBERUSAgent(ObsidianAgent):
    """CERBERUS - Guardian Analyst Agent (Digital Evidence Analysis)"""
    def __init__(self):
        super().__init__(
            name="CERBERUS - Guardian Analyst",
            codename="CERBERUS",
            specialization="Digital Evidence Analysis", 
            tools=["autopsy", "volatility", "binwalk", "exiftool"],
            ai_backends=["claude", "local"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["evidence_analysis", "file_forensics", "metadata_extraction"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Digital evidence analysis", "confidence": 0.9}

class PHOENIXAgent(ObsidianAgent):
    """PHOENIX - Data Recovery Agent"""
    def __init__(self):
        super().__init__(
            name="PHOENIX - Data Recovery",
            codename="PHOENIX",
            specialization="Deleted Data Recovery",
            tools=["photorec", "testdisk", "scalpel", "foremost"],
            ai_backends=["claude", "local"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["data_recovery", "file_carving", "deleted_file_analysis"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Data recovery analysis", "confidence": 0.75}

class SENTINELAgent(ObsidianAgent):
    """SENTINEL - Area Monitor Agent"""
    def __init__(self):
        super().__init__(
            name="SENTINEL - Area Monitor", 
            codename="SENTINEL",
            specialization="Surveillance Analysis",
            tools=["opencv", "facial-detection", "movement-tracking", "cctv-analysis"],
            ai_backends=["claude", "local"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["surveillance_analysis", "area_monitoring", "movement_detection"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Surveillance area analysis", "confidence": 0.8}

class SPHINXAgent(ObsidianAgent):
    """SPHINX - Riddle Solver Agent"""
    def __init__(self):
        super().__init__(
            name="SPHINX - Riddle Solver",
            codename="SPHINX",
            specialization="Anonymous Identity Resolution",
            tools=["username-analysis", "writing-style-analysis", "behavioral-profiling"],
            ai_backends=["claude", "chatgpt", "gemini"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["anonymous_analysis", "identity_resolution", "behavioral_profiling"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Anonymous identity analysis", "confidence": 0.7}

class NETWORKAgent(ObsidianAgent):
    """NETWORK - Connection Mapper Agent"""
    def __init__(self):
        super().__init__(
            name="NETWORK - Connection Mapper",
            codename="NETWORK", 
            specialization="Relationship Analysis",
            tools=["maltego", "gephi", "networkx", "social-network-analysis"],
            ai_backends=["claude", "chatgpt"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["relationship_mapping", "network_analysis", "connection_discovery"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Network relationship analysis", "confidence": 0.85}

class GRAPHAgent(ObsidianAgent):
    """GRAPH - Visual Analyst Agent"""
    def __init__(self):
        super().__init__(
            name="GRAPH - Visual Analyst",
            codename="GRAPH",
            specialization="Network Visualization", 
            tools=["d3js", "cytoscape", "plotly", "matplotlib"],
            ai_backends=["claude", "local"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["data_visualization", "network_graphs", "pattern_visualization"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Visual pattern analysis", "confidence": 0.8}

class MOTORAgent(ObsidianAgent):
    """MOTOR - Vehicle Expert Agent"""
    def __init__(self):
        super().__init__(
            name="MOTOR - Vehicle Expert",
            codename="MOTOR",
            specialization="Vehicle Intelligence",
            tools=["license-plate-recognition", "vin-decoder", "vehicle-database"],
            ai_backends=["claude", "chatgpt"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["vehicle_analysis", "license_plate_lookup", "vehicle_identification"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Vehicle intelligence analysis", "confidence": 0.8}

class TRACEAgent(ObsidianAgent):
    """TRACE - Movement Tracker Agent"""
    def __init__(self):
        super().__init__(
            name="TRACE - Movement Tracker", 
            codename="TRACE",
            specialization="Vehicle Tracking",
            tools=["gps-analysis", "traffic-cam-integration", "route-optimization"],
            ai_backends=["claude", "local"]
        )
    
    async def get_capabilities(self):
        return {"supported_tasks": ["movement_tracking", "route_analysis", "location_prediction"]}
    
    async def analyze(self, data, context=None):
        return {"analysis": "Vehicle movement analysis", "confidence": 0.75}

# Agent Registry
AGENT_REGISTRY: Dict[str, Type[ObsidianAgent]] = {
    # Social Media Intelligence Division
    "ARGUS": ARGUSAgent,
    "HYDRA": HYDRAAgent, 
    "KRONOS": KRONOSAgent,
    
    # Digital Forensics Division
    "CERBERUS": CERBERUSAgent,
    "PHOENIX": PHOENIXAgent,
    
    # Geolocation Intelligence Division
    "ATLAS": ATLASAgent,
    "SENTINEL": SENTINELAgent,
    
    # Identity Resolution Division
    "ORACLE": ORACLEAgent,
    "SPHINX": SPHINXAgent,
    
    # Link Analysis Division
    "NETWORK": NETWORKAgent,
    "GRAPH": GRAPHAgent,
    
    # Vehicle Analysis Division
    "MOTOR": MOTORAgent,
    "TRACE": TRACEAgent
}

AGENT_DIVISIONS = {
    "Social Media Intelligence": ["ARGUS", "HYDRA", "KRONOS"],
    "Digital Forensics": ["CERBERUS", "PHOENIX"],
    "Geolocation Intelligence": ["ATLAS", "SENTINEL"], 
    "Identity Resolution": ["ORACLE", "SPHINX"],
    "Link Analysis": ["NETWORK", "GRAPH"],
    "Vehicle Analysis": ["MOTOR", "TRACE"]
}

def create_agent(codename: str) -> ObsidianAgent:
    """Create an agent instance by codename"""
    if codename not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent codename: {codename}")
    
    agent_class = AGENT_REGISTRY[codename]
    return agent_class()

def get_all_agent_codenames() -> List[str]:
    """Get list of all available agent codenames"""
    return list(AGENT_REGISTRY.keys())

def get_agents_by_division(division: str) -> List[str]:
    """Get agent codenames for a specific division"""
    return AGENT_DIVISIONS.get(division, [])

def get_agent_info() -> Dict[str, Dict[str, str]]:
    """Get information about all agents"""
    info = {}
    
    for codename, agent_class in AGENT_REGISTRY.items():
        # Create temporary instance to get info
        temp_agent = agent_class()
        info[codename] = {
            "name": temp_agent.name,
            "specialization": temp_agent.specialization,
            "tools": temp_agent.tools,
            "ai_backends": temp_agent.ai_backends
        }
    
    return info

def get_division_info() -> Dict[str, List[Dict[str, str]]]:
    """Get organized information by division"""
    division_info = {}
    
    for division, agents in AGENT_DIVISIONS.items():
        division_info[division] = []
        
        for codename in agents:
            agent_class = AGENT_REGISTRY[codename]
            temp_agent = agent_class()
            
            division_info[division].append({
                "codename": codename,
                "name": temp_agent.name,
                "specialization": temp_agent.specialization
            })
    
    return division_info