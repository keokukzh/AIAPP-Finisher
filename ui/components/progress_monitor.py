"""
Live-Fortschrittsanzeige mit animierten Tasks
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import streamlit as st


class ProgressMonitor:
    """Animierte Task-Liste für Workflow-Tracking"""

    def __init__(self):
        self.phase_icons = {
            "analyze": "🔍",
            "generate_agents": "🤖",
            "generate_skills": "🛠️",
            "generate_workflows": "🔄",
            "optimization": "⚡",
            "generate_tests": "🧪",
            "create_reports": "📋",
            "create_artifacts": "📁",
        }

    def render(self, workflow_state: Dict[str, Any]):
        """Rendert die Live-Fortschrittsanzeige"""

        if not workflow_state or workflow_state.get("status") == "idle":
            self.render_idle_state()
            return

        # Header mit Gesamt-Fortschritt
        self.render_progress_header(workflow_state)

        # Phasen-Liste mit Animationen
        self.render_phases_list(workflow_state)

        # ETA und Details
        self.render_eta_and_details(workflow_state)

    def render_idle_state(self):
        """Rendert den Idle-Zustand"""
        st.markdown("### 📊 Fortschritt")

        # Placeholder mit Animation
        placeholder_html = """
        <div style="text-align: center; padding: 2rem; color: #666;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⏳</div>
            <h3>Bereit für Analyse</h3>
            <p>Wähle ein Projekt aus und starte eine Analyse</p>
        </div>
        """
        st.markdown(placeholder_html, unsafe_allow_html=True)

    def render_progress_header(self, workflow_state: Dict[str, Any]):
        """Rendert den Fortschritts-Header"""
        overall_progress = workflow_state.get("overall_progress", 0)
        status = workflow_state.get("status", "idle")
        current_phase = workflow_state.get("current_phase", "")

        # Gesamt-Fortschritt
        st.markdown("### 📊 Fortschritt")

        # Progress Bar mit Animation
        progress_bar = st.progress(overall_progress / 100)

        # Status-Info
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.metric("Gesamtfortschritt", f"{overall_progress}%")

        with col2:
            if status == "running":
                st.metric("Status", "⚙️ Läuft", delta="Aktiv")
            elif status == "completed":
                st.metric("Status", "✅ Fertig", delta="Abgeschlossen")
            elif status == "error":
                st.metric("Status", "❌ Fehler", delta="Gestoppt")
            else:
                st.metric("Status", "⏸️ Bereit")

        with col3:
            if current_phase:
                st.metric("Aktuelle Phase", current_phase)

    def render_phases_list(self, workflow_state: Dict[str, Any]):
        """Rendert die animierte Phasen-Liste"""
        phases = workflow_state.get("phases", [])

        if not phases:
            return

        st.markdown("#### 📋 Workflow-Phasen")

        for i, phase in enumerate(phases):
            self.render_phase_item(phase, i)

    def render_phase_item(self, phase: Dict[str, Any], index: int):
        """Rendert eine einzelne Phase mit Animation und Details"""
        name = phase.get("name", "Unbekannt")
        status = phase.get("status", "pending")
        progress = phase.get("progress", 0)
        start_time = phase.get("start_time")
        end_time = phase.get("end_time")
        details = phase.get("details", {})

        # Phase-Icon basierend auf Name
        icon = self.get_phase_icon(name)

        # Status-Icon und CSS-Klasse
        if status == "completed":
            status_icon = "✅"
            css_class = "phase-completed"
            progress_text = "Abgeschlossen"
        elif status == "running":
            status_icon = "⚙️"
            css_class = "phase-running"
            progress_text = f"Läuft... ({progress}%)"
        elif status == "error":
            status_icon = "❌"
            css_class = "phase-error"
            progress_text = "Fehler"
        else:
            status_icon = "⏳"
            css_class = "phase-pending"
            progress_text = "Wartet"

        # Live-Details für laufende Phasen
        live_details = self.render_live_details(details, status)

        # Phase-Container
        phase_html = f"""
        <div class="phase-item {css_class}" style="margin: 0.5rem 0;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
                    <div>
                        <strong>{name}</strong>
                        <div style="font-size: 0.9rem; color: #666;">{progress_text}</div>
                        {live_details}
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 1.2rem;">{status_icon}</span>
                    {self.render_phase_timing(start_time, end_time, status)}
                </div>
            </div>
            {self.render_phase_progress_bar(progress, status)}
        </div>
        """

        st.markdown(phase_html, unsafe_allow_html=True)

    def render_live_details(self, details: Dict[str, Any], status: str) -> str:
        """Rendert Live-Details für laufende Phasen"""
        if status != "running" or not details:
            return ""

        detail_parts = []

        # Aktuelle Datei
        if "current_file" in details:
            current_file = details["current_file"]
            if len(current_file) > 50:
                current_file = "..." + current_file[-47:]
            detail_parts.append(f"📁 {current_file}")

        # Datei-Fortschritt
        if "files_analyzed" in details and "total_files" in details:
            files_analyzed = details["files_analyzed"]
            total_files = details["total_files"]
            detail_parts.append(f"📊 {files_analyzed}/{total_files} Dateien")

        # Aktuelle Aktion
        if "current_action" in details:
            action = details["current_action"]
            detail_parts.append(f"⚡ {action}")

        if detail_parts:
            return f"""
            <div style="font-size: 0.8rem; color: #888; margin-top: 0.2rem;">
                {' • '.join(detail_parts)}
            </div>
            """

        return ""

    def render_phase_progress_bar(self, progress: int, status: str):
        """Rendert eine Mini-Progress-Bar für die Phase"""
        if status == "pending":
            return ""

        color = (
            "#4caf50" if status == "completed" else "#ff9800" if status == "running" else "#f44336"
        )

        return f"""
        <div style="margin-top: 0.5rem;">
            <div style="background-color: #e0e0e0; border-radius: 10px; height: 6px; overflow: hidden;">
                <div style="background-color: {color}; height: 100%; width: {progress}%; transition: width 0.5s ease;"></div>
            </div>
        </div>
        """

    def render_phase_timing(self, start_time: str, end_time: str, status: str):
        """Rendert Timing-Informationen für die Phase"""
        if not start_time:
            return ""

        try:
            start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))

            if end_time:
                end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                duration = end - start
                return f"<div style='font-size: 0.8rem; color: #666;'>{duration.total_seconds():.1f}s</div>"
            elif status == "running":
                duration = datetime.now() - start
                return f"<div style='font-size: 0.8rem; color: #666;'>{duration.total_seconds():.1f}s</div>"
        except:
            pass

        return ""

    def render_eta_and_details(self, workflow_state: Dict[str, Any]):
        """Rendert ETA und erweiterte Details"""
        status = workflow_state.get("status", "idle")

        if status != "running":
            return

        # ETA-Berechnung
        phases = workflow_state.get("phases", [])
        completed_phases = [p for p in phases if p.get("status") == "completed"]
        running_phases = [p for p in phases if p.get("status") == "running"]
        pending_phases = [p for p in phases if p.get("status") == "pending"]

        if completed_phases and running_phases:
            # Schätze ETA basierend auf bisheriger Performance
            try:
                total_time = sum(
                    [
                        (
                            datetime.fromisoformat(p.get("end_time", "").replace("Z", "+00:00"))
                            - datetime.fromisoformat(p.get("start_time", "").replace("Z", "+00:00"))
                        ).total_seconds()
                        for p in completed_phases
                        if p.get("start_time") and p.get("end_time")
                    ]
                )

                avg_time_per_phase = total_time / len(completed_phases) if completed_phases else 30
                estimated_remaining = avg_time_per_phase * len(pending_phases)

                eta = datetime.now() + timedelta(seconds=estimated_remaining)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Geschätzte Restzeit", f"{estimated_remaining/60:.1f} Min")
                with col2:
                    st.metric("Geschätzte Fertigstellung", eta.strftime("%H:%M:%S"))
            except:
                pass

        # Erweiterte Details
        with st.expander("🔍 Erweiterte Details", expanded=False):
            st.json(workflow_state)

    def get_phase_icon(self, phase_name: str) -> str:
        """Gibt das passende Icon für eine Phase zurück"""
        phase_lower = phase_name.lower()

        for key, icon in self.phase_icons.items():
            if key in phase_lower:
                return icon

        # Fallback-Icons basierend auf Keywords
        if "analyse" in phase_lower or "analyze" in phase_lower:
            return "🔍"
        elif "agent" in phase_lower:
            return "🤖"
        elif "skill" in phase_lower:
            return "🛠️"
        elif "workflow" in phase_lower:
            return "🔄"
        elif "optim" in phase_lower:
            return "⚡"
        elif "test" in phase_lower:
            return "🧪"
        elif "report" in phase_lower:
            return "📋"
        elif "artifact" in phase_lower:
            return "📁"
        else:
            return "📝"
