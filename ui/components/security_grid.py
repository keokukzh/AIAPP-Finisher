"""
Security Grid Component - Visual display of security issues

Provides color-coded cards for security vulnerabilities with:
- Severity badges (Critical, High, Medium, Low)
- File location and line numbers
- Detailed descriptions
- Fix action buttons
"""

import logging
from typing import Any, Dict, List

import streamlit as st

logger = logging.getLogger(__name__)


# Color scheme for severity levels
SEVERITY_COLORS = {
    "critical": {"bg": "#FFF5F5", "border": "#FF0000", "badge": "#FF0000", "text": "#C00000"},
    "high": {"bg": "#FFF8F0", "border": "#FF6B00", "badge": "#FF6B00", "text": "#E65100"},
    "medium": {"bg": "#FFFBF0", "border": "#FFB800", "badge": "#FFB800", "text": "#F57C00"},
    "low": {"bg": "#F0FFF4", "border": "#00C853", "badge": "#00C853", "text": "#2E7D32"},
}


def render_security_issue_card(issue: Dict[str, Any], key_suffix: str = "") -> str:
    """
    Render single security issue card as HTML

    Args:
        issue: Security issue dict with keys:
            - title: Issue title
            - severity: critical|high|medium|low
            - description: Detailed description
            - file: File path
            - line: Line number
            - cve: Optional CVE reference
        key_suffix: Unique suffix for Streamlit keys

    Returns:
        HTML string for the card
    """
    severity = issue.get("severity", "medium").lower()
    colors = SEVERITY_COLORS.get(severity, SEVERITY_COLORS["medium"])

    title = issue.get("title", "Security Issue")
    description = issue.get("description", "No description available")
    file_path = issue.get("file", "Unknown file")
    line_num = issue.get("line", "?")
    cve = issue.get("cve", "")

    # Truncate long file paths
    if len(file_path) > 50:
        file_path = "..." + file_path[-47:]

    # CVE badge if available
    cve_badge = ""
    if cve:
        cve_badge = f"""
        <span style="
            display: inline-block;
            background: #2196F3;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-left: 8px;
        ">{cve}</span>
        """

    card_html = f"""
    <div style="
        background: {colors['bg']};
        border-left: 4px solid {colors['border']};
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s;
    " onmouseover="this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'"
       onmouseout="this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">
        
        <!-- Header -->
        <div style="display: flex; align-items: center; margin-bottom: 12px;">
            <span style="
                background: {colors['badge']};
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">{severity}</span>
            {cve_badge}
        </div>
        
        <!-- Title -->
        <h4 style="
            color: {colors['text']};
            margin: 0 0 8px 0;
            font-size: 1.1rem;
            font-weight: 600;
        ">{title}</h4>
        
        <!-- Description -->
        <p style="
            color: #424242;
            margin: 0 0 12px 0;
            font-size: 0.9rem;
            line-height: 1.5;
        ">{description}</p>
        
        <!-- Metadata -->
        <div style="
            display: flex;
            gap: 16px;
            color: #757575;
            font-size: 0.85rem;
            padding-top: 8px;
            border-top: 1px solid rgba(0,0,0,0.1);
        ">
            <span>📁 {file_path}</span>
            <span>📍 Line {line_num}</span>
        </div>
    </div>
    """

    return card_html


