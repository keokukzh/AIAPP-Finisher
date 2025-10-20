"""
Skill Generator - Generiert projektspezifische Skills basierend auf Analyse
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from llm.model_manager import ModelManager
from llm.prompt_templates import SKILL_GENERATION_PROMPT

from .skill_templates import (
    get_code_analysis_skill_template,
    get_generic_skill_template,
    get_performance_optimization_skill_template,
)

logger = logging.getLogger(__name__)


class SkillGenerator:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.generated_skills = {}
        self.skill_templates = self._load_skill_templates()

    def _load_skill_templates(self) -> Dict[str, str]:
        """Lädt Skill-Templates für verschiedene Projekt-Typen"""
        return {
            "code_analysis": get_code_analysis_skill_template(),
            "performance_optimization": get_performance_optimization_skill_template(),
            "security_audit": get_generic_skill_template(),  # Placeholder
            "test_generation": get_generic_skill_template(),  # Placeholder
            "documentation": get_generic_skill_template(),  # Placeholder
            "refactoring": get_generic_skill_template(),  # Placeholder
            "dependency_management": get_generic_skill_template(),  # Placeholder
            "api_optimization": get_generic_skill_template(),  # Placeholder
        }

    async def generate_skills_for_project(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generiert Skills basierend auf der Projekt-Analyse"""
        try:
            logger.info("🛠️ Starting skill generation for project...")

            project_name = analysis_results.get("project_name", "unknown_project")
            generated_skills = {}

            # Bestimme benötigte Skill-Typen basierend auf der Analyse
            required_skills = self._determine_required_skills(analysis_results)

            for skill_type in required_skills:
                logger.info(f"🔧 Generating {skill_type} skill...")

                skill_code = await self._generate_skill_code(
                    skill_type=skill_type,
                    project_name=project_name,
                    analysis_results=analysis_results,
                )

                # Speichere generierten Skill
                skill_file_path = await self._save_skill_file(
                    skill_type=skill_type, project_name=project_name, skill_code=skill_code
                )

                generated_skills[skill_type] = {
                    "file_path": skill_file_path,
                    "code": skill_code,
                    "status": "generated",
                }

                logger.info(f"✅ Generated {skill_type} skill: {skill_file_path}")

            self.generated_skills = generated_skills
            return generated_skills

        except Exception as e:
            logger.error(f"❌ Error generating skills: {e}")
            raise

    def _determine_required_skills(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Bestimmt welche Skill-Typen basierend auf der Analyse benötigt werden"""
        required_skills = []

        # Code Analysis - immer generieren
        required_skills.append("code_analysis")

        # Performance Optimization - wenn Performance-kritische Frameworks
        frameworks = analysis_results.get("frameworks", {})
        if any(
            fw in ["FastAPI", "Django", "Express.js", "React", "Vue.js"] for fw in frameworks.keys()
        ):
            required_skills.append("performance_optimization")

        # Security Audit - wenn Security-relevante Dependencies
        dependencies = analysis_results.get("dependencies", {})
        if self._has_security_dependencies(dependencies):
            required_skills.append("security_audit")

        # Test Generation - wenn Test-Framework erkannt
        if self._has_test_frameworks(analysis_results):
            required_skills.append("test_generation")

        # Documentation - wenn komplexe APIs erkannt
        apis = analysis_results.get("apis", [])
        if apis:
            required_skills.append("documentation")

        # Refactoring - wenn komplexe Code-Struktur
        if self._has_complex_code_structure(analysis_results):
            required_skills.append("refactoring")

        # Dependency Management - wenn viele Dependencies
        if self._has_many_dependencies(dependencies):
            required_skills.append("dependency_management")

        # API Optimization - wenn API-Endpoints erkannt
        if any(api in ["FastAPI", "Flask API", "Express.js API"] for api in apis):
            required_skills.append("api_optimization")

        return required_skills

    def _has_security_dependencies(self, dependencies: Dict[str, Any]) -> bool:
        """Prüft ob Security-relevante Dependencies vorhanden sind"""
        security_keywords = ["auth", "security", "jwt", "oauth", "cors", "helmet", "bcrypt"]

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                for dep in deps["dependencies"]:
                    if any(keyword in dep.lower() for keyword in security_keywords):
                        return True
        return False

    def _has_test_frameworks(self, analysis_results: Dict[str, Any]) -> bool:
        """Prüft ob Test-Frameworks vorhanden sind"""
        dependencies = analysis_results.get("dependencies", {})
        test_keywords = ["pytest", "jest", "mocha", "unittest", "vitest"]

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                for dep in deps["dependencies"]:
                    if any(keyword in dep.lower() for keyword in test_keywords):
                        return True
        return False

    def _has_complex_code_structure(self, analysis_results: Dict[str, Any]) -> bool:
        """Prüft ob komplexe Code-Struktur vorhanden ist"""
        file_count = analysis_results.get("file_count", 0)
        total_lines = analysis_results.get("total_lines", 0)

        # Heuristik: Komplex wenn viele Dateien oder viele Zeilen
        return file_count > 50 or total_lines > 10000

    def _has_many_dependencies(self, dependencies: Dict[str, Any]) -> bool:
        """Prüft ob viele Dependencies vorhanden sind"""
        total_deps = 0

        for lang, deps in dependencies.items():
            if isinstance(deps, dict) and "dependencies" in deps:
                total_deps += len(deps["dependencies"])

        return total_deps > 20

    async def _generate_skill_code(
        self, skill_type: str, project_name: str, analysis_results: Dict[str, Any]
    ) -> str:
        """Generiert den Code für einen spezifischen Skill"""
        try:
            # Hole Template
            template = self.skill_templates.get(skill_type, self._get_generic_skill_template())

            # Erstelle Prompt für LLM
            prompt = SKILL_GENERATION_PROMPT.format(
                analysis_results=json.dumps(analysis_results, indent=2),
                skill_name=skill_type,
                skill_purpose=self._get_skill_purpose(skill_type),
                skill_inputs=self._get_skill_inputs(skill_type),
                skill_outputs=self._get_skill_outputs(skill_type),
                skill_dependencies=self._get_skill_dependencies(skill_type, analysis_results),
            )

            # Generiere Code mit LLM
            model = self.model_manager.get_model()
            generated_code = await model.generate_response(prompt)

            # Kombiniere Template mit generiertem Code
            final_code = template.format(
                skill_name=skill_type,
                skill_class=f"{skill_type.title()}Skill",
                generated_implementation=generated_code,
                project_name=project_name,
            )

            return final_code

        except Exception as e:
            logger.error(f"❌ Error generating code for {skill_type} skill: {e}")
            # Fallback zu Template
            return self.skill_templates.get(skill_type, self._get_generic_skill_template()).format(
                skill_name=skill_type,
                skill_class=f"{skill_type.title()}Skill",
                generated_implementation="# Error generating skill implementation with LLM",
                project_name=project_name,
            )

    async def _save_skill_file(self, skill_type: str, project_name: str, skill_code: str) -> str:
        """Speichert den generierten Skill-Code in eine Datei"""
        try:
            # Erstelle skills/generated Verzeichnis
            generated_dir = Path("skills/generated")
            generated_dir.mkdir(parents=True, exist_ok=True)

            # Dateiname
            filename = f"{project_name}_{skill_type}_skill.py"
            file_path = generated_dir / filename

            # Speichere Code
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(skill_code)

            return str(file_path)

        except Exception as e:
            logger.error(f"❌ Error saving skill file: {e}")
            raise

    def _get_skill_purpose(self, skill_type: str) -> str:
        """Gibt den Zweck des Skills zurück"""
        purposes = {
            "code_analysis": "Analysiert Code-Qualität und Komplexität",
            "performance_optimization": "Optimiert Performance und Ressourcennutzung",
            "security_audit": "Führt Security-Audits und Vulnerability-Scans durch",
            "test_generation": "Generiert automatisch Tests für Code",
            "documentation": "Generiert und aktualisiert Dokumentation",
            "refactoring": "Führt Code-Refactoring durch",
            "dependency_management": "Verwaltet und optimiert Dependencies",
            "api_optimization": "Optimiert API-Performance und Design",
        }
        return purposes.get(skill_type, "Allgemeine Projekt-Unterstützung")

    def _get_skill_inputs(self, skill_type: str) -> List[str]:
        """Gibt die Eingaben des Skills zurück"""
        inputs = {
            "code_analysis": ["file_path", "analysis_options"],
            "performance_optimization": ["code_files", "performance_metrics"],
            "security_audit": ["project_files", "security_rules"],
            "test_generation": ["source_code", "test_framework"],
            "documentation": ["code_files", "documentation_template"],
            "refactoring": ["source_code", "refactoring_rules"],
            "dependency_management": ["dependency_files", "update_policy"],
            "api_optimization": ["api_endpoints", "performance_requirements"],
        }
        return inputs.get(skill_type, ["project_files"])

    def _get_skill_outputs(self, skill_type: str) -> List[str]:
        """Gibt die Ausgaben des Skills zurück"""
        outputs = {
            "code_analysis": ["analysis_report", "complexity_metrics"],
            "performance_optimization": ["optimized_code", "performance_report"],
            "security_audit": ["security_report", "vulnerability_list"],
            "test_generation": ["test_files", "test_coverage"],
            "documentation": ["documentation_files", "api_docs"],
            "refactoring": ["refactored_code", "refactoring_report"],
            "dependency_management": ["updated_dependencies", "dependency_report"],
            "api_optimization": ["optimized_apis", "performance_metrics"],
        }
        return outputs.get(skill_type, ["output_report"])

    def _get_skill_dependencies(
        self, skill_type: str, analysis_results: Dict[str, Any]
    ) -> List[str]:
        """Gibt die Dependencies des Skills zurück"""
        base_deps = ["ast", "pathlib", "logging"]

        skill_specific_deps = {
            "code_analysis": ["radon", "lizard", "mccabe"],
            "performance_optimization": ["psutil", "memory_profiler"],
            "security_audit": ["safety", "bandit"],
            "test_generation": ["pytest", "unittest"],
            "documentation": ["sphinx", "mkdocs"],
            "refactoring": ["rope", "autopep8"],
            "dependency_management": ["pip", "pipenv"],
            "api_optimization": ["requests", "aiohttp"],
        }

        deps = base_deps + skill_specific_deps.get(skill_type, [])

        # Füge projektspezifische Dependencies hinzu
        frameworks = analysis_results.get("frameworks", {})
        for framework in frameworks.keys():
            if framework.lower() in ["fastapi", "django", "flask"]:
                deps.append(framework.lower())
            elif framework.lower() in ["react", "vue", "angular"]:
                deps.append("nodejs")

        return deps
