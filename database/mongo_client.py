"""
MongoDB Client - CRUD Operations for Project Analysis

Provides high-level interface for database operations including:
- Creating and saving analysis results
- Querying and filtering projects
- Updating analysis data
- Managing project library
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MongoClient:
    """
    MongoDB client for project analysis persistence

    Handles all database operations with automatic connection
    management and error handling.
    """

    def __init__(self, uri: str = "mongodb://mongodb:27017/ai-pm"):
        """
        Initialize MongoDB client

        Args:
            uri: MongoDB connection URI
        """
        self.uri = uri
        self._initialized = False
        self._connect()

    def _connect(self):
        """Establish MongoDB connection"""
        try:
            from mongoengine import connect

            from .models import init_mongodb

            init_mongodb(self.uri)
            self._initialized = True
            logger.info("✅ MongoClient initialized")

        except ImportError as e:
            logger.warning(f"⚠️ MongoEngine not installed: {e}")
            logger.info("💡 Install with: pip install mongoengine")
            self._initialized = False

        except Exception as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            self._initialized = False

    async def save_analysis(
        self, project_path: str, results: Dict[str, Any], status: str = "completed"
    ) -> Optional[str]:
        """
        Save analysis results to MongoDB

        Args:
            project_path: Path to analyzed project
            results: Analysis results dictionary
            status: Analysis status (completed, failed, in_progress)

        Returns:
            Document ID as string, or None if save failed
        """
        if not self._initialized:
            logger.warning("⚠️ MongoDB not available - skipping save")
            return None

        try:
            from .models import ProjectAnalysis

            # Extract project name from path
            project_name = Path(project_path).name

            # Extract key metrics
            total_files = results.get("total_files", 0)
            total_lines = results.get("total_lines_of_code", 0)

            # Extract languages (handle different formats)
            languages = []
            if "languages" in results:
                lang_data = results["languages"]
                if isinstance(lang_data, list):
                    languages = [
                        lang if isinstance(lang, str) else lang.get("name", "Unknown")
                        for lang in lang_data
                    ]
                elif isinstance(lang_data, dict):
                    languages = list(lang_data.keys())

            # Extract frameworks
            frameworks = []
            if "frameworks" in results:
                fw_data = results["frameworks"]
                if isinstance(fw_data, list):
                    frameworks = [
                        fw if isinstance(fw, str) else fw.get("name", "Unknown") for fw in fw_data
                    ]

            # Extract optimization suggestions
            optimizations = results.get("optimizations", [])

            # Extract security issues
            security_issues = results.get("security_issues", [])

            # Calculate scores
            quality_score = self._calculate_quality_score(results)
            complexity_score = self._calculate_complexity_score(results)
            security_score = self._calculate_security_score(security_issues)

            # Create document
            analysis = ProjectAnalysis(
                project_path=project_path,
                project_name=project_name,
                status=status,
                analysis_results=results,
                total_files=total_files,
                total_lines=total_lines,
                languages=languages,
                frameworks=frameworks,
                optimization_suggestions=optimizations,
                security_issues=security_issues,
                quality_score=quality_score,
                complexity_score=complexity_score,
                security_score=security_score,
                metadata={
                    "lines_of_code": total_lines,
                    "file_count": total_files,
                    "language_count": len(languages),
                    "framework_count": len(frameworks),
                },
            )

            analysis.save()
            logger.info(f"💾 Saved analysis to MongoDB: {project_name} (ID: {analysis.id})")

            return str(analysis.id)

        except Exception as e:
            logger.error(f"❌ Failed to save analysis: {e}")
            return None

    async def get_analysis(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get analysis by ID

        Args:
            project_id: MongoDB document ID

        Returns:
            Analysis data as dictionary, or None if not found
        """
        if not self._initialized:
            return None

        try:
            from bson import ObjectId

            from .models import ProjectAnalysis

            analysis = ProjectAnalysis.objects(id=ObjectId(project_id)).first()

            if analysis:
                return analysis.to_dict()
            else:
                logger.warning(f"⚠️ Analysis not found: {project_id}")
                return None

        except Exception as e:
            logger.error(f"❌ Failed to get analysis: {e}")
            return None

    async def list_projects(
        self, limit: int = 50, status: Optional[str] = None, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List projects with optional filtering

        Args:
            limit: Maximum number of results
            status: Filter by status (completed, failed, in_progress)
            skip: Number of results to skip (for pagination)

        Returns:
            List of project analysis dictionaries
        """
        if not self._initialized:
            return []

        try:
            from .models import ProjectAnalysis

            # Build query
            query = ProjectAnalysis.objects

            if status:
                query = query.filter(status=status)

            # Execute query with sorting and limits
            projects = query.order_by("-analyzed_at").skip(skip).limit(limit)

            # Convert to dicts
            result = []
            for project in projects:
                project_dict = project.to_dict()

                # Add human-readable date
                if project.analyzed_at:
                    project_dict["analyzed_at_human"] = self._format_date(project.analyzed_at)

                # Add health status
                project_dict["health_status"] = self._determine_health_status(project)

                result.append(project_dict)

            logger.info(f"📋 Retrieved {len(result)} projects from MongoDB")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to list projects: {e}")
            return []

    async def update_analysis(self, project_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing analysis

        Args:
            project_id: MongoDB document ID
            updates: Dictionary of fields to update

        Returns:
            True if successful, False otherwise
        """
        if not self._initialized:
            return False

        try:
            from bson import ObjectId

            from .models import ProjectAnalysis

            # Update document
            result = ProjectAnalysis.objects(id=ObjectId(project_id)).update(**updates)

            if result:
                logger.info(f"✅ Updated analysis: {project_id}")
                return True
            else:
                logger.warning(f"⚠️ Analysis not found for update: {project_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to update analysis: {e}")
            return False

    async def delete_analysis(self, project_id: str) -> bool:
        """
        Delete an analysis

        Args:
            project_id: MongoDB document ID

        Returns:
            True if successful, False otherwise
        """
        if not self._initialized:
            return False

        try:
            from bson import ObjectId

            from .models import ProjectAnalysis

            analysis = ProjectAnalysis.objects(id=ObjectId(project_id)).first()

            if analysis:
                analysis.delete()
                logger.info(f"🗑️ Deleted analysis: {project_id}")
                return True
            else:
                logger.warning(f"⚠️ Analysis not found for deletion: {project_id}")
                return False

        except Exception as e:
            logger.error(f"❌ Failed to delete analysis: {e}")
            return False

    async def search_projects(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search projects by name or path

        Args:
            search_term: Search string
            limit: Maximum results

        Returns:
            List of matching projects
        """
        if not self._initialized:
            return []

        try:
            # Search in project name and path
            from mongoengine.queryset.visitor import Q

            from .models import ProjectAnalysis

            query = (
                ProjectAnalysis.objects(
                    Q(project_name__icontains=search_term) | Q(project_path__icontains=search_term)
                )
                .order_by("-analyzed_at")
                .limit(limit)
            )

            return [p.to_dict() for p in query]

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []

    # Helper methods

    def _calculate_quality_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall code quality score from results"""
        # Simplified scoring - can be enhanced
        base_score = 75.0

        # Deduct for high complexity
        if "complexity" in results:
            complexity = results["complexity"]
            if isinstance(complexity, dict):
                avg_complexity = complexity.get("average", 5)
                if avg_complexity > 10:
                    base_score -= min(20, (avg_complexity - 10) * 2)

        # Deduct for security issues
        security_issues = results.get("security_issues", [])
        if security_issues:
            base_score -= min(30, len(security_issues) * 3)

        return max(0, min(100, base_score))

    def _calculate_complexity_score(self, results: Dict[str, Any]) -> float:
        """Calculate complexity score (100 = low complexity)"""
        if "complexity" in results:
            complexity = results["complexity"]
            if isinstance(complexity, dict):
                avg_complexity = complexity.get("average", 5)
                # Convert to 0-100 scale (inverse)
                return max(0, min(100, 100 - (avg_complexity * 5)))

        return 75.0  # Default

    def _calculate_security_score(self, security_issues: List[Dict]) -> float:
        """Calculate security score (100 = no issues)"""
        if not security_issues:
            return 100.0

        # Weighted scoring by severity
        score = 100.0
        for issue in security_issues:
            severity = issue.get("severity", "medium").lower()
            if severity == "critical":
                score -= 15
            elif severity == "high":
                score -= 10
            elif severity == "medium":
                score -= 5
            else:
                score -= 2

        return max(0, score)

    def _format_date(self, dt: datetime) -> str:
        """Format datetime to human-readable string"""
        now = datetime.utcnow()
        diff = now - dt

        if diff.days == 0:
            if diff.seconds < 3600:
                return f"{diff.seconds // 60} minutes ago"
            else:
                return f"{diff.seconds // 3600} hours ago"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        else:
            return dt.strftime("%Y-%m-%d")

    def _determine_health_status(self, project) -> str:
        """Determine project health status from scores"""
        avg_score = (
            (project.quality_score or 0)
            + (project.complexity_score or 0)
            + (project.security_score or 0)
        ) / 3

        if avg_score >= 75:
            return "healthy"
        elif avg_score >= 50:
            return "needs_attention"
        else:
            return "critical"

    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self._initialized


# Global instance
_mongo_client = None


def get_mongo_client() -> MongoClient:
    """Get or create global MongoDB client instance"""
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient()
    return _mongo_client
