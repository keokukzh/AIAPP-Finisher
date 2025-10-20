"""
Modern Design System for KI-Projektmanagement-System
Professional color palettes, typography, and styling
"""

# 🎨 Modern Color Palette (Material Design 3.0 inspired)
COLORS = {
    # Primary Colors
    "primary": "#6366f1",  # Indigo
    "primary_light": "#818cf8",
    "primary_dark": "#4f46e5",
    # Secondary Colors
    "secondary": "#ec4899",  # Pink
    "secondary_light": "#f472b6",
    "secondary_dark": "#db2777",
    # Accent Colors
    "accent": "#14b8a6",  # Teal
    "accent_light": "#2dd4bf",
    "accent_dark": "#0d9488",
    # Neutral Colors
    "background": "#f8fafc",
    "surface": "#ffffff",
    "surface_variant": "#f1f5f9",
    # Text Colors
    "text_primary": "#0f172a",
    "text_secondary": "#64748b",
    "text_disabled": "#cbd5e1",
    # Status Colors
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
    "info": "#3b82f6",
    # Dark Mode
    "dark_background": "#0f172a",
    "dark_surface": "#1e293b",
    "dark_text": "#f1f5f9",
}

# 📝 Typography System
TYPOGRAPHY = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_family_mono": "'Fira Code', 'Courier New', monospace",
    "h1": {"size": "2.5rem", "weight": "700", "line_height": "1.2"},
    "h2": {"size": "2rem", "weight": "600", "line_height": "1.3"},
    "h3": {"size": "1.5rem", "weight": "600", "line_height": "1.4"},
    "h4": {"size": "1.25rem", "weight": "500", "line_height": "1.5"},
    "body": {"size": "1rem", "weight": "400", "line_height": "1.6"},
    "small": {"size": "0.875rem", "weight": "400", "line_height": "1.5"},
    "caption": {"size": "0.75rem", "weight": "400", "line_height": "1.4"},
}

# 📦 Spacing System (8px base)
SPACING = {
    "xs": "0.25rem",  # 4px
    "sm": "0.5rem",  # 8px
    "md": "1rem",  # 16px
    "lg": "1.5rem",  # 24px
    "xl": "2rem",  # 32px
    "2xl": "3rem",  # 48px
    "3xl": "4rem",  # 64px
}

# 🎭 Shadows (Material Design)
SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
}

# 🔄 Animations
ANIMATIONS = {
    "fast": "150ms cubic-bezier(0.4, 0, 0.2, 1)",
    "normal": "300ms cubic-bezier(0.4, 0, 0.2, 1)",
    "slow": "500ms cubic-bezier(0.4, 0, 0.2, 1)",
}

# 📐 Border Radius
BORDERS = {
    "sm": "0.375rem",  # 6px
    "md": "0.5rem",  # 8px
    "lg": "0.75rem",  # 12px
    "xl": "1rem",  # 16px
    "full": "9999px",  # Pill shape
}


