"""Agent Orchestrator - generation and execution coordination.

Coordinates automatic generation of agents, workflows, and skills based on
analysis results, initializes runtime instances, executes generated flows,
and aggregates a run summary.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

from generators.agent_generator import AgentGenerator
from generators.skill_generator import SkillGenerator
from generators.workflow_generator import WorkflowGenerator
from llm.model_manager import ModelManager

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """High-level coordinator for agent, workflow, and skill orchestration.

    Attributes:
        model_manager: LLM model manager used by downstream generators.
        agent_generator: Generator responsible for agent code creation.
        workflow_generator: Generator responsible for workflow code creation.
        skill_generator: Generator responsible for skill code creation.
        generated_agents: Cache of generated agent artifacts.
        generated_workflows: Cache of generated workflow artifacts.
        generated_skills: Cache of generated skill artifacts.
        active_agents: Mapping of agent type to initialized runtime instances.
    """

    def __init__(self, model_manager: ModelManager) -> None:
        self.model_manager = model_manager
        self.agent_generator = AgentGenerator(model_manager)
        self.workflow_generator = WorkflowGenerator(model_manager)
        self.skill_generator = SkillGenerator(model_manager)

        self.generated_agents = {}
        self.generated_workflows = {}
        self.generated_skills = {}
        self.active_agents = {}

    async def orchestrate_project_automation(
        self, analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run full project automation pipeline and return a result summary.

        Args:
            analysis_results: Dictionary produced by the analysis engine.

        Returns:
            Dictionary with orchestration status, generated artifacts, and summary.
        """
        try:
            logger.info("🎭 Starting project automation orchestration...")

            project_name = analysis_results.get("project_name", "unknown_project")

            # Phase 1: Generiere Agents
            logger.info("🤖 Phase 1: Generating agents...")
            self.generated_agents = await self.agent_generator.generate_agents_for_project(
                analysis_results
            )

            # Phase 2: Generiere Workflows
            logger.info("🔄 Phase 2: Generating workflows...")
            self.generated_workflows = await self.workflow_generator.generate_workflows_for_project(
                analysis_results
            )

            # Phase 3: Generiere Skills
            logger.info("🛠️ Phase 3: Generating skills...")
            self.generated_skills = await self.skill_generator.generate_skills_for_project(
                analysis_results
            )

            # Phase 4: Initialisiere und starte Agents
            logger.info("🚀 Phase 4: Initializing and starting agents...")
            await self._initialize_agents(analysis_results)

            # Phase 5: Führe Workflows aus
            logger.info("⚡ Phase 5: Executing workflows...")
            workflow_results = await self._execute_workflows()

            # Phase 6: Generiere Zusammenfassung
            logger.info("📊 Phase 6: Generating summary...")
            summary = await self._generate_summary(analysis_results, workflow_results)

            logger.info("✅ Project automation orchestration completed successfully")

            return {
                "project_name": project_name,
                "orchestration_status": "completed",
                "generated_agents": self.generated_agents,
                "generated_workflows": self.generated_workflows,
                "generated_skills": self.generated_skills,
                "active_agents": self.active_agents,
                "workflow_results": workflow_results,
                "summary": summary,
            }

        except Exception as e:
            logger.error(f"❌ Error in project automation orchestration: {e}")
            return {"orchestration_status": "failed", "error": str(e)}

    async def _initialize_agents(self, analysis_results: Dict[str, Any]) -> None:
        """Initialize generated agent instances if files are present.

        Args:
            analysis_results: Project analysis dictionary (used for project_path).
        """
        try:
            project_path = analysis_results.get("project_path", ".")

            for agent_type, agent_info in self.generated_agents.items():
                logger.info(f"🔧 Initializing {agent_type} agent...")

                # Lade den generierten Agent-Code
                agent_file_path = agent_info.get("file_path")
                if agent_file_path and Path(agent_file_path).exists():
                    # Importiere und initialisiere den Agent
                    agent_instance = await self._load_agent_instance(agent_file_path, project_path)
                    if agent_instance:
                        self.active_agents[agent_type] = agent_instance
                        logger.info(f"✅ {agent_type} agent initialized successfully")
                    else:
                        logger.warning(f"⚠️ Failed to initialize {agent_type} agent")
                else:
                    logger.warning(f"⚠️ Agent file not found: {agent_file_path}")

        except Exception as e:
            logger.error(f"❌ Error initializing agents: {e}")

    async def _load_agent_instance(self, agent_file_path: str, project_path: str):
        """Load an agent instance from a generated file path.

        Args:
            agent_file_path: File system path to generated agent module.
            project_path: Project path passed to agent constructor.

        Returns:
            Initialized agent instance or None if loading fails.
        """
        try:
            # Dynamischer Import des generierten Agents
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location("generated_agent", agent_file_path)
            if spec is None:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules["generated_agent"] = module
            spec.loader.exec_module(module)

            # Finde die Agent-Klasse
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "__init__") and "Agent" in attr_name:

                    # Erstelle Agent-Instanz
                    agent_instance = attr(project_path)
                    await agent_instance.initialize()
                    return agent_instance

            return None

        except Exception as e:
            logger.error(f"❌ Error loading agent instance: {e}")
            return None

    async def _execute_workflows(self) -> Dict[str, Any]:
        """Execute all generated workflows and collect their results.

        Returns:
            Mapping of workflow type to execution result payload.
        """
        workflow_results = {}

        try:
            for workflow_type, workflow_info in self.generated_workflows.items():
                logger.info(f"🔄 Executing {workflow_type} workflow...")

                # Lade und führe Workflow aus
                workflow_file_path = workflow_info.get("file_path")
                if workflow_file_path and Path(workflow_file_path).exists():
                    result = await self._execute_workflow(workflow_file_path)
                    workflow_results[workflow_type] = result
                    logger.info(f"✅ {workflow_type} workflow completed")
                else:
                    logger.warning(f"⚠️ Workflow file not found: {workflow_file_path}")
                    workflow_results[workflow_type] = {
                        "status": "failed",
                        "error": "File not found",
                    }

        except Exception as e:
            logger.error(f"❌ Error executing workflows: {e}")
            workflow_results["error"] = str(e)

        return workflow_results

    async def _execute_workflow(self, workflow_file_path: str) -> Dict[str, Any]:
        """Execute a single generated workflow module by dynamic import.

        Args:
            workflow_file_path: File system path to the generated workflow module.

        Returns:
            Workflow execution result dictionary with status and details.
        """
        try:
            # Dynamischer Import des generierten Workflows
            import importlib.util
            import sys

            spec = importlib.util.spec_from_file_location("generated_workflow", workflow_file_path)
            if spec is None:
                return {"status": "failed", "error": "Could not load workflow"}

            module = importlib.util.module_from_spec(spec)
            sys.modules["generated_workflow"] = module
            spec.loader.exec_module(module)

            # Finde die Workflow-Klasse
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "execute") and "Workflow" in attr_name:

                    # Erstelle Workflow-Instanz und führe aus
                    workflow_instance = attr(".")
                    result = await workflow_instance.execute()
                    await workflow_instance.cleanup()
                    return result

            return {"status": "failed", "error": "No workflow class found"}

        except Exception as e:
            logger.error(f"❌ Error executing workflow: {e}")
            return {"status": "failed", "error": str(e)}

    async def _generate_summary(
        self, analysis_results: Dict[str, Any], workflow_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate an orchestration summary from inputs and results.

        Args:
            analysis_results: Source analysis dictionary for high-level metrics.
            workflow_results: Results mapping for executed workflows.

        Returns:
            Summary dictionary with counts, generated artifacts, and recommendations.
        """
        try:
            summary = {
                "project_name": analysis_results.get("project_name", "unknown"),
                "total_agents_generated": len(self.generated_agents),
                "total_workflows_generated": len(self.generated_workflows),
                "total_skills_generated": len(self.generated_skills),
                "active_agents": len(self.active_agents),
                "workflows_executed": len(workflow_results),
                "successful_workflows": len(
                    [r for r in workflow_results.values() if r.get("status") != "failed"]
                ),
                "failed_workflows": len(
                    [r for r in workflow_results.values() if r.get("status") == "failed"]
                ),
                "generated_files": {
                    "agents": list(self.generated_agents.keys()),
                    "workflows": list(self.generated_workflows.keys()),
                    "skills": list(self.generated_skills.keys()),
                },
                "recommendations": self._generate_recommendations(
                    analysis_results, workflow_results
                ),
            }

            return summary

        except Exception as e:
            logger.error(f"❌ Error generating summary: {e}")
            return {"error": str(e)}

    def _generate_recommendations(
        self, analysis_results: Dict[str, Any], workflow_results: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on analysis and workflow outcomes.

        Args:
            analysis_results: Input analysis results.
            workflow_results: Mapping of workflow execution results.

        Returns:
            List of recommendation strings.
        """
        recommendations = []

        # Empfehlungen basierend auf der Analyse
        if analysis_results.get("file_count", 0) > 100:
            recommendations.append("Consider breaking down the project into smaller modules")

        if analysis_results.get("total_lines", 0) > 50000:
            recommendations.append("Consider implementing code splitting and lazy loading")

        # Empfehlungen basierend auf Workflow-Ergebnissen
        failed_workflows = [k for k, v in workflow_results.items() if v.get("status") == "failed"]
        if failed_workflows:
            recommendations.append(
                f"Review and fix failed workflows: {', '.join(failed_workflows)}"
            )

        # Allgemeine Empfehlungen
        recommendations.extend(
            [
                "Regularly run the generated agents to maintain code quality",
                "Update generated workflows as the project evolves",
                "Monitor the performance of generated skills and optimize as needed",
            ]
        )

        return recommendations

    async def get_agent_status(self) -> Dict[str, Any]:
        """Return status for all active agents."""
        status = {"total_agents": len(self.active_agents), "agent_status": {}}

        for agent_type, agent_instance in self.active_agents.items():
            try:
                if hasattr(agent_instance, "get_status"):
                    agent_status = await agent_instance.get_status()
                else:
                    agent_status = {"status": "active", "type": agent_type}

                status["agent_status"][agent_type] = agent_status

            except Exception as e:
                status["agent_status"][agent_type] = {"status": "error", "error": str(e)}

        return status

    async def cleanup(self) -> None:
        """Cleanup orchestrator state and underlying agent resources."""
        try:
            logger.info("🧹 Cleaning up agent orchestrator...")

            # Bereinige aktive Agents
            for agent_type, agent_instance in self.active_agents.items():
                try:
                    if hasattr(agent_instance, "cleanup"):
                        await agent_instance.cleanup()
                except Exception as e:
                    logger.error(f"❌ Error cleaning up {agent_type} agent: {e}")

            self.active_agents.clear()
            logger.info("✅ Agent orchestrator cleanup completed")

        except Exception as e:
            logger.error(f"❌ Error during orchestrator cleanup: {e}")
