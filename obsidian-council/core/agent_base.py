#!/usr/bin/env python3
"""
Obsidian Council - Base Agent Framework
Core infrastructure for AI-powered OSINT agents
"""

import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis
import websockets

# Agent Status Types
class AgentStatus(Enum):
    OFFLINE = "offline"
    IDLE = "idle"
    WORKING = "working"
    ERROR = "error"
    COLLABORATION = "collaboration"

# Task Priority Levels
class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

@dataclass
class AgentTask:
    """Represents a task assigned to an agent"""
    id: str
    case_id: str
    task_type: str
    priority: Priority
    data: Dict[str, Any]
    assigned_at: datetime
    deadline: Optional[datetime] = None
    progress: float = 0.0
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None

@dataclass
class AgentMessage:
    """Message for inter-agent communication"""
    id: str
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime
    priority: Priority = Priority.MEDIUM

class ObsidianAgent(ABC):
    """
    Base class for all Obsidian Council agents
    
    Each specialized agent inherits from this base class and implements
    their specific analysis capabilities while sharing common infrastructure.
    """
    
    def __init__(
        self,
        name: str,
        codename: str,
        specialization: str,
        tools: List[str],
        ai_backends: List[str] = None
    ):
        self.name = name
        self.codename = codename
        self.specialization = specialization
        self.tools = tools or []
        self.ai_backends = ai_backends or ["claude", "local"]
        
        # Agent state
        self.status = AgentStatus.OFFLINE
        self.current_tasks: Dict[str, AgentTask] = {}
        self.session_memory: Dict[str, Any] = {}
        self.case_assignments: List[str] = []
        
        # Communication
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.websocket_connections: List[websockets.WebSocketServerProtocol] = []
        
        # Database and cache
        self.db_engine = None
        self.redis_client = None
        self.session_maker = None
        
        # Logging
        self.logger = self._setup_logging()
        
        # Collaboration partners
        self.council_agents: Dict[str, 'ObsidianAgent'] = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup agent-specific logging"""
        logger = logging.getLogger(f"obsidian.{self.codename.lower()}")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'[{self.codename}] %(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    async def initialize(self, db_url: str, redis_url: str):
        """Initialize agent connections and services"""
        self.logger.info(f"Initializing {self.name}...")
        
        # Database connection
        self.db_engine = create_async_engine(db_url)
        self.session_maker = sessionmaker(
            self.db_engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # Redis connection
        self.redis_client = Redis.from_url(redis_url)
        
        # Set status to idle
        self.status = AgentStatus.IDLE
        
        # Start background tasks
        asyncio.create_task(self._message_processor())
        asyncio.create_task(self._health_monitor())
        
        self.logger.info(f"{self.name} initialized and ready")
    
    async def _message_processor(self):
        """Process incoming messages from other agents"""
        while True:
            try:
                message = await self.message_queue.get()
                await self._handle_message(message)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
            await asyncio.sleep(0.1)
    
    async def _health_monitor(self):
        """Monitor agent health and report status"""
        while True:
            try:
                # Update status in Redis
                await self.redis_client.hset(
                    f"agent:{self.codename.lower()}",
                    mapping={
                        "status": self.status.value,
                        "last_heartbeat": datetime.now().isoformat(),
                        "active_tasks": len(self.current_tasks),
                        "specialization": self.specialization
                    }
                )
            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")
            
            await asyncio.sleep(30)  # Heartbeat every 30 seconds
    
    async def _handle_message(self, message: AgentMessage):
        """Handle incoming messages from other agents"""
        self.logger.info(f"Received message from {message.sender}: {message.message_type}")
        
        if message.message_type == "collaboration_request":
            await self._handle_collaboration_request(message)
        elif message.message_type == "data_share":
            await self._handle_data_share(message)
        elif message.message_type == "task_delegation":
            await self._handle_task_delegation(message)
        else:
            await self.handle_custom_message(message)
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Core analysis method - each agent implements their specialized analysis
        
        Args:
            data: Input data for analysis
            context: Additional context information
            
        Returns:
            Analysis results dictionary
        """
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities and available operations"""
        pass
    
    async def handle_custom_message(self, message: AgentMessage):
        """Handle custom message types - override in subclasses"""
        self.logger.warning(f"Unhandled message type: {message.message_type}")
    
    async def assign_task(self, task: AgentTask) -> bool:
        """Assign a new task to this agent"""
        try:
            self.logger.info(f"Received task {task.id}: {task.task_type}")
            
            # Check if agent can handle this task type
            if not await self._can_handle_task(task):
                self.logger.warning(f"Cannot handle task type: {task.task_type}")
                return False
            
            # Add to current tasks
            self.current_tasks[task.id] = task
            self.status = AgentStatus.WORKING
            
            # Process task asynchronously
            asyncio.create_task(self._process_task(task))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error assigning task: {e}")
            return False
    
    async def _process_task(self, task: AgentTask):
        """Process an assigned task"""
        try:
            task.status = "in_progress"
            
            # Execute the analysis
            result = await self.analyze(task.data, {"case_id": task.case_id})
            
            # Update task with results
            task.result = result
            task.status = "completed"
            task.progress = 100.0
            
            self.logger.info(f"Task {task.id} completed successfully")
            
            # Notify completion
            await self._notify_task_completion(task)
            
        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            self.logger.error(f"Task {task.id} failed: {e}")
        
        finally:
            # Remove from current tasks
            if task.id in self.current_tasks:
                del self.current_tasks[task.id]
            
            # Update status
            if not self.current_tasks:
                self.status = AgentStatus.IDLE
    
    async def _can_handle_task(self, task: AgentTask) -> bool:
        """Check if agent can handle the given task type"""
        capabilities = await self.get_capabilities()
        supported_tasks = capabilities.get("supported_tasks", [])
        return task.task_type in supported_tasks
    
    async def _notify_task_completion(self, task: AgentTask):
        """Notify the system that a task has been completed"""
        notification = {
            "agent": self.codename,
            "task_id": task.id,
            "status": task.status,
            "result": task.result,
            "timestamp": datetime.now().isoformat()
        }
        
        # Publish to Redis
        await self.redis_client.publish(
            "task_completions",
            json.dumps(notification)
        )
        
        # Notify WebSocket clients
        await self._broadcast_to_websockets(notification)
    
    async def collaborate_with(self, agent_name: str, request: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate collaboration with another agent"""
        if agent_name not in self.council_agents:
            raise ValueError(f"Agent {agent_name} not available for collaboration")
        
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.codename,
            recipient=agent_name,
            message_type="collaboration_request",
            content=request,
            timestamp=datetime.now()
        )
        
        target_agent = self.council_agents[agent_name]
        await target_agent.message_queue.put(message)
        
        self.logger.info(f"Initiated collaboration with {agent_name}")
    
    async def _handle_collaboration_request(self, message: AgentMessage):
        """Handle collaboration request from another agent"""
        self.logger.info(f"Collaboration request from {message.sender}")
        
        # Set status to collaboration mode
        self.status = AgentStatus.COLLABORATION
        
        try:
            # Process the collaboration request
            result = await self.analyze(message.content, {"collaboration": True})
            
            # Send response back
            response = AgentMessage(
                id=str(uuid.uuid4()),
                sender=self.codename,
                recipient=message.sender,
                message_type="collaboration_response",
                content={"result": result},
                timestamp=datetime.now()
            )
            
            sender_agent = self.council_agents.get(message.sender)
            if sender_agent:
                await sender_agent.message_queue.put(response)
                
        except Exception as e:
            self.logger.error(f"Collaboration error: {e}")
        
        finally:
            if not self.current_tasks:
                self.status = AgentStatus.IDLE
    
    async def _handle_data_share(self, message: AgentMessage):
        """Handle data sharing from another agent"""
        self.logger.info(f"Received shared data from {message.sender}")
        
        # Store shared data in session memory
        key = f"shared_data_{message.sender}_{message.id}"
        self.session_memory[key] = {
            "data": message.content,
            "timestamp": message.timestamp,
            "sender": message.sender
        }
    
    async def _handle_task_delegation(self, message: AgentMessage):
        """Handle task delegation from another agent"""
        self.logger.info(f"Received delegated task from {message.sender}")
        
        # Create task from message
        task = AgentTask(
            id=str(uuid.uuid4()),
            case_id=message.content.get("case_id", "unknown"),
            task_type=message.content.get("task_type"),
            priority=Priority(message.content.get("priority", 2)),
            data=message.content.get("data", {}),
            assigned_at=datetime.now()
        )
        
        await self.assign_task(task)
    
    async def register_with_council(self, council_agents: Dict[str, 'ObsidianAgent']):
        """Register this agent with the Obsidian Council"""
        self.council_agents = council_agents
        self.logger.info(f"Registered with council - {len(council_agents)} agents available")
    
    async def add_websocket_client(self, websocket: websockets.WebSocketServerProtocol):
        """Add a WebSocket client for real-time updates"""
        self.websocket_connections.append(websocket)
        self.logger.info("WebSocket client connected")
    
    async def remove_websocket_client(self, websocket: websockets.WebSocketServerProtocol):
        """Remove a WebSocket client"""
        if websocket in self.websocket_connections:
            self.websocket_connections.remove(websocket)
            self.logger.info("WebSocket client disconnected")
    
    async def _broadcast_to_websockets(self, message: Dict[str, Any]):
        """Broadcast message to all connected WebSocket clients"""
        if self.websocket_connections:
            message_json = json.dumps(message)
            disconnected = []
            
            for ws in self.websocket_connections:
                try:
                    await ws.send(message_json)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(ws)
            
            # Remove disconnected clients
            for ws in disconnected:
                await self.remove_websocket_client(ws)
    
    async def save_session(self, session_id: str):
        """Save current session state"""
        session_data = {
            "agent": self.codename,
            "memory": self.session_memory,
            "tasks": {k: asdict(v) for k, v in self.current_tasks.items()},
            "status": self.status.value,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.redis_client.hset(
            f"session:{session_id}",
            f"agent:{self.codename.lower()}",
            json.dumps(session_data)
        )
    
    async def load_session(self, session_id: str):
        """Load previous session state"""
        session_data = await self.redis_client.hget(
            f"session:{session_id}",
            f"agent:{self.codename.lower()}"
        )
        
        if session_data:
            data = json.loads(session_data)
            self.session_memory = data.get("memory", {})
            # Note: Don't restore tasks as they may be stale
            self.logger.info(f"Session {session_id} loaded")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "codename": self.codename,
            "specialization": self.specialization,
            "status": self.status.value,
            "active_tasks": len(self.current_tasks),
            "tools": self.tools,
            "ai_backends": self.ai_backends,
            "capabilities": await self.get_capabilities()
        }
    
    async def shutdown(self):
        """Gracefully shutdown the agent"""
        self.logger.info(f"Shutting down {self.name}...")
        
        self.status = AgentStatus.OFFLINE
        
        # Close database connections
        if self.db_engine:
            await self.db_engine.dispose()
        
        # Close Redis connection
        if self.redis_client:
            await self.redis_client.close()
        
        # Close WebSocket connections
        for ws in self.websocket_connections:
            await ws.close()
        
        self.logger.info(f"{self.name} shutdown complete")

# Utility functions for agent management
async def create_agent_task(
    case_id: str,
    task_type: str,
    data: Dict[str, Any],
    priority: Priority = Priority.MEDIUM,
    deadline: Optional[datetime] = None
) -> AgentTask:
    """Create a new agent task"""
    return AgentTask(
        id=str(uuid.uuid4()),
        case_id=case_id,
        task_type=task_type,
        priority=priority,
        data=data,
        assigned_at=datetime.now(),
        deadline=deadline
    )

def serialize_agent_message(message: AgentMessage) -> str:
    """Serialize agent message for transmission"""
    return json.dumps({
        "id": message.id,
        "sender": message.sender,
        "recipient": message.recipient,
        "message_type": message.message_type,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "priority": message.priority.value
    })

def deserialize_agent_message(data: str) -> AgentMessage:
    """Deserialize agent message from transmission"""
    obj = json.loads(data)
    return AgentMessage(
        id=obj["id"],
        sender=obj["sender"],
        recipient=obj["recipient"],
        message_type=obj["message_type"],
        content=obj["content"],
        timestamp=datetime.fromisoformat(obj["timestamp"]),
        priority=Priority(obj["priority"])
    )