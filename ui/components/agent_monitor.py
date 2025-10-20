"""
Agent-Monitor-Komponente
"""

import random
import time
from datetime import datetime
from typing import Any, Dict, List

import streamlit as st


class AgentMonitor:
    """Komponente für das Agent-Monitoring"""

    def __init__(self):
        self.agents = []
        self.tasks = []
        self.initialize_demo_data()

    def initialize_demo_data(self):
        """Initialisiert Demo-Daten für die Agenten"""
        self.agents = [
            {
                "id": "project_manager",
                "name": "KI-Projektmanager",
                "type": "Project Manager",
                "status": "active",
                "cpu_usage": 15.2,
                "memory_usage": 128.5,
                "tasks_completed": 45,
                "current_task": "Projekt-Analyse koordinieren",
                "last_activity": datetime.now().isoformat(),
            },
            {
                "id": "code_analyzer",
                "name": "Code-Analyzer",
                "type": "Analyzer",
                "status": "active",
                "cpu_usage": 35.8,
                "memory_usage": 256.3,
                "tasks_completed": 23,
                "current_task": "Python-Code analysieren",
                "last_activity": datetime.now().isoformat(),
            },
            {
                "id": "security_scanner",
                "name": "Security-Scanner",
                "type": "Security",
                "status": "idle",
                "cpu_usage": 2.1,
                "memory_usage": 64.2,
                "tasks_completed": 12,
                "current_task": "Wartet auf neue Tasks",
                "last_activity": datetime.now().isoformat(),
            },
            {
                "id": "test_generator",
                "name": "Test-Generator",
                "type": "Testing",
                "status": "active",
                "cpu_usage": 28.4,
                "memory_usage": 192.7,
                "tasks_completed": 8,
                "current_task": "Unit-Tests generieren",
                "last_activity": datetime.now().isoformat(),
            },
            {
                "id": "optimizer",
                "name": "Code-Optimizer",
                "type": "Optimizer",
                "status": "error",
                "cpu_usage": 0.0,
                "memory_usage": 32.1,
                "tasks_completed": 5,
                "current_task": "Fehler beim Optimieren",
                "last_activity": datetime.now().isoformat(),
            },
        ]

        self.tasks = [
            {
                "id": "task_001",
                "name": "Projekt-Analyse",
                "agent": "code_analyzer",
                "status": "running",
                "progress": 75,
                "started_at": datetime.now().isoformat(),
                "estimated_completion": "2 min",
            },
            {
                "id": "task_002",
                "name": "Security-Scan",
                "agent": "security_scanner",
                "status": "pending",
                "progress": 0,
                "started_at": None,
                "estimated_completion": "5 min",
            },
            {
                "id": "task_003",
                "name": "Test-Generierung",
                "agent": "test_generator",
                "status": "running",
                "progress": 45,
                "started_at": datetime.now().isoformat(),
                "estimated_completion": "3 min",
            },
            {
                "id": "task_004",
                "name": "Performance-Optimierung",
                "agent": "optimizer",
                "status": "failed",
                "progress": 20,
                "started_at": datetime.now().isoformat(),
                "estimated_completion": "N/A",
            },
        ]

    def render(self):
        """Rendert den Agent-Monitor"""
        st.markdown("## 🤖 Agent-Monitor")

        # Auto-Refresh
        auto_refresh = st.checkbox("🔄 Auto-Refresh", value=True)
        if auto_refresh:
            time.sleep(1)
            st.rerun()

        # Übersicht
        self.render_overview()

        # Agent-Status
        self.render_agent_status()

        # Task-Queue
        self.render_task_queue()

        # Performance-Metriken
        self.render_performance_metrics()

        # Agent-Details
        self.render_agent_details()

    def render_overview(self):
        """Rendert die Agent-Übersicht"""
        st.markdown("### 📊 Agent-Übersicht")

        # Statistiken
        total_agents = len(self.agents)
        active_agents = len([agent for agent in self.agents if agent["status"] == "active"])
        idle_agents = len([agent for agent in self.agents if agent["status"] == "idle"])
        error_agents = len([agent for agent in self.agents if agent["status"] == "error"])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="🤖 Gesamt", value=total_agents, delta=None)

        with col2:
            st.metric(label="🟢 Aktiv", value=active_agents, delta=None)

        with col3:
            st.metric(label="⚪ Idle", value=idle_agents, delta=None)

        with col4:
            st.metric(label="🔴 Fehler", value=error_agents, delta=None)

        # Task-Statistiken
        total_tasks = len(self.tasks)
        running_tasks = len([task for task in self.tasks if task["status"] == "running"])
        pending_tasks = len([task for task in self.tasks if task["status"] == "pending"])
        completed_tasks = len([task for task in self.tasks if task["status"] == "completed"])
        failed_tasks = len([task for task in self.tasks if task["status"] == "failed"])

        st.markdown("#### 📋 Task-Statistiken")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(label="📋 Gesamt", value=total_tasks, delta=None)

        with col2:
            st.metric(label="🔄 Laufend", value=running_tasks, delta=None)

        with col3:
            st.metric(label="⏳ Wartend", value=pending_tasks, delta=None)

        with col4:
            st.metric(label="✅ Abgeschlossen", value=completed_tasks, delta=None)

        with col5:
            st.metric(label="❌ Fehlgeschlagen", value=failed_tasks, delta=None)

    def render_agent_status(self):
        """Rendert den Agent-Status"""
        st.markdown("### 🤖 Agent-Status")

        # Agent-Karten
        for agent in self.agents:
            self.render_agent_card(agent)

    def render_agent_card(self, agent: Dict[str, Any]):
        """Rendert eine Agent-Karte"""
        status = agent["status"]
        name = agent["name"]
        agent_type = agent["type"]
        cpu_usage = agent["cpu_usage"]
        memory_usage = agent["memory_usage"]
        current_task = agent["current_task"]

        # Status-Farben
        status_colors = {"active": "#48dbf5", "idle": "#95a5a6", "error": "#ff6b6b"}
        status_color = status_colors.get(status, "#95a5a6")

        # Status-Icons
        status_icons = {"active": "🟢", "idle": "⚪", "error": "🔴"}
        status_icon = status_icons.get(status, "⚪")

        with st.expander(f"{status_icon} {name} ({agent_type})", expanded=status == "error"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Status:** {status_icon} {status.title()}")
                st.markdown(f"**Typ:** {agent_type}")
                st.markdown(f"**Aktuelle Aufgabe:** {current_task}")

            with col2:
                st.markdown(f"**CPU:** {cpu_usage}%")
                st.markdown(f"**Speicher:** {memory_usage} MB")
                st.markdown(f"**Tasks abgeschlossen:** {agent['tasks_completed']}")

            # Performance-Balken
            st.markdown("**Performance:**")
            col1, col2 = st.columns(2)

            with col1:
                st.progress(cpu_usage / 100)
                st.markdown(f"CPU: {cpu_usage}%")

            with col2:
                st.progress(memory_usage / 512)  # Annahme: 512 MB max
                st.markdown(f"Speicher: {memory_usage} MB")

            # Aktionen
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"🔄 Neustart", key=f"restart_{agent['id']}"):
                    st.success(f"Agent {name} wird neugestartet...")

            with col2:
                if st.button(f"⏸️ Pausieren", key=f"pause_{agent['id']}"):
                    st.info(f"Agent {name} wird pausiert...")

            with col3:
                if st.button(f"📊 Details", key=f"details_{agent['id']}"):
                    self.show_agent_details(agent)

    def render_task_queue(self):
        """Rendert die Task-Queue"""
        st.markdown("### 📋 Task-Queue")

        # Task-Filter
        col1, col2 = st.columns(2)

        with col1:
            status_filter = st.selectbox(
                "Status filtern:", ["Alle", "Running", "Pending", "Completed", "Failed"]
            )

        with col2:
            agent_filter = st.selectbox(
                "Agent filtern:", ["Alle"] + [agent["name"] for agent in self.agents]
            )

        # Gefilterte Tasks
        filtered_tasks = self.filter_tasks(status_filter, agent_filter)

        # Task-Liste
        for task in filtered_tasks:
            self.render_task_card(task)

    def render_task_card(self, task: Dict[str, Any]):
        """Rendert eine Task-Karte"""
        status = task["status"]
        name = task["name"]
        agent = task["agent"]
        progress = task["progress"]

        # Status-Farben
        status_colors = {
            "running": "#48dbf5",
            "pending": "#feca57",
            "completed": "#48dbf5",
            "failed": "#ff6b6b",
        }
        status_color = status_colors.get(status, "#95a5a6")

        # Status-Icons
        status_icons = {"running": "🔄", "pending": "⏳", "completed": "✅", "failed": "❌"}
        status_icon = status_icons.get(status, "⚪")

        with st.expander(f"{status_icon} {name}", expanded=status == "failed"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Status:** {status_icon} {status.title()}")
                st.markdown(f"**Agent:** {agent}")
                st.markdown(f"**Geschätzte Zeit:** {task['estimated_completion']}")

            with col2:
                st.markdown(f"**Fortschritt:** {progress}%")
                st.progress(progress / 100)

                if task["started_at"]:
                    st.markdown(f"**Gestartet:** {task['started_at']}")

            # Aktionen
            if status == "pending":
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"▶️ Starten", key=f"start_{task['id']}"):
                        st.success(f"Task {name} wird gestartet...")

                with col2:
                    if st.button(f"❌ Abbrechen", key=f"cancel_{task['id']}"):
                        st.warning(f"Task {name} wird abgebrochen...")

            elif status == "failed":
                if st.button(f"🔄 Wiederholen", key=f"retry_{task['id']}"):
                    st.info(f"Task {name} wird wiederholt...")

    def render_performance_metrics(self):
        """Rendert die Performance-Metriken"""
        st.markdown("### 📊 Performance-Metriken")

        # System-Metriken
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_cpu = sum(agent["cpu_usage"] for agent in self.agents)
            st.metric(label="💻 Gesamt-CPU", value=f"{total_cpu:.1f}%", delta=None)

        with col2:
            total_memory = sum(agent["memory_usage"] for agent in self.agents)
            st.metric(label="🧠 Gesamt-Speicher", value=f"{total_memory:.1f} MB", delta=None)

        with col3:
            total_tasks = sum(agent["tasks_completed"] for agent in self.agents)
            st.metric(label="✅ Tasks abgeschlossen", value=total_tasks, delta="+3")

        with col4:
            # Simuliere Durchsatz
            throughput = random.uniform(10, 50)
            st.metric(label="⚡ Durchsatz", value=f"{throughput:.1f} tasks/min", delta="+2.3")

        # Performance-Graph (simuliert)
        st.markdown("#### 📈 Performance-Verlauf")

        # Simuliere Performance-Daten
        import numpy as np
        import pandas as pd

        # Erstelle Zeitreihe
        timestamps = pd.date_range(start="2024-01-01", periods=24, freq="H")
        cpu_data = np.random.normal(30, 10, 24)
        memory_data = np.random.normal(200, 50, 24)

        df = pd.DataFrame({"Zeit": timestamps, "CPU (%)": cpu_data, "Speicher (MB)": memory_data})

        st.line_chart(df.set_index("Zeit"))

    def render_agent_details(self):
        """Rendert die Agent-Details"""
        st.markdown("### 🔍 Agent-Details")

        # Agent-Auswahl
        selected_agent = st.selectbox("Agent auswählen:", [agent["name"] for agent in self.agents])

        # Finde ausgewählten Agent
        agent = next((a for a in self.agents if a["name"] == selected_agent), None)

        if agent:
            self.show_agent_details(agent)

    def show_agent_details(self, agent: Dict[str, Any]):
        """Zeigt detaillierte Agent-Informationen"""
        st.markdown(f"#### 🤖 {agent['name']}")

        # Vollständige Agent-Informationen
        st.json(agent)

        # Logs (simuliert)
        st.markdown("#### 📝 Agent-Logs")

        # Simuliere Logs
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Agent gestartet",
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Task 'Projekt-Analyse' übernommen",
            f"[{datetime.now().strftime('%H:%M:%S')}] DEBUG: Code-Scan gestartet",
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: 150 Dateien analysiert",
            f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: Langsame Query erkannt",
            f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Task abgeschlossen",
        ]

        for log in logs:
            st.text(log)

    def filter_tasks(self, status_filter: str, agent_filter: str) -> List[Dict[str, Any]]:
        """Filtert Tasks nach Status und Agent"""
        filtered = self.tasks.copy()

        if status_filter != "Alle":
            status_map = {
                "Running": "running",
                "Pending": "pending",
                "Completed": "completed",
                "Failed": "failed",
            }
            target_status = status_map.get(status_filter, "running")
            filtered = [task for task in filtered if task["status"] == target_status]

        if agent_filter != "Alle":
            filtered = [task for task in filtered if task["agent"] == agent_filter]

        return filtered
