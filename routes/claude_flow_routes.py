"""
Claude Flow Routes - API routes for Claude-based workflows
Refactored to use specialized handlers
"""

import logging
from typing import Any, Dict

from fastapi import APIRouter

from .handlers import MemoryHandler, SwarmHandler

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/claude-flow", tags=["Claude Flow"])

# Initialize handlers
swarm_handler = SwarmHandler()
memory_handler = MemoryHandler()


# ============================================================================
# SWARM ENDPOINTS
# ============================================================================


@router.post("/swarm/create")
async def create_swarm(config: Dict[str, Any]):
    """Create a new swarm"""
    return await swarm_handler.create_swarm(config)


@router.post("/swarm/{swarm_id}/execute")
async def execute_swarm(swarm_id: str):
    """Execute a swarm"""
    return await swarm_handler.execute_swarm(swarm_id)


@router.get("/swarm/{swarm_id}/status")
async def get_swarm_status(swarm_id: str):
    """Get swarm status"""
    return await swarm_handler.get_swarm_status(swarm_id)


@router.get("/swarm/list")
async def list_swarms():
    """List all swarms"""
    swarms = await swarm_handler.list_swarms()
    return {"status": "success", "count": len(swarms), "swarms": swarms}


@router.delete("/swarm/{swarm_id}")
async def delete_swarm(swarm_id: str):
    """Delete a swarm"""
    return await swarm_handler.delete_swarm(swarm_id)


# ============================================================================
# MEMORY ENDPOINTS
# ============================================================================


@router.post("/memory/store")
async def store_memory(memory_data: Dict[str, Any]):
    """Store a memory"""
    return await memory_handler.store_memory(memory_data)


@router.get("/memory/{agent_id}")
async def get_memories(agent_id: str, memory_type: str = None, limit: int = 10):
    """Retrieve memories for an agent"""
    memories = await memory_handler.retrieve_memories(agent_id, memory_type, limit)
    return {"status": "success", "agent_id": agent_id, "count": len(memories), "memories": memories}


@router.get("/memory/search")
async def search_memories(query: str, agent_id: str = None):
    """Search memories"""
    results = await memory_handler.search_memories(query, agent_id)
    return {"status": "success", "query": query, "count": len(results), "results": results}


@router.delete("/memory/{agent_id}/{memory_id}")
async def delete_memory(agent_id: str, memory_id: str):
    """Delete a specific memory"""
    return await memory_handler.delete_memory(memory_id, agent_id)


@router.delete("/memory/{agent_id}/clear")
async def clear_agent_memories(agent_id: str):
    """Clear all memories for an agent"""
    return await memory_handler.clear_agent_memories(agent_id)


@router.get("/memory/stats")
async def get_memory_stats(agent_id: str = None):
    """Get memory statistics"""
    stats = await memory_handler.get_memory_stats(agent_id)
    return {"status": "success", "stats": stats}


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "claude-flow",
        "handlers": {"swarm": "active", "memory": "active"},
    }
