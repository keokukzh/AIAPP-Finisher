"""
Memory Handler - Handles memory storage and retrieval
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class MemoryHandler:
    """Handles memory storage and retrieval for agents"""

    def __init__(self):
        self.memories = {}
        self.memory_index = 0

    async def store_memory(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store a memory"""
        try:
            agent_id = memory_data.get("agent_id", "default")
            content = memory_data.get("content", "")
            memory_type = memory_data.get("type", "general")

            if not content:
                raise ValueError("Content is required")

            self.memory_index += 1
            memory_id = f"mem_{self.memory_index}"

            memory = {
                "id": memory_id,
                "agent_id": agent_id,
                "content": content,
                "type": memory_type,
                "timestamp": datetime.now().isoformat(),
                "metadata": memory_data.get("metadata", {}),
            }

            if agent_id not in self.memories:
                self.memories[agent_id] = []

            self.memories[agent_id].append(memory)
            logger.info(f"Stored memory {memory_id} for agent {agent_id}")

            return {"status": "success", "memory_id": memory_id, "memory": memory}

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def retrieve_memories(
        self, agent_id: str, memory_type: str = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve memories for an agent"""
        try:
            if agent_id not in self.memories:
                return []

            memories = self.memories[agent_id]

            # Filter by type if specified
            if memory_type:
                memories = [m for m in memories if m["type"] == memory_type]

            # Limit results
            memories = memories[-limit:]

            return memories

        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def search_memories(self, query: str, agent_id: str = None) -> List[Dict[str, Any]]:
        """Search memories by content"""
        try:
            query_lower = query.lower()
            results = []

            # Determine which agents to search
            agents_to_search = [agent_id] if agent_id else list(self.memories.keys())

            for aid in agents_to_search:
                if aid in self.memories:
                    for memory in self.memories[aid]:
                        if query_lower in memory["content"].lower():
                            results.append(memory)

            return results

        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_memory(self, memory_id: str, agent_id: str) -> Dict[str, Any]:
        """Delete a specific memory"""
        try:
            if agent_id not in self.memories:
                raise HTTPException(status_code=404, detail=f"No memories for agent {agent_id}")

            memories = self.memories[agent_id]
            memory_to_delete = None

            for i, mem in enumerate(memories):
                if mem["id"] == memory_id:
                    memory_to_delete = memories.pop(i)
                    break

            if not memory_to_delete:
                raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")

            logger.info(f"Deleted memory {memory_id} for agent {agent_id}")

            return {"status": "success", "message": f"Memory {memory_id} deleted"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting memory: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def clear_agent_memories(self, agent_id: str) -> Dict[str, Any]:
        """Clear all memories for an agent"""
        try:
            if agent_id in self.memories:
                count = len(self.memories[agent_id])
                del self.memories[agent_id]
                logger.info(f"Cleared {count} memories for agent {agent_id}")

                return {
                    "status": "success",
                    "message": f"Cleared {count} memories for agent {agent_id}",
                }
            else:
                return {"status": "success", "message": f"No memories found for agent {agent_id}"}

        except Exception as e:
            logger.error(f"Error clearing memories: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_memory_stats(self, agent_id: str = None) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            if agent_id:
                count = len(self.memories.get(agent_id, []))
                return {"agent_id": agent_id, "memory_count": count}
            else:
                stats = {
                    "total_agents": len(self.memories),
                    "total_memories": sum(len(mems) for mems in self.memories.values()),
                    "by_agent": {aid: len(mems) for aid, mems in self.memories.items()},
                }
                return stats

        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            raise HTTPException(status_code=500, detail=str(e))
