"""
Model Manager für LLM-Integration
"""

import asyncio
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from .api_models import APIModelManager
from .local_models import LocalModelManager

logger = logging.getLogger(__name__)


class ModelManager:
    """Hauptklasse für LLM-Modell-Management"""

    def __init__(self):
        self.local_manager = LocalModelManager()
        self.api_manager = APIModelManager()
        self.current_model = None
        self.model_type = None  # 'local' oder 'api'
        self.model_config = {}

    async def initialize(self):
        """Initialisiert den Model Manager"""
        try:
            # Initialisiere lokale Modelle
            await self.local_manager.initialize()

            # Initialisiere API-Modelle
            await self.api_manager.initialize()

            # Setze Standard-Modell
            await self.set_default_model()

            logger.info("Model Manager initialisiert")

        except Exception as e:
            logger.error(f"Fehler bei der Model Manager-Initialisierung: {e}")
            raise

    async def set_default_model(self):
        """Setzt das Standard-Modell"""
        try:
            # Prüfe verfügbare Modelle
            local_models = await self.local_manager.get_available_models()
            api_models = await self.api_manager.get_available_models()

            # Priorisiere lokale Modelle
            if local_models:
                self.current_model = local_models[0]
                self.model_type = "local"
                self.model_config = await self.local_manager.get_model_config(self.current_model)
            elif api_models:
                self.current_model = api_models[0]
                self.model_type = "api"
                self.model_config = await self.api_manager.get_model_config(self.current_model)
            else:
                logger.warning("Keine Modelle verfügbar")

        except Exception as e:
            logger.error(f"Fehler beim Setzen des Standard-Modells: {e}")

    async def set_model(self, model_name: str, model_type: str = "auto"):
        """
        Setzt das aktuelle Modell

        Args:
            model_name: Name des Modells
            model_type: 'local', 'api' oder 'auto'
        """
        try:
            if model_type == "auto":
                # Prüfe zuerst lokale Modelle
                local_models = await self.local_manager.get_available_models()
                if model_name in local_models:
                    model_type = "local"
                else:
                    model_type = "api"

            if model_type == "local":
                if await self.local_manager.is_model_available(model_name):
                    self.current_model = model_name
                    self.model_type = "local"
                    self.model_config = await self.local_manager.get_model_config(model_name)
                    logger.info(f"Lokales Modell gesetzt: {model_name}")
                else:
                    raise ValueError(f"Lokales Modell {model_name} nicht verfügbar")

            elif model_type == "api":
                if await self.api_manager.is_model_available(model_name):
                    self.current_model = model_name
                    self.model_type = "api"
                    self.model_config = await self.api_manager.get_model_config(model_name)
                    logger.info(f"API-Modell gesetzt: {model_name}")
                else:
                    raise ValueError(f"API-Modell {model_name} nicht verfügbar")

            else:
                raise ValueError(f"Unbekannter Modell-Typ: {model_type}")

        except Exception as e:
            logger.error(f"Fehler beim Setzen des Modells: {e}")
            raise

    async def generate_response(self, prompt: str, **kwargs) -> str:
        """
        Generiert eine Antwort mit dem aktuellen Modell

        Args:
            prompt: Eingabe-Prompt
            **kwargs: Zusätzliche Parameter

        Returns:
            Generierte Antwort
        """
        try:
            if not self.current_model:
                raise ValueError("Kein Modell ausgewählt")

            if self.model_type == "local":
                return await self.local_manager.generate_response(
                    self.current_model, prompt, **kwargs
                )
            elif self.model_type == "api":
                return await self.api_manager.generate_response(
                    self.current_model, prompt, **kwargs
                )
            else:
                raise ValueError(f"Unbekannter Modell-Typ: {self.model_type}")

        except Exception as e:
            logger.error(f"Fehler bei der Antwort-Generierung: {e}")
            raise

    async def generate_streaming_response(self, prompt: str, **kwargs):
        """
        Generiert eine Streaming-Antwort

        Args:
            prompt: Eingabe-Prompt
            **kwargs: Zusätzliche Parameter

        Yields:
            Antwort-Chunks
        """
        try:
            if not self.current_model:
                raise ValueError("Kein Modell ausgewählt")

            if self.model_type == "local":
                async for chunk in self.local_manager.generate_streaming_response(
                    self.current_model, prompt, **kwargs
                ):
                    yield chunk
            elif self.model_type == "api":
                async for chunk in self.api_manager.generate_streaming_response(
                    self.current_model, prompt, **kwargs
                ):
                    yield chunk
            else:
                raise ValueError(f"Unbekannter Modell-Typ: {self.model_type}")

        except Exception as e:
            logger.error(f"Fehler bei der Streaming-Antwort: {e}")
            raise

    async def get_available_models(self) -> Dict[str, List[str]]:
        """Gibt alle verfügbaren Modelle zurück"""
        try:
            local_models = await self.local_manager.get_available_models()
            api_models = await self.api_manager.get_available_models()

            return {"local": local_models, "api": api_models}

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der verfügbaren Modelle: {e}")
            return {"local": [], "api": []}

    async def get_model_info(self, model_name: str, model_type: str = "auto") -> Dict[str, Any]:
        """Gibt Informationen über ein Modell zurück"""
        try:
            if model_type == "auto":
                local_models = await self.local_manager.get_available_models()
                if model_name in local_models:
                    model_type = "local"
                else:
                    model_type = "api"

            if model_type == "local":
                return await self.local_manager.get_model_info(model_name)
            elif model_type == "api":
                return await self.api_manager.get_model_info(model_name)
            else:
                raise ValueError(f"Unbekannter Modell-Typ: {model_type}")

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Modell-Informationen: {e}")
            return {}

    async def test_model(self, model_name: str, model_type: str = "auto") -> Dict[str, Any]:
        """Testet ein Modell"""
        try:
            if model_type == "auto":
                local_models = await self.local_manager.get_available_models()
                if model_name in local_models:
                    model_type = "local"
                else:
                    model_type = "api"

            test_prompt = "Hallo! Bist du bereit, mir bei der Projektanalyse zu helfen?"

            if model_type == "local":
                response = await self.local_manager.generate_response(model_name, test_prompt)
            elif model_type == "api":
                response = await self.api_manager.generate_response(model_name, test_prompt)
            else:
                raise ValueError(f"Unbekannter Modell-Typ: {model_type}")

            return {
                "model_name": model_name,
                "model_type": model_type,
                "status": "success",
                "response": response,
                "response_length": len(response),
            }

        except Exception as e:
            logger.error(f"Fehler beim Testen des Modells: {e}")
            return {
                "model_name": model_name,
                "model_type": model_type,
                "status": "error",
                "error": str(e),
            }

    def get_current_model(self) -> Dict[str, Any]:
        """Gibt das aktuelle Modell zurück"""
        return {"name": self.current_model, "type": self.model_type, "config": self.model_config}

    async def health_check(self) -> Dict[str, Any]:
        """Führt einen Health-Check durch"""
        try:
            health_status = {
                "local_manager": await self.local_manager.health_check(),
                "api_manager": await self.api_manager.health_check(),
                "current_model": self.get_current_model(),
            }

            # Gesamt-Status
            if (
                health_status["local_manager"]["status"] == "healthy"
                or health_status["api_manager"]["status"] == "healthy"
            ):
                health_status["overall_status"] = "healthy"
            else:
                health_status["overall_status"] = "unhealthy"

            return health_status

        except Exception as e:
            logger.error(f"Fehler beim Health-Check: {e}")
            return {"overall_status": "error", "error": str(e)}

    async def cleanup(self):
        """Bereinigt Ressourcen"""
        try:
            await self.local_manager.cleanup()
            await self.api_manager.cleanup()
            logger.info("Model Manager bereinigt")

        except Exception as e:
            logger.error(f"Fehler bei der Bereinigung: {e}")
