"""
Tests für das Agent-System
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Füge das Projekt-Root zum Python-Pfad hinzu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents import BaseAgent, ConversationalAgent, DataProcessingAgent, TaskAgent


class TestBaseAgent:
    """Test-Klasse für BaseAgent"""

    def test_base_agent_initialization(self):
        """Test für Agent-Initialisierung"""
        # Use TaskAgent instead of abstract BaseAgent
        agent = TaskAgent("test_agent", "Test agent description")

        assert agent.name == "test_agent"
        assert agent.description == "Test agent description"
        assert agent.status == "initialized"
        assert len(agent.skills) == 0

    def test_add_skill(self):
        """Test für Skill-Hinzufügung"""
        agent = TaskAgent("test_agent")
        mock_skill = MagicMock()
        mock_skill.__class__.__name__ = "TestSkill"

        agent.add_skill(mock_skill)

        assert len(agent.skills) == 1
        assert mock_skill in agent.skills

    def test_get_status(self):
        """Test für Status-Abfrage"""
        agent = TaskAgent("test_agent", "Test description")
        mock_skill = MagicMock()
        mock_skill.__class__.__name__ = "TestSkill"
        agent.add_skill(mock_skill)

        status = agent.get_status()

        assert status["name"] == "test_agent"
        assert status["description"] == "Test description"
        assert status["status"] == "initialized"
        assert status["skills_count"] == 1
        assert "TestSkill" in status["skills"]

    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test für Agent-Initialisierung"""
        agent = TaskAgent("test_agent")

        await agent.initialize()

        assert agent.status == "ready"


class TestTaskAgent:
    """Test-Klasse für TaskAgent"""

    def test_task_agent_initialization(self):
        """Test für TaskAgent-Initialisierung"""
        agent = TaskAgent("task_agent", "Task agent description", "custom")

        assert agent.name == "task_agent"
        assert agent.description == "Task agent description"
        assert agent.task_type == "custom"

    @pytest.mark.asyncio
    async def test_run_general_task(self):
        """Test für allgemeine Task-Ausführung"""
        agent = TaskAgent("task_agent")

        result = await agent.run("test task", {"param1": "value1"})

        assert result["task"] == "test task"
        assert result["agent"] == "task_agent"
        assert result["task_type"] == "general"
        assert result["parameters"]["param1"] == "value1"
        assert result["status"] == "completed"
        assert "result" in result


class TestConversationalAgent:
    """Test-Klasse für ConversationalAgent"""

    def test_conversational_agent_initialization(self):
        """Test für ConversationalAgent-Initialisierung"""
        agent = ConversationalAgent("conv_agent", "Conversational agent", "friendly")

        assert agent.name == "conv_agent"
        assert agent.description == "Conversational agent"
        assert agent.personality == "friendly"
        assert len(agent.conversation_history) == 0

    @pytest.mark.asyncio
    async def test_run_conversation(self):
        """Test für Konversations-Ausführung"""
        agent = ConversationalAgent("conv_agent")

        result = await agent.run("Hello there!", {"context": "greeting"})

        assert result["task"] == "Hello there!"
        assert result["agent"] == "conv_agent"
        assert result["personality"] == "helpful"
        assert "response" in result
        assert result["conversation_length"] == 1
        assert result["status"] == "completed"

        # Prüfe Konversationshistorie
        assert len(agent.conversation_history) == 1
        assert agent.conversation_history[0]["input"] == "Hello there!"

    def test_get_conversation_history(self):
        """Test für Konversationshistorie"""
        agent = ConversationalAgent("conv_agent")

        # Simuliere Konversation
        agent.conversation_history = [
            {"input": "Hello", "timestamp": "2023-01-01T00:00:00"},
            {"input": "How are you?", "timestamp": "2023-01-01T00:01:00"},
        ]

        history = agent.get_conversation_history()

        assert len(history) == 2
        assert history[0]["input"] == "Hello"
        assert history[1]["input"] == "How are you?"


class TestDataProcessingAgent:
    """Test-Klasse für DataProcessingAgent"""

    def test_data_processing_agent_initialization(self):
        """Test für DataProcessingAgent-Initialisierung"""
        agent = DataProcessingAgent("data_agent", "Data processing agent", ["text", "json"])

        assert agent.name == "data_agent"
        assert agent.description == "Data processing agent"
        assert agent.data_types == ["text", "json"]
        assert agent.processed_items == 0

    @pytest.mark.asyncio
    async def test_run_text_processing(self):
        """Test für Text-Verarbeitung"""
        agent = DataProcessingAgent("data_agent")

        result = await agent.run("process text", {"data": "Hello World", "data_type": "text"})

        assert result["task"] == "process text"
        assert result["agent"] == "data_agent"
        assert result["data_type"] == "text"
        assert result["total_processed"] == 1
        assert result["status"] == "completed"
        assert "processed_data" in result

    @pytest.mark.asyncio
    async def test_run_json_processing(self):
        """Test für JSON-Verarbeitung"""
        agent = DataProcessingAgent("data_agent")

        result = await agent.run(
            "process json", {"data": {"key": "value", "number": 42}, "data_type": "json"}
        )

        assert result["data_type"] == "json"
        assert result["total_processed"] == 1
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_run_unsupported_data_type(self):
        """Test für nicht unterstützten Datentyp"""
        agent = DataProcessingAgent("data_agent", data_types=["text"])

        with pytest.raises(ValueError, match="Unsupported data type"):
            await agent.run("process data", {"data": "some data", "data_type": "unsupported"})


