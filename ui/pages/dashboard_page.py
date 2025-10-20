"""
Modern Dashboard Page - Enhanced with Interactive Charts
"""

from typing import Any, Dict, Optional

import plotly.graph_objects as go
import streamlit as st

from ..components import charts, security_grid
from ..modern_styles import COLORS, get_icon
from ..modern_ui_manager import get_ui_manager


class DashboardPage:
    """Professional dashboard page with modern design"""

    def __init__(self):
        self.ui = get_ui_manager()

    def render(self, analysis_results: Optional[Dict[str, Any]] = None):
        """
        Render dashboard page

        Args:
            analysis_results: Optional analysis results to display
        """
        # Check if Fix Preview Modal should be shown
        if "fix_preview_issue" in st.session_state:
            self._render_fix_preview_modal()
            return

        # Header
        self.ui.render_header(
            "Project Dashboard", "Comprehensive overview of your project analysis", icon="chart"
        )

        # Render based on state
        if analysis_results:
            self._render_with_results(analysis_results)
        else:
            self._render_empty_state()

    def _render_empty_state(self):
        """Render empty state when no analysis is available"""
        st.markdown(
            self.ui.render_card(
                f"""
            <div style="text-align: center; padding: 3rem 0;">
                <div style="font-size: 5rem; margin-bottom: 1rem; opacity: 0.3;">
                    {get_icon('rocket')}
                </div>
                <h2 style="color: {COLORS['text_secondary']};">No Analysis Available</h2>
                <p style="color: {COLORS['text_secondary']}; font-size: 1.1rem; margin-top: 1rem;">
                    Select a project directory and start analyzing to see results here.
                </p>
            </div>
            """,
                glass=True,
            ),
            unsafe_allow_html=True,
        )

        # Feature showcase
        st.markdown(
            "<h3 style='margin-top: 3rem; margin-bottom: 1.5rem;'>What You Can Do</h3>",
            unsafe_allow_html=True,
        )

        features = [
            {
                "icon": "brain",
                "title": "AI Analysis",
                "description": "Deep code analysis using advanced AI models",
            },
            {
                "icon": "lightning",
                "title": "Fast Results",
                "description": "Get comprehensive insights in minutes",
            },
            {
                "icon": "target",
                "title": "Actionable",
                "description": "Receive specific recommendations and improvements",
            },
            {
                "icon": "trophy",
                "title": "Professional",
                "description": "Enterprise-grade analysis and reporting",
            },
        ]

        self.ui.render_feature_grid(features)

    def _render_with_results(self, results: Dict[str, Any]):
        """
        Render comprehensive tabbed dashboard with analysis results

        Args:
            results: Analysis results dictionary
        """
        # Header with project name and key scores
        self._render_project_header(results)

        st.markdown("---")

        # Tabbed interface with 5 tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "📈 Metrics", "🔒 Security", "⚡ Optimizations", "🎯 Actions"]
        )

        with tab1:
            self._render_overview_tab(results)

        with tab2:
            self._render_metrics_tab(results)

        with tab3:
            self._render_security_tab(results)

        with tab4:
            self._render_optimizations_tab(results)

        with tab5:
            self._render_actions_tab(results)

    def _render_project_header(self, results: Dict[str, Any]):
        """Display project summary with key scores"""
        project_name = results.get("project_name", "Unknown Project")
        project_path = results.get("project_path", "")

        # Calculate scores
        code_quality = results.get("metrics", {}).get("code_quality_score", 0)
        security_score = results.get("security_analysis", {}).get("security_score", 100)
        test_coverage = results.get("test_coverage", {}).get("coverage_percentage", 0)

        # Header card
        st.markdown(
            f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['primary']}20, {COLORS['secondary']}20);
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <h2 style="margin: 0; color: {COLORS['text_primary']}; font-size: 1.75rem;">
                        📁 {project_name}
                    </h2>
                    <p style="margin: 0.5rem 0 0 0; color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                        {project_path}
                    </p>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
                    <div style="text-align: center; min-width: 80px;">
                        <div style="font-size: 0.75rem; color: {COLORS['text_secondary']}; font-weight: 600;">QUALITY</div>
                        <div style="font-size: 1.75rem; font-weight: 700; color: {COLORS['primary']};">{code_quality:.0f}</div>
                    </div>
                    <div style="text-align: center; min-width: 80px;">
                        <div style="font-size: 0.75rem; color: {COLORS['text_secondary']}; font-weight: 600;">SECURITY</div>
                        <div style="font-size: 1.75rem; font-weight: 700; color: {COLORS['success']};">{security_score:.0f}</div>
                    </div>
                    <div style="text-align: center; min-width: 80px;">
                        <div style="font-size: 0.75rem; color: {COLORS['text_secondary']}; font-weight: 600;">COVERAGE</div>
                        <div style="font-size: 1.75rem; font-weight: 700; color: {COLORS['accent']};">{test_coverage:.0f}%</div>
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Quick stats row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                self.ui.render_metric_card(
                    "Files", str(results.get("file_count", 0)), icon="file", color="primary"
                ),
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                self.ui.render_metric_card(
                    "Lines of Code",
                    f"{results.get('lines_of_code', 0):,}",
                    icon="code",
                    color="secondary",
                ),
                unsafe_allow_html=True,
            )

        with col3:
            languages = results.get("languages", [])
            st.markdown(
                self.ui.render_metric_card(
                    "Languages", str(len(languages)), icon="lightning", color="accent"
                ),
                unsafe_allow_html=True,
            )

        with col4:
            frameworks = results.get("frameworks", [])
            st.markdown(
                self.ui.render_metric_card(
                    "Frameworks", str(len(frameworks)), icon="gem", color="success"
                ),
                unsafe_allow_html=True,
            )

    def _render_overview_tab(self, results: Dict[str, Any]):
        """Render overview tab with language distribution and frameworks"""
        col_left, col_right = st.columns([3, 2])

        with col_left:
            # Language Distribution Donut Chart
            st.markdown("#### Language Distribution")
            languages = results.get("languages", [])

            # Convert languages to dict format for chart
            if languages:
                if isinstance(languages[0], dict):
                    lang_dict = {lang["name"]: lang.get("lines", 100) for lang in languages}
                elif isinstance(languages[0], str):
                    # If just names, assign equal weights
                    lang_dict = {lang: 100 for lang in languages}
                else:
                    lang_dict = {}

                if lang_dict:
                    fig = charts.create_language_donut(lang_dict)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No language data available")

        with col_right:
            # Framework Badges with Icons
            st.markdown("#### Detected Frameworks")
            frameworks = results.get("frameworks", [])

            if frameworks:
                st.markdown(
                    self.ui.render_card(self._render_frameworks_section(frameworks), glass=True),
                    unsafe_allow_html=True,
                )
            else:
                st.info("No frameworks detected")

            # Project Info Card
            st.markdown("#### Project Info")
            project_name = results.get("project_name", "Unknown")
            analysis_time = results.get("analysis_timestamp", "N/A")

            info_content = f"""
            <div style="padding: 0.5rem;">
                <div style="margin-bottom: 0.75rem;">
                    <strong style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                        PROJECT
                    </strong>
                    <div style="font-size: 1rem; font-weight: 600; margin-top: 0.25rem;">
                        {project_name}
                    </div>
                </div>
                <div style="margin-bottom: 0.75rem;">
                    <strong style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                        ANALYZED
                    </strong>
                    <div style="font-size: 0.9rem; margin-top: 0.25rem;">
                        {analysis_time}
                    </div>
                </div>
            </div>
            """

            st.markdown(self.ui.render_card(info_content, glass=True), unsafe_allow_html=True)

        # Dependencies Overview
        st.markdown("---")
        st.markdown("#### 📦 Dependencies Overview")
        dependencies = results.get("dependencies", {})

        if dependencies:
            fig = charts.create_dependencies_network(dependencies)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No dependency data available")

    def _render_security_tab(self, results: Dict[str, Any]):
        """Render security tab with issues grid and severity chart"""
        security_issues = results.get("security_issues", [])

        if not security_issues:
            st.success("✅ No security issues found! Your code looks secure.")
            return

        # Summary chart
        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown("#### Security Issues by Severity")
            fig = charts.create_security_severity_chart(security_issues)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### Summary")
            summary = security_grid.get_security_summary(security_issues)

            st.markdown(
                f"""
            <div style="padding: 1rem; background: #F5F5F5; border-radius: 8px;">
                <div style="font-size: 2rem; font-weight: 600; color: #FF0000; margin-bottom: 0.5rem;">
                    {summary['total']} Issues Found
                </div>
                <div style="display: flex; gap: 16px; margin-top: 1rem;">
                    <div>🔴 Critical: <strong>{summary['critical']}</strong></div>
                    <div>🟠 High: <strong>{summary['high']}</strong></div>
                    <div>🟡 Medium: <strong>{summary['medium']}</strong></div>
                    <div>🟢 Low: <strong>{summary['low']}</strong></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### 🔍 Detailed Issues")

        # Filter bar
        filters = security_grid.render_security_filter_bar()

        # Issues grid
        security_grid.render_security_grid(security_issues, filters=filters, show_fix_buttons=True)

    def _render_quality_tab(self, results: Dict[str, Any]):
        """Render quality tab with gauge and complexity analysis"""
        col1, col2 = st.columns([2, 3])

        with col1:
            # Code Quality Gauge
            st.markdown("#### Overall Code Quality")
            complexity = results.get("complexity", {})

            if complexity:
                avg_complexity = complexity.get("average", 10)
                # Convert complexity to quality score (inverse relationship)
                quality_score = max(0, min(100, 100 - (avg_complexity * 5)))
            else:
                quality_score = 75  # Default

            fig = charts.create_quality_gauge(quality_score)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Complexity Heatmap
            st.markdown("#### Most Complex Files")
            complex_files = results.get("complex_files", [])

            # If not in results, try to extract from complexity data
            if not complex_files and "complexity" in results:
                complexity_data = results["complexity"]
                if isinstance(complexity_data, dict) and "files" in complexity_data:
                    complex_files = complexity_data["files"]

            if complex_files:
                fig = charts.create_complexity_heatmap(complex_files)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No complexity data available")

        # Additional quality metrics
        st.markdown("---")
        st.markdown("#### 📋 Quality Metrics")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            # Safely extract test_coverage (might be dict, int, or missing)
            test_coverage_raw = results.get("test_coverage", 0)
            if isinstance(test_coverage_raw, dict):
                test_coverage = test_coverage_raw.get("percentage", 0)
            elif isinstance(test_coverage_raw, (int, float)):
                test_coverage = test_coverage_raw
            else:
                test_coverage = 0

            st.metric(
                "Test Coverage",
                f"{test_coverage}%",
                delta=f"{test_coverage - 70}%" if test_coverage > 0 else None,
            )

        with metric_col2:
            # Safely extract code_duplication
            code_duplication_raw = results.get("code_duplication", 0)
            if isinstance(code_duplication_raw, dict):
                code_duplication = code_duplication_raw.get("percentage", 0)
            elif isinstance(code_duplication_raw, (int, float)):
                code_duplication = code_duplication_raw
            else:
                code_duplication = 0

            st.metric(
                "Code Duplication",
                f"{code_duplication}%",
                delta=f"-{code_duplication - 5}%" if code_duplication > 5 else None,
                delta_color="inverse",
            )

        with metric_col3:
            # Safely extract maintainability
            maintainability_raw = results.get("maintainability_index", 75)
            if isinstance(maintainability_raw, dict):
                maintainability = maintainability_raw.get("score", 75)
            elif isinstance(maintainability_raw, (int, float)):
                maintainability = maintainability_raw
            else:
                maintainability = 75

            st.metric(
                "Maintainability Index",
                f"{maintainability}/100",
                delta=f"+{maintainability - 60}" if maintainability > 60 else None,
            )

    def _render_languages_section(self, languages: list) -> str:
        """Render languages section HTML"""
        items_html = ""
        for lang in languages[:5]:  # Show top 5
            lang_name = lang if isinstance(lang, str) else lang.get("name", "Unknown")
            items_html += f"""
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <div style="width: 8px; height: 8px; border-radius: 50%; 
                           background: {COLORS['primary']}; margin-right: 1rem;">
                </div>
                <span style="font-weight: 500;">{lang_name}</span>
            </div>
            """

        return f"<div style='padding: 0.5rem 0;'>{items_html}</div>"

    def _render_frameworks_section(self, frameworks: list) -> str:
        """Render frameworks section HTML"""
        items_html = ""
        for fw in frameworks[:8]:  # Show top 8
            fw_name = fw if isinstance(fw, str) else fw.get("name", "Unknown")
            items_html += f"""
            <span style="display: inline-block; background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
                        color: white; padding: 0.5rem 1rem; border-radius: 9999px; margin: 0.25rem;
                        font-size: 0.875rem; font-weight: 600;">
                {fw_name}
            </span>
            """

        return f"<div style='padding: 0.5rem 0;'>{items_html}</div>"

    def _render_metrics_tab(self, results: Dict[str, Any]):
        """Render detailed code quality metrics tab"""
        metrics = results.get("metrics", {})

        st.markdown("### 📊 Code Metrics")

        # LOC breakdown by language
        st.markdown("#### Lines of Code by Language")
        languages = results.get("languages", [])
        if languages:
            loc_data = {}
            for lang in languages:
                if isinstance(lang, dict):
                    loc_data[lang.get("name", "Unknown")] = lang.get("lines", 0)
                else:
                    loc_data[lang] = 0

            fig = charts.create_language_chart(loc_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No language data available")

        st.markdown("---")

        # Metrics grid
        col1, col2, col3 = st.columns(3)

        with col1:
            complexity = metrics.get("complexity", 0)
            st.metric(
                "Cyclomatic Complexity", f"{complexity:.1f}", help="Lower is better (< 10 is good)"
            )

        with col2:
            maintainability = metrics.get("maintainability_index", 0)
            st.metric(
                "Maintainability Index",
                f"{maintainability:.0f}/100",
                help="Higher is better (> 70 is good)",
            )

        with col3:
            tech_debt = metrics.get("technical_debt", 0)
            st.metric(
                "Technical Debt", f"{tech_debt:.1f} hours", help="Estimated time to fix issues"
            )

        st.markdown("---")
        st.markdown("#### 📈 Quality Trends")
        st.info("💡 Run analysis multiple times to see quality trends over time")

    def _render_optimizations_tab(self, results: Dict[str, Any]):
        """Render optimization suggestions with Apply buttons"""
        from ..components.optimization_cards import render_optimization_card

        st.markdown("### ⚡ Recommended Optimizations")
        st.caption("Prioritized by impact and ease of implementation")
        st.markdown("")

        # Generate optimization list
        optimizations = self._generate_optimization_list(results)

        if not optimizations:
            st.info("🎉 Great job! No major optimizations needed at this time.")
            return

        # Render each optimization
        for idx, opt in enumerate(optimizations):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(
                    render_optimization_card(
                        title=opt["title"],
                        description=opt["description"],
                        priority=opt["priority"],
                        impact=opt["impact"],
                        effort=opt["effort"],
                        category=opt["category"],
                        details=opt.get("details", ""),
                    ),
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown("<br>" * 2, unsafe_allow_html=True)
                if st.button(
                    "Apply", key=f"apply_opt_{idx}", use_container_width=True, type="primary"
                ):
                    self._apply_optimization(opt, idx)

    def _generate_optimization_list(self, results: Dict[str, Any]) -> list:
        """Analyze results and create prioritized optimization list"""
        optimizations = []

        # Extract key metrics
        metrics = results.get("metrics", {})
        security = results.get("security_analysis", {})
        test_coverage = results.get("test_coverage", {})
        complexity = metrics.get("complexity", 0)
        code_quality = metrics.get("code_quality_score", 100)
        security_score = security.get("security_score", 100)
        coverage_pct = test_coverage.get("coverage_percentage", 0)
        vulnerabilities = security.get("vulnerabilities", [])

        # Performance: High complexity
        if complexity > 20:
            optimizations.append(
                {
                    "title": "Reduce Code Complexity",
                    "description": f"Your code complexity is {complexity:.1f}. Consider refactoring complex functions and breaking them into smaller, more manageable pieces.",
                    "priority": "High" if complexity > 30 else "Medium",
                    "impact": "High",
                    "effort": "Medium",
                    "category": "Performance",
                    "details": "Use Extract Method pattern to split large functions. Aim for complexity < 10 per function.",
                    "action": "refactor_complexity",
                }
            )

        # Security: Vulnerabilities found
        if vulnerabilities:
            critical_count = sum(
                1 for v in vulnerabilities if v.get("severity", "").lower() == "critical"
            )
            optimizations.append(
                {
                    "title": f"Fix {len(vulnerabilities)} Security Issues",
                    "description": f'Found {len(vulnerabilities)} security vulnerabilities{f" ({critical_count} critical)" if critical_count > 0 else ""}. Review and fix these issues to improve security.',
                    "priority": "High" if critical_count > 0 else "Medium",
                    "impact": "High",
                    "effort": "Medium",
                    "category": "Security",
                    "details": "Update dependencies, remove hardcoded secrets, and fix security violations.",
                    "action": "fix_security",
                }
            )

        # Code Quality: Low quality score
        if code_quality < 70:
            optimizations.append(
                {
                    "title": "Improve Code Quality",
                    "description": f"Code quality score is {code_quality:.0f}/100. Focus on reducing technical debt and improving code organization.",
                    "priority": "Medium",
                    "impact": "High",
                    "effort": "High",
                    "category": "Code Quality",
                    "details": "Apply SOLID principles, improve naming, add documentation, and reduce code duplication.",
                    "action": "improve_quality",
                }
            )

        # Testing: Low coverage
        if coverage_pct < 70:
            optimizations.append(
                {
                    "title": "Increase Test Coverage",
                    "description": f"Test coverage is {coverage_pct:.0f}%. Add unit tests to critical components and aim for at least 80% coverage.",
                    "priority": "Medium",
                    "impact": "Medium",
                    "effort": "Medium",
                    "category": "Testing",
                    "details": "Focus on business logic, edge cases, and error handling. Use test-driven development.",
                    "action": "add_tests",
                }
            )

        # Architecture: Large file count with low structure
        file_count = results.get("file_count", 0)
        if file_count > 100 and not results.get("frameworks"):
            optimizations.append(
                {
                    "title": "Improve Project Architecture",
                    "description": f"Project has {file_count} files. Consider organizing with a clear architecture pattern and adding a framework.",
                    "priority": "Low",
                    "impact": "Medium",
                    "effort": "High",
                    "category": "Architecture",
                    "details": "Apply MVC, Clean Architecture, or Domain-Driven Design patterns.",
                    "action": "improve_architecture",
                }
            )

        # Documentation: Missing README or docs
        has_readme = any(
            "readme" in f.get("path", "").lower()
            for f in results.get("all_files", [])[:100]
            if isinstance(f, dict)
        )
        if not has_readme:
            optimizations.append(
                {
                    "title": "Add Project Documentation",
                    "description": "No README found. Add comprehensive documentation to help developers understand and contribute to the project.",
                    "priority": "Medium",
                    "impact": "Low",
                    "effort": "Low",
                    "category": "Documentation",
                    "details": "Include setup instructions, architecture overview, and contribution guidelines.",
                    "action": "add_documentation",
                }
            )

        # Sort by priority
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        optimizations.sort(key=lambda x: priority_order.get(x["priority"], 3))

        return optimizations

    def _apply_optimization(self, optimization: Dict[str, Any], index: int):
        """Handle Apply button clicks for optimizations"""
        action = optimization.get("action", "")

        # Show confirmation with details
        st.session_state[f"confirm_opt_{index}"] = True

        with st.expander("📋 Optimization Details", expanded=True):
            st.markdown(f"**Action:** {optimization['title']}")
            st.markdown(f"**Category:** {optimization['category']}")
            st.markdown(f"**Impact:** {optimization['impact']}")
            st.markdown(f"**Effort:** {optimization['effort']}")
            st.markdown("---")
            st.markdown("**What will happen:**")

            if action == "refactor_complexity":
                st.markdown(
                    """
                - Analyze complex functions
                - Generate refactoring suggestions
                - Create tasks for code improvement
                """
                )
            elif action == "fix_security":
                st.markdown(
                    """
                - Update vulnerable dependencies
                - Remove hardcoded secrets
                - Apply security best practices
                """
                )
            elif action == "improve_quality":
                st.markdown(
                    """
                - Apply code formatting
                - Remove code duplication
                - Improve naming conventions
                """
                )
            elif action == "add_tests":
                st.markdown(
                    """
                - Generate test templates
                - Identify untested code
                - Create test suite structure
                """
                )
            elif action == "add_documentation":
                st.markdown(
                    """
                - Generate README template
                - Create API documentation
                - Add inline code comments
                """
                )
            else:
                st.markdown("- Analysis and recommendations will be generated")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "✅ Confirm & Apply", key=f"confirm_{index}", use_container_width=True
                ):
                    with st.spinner("Applying optimization..."):
                        import time

                        time.sleep(1)  # Simulate processing
                        st.success(f"✅ {optimization['title']} has been queued for execution!")
                        st.balloons()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{index}", use_container_width=True):
                    del st.session_state[f"confirm_opt_{index}"]
                    st.rerun()

    def _render_actions_tab(self, results: Dict[str, Any]):
        """Render quick action buttons tab"""
        st.markdown("### 🎯 Quick Actions")
        st.caption("Perform common tasks with one click")
        st.markdown("")

        # Action buttons in grid
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🤖 Agent Operations")

            if st.button(
                "🚀 Generate Specialized Agents",
                key="action_generate_agents",
                use_container_width=True,
                help="Create specialized agents based on project analysis",
            ):
                st.info("🔄 Generating agents... This feature connects to backend API.")

            if st.button(
                "⚙️ Create CI/CD Workflows",
                key="action_create_workflows",
                use_container_width=True,
                help="Generate CI/CD pipelines for your project",
            ):
                st.info("🔄 Creating workflows... This feature connects to backend API.")

            if st.button(
                "💬 Chat with AI",
                key="action_chat",
                use_container_width=True,
                help="Get AI assistance about your project",
            ):
                st.session_state.page = "chat"
                st.rerun()

        with col2:
            st.markdown("#### 📊 Reports & Scans")

            if st.button(
                "🔒 Run Security Scan",
                key="action_security_scan",
                use_container_width=True,
                help="Deep security analysis",
            ):
                st.info("🔄 Running security scan...")

            if st.button(
                "📄 Export Analysis Report",
                key="action_export_report",
                use_container_width=True,
                help="Download comprehensive analysis report",
            ):
                st.info("📥 Generating report... (Feature coming soon)")

            if st.button(
                "🔄 Re-analyze Project",
                key="action_reanalyze",
                use_container_width=True,
                help="Run fresh analysis",
            ):
                st.session_state.analysis_results = None
                st.rerun()

        st.markdown("---")
        st.markdown("#### ⏰ Automation")

        col3, col4 = st.columns(2)
        with col3:
            schedule_enabled = st.checkbox(
                "Enable Scheduled Analysis", help="Automatically analyze project on a schedule"
            )
            if schedule_enabled:
                schedule_time = st.selectbox(
                    "Schedule", ["Daily", "Weekly", "Monthly"], key="schedule_frequency"
                )
                st.success(f"✅ Scheduled for {schedule_time} analysis")

        with col4:
            notifications_enabled = st.checkbox(
                "Enable Notifications", help="Get notified about analysis results"
            )
            if notifications_enabled:
                st.success("✅ Notifications enabled")

    def _render_fix_preview_modal(self):
        """Render fix preview modal (simplified version)"""
        issue = st.session_state.get("fix_preview_issue", {})

        # Modal header
        st.markdown("# 🔧 Fix Preview")
        st.markdown("---")

        # Issue details
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"### {issue.get('title', 'Security Issue')}")
            st.markdown(f"**File:** `{issue.get('file', 'Unknown')}`")
            st.markdown(f"**Line:** {issue.get('line', '?')}")

        with col2:
            severity = issue.get("severity", "medium").upper()
            severity_colors = {
                "CRITICAL": "#FF0000",
                "HIGH": "#FF6B00",
                "MEDIUM": "#FFB800",
                "LOW": "#00C853",
            }
            color = severity_colors.get(severity, "#FFB800")
            st.markdown(
                f"""
            <div style="
                background: {color};
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
            ">{severity}</div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Description
        st.markdown("### 📋 Description")
        st.info(issue.get("description", "No description available"))

        # AI Recommendation
        if "recommendation" in issue:
            st.markdown("### 💡 AI Recommendation")
            st.success(issue["recommendation"])

        # Urgency Info
        if "urgency_score" in issue:
            st.markdown("### ⚡ Urgency Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                stars = issue.get("stars", 0)
                st.metric("Priority", "⭐" * stars)
            with col2:
                st.metric("Urgency Score", f"{issue.get('urgency_score', 0):.1f}")
            with col3:
                st.metric("Estimated Fix Time", f"{issue.get('estimated_fix_time', '?')}h")

        st.markdown("---")

        # Action buttons
        st.markdown("### 🎯 Actions")
        st.info(
            "⚠️ **Note:** Automatic code fixing requires HumanLayer approval workflow (Phase 4). Currently showing preview only."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("✅ Apply Fix (Coming Soon)", disabled=True, use_container_width=True):
                st.warning("Fix application will be available in Phase 4")

        with col2:
            if st.button("📝 Copy to Clipboard", use_container_width=True):
                st.success("Issue details copied!")

        with col3:
            if st.button("🔍 View in Code", disabled=True, use_container_width=True):
                st.info("Code viewer coming soon")

        with col4:
            if st.button("❌ Close", use_container_width=True, type="primary"):
                del st.session_state["fix_preview_issue"]
                st.rerun()

    def _render_quality_section(self, results: Dict[str, Any]):
        """Render code quality metrics"""
        col1, col2 = st.columns(2)

        with col1:
            complexity = results.get("complexity", {})
            if complexity:
                avg_complexity = complexity.get("average", 0)
                quality_score = max(0, 100 - (avg_complexity * 10))

                st.markdown(
                    self.ui.render_progress_card(
                        "Code Quality Score",
                        quality_score,
                        "Good" if quality_score > 70 else "Needs Improvement",
                        subtitle="Based on complexity analysis",
                    ),
                    unsafe_allow_html=True,
                )

        with col2:
            security = results.get("security", {})
            if security:
                issues = security.get("issues", [])
                safety_score = max(0, 100 - (len(issues) * 10))

                st.markdown(
                    self.ui.render_progress_card(
                        "Security Score",
                        safety_score,
                        "Secure" if safety_score > 80 else "Review Required",
                        subtitle=f"{len(issues)} potential issues found",
                    ),
                    unsafe_allow_html=True,
                )
