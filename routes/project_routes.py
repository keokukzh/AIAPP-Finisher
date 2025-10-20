"""
Project Routes - Project Library Management

Provides endpoints for:
- Listing all analyzed projects
- Getting project details
- Re-analyzing projects
- Comparing projects
- Searching projects
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from database.mongo_client import get_mongo_client

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/library")
async def list_projects(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of projects to return"),
    status: Optional[str] = Query(
        None, description="Filter by status: completed, failed, in_progress"
    ),
    skip: int = Query(0, ge=0, description="Number of projects to skip (pagination)"),
):
    """
    List all analyzed projects with optional filtering

    Returns project library with metadata, scores, and health status.
    """
    try:
        mongo = get_mongo_client()

        if not mongo.is_connected():
            logger.warning("⚠️ MongoDB not connected - returning empty list")
            return {"projects": [], "total": 0, "message": "MongoDB not available"}

        projects = await mongo.list_projects(limit=limit, status=status, skip=skip)

        logger.info(f"📋 Retrieved {len(projects)} projects from library")

        return {"projects": projects, "total": len(projects), "limit": limit, "skip": skip}

    except Exception as e:
        logger.error(f"❌ Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {str(e)}")


@router.get("/{project_id}")
async def get_project(project_id: str):
    """
    Get detailed information about a specific project

    Args:
        project_id: MongoDB document ID

    Returns:
        Full project analysis data including results, optimizations, and history
    """
    try:
        mongo = get_mongo_client()

        if not mongo.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not available")

        project = await mongo.get_analysis(project_id)

        if not project:
            raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")

        logger.info(f"📂 Retrieved project: {project.get('project_name')}")

        return {"status": "success", "project": project}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """
    Delete a project from the library

    Args:
        project_id: MongoDB document ID

    Returns:
        Confirmation of deletion
    """
    try:
        mongo = get_mongo_client()

        if not mongo.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not available")

        success = await mongo.delete_analysis(project_id)

        if not success:
            raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")

        logger.info(f"🗑️ Deleted project: {project_id}")

        return {"status": "success", "message": f"Project {project_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_projects(
    query: str = Query(..., min_length=1, description="Search term"),
    limit: int = Query(50, ge=1, le=100, description="Maximum results"),
):
    """
    Search projects by name or path

    Args:
        query: Search string
        limit: Maximum number of results

    Returns:
        List of matching projects
    """
    try:
        mongo = get_mongo_client()

        if not mongo.is_connected():
            raise HTTPException(status_code=503, detail="MongoDB not available")

        results = await mongo.search_projects(query, limit)

        logger.info(f"🔍 Search '{query}' returned {len(results)} results")

        return {"status": "success", "query": query, "results": results, "count": len(results)}

    except Exception as e:
        logger.error(f"❌ Error searching projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_library_stats():
    """
    Get statistics about the project library

    Returns:
        - Total projects
        - Projects by status
        - Average scores
        - Language distribution
    """
    try:
        mongo = get_mongo_client()

        if not mongo.is_connected():
            return {"status": "unavailable", "message": "MongoDB not connected"}

        # Get all projects
        all_projects = await mongo.list_projects(limit=1000)

        # Calculate statistics
        stats = {
            "total_projects": len(all_projects),
            "by_status": {},
            "by_health": {"healthy": 0, "needs_attention": 0, "critical": 0},
            "average_scores": {"quality": 0, "security": 0, "complexity": 0},
            "top_languages": {},
            "top_frameworks": {},
        }

        # Count by status and health
        quality_sum = 0
        security_sum = 0
        complexity_sum = 0

        for project in all_projects:
            # Status
            status = project.get("status", "unknown")
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

            # Health
            health = project.get("health_status", "unknown")
            if health in stats["by_health"]:
                stats["by_health"][health] += 1

            # Scores
            quality_sum += project.get("quality_score", 0)
            security_sum += project.get("security_score", 0)
            complexity_sum += project.get("complexity_score", 0)

            # Languages
            for lang in project.get("languages", []):
                stats["top_languages"][lang] = stats["top_languages"].get(lang, 0) + 1

            # Frameworks
            for fw in project.get("frameworks", []):
                stats["top_frameworks"][fw] = stats["top_frameworks"].get(fw, 0) + 1

        # Calculate averages
        if len(all_projects) > 0:
            stats["average_scores"]["quality"] = round(quality_sum / len(all_projects), 1)
            stats["average_scores"]["security"] = round(security_sum / len(all_projects), 1)
            stats["average_scores"]["complexity"] = round(complexity_sum / len(all_projects), 1)

        # Sort top languages and frameworks
        stats["top_languages"] = dict(
            sorted(stats["top_languages"].items(), key=lambda x: x[1], reverse=True)[:10]
        )
        stats["top_frameworks"] = dict(
            sorted(stats["top_frameworks"].items(), key=lambda x: x[1], reverse=True)[:10]
        )

        logger.info(f"📊 Library stats: {stats['total_projects']} projects")

        return {"status": "success", "stats": stats}

    except Exception as e:
        logger.error(f"❌ Error getting library stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
