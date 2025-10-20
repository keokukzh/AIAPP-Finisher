"""
Application Lifecycle Management - Handles startup and shutdown
"""

import logging

from agents.project_manager_agent import ProjectManagerAgent
from llm.model_manager import ModelManager

logger = logging.getLogger(__name__)

# Global state
model_manager = None
project_manager_agent = None
_components_initialized = False


async def initialize_components():
    """Initialize all system components on startup"""
    global model_manager, project_manager_agent, _components_initialized

    try:
        logger.info("🚀 Initializing system components...")

        # Initialize ModelManager
        model_manager = ModelManager()
        await model_manager.initialize()
        logger.info("✅ ModelManager initialized")

        # Mark as initialized
        _components_initialized = True
        logger.info("✅ All components initialized successfully")

    except Exception as e:
        logger.error(f"❌ Error initializing components: {e}")
        raise


async def get_project_manager_agent() -> ProjectManagerAgent:
    """Lazy load ProjectManagerAgent"""
    global project_manager_agent, model_manager

    if project_manager_agent is None:
        if model_manager is None:
            raise RuntimeError("ModelManager not initialized. Call initialize_components() first.")

        project_manager_agent = ProjectManagerAgent(model_manager)
        await project_manager_agent.initialize()
        logger.info("✅ ProjectManagerAgent initialized")

    return project_manager_agent


async def shutdown_components():
    """Cleanup all system components on shutdown"""
    global model_manager, project_manager_agent

    try:
        logger.info("🔄 Shutting down system components...")

        if project_manager_agent:
            await project_manager_agent.cleanup()

        if model_manager:
            await model_manager.cleanup()

        logger.info("✅ All components shut down successfully")

    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")
