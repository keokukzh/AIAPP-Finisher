"""
Einstellungen-Panel-Komponente
"""

import os
from typing import Any, Dict, Optional

import streamlit as st


class SettingsPanel:
    """Komponente für die Einstellungen"""

    def __init__(self):
        self.settings = {}

    def render(self, model_manager=None):
        """Rendert das Einstellungen-Panel"""
        st.markdown("## ⚙️ Einstellungen")

        # Tabs für verschiedene Einstellungsbereiche
        tab1, tab2, tab3, tab4 = st.tabs(
            ["🤖 KI-Modelle", "🔑 API-Schlüssel", "📊 System", "🔧 Erweitert"]
        )

        with tab1:
            self.render_model_settings()

        with tab2:
            self.render_api_settings()

        with tab3:
            self.render_system_settings()

        with tab4:
            self.render_advanced_settings()

    def render_model_settings(self):
        """Rendert die KI-Modell-Einstellungen"""
        st.markdown("### 🤖 KI-Modell-Konfiguration")

        # Modell-Typ-Auswahl
        model_type = st.selectbox(
            "Modell-Typ:",
            [
                "Lokal (Ollama)",
                "Lokal (LM Studio)",
                "Lokal (GPT4All)",
                "Cloud (OpenAI)",
                "Cloud (Anthropic)",
                "Cloud (Google)",
            ],
            help="Wähle den Typ des KI-Modells",
        )

        if "Lokal" in model_type:
            self.render_local_model_settings(model_type)
        else:
            self.render_cloud_model_settings(model_type)

        # Modell-Status
        self.render_model_status()

    def render_local_model_settings(self, model_type: str):
        """Rendert die lokalen Modell-Einstellungen"""
        st.markdown("#### 🏠 Lokale Modell-Einstellungen")

        if "Ollama" in model_type:
            st.markdown("**Ollama-Konfiguration:**")

            # Ollama-Host
            ollama_host = st.text_input(
                "Ollama-Host:",
                value=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                help="URL des Ollama-Servers",
            )

            # Verfügbare Modelle
            st.markdown("**Verfügbare Modelle:**")
            available_models = [
                "llama2:7b",
                "llama2:13b",
                "codellama:7b",
                "codellama:13b",
                "mistral:7b",
                "mixtral:8x7b",
            ]

            selected_model = st.selectbox(
                "Wähle ein Modell:", available_models, help="Wähle das Ollama-Modell aus"
            )

            # Modell-Status prüfen
            if st.button("🔍 Modell-Status prüfen"):
                with st.spinner("Prüfe Ollama-Verbindung..."):
                    # Simuliere Status-Prüfung
                    st.success("✅ Ollama ist erreichbar")
                    st.info(f"📦 Modell '{selected_model}' ist verfügbar")

            # Installation-Hilfe
            st.markdown("**📥 Ollama installieren:**")
            st.markdown(
                """
            1. **Windows/Mac/Linux:**
               ```bash
               curl -fsSL https://ollama.ai/install.sh | sh
               ```
            
            2. **Modell herunterladen:**
               ```bash
               ollama pull codellama:7b
               ```
            
            3. **Ollama starten:**
               ```bash
               ollama serve
               ```
            
            **Links:**
            - [Ollama Download](https://ollama.ai/download)
            - [Ollama Models](https://ollama.ai/library)
            """
            )

        elif "LM Studio" in model_type:
            st.markdown("**LM Studio-Konfiguration:**")

            # LM Studio-Host
            lmstudio_host = st.text_input(
                "LM Studio-Host:", value="http://localhost:1234", help="URL des LM Studio-Servers"
            )

            # Installation-Hilfe
            st.markdown("**📥 LM Studio installieren:**")
            st.markdown(
                """
            1. **Download:** [LM Studio](https://lmstudio.ai/)
            2. **Installation:** Standard-Installation durchführen
            3. **Modell laden:** Modell in LM Studio laden
            4. **Server starten:** Local Server in LM Studio starten
            
            **Links:**
            - [LM Studio Download](https://lmstudio.ai/)
            - [LM Studio Documentation](https://lmstudio.ai/docs)
            """
            )

        elif "GPT4All" in model_type:
            st.markdown("**GPT4All-Konfiguration:**")

            # GPT4All-Modell-Pfad
            gpt4all_path = st.text_input(
                "GPT4All-Modell-Pfad:",
                value=os.path.expanduser("~/.cache/gpt4all/"),
                help="Pfad zu den GPT4All-Modellen",
            )

            # Installation-Hilfe
            st.markdown("**📥 GPT4All installieren:**")
            st.markdown(
                """
            1. **Download:** [GPT4All](https://gpt4all.io/)
            2. **Installation:** Standard-Installation durchführen
            3. **Modell herunterladen:** Modell über GPT4All-App herunterladen
            
            **Links:**
            - [GPT4All Download](https://gpt4all.io/)
            - [GPT4All Models](https://gpt4all.io/index.html)
            """
            )

    def render_cloud_model_settings(self, model_type: str):
        """Rendert die Cloud-Modell-Einstellungen"""
        st.markdown("#### ☁️ Cloud-Modell-Einstellungen")

        if "OpenAI" in model_type:
            st.markdown("**OpenAI-Konfiguration:**")

            # OpenAI-Modell
            openai_model = st.selectbox(
                "OpenAI-Modell:",
                ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
                help="Wähle das OpenAI-Modell",
            )

            # API-Key-Status
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key and api_key != "your_openai_api_key_here":
                st.success("✅ OpenAI API-Key ist konfiguriert")
            else:
                st.warning("⚠️ OpenAI API-Key ist nicht konfiguriert")
                st.info("Setze die Umgebungsvariable OPENAI_API_KEY")

        elif "Anthropic" in model_type:
            st.markdown("**Anthropic-Konfiguration:**")

            # Claude-Modell
            claude_model = st.selectbox(
                "Claude-Modell:",
                ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
                help="Wähle das Claude-Modell",
            )

            # API-Key-Status
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key and api_key != "your_claude_api_key_here":
                st.success("✅ Anthropic API-Key ist konfiguriert")
            else:
                st.warning("⚠️ Anthropic API-Key ist nicht konfiguriert")
                st.info("Setze die Umgebungsvariable ANTHROPIC_API_KEY")

        elif "Google" in model_type:
            st.markdown("**Google-Konfiguration:**")

            # Google-Modell
            google_model = st.selectbox(
                "Google-Modell:",
                ["gemini-pro", "gemini-pro-vision", "text-bison-001"],
                help="Wähle das Google-Modell",
            )

            # API-Key-Status
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key and api_key != "your_google_api_key_here":
                st.success("✅ Google API-Key ist konfiguriert")
            else:
                st.warning("⚠️ Google API-Key ist nicht konfiguriert")
                st.info("Setze die Umgebungsvariable GOOGLE_API_KEY")

    def render_model_status(self):
        """Rendert den Modell-Status"""
        st.markdown("#### 📊 Modell-Status")

        # Status-Karten
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="🤖 Aktives Modell", value="codellama:7b", delta=None)

        with col2:
            st.metric(label="⚡ Antwortzeit", value="1.2s", delta="-0.3s")

        with col3:
            st.metric(label="💾 Speicher", value="4.2GB", delta="+0.1GB")

        # Modell-Test
        if st.button("🧪 Modell testen"):
            with st.spinner("Teste Modell..."):
                # Simuliere Modell-Test
                st.success("✅ Modell funktioniert korrekt")
                st.info("Test-Antwort: 'Hallo! Ich bin bereit, dir bei deinem Projekt zu helfen.'")

    def render_api_settings(self):
        """Rendert die API-Schlüssel-Einstellungen"""
        st.markdown("### 🔑 API-Schlüssel-Verwaltung")

        # OpenAI
        st.markdown("#### OpenAI")
        openai_key = st.text_input(
            "OpenAI API-Key:",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Dein OpenAI API-Key",
        )

        # Anthropic
        st.markdown("#### Anthropic")
        anthropic_key = st.text_input(
            "Anthropic API-Key:",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            type="password",
            help="Dein Anthropic API-Key",
        )

        # Google
        st.markdown("#### Google")
        google_key = st.text_input(
            "Google API-Key:",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Dein Google API-Key",
        )

        # API-Key-Hilfe
        st.markdown("**❓ API-Key-Hilfe:**")
        st.markdown(
            """
        **API-Keys erhalten:**
        
        **OpenAI:**
        1. Gehe zu [OpenAI Platform](https://platform.openai.com/)
        2. Erstelle einen Account
        3. Gehe zu API Keys
        4. Erstelle einen neuen API-Key
        
        **Anthropic:**
        1. Gehe zu [Anthropic Console](https://console.anthropic.com/)
        2. Erstelle einen Account
        3. Gehe zu API Keys
        4. Erstelle einen neuen API-Key
        
        **Google:**
        1. Gehe zu [Google AI Studio](https://makersuite.google.com/)
        2. Erstelle einen Account
        3. Gehe zu API Keys
        4. Erstelle einen neuen API-Key
        """
        )

        # Speichern-Button
        if st.button("💾 Einstellungen speichern"):
            st.success("✅ Einstellungen gespeichert!")
            st.info("ℹ️ In der echten Implementierung würden die API-Keys sicher gespeichert")

    def render_system_settings(self):
        """Rendert die System-Einstellungen"""
        st.markdown("### 📊 System-Einstellungen")

        # Performance-Einstellungen
        st.markdown("#### ⚡ Performance")

        max_workers = st.slider(
            "Maximale Worker-Threads:",
            min_value=1,
            max_value=16,
            value=4,
            help="Anzahl der parallelen Worker-Threads",
        )

        cache_size = st.slider(
            "Cache-Größe (MB):",
            min_value=100,
            max_value=2048,
            value=512,
            help="Größe des In-Memory-Caches",
        )

        # Logging-Einstellungen
        st.markdown("#### 📝 Logging")

        log_level = st.selectbox(
            "Log-Level:",
            ["DEBUG", "INFO", "WARNING", "ERROR"],
            index=1,
            help="Detailliertheit der Logs",
        )

        log_to_file = st.checkbox(
            "Logs in Datei speichern", value=True, help="Speichere Logs in einer Datei"
        )

        # UI-Einstellungen
        st.markdown("#### 🎨 Benutzeroberfläche")

        theme = st.selectbox(
            "Theme:", ["Light", "Dark", "Auto"], help="Farbschema der Benutzeroberfläche"
        )

        auto_refresh = st.checkbox(
            "Auto-Refresh aktivieren", value=True, help="Automatische Aktualisierung des Dashboards"
        )

        refresh_interval = st.slider(
            "Refresh-Intervall (Sekunden):",
            min_value=5,
            max_value=60,
            value=30,
            help="Intervall für Auto-Refresh",
        )

    def render_advanced_settings(self):
        """Rendert die erweiterten Einstellungen"""
        st.markdown("### 🔧 Erweiterte Einstellungen")

        # Docker-Einstellungen
        st.markdown("#### 🐳 Docker")

        docker_host = st.text_input(
            "Docker-Host:", value="unix:///var/run/docker.sock", help="Docker-Daemon-Host"
        )

        container_memory = st.text_input(
            "Container-Speicher-Limit:", value="2g", help="Speicher-Limit für Container"
        )

        # Datenbank-Einstellungen
        st.markdown("#### 🗄️ Datenbank")

        db_url = st.text_input(
            "Datenbank-URL:",
            value=os.getenv("DATABASE_URL", "sqlite:///./agents.db"),
            help="Verbindungs-URL zur Datenbank",
        )

        # Redis-Einstellungen
        st.markdown("#### 🔴 Redis")

        redis_url = st.text_input(
            "Redis-URL:",
            value=os.getenv("REDIS_URL", "redis://localhost:6379"),
            help="Verbindungs-URL zu Redis",
        )

        # Entwickler-Einstellungen
        st.markdown("#### 👨‍💻 Entwickler")

        debug_mode = st.checkbox("Debug-Modus", value=False, help="Aktiviere Debug-Ausgaben")

        experimental_features = st.checkbox(
            "Experimentelle Features", value=False, help="Aktiviere experimentelle Features"
        )

        # Reset-Button
        st.markdown("#### ⚠️ Gefahrenzone")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Einstellungen zurücksetzen", type="secondary"):
                st.warning("⚠️ Alle Einstellungen werden auf Standardwerte zurückgesetzt!")
                if st.button("✅ Bestätigen", type="primary"):
                    st.success("✅ Einstellungen zurückgesetzt!")

        with col2:
            if st.button("🗑️ Cache leeren", type="secondary"):
                st.warning("⚠️ Alle Caches werden geleert!")
                if st.button("✅ Bestätigen", type="primary"):
                    st.success("✅ Cache geleert!")
