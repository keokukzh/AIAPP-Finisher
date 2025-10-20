"""
Chat-Interface-Komponente für den KI-Projektmanager
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st


class ChatInterface:
    """Komponente für das Chat-Interface mit dem KI-Projektmanager"""

    def __init__(self):
        self.chat_history = []
        self.project_context = None

    def render(self, project_context: Dict[str, Any], model_manager=None):
        """Rendert das Chat-Interface"""
        self.project_context = project_context

        st.markdown("### 💬 Chat mit KI-Projektmanager")

        # Chat-Status
        self.render_chat_status()

        # Chat-Historie
        self.render_chat_history()

        # Chat-Input
        self.render_chat_input()

        # Schnellzugriff-Buttons
        self.render_quick_actions()

    def render_chat_status(self):
        """Rendert den Chat-Status"""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🤖 KI-Projektmanager:** Online")

        with col2:
            if self.project_context:
                project_name = self.project_context.get("project_name", "Unbekannt")
                st.markdown(f"**📁 Projekt:** {project_name}")
            else:
                st.markdown("**📁 Projekt:** Nicht geladen")

        with col3:
            st.markdown(f"**💬 Nachrichten:** {len(self.chat_history)}")

    def render_chat_history(self):
        """Rendert die Chat-Historie"""
        st.markdown("#### 📜 Chat-Verlauf")

        # Chat-Container
        chat_container = st.container()

        with chat_container:
            if not self.chat_history:
                st.info("👋 Hallo! Ich bin dein KI-Projektmanager. Wie kann ich dir helfen?")
            else:
                for message in self.chat_history:
                    self.render_message(message)

    def render_message(self, message: Dict[str, Any]):
        """Rendert eine einzelne Chat-Nachricht"""
        message_type = message.get("type", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", datetime.now().isoformat())

        if message_type == "user":
            st.markdown(
                f"""
            <div class="chat-message user-message">
                <strong>👤 Du:</strong><br>
                {content}<br>
                <small>{timestamp}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="chat-message ai-message">
                <strong>🤖 KI-Projektmanager:</strong><br>
                {content}<br>
                <small>{timestamp}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    def render_chat_input(self):
        """Rendert den Chat-Input"""
        st.markdown("#### 💭 Nachricht eingeben")

        # Chat-Input
        user_input = st.text_area(
            "Deine Nachricht:",
            placeholder="Frage mich alles über dein Projekt! Z.B.: 'Optimiere die Performance' oder 'Erstelle Tests für die API'",
            height=100,
            key="chat_input",
        )

        # Send-Button
        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            if st.button("📤 Senden", type="primary"):
                if user_input.strip():
                    self.send_message(user_input.strip())
                    st.rerun()

        with col2:
            if st.button("🗑️ Löschen"):
                self.chat_history.clear()
                st.rerun()

    def render_quick_actions(self):
        """Rendert Schnellzugriff-Buttons"""
        st.markdown("#### ⚡ Schnellzugriff")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔍 Projekt analysieren"):
                self.send_message("Analysiere das Projekt und zeige mir eine Übersicht")

        with col2:
            if st.button("🛠️ Optimierungen"):
                self.send_message("Welche Optimierungen kannst du für mein Projekt vorschlagen?")

        with col3:
            if st.button("🧪 Tests erstellen"):
                self.send_message("Erstelle Tests für die wichtigsten Komponenten")

        with col4:
            if st.button("📊 Performance"):
                self.send_message("Analysiere die Performance und zeige Verbesserungsmöglichkeiten")

    def send_message(self, message: str):
        """Sendet eine Nachricht und generiert eine Antwort"""
        # User-Nachricht hinzufügen
        user_message = {
            "type": "user",
            "content": message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        self.chat_history.append(user_message)

        # KI-Antwort generieren (echt)
        ai_response = self.generate_real_ai_response(message)

        # KI-Antwort hinzufügen
        ai_message = {
            "type": "ai",
            "content": ai_response,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        }
        self.chat_history.append(ai_message)

    def generate_real_ai_response(self, user_message: str) -> str:
        """Generiert eine echte KI-Antwort basierend auf der User-Nachricht"""
        try:
            import requests

            # Sende Nachricht an Backend Chat-API
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": user_message, "context": self.project_context},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("response", "Keine Antwort erhalten")
            else:
                return f"Fehler beim Generieren der Antwort: {response.text}"

        except Exception as e:
            return f"Fehler bei der KI-Kommunikation: {str(e)}"

    def generate_ai_response(self, user_message: str) -> str:
        """DEPRECATED: Verwende generate_real_ai_response"""
        return self.generate_real_ai_response(user_message)

    def generate_analysis_response(self) -> str:
        """Generiert eine Analyse-Antwort"""
        if not self.project_context:
            return "❌ Kein Projekt geladen. Bitte wähle zuerst ein Projekt aus."

        project_name = self.project_context.get("project_name", "Unbekannt")
        file_count = self.project_context.get("file_count", 0)
        frameworks = self.project_context.get("frameworks", [])

        response = f"""
        📊 **Projekt-Analyse für {project_name}:**

        **Grundlegende Informationen:**
        - 📄 {file_count} Dateien gefunden
        - 🛠️ {len(frameworks)} Frameworks erkannt
        
        **Erkannte Technologien:**
        """

        for framework in frameworks:
            response += (
                f"- {framework.get('name', 'Unknown')} ({framework.get('type', 'Unknown')})\n"
            )

        response += """
        
        **Nächste Schritte:**
        1. 🔍 Detaillierte Code-Analyse
        2. 📦 Dependency-Check
        3. 🧪 Test-Coverage-Analyse
        4. 🔒 Security-Scan
        
        Möchtest du, dass ich eine dieser Analysen durchführe?
        """

        return response

    def generate_optimization_response(self) -> str:
        """Generiert eine Optimierungs-Antwort"""
        return """
        🚀 **Optimierungsvorschläge:**

        **Performance-Optimierungen:**
        - ⚡ Lazy Loading für große Module implementieren
        - 🗄️ Datenbankabfragen optimieren
        - 📦 Bundle-Size reduzieren
        - 🔄 Caching-Strategien implementieren

        **Code-Qualität:**
        - 🧹 Code-Duplikate entfernen
        - 📝 Type Hints hinzufügen
        - 🧪 Test-Coverage erhöhen
        - 📚 Dokumentation verbessern

        **Security-Verbesserungen:**
        - 🔐 Input-Validierung verstärken
        - 🛡️ Dependencies aktualisieren
        - 🔒 Secrets-Management verbessern

        Soll ich eine dieser Optimierungen für dich durchführen?
        """

    def generate_testing_response(self) -> str:
        """Generiert eine Testing-Antwort"""
        return """
        🧪 **Test-Strategie:**

        **Unit-Tests:**
        - ✅ Test-Framework erkannt: pytest
        - 📝 Generiere Tests für kritische Funktionen
        - 🎯 Ziel: 80% Code-Coverage

        **Integration-Tests:**
        - 🔗 API-Endpoint-Tests
        - 🗄️ Datenbank-Integration-Tests
        - 🌐 Frontend-Backend-Integration

        **Test-Automatisierung:**
        - ⚙️ CI/CD-Pipeline einrichten
        - 🔄 Automatische Test-Ausführung
        - 📊 Coverage-Reports generieren

        Soll ich Tests für spezifische Komponenten erstellen?
        """

    def generate_security_response(self) -> str:
        """Generiert eine Security-Antwort"""
        return """
        🔒 **Security-Analyse:**

        **Dependency-Scan:**
        - ✅ Keine kritischen Vulnerabilities gefunden
        - ⚠️ 2 mittlere Sicherheitslücken in Dependencies
        - 🔄 Update-Empfehlungen verfügbar

        **Code-Security:**
        - ✅ Keine hardcoded Secrets gefunden
        - ✅ Input-Validierung implementiert
        - ⚠️ SQL-Injection-Schutz prüfen

        **Empfohlene Maßnahmen:**
        1. 🔄 Dependencies aktualisieren
        2. 🛡️ Security-Headers hinzufügen
        3. 🔐 Rate-Limiting implementieren

        Soll ich diese Security-Verbesserungen durchführen?
        """

    def generate_deployment_response(self) -> str:
        """Generiert eine Deployment-Antwort"""
        return """
        🚀 **Deployment-Strategie:**

        **Containerisierung:**
        - 🐳 Docker-Container erstellen
        - 📦 Multi-Stage-Build optimieren
        - 🔧 Environment-Configs

        **CI/CD-Pipeline:**
        - ⚙️ GitHub Actions / GitLab CI
        - 🧪 Automatische Tests
        - 🚀 Automatisches Deployment

        **Infrastruktur:**
        - ☁️ Cloud-Deployment (AWS/Azure/GCP)
        - 🔄 Load-Balancing
        - 📊 Monitoring & Logging

        **Nächste Schritte:**
        1. Dockerfile erstellen
        2. CI/CD-Pipeline einrichten
        3. Production-Environment konfigurieren

        Soll ich die Deployment-Pipeline für dich einrichten?
        """

    def generate_documentation_response(self) -> str:
        """Generiert eine Dokumentations-Antwort"""
        return """
        📚 **Dokumentations-Plan:**

        **API-Dokumentation:**
        - 📖 OpenAPI/Swagger-Spec generieren
        - 🔗 Endpoint-Dokumentation
        - 💡 Beispiel-Requests

        **Code-Dokumentation:**
        - 📝 Docstrings für alle Funktionen
        - 🏗️ Architektur-Diagramme
        - 🎯 README mit Setup-Anleitung

        **Benutzer-Dokumentation:**
        - 👥 User-Guide erstellen
        - 🔧 Installation-Anleitung
        - ❓ FAQ-Sektion

        **Entwickler-Dokumentation:**
        - 🏗️ Architektur-Übersicht
        - 🔄 Contributing-Guide
        - 🧪 Testing-Guide

        Soll ich die Dokumentation für dein Projekt erstellen?
        """

    def generate_general_response(self) -> str:
        """Generiert eine allgemeine Antwort"""
        return """
        🤖 **KI-Projektmanager:**

        Ich bin hier, um dir bei deinem Projekt zu helfen! Ich kann:

        🔍 **Analysieren:** Dein Projekt vollständig durchleuchten
        🛠️ **Optimieren:** Performance und Code-Qualität verbessern
        🧪 **Testen:** Umfassende Tests erstellen
        🔒 **Sichern:** Security-Issues finden und beheben
        🚀 **Deployen:** Deployment-Pipeline einrichten
        📚 **Dokumentieren:** Vollständige Dokumentation erstellen

        **Beispiel-Fragen:**
        - "Analysiere mein Projekt"
        - "Optimiere die Performance"
        - "Erstelle Tests für die API"
        - "Finde Security-Probleme"
        - "Bereite Deployment vor"

        Was möchtest du als nächstes machen?
        """
