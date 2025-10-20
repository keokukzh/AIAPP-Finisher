"""
Agent Coordinator - Coordinates agent creation and request handling
Implements Coordinator pattern for agents
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AgentCoordinator:
    """Coordinates agent generation and request handling using composition"""

    def __init__(self, agent_generator, agent_orchestrator, project_manager_agent):
        # Composition over inheritance - inject dependencies
        self.agent_generator = agent_generator
        self.agent_orchestrator = agent_orchestrator
        self.project_manager_agent = project_manager_agent

        self.active_agents = {}
        self.request_history = []

    async def generate_and_initialize_agents(
        self, analysis_results: Dict[str, Any], progress_callback=None
    ) -> Dict[str, Any]:
        """Generate and initialize agents for a project"""
        results = {"agents_generated": [], "agents_initialized": [], "failed_agents": []}

        try:
            # Phase 1: Generate agents
            if progress_callback:
                progress_callback("Generating agents", 0.0)

            generated = await self.agent_generator.generate_agents_for_project(analysis_results)

            results["agents_generated"] = [a["name"] for a in generated]

            # Phase 2: Initialize via orchestrator
            if progress_callback:
                progress_callback("Initializing agents", 0.5)

            for agent_data in generated:
                try:
                    agent_name = agent_data["name"]

                    # Register agent
                    self.active_agents[agent_name] = {
                        "name": agent_name,
                        "type": agent_data.get("type", "generic"),
                        "status": "initialized",
                        "data": agent_data,
                    }

                    results["agents_initialized"].append(agent_name)

                except Exception as e:
                    logger.error(f"Failed to initialize agent {agent_data.get('name')}: {e}")
                    results["failed_agents"].append(
                        {"name": agent_data.get("name"), "error": str(e)}
                    )

            if progress_callback:
                progress_callback("Agents ready", 1.0)

            logger.info(
                f"Agent coordination complete: {len(results['agents_initialized'])} initialized, "
                f"{len(results['failed_agents'])} failed"
            )

        except Exception as e:
            logger.error(f"Error coordinating agents: {e}")
            raise

        return results

    async def handle_request(
        self, request_type: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate request handling across agents"""
        try:
            # Route request to project manager agent
            response = await self.project_manager_agent.chat(
                request_data.get("message", ""), request_data.get("context")
            )

            # Record in history
            self.request_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "type": request_type,
                    "response_length": len(response),
                }
            )

            return {"status": "success", "response": response}

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            raise

    async def get_agent_status(self, agent_name: str = None) -> Dict[str, Any]:
        """Get status of agents"""
        if agent_name:
            return self.active_agents.get(agent_name, {})
        else:
            return {"active_count": len(self.active_agents), "agents": self.active_agents}

    def get_request_history(self) -> List[Dict[str, Any]]:
        """Get request history"""
        return self.request_history
