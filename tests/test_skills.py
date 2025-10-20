"""
Tests für das Skills-System
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Füge das Projekt-Root zum Python-Pfad hinzu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from skills import APIIntegrationSkill, BaseSkill, DataAnalysisSkill, TextProcessingSkill


# Concrete test implementation of BaseSkill for testing
class TestSkill(BaseSkill):
    """Concrete implementation of BaseSkill for testing"""

    async def execute(self, operation: str, input_data: dict):
        return {"result": f"test_{operation}"}


class TestBaseSkill:
    """Test-Klasse für BaseSkill"""

    def test_base_skill_initialization(self):
        """Test für Skill-Initialisierung"""
        skill = TestSkill("test_skill", "Test skill description")

        assert skill.name == "test_skill"
        assert skill.description == "Test skill description"
        assert skill.status == "initialized"
        assert skill.parameters == {}

    def test_get_info(self):
        """Test für Skill-Info-Abfrage"""
        skill = TestSkill("test_skill", "Test description")
        skill.parameters = {"param1": "value1"}

        info = skill.get_info()

        assert info["name"] == "test_skill"
        assert info["description"] == "Test description"
        assert info["parameters"]["param1"] == "value1"
        assert info["status"] == "initialized"

    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test für Skill-Initialisierung"""
        skill = TestSkill("test_skill")

        await skill.initialize()

        assert skill.status == "ready"


class TestTextProcessingSkill:
    """Test-Klasse für TextProcessingSkill"""

    def test_text_processing_skill_initialization(self):
        """Test für TextProcessingSkill-Initialisierung"""
        skill = TextProcessingSkill()

        assert skill.name == "text_processing"
        assert "Verarbeitet und analysiert Text" in skill.description
        assert "operation" in skill.parameters
        assert "language" in skill.parameters
        assert "max_length" in skill.parameters

    @pytest.mark.asyncio
    async def test_execute_analyze_operation(self):
        """Test für Text-Analyse-Operation"""
        skill = TextProcessingSkill()

        result = await skill.execute("Hello World! This is a test.", {"operation": "analyze"})

        assert result["skill"] == "text_processing"
        assert result["operation"] == "analyze"
        assert result["input_length"] == 28
        assert result["status"] == "completed"

        # Prüfe Analyse-Ergebnisse
        analysis_result = result["result"]
        assert analysis_result["word_count"] == 6
        assert analysis_result["character_count"] == 28
        assert analysis_result["sentence_count"] == 1
        assert analysis_result["paragraph_count"] == 1
        assert analysis_result["average_word_length"] > 0

    @pytest.mark.asyncio
    async def test_execute_summarize_operation(self):
        """Test für Text-Zusammenfassung-Operation"""
        skill = TextProcessingSkill()

        long_text = "This is a very long text that should be summarized. " * 10

        result = await skill.execute(long_text, {"operation": "summarize", "max_length": 50})

        assert result["skill"] == "text_processing"
        assert result["operation"] == "summarize"
        assert result["status"] == "completed"

        # Prüfe, dass Text gekürzt wurde
        summary = result["result"]
        assert len(summary.split()) <= 50
        assert summary.endswith("...")

    @pytest.mark.asyncio
    async def test_execute_sentiment_operation_positive(self):
        """Test für Sentiment-Analyse mit positivem Text"""
        skill = TextProcessingSkill()

        result = await skill.execute(
            "This is a great and amazing product!", {"operation": "sentiment"}
        )

        assert result["skill"] == "text_processing"
        assert result["operation"] == "sentiment"
        assert result["status"] == "completed"

        sentiment_result = result["result"]
        assert sentiment_result["sentiment"] == "positive"
        assert sentiment_result["positive_score"] > 0
        assert sentiment_result["negative_score"] == 0

    @pytest.mark.asyncio
    async def test_execute_sentiment_operation_negative(self):
        """Test für Sentiment-Analyse mit negativem Text"""
        skill = TextProcessingSkill()

        result = await skill.execute(
            "This is a terrible and awful product!", {"operation": "sentiment"}
        )

        sentiment_result = result["result"]
        assert sentiment_result["sentiment"] == "negative"
        assert sentiment_result["negative_score"] > 0
        assert sentiment_result["positive_score"] == 0

    @pytest.mark.asyncio
    async def test_execute_sentiment_operation_neutral(self):
        """Test für Sentiment-Analyse mit neutralem Text"""
        skill = TextProcessingSkill()

        result = await skill.execute("This is a normal product.", {"operation": "sentiment"})

        sentiment_result = result["result"]
        assert sentiment_result["sentiment"] == "neutral"
        assert sentiment_result["positive_score"] == 0
        assert sentiment_result["negative_score"] == 0

    @pytest.mark.asyncio
    async def test_execute_unknown_operation(self):
        """Test für unbekannte Operation"""
        skill = TextProcessingSkill()

        result = await skill.execute("test text", {"operation": "unknown_operation"})

        assert result["skill"] == "text_processing"
        assert result["operation"] == "unknown_operation"
        assert result["status"] == "completed"
        assert "Unknown operation" in result["result"]

    @pytest.mark.asyncio
    async def test_execute_invalid_input(self):
        """Test für ungültige Eingabe"""
        skill = TextProcessingSkill()

        with pytest.raises(ValueError, match="Input data must be a string"):
            await skill.execute(123, {"operation": "analyze"})


