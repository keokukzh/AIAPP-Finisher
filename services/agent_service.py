"""
Agent Service for KI-Projektmanagement-System
Contains business logic for agent management and generation
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AgentService:
    """Service class for agent-related operations"""

    def __init__(self, agent_orchestrator, project_manager_agent):
        self.agent_orchestrator = agent_orchestrator
        self.project_manager_agent = project_manager_agent
        self.loaded_agents: Dict[str, Any] = {}

    async def initialize_project_manager(self):
        """Initializes the project manager agent"""
        try:
            if self.project_manager_agent:
                await self.project_manager_agent.initialize()
                logger.info("✅ Project manager agent initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing project manager: {e}")
            raise

    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Sends a message to the project manager agent

        Args:
            message: Message to send
            context: Optional context dictionary

        Returns:
            Agent response string
        """
        try:
            if not self.project_manager_agent:
                raise ValueError("Project manager agent not available")

            response = await self.project_manager_agent.chat(message, context)
            return response

        except Exception as e:
            logger.error(f"❌ Error in chat: {e}")
            raise

    async def generate_agents(
        self, analysis_results: Dict[str, Any], agent_generator
    ) -> List[Dict[str, Any]]:
        """
        Generates agents based on analysis results

        Args:
            analysis_results: Project analysis results
            agent_generator: Agent generator instance

        Returns:
            List of generated agent definitions
        """
        try:
            logger.info("🤖 Generating agents from analysis results")

            generated_agents = await agent_generator.generate_from_analysis(analysis_results)

            # Store generated agents
            for agent in generated_agents:
                agent_name = agent.get("name", f"agent_{len(self.loaded_agents)}")
                self.loaded_agents[agent_name] = agent

            logger.info(f"✅ Generated {len(generated_agents)} agents")
            return generated_agents

        except Exception as e:
            logger.error(f"❌ Error generating agents: {e}")
            raise

    def get_agent_status(self) -> Dict[str, Any]:
        """Returns status of all loaded agents"""
        agent_list = []

        for agent_name, agent in self.loaded_agents.items():
            status = {
                "name": agent_name,
                "type": type(agent).__name__,
                "status": getattr(agent, "status", "unknown"),
            }

            if hasattr(agent, "get_status"):
                status.update(agent.get_status())

            agent_list.append(status)

        return {"total_agents": len(self.loaded_agents), "agents": agent_list}

    async def set_project_context(self, analysis_results: Dict[str, Any]):
        """Sets the project context for the project manager agent"""
        try:
            if self.project_manager_agent:
                await self.project_manager_agent.set_project_context(analysis_results)
                logger.info("✅ Project context set for agent")
        except Exception as e:
            logger.error(f"❌ Error setting project context: {e}")
            raise
