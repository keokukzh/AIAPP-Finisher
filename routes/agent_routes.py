"""
Agent Routes for KI-Projektmanagement-System
Handles chat, agent generation, agent status, and optimization endpoints
"""

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/agents", tags=["agents"])


class ChatRequest(BaseModel):
    """Request model for chat"""

    message: str
    context: Optional[Dict[str, Any]] = None


@router.post("/chat")
async def chat_with_agent(request: ChatRequest, project_manager_agent):
    """Chat with the AI project manager"""
    try:
        if not project_manager_agent:
            raise HTTPException(status_code=503, detail="Project manager agent not available")

        response = await project_manager_agent.chat(request.message, request.context)

        return {
            "message": request.message,
            "response": response,
            "timestamp": "2024-01-01T00:00:00Z",
        }

    except Exception as e:
        logger.error(f"❌ Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_agents(analysis_results, agent_generator):
    """Generates agents based on analysis results"""
    try:
        if analysis_results is None:
            raise HTTPException(
                status_code=404, detail="No analysis results available. Run analysis first."
            )

        # Generate agents
        generated_agents = await agent_generator.generate_from_analysis(analysis_results)

        return {
            "status": "success",
            "agents_generated": len(generated_agents),
            "agents": generated_agents,
        }

    except Exception as e:
        logger.error(f"❌ Error generating agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_agent_status(loaded_modules):
    """Returns the status of all agents"""
    try:
        agents = loaded_modules.get("agents", {})

        agent_status = []
        for agent_name, agent in agents.items():
            status_info = {
                "name": agent_name,
                "type": type(agent).__name__,
                "status": getattr(agent, "status", "unknown"),
            }
            if hasattr(agent, "get_status"):
                status_info.update(agent.get_status())
            agent_status.append(status_info)

        return {"total_agents": len(agents), "agents": agent_status}

    except Exception as e:
        logger.error(f"❌ Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimizations")
async def get_optimizations(optimization_engine, analysis_results):
    """Returns optimization suggestions"""
    try:
        if analysis_results is None:
            raise HTTPException(
                status_code=404,
                detail="No analysis results available. Run /api/analysis/analyze first.",
            )

        # Use the correct method name
        optimizations = await optimization_engine.analyze_and_optimize(analysis_results)

        return {
            "status": "success",
            "optimizations": optimizations.get("suggestions", []),
            "optimization_plan": optimizations.get("optimization_plan", {}),
            "estimated_impact": optimizations.get("estimated_impact", 0),
        }

    except Exception as e:
        logger.error(f"❌ Error getting optimizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
