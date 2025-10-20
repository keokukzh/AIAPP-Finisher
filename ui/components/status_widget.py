"""
Kompakte System-Status-Anzeige
"""

import os
from typing import Any, Dict

import streamlit as st


class StatusWidget:
    """Kompakte System-Status-Anzeige für das linke Panel"""

    def __init__(self):
        pass

    def render(
        self, initialized: bool, current_project: str = None, workflow_state: Dict[str, Any] = None
    ):
        """Rendert das Status-Widget"""
        st.markdown('<div class="status-widget">', unsafe_allow_html=True)
        st.markdown("**System Status**")

        # System-Status
        if initialized:
            st.success("✅ System bereit")
        else:
            st.error("❌ System nicht initialisiert")

        # Projekt-Status
        if current_project:
            project_name = os.path.basename(current_project) if current_project else "Unbekannt"
            st.info(f"📁 Projekt: {project_name}")
        else:
            st.warning("⚠️ Kein Projekt ausgewählt")

        # Workflow-Status
        if workflow_state:
            workflow_status = workflow_state.get("status", "idle")
            if workflow_status == "idle":
                st.info("⏸️ Workflow bereit")
            elif workflow_status == "running":
                st.warning("⚙️ Workflow läuft...")
            elif workflow_status == "completed":
                st.success("✅ Workflow abgeschlossen")
            elif workflow_status == "error":
                st.error("❌ Workflow fehlerhaft")
        else:
            st.info("⏸️ Workflow bereit")

        # Zusätzliche Metriken
        if workflow_state and workflow_state.get("status") == "running":
            overall_progress = workflow_state.get("overall_progress", 0)
            st.metric("Fortschritt", f"{overall_progress}%")

            phases = workflow_state.get("phases", [])
            completed_phases = len([p for p in phases if p.get("status") == "completed"])
            total_phases = len(phases)
            if total_phases > 0:
                st.metric("Phasen", f"{completed_phases}/{total_phases}")

        st.markdown("</div>", unsafe_allow_html=True)
