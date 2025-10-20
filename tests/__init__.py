"""
Test Suite für das AI-Agent-System
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# Füge das Projekt-Root zum Python-Pfad hinzu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test-Konfiguration
TEST_CONFIG = {
    "app": {
        "name": "AI Agent System Test",
        "version": "1.0.0-test",
        "debug": True,
        "log_level": "DEBUG",
        "host": "127.0.0.1",
        "port": 8001,
    },
    "database": {"url": "sqlite:///./test_agents.db"},
}


# Test-Fixtures
@pytest.fixture
def event_loop():
    """Erstellt einen Event Loop für asyncio-Tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_config():
    """Gibt Test-Konfiguration zurück"""
    return TEST_CONFIG


@pytest.fixture
def mock_api_keys():
    """Mock API-Schlüssel für Tests"""
    return {"openai": "test_openai_key", "google": "test_google_key", "claude": "test_claude_key"}
