"""
Moderne Drag & Drop Projektauswahl-Komponente
"""

import os
import time
from pathlib import Path
from typing import Optional

import streamlit as st


class ModernProjectSelector:
    """Moderne Projektauswahl mit Drag & Drop Zone"""

    def __init__(self):
        self.selected_path = None

    def render(self) -> Optional[str]:
        """Rendert die moderne Projekt-Auswahl-Komponente"""

        # Drag & Drop Zone
        self.render_drag_drop_zone()

        # Alternative: Pfad-Eingabe
        st.markdown("**oder**")
        self.render_path_input()

        # Quick-Select Buttons
        self.render_quick_select()

        return self.selected_path

    def render_drag_drop_zone(self):
        """Rendert die Drag & Drop Zone"""
        st.markdown("### 📁 Projekt auswählen")

        # Drag & Drop Zone HTML
        drag_drop_html = """
        <div class="drag-drop-zone" id="dragDropZone">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
            <h3>Projektordner hier ablegen</h3>
            <p>Ziehe deinen Projektordner in diese Zone</p>
            <p style="color: #666; font-size: 0.9rem;">oder klicke zum Durchsuchen</p>
        </div>
        
        <script>
        const dragDropZone = document.getElementById('dragDropZone');
        
        // Drag & Drop Event Listeners
        dragDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dragDropZone.style.backgroundColor = '#e3f2fd';
            dragDropZone.style.borderColor = '#0d47a1';
        });
        
        dragDropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dragDropZone.style.backgroundColor = '#f8f9fa';
            dragDropZone.style.borderColor = '#1f77b4';
        });
        
        dragDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dragDropZone.style.backgroundColor = '#c8e6c9';
            dragDropZone.style.borderColor = '#4caf50';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                // In einer echten Implementierung würde hier der Pfad verarbeitet werden
                console.log('Dropped file:', files[0].name);
                // Streamlit Session State Update würde hier erfolgen
            }
        });
        
        // Click to browse
        dragDropZone.addEventListener('click', () => {
            // In einer echten Implementierung würde hier ein File Dialog geöffnet
            console.log('Clicked to browse');
        });
        </script>
        """

        st.markdown(drag_drop_html, unsafe_allow_html=True)

        # Fallback: File Uploader für Demo
        st.markdown("**Demo: Datei hochladen**")
        uploaded_file = st.file_uploader(
            "Lade eine Projekt-Datei hoch:",
            type=["zip", "tar", "gz"],
            help="Für Demo-Zwecke: Lade eine ZIP-Datei deines Projekts hoch",
            label_visibility="collapsed",
        )

        if uploaded_file:
            self.selected_path = f"/workspace/uploaded_{uploaded_file.name}"
            st.success(f"✅ Datei hochgeladen: {uploaded_file.name}")
            st.info("ℹ️ In der echten Implementierung würde die Datei entpackt und analysiert")

    def render_path_input(self):
        """Rendert die Pfad-Eingabe"""
        col1, col2 = st.columns([3, 1])

        with col1:
            project_path = st.text_input(
                "Projekt-Pfad eingeben:",
                value=st.session_state.get("current_project", ""),
                placeholder="C:/Pfad/zum/Projekt",
                help="Geben Sie den vollständigen Pfad zu Ihrem Projektordner ein",
                label_visibility="collapsed",
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📁 Durchsuchen", use_container_width=True):
                st.info(
                    "Bitte geben Sie den Pfad manuell ein oder wählen Sie aus den Beispielen unten"
                )

        if project_path:
            if os.path.exists(project_path):
                if os.path.isdir(project_path):
                    self.selected_path = project_path
                    st.session_state.current_project = project_path
                    st.success(f"✅ Projekt ausgewählt: {os.path.basename(project_path)}")
                    self.show_project_preview(project_path)
                else:
                    st.error("❌ Der angegebene Pfad ist kein Ordner")
            else:
                st.warning("⚠️ Pfad existiert nicht")

    def render_quick_select(self):
        """Rendert Quick-Select Buttons"""
        st.markdown("**Schnellauswahl:**")

        quick_paths = ["C:/Users/keoku/Desktop/APP-Finisher", "C:/Projects/MyProject", "."]

        cols = st.columns(len(quick_paths))
        for i, path in enumerate(quick_paths):
            with cols[i]:
                if st.button(f"📂 {os.path.basename(path) or path}", key=f"quick_{i}"):
                    self.selected_path = path
                    st.session_state.current_project = path
                    st.success(f"✅ Projekt: {os.path.basename(path) or path}")
                    st.rerun()

    def show_project_preview(self, project_path: str):
        """Zeigt eine Vorschau des ausgewählten Projekts"""
        try:
            path_obj = Path(project_path)

            # Projekt-Info
            with st.expander("📋 Projekt-Vorschau", expanded=False):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Name:** {path_obj.name}")
                    st.markdown(f"**Pfad:** {project_path}")

                with col2:
                    if os.path.exists(project_path):
                        try:
                            file_count = len(list(Path(project_path).rglob("*")))
                            st.markdown(f"**Dateien:** {file_count}")
                        except:
                            st.markdown("**Dateien:** Unbekannt")

                        # Erkannte Projekt-Dateien
                        project_files = self.detect_project_files(project_path)
                        if project_files:
                            st.markdown("**Erkannte Dateien:**")
                            for file_type in project_files[:3]:  # Zeige nur erste 3
                                st.markdown(f"- {file_type}")
                            if len(project_files) > 3:
                                st.markdown(f"- ... und {len(project_files) - 3} weitere")

        except Exception as e:
            st.error(f"Fehler beim Lesen der Projekt-Informationen: {e}")

    def detect_project_files(self, project_path: str) -> list:
        """Erkennt bekannte Projekt-Dateien"""
        project_files = []

        # Bekannte Projekt-Dateien
        known_files = {
            "package.json": "Node.js",
            "requirements.txt": "Python",
            "Pipfile": "Python (Pipenv)",
            "pyproject.toml": "Python (Poetry)",
            "composer.json": "PHP",
            "Gemfile": "Ruby",
            "Cargo.toml": "Rust",
            "go.mod": "Go",
            "pom.xml": "Java (Maven)",
            "build.gradle": "Java (Gradle)",
            "Dockerfile": "Docker",
            "docker-compose.yml": "Docker Compose",
            "README.md": "Dokumentation",
            ".git": "Git Repository",
            "app.py": "Python App",
            "main.py": "Python App",
            "index.js": "Node.js App",
            "index.html": "Web App",
            "src/": "Source Code",
            "tests/": "Tests",
            "test/": "Tests",
        }

        try:
            for file_name, description in known_files.items():
                file_path = Path(project_path) / file_name
                if file_path.exists():
                    project_files.append(description)
        except:
            pass

        return project_files
