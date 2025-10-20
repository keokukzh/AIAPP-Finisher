"""Type definitions for APP-Finisher.

Exports all type definitions for easy import across the project.
"""

from .analysis_types import (  # Type Aliases; TypedDict Classes
    AnalysisPhase,
    AnalysisResults,
    APIEndpoint,
    DatabaseSchema,
    DependencyInfo,
    FrameworkInfo,
    LanguageInfo,
    MetricsDict,
    OptimizationSuggestion,
    Priority,
    SecurityDict,
    SecurityIssue,
    Severity,
    TestCoverageDict,
    WorkflowStatus,
)

__all__ = [
    # Type Aliases
    "Priority",
    "Severity",
    "AnalysisPhase",
    # TypedDict Classes
    "LanguageInfo",
    "FrameworkInfo",
    "MetricsDict",
    "SecurityIssue",
    "SecurityDict",
    "TestCoverageDict",
    "DependencyInfo",
    "APIEndpoint",
    "DatabaseSchema",
    "AnalysisResults",
    "OptimizationSuggestion",
    "WorkflowStatus",
]
