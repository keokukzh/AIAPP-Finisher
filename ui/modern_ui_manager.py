"""
Modern UI Manager - Orchestrates all UI components with professional design
"""

from typing import Any, Dict, List, Optional

import streamlit as st

from .modern_styles import COLORS, get_icon, get_modern_css


class ModernUIManager:
    """Manages modern UI components and layout"""

    def __init__(self):
        self.page_config_set = False

    def setup_page(self, title: str = "KI-Projektmanagement-System"):
        """Setup page configuration and inject modern CSS"""
        if not self.page_config_set:
            st.set_page_config(
                page_title=title,
                page_icon="🚀",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    "Get Help": "https://github.com/yourusername/ki-projektmanagement",
                    "Report a bug": "https://github.com/yourusername/ki-projektmanagement/issues",
                    "About": "# KI-Projektmanagement-System\nIntelligent AI-Powered Project Management",
                },
            )
            self.page_config_set = True

        # Inject modern CSS
        st.markdown(get_modern_css(), unsafe_allow_html=True)

    def render_header(self, title: str, subtitle: Optional[str] = None, icon: str = "rocket"):
        """
        Render modern page header

        Args:
            title: Main title
            subtitle: Optional subtitle
            icon: Icon name
        """
        st.markdown(
            f"""
        <div class="premium-card animate-slide-up" style="margin-bottom: 2rem;">
            <h1 style="margin: 0;">{get_icon(icon)} {title}</h1>
            {f'<p style="font-size: 1.1rem; color: {COLORS["text_secondary"]}; margin: 0.5rem 0 0 0;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_metric_card(
        self,
        label: str,
        value: str,
        delta: Optional[str] = None,
        icon: str = "chart",
        color: str = "primary",
    ):
        """
        Render modern metric card

        Args:
            label: Metric label
            value: Metric value
            delta: Optional delta value
            icon: Icon name
            color: Color theme
        """
        delta_html = ""
        if delta:
            delta_color = COLORS["success"] if delta.startswith("+") else COLORS["error"]
            delta_html = f'<div style="color: {delta_color}; font-weight: 600; margin-top: 0.5rem;">{delta}</div>'

        return f"""
        <div class="card animate-fade-in">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.875rem; font-weight: 600; color: {COLORS['text_secondary']}; 
                               text-transform: uppercase; letter-spacing: 0.05em;">
                        {label}
                    </div>
                    <div style="font-size: 2rem; font-weight: 700; color: {COLORS[color]}; margin-top: 0.5rem;">
                        {value}
                    </div>
                    {delta_html}
                </div>
                <div style="font-size: 3rem; opacity: 0.3;">
                    {get_icon(icon)}
                </div>
            </div>
        </div>
        """

    def render_status_badge(self, status: str, type: str = "info") -> str:
        """
        Render status badge

        Args:
            status: Status text
            type: Badge type (success, warning, error, info)

        Returns:
            HTML string for badge
        """
        return f'<span class="status-pill status-{type}">{status}</span>'

    def render_card(
        self,
        content: str,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        glass: bool = False,
    ) -> str:
        """
        Render content card

        Args:
            content: Card content (HTML)
            title: Optional card title
            icon: Optional icon name
            glass: Use glassmorphism effect

        Returns:
            HTML string for card
        """
        card_class = "glass" if glass else "card"
        title_html = ""
        if title:
            icon_html = f"{get_icon(icon)} " if icon else ""
            title_html = f'<h3 style="margin-top: 0;">{icon_html}{title}</h3>'

        return f"""
        <div class="{card_class} animate-fade-in">
            {title_html}
            {content}
        </div>
        """

    def render_progress_card(
        self, title: str, progress: float, status: str, subtitle: Optional[str] = None
    ) -> str:
        """
        Render progress card with modern design

        Args:
            title: Card title
            progress: Progress value (0-100)
            status: Status text
            subtitle: Optional subtitle

        Returns:
            HTML string for progress card
        """
        status_type = "success" if progress == 100 else "info" if progress > 0 else "warning"
        status_badge = self.render_status_badge(status, status_type)
        subtitle_html = (
            f'<p style="color: {COLORS["text_secondary"]}; margin: 0.5rem 0;">{subtitle}</p>'
            if subtitle
            else ""
        )

        return f"""
        <div class="card animate-slide-up">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0;">{title}</h4>
                {status_badge}
            </div>
            {subtitle_html}
            <div style="background: {COLORS['surface_variant']}; border-radius: 9999px; height: 12px; overflow: hidden; margin-top: 1rem;">
                <div style="background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%); 
                           height: 100%; width: {progress}%; transition: width 0.5s ease-out; border-radius: 9999px;">
                </div>
            </div>
            <div style="text-align: right; margin-top: 0.5rem; font-weight: 600; color: {COLORS['primary']};">
                {progress:.1f}%
            </div>
        </div>
        """

    def create_columns_layout(self, ratios: List[int]):
        """
        Create responsive column layout

        Args:
            ratios: Column width ratios

        Returns:
            Streamlit columns
        """
        return st.columns(ratios)

    def render_sidebar_header(self, title: str, icon: str = "settings"):
        """Render sidebar header"""
        st.sidebar.markdown(
            f"""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">
                {get_icon(icon)}
            </div>
            <h2 style="color: white; margin: 0; font-size: 1.5rem;">
                {title}
            </h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_feature_grid(self, features: List[Dict[str, str]]):
        """
        Render feature grid

        Args:
            features: List of dicts with 'icon', 'title', 'description'
        """
        cols = st.columns(len(features))
        for col, feature in zip(cols, features):
            with col:
                st.markdown(
                    f"""
                <div class="card" style="text-align: center; height: 100%;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">
                        {get_icon(feature.get('icon', 'star'))}
                    </div>
                    <h4>{feature['title']}</h4>
                    <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                        {feature['description']}
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    def render_timeline_item(
        self, title: str, status: str, time: str, description: Optional[str] = None
    ):
        """Render timeline item"""
        status_colors = {
            "completed": COLORS["success"],
            "in_progress": COLORS["info"],
            "pending": COLORS["text_secondary"],
        }
        color = status_colors.get(status, COLORS["text_secondary"])

        desc_html = (
            f'<p style="margin: 0.5rem 0 0 0; color: {COLORS["text_secondary"]};">{description}</p>'
            if description
            else ""
        )

        st.markdown(
            f"""
        <div class="card" style="border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0;">{title}</h4>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">{time}</span>
            </div>
            {desc_html}
        </div>
        """,
            unsafe_allow_html=True,
        )

    def show_success(self, message: str):
        """Show success message"""
        st.success(f"{get_icon('check')} {message}")

    def show_error(self, message: str):
        """Show error message"""
        st.error(f"{get_icon('error')} {message}")

    def show_warning(self, message: str):
        """Show warning message"""
        st.warning(f"{get_icon('warning')} {message}")

    def show_info(self, message: str):
        """Show info message"""
        st.info(f"{get_icon('info')} {message}")


# Singleton instance
_ui_manager = None


def get_ui_manager() -> ModernUIManager:
    """Get or create UI manager instance"""
    global _ui_manager
    if _ui_manager is None:
        _ui_manager = ModernUIManager()
    return _ui_manager
