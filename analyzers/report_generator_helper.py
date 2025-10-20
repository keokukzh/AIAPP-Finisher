"""
Report Generator Helper - Generates analysis reports
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ReportGeneratorHelper:
    """Generates markdown and JSON analysis reports"""

    async def generate_reports(self, project_path: str, analysis_results: Dict[str, Any]):
        """Generiert Analyse-Berichte"""
        try:
            # Erstelle Output-Ordner
            output_dir = Path(project_path).parent / "analysis_output"
            output_dir.mkdir(exist_ok=True)

            # JSON-Report
            json_report_path = output_dir / "project_analysis.json"
            await self._generate_json_report(json_report_path, analysis_results)

            # Markdown-Report
            md_report_path = output_dir / "PROJECT_ANALYSIS.md"
            await self._generate_markdown_report(md_report_path, analysis_results)

            logger.info(f"Berichte generiert in: {output_dir}")

        except Exception as e:
            logger.error(f"Fehler beim Generieren der Berichte: {e}")

    async def _generate_json_report(self, report_path: Path, analysis_results: Dict[str, Any]):
        """Generiert JSON-Bericht"""
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Fehler beim Generieren des JSON-Berichts: {e}")

    async def _generate_markdown_report(self, report_path: Path, analysis_results: Dict[str, Any]):
        """Generiert einen Markdown-Bericht"""
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# Projekt-Analyse: {analysis_results['project_name']}\n\n")
                f.write(f"**Analyse-Datum:** {analysis_results['analysis_date']}\n\n")

                # Übersicht
                f.write("## 📊 Übersicht\n\n")
                f.write(f"- **Dateien:** {analysis_results.get('file_count', 0)}\n")
                f.write(f"- **Zeilen Code:** {analysis_results.get('lines_of_code', 0):,}\n")
                f.write(f"- **Dependencies:** {analysis_results.get('dependency_count', 0)}\n")
                f.write(f"- **Frameworks:** {len(analysis_results.get('frameworks', []))}\n\n")

                # Sprachen
                languages = analysis_results.get("languages", [])
                if languages:
                    f.write("## 🌐 Programmiersprachen\n\n")
                    for lang in languages:
                        f.write(f"- {lang}\n")
                    f.write("\n")

                # Frameworks
                frameworks = analysis_results.get("frameworks", [])
                if frameworks:
                    f.write("## 🛠️ Frameworks & Libraries\n\n")
                    for framework in frameworks:
                        f.write(
                            f"- **{framework.get('name', 'Unknown')}** ({framework.get('type', 'Unknown')})\n"
                        )
                    f.write("\n")

                # Security-Issues
                security_issues = analysis_results.get("security_issues", [])
                if security_issues:
                    f.write("## 🔒 Security-Issues\n\n")
                    for issue in security_issues:
                        f.write(
                            f"- **{issue.get('severity', 'unknown').upper()}:** {issue.get('message', 'Unknown')}\n"
                        )
                    f.write("\n")
                else:
                    f.write("## 🔒 Security\n\n✅ Keine kritischen Security-Issues gefunden\n\n")

                # Test-Coverage
                test_coverage = analysis_results.get("test_coverage", {})
                if test_coverage:
                    f.write("## 🧪 Test-Coverage\n\n")
                    f.write(f"- **Coverage:** {test_coverage.get('coverage_percentage', 0):.1f}%\n")
                    f.write(
                        f"- **Test-Frameworks:** {', '.join(test_coverage.get('test_frameworks', []))}\n"
                    )
                    f.write(f"- **Test-Dateien:** {len(test_coverage.get('test_files', []))}\n\n")

        except Exception as e:
            logger.error(f"Fehler beim Generieren des Markdown-Berichts: {e}")
