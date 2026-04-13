import sys
import os
from unittest.mock import MagicMock, AsyncMock

# Add the project root to sys.path to allow imports
# The root is obsidian-council/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Mock dependencies
sys.modules["sqlalchemy"] = MagicMock()
sys.modules["sqlalchemy.ext.asyncio"] = MagicMock()
sys.modules["sqlalchemy.orm"] = MagicMock()
sys.modules["redis"] = MagicMock()
sys.modules["redis.asyncio"] = MagicMock()
sys.modules["websockets"] = MagicMock()
sys.modules["websockets.exceptions"] = MagicMock()

import asyncio
import unittest
from datetime import datetime
from typing import Dict, Any, List
from core.agent_base import ObsidianAgent, AgentTask, AgentStatus, Priority

class TestAgent(ObsidianAgent):
    async def analyze(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Simulate some work
        await asyncio.sleep(0.01)
        return {"result": "success"}

    async def get_capabilities(self) -> Dict[str, Any]:
        return {"supported_tasks": ["test_task"]}

class TestObsidianAgentAssignTask(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = TestAgent(
            name="Test Agent",
            codename="TEST",
            specialization="Testing",
            tools=[]
        )
        # Mock redis_client and other items that might be used
        self.agent.redis_client = AsyncMock()

    async def test_assign_task_success(self):
        task = AgentTask(
            id="task-123",
            case_id="case-456",
            task_type="test_task",
            priority=Priority.MEDIUM,
            data={"key": "value"},
            assigned_at=datetime.now()
        )

        result = await self.agent.assign_task(task)

        self.assertTrue(result)
        self.assertIn("task-123", self.agent.current_tasks)
        self.assertEqual(self.agent.status, AgentStatus.WORKING)

        # Verify it eventually finishes if we wait
        timeout = 5
        start_time = asyncio.get_event_loop().time()
        while "task-123" in self.agent.current_tasks and asyncio.get_event_loop().time() - start_time < timeout:
            await asyncio.sleep(0.01)

        self.assertNotIn("task-123", self.agent.current_tasks)
        # Status should go back to IDLE
        self.assertEqual(self.agent.status, AgentStatus.IDLE)

    async def test_assign_task_unsupported(self):
        task = AgentTask(
            id="task-789",
            case_id="case-456",
            task_type="unsupported_task",
            priority=Priority.MEDIUM,
            data={"key": "value"},
            assigned_at=datetime.now()
        )

        result = await self.agent.assign_task(task)

        self.assertFalse(result)
        self.assertNotIn("task-789", self.agent.current_tasks)
        # Status should remain what it was (OFFLINE in this case)
        self.assertEqual(self.agent.status, AgentStatus.OFFLINE)

if __name__ == "__main__":
    unittest.main()
