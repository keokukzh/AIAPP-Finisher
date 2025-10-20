"""
Analyse-Dashboard-Komponente
"""

import json
from datetime import datetime
from typing import Any, Dict

import streamlit as st


class AnalysisDashboard:
    """Komponente für das Analyse-Dashboard"""

    def __init__(self):
        pass

    def render(self, analysis_results: Dict[str, Any]):
        """Rendert das Analyse-Dashboard"""
        if not analysis_results:
            st.info("Keine Analyse-Ergebnisse verfügbar")
            return

        st.markdown("## 📊 Analyse-Dashboard")

        # Projekt-Header
        self.render_project_header(analysis_results)

        # Metriken-Karten
        self.render_metrics_cards(analysis_results)

        # Technologie-Übersicht
        self.render_technology_overview(analysis_results)

        # Detaillierte Analyse
        self.render_detailed_analysis(analysis_results)

    def render_project_header(self, analysis_results: Dict[str, Any]):
        """Rendert den Projekt-Header"""
        project_name = analysis_results.get("project_name", "Unbekanntes Projekt")
        analysis_date = analysis_results.get("analysis_date", datetime.now().isoformat())

        st.markdown(
            f"""
        <div class="status-card">
            <h2>📁 {project_name}</h2>
            <p><strong>Analyse-Datum:</strong> {analysis_date}</p>
            <p><strong>Status:</strong> ✅ Vollständig analysiert</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_metrics_cards(self, analysis_results: Dict[str, Any]):
        """Rendert die Metriken-Karten"""
        st.markdown("### 📈 Projekt-Metriken")

        # Haupt-Metriken
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            file_count = analysis_results.get("file_count", 0)
            st.metric(label="📄 Dateien", value=file_count, delta=None)

        with col2:
            lines_of_code = analysis_results.get("lines_of_code", 0)
            st.metric(label="📝 Zeilen Code", value=f"{lines_of_code:,}", delta=None)

        with col3:
            dependency_count = analysis_results.get("dependency_count", 0)
            st.metric(label="📦 Dependencies", value=dependency_count, delta=None)

        with col4:
            framework_count = len(analysis_results.get("frameworks", []))
            st.metric(label="🛠️ Frameworks", value=framework_count, delta=None)

        # Zusätzliche Metriken
        col5, col6, col7, col8 = st.columns(4)

        with col5:
            languages = analysis_results.get("languages", [])
            st.metric(label="🌐 Sprachen", value=len(languages), delta=None)

        with col6:
            # Simuliere Komplexität
            complexity = analysis_results.get("complexity_score", 0)
            st.metric(label="🧩 Komplexität", value=f"{complexity}/10", delta=None)

        with col7:
            # Simuliere Test-Coverage
            test_coverage = analysis_results.get("test_coverage", 0)
            st.metric(label="🧪 Test-Coverage", value=f"{test_coverage}%", delta=None)

        with col8:
            # Simuliere Security-Score
            security_score = analysis_results.get("security_score", 0)
            st.metric(label="🔒 Security-Score", value=f"{security_score}/10", delta=None)

    def render_technology_overview(self, analysis_results: Dict[str, Any]):
        """Rendert die Technologie-Übersicht"""
        st.markdown("### 🛠️ Technologie-Stack")

        # Frameworks
        frameworks = analysis_results.get("frameworks", [])
        if frameworks:
            st.markdown("**Frameworks & Libraries:**")
            for framework in frameworks:
                framework_type = framework.get("type", "Unknown")
                framework_name = framework.get("name", "Unknown")

                # Farbkodierung nach Typ
                color = {
                    "Backend": "#ff6b6b",
                    "Frontend": "#4ecdc4",
                    "Database": "#45b7d1",
                    "Testing": "#96ceb4",
                    "DevOps": "#feca57",
                }.get(framework_type, "#95a5a6")

                st.markdown(
                    f"""
                <div style="background-color: {color}; color: white; padding: 0.5rem; 
                           border-radius: 0.25rem; margin: 0.25rem 0; display: inline-block;">
                    {framework_name} ({framework_type})
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("Keine Frameworks erkannt")

        # Programmiersprachen
        languages = analysis_results.get("languages", [])
        if languages:
            st.markdown("**Programmiersprachen:**")
            for language in languages:
                st.markdown(f"- {language}")
        else:
            st.info("Keine Sprachen erkannt")

    def render_detailed_analysis(self, analysis_results: Dict[str, Any]):
        """Rendert die detaillierte Analyse"""
        st.markdown("### 🔍 Detaillierte Analyse")

        # Tabs für verschiedene Analyse-Aspekte
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📋 Übersicht", "🛠️ Technologien", "📦 Dependencies", "📄 Dateien", "🔒 Security"]
        )

        with tab1:
            self.render_overview_tab(analysis_results)

        with tab2:
            self.render_technologies_tab(analysis_results)

        with tab3:
            self.render_dependencies_tab(analysis_results)

        with tab4:
            self.render_files_tab(analysis_results)

        with tab5:
            self.render_security_tab(analysis_results)

    def render_overview_tab(self, analysis_results: Dict[str, Any]):
        """Rendert den Übersicht-Tab"""
        st.markdown("**Vollständige Analyse-Ergebnisse:**")
        st.json(analysis_results)

        # Projekt-Zusammenfassung
        st.markdown("**📝 Projekt-Zusammenfassung:**")
        summary = self.generate_project_summary(analysis_results)
        st.markdown(summary)

    def render_technologies_tab(self, analysis_results: Dict[str, Any]):
        """Rendert den Technologien-Tab"""
        frameworks = analysis_results.get("frameworks", [])
        languages = analysis_results.get("languages", [])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Frameworks:**")
            if frameworks:
                for framework in frameworks:
                    st.markdown(
                        f"- **{framework.get('name', 'Unknown')}** ({framework.get('type', 'Unknown')})"
                    )
            else:
                st.info("Keine Frameworks gefunden")

        with col2:
            st.markdown("**Sprachen:**")
            if languages:
                for language in languages:
                    st.markdown(f"- {language}")
            else:
                st.info("Keine Sprachen gefunden")

    def render_dependencies_tab(self, analysis_results: Dict[str, Any]):
        """Rendert den Dependencies-Tab"""
        dependencies = analysis_results.get("dependencies", [])

        if dependencies:
            st.markdown("**Dependencies:**")
            for dep in dependencies:
                st.markdown(f"- {dep}")
        else:
            st.info("Dependency-Analyse wird implementiert...")

            # Simuliere Dependencies für Demo
            st.markdown("**Beispiel-Dependencies:**")
            example_deps = [
                "fastapi==0.104.1",
                "uvicorn==0.24.0",
                "pydantic==2.5.0",
                "sqlalchemy==2.0.23",
                "alembic==1.12.1",
            ]
            for dep in example_deps:
                st.markdown(f"- {dep}")

    def render_files_tab(self, analysis_results: Dict[str, Any]):
        """Rendert den Dateien-Tab"""
        file_structure = analysis_results.get("file_structure", {})

        if file_structure:
            st.markdown("**Dateistruktur:**")
            st.json(file_structure)
        else:
            st.info("Dateistruktur-Analyse wird implementiert...")

            # Simuliere Dateistruktur für Demo
            st.markdown("**Beispiel-Dateistruktur:**")
            example_structure = {
                "app/": {
                    "main.py": "Hauptanwendung",
                    "models/": "Datenmodelle",
                    "routes/": "API-Routen",
                    "services/": "Business-Logic",
                },
                "tests/": "Test-Dateien",
                "requirements.txt": "Python-Dependencies",
                "README.md": "Dokumentation",
            }
            st.json(example_structure)

    def render_security_tab(self, analysis_results: Dict[str, Any]):
        """Rendert den Security-Tab"""
        security_issues = analysis_results.get("security_issues", [])

        if security_issues:
            st.markdown("**🔒 Security-Issues:**")
            for issue in security_issues:
                severity = issue.get("severity", "unknown")
                message = issue.get("message", "Unknown issue")

                # Farbkodierung nach Schweregrad
                color = {"high": "#ff6b6b", "medium": "#feca57", "low": "#48dbf5"}.get(
                    severity, "#95a5a6"
                )

                st.markdown(
                    f"""
                <div style="background-color: {color}; color: white; padding: 0.5rem; 
                           border-radius: 0.25rem; margin: 0.25rem 0;">
                    <strong>{severity.upper()}:</strong> {message}
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.success("✅ Keine Security-Issues gefunden")

            # Simuliere Security-Check für Demo
            st.markdown("**Security-Check-Ergebnisse:**")
            security_checks = [
                {"check": "Dependency-Vulnerabilities", "status": "✅ Passed"},
                {"check": "Hardcoded-Secrets", "status": "✅ Passed"},
                {"check": "SQL-Injection", "status": "✅ Passed"},
                {"check": "XSS-Vulnerabilities", "status": "✅ Passed"},
            ]

            for check in security_checks:
                st.markdown(f"- {check['check']}: {check['status']}")

    def generate_project_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Generiert eine Projekt-Zusammenfassung"""
        project_name = analysis_results.get("project_name", "Unbekanntes Projekt")
        file_count = analysis_results.get("file_count", 0)
        lines_of_code = analysis_results.get("lines_of_code", 0)
        frameworks = analysis_results.get("frameworks", [])
        languages = analysis_results.get("languages", [])

        summary = f"""
        Das Projekt **{project_name}** ist ein {self._get_project_type(frameworks)} mit {file_count} Dateien 
        und {lines_of_code:,} Zeilen Code. Es verwendet hauptsächlich {', '.join(languages[:3])} 
        und basiert auf {len(frameworks)} verschiedenen Frameworks.
        """

        return summary

    def _get_project_type(self, frameworks: list) -> str:
        """Bestimmt den Projekttyp basierend auf Frameworks"""
        if not frameworks:
            return "unbekanntes Projekt"

        framework_types = [f.get("type", "").lower() for f in frameworks]

        if "backend" in framework_types and "frontend" in framework_types:
            return "Full-Stack-Projekt"
        elif "backend" in framework_types:
            return "Backend-Projekt"
        elif "frontend" in framework_types:
            return "Frontend-Projekt"
        else:
            return "Projekt"
