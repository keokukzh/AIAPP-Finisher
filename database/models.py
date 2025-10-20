"""
MongoDB Models for Project Analysis Persistence

Defines data models for storing project analyses in MongoDB.
Uses MongoEngine ODM for schema definition and validation.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from mongoengine import Document, fields

logger = logging.getLogger(__name__)


class ProjectAnalysis(Document):
    """
    MongoDB document model for project analysis results

    Stores comprehensive analysis data including:
    - Project metadata (path, name, timestamps)
    - Analysis results (languages, frameworks, dependencies)
    - Optimization suggestions
    - Security issues
    - Code quality metrics
    """

    meta = {
        "collection": "project_analyses",
        "indexes": [
            "project_path",
            "-analyzed_at",  # Descending for latest first
            "status",
            "project_name",
            ("project_path", "-analyzed_at"),  # Compound index
        ],
    }

    # Core fields
    project_path = fields.StringField(required=True, max_length=500)
    project_name = fields.StringField(required=True, max_length=200)
    analyzed_at = fields.DateTimeField(default=datetime.utcnow)
    status = fields.StringField(
        choices=["completed", "failed", "in_progress", "pending"], default="pending"
    )

    # Analysis results
    analysis_results = fields.DictField()

    # Extracted key metrics (for quick queries)
    total_files = fields.IntField(default=0)
    total_lines = fields.IntField(default=0)
    languages = fields.ListField(fields.StringField())
    frameworks = fields.ListField(fields.StringField())

    # Optimization and issues
    optimization_suggestions = fields.ListField(fields.DictField())
    security_issues = fields.ListField(fields.DictField())

    # Quality scores
    quality_score = fields.FloatField(min_value=0.0, max_value=100.0)
    complexity_score = fields.FloatField(min_value=0.0, max_value=100.0)
    security_score = fields.FloatField(min_value=0.0, max_value=100.0)

    # Additional metadata
    metadata = fields.DictField()  # LOC, test coverage, etc

    # Analysis configuration
    analysis_config = fields.DictField()  # Settings used for analysis

    # Error tracking
    error_message = fields.StringField()
    error_traceback = fields.StringField()

    # Timestamps
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        """Override save to update timestamps"""
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary"""
        return {
            "id": str(self.id),
            "project_path": self.project_path,
            "project_name": self.project_name,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None,
            "status": self.status,
            "analysis_results": self.analysis_results,
            "optimization_suggestions": self.optimization_suggestions,
            "security_issues": self.security_issues,
            "quality_score": self.quality_score,
            "complexity_score": self.complexity_score,
            "security_score": self.security_score,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<ProjectAnalysis {self.project_name} ({self.status})>"


class OptimizationHistory(Document):
    """
    Track history of applied optimizations

    Stores information about code fixes and optimizations
    that were applied to projects.
    """

    meta = {
        "collection": "optimization_history",
        "indexes": ["project_analysis", "-applied_at", "status"],
    }

    # Reference to project analysis
    project_analysis = fields.ReferenceField(ProjectAnalysis, required=True)

    # Optimization details
    optimization_type = fields.StringField(
        choices=["security_fix", "performance", "code_quality", "refactoring"], required=True
    )
    description = fields.StringField(required=True)

    # Files affected
    files_modified = fields.ListField(fields.StringField())

    # Changes made
    changes_summary = fields.DictField()
    diff = fields.StringField()  # Unified diff

    # Status
    status = fields.StringField(
        choices=["pending", "applied", "failed", "rolled_back"], default="pending"
    )

    # Backup information
    backup_path = fields.StringField()

    # Approval workflow
    approval_status = fields.StringField(
        choices=["pending", "approved", "rejected"], default="pending"
    )
    approved_by = fields.StringField()
    approved_at = fields.DateTimeField()

    # Timestamps
    created_at = fields.DateTimeField(default=datetime.utcnow)
    applied_at = fields.DateTimeField()

    def __repr__(self):
        return f"<OptimizationHistory {self.optimization_type} - {self.status}>"


class AnalysisSession(Document):
    """
    Track analysis sessions for performance monitoring

    Stores metadata about analysis execution including
    duration, resources used, and errors encountered.
    """

    meta = {"collection": "analysis_sessions", "indexes": ["-started_at", "status"]}

    session_id = fields.StringField(required=True, unique=True)
    project_path = fields.StringField(required=True)

    # Session metadata
    status = fields.StringField(
        choices=["running", "completed", "failed", "cancelled"], default="running"
    )

    # Timing
    started_at = fields.DateTimeField(default=datetime.utcnow)
    completed_at = fields.DateTimeField()
    duration_seconds = fields.FloatField()

    # Phases tracking
    phases = fields.ListField(fields.DictField())

    # Resource usage
    cpu_usage_percent = fields.FloatField()
    memory_usage_mb = fields.FloatField()

    # LLM usage
    llm_calls = fields.IntField(default=0)
    llm_tokens_used = fields.IntField(default=0)
    llm_cost = fields.FloatField(default=0.0)

    # Results
    result_id = fields.ReferenceField(ProjectAnalysis)

    # Error tracking
    error_message = fields.StringField()
    error_phase = fields.StringField()

    def __repr__(self):
        return f"<AnalysisSession {self.session_id} - {self.status}>"


def init_mongodb(uri: str = "mongodb://mongodb:27017/ai-pm"):
    """
    Initialize MongoDB connection

    Args:
        uri: MongoDB connection URI
    """
    try:
        from mongoengine import connect

        connect(host=uri, alias="default")
        logger.info(f"✅ MongoDB connected: {uri}")
        return True
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return False
