"""
Intent Analyzer - Analyzes user intent from messages
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class IntentAnalyzer:
    """Analyzes user intent from chat messages"""

    def __init__(self):
        self.intent_keywords = {
            "project_analysis": ["analysiere", "analyse", "übersicht", "bewerte", "beurteile"],
            "optimization": ["optimiere", "verbesser", "performance", "schneller", "effizienter"],
            "testing": ["test", "tests", "testing", "prüfe", "validiere"],
            "security": ["security", "sicherheit", "vulnerabilit", "schwachstelle"],
            "deployment": ["deploy", "deployment", "produktion", "release", "veröffentlich"],
            "documentation": ["dokumentation", "docs", "dokumentiere", "beschreibe"],
            "code_review": ["review", "code", "bewerte", "prüfe code", "feedback"],
        }

    async def analyze_intent(self, user_message: str) -> Dict[str, Any]:
        """Analysiert die User-Intent"""
        message_lower = user_message.lower()

        detected_intent = "general"
        confidence = 0.0

        for intent_type, keywords in self.intent_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > 0:
                confidence = matches / len(keywords)
                if confidence > 0.1:  # Mindest-Confidence
                    detected_intent = intent_type
                    break

        return {
            "type": detected_intent,
            "confidence": confidence,
            "keywords_found": [
                kw for kw in self.intent_keywords.get(detected_intent, []) if kw in message_lower
            ],
        }
