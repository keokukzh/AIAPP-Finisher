"""Example agents for the AI Agent System.

Provides simple example implementations for task execution, conversational
responses, and data processing to demonstrate agent patterns. These classes
are lightweight stand-ins for richer base classes that may exist in a
full implementation.

Typical usage example:
    task_agent = ExampleTaskAgent()
    result = await task_agent.run("greet")
    print(result["result"])  # -> "Hello! I'm the example task agent..."
"""

import asyncio

# Base classes not available - using simple implementation
# from agents.base_agent import BaseAgent, TaskAgent, ConversationalAgent, DataProcessingAgent
from typing import Any, Dict, Optional


class BaseAgent:
    """Base class for all agents.

    Attributes:
        name: Unique agent identifier.
        description: Short agent description.
    """

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class TaskAgent(BaseAgent):
    """Agent for task execution."""

    def __init__(self, name: str, description: str, task_type: str) -> None:
        super().__init__(name, description)
        self.task_type = task_type


class ConversationalAgent(BaseAgent):
    """Agent for conversations."""

    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)


class DataProcessingAgent(BaseAgent):
    """Agent for data processing."""

    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)


class ExampleTaskAgent(TaskAgent):
    """Beispiel-Agent für allgemeine Aufgaben"""

    def __init__(self) -> None:
        super().__init__(
            name="example_task_agent",
            description="Ein Beispiel-Agent für allgemeine Aufgaben",
            task_type="example",
        )

    async def run(self, task: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute simple example tasks.

        Args:
            task: Short task description (e.g., "greet", "calculate").
            parameters: Optional parameter dictionary for task execution.

        Returns:
            Dictionary containing task, agent name, computed result, original parameters,
            and status field.
        """
        self.logger.info(f"Example agent executing task: {task}")

        # Simuliere Verarbeitungszeit
        await asyncio.sleep(0.1)

        # Beispiel-Logik basierend auf Task-Typ
        if "greet" in task.lower():
            result = "Hello! I'm the example task agent. Nice to meet you!"
        elif "calculate" in task.lower():
            # Einfache Berechnung
            numbers = parameters.get("numbers", [1, 2, 3]) if parameters else [1, 2, 3]
            result = f"Sum of {numbers} is {sum(numbers)}"
        elif "analyze" in task.lower():
            text = parameters.get("text", "Hello World") if parameters else "Hello World"
            result = f"Analysis of '{text}': {len(text)} characters, {len(text.split())} words"
        else:
            result = f"I processed the task: '{task}' with parameters: {parameters or {}}"

        return {
            "task": task,
            "agent": self.name,
            "result": result,
            "parameters": parameters or {},
            "status": "completed",
        }


class ExampleConversationalAgent(ConversationalAgent):
    """Beispiel-Agent für Konversationen"""

    def __init__(self) -> None:
        super().__init__(
            name="example_conversational_agent",
            description="Ein freundlicher Konversations-Agent",
            personality="helpful and friendly",
        )

    async def run(self, task: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process conversational requests and produce a natural response.

        Args:
            task: User utterance or conversational input.
            parameters: Optional extra inputs for the conversational context.

        Returns:
            Dictionary with the original task, agent name, generated response,
            conversation length, personality marker, and status.
        """
        self.logger.info(f"Conversational agent processing: {task}")

        # Simuliere Verarbeitungszeit
        await asyncio.sleep(0.05)

        # Einfache Konversationslogik
        task_lower = task.lower()

        if any(word in task_lower for word in ["hello", "hi", "hey"]):
            response = f"Hello there! I'm {self.name}. How can I help you today?"
        elif any(word in task_lower for word in ["how", "what", "why", "when", "where"]):
            response = (
                f"That's an interesting question: '{task}'. I'm here to help you find answers!"
            )
        elif any(word in task_lower for word in ["thank", "thanks"]):
            response = "You're very welcome! I'm happy to help."
        else:
            response = f"I understand you're saying: '{task}'. That's interesting! Tell me more."

        # Speichere in Historie
        self.conversation_history.append(
            {"input": task, "response": response, "timestamp": self._get_timestamp()}
        )

        return {
            "task": task,
            "agent": self.name,
            "response": response,
            "conversation_length": len(self.conversation_history),
            "personality": self.personality,
            "status": "completed",
        }


class ExampleDataAgent(DataProcessingAgent):
    """Beispiel-Agent für Datenverarbeitung"""

    def __init__(self) -> None:
        super().__init__(
            name="example_data_agent",
            description="Ein Agent für Datenverarbeitung und -analyse",
            data_types=["text", "json", "numbers", "list"],
        )

    async def run(self, task: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process various data types and return computed results.

        Args:
            task: Logical operation name or description.
            parameters: Dictionary containing 'data' and 'data_type'.

        Returns:
            Dictionary with original data, derived metrics, counters and status.

        Raises:
            ValueError: If required parameters are missing.
        """
        self.logger.info(f"Data agent processing: {task}")

        if not parameters:
            raise ValueError("Data processing requires parameters with 'data' and 'data_type'")

        data = parameters.get("data")
        data_type = parameters.get("data_type", "text")

        if data is None:
            raise ValueError("Parameter 'data' is required")

        # Simuliere Verarbeitungszeit
        await asyncio.sleep(0.1)

        # Verarbeitung basierend auf Datentyp
        if data_type == "text":
            processed = {
                "length": len(str(data)),
                "words": len(str(data).split()),
                "uppercase": str(data).upper(),
                "lowercase": str(data).lower(),
            }
        elif data_type == "json":
            import json

            try:
                if isinstance(data, str):
                    parsed = json.loads(data)
                else:
                    parsed = data
                processed = {
                    "keys": list(parsed.keys()) if isinstance(parsed, dict) else "Not a dict",
                    "type": type(parsed).__name__,
                    "size": len(str(parsed)),
                }
            except json.JSONDecodeError:
                processed = {"error": "Invalid JSON"}
        elif data_type == "numbers":
            try:
                numbers = [float(x) for x in str(data).split()]
                processed = {
                    "sum": sum(numbers),
                    "average": sum(numbers) / len(numbers) if numbers else 0,
                    "min": min(numbers) if numbers else 0,
                    "max": max(numbers) if numbers else 0,
                    "count": len(numbers),
                }
            except ValueError:
                processed = {"error": "Invalid numbers"}
        elif data_type == "list":
            try:
                items = list(data) if not isinstance(data, list) else data
                processed = {
                    "length": len(items),
                    "first": items[0] if items else None,
                    "last": items[-1] if items else None,
                    "unique_count": len(set(str(x) for x in items)),
                }
            except Exception:
                processed = {"error": "Invalid list data"}
        else:
            processed = {"error": f"Unsupported data type: {data_type}"}

        self.processed_items += 1

        return {
            "task": task,
            "agent": self.name,
            "data_type": data_type,
            "original_data": str(data)[:100] + "..." if len(str(data)) > 100 else str(data),
            "processed_data": processed,
            "total_processed": self.processed_items,
            "status": "completed",
        }


# Initialisierungsfunktion für das Modul
async def initialize() -> Dict[str, Any]:
    """Initialize example agents and return instances.

    Returns:
        Mapping of agent role names to their instantiated objects.
    """
    print("Initializing example agents...")

    # Erstelle Beispiel-Agenten
    task_agent = ExampleTaskAgent()
    conversational_agent = ExampleConversationalAgent()
    data_agent = ExampleDataAgent()

    # Initialisiere sie
    await task_agent.initialize()
    await conversational_agent.initialize()
    await data_agent.initialize()

    print("Example agents initialized successfully!")

    return {
        "task_agent": task_agent,
        "conversational_agent": conversational_agent,
        "data_agent": data_agent,
    }
