"""
Optimization Engine
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List

from llm.model_manager import ModelManager

logger = logging.getLogger(__name__)


class OptimizationEngine:
    """Continuous improvement and optimization engine"""

    def __init__(self, model_manager=None):
        """
        Initialize optimization engine

        Args:
            model_manager: Optional ModelManager instance to use. If None, creates new one.
        """
        self.llm_manager = model_manager if model_manager else ModelManager()
        self.optimization_history = []
        self.active_suggestions = []

    async def analyze_and_optimize(
        self, analysis_results: Dict[str, Any], current_performance: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Analyze project and generate optimization suggestions"""

        # Generate optimization suggestions
        suggestions = await self._generate_optimization_suggestions(
            analysis_results, current_performance
        )

        # Prioritize suggestions
        prioritized_suggestions = self._prioritize_suggestions(suggestions)

        # Create optimization plan
        optimization_plan = await self._create_optimization_plan(prioritized_suggestions)

        result = {
            "timestamp": datetime.now().isoformat(),
            "suggestions": prioritized_suggestions,
            "optimization_plan": optimization_plan,
            "estimated_impact": self._calculate_impact_score(prioritized_suggestions),
        }

        self.optimization_history.append(result)
        return result

    async def _generate_optimization_suggestions(
        self, analysis_results: Dict[str, Any], current_performance: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Generate optimization suggestions using LLM"""

        # Create a summary of the analysis for the LLM
        summary = self._create_analysis_summary(analysis_results)

        prompt = f"""
        Analyze the following project and generate specific optimization suggestions:
        
        Project Analysis Summary:
        {summary}
        
        Current Performance: {current_performance or "Not available"}
        
        Focus on these areas:
        1. Code Quality (complexity, maintainability, best practices)
        2. Performance (bottlenecks, efficiency, resource usage)
        3. Security (vulnerabilities, outdated dependencies, best practices)
        4. Architecture (scalability, modularity, design patterns)
        5. Testing (coverage, quality, automation)
        6. Documentation (completeness, clarity, maintenance)
        7. DevOps (CI/CD, deployment, monitoring)
        
        For each suggestion, provide:
        - Title
        - Description
        - Category
        - Priority (High/Medium/Low)
        - Estimated effort (hours)
        - Expected impact (High/Medium/Low)
        - Implementation steps
        
        Return as a structured list of suggestions.
        """

        try:
            response = await self.llm_manager.generate_response(prompt)

            # Parse response into structured suggestions
            suggestions = self._parse_suggestions(response)
            return suggestions
        except Exception as e:
            logger.error(f"❌ Error generating LLM suggestions: {e}")
            # Return fallback suggestions based on analysis
            return self._generate_fallback_suggestions(analysis_results)

    def _parse_suggestions(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured suggestions"""
        # This is a simplified parser - in production, you'd want more robust parsing
        suggestions = []

        # Split by suggestion markers (this is a basic implementation)
        lines = response.split("\n")
        current_suggestion = {}

        for line in lines:
            line = line.strip()
            if line.startswith("**") and line.endswith("**"):
                if current_suggestion:
                    suggestions.append(current_suggestion)
                current_suggestion = {"title": line.strip("*")}
            elif line.startswith("- **") and ":**" in line:
                key, value = line.split(":**", 1)
                key = key.replace("- **", "").strip()
                current_suggestion[key.lower().replace(" ", "_")] = value.strip()

        if current_suggestion:
            suggestions.append(current_suggestion)

        return suggestions

    def _prioritize_suggestions(self, suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize suggestions based on impact and effort"""

        def priority_score(suggestion):
            priority_map = {"High": 3, "Medium": 2, "Low": 1}
            impact_map = {"High": 3, "Medium": 2, "Low": 1}

            priority = priority_map.get(suggestion.get("priority", "Medium"), 2)
            impact = impact_map.get(suggestion.get("expected_impact", "Medium"), 2)
            effort = suggestion.get("estimated_effort", 0)

            # Higher score = higher priority
            # Consider impact, priority, and inverse effort
            effort_factor = max(1, 10 - effort) if isinstance(effort, (int, float)) else 5
            return priority * impact * effort_factor

        return sorted(suggestions, key=priority_score, reverse=True)

    async def _create_optimization_plan(self, suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a structured optimization plan"""

        if not suggestions:
            return {
                "plan": "No suggestions available to create a plan",
                "total_suggestions": 0,
                "high_priority_count": 0,
                "estimated_total_effort": 0,
            }

        # Create a basic plan structure without LLM
        high_priority = [s for s in suggestions if s.get("priority") == "High"]
        medium_priority = [s for s in suggestions if s.get("priority") == "Medium"]
        low_priority = [s for s in suggestions if s.get("priority") == "Low"]

        plan_text = "Optimization Plan:\n\n"
        plan_text += "IMMEDIATE ACTIONS (High Priority):\n"
        for i, s in enumerate(high_priority[:5], 1):
            plan_text += f"{i}. {s.get('title', 'Unknown')}\n"

        plan_text += "\nSHORT-TERM GOALS (Medium Priority):\n"
        for i, s in enumerate(medium_priority[:5], 1):
            plan_text += f"{i}. {s.get('title', 'Unknown')}\n"

        plan_text += "\nLONG-TERM OBJECTIVES (Low Priority):\n"
        for i, s in enumerate(low_priority[:5], 1):
            plan_text += f"{i}. {s.get('title', 'Unknown')}\n"

        return {
            "plan": plan_text,
            "total_suggestions": len(suggestions),
            "high_priority_count": len(high_priority),
            "estimated_total_effort": sum(
                [
                    s.get("estimated_effort", 0)
                    for s in suggestions
                    if isinstance(s.get("estimated_effort"), (int, float))
                ]
            ),
        }

    def _calculate_impact_score(self, suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall impact score"""

        impact_map = {"High": 3, "Medium": 2, "Low": 1}
        category_impacts = {}

        for suggestion in suggestions:
            category = suggestion.get("category", "Other")
            impact = impact_map.get(suggestion.get("expected_impact", "Medium"), 2)

            if category not in category_impacts:
                category_impacts[category] = 0
            category_impacts[category] += impact

        total_impact = sum(category_impacts.values())
        max_possible_impact = len(suggestions) * 3

        return {
            "overall_score": (
                (total_impact / max_possible_impact * 100) if max_possible_impact > 0 else 0
            ),
            "category_breakdown": category_impacts,
            "total_suggestions": len(suggestions),
        }

    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get optimization history"""
        return self.optimization_history

    def get_active_suggestions(self) -> List[Dict[str, Any]]:
        """Get currently active suggestions"""
        return self.active_suggestions

    def mark_suggestion_completed(self, suggestion_id: str):
        """Mark a suggestion as completed"""
        # Implementation for tracking completed suggestions
        pass

    async def generate_continuous_improvement_report(self) -> str:
        """Generate a continuous improvement report"""

        if not self.optimization_history:
            return "No optimization history available."

        latest_analysis = self.optimization_history[-1]

        report = f"""
# Continuous Improvement Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- **Total Suggestions:** {latest_analysis['estimated_impact']['total_suggestions']}
- **Overall Impact Score:** {latest_analysis['estimated_impact']['overall_score']:.1f}%
- **High Priority Items:** {latest_analysis['estimated_impact']['total_suggestions']}

## Top Recommendations
"""

        # Add top 5 suggestions
        top_suggestions = latest_analysis["suggestions"][:5]
        for i, suggestion in enumerate(top_suggestions, 1):
            report += f"""
### {i}. {suggestion.get('title', 'Untitled')}
- **Category:** {suggestion.get('category', 'N/A')}
- **Priority:** {suggestion.get('priority', 'N/A')}
- **Impact:** {suggestion.get('expected_impact', 'N/A')}
- **Effort:** {suggestion.get('estimated_effort', 'N/A')} hours
- **Description:** {suggestion.get('description', 'N/A')}
"""

        return report

    def _create_analysis_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Create a concise summary of analysis results for LLM"""
        summary = []

        if "file_count" in analysis_results:
            summary.append(f"Files analyzed: {analysis_results['file_count']}")

        if "lines_of_code" in analysis_results:
            summary.append(f"Lines of code: {analysis_results['lines_of_code']}")

        if "languages" in analysis_results:
            langs = ", ".join(analysis_results["languages"])
            summary.append(f"Languages: {langs}")

        if "security_issues" in analysis_results:
            issues = analysis_results["security_issues"]
            if isinstance(issues, list):
                summary.append(f"Security issues found: {len(issues)}")

        if "code_quality_score" in analysis_results:
            summary.append(f"Code quality score: {analysis_results['code_quality_score']}")

        return "\n".join(summary) if summary else "No detailed metrics available"

    def _generate_fallback_suggestions(
        self, analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate fallback suggestions when LLM is not available"""
        suggestions = []

        # Security suggestions based on analysis
        if "security_issues" in analysis_results:
            issues = analysis_results.get("security_issues", [])
            if isinstance(issues, list) and len(issues) > 0:
                suggestions.append(
                    {
                        "title": "Address Security Issues",
                        "description": f"Found {len(issues)} security issues that should be addressed",
                        "category": "Security",
                        "priority": "High",
                        "estimated_effort": len(issues) * 2,
                        "expected_impact": "High",
                    }
                )

        # Complexity suggestions
        if "complexity_score" in analysis_results:
            score = analysis_results.get("complexity_score", 0)
            if score > 10:
                suggestions.append(
                    {
                        "title": "Reduce Code Complexity",
                        "description": "High complexity detected. Consider refactoring complex functions",
                        "category": "Code Quality",
                        "priority": "Medium",
                        "estimated_effort": 8,
                        "expected_impact": "Medium",
                    }
                )

        # Test coverage suggestions
        if "test_coverage" in analysis_results:
            coverage = analysis_results.get("test_coverage", {})
            coverage_pct = coverage.get("coverage_percentage", 100)
            if coverage_pct < 80:
                suggestions.append(
                    {
                        "title": "Improve Test Coverage",
                        "description": f"Current test coverage is {coverage_pct}%. Aim for at least 80%",
                        "category": "Testing",
                        "priority": "Medium",
                        "estimated_effort": 16,
                        "expected_impact": "High",
                    }
                )

        # Documentation suggestions
        suggestions.append(
            {
                "title": "Enhance Documentation",
                "description": "Ensure all major components have clear documentation",
                "category": "Documentation",
                "priority": "Low",
                "estimated_effort": 4,
                "expected_impact": "Medium",
            }
        )

        return (
            suggestions
            if suggestions
            else [
                {
                    "title": "General Code Review",
                    "description": "Conduct a comprehensive code review",
                    "category": "Code Quality",
                    "priority": "Medium",
                    "estimated_effort": 8,
                    "expected_impact": "Medium",
                }
            ]
        )

    # ==================== URGENCY SCORING (NEW) ====================

    def calculate_urgency_score(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate urgency score for an issue

        Urgency = (Severity Weight * Impact Factor) / Fix Difficulty

        Args:
            issue: Issue dict with severity, affected_files, difficulty

        Returns:
            Dict with urgency_score, stars (1-5), color, estimated_fix_time
        """
        severity_weights = {"critical": 100, "high": 75, "medium": 50, "low": 25}

        # Get severity
        severity = issue.get("severity", "medium").lower()
        base_score = severity_weights.get(severity, 50)

        # Impact: How many LOC/Files affected
        impact_factor = 1.0
        if "affected_files" in issue:
            affected = issue["affected_files"]
            if isinstance(affected, list):
                impact_factor = min(len(affected) / 10, 5.0)
            elif isinstance(affected, int):
                impact_factor = min(affected / 10, 5.0)

        # Fix Difficulty: Easy=1h, Medium=4h, Hard=16h
        difficulty_hours = {"easy": 1, "medium": 4, "hard": 16}
        difficulty = difficulty_hours.get(issue.get("difficulty", "medium").lower(), 4)

        # Calculate urgency
        urgency = (base_score * impact_factor) / difficulty

        # Convert to 1-5 stars
        if urgency >= 80:
            stars, color = 5, "red"
        elif urgency >= 60:
            stars, color = 4, "orange"
        elif urgency >= 40:
            stars, color = 3, "yellow"
        elif urgency >= 20:
            stars, color = 2, "lightblue"
        else:
            stars, color = 1, "green"

        return {
            "urgency_score": round(urgency, 2),
            "stars": stars,
            "color": color,
            "estimated_fix_time": difficulty,
        }

    async def analyze_with_urgency(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze and prioritize issues with urgency scoring

        Automatically triggered after scan.
        Uses ContextEngineer for smart LLM context.

        Args:
            analysis_results: Project analysis results

        Returns:
            List of optimizations sorted by urgency (descending)
        """
        logger.info("🤖 Generating AI optimizations with urgency scoring...")

        issues = analysis_results.get("security_issues", [])

        # Use Context Engineer for smart LLM context
        try:
            from services.context_engineer import get_context_engineer

            context_engineer = get_context_engineer()
            context = context_engineer.build_analysis_context(
                analysis_results.get("project_path", ".")
            )
            logger.info(
                f"   Context: {context['selected_count']} files, {context['metadata']['total_tokens']} tokens"
            )
        except Exception as e:
            logger.warning(f"⚠️ Context engineer not available: {e}")
            context = {}

        optimizations = []

        for i, issue in enumerate(issues):
            # Calculate urgency
            urgency = self.calculate_urgency_score(issue)

            # Generate AI recommendation with context
            try:
                recommendation = await self._generate_recommendation(issue, context)
            except Exception as e:
                logger.warning(f"Could not generate recommendation for issue {i}: {e}")
                recommendation = issue.get("description", "No description available")

            # Combine issue with urgency and recommendation
            optimizations.append(
                {"id": f"issue_{i}", **issue, **urgency, "recommendation": recommendation}
            )

        # Sort by urgency descending
        sorted_optimizations = sorted(optimizations, key=lambda x: x["urgency_score"], reverse=True)

        logger.info(f"✅ Generated {len(sorted_optimizations)} prioritized suggestions")

        return sorted_optimizations

    async def _generate_recommendation(self, issue: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Generate AI recommendation for fixing an issue

        Args:
            issue: Issue details
            context: Context from ContextEngineer

        Returns:
            Recommendation text
        """
        # Build prompt with context
        context_summary = ""
        if context and "metadata" in context:
            meta = context["metadata"]
            context_summary = f"""
            Context:
            - Selected files: {context.get('selected_count', 0)}
            - Total lines: {meta.get('total_lines', 0)}
            - File types: {', '.join(meta.get('file_types', {}).keys())}
            """

        prompt = f"""
        Security Issue Analysis:
        
        {context_summary}
        
        Issue Details:
        - Title: {issue.get('title', 'Unknown')}
        - Severity: {issue.get('severity', 'Unknown')}
        - Description: {issue.get('description', 'No description')}
        - File: {issue.get('file', 'Unknown')}
        - Line: {issue.get('line', '?')}
        
        Provide a concise, actionable recommendation for fixing this issue.
        Include:
        1. What needs to be changed
        2. Why it's important
        3. A concrete code example if applicable
        
        Keep it under 150 words.
        """

        try:
            response = await self.llm_manager.generate_response(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"❌ Failed to generate recommendation: {e}")
            # Fallback recommendation
            return f"Fix {issue.get('severity', 'this')} issue in {issue.get('file', 'the affected file')}. Review the code and apply security best practices."
