"""Custom exception classes for APP-Finisher.

Provides a hierarchy of exceptions for fine-grained error handling
across analysis, generation, and execution operations.
"""

from typing import Optional


class AppFinisherError(Exception):
    """Base exception for all APP-Finisher errors."""

    pass


class AnalysisError(AppFinisherError):
    """Raised when project analysis fails."""

    def __init__(self, message: str, project_path: str, cause: Optional[Exception] = None):
        self.project_path = project_path
        self.cause = cause
        super().__init__(f"{message} (project: {project_path})")


class ParsingError(AnalysisError):
    """Raised when file parsing fails."""

    pass


class GenerationError(AppFinisherError):
    """Raised when agent/workflow generation fails."""

    def __init__(self, message: str, generation_type: str, cause: Optional[Exception] = None):
        self.generation_type = generation_type
        self.cause = cause
        super().__init__(f"{message} (type: {generation_type})")


class LLMError(AppFinisherError):
    """Raised when LLM interaction fails."""

    def __init__(self, message: str, model_name: str, provider: str):
        self.model_name = model_name
        self.provider = provider
        super().__init__(f"{message} (model: {model_name}, provider: {provider})")


class ConfigurationError(AppFinisherError):
    """Raised when configuration is invalid or missing."""

    pass


class WorkflowError(AppFinisherError):
    """Raised when workflow execution fails."""

    def __init__(self, message: str, workflow_id: str, cause: Optional[Exception] = None):
        self.workflow_id = workflow_id
        self.cause = cause
        super().__init__(f"{message} (workflow: {workflow_id})")


class DatabaseError(AppFinisherError):
    """Raised when database operations fail."""

    pass
