"""
Claude-Flow Integration for KI-Projektmanagement-System
Provides multi-agent orchestration, swarm intelligence, and ReasoningBank memory
Based on: https://github.com/ruvnet/claude-flow
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ClaudeFlowIntegration:
    """
    Integration with Claude-Flow agent orchestration platform

    Features:
    - Multi-agent swarm coordination (84.8% SWE-Bench solve rate)
    - ReasoningBank persistent memory with semantic search
    - 100 MCP tools for automation
    - 64 specialized agents
    - 32.3% token reduction, 2.8-4.4x speed improvement
    """

    def __init__(self, swarm_dir: str = ".swarm"):
        self.swarm_dir = Path(swarm_dir)
        self.swarm_dir.mkdir(exist_ok=True)
        self.memory_db = self.swarm_dir / "memory.db"
        self._initialized = False

    async def initialize(self) -> bool:
        """Initialize Claude-Flow system"""
        try:
            # First check if node/npm is available
            node_check = subprocess.run(
                ["node", "--version"], capture_output=True, text=True, timeout=5
            )

            if node_check.returncode != 0:
                logger.warning("⚠️ Node.js not found - Claude-Flow requires Node.js")
                logger.info("💡 Install from: https://nodejs.org/")
                return False

            # Check if npx is available
            npx_check = subprocess.run(
                ["npx", "--version"], capture_output=True, text=True, timeout=5
            )

            if npx_check.returncode != 0:
                logger.warning("⚠️ npx not found - comes with npm (Node Package Manager)")
                return False

            # Check if claude-flow is available via npx
            result = subprocess.run(
                ["npx", "claude-flow@alpha", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                self._initialized = True
                logger.info("✅ Claude-Flow initialized successfully")
                logger.info(f"   Node: {node_check.stdout.strip()}")
                logger.info(f"   npx: {npx_check.stdout.strip()}")
                return True
            else:
                logger.warning("⚠️ Claude-Flow not available via npx")
                logger.info("💡 Run: npm install -g claude-flow@alpha")
                return False

        except FileNotFoundError as e:
            logger.error(f"❌ Command not found: {e}")
            logger.info("💡 Install Node.js from: https://nodejs.org/")
            return False
        except Exception as e:
            logger.error(f"❌ Error initializing Claude-Flow: {e}")
            return False

    async def init_swarm(self, topology: str = "mesh", max_agents: int = 5) -> Dict[str, Any]:
        """
        Initialize a swarm with specified topology

        Args:
            topology: mesh, hierarchical, or star
            max_agents: Maximum number of agents

        Returns:
            Swarm initialization result
        """
        try:
            cmd = [
                "npx",
                "claude-flow@alpha",
                "swarm",
                "init",
                "--topology",
                topology,
                "--max-agents",
                str(max_agents),
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=30
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
            }

        except Exception as e:
            logger.error(f"❌ Error initializing swarm: {e}")
            return {"success": False, "error": str(e)}

    async def execute_task(
        self, task: str, use_claude: bool = True, agents: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute a task using Claude-Flow swarm

        Args:
            task: Task description
            use_claude: Use Claude AI for execution
            agents: Specific agents to use (optional)

        Returns:
            Task execution result
        """
        try:
            cmd = ["npx", "claude-flow@alpha", "swarm", task]

            if use_claude:
                cmd.append("--claude")

            if agents:
                cmd.extend(["--agents", ",".join(agents)])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.swarm_dir),
                timeout=300,  # 5 minutes for complex tasks
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "task": task,
            }

        except subprocess.TimeoutExpired:
            logger.error(f"⏱️ Task timeout: {task}")
            return {"success": False, "error": "Task timeout"}
        except Exception as e:
            logger.error(f"❌ Error executing task: {e}")
            return {"success": False, "error": str(e)}

    async def spawn_agent(self, agent_type: str, task: str) -> Dict[str, Any]:
        """
        Spawn a specialized agent for a specific task

        Available agents: researcher, coder, tester, reviewer, architect, etc.

        Args:
            agent_type: Type of agent to spawn
            task: Task for the agent

        Returns:
            Agent spawn result
        """
        try:
            cmd = ["npx", "claude-flow@alpha", "swarm", "spawn", agent_type, task]

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=60
            )

            return {
                "success": result.returncode == 0,
                "agent_type": agent_type,
                "task": task,
                "output": result.stdout,
            }

        except Exception as e:
            logger.error(f"❌ Error spawning agent: {e}")
            return {"success": False, "error": str(e)}

    async def memory_store(
        self, key: str, value: str, namespace: str = "default", use_reasoningbank: bool = True
    ) -> Dict[str, Any]:
        """
        Store information in ReasoningBank persistent memory

        Features:
        - SQLite-based persistent storage
        - Semantic search with MMR ranking
        - 2-3ms query latency
        - Namespace isolation

        Args:
            key: Memory key
            value: Memory value
            namespace: Namespace for organization
            use_reasoningbank: Use ReasoningBank (persistent)

        Returns:
            Storage result
        """
        try:
            cmd = [
                "npx",
                "claude-flow@alpha",
                "memory",
                "store",
                key,
                value,
                "--namespace",
                namespace,
            ]

            if use_reasoningbank:
                cmd.append("--reasoningbank")

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=10
            )

            return {
                "success": result.returncode == 0,
                "key": key,
                "namespace": namespace,
                "reasoningbank": use_reasoningbank,
            }

        except Exception as e:
            logger.error(f"❌ Error storing memory: {e}")
            return {"success": False, "error": str(e)}

    async def memory_query(
        self, query: str, namespace: str = "default", use_reasoningbank: bool = True
    ) -> Dict[str, Any]:
        """
        Query ReasoningBank memory with semantic search

        Args:
            query: Search query
            namespace: Namespace to search
            use_reasoningbank: Use ReasoningBank

        Returns:
            Query results with semantic ranking
        """
        try:
            cmd = ["npx", "claude-flow@alpha", "memory", "query", query, "--namespace", namespace]

            if use_reasoningbank:
                cmd.append("--reasoningbank")

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=10
            )

            return {
                "success": result.returncode == 0,
                "query": query,
                "results": result.stdout,
                "namespace": namespace,
            }

        except Exception as e:
            logger.error(f"❌ Error querying memory: {e}")
            return {"success": False, "error": str(e)}

    async def memory_status(self) -> Dict[str, Any]:
        """Get ReasoningBank memory status and statistics"""
        try:
            cmd = ["npx", "claude-flow@alpha", "memory", "status", "--reasoningbank"]

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=10
            )

            return {
                "success": result.returncode == 0,
                "status": result.stdout,
                "memory_db": str(self.memory_db),
                "db_exists": self.memory_db.exists(),
            }

        except Exception as e:
            logger.error(f"❌ Error getting memory status: {e}")
            return {"success": False, "error": str(e)}

    async def init_hive_mind(self, project_task: str, use_claude: bool = True) -> Dict[str, Any]:
        """
        Initialize Hive-Mind for complex projects

        Hive-Mind features:
        - Queen-led coordination
        - Project-wide SQLite memory
        - Persistent sessions
        - Advanced coordination

        Args:
            project_task: Main project task
            use_claude: Use Claude AI

        Returns:
            Hive-Mind initialization result
        """
        try:
            cmd = ["npx", "claude-flow@alpha", "hive-mind", "spawn", project_task]

            if use_claude:
                cmd.append("--claude")

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=300
            )

            return {
                "success": result.returncode == 0,
                "project_task": project_task,
                "output": result.stdout,
            }

        except Exception as e:
            logger.error(f"❌ Error initializing hive-mind: {e}")
            return {"success": False, "error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """
        Comprehensive health check for Claude-Flow integration

        Returns:
            Health status with detailed diagnostics
        """
        health = {
            "claude_flow_initialized": self._initialized,
            "node_available": False,
            "npm_available": False,
            "claude_flow_available": False,
            "swarm_dir_exists": self.swarm_dir.exists(),
            "memory_db_exists": self.memory_db.exists(),
            "recommendations": [],
        }

        try:
            # Check Node.js
            node_result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True, timeout=5
            )
            if node_result.returncode == 0:
                health["node_available"] = True
                health["node_version"] = node_result.stdout.strip()
            else:
                health["recommendations"].append("Install Node.js from https://nodejs.org/")

            # Check npm/npx
            npm_result = subprocess.run(
                ["npx", "--version"], capture_output=True, text=True, timeout=5
            )
            if npm_result.returncode == 0:
                health["npm_available"] = True
                health["npx_version"] = npm_result.stdout.strip()

            # Check Claude-Flow
            if health["node_available"] and health["npm_available"]:
                cf_result = subprocess.run(
                    ["npx", "claude-flow@alpha", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if cf_result.returncode == 0:
                    health["claude_flow_available"] = True
                    health["claude_flow_version"] = cf_result.stdout.strip()
                else:
                    health["recommendations"].append("Run: npm install -g claude-flow@alpha")

            health["status"] = "healthy" if health["claude_flow_available"] else "degraded"

        except Exception as e:
            health["status"] = "unhealthy"
            health["error"] = str(e)

        return health

    async def get_swarm_status(self) -> Dict[str, Any]:
        """Get current swarm status"""
        try:
            cmd = ["npx", "claude-flow@alpha", "swarm", "status"]

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(self.swarm_dir), timeout=10
            )

            return {"success": result.returncode == 0, "status": result.stdout}

        except Exception as e:
            logger.error(f"❌ Error getting swarm status: {e}")
            return {"success": False, "error": str(e)}

    async def execute_with_mcp_tools(self, task: str, tools: List[str]) -> Dict[str, Any]:
        """
        Execute task using specific MCP tools from Claude-Flow's 100 tools

        Available tool categories:
        - Core: swarm_init, agent_spawn, task_orchestrate
        - Memory: memory_usage, memory_search
        - Neural: neural_status, neural_train
        - GitHub: github_repo_analyze, github_pr_manage
        - Performance: benchmark_run, bottleneck_analyze

        Args:
            task: Task description
            tools: List of MCP tool names

        Returns:
            Execution result
        """
        try:
            # This would use MCP protocol - for now, route through swarm
            return await self.execute_task(
                task=f"{task} (using tools: {', '.join(tools)})", use_claude=True
            )

        except Exception as e:
            logger.error(f"❌ Error executing with MCP tools: {e}")
            return {"success": False, "error": str(e)}


# Singleton instance
_claude_flow_instance: Optional[ClaudeFlowIntegration] = None


async def get_claude_flow() -> ClaudeFlowIntegration:
    """Get or create Claude-Flow integration instance"""
    global _claude_flow_instance

    if _claude_flow_instance is None:
        _claude_flow_instance = ClaudeFlowIntegration()
        await _claude_flow_instance.initialize()

    return _claude_flow_instance