class TestDataAnalysisSkill:
    """Test-Klasse für DataAnalysisSkill"""

    def test_data_analysis_skill_initialization(self):
        """Test für DataAnalysisSkill-Initialisierung"""
        skill = DataAnalysisSkill()

        assert skill.name == "data_analysis"
        assert "Analysiert und verarbeitet Daten" in skill.description
        assert "data_type" in skill.parameters
        assert "operation" in skill.parameters
        assert "filters" in skill.parameters

    @pytest.mark.asyncio
    async def test_execute_numbers_statistics(self):
        """Test für Zahlen-Statistik-Operation"""
        skill = DataAnalysisSkill()

        numbers = [1, 2, 3, 4, 5, 10, 15, 20]

        result = await skill.execute(numbers, {"data_type": "numbers", "operation": "statistics"})

        assert result["skill"] == "data_analysis"
        assert result["data_type"] == "numbers"
        assert result["operation"] == "statistics"
        assert result["status"] == "completed"

        stats = result["result"]
        assert stats["count"] == 8
        assert stats["sum"] == 60  # 1+2+3+4+5+10+15+20
        assert stats["mean"] == 7.5  # 60/8
        assert stats["min"] == 1
        assert stats["max"] == 20
        assert stats["range"] == 19  # 20-1

    @pytest.mark.asyncio
    async def test_execute_json_statistics(self):
        """Test für JSON-Statistik-Operation"""
        skill = DataAnalysisSkill()

        json_data = {
            "name": "John",
            "age": 30,
            "city": "New York",
            "hobbies": ["reading", "swimming"],
        }

        result = await skill.execute(json_data, {"data_type": "json", "operation": "statistics"})

        assert result["skill"] == "data_analysis"
        assert result["data_type"] == "json"
        assert result["operation"] == "statistics"
        assert result["status"] == "completed"

        stats = result["result"]
        assert "name" in stats["keys"]
        assert "age" in stats["keys"]
        assert "city" in stats["keys"]
        assert "hobbies" in stats["keys"]
        assert stats["key_count"] == 4
        assert stats["data_type"] == "dict"
        assert stats["size"] > 0

    @pytest.mark.asyncio
    async def test_execute_auto_type_detection_numbers(self):
        """Test für automatische Typ-Erkennung bei Zahlen"""
        skill = DataAnalysisSkill()

        numbers = [10, 20, 30, 40, 50]

        result = await skill.execute(numbers, {"data_type": "auto", "operation": "statistics"})

        assert result["data_type"] == "numbers"
        assert result["result"]["count"] == 5
        assert result["result"]["sum"] == 150

    @pytest.mark.asyncio
    async def test_execute_auto_type_detection_json(self):
        """Test für automatische Typ-Erkennung bei JSON"""
        skill = DataAnalysisSkill()

        json_data = {"key": "value", "number": 42}

        result = await skill.execute(json_data, {"data_type": "auto", "operation": "statistics"})

        assert result["data_type"] == "json"
        assert result["result"]["key_count"] == 2

    @pytest.mark.asyncio
    async def test_execute_auto_type_detection_text(self):
        """Test für automatische Typ-Erkennung bei Text"""
        skill = DataAnalysisSkill()

        text_data = "This is a text string"

        result = await skill.execute(text_data, {"data_type": "auto", "operation": "statistics"})

        assert result["data_type"] == "text"

    @pytest.mark.asyncio
    async def test_execute_auto_type_detection_list(self):
        """Test für automatische Typ-Erkennung bei Liste"""
        skill = DataAnalysisSkill()

        list_data = ["item1", "item2", "item3"]

        result = await skill.execute(list_data, {"data_type": "auto", "operation": "statistics"})

        assert result["data_type"] == "list"

    @pytest.mark.asyncio
    async def test_execute_unsupported_operation(self):
        """Test für nicht unterstützte Operation"""
        skill = DataAnalysisSkill()

        result = await skill.execute(
            [1, 2, 3], {"data_type": "numbers", "operation": "unsupported_operation"}
        )

        assert "not supported" in result["result"]

    @pytest.mark.asyncio
    async def test_execute_unsupported_data_type(self):
        """Test für nicht unterstützten Datentyp"""
        skill = DataAnalysisSkill()

        result = await skill.execute(
            "some data", {"data_type": "unsupported_type", "operation": "statistics"}
        )

        assert "not supported" in result["result"]