def render_security_grid(
    issues: List[Dict[str, Any]], filters: Dict[str, Any] = None, show_fix_buttons: bool = True
):
    """
    Render grid of security issues with filters

    Args:
        issues: List of security issue dicts
        filters: Optional dict with filter settings:
            - severity: List of severities to show
            - search: Search term
        show_fix_buttons: Whether to show "Fix Now" buttons
    """
    if not issues:
        st.success("✅ No security issues found! Your code looks secure.")
        return

    # Apply filters
    filtered_issues = issues

    if filters:
        # Severity filter
        if "severity" in filters and filters["severity"]:
            filtered_issues = [
                issue
                for issue in filtered_issues
                if issue.get("severity", "").lower() in [s.lower() for s in filters["severity"]]
            ]

        # Search filter
        if "search" in filters and filters["search"]:
            search_term = filters["search"].lower()
            filtered_issues = [
                issue
                for issue in filtered_issues
                if search_term in issue.get("title", "").lower()
                or search_term in issue.get("description", "").lower()
                or search_term in issue.get("file", "").lower()
            ]

    if not filtered_issues:
        st.info("No issues match your filters")
        return

    # Group by severity
    severity_groups = {"critical": [], "high": [], "medium": [], "low": []}

    for issue in filtered_issues:
        severity = issue.get("severity", "medium").lower()
        if severity in severity_groups:
            severity_groups[severity].append(issue)

    # Display statistics
    st.markdown(
        f"""
    <div style="
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        padding: 12px;
        background: #F5F5F5;
        border-radius: 8px;
    ">
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #FF0000;">
                {len(severity_groups['critical'])}
            </div>
            <div style="font-size: 0.85rem; color: #757575;">Critical</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #FF6B00;">
                {len(severity_groups['high'])}
            </div>
            <div style="font-size: 0.85rem; color: #757575;">High</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #FFB800;">
                {len(severity_groups['medium'])}
            </div>
            <div style="font-size: 0.85rem; color: #757575;">Medium</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 600; color: #00C853;">
                {len(severity_groups['low'])}
            </div>
            <div style="font-size: 0.85rem; color: #757575;">Low</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Render issues by severity
    for severity in ["critical", "high", "medium", "low"]:
        issues_in_group = severity_groups[severity]

        if not issues_in_group:
            continue

        # Section header
        severity_labels = {
            "critical": ("🔴", "Critical Issues", "Fix immediately!"),
            "high": ("🟠", "High Priority", "Fix this week"),
            "medium": ("🟡", "Medium Priority", "Address soon"),
            "low": ("🟢", "Low Priority", "Review when possible"),
        }

        icon, label, subtitle = severity_labels[severity]

        with st.expander(
            f"{icon} {label} ({len(issues_in_group)})", expanded=(severity in ["critical", "high"])
        ):
            st.caption(subtitle)

            for i, issue in enumerate(issues_in_group):
                # Render card
                st.markdown(
                    render_security_issue_card(issue, f"{severity}_{i}"), unsafe_allow_html=True
                )

                # Fix button
                if show_fix_buttons:
                    col1, col2, col3 = st.columns([1, 1, 3])
                    with col1:
                        if st.button("🔧 Fix Now", key=f"fix_{severity}_{i}"):
                            st.session_state["fix_preview_issue"] = issue
                            st.rerun()
                    with col2:
                        if st.button("ℹ️ Details", key=f"details_{severity}_{i}"):
                            with st.expander("📋 Issue Details", expanded=True):
                                st.markdown(f"**File:** `{issue.get('file', 'Unknown')}`")
                                st.markdown(f"**Line:** {issue.get('line', '?')}")
                                st.markdown(f"**Severity:** {issue.get('severity', 'Unknown')}")
                                if "cve" in issue:
                                    st.markdown(f"**CVE:** {issue.get('cve')}")
                                st.markdown("---")
                                st.markdown(issue.get("description", "No description"))
                                if "recommendation" in issue:
                                    st.markdown("**Recommendation:**")
                                    st.info(issue["recommendation"])


def render_security_filter_bar():
    """
    Render filter controls for security issues

    Returns:
        Dict with filter settings
    """
    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input(
            "🔍 Search issues",
            placeholder="Search by title, description, or file...",
            key="security_search",
        )

    with col2:
        severity_filter = st.multiselect(
            "Severity",
            options=["Critical", "High", "Medium", "Low"],
            default=["Critical", "High"],
            key="severity_filter",
        )

    return {"search": search, "severity": severity_filter}


def get_security_summary(issues: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Get summary statistics for security issues

    Args:
        issues: List of security issues

    Returns:
        Dict with counts by severity and total
    """
    summary = {"total": len(issues), "critical": 0, "high": 0, "medium": 0, "low": 0}

    for issue in issues:
        severity = issue.get("severity", "medium").lower()
        if severity in summary:
            summary[severity] += 1

    return summary
