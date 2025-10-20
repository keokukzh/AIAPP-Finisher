"""
Report Generator
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates comprehensive reports from analysis results"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_project_report(
        self,
        analysis_results: Dict[str, Any],
        agents: Dict[str, Any] = None,
        skills: Dict[str, Any] = None,
        workflows: Dict[str, Any] = None,
    ) -> str:
        """Generate comprehensive project report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"project_report_{timestamp}.md")

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(self._generate_markdown_report(analysis_results, agents, skills, workflows))

        logger.info(f"Generated project report: {report_file}")
        return report_file

    def _generate_markdown_report(
        self,
        analysis_results: Dict[str, Any],
        agents: Dict[str, Any] = None,
        skills: Dict[str, Any] = None,
        workflows: Dict[str, Any] = None,
    ) -> str:
        """Generate markdown report content"""

        report = f"""# KI-Projektmanagement Report

**Generiert am:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Projekt:** {analysis_results.get('project_name', 'Unbekannt')}
**Pfad:** {analysis_results.get('project_path', 'N/A')}

## 📊 Projekt-Analyse

### Grundlegende Informationen
- **Dateien:** {analysis_results.get('file_count', 0)}
- **Zeilen Code:** {analysis_results.get('total_lines', 0)}
- **Sprachen:** {', '.join(analysis_results.get('languages', {}).keys())}

### Erkannte Technologien
"""

        # Frameworks
        if analysis_results.get("frameworks"):
            report += "\n#### Frameworks\n"
            for framework, count in analysis_results["frameworks"].items():
                report += f"- **{framework}**: {count} Dateien\n"

        # Dependencies
        if analysis_results.get("dependencies"):
            report += "\n#### Abhängigkeiten\n"
            for lang, deps in analysis_results["dependencies"].items():
                report += f"\n**{lang.title()}:**\n"
                if isinstance(deps, dict) and "dependencies" in deps:
                    for dep in deps["dependencies"]:
                        report += f"- {dep}\n"

        # APIs
        if analysis_results.get("apis"):
            report += "\n#### API-Integrationen\n"
            for api in analysis_results["apis"]:
                report += f"- {api}\n"

        # Databases
        if analysis_results.get("databases"):
            report += "\n#### Datenbanken\n"
            for db in analysis_results["databases"]:
                report += f"- {db}\n"

        # Generated Agents
        if agents:
            report += "\n## 🤖 Generierte Agenten\n"
            for agent_name, agent_info in agents.items():
                report += f"\n### {agent_name}\n"
                if isinstance(agent_info, dict):
                    report += f"- **Rolle:** {agent_info.get('role', 'N/A')}\n"
                    report += f"- **Ziel:** {agent_info.get('goal', 'N/A')}\n"
                    report += f"- **Skills:** {', '.join(agent_info.get('skills', []))}\n"

        # Generated Skills
        if skills:
            report += "\n## 🛠️ Generierte Skills\n"
            for skill_name, skill_info in skills.items():
                report += f"\n### {skill_name}\n"
                if isinstance(skill_info, dict):
                    report += f"- **Zweck:** {skill_info.get('purpose', 'N/A')}\n"
                    report += f"- **Eingaben:** {skill_info.get('inputs', 'N/A')}\n"
                    report += f"- **Ausgaben:** {skill_info.get('outputs', 'N/A')}\n"

        # Generated Workflows
        if workflows:
            report += "\n## 🔄 Generierte Workflows\n"
            for workflow_name, workflow_info in workflows.items():
                report += f"\n### {workflow_name}\n"
                if isinstance(workflow_info, dict):
                    report += f"- **Zweck:** {workflow_info.get('purpose', 'N/A')}\n"
                    report += f"- **Schritte:** {len(workflow_info.get('steps', []))}\n"

        # Project Structure
        if analysis_results.get("structure"):
            report += "\n## 📁 Projektstruktur\n"
            report += "```\n"
            report += analysis_results["structure"]
            report += "\n```\n"

        # Recommendations
        report += "\n## 💡 Empfehlungen\n"
        report += """
### Nächste Schritte
1. **Code-Review:** Überprüfe die generierten Agenten und Skills
2. **Testing:** Führe die generierten Tests aus
3. **Optimierung:** Implementiere die vorgeschlagenen Verbesserungen
4. **Deployment:** Plane die Bereitstellung der Agenten

### Optimierungsmöglichkeiten
- Automatisierung von Routineaufgaben
- Verbesserung der Code-Qualität
- Erhöhung der Test-Abdeckung
- Performance-Optimierungen
"""

        return report

    def generate_json_report(
        self,
        analysis_results: Dict[str, Any],
        agents: Dict[str, Any] = None,
        skills: Dict[str, Any] = None,
        workflows: Dict[str, Any] = None,
    ) -> str:
        """Generate JSON report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"project_report_{timestamp}.json")

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_results,
            "agents": agents or {},
            "skills": skills or {},
            "workflows": workflows or {},
        }

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Generated JSON report: {report_file}")
        return report_file

    def generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate project summary"""
        return {
            "project_name": analysis_results.get("project_name", "Unbekannt"),
            "file_count": analysis_results.get("file_count", 0),
            "total_lines": analysis_results.get("total_lines", 0),
            "languages": list(analysis_results.get("languages", {}).keys()),
            "frameworks": list(analysis_results.get("frameworks", {}).keys()),
            "apis": analysis_results.get("apis", []),
            "databases": analysis_results.get("databases", []),
            "complexity_score": self._calculate_complexity_score(analysis_results),
        }

    def _calculate_complexity_score(self, analysis_results: Dict[str, Any]) -> int:
        """Calculate project complexity score"""
        score = 0

        # File count factor
        file_count = analysis_results.get("file_count", 0)
        score += min(file_count // 10, 20)

        # Language diversity factor
        languages = len(analysis_results.get("languages", {}))
        score += languages * 5

        # Framework complexity factor
        frameworks = len(analysis_results.get("frameworks", {}))
        score += frameworks * 3

        # API integrations factor
        apis = len(analysis_results.get("apis", []))
        score += apis * 2

        return min(score, 100)  # Cap at 100