class TestAPIIntegrationSkill:
    """Test-Klasse für APIIntegrationSkill"""

    def test_api_integration_skill_initialization(self):
        """Test für APIIntegrationSkill-Initialisierung"""
        skill = APIIntegrationSkill()

        assert skill.name == "api_integration"
        assert "Integriert externe APIs" in skill.description
        assert "api_type" in skill.parameters
        assert "endpoint" in skill.parameters
        assert "method" in skill.parameters
        assert "headers" in skill.parameters
        assert "data" in skill.parameters

    @pytest.mark.asyncio
    async def test_execute_openai_api(self):
        """Test für OpenAI API-Integration"""
        skill = APIIntegrationSkill()

        result = await skill.execute("Hello, how are you?", {"api_type": "openai"})

        assert result["skill"] == "api_integration"
        assert result["api_type"] == "openai"
        assert result["status"] == "completed"

        api_result = result["result"]
        assert api_result["api_type"] == "openai"
        assert "OpenAI API call for:" in api_result["response"]
        assert "tokens_used" in api_result
        assert "model" in api_result
        assert api_result["model"] == "gpt-3.5-turbo"

    @pytest.mark.asyncio
    async def test_execute_google_api(self):
        """Test für Google API-Integration"""
        skill = APIIntegrationSkill()

        result = await skill.execute("Search query", {"api_type": "google"})

        assert result["skill"] == "api_integration"
        assert result["api_type"] == "google"
        assert result["status"] == "completed"

        api_result = result["result"]
        assert api_result["api_type"] == "google"
        assert "Google API call for:" in api_result["response"]
        assert "quota_used" in api_result
        assert "service" in api_result
        assert api_result["service"] == "custom-search"

    @pytest.mark.asyncio
    async def test_execute_claude_api(self):
        """Test für Claude API-Integration"""
        skill = APIIntegrationSkill()

        result = await skill.execute("Analyze this text", {"api_type": "claude"})

        assert result["skill"] == "api_integration"
        assert result["api_type"] == "claude"
        assert result["status"] == "completed"

        api_result = result["result"]
        assert api_result["api_type"] == "claude"
        assert "Claude API call for:" in api_result["response"]
        assert "tokens_used" in api_result
        assert "model" in api_result
        assert api_result["model"] == "claude-3-sonnet"

    @pytest.mark.asyncio
    async def test_execute_unknown_api_type(self):
        """Test für unbekannten API-Typ"""
        skill = APIIntegrationSkill()

        result = await skill.execute("test data", {"api_type": "unknown_api"})

        assert result["skill"] == "api_integration"
        assert result["api_type"] == "unknown_api"
        assert result["status"] == "completed"

        api_result = result["result"]
        assert api_result["api_type"] == "unknown_api"
        assert "Unknown API type" in api_result["response"]
        assert "error" in api_result
        assert "not supported" in api_result["error"]


@pytest.mark.asyncio
async def test_skills_initialization():
    """Test für Skills-Modul-Initialisierung"""
    from skills import initialize

    skills = await initialize()

    assert "text_processing" in skills
    assert "data_analysis" in skills
    assert "api_integration" in skills

    # Teste, dass alle Skills initialisiert sind
    for skill in skills.values():
        assert skill.status == "ready"
