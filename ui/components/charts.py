"""
Chart Components - Modern visualizations for dashboard

Provides interactive Plotly charts for:
- Language distribution (donut charts)
- Code quality gauges
- Security trend lines
- Complexity heatmaps
"""

import logging
from typing import Any, Dict, List

import plotly.express as px
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


def create_language_donut(languages: Dict[str, int]) -> go.Figure:
    """
    Create donut chart for language distribution

    Args:
        languages: Dict mapping language names to line counts

    Returns:
        Plotly figure object
    """
    if not languages:
        # Empty placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="No language data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="gray"),
        )
        return fig

    # Extract data
    langs = list(languages.keys())
    counts = list(languages.values())

    # Calculate percentages
    total = sum(counts)
    percentages = [f"{(c/total*100):.1f}%" for c in counts]

    # Create donut chart
    fig = px.pie(values=counts, names=langs, hole=0.4, title="Language Distribution")

    # Customize layout
    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>Lines: %{value:,}<br>Share: %{percent}<extra></extra>",
        marker=dict(line=dict(color="white", width=2)),
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


def create_quality_gauge(score: float, max_score: float = 100) -> go.Figure:
    """
    Create circular gauge for code quality score

    Args:
        score: Current quality score (0-100)
        max_score: Maximum possible score

    Returns:
        Plotly gauge figure
    """
    # Normalize score
    normalized_score = min(max(score, 0), max_score)

    # Determine color based on score
    if normalized_score >= 75:
        color = "#00C853"  # Green
        rating = "Excellent"
    elif normalized_score >= 50:
        color = "#FFB800"  # Yellow
        rating = "Good"
    elif normalized_score >= 25:
        color = "#FF6B00"  # Orange
        rating = "Needs Work"
    else:
        color = "#FF0000"  # Red
        rating = "Critical"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=normalized_score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": f"Code Quality<br><span style='font-size:0.8em;color:gray'>{rating}</span>"
            },
            delta={"reference": 75, "increasing": {"color": "green"}},
            gauge={
                "axis": {"range": [None, max_score], "tickwidth": 1, "tickcolor": "darkgray"},
                "bar": {"color": color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 25], "color": "#FFE6E6"},
                    {"range": [25, 50], "color": "#FFF4E6"},
                    {"range": [50, 75], "color": "#FFFBE6"},
                    {"range": [75, 100], "color": "#E6F4EA"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "thickness": 0.75, "value": 90},
            },
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={"color": "darkblue", "family": "Arial"},
    )

    return fig


def create_security_severity_chart(issues: List[Dict[str, Any]]) -> go.Figure:
    """
    Create bar chart showing security issues by severity

    Args:
        issues: List of security issue dicts with 'severity' field

    Returns:
        Plotly bar chart figure
    """
    if not issues:
        fig = go.Figure()
        fig.add_annotation(
            text="No security issues found ✅",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="green", weight="bold"),
        )
        return fig

    # Count by severity
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for issue in issues:
        sev = issue.get("severity", "medium").lower()
        if sev in severity_counts:
            severity_counts[sev] += 1

    # Create bar chart
    severities = list(severity_counts.keys())
    counts = list(severity_counts.values())
    colors = ["#FF0000", "#FF6B00", "#FFB800", "#00C853"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=severities,
                y=counts,
                marker_color=colors,
                text=counts,
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Issues: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Security Issues by Severity",
        xaxis_title="Severity",
        yaxis_title="Number of Issues",
        height=350,
        margin=dict(l=20, r=20, t=60, b=60),
        showlegend=False,
    )

    return fig


def create_complexity_heatmap(complex_files: List[Dict[str, Any]]) -> go.Figure:
    """
    Create heatmap of most complex files

    Args:
        complex_files: List of dicts with 'file', 'complexity', 'loc'

    Returns:
        Plotly heatmap figure
    """
    if not complex_files:
        fig = go.Figure()
        fig.add_annotation(
            text="No complexity data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="gray"),
        )
        return fig

    # Sort by complexity and take top 10
    sorted_files = sorted(complex_files, key=lambda x: x.get("complexity", 0), reverse=True)[:10]

    files = [f["file"].split("/")[-1][:30] for f in sorted_files]  # Short file names
    complexities = [f.get("complexity", 0) for f in sorted_files]
    locs = [f.get("loc", 0) for f in sorted_files]

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=[complexities],
            x=files,
            y=["Complexity"],
            colorscale=[
                [0, "#00C853"],  # Green for low
                [0.5, "#FFB800"],  # Yellow for medium
                [1, "#FF0000"],  # Red for high
            ],
            text=[[f"{c}<br>{loc} LOC" for c, loc in zip(complexities, locs)]],
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate="<b>%{x}</b><br>Complexity: %{z}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Top 10 Most Complex Files",
        xaxis_title="Files",
        height=250,
        margin=dict(l=20, r=20, t=60, b=100),
        xaxis={"tickangle": -45},
    )

    return fig


def create_dependencies_network(dependencies: Dict[str, List[str]]) -> go.Figure:
    """
    Create network graph of dependencies

    Args:
        dependencies: Dict mapping packages to their dependencies

    Returns:
        Plotly network graph figure
    """
    # Simplified version - full implementation would use networkx
    if not dependencies:
        fig = go.Figure()
        fig.add_annotation(
            text="No dependency data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="gray"),
        )
        return fig

    # Count total dependencies
    total_deps = sum(len(deps) if isinstance(deps, list) else 0 for deps in dependencies.values())

    fig = go.Figure()
    fig.add_annotation(
        text=f"Total Dependencies: {total_deps}",
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=20, color="darkblue", family="Arial"),
    )

    # Add top dependencies list
    if isinstance(dependencies, dict):
        top_packages = sorted(
            dependencies.items(),
            key=lambda x: len(x[1]) if isinstance(x[1], list) else 0,
            reverse=True,
        )[:5]

        y_pos = 0.35
        for pkg, deps in top_packages:
            dep_count = len(deps) if isinstance(deps, list) else 0
            fig.add_annotation(
                text=f"{pkg}: {dep_count} dependencies",
                xref="paper",
                yref="paper",
                x=0.5,
                y=y_pos,
                showarrow=False,
                font=dict(size=12, color="gray"),
            )
            y_pos -= 0.06

    fig.update_layout(title="Dependency Overview", height=400, margin=dict(l=20, r=20, t=60, b=20))

    return fig
