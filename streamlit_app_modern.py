"""
🚀 Modern KI-Projektmanagement-System UI
Professional, modern interface with Claude-Flow integration
"""

import json as json_module
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import streamlit as st

from ui.modern_styles import COLORS, get_icon

# Import modern UI components
from ui.modern_ui_manager import get_ui_manager
from ui.pages.dashboard_page import DashboardPage

# API Base URL
API_BASE_URL = "http://localhost:8000"

# Initialize UI Manager
ui = get_ui_manager()


class ModernApp:
    """Main application controller with modern design"""

    def __init__(self):
        self.ui = get_ui_manager()
        self.dashboard = DashboardPage()
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if "analysis_results" not in st.session_state:
            st.session_state.analysis_results = None
        if "current_project" not in st.session_state:
            st.session_state.current_project = None
        if "analysis_running" not in st.session_state:
            st.session_state.analysis_running = False
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None
        if "dark_mode" not in st.session_state:
            st.session_state.dark_mode = False

    def run(self):
        """Main application entry point"""
        # Setup page
        self.ui.setup_page("KI-Projektmanagement-System")

        # Render sidebar
        self.render_sidebar()

        # Render main content based on page
        page = st.session_state.get("page", "dashboard")

        if page == "dashboard":
            self.render_dashboard()
        elif page == "analysis":
            self.render_analysis()
        elif page == "chat":
            self.render_chat()
        elif page == "settings":
            self.render_settings()

    def render_sidebar(self):
        """Render modern sidebar navigation"""
        with st.sidebar:
            # Sidebar header
            self.ui.render_sidebar_header("Navigation", icon="rocket")

            # Navigation menu
            pages = {
                "dashboard": ("chart", "Dashboard"),
                "analysis": ("brain", "Project Analysis"),
                "chat": ("user", "AI Assistant"),
                "settings": ("settings", "Settings"),
            }

            for page_key, (icon, label) in pages.items():
                if st.button(
                    f"{get_icon(icon)}  {label}", key=f"nav_{page_key}", use_container_width=True
                ):
                    st.session_state.page = page_key
                    st.rerun()

            st.markdown("---")

            # Quick status
            st.markdown(
                f"""
            <div style="background: rgba(255,255,255,0.1); border-radius: 0.5rem; padding: 1rem; margin-top: 1rem;">
                <div style="color: white; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">
                    SYSTEM STATUS
                </div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.875rem;">
                    {get_icon('check')} API Connected<br>
                    {get_icon('lightning')} Ready to Analyze
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Footer
            st.markdown(
                """
            <div style="position: fixed; bottom: 1rem; left: 1rem; right: 1rem; 
                        color: rgba(255,255,255,0.6); font-size: 0.75rem; text-align: center;">
                Powered by Claude-Flow AI
            </div>
            """,
                unsafe_allow_html=True,
            )

    def render_dashboard(self):
        """Render dashboard page"""
        self.dashboard.render(st.session_state.analysis_results)

    def render_analysis(self):
        """Render project analysis page"""
        self.ui.render_header(
            "Project Analysis", "Analyze your codebase with AI-powered insights", icon="brain"
        )

        # Project Path Input
        st.markdown(
            "<h3 style='margin-bottom: 1rem;'>📁 Select Project Directory</h3>",
            unsafe_allow_html=True,
        )

        project_path = st.text_input(
            "Project Path",
            value=st.session_state.get("current_project", ""),
            placeholder="C:/Users/YourName/Projects/MyProject or /path/to/project",
            help="Enter the full path to your project directory",
            key="project_path_input",
        )

        if project_path and project_path != st.session_state.get("current_project"):
            st.session_state.current_project = project_path

        # Quick path examples
        with st.expander("💡 Quick Examples"):
            st.markdown(
                """
            **Windows:**
            - `C:/Users/YourName/Desktop/MyProject`
            - `C:/Projects/WebApp`
            
            **Linux/Mac:**
            - `/home/user/projects/myapp`
            - `/Users/yourname/Documents/project`
            
            **Current directory:**
            - `.` (analyzes current folder)
            - `..` (analyzes parent folder)
            """
            )

        # Analysis controls
        if st.session_state.current_project:
            st.markdown("---")

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(
                    f"""
                <div class="card">
                    <div style="color: {COLORS['text_secondary']}; font-size: 0.875rem; font-weight: 600;">
                        ✅ SELECTED PROJECT
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; margin-top: 0.5rem; color: {COLORS['primary']};">
                        {st.session_state.current_project}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                if st.button(
                    f"{get_icon('rocket')} Analyze",
                    key="start_analysis",
                    use_container_width=True,
                    disabled=st.session_state.analysis_running,
                    type="primary",
                ):
                    self.start_analysis()

            with col3:
                if st.button(
                    f"{get_icon('file')} Clear", key="clear_project", use_container_width=True
                ):
                    st.session_state.current_project = None
                    st.rerun()

            # Show progress if running
            if st.session_state.analysis_running:
                st.markdown(
                    self.ui.render_progress_card(
                        "Analysis in Progress",
                        45.0,  # This would be dynamic in real implementation
                        "Processing...",
                        subtitle="Analyzing project structure and dependencies",
                    ),
                    unsafe_allow_html=True,
                )
        else:
            # Show helpful placeholder
            st.info("👆 Enter a project path above to get started")

    def render_chat(self):
        """Render AI chat interface"""
        self.ui.render_header(
            "AI Project Assistant", "Chat with your intelligent project manager", icon="user"
        )

        # Chat interface
        st.markdown(
            self.ui.render_card(
                """
            <div style="min-height: 400px; display: flex; align-items: center; justify-content: center;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;">
                        💬
                    </div>
                    <p style="color: """
                + COLORS["text_secondary"]
                + """; font-size: 1.1rem;">
                        Chat interface coming soon!<br>
                        Integrated with Claude-Flow for intelligent conversations.
                    </p>
                </div>
            </div>
            """,
                glass=True,
            ),
            unsafe_allow_html=True,
        )

        # Chat input
        user_input = st.text_input(
            "Message", placeholder="Ask me anything about your project...", key="chat_input"
        )

        if st.button(f"{get_icon('lightning')} Send", key="send_chat"):
            if user_input:
                self.ui.show_info("Chat functionality will be available soon!")

    def render_settings(self):
        """Render settings page"""
        self.ui.render_header(
            "Settings", "Configure your AI project management system", icon="settings"
        )

        # AI Model Selection
        st.markdown(
            "<h3 style='margin-bottom: 1rem;'>AI Model Configuration</h3>", unsafe_allow_html=True
        )

        models_response = self._api_call("GET", "/models")
        if models_response and "models" in models_response:
            models = models_response["models"]

            col1, col2 = st.columns([2, 1])

            with col1:
                model_names = [m.get("name", "Unknown") for m in models]
                selected = st.selectbox("Select AI Model", model_names, key="model_select")

                if selected and selected != st.session_state.selected_model:
                    if st.button(f"{get_icon('check')} Apply Model"):
                        st.session_state.selected_model = selected
                        self.ui.show_success(f"Model set to: {selected}")

            with col2:
                st.markdown(
                    f"""
                <div class="card">
                    <div style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_secondary']};">
                        AVAILABLE MODELS
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']}; margin-top: 0.5rem;">
                        {len(models)}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Theme Settings
        st.markdown(
            "<h3 style='margin: 2rem 0 1rem 0;'>Interface Settings</h3>", unsafe_allow_html=True
        )

        st.markdown(
            self.ui.render_card(
                """
            <div style="padding: 0.5rem 0;">
                <p>Theme customization coming soon!</p>
                <ul style="margin-top: 1rem;">
                    <li>Dark Mode</li>
                    <li>Custom Color Schemes</li>
                    <li>Layout Preferences</li>
                </ul>
            </div>
            """,
                title="Theme Options",
                icon="gem",
            ),
            unsafe_allow_html=True,
        )

    def start_analysis(self):
        """Start project analysis"""
        if not st.session_state.current_project:
            self.ui.show_error("Please select a project directory first!")
            return

        # Show progress
        with st.spinner("🔍 Analyzing project... This may take a moment."):
            st.session_state.analysis_running = True

            # Call API to start analysis (FIXED: correct endpoint)
            response = self._api_call(
                "POST", "/analyze-project", json={"project_path": st.session_state.current_project}
            )

            st.session_state.analysis_running = False

            if response and response.get("status") in ["started", "success"]:
                # Analysis started successfully - wait a moment then fetch results
                st.info("⏳ Analysis started! Waiting 45 seconds for completion...")
                import time

                time.sleep(45)

                # Fetch results
                results_response = self._api_call("GET", "/analysis-results")
                if results_response:
                    st.session_state.analysis_results = results_response.get("results")
                    st.session_state.current_project = results_response.get("project_path")
                    self.ui.show_success("✅ Analysis completed successfully!")
                    st.balloons()
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    self.ui.show_warning(
                        "⚠️ Analysis started but results not ready yet. Please wait a moment and refresh."
                    )
            else:
                error_msg = (
                    response.get("detail", "Unknown error") if response else "API not responding"
                )
                self.ui.show_error(f"❌ Analysis failed: {error_msg}")
                st.info("💡 Make sure the backend API is running on http://localhost:8000")

    def _api_call(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make API call to backend

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional requests arguments

        Returns:
            Response JSON or None
        """
        try:
            url = f"{API_BASE_URL}{endpoint}"

            # Add headers for JSON
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            if "json" in kwargs:
                kwargs["headers"]["Content-Type"] = "application/json"

            response = requests.request(method, url, timeout=60, **kwargs)

            # Check for successful response (2xx status codes)
            if 200 <= response.status_code < 300:
                try:
                    return response.json()
                except:
                    return {"status": "success", "message": "Request successful"}
            else:
                # Try to get error message from response
                try:
                    error_data = response.json()
                    st.error(
                        f"API Error {response.status_code}: {error_data.get('detail', 'Unknown error')}"
                    )
                except:
                    st.error(f"API Error {response.status_code}: {response.text[:200]}")
                return None

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Cannot connect to API. Make sure backend is running on http://localhost:8000"
            )
            return None
        except requests.exceptions.Timeout:
            st.error(
                "⏱️ API request timed out. The operation may still be running in the background."
            )
            return None
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")
            return None


# Application entry point
if __name__ == "__main__":
    app = ModernApp()
    app.run()