class TestExampleAgents:
    """Test-Klasse für Beispiel-Agenten"""

    @pytest.mark.asyncio
    async def test_example_task_agent_greet(self):
        """Test für TaskAgent mit Greet-Task"""
        agent = TaskAgent("example_task_agent", "Example task agent for testing")

        result = await agent.run("greet user")

        assert result["task"] == "greet user"
        assert result["agent"] == "example_task_agent"
        assert "greet user" in result["result"]
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_example_task_agent_calculate(self):
        """Test für TaskAgent mit Calculate-Task"""
        agent = TaskAgent("example_task_agent", "Example task agent for testing")

        result = await agent.run("calculate sum", {"numbers": [1, 2, 3, 4, 5]})

        assert result["task"] == "calculate sum"
        assert result["agent"] == "example_task_agent"
        assert result["status"] == "completed"
        assert "calculate sum" in result["result"]

    @pytest.mark.asyncio
    async def test_example_task_agent_analyze(self):
        """Test für TaskAgent mit Analyze-Task"""
        agent = TaskAgent("test_agent", "Test agent")

        result = await agent.run("analyze text", {"text": "Hello World Test"})

        assert result["task"] == "analyze text"
        assert result["agent"] == "test_agent"
        assert result["status"] == "completed"
        assert "analyze text" in result["result"]

    @pytest.mark.asyncio
    async def test_example_conversational_agent_greeting(self):
        """Test für ConversationalAgent mit Begrüßung"""
        agent = ConversationalAgent("test_conversational_agent", "Test conversational agent")

        result = await agent.run("Hello there!")

        assert result["task"] == "Hello there!"
        assert result["agent"] == "test_conversational_agent"
        assert "Hello" in result["response"]
        assert result["conversation_length"] == 1
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_example_conversational_agent_question(self):
        """Test für ConversationalAgent mit Frage"""
        agent = ConversationalAgent("test_conversational_agent", "Test conversational agent")

        result = await agent.run("How are you doing?")

        assert result["task"] == "How are you doing?"
        assert result["agent"] == "test_conversational_agent"
        assert result["status"] == "completed"
        assert len(result["response"]) > 0

    @pytest.mark.asyncio
    async def test_example_conversational_agent_thanks(self):
        """Test für ConversationalAgent mit Dank"""
        agent = ConversationalAgent("test_conversational_agent", "Test conversational agent")

        result = await agent.run("Thank you very much!")

        assert result["task"] == "Thank you very much!"
        assert result["status"] == "completed"
        assert len(result["response"]) > 0

    @pytest.mark.asyncio
    async def test_example_data_agent_text_processing(self):
        """Test für DataProcessingAgent mit Text-Verarbeitung"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        result = await agent.run("process text data", {"data": "Hello World", "data_type": "text"})

        assert result["task"] == "process text data"
        assert result["agent"] == "test_data_agent"
        assert result["data_type"] == "text"
        assert result["total_processed"] == 1
        assert result["status"] == "completed"
        assert "Processed text data" in result["processed_data"]

    @pytest.mark.asyncio
    async def test_example_data_agent_json_processing(self):
        """Test für DataProcessingAgent with JSON-Verarbeitung"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        result = await agent.run(
            "process json data", {"data": '{"name": "John", "age": 30}', "data_type": "json"}
        )

        assert result["data_type"] == "json"
        assert result["agent"] == "test_data_agent"
        assert result["status"] == "completed"
        assert "Processed json data" in result["processed_data"]

    @pytest.mark.asyncio
    async def test_example_data_agent_csv_processing(self):
        """Test für DataProcessingAgent mit CSV-Verarbeitung"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        result = await agent.run(
            "process csv", {"data": "name,age\nJohn,30\nJane,25", "data_type": "csv"}
        )

        assert result["data_type"] == "csv"
        assert result["agent"] == "test_data_agent"
        assert result["status"] == "completed"
        assert "Processed csv data" in result["processed_data"]

    @pytest.mark.asyncio
    async def test_example_data_agent_unsupported_type(self):
        """Test für DataProcessingAgent mit unsupportedtype"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        with pytest.raises(ValueError, match="Unsupported data type"):
            await agent.run("process list", {"data": ["apple", "banana"], "data_type": "list"})

    @pytest.mark.asyncio
    async def test_example_data_agent_missing_parameters(self):
        """Test für DataProcessingAgent ohne Parameter"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        # Without parameters, data will be empty string
        result = await agent.run("process data")
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_example_data_agent_missing_data(self):
        """Test für DataProcessingAgent ohne Daten"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        # Without data param, it defaults to empty string
        result = await agent.run("process data", {"data_type": "text"})
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_example_data_agent_text_only(self):
        """Test für DataProcessingAgent mit nur Text"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        result = await agent.run("process text", {"data": "sample text data", "data_type": "text"})

        assert result["data_type"] == "text"
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_example_data_agent_unsupported_numbers(self):
        """Test für DataProcessingAgent mit unsupported numbers type"""
        agent = DataProcessingAgent("test_data_agent", "Test data processing agent")

        # Numbers is not a supported data type, should raise ValueError
        with pytest.raises(ValueError, match="Unsupported data type"):
            await agent.run(
                "process numbers", {"data": "not numbers at all", "data_type": "numbers"}
            )


@pytest.mark.asyncio
async def test_agent_initialization():
    """Test für Agent-Modul-Initialisierung"""
    # Test basic agent initialization from base module
    task_agent = TaskAgent("test_agent", "Test task agent")
    conv_agent = ConversationalAgent("conv_agent", "Test conversational agent")
    data_agent = DataProcessingAgent("data_agent", "Test data agent")

    # Initialize agents
    await task_agent.initialize()
    await conv_agent.initialize()
    await data_agent.initialize()

    # Teste, dass alle Agenten initialisiert sind
    assert task_agent.status == "ready"
    assert conv_agent.status == "ready"
    assert data_agent.status == "ready"