def get_modern_css() -> str:
    """
    Generate comprehensive modern CSS for Streamlit

    Returns:
        CSS string with all modern styling
    """
    return f"""
    <style>
    /* 🎨 Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap');
    
    /* 🌐 Global Styles */
    :root {{
        --primary: {COLORS['primary']};
        --primary-light: {COLORS['primary_light']};
        --primary-dark: {COLORS['primary_dark']};
        --secondary: {COLORS['secondary']};
        --accent: {COLORS['accent']};
        --background: {COLORS['background']};
        --surface: {COLORS['surface']};
        --text-primary: {COLORS['text_primary']};
        --text-secondary: {COLORS['text_secondary']};
        --success: {COLORS['success']};
        --warning: {COLORS['warning']};
        --error: {COLORS['error']};
        --info: {COLORS['info']};
        
        --shadow-sm: {SHADOWS['sm']};
        --shadow-md: {SHADOWS['md']};
        --shadow-lg: {SHADOWS['lg']};
        --shadow-xl: {SHADOWS['xl']};
        
        --border-radius: {BORDERS['md']};
        --transition: {ANIMATIONS['normal']};
    }}
    
    /* 📱 Base Layout */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: {TYPOGRAPHY['font_family']};
    }}
    
    /* 🎯 Main Container */
    .main {{
        background: var(--background);
        border-radius: 1.5rem;
        margin: 1rem;
        padding: 2rem;
        box-shadow: var(--shadow-2xl);
    }}
    
    /* 📊 Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
        padding: 2rem 1rem;
    }}
    
    [data-testid="stSidebar"] .element-container {{
        color: white !important;
    }}
    
    /* 🎴 Card Components */
    .card {{
        background: var(--surface);
        border-radius: var(--border-radius);
        padding: {SPACING['lg']};
        margin-bottom: {SPACING['md']};
        box-shadow: var(--shadow-md);
        transition: all var(--transition);
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }}
    
    /* 📝 Headers */
    h1, h2, h3, h4, h5, h6 {{
        font-family: {TYPOGRAPHY['font_family']};
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: {SPACING['md']};
    }}
    
    h1 {{
        font-size: {TYPOGRAPHY['h1']['size']};
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    h2 {{
        font-size: {TYPOGRAPHY['h2']['size']};
        color: var(--primary);
    }}
    
    h3 {{
        font-size: {TYPOGRAPHY['h3']['size']};
    }}
    
    /* 🔘 Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: var(--shadow-md);
        transition: all var(--transition);
        cursor: pointer;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* 📊 Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* 📈 Progress Bars */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: {BORDERS['full']};
        height: 12px;
    }}
    
    .stProgress > div > div {{
        background: var(--surface-variant);
        border-radius: {BORDERS['full']};
        height: 12px;
    }}
    
    /* 🎨 Status Pills */
    .status-pill {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: {BORDERS['full']};
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .status-success {{
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
    }}
    
    .status-warning {{
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
    }}
    
    .status-error {{
        background: rgba(239, 68, 68, 0.1);
        color: var(--error);
    }}
    
    .status-info {{
        background: rgba(59, 130, 246, 0.1);
        color: var(--info);
    }}
    
    /* 💬 Chat Interface */
    .chat-message {{
        background: var(--surface);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: var(--shadow-sm);
        animation: slideIn 0.3s ease-out;
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* 🎯 Input Fields */
    .stTextInput > div > div > input {{
        border-radius: var(--border-radius);
        border: 2px solid var(--surface-variant);
        padding: 0.75rem;
        font-size: 1rem;
        transition: all var(--transition);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }}
    
    /* 📋 Selectbox */
    .stSelectbox > div > div {{
        border-radius: var(--border-radius);
        border: 2px solid var(--surface-variant);
    }}
    
    /* 🎲 Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: var(--surface);
        padding: 0.5rem;
        border-radius: var(--border-radius);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all var(--transition);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
    }}
    
    /* 🔔 Alerts/Info boxes */
    .stAlert {{
        border-radius: var(--border-radius);
        border: none;
        box-shadow: var(--shadow-sm);
    }}
    
    /* 📊 DataFrame/Tables */
    .stDataFrame {{
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }}
    
    /* 🎭 Loading Spinner */
    .stSpinner > div {{
        border-color: var(--primary) !important;
    }}
    
    /* 🌙 Dark Mode Support */
    @media (prefers-color-scheme: dark) {{
        :root {{
            --background: {COLORS['dark_background']};
            --surface: {COLORS['dark_surface']};
            --text-primary: {COLORS['dark_text']};
            --text-secondary: #94a3b8;
        }}
    }}
    
    /* 📱 Responsive Design */
    @media (max-width: 768px) {{
        .main {{
            margin: 0.5rem;
            padding: 1rem;
        }}
        
        h1 {{
            font-size: 2rem;
        }}
    }}
    
    /* ✨ Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    .animate-slide-up {{
        animation: slideUp 0.5s ease-out;
    }}
    
    /* 🎯 Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--surface-variant);
        border-radius: {BORDERS['full']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: {BORDERS['full']};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary-light) 100%);
    }}
    
    /* 🎨 Glassmorphism Effect */
    .glass {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* 🔥 Gradient Text */
    .gradient-text {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    /* 💎 Premium Card */
    .premium-card {{
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        backdrop-filter: blur(20px);
        border-radius: 1.5rem;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }}
    </style>
    """


def get_icon(name: str) -> str:
    """
    Get emoji icon for UI elements

    Args:
        name: Icon name

    Returns:
        Emoji icon
    """
    icons = {
        "rocket": "🚀",
        "chart": "📊",
        "settings": "⚙️",
        "file": "📁",
        "code": "💻",
        "check": "✅",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
        "user": "👤",
        "team": "👥",
        "star": "⭐",
        "heart": "❤️",
        "fire": "🔥",
        "lightning": "⚡",
        "brain": "🧠",
        "target": "🎯",
        "trophy": "🏆",
        "medal": "🥇",
        "magic": "✨",
        "crystal": "🔮",
        "gem": "💎",
        "crown": "👑",
    }
    return icons.get(name, "•")
