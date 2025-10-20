"""
Application Dependencies - Dependency injection for FastAPI
"""

import logging
from typing import Any, Dict

from fastapi import HTTPException

from analyzers.project_analyzer import ProjectAnalyzer
from app_lifecycle import get_project_manager_agent, model_manager
from generators.agent_generator import AgentGenerator
from generators.workflow_generator import WorkflowGenerator
from orchestrator.agent_orchestrator import AgentOrchestrator
from orchestrator.workflow_orchestrator import WorkflowOrchestrator

logger = logging.getLogger(__name__)

# Global state
current_project = None
analysis_results = {}
loaded_modules = {
    "agents": {},
    "skills": {},
    "commands": {},
    "hooks": {},
    "plugins": {},
    "mcps": {},
}


async def get_project_analyzer() -> ProjectAnalyzer:
    """Get or create ProjectAnalyzer instance"""
    return ProjectAnalyzer()


async def get_agent_generator():
    """Get or create AgentGenerator instance"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="ModelManager not initialized")
    return AgentGenerator(model_manager)


async def get_workflow_generator():
    """Get or create WorkflowGenerator instance"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="ModelManager not initialized")
    return WorkflowGenerator(model_manager)


async def get_workflow_orchestrator() -> WorkflowOrchestrator:
    """Get or create WorkflowOrchestrator instance"""
    return WorkflowOrchestrator()


async def get_agent_orchestrator() -> AgentOrchestrator:
    """Get or create AgentOrchestrator instance"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="ModelManager not initialized")
    return AgentOrchestrator(model_manager)


def get_current_project() -> str:
    """Get current project path"""
    return current_project


def set_current_project(project_path: str):
    """Set current project path"""
    global current_project
    current_project = project_path


def get_analysis_results() -> Dict[str, Any]:
    """Get current analysis results"""
    return analysis_results


def set_analysis_results(results: Dict[str, Any]):
    """Set analysis results"""
    global analysis_results
    analysis_results = results


def get_loaded_modules() -> Dict[str, Any]:
    """Get loaded modules registry"""
    return loaded_modules


def register_module(module_type: str, module_name: str, module_instance: Any):
    """Register a dynamically loaded module"""
    if module_type not in loaded_modules:
        loaded_modules[module_type] = {}
    loaded_modules[module_type][module_name] = module_instance
    logger.info(f"Registered {module_type}: {module_name}")
