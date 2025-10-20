# flake8: noqa: W293,E501
"""
Agent Generator - Generiert projektspezifische Agents basierend auf Analyse
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from llm.model_manager import ModelManager
from llm.prompt_templates import AGENT_GENERATION_PROMPT

logger = logging.getLogger(__name__)


class AgentGenerator:
    """Generates specialized agents based on project analysis.

    Uses LLM prompts and predefined templates to generate code for different
    agent types (backend, frontend, database, api, test, security, deployment)
    depending on the detected project characteristics.

    Attributes:
        model_manager: Provides access to the configured LLM model.
        generated_agents: Cache of the most recently generated agent artifacts.
        agent_templates: String templates keyed by agent type.
    """

    def __init__(self, model_manager: ModelManager) -> None:
        self.model_manager = model_manager
        self.generated_agents = {}
        self.agent_templates = self._load_agent_templates()

    def _load_agent_templates(self) -> Dict[str, str]:
        """Load agent templates for various project types.

        Returns:
            Mapping of agent_type to template string with placeholders.
        """
        return {
            "backend": self._get_backend_agent_template(),
            "frontend": self._get_frontend_agent_template(),
            "database": self._get_database_agent_template(),
            "api": self._get_api_agent_template(),
            "test": self._get_test_agent_template(),
            "security": self._get_security_agent_template(),
            "deployment": self._get_deployment_agent_template(),
        }

    async def generate_agents_for_project(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agents based on comprehensive project analysis results.

        Args:
            analysis_results: Dictionary of detected languages, frameworks,
                dependencies, structure and other analysis metadata.

        Returns:
            Dictionary keyed by agent_type with file_path, code and status.
        """
        try:
            logger.info("🤖 Starting agent generation for project...")

            project_name = analysis_results.get("project_name", "unknown_project")
            generated_agents = {}

            # Bestimme benötigte Agent-Typen basierend auf der Analyse
            required_agents = self._determine_required_agents(analysis_results)

            for agent_type in required_agents:
                logger.info(f"🤖 Generating {agent_type} agent...")

                agent_code = await self._generate_agent_code(
                    agent_type=agent_type,
                    project_name=project_name,
                    analysis_results=analysis_results,
                )

                # Speichere generierten Agent
                agent_file_path = await self._save_agent_file(
                    agent_type=agent_type, project_name=project_name, agent_code=agent_code
                )

                generated_agents[agent_type] = {
                    "file_path": agent_file_path,
                    "code": agent_code,
                    "status": "generated",
                }

                logger.info(f"✅ Generated {agent_type} agent: {agent_file_path}")

            self.generated_agents = generated_agents
            return generated_agents

        except Exception as e:
            logger.error(f"❌ Error generating agents: {e}")
            raise

    def _determine_required_agents(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Determine which agent types are required from analysis results.

        Args:
            analysis_results: Project analysis dictionary.

        Returns:
            Ordered list of agent type strings to be generated.
        """
        required_agents = []

        # Backend Agent - wenn Python/Node.js Backend erkannt
        languages = analysis_results.get("languages", {})
        if "Python" in languages or "JavaScript" in languages or "TypeScript" in languages:
            required_agents.append("backend")

        # Frontend Agent - wenn HTML/CSS/JS erkannt
        if "HTML" in languages or "CSS" in languages or "JavaScript" in languages:
            required_agents.append("frontend")

        # Database Agent - wenn Datenbanken erkannt
        databases = analysis_results.get("databases", [])
        if databases:
            required_agents.append("database")

        # API Agent - wenn APIs erkannt
        apis = analysis_results.get("apis", [])
        if apis:
            required_agents.append("api")

        # Test Agent - wenn Test-Frameworks erkannt
        dependencies = analysis_results.get("dependencies", {})
        if self._has_test_frameworks(dependencies):
            required_agents.append("test")

        # Security Agent - immer generieren
        required_agents.append("security")

        # Deployment Agent - wenn Docker/Deployment-Files erkannt
        if self._has_deployment_files(analysis_results):
            required_agents.append("deployment")

        return required_agents

    def _has_test_frameworks(self, dependencies: Dict[str, Any]) -> bool:
        """Check whether test frameworks are present in dependencies.

        Args:
            dependencies: Dependency map by language or package manager.

        Returns:
            True if a known test framework is detected, otherwise False.
        """
        test_keywords = ["pytest", "jest", "mocha", "unittest", "vitest"]

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                for dep in deps["dependencies"]:
                    if any(keyword in dep.lower() for keyword in test_keywords):
                        return True
        return False

    def _has_deployment_files(self, analysis_results: Dict[str, Any]) -> bool:
        """Check whether deployment-related files are present.

        Args:
            analysis_results: Project analysis dictionary with structure text.

        Returns:
            True when deployment indicators are found, otherwise False.
        """
        # Einfache Heuristik: Prüfe auf Docker, Kubernetes, etc.
        structure = analysis_results.get("structure", "")
        deployment_keywords = ["dockerfile", "docker-compose", "kubernetes", "deployment"]

        return any(keyword in structure.lower() for keyword in deployment_keywords)

    async def _generate_agent_code(
        self, agent_type: str, project_name: str, analysis_results: Dict[str, Any]
    ) -> str:
        """Generate concrete agent implementation code using the LLM.

        Args:
            agent_type: Agent type identifier (e.g., "backend").
            project_name: Current project name slug.
            analysis_results: Project analysis dictionary.

        Returns:
            Rendered agent source code string.
        """
        try:
            # Hole Template
            template = self.agent_templates.get(agent_type, self._get_generic_agent_template())

            # Erstelle Prompt für LLM
            prompt = AGENT_GENERATION_PROMPT.format(
                analysis_results=json.dumps(analysis_results, indent=2),
                agent_name=agent_type,
                agent_role=self._get_agent_role(agent_type),
                agent_goal=self._get_agent_goal(agent_type),
                required_skills=self._get_required_skills(agent_type),
            )

            # Generiere Code mit LLM
            model = self.model_manager.get_model()
            generated_code = await model.generate_response(prompt)

            # Kombiniere Template mit generiertem Code
            agent_class_name = f"{agent_type.title()}Agent" if agent_type else "GenericAgent"
            final_code = template.format(
                agent_name=agent_type or "generic",
                agent_class=agent_class_name,
                generated_implementation=generated_code,
                project_name=project_name,
            )

            return final_code

        except Exception as e:
            logger.error(f"❌ Error generating code for {agent_type} agent: {e}")
            # Fallback zu Template
            agent_class_name = f"{agent_type.title()}Agent" if agent_type else "GenericAgent"
            return self.agent_templates.get(agent_type, self._get_generic_agent_template()).format(
                agent_name=agent_type or "generic",
                agent_class=agent_class_name,
                generated_implementation="# Error generating agent implementation with LLM",
                project_name=project_name,
            )

    async def _save_agent_file(self, agent_type: str, project_name: str, agent_code: str) -> str:
        """Persist generated agent code to disk and return file path.

        Args:
            agent_type: Agent type identifier.
            project_name: Project name slug.
            agent_code: Generated agent source code.

        Returns:
            File system path to the saved agent.
        """
        try:
            # Erstelle agents/generated Verzeichnis
            generated_dir = Path("agents/generated")
            generated_dir.mkdir(parents=True, exist_ok=True)

            # Dateiname
            filename = f"{project_name}_{agent_type}_agent.py"
            file_path = generated_dir / filename

            # Speichere Code
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(agent_code)

            return str(file_path)

        except Exception as e:
            logger.error(f"❌ Error saving agent file: {e}")
            raise

    def _get_agent_role(self, agent_type: str) -> str:
        """Return the human-readable role description for an agent type.

        Args:
            agent_type: Agent type identifier.

        Returns:
            Descriptive role string.
        """
        roles = {
            "backend": "Backend-Entwicklung und -Optimierung",
            "frontend": "Frontend-Entwicklung und UI/UX",
            "database": "Datenbank-Management und -Optimierung",
            "api": "API-Entwicklung und -Integration",
            "test": "Test-Automatisierung und Qualitätssicherung",
            "security": "Sicherheits-Audits und -Optimierung",
            "deployment": "Deployment und DevOps",
        }
        return roles.get(agent_type, "Allgemeine Projekt-Unterstützung")

    def _get_agent_goal(self, agent_type: str) -> str:
        """Return the main goal statement for an agent type.

        Args:
            agent_type: Agent type identifier.

        Returns:
            Descriptive goal string.
        """
        goals = {
            "backend": "Optimierung der Backend-Performance und -Architektur",
            "frontend": "Verbesserung der Benutzererfahrung und Performance",
            "database": "Optimierung der Datenbank-Performance und -Sicherheit",
            "api": "Verbesserung der API-Performance und -Dokumentation",
            "test": "Erhöhung der Test-Abdeckung und -Qualität",
            "security": "Erhöhung der Sicherheit und Compliance",
            "deployment": "Automatisierung und Optimierung des Deployments",
        }
        return goals.get(agent_type, "Verbesserung der Projekt-Qualität")

    def _get_required_skills(self, agent_type: str) -> List[str]:
        """Return the required skills for a given agent type.

        Args:
            agent_type: Agent type identifier.

        Returns:
            List of skill identifiers.
        """
        skills = {
            "backend": ["code_analysis", "performance_optimization", "refactoring"],
            "frontend": ["ui_optimization", "performance_optimization", "accessibility"],
            "database": ["query_optimization", "schema_analysis", "migration_management"],
            "api": ["endpoint_analysis", "documentation", "performance_optimization"],
            "test": ["test_generation", "coverage_analysis", "test_optimization"],
            "security": ["security_audit", "vulnerability_scan", "compliance_check"],
            "deployment": ["deployment_automation", "infrastructure_analysis", "monitoring"],
        }
        return skills.get(agent_type, ["general_analysis"])

    def _get_backend_agent_template(self) -> str:
        """Return the backend agent template string."""
        return '''"""
{agent_class} - Automatisch generierter Backend-Agent
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class {agent_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.agent_type = "backend"
    
    async def initialize(self):
        """Initialisiert den Agent"""
        logger.info(f"🚀 Initializing {self.agent_type} agent for project: {self.project_name}")
    
    async def analyze_backend(self, **kwargs) -> Dict[str, Any]:
        """Analysiert das Backend des Projekts"""
        logger.info("🔍 Starting backend analysis...")
        
        results = {{
            "backend_files": 0,
            "api_endpoints": 0,
            "performance_issues": [],
            "optimization_suggestions": []
        }}
        
        try:
            # Analysiere Backend-Dateien
            backend_files = list(self.project_path.rglob("*.py")) + list(self.project_path.rglob("*.js"))
            results["backend_files"] = len(backend_files)
            
            # Generierte Implementation vom LLM
            {generated_implementation}
            
            logger.info(f"✅ Backend analysis completed: {results}")
            
        except Exception as e:
            logger.error(f"❌ Error in backend analysis: {e}")
            results["error"] = str(e)
        
        return results
    
    async def optimize_performance(self, **kwargs) -> Dict[str, Any]:
        """Optimiert die Backend-Performance"""
        logger.info("⚡ Starting performance optimization...")
        
        optimizations = []
        
        # Einfache Optimierungen
        optimizations.append("Consider using async/await for I/O operations")
        optimizations.append("Review database query performance")
        optimizations.append("Implement caching for frequently accessed data")
        
        logger.info(f"✅ Performance optimization completed: {len(optimizations)} suggestions")
        return {{"optimizations": optimizations}}
    
    async def get_status(self) -> Dict[str, Any]:
        """Gibt den Status des Agents zurück"""
        return {{
            "agent_type": self.agent_type,
            "status": "active",
            "project_name": self.project_name
        }}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {self.agent_type} agent")
'''

    def _get_generic_agent_template(self) -> str:
        """Return the generic agent template string."""
        return '''"""
{agent_class} - Automatisch generierter Agent
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class {agent_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.agent_type = "generic"
    
    async def initialize(self):
        """Initialisiert den Agent"""
        logger.info(f"🚀 Initializing {self.agent_type} agent for project: {self.project_name}")
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Führt den Agent aus"""
        logger.info(f"🔧 Starting {self.agent_type} agent execution")
        
        results = {{
            "agent_type": self.agent_type,
            "execution_successful": True,
            "output": "Agent executed successfully"
        }}
        
        try:
            # Generierte Implementation vom LLM
            {generated_implementation}
            
            logger.info(f"✅ {self.agent_type} agent completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error in {self.agent_type} agent: {e}")
            results["error"] = str(e)
            results["execution_successful"] = False
        
        return results
    
    async def get_status(self) -> Dict[str, Any]:
        """Gibt den Status des Agents zurück"""
        return {{
            "agent_type": self.agent_type,
            "status": "active",
            "project_name": self.project_name
        }}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {self.agent_type} agent")
'''

    # Weitere Templates für andere Agent-Typen...
    def _get_frontend_agent_template(self) -> str:
        """Return the frontend agent template string."""
        return self._get_generic_agent_template()

    def _get_database_agent_template(self) -> str:
        """Return the database agent template string."""
        return self._get_generic_agent_template()

    def _get_api_agent_template(self) -> str:
        """Return the API agent template string."""
        return self._get_generic_agent_template()

    def _get_test_agent_template(self) -> str:
        """Return the test agent template string."""
        return self._get_generic_agent_template()

    def _get_security_agent_template(self) -> str:
        """Return the security agent template string."""
        return self._get_generic_agent_template()

    def _get_deployment_agent_template(self) -> str:
        """Return the deployment agent template string."""
        return self._get_generic_agent_template()
