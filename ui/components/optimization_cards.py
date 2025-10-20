"""
Optimization Cards Component
Renders optimization suggestion cards with Apply buttons
"""

from ..modern_styles import COLORS, get_icon


def render_optimization_card(
    title: str,
    description: str,
    priority: str,
    impact: str,
    effort: str,
    category: str,
    details: str = "",
) -> str:
    """
    Render a single optimization suggestion card with Apply button

    Args:
        title: Optimization title
        description: Brief description
        priority: High/Medium/Low
        impact: Expected impact description
        effort: Implementation effort
        category: Category (Performance, Security, Quality, etc.)
        details: Additional details/explanation

    Returns:
        HTML string for the card
    """

    # Priority colors
    priority_colors = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}

    # Category icons
    category_icons = {
        "Performance": "⚡",
        "Security": "🔒",
        "Code Quality": "✨",
        "Testing": "🧪",
        "Documentation": "📚",
        "Architecture": "🏗️",
    }

    priority_color = priority_colors.get(priority, COLORS["text_secondary"])
    category_icon = category_icons.get(category, "📋")

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['glass_bg']}, {COLORS['card_bg']});
        backdrop-filter: blur(10px);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.25rem;">{category_icon}</span>
                    <span style="
                        font-size: 0.75rem;
                        font-weight: 600;
                        color: {COLORS['text_secondary']};
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">{category}</span>
                </div>
                <h4 style="
                    font-size: 1.125rem;
                    font-weight: 700;
                    color: {COLORS['text_primary']};
                    margin: 0 0 0.5rem 0;
                ">{title}</h4>
            </div>
            <div style="
                background: {priority_color}20;
                color: {priority_color};
                padding: 0.25rem 0.75rem;
                border-radius: 6px;
                font-size: 0.75rem;
                font-weight: 700;
                white-space: nowrap;
            ">
                {priority} Priority
            </div>
        </div>
        
        <p style="
            color: {COLORS['text_secondary']};
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        ">{description}</p>
        
        <div style="
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        ">
            <div style="
                background: {COLORS['surface']};
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                border-left: 3px solid {COLORS['primary']};
            ">
                <div style="font-size: 0.7rem; color: {COLORS['text_secondary']}; font-weight: 600;">IMPACT</div>
                <div style="font-size: 0.875rem; color: {COLORS['text_primary']}; font-weight: 600; margin-top: 0.25rem;">{impact}</div>
            </div>
            <div style="
                background: {COLORS['surface']};
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                border-left: 3px solid {COLORS['secondary']};
            ">
                <div style="font-size: 0.7rem; color: {COLORS['text_secondary']}; font-weight: 600;">EFFORT</div>
                <div style="font-size: 0.875rem; color: {COLORS['text_primary']}; font-weight: 600; margin-top: 0.25rem;">{effort}</div>
            </div>
        </div>
        
        {f'<p style="color: {COLORS["text_secondary"]}; font-size: 0.875rem; font-style: italic; margin-top: 0.75rem;">{details}</p>' if details else ''}
    </div>
    """

    return card_html
