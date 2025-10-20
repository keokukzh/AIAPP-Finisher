"""Type definitions for project analysis operations.

Provides TypedDict definitions and type aliases for structured data
used throughout the analysis system.
"""

from typing import Any, Dict, List, Literal, Optional, TypedDict

# Type Aliases
Priority = Literal["High", "Medium", "Low"]
Severity = Literal["critical", "high", "medium", "low"]
AnalysisPhase = Literal[
    "initialization",
    "file_scanning",
    "language_detection",
    "framework_detection",
    "dependency_analysis",
    "api_analysis",
    "database_analysis",
    "security_scan",
    "metrics_calculation",
    "report_generation",
    "completed",
]


class LanguageInfo(TypedDict):
    """Information about a detected programming language."""

    name: str
    percentage: float
    lines: int
    files: int


class FrameworkInfo(TypedDict):
    """Information about a detected framework."""

    name: str
    type: str  # 'Frontend' or 'Backend'
    version: Optional[str]
    confidence: float


class MetricsDict(TypedDict, total=False):
    """Code quality metrics."""

    complexity: float
    cyclomatic_complexity: float
    maintainability_index: float
    code_quality_score: float
    technical_debt: float
    lines_of_code: int
    comment_ratio: float


class SecurityIssue(TypedDict):
    """Security vulnerability information."""

    severity: Severity
    title: str
    description: str
    file_path: str
    line_number: Optional[int]
    cve_id: Optional[str]
    recommendation: str


class SecurityDict(TypedDict, total=False):
    """Security analysis results."""

    security_score: float
    vulnerabilities: List[SecurityIssue]
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int


class TestCoverageDict(TypedDict, total=False):
    """Test coverage information."""

    coverage_percentage: float
    lines_covered: int
    lines_total: int
    test_files_count: int
    test_frameworks: List[str]


class DependencyInfo(TypedDict):
    """Information about a project dependency."""

    name: str
    version: str
    type: str  # 'direct' or 'transitive'
    ecosystem: str  # 'npm', 'pip', 'maven', etc.


class APIEndpoint(TypedDict):
    """Information about an API endpoint."""

    path: str
    method: str
    handler: str
    file_path: str
    line_number: int
    parameters: List[str]
    authenticated: bool


class DatabaseSchema(TypedDict):
    """Database schema information."""

    database_type: str
    tables: List[Dict[str, Any]]
    models: List[Dict[str, Any]]
    migrations_count: int


class AnalysisResults(TypedDict, total=False):
    """Complete project analysis results."""

    project_path: str
    project_name: str
    analysis_timestamp: str
    file_count: int
    total_files: int
    lines_of_code: int

    # Language and framework info
    languages: List[LanguageInfo]
    frameworks: List[FrameworkInfo]

    # Dependencies
    dependencies: Dict[str, List[DependencyInfo]]
    dependency_count: int

    # API information
    api_endpoints: List[APIEndpoint]
    api_count: int

    # Database information
    database_schema: DatabaseSchema

    # Code quality
    metrics: MetricsDict
    complexity: Dict[str, Any]

    # Security
    security_analysis: SecurityDict

    # Testing
    test_coverage: TestCoverageDict

    # Additional metadata
    analysis_duration: float
    analysis_phases: List[str]


class OptimizationSuggestion(TypedDict):
    """Optimization suggestion information."""

    title: str
    description: str
    priority: Priority
    impact: str
    effort: str
    category: str
    details: str
    action: str


class WorkflowStatus(TypedDict):
    """Workflow execution status."""

    workflow_id: str
    workflow_type: str
    status: Literal["pending", "running", "completed", "failed"]
    current_phase: str
    overall_progress: float
    start_time: Optional[float]
    end_time: Optional[float]
    error: Optional[str]
