"""
Workflow Generator - Generiert projektspezifische Workflows basierend auf Analyse
Refactored to use dedicated workflow builders
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from llm.model_manager import ModelManager
from llm.prompt_templates import WORKFLOW_GENERATION_PROMPT

from .workflow_builders import (
    BuildDeploymentWorkflowBuilder,
    CICDSecurityWorkflowBuilder,
    PerformanceWorkflowBuilder,
    TestingWorkflowBuilder,
)

logger = logging.getLogger(__name__)


class WorkflowGenerator:
    """Coordinates workflow generation using specialized builders.

    Uses project analysis results to determine which workflows are needed
    (testing, build, deployment, CI/CD, security, performance) and then
    renders code via LLM prompts combined with builder-provided templates.

    Attributes:
        model_manager: Provides access to the active LLM model.
        generated_workflows: Cache of generated workflow artifacts.
        testing_builder: Builder responsible for testing workflow templates.
        build_deployment_builder: Builder for build and deployment templates.
        cicd_security_builder: Builder for CI/CD and security templates.
        performance_builder: Builder for performance templates and generic fallback.
    """

    def __init__(self, model_manager: ModelManager) -> None:
        self.model_manager = model_manager
        self.generated_workflows = {}
        self._initialize_builders()

    def _initialize_builders(self) -> None:
        """Initialize workflow builders for all supported workflow types."""
        self.testing_builder = TestingWorkflowBuilder()
        self.build_deployment_builder = BuildDeploymentWorkflowBuilder()
        self.cicd_security_builder = CICDSecurityWorkflowBuilder()
        self.performance_builder = PerformanceWorkflowBuilder()

    async def generate_workflows_for_project(
        self, analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate workflows based on comprehensive project analysis.

        Args:
            analysis_results: Dictionary containing frameworks, dependencies,
                structure, and other metadata from project analysis.

        Returns:
            Dictionary keyed by workflow_type with file_path, code and status.
        """
        try:
            logger.info("🔄 Starting workflow generation for project...")

            project_name = analysis_results.get("project_name", "unknown_project")
            generated_workflows = {}

            # Bestimme benötigte Workflow-Typen basierend auf der Analyse
            required_workflows = self._determine_required_workflows(analysis_results)

            for workflow_type in required_workflows:
                logger.info(f"🔧 Generating {workflow_type} workflow...")

                workflow_code = await self._generate_workflow_code(
                    workflow_type=workflow_type,
                    project_name=project_name,
                    analysis_results=analysis_results,
                )

                # Speichere generierten Workflow
                workflow_file_path = await self._save_workflow_file(
                    workflow_type=workflow_type,
                    project_name=project_name,
                    workflow_code=workflow_code,
                )

                generated_workflows[workflow_type] = {
                    "file_path": workflow_file_path,
                    "code": workflow_code,
                    "status": "generated",
                }

                logger.info(f"✅ Generated {workflow_type} workflow: {workflow_file_path}")

            self.generated_workflows = generated_workflows
            return generated_workflows

        except Exception as e:
            logger.error(f"❌ Error generating workflows: {e}")
            raise

    def _determine_required_workflows(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Determine required workflow types from analysis results.

        Args:
            analysis_results: Project analysis dictionary.

        Returns:
            Ordered list of workflow type strings to be generated.
        """
        required_workflows = []

        # Testing Workflow - immer generieren
        required_workflows.append("testing")

        # Build Workflow - wenn Build-Tools erkannt
        frameworks = analysis_results.get("frameworks", {})
        if any(
            fw in ["React", "Vue.js", "Angular", "Next.js", "Nuxt.js", "Webpack", "Vite"]
            for fw in frameworks.keys()
        ):
            required_workflows.append("build")

        # Deployment Workflow - wenn Deployment-Configs erkannt
        if self._has_deployment_configs(analysis_results):
            required_workflows.append("deployment")

        # CI/CD Workflow - wenn Git-Repository erkannt
        if (Path(analysis_results.get("project_path", "")) / ".git").exists():
            required_workflows.append("ci_cd")

        # Security Workflow - wenn Security-relevante Dependencies
        dependencies = analysis_results.get("dependencies", {})
        if self._has_security_dependencies(dependencies):
            required_workflows.append("security")

        # Performance Workflow - wenn Performance-kritische Frameworks
        if any(
            fw in ["FastAPI", "Django", "Express.js", "React", "Vue.js"] for fw in frameworks.keys()
        ):
            required_workflows.append("performance")

        return required_workflows

    def _has_deployment_configs(self, analysis_results: Dict[str, Any]) -> bool:
        """Check whether deployment configuration files are present.

        Args:
            analysis_results: Project analysis results containing structure text.

        Returns:
            True if any known deployment file or directory is mentioned.
        """
        structure = analysis_results.get("structure", "")
        deployment_files = ["docker-compose.yml", "Dockerfile", "k8s", "kubernetes", "deploy"]

        return any(file in structure for file in deployment_files)

    def _has_security_dependencies(self, dependencies: Dict[str, Any]) -> bool:
        """Check presence of security-relevant dependencies.

        Args:
            dependencies: Dependency map by language or package manager.

        Returns:
            True if a known security-related package name is detected.
        """
        security_keywords = ["auth", "security", "jwt", "oauth", "cors", "helmet", "bcrypt"]

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                for dep in deps["dependencies"]:
                    if any(keyword in dep.lower() for keyword in security_keywords):
                        return True
        return False

    async def _generate_workflow_code(
        self, workflow_type: str, project_name: str, analysis_results: Dict[str, Any]
    ) -> str:
        """Generate concrete workflow implementation code using the LLM.

        Args:
            workflow_type: Workflow type identifier (e.g., "testing").
            project_name: Project name slug.
            analysis_results: Project analysis dictionary.

        Returns:
            Rendered workflow source code string.
        """
        try:
            # Hole Template vom entsprechenden Builder
            template = self._get_template_for_type(workflow_type)

            # Erstelle Prompt für LLM
            prompt = WORKFLOW_GENERATION_PROMPT.format(
                analysis_results=json.dumps(analysis_results, indent=2),
                workflow_type=workflow_type,
                project_name=project_name,
                project_frameworks=self._get_project_frameworks(analysis_results),
                project_dependencies=self._get_project_dependencies(analysis_results),
            )

            # Generiere Code mit LLM
            model = self.model_manager.get_model()
            generated_code = await model.generate_response(prompt)

            # Kombiniere Template mit generiertem Code
            final_code = template.format(
                workflow_name=f"{project_name}_{workflow_type}",
                workflow_class=f"{project_name.title()}{workflow_type.title()}Workflow",
                generated_steps=generated_code,
                project_name=project_name,
            )

            return final_code

        except Exception as e:
            logger.error(f"❌ Error generating code for {workflow_type} workflow: {e}")
            # Fallback zu Template
            template = self._get_template_for_type(workflow_type)
            return template.format(
                workflow_name=f"{project_name}_{workflow_type}",
                workflow_class=f"{project_name.title()}{workflow_type.title()}Workflow",
                generated_steps="# Error generating workflow steps with LLM",
                project_name=project_name,
            )

    def _get_template_for_type(self, workflow_type: str) -> str:
        """Return the template string for a specific workflow type.

        Args:
            workflow_type: Workflow type identifier.

        Returns:
            Template string provided by the appropriate builder.
        """
        template_map = {
            "testing": self.testing_builder.get_template(),
            "build": self.build_deployment_builder.get_build_template(),
            "deployment": self.build_deployment_builder.get_deployment_template(),
            "ci_cd": self.cicd_security_builder.get_cicd_template(),
            "security": self.cicd_security_builder.get_security_template(),
            "performance": self.performance_builder.get_performance_template(),
            "generic": self.performance_builder.get_generic_template(),
        }

        return template_map.get(workflow_type, self.performance_builder.get_generic_template())

    async def _save_workflow_file(
        self, workflow_type: str, project_name: str, workflow_code: str
    ) -> str:
        """Persist generated workflow code to disk and return file path.

        Args:
            workflow_type: Workflow type identifier.
            project_name: Project name slug.
            workflow_code: Generated workflow source code.

        Returns:
            File system path to the saved workflow file.
        """
        try:
            # Erstelle workflows/generated Verzeichnis
            generated_dir = Path("workflows/generated")
            generated_dir.mkdir(parents=True, exist_ok=True)

            # Dateiname
            filename = f"{project_name}_{workflow_type}_workflow.py"
            file_path = generated_dir / filename

            # Speichere Code
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(workflow_code)

            return str(file_path)

        except Exception as e:
            logger.error(f"❌ Error saving workflow file: {e}")
            raise

    def _get_project_frameworks(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Gibt die erkannten Frameworks zurück"""
        frameworks = analysis_results.get("frameworks", {})
        return list(frameworks.keys())

    def _get_project_dependencies(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Gibt die wichtigsten Dependencies zurück"""
        dependencies = analysis_results.get("dependencies", {})
        all_deps = []

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                all_deps.extend(deps["dependencies"][:5])  # Top 5 pro Sprache

        return all_deps
