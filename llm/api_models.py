"""
API-Modelle (OpenAI, Anthropic, Google)
"""

import asyncio
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


class APIModelManager:
    """Manager für API-basierte LLM-Modelle"""

    def __init__(self):
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "anthropic": os.getenv("ANTHROPIC_API_KEY"),
            "google": os.getenv("GOOGLE_API_KEY"),
        }

        self.api_endpoints = {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com/v1",
            "google": "https://generativelanguage.googleapis.com/v1",
        }

        self.available_models = []
        self.model_configs = {}

        # Standard-Modelle
        self.default_models = {
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"],
            "anthropic": [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
            ],
            "google": ["gemini-pro", "gemini-pro-vision", "text-bison-001"],
        }

        # Standard-Konfigurationen
        self.default_configs = {
            "openai": {
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            },
            "anthropic": {"temperature": 0.7, "max_tokens": 2048, "top_p": 0.9},
            "google": {"temperature": 0.7, "max_output_tokens": 2048, "top_p": 0.9, "top_k": 40},
        }

    async def initialize(self):
        """Initialisiert den API Model Manager"""
        try:
            # Lade verfügbare Modelle
            await self._load_available_models()

            logger.info(
                f"API Model Manager initialisiert: {len(self.available_models)} Modelle verfügbar"
            )

        except Exception as e:
            logger.error(f"Fehler bei der Initialisierung des API Model Managers: {e}")

    async def _load_available_models(self):
        """Lädt verfügbare API-Modelle"""
        self.available_models = []

        for provider, models in self.default_models.items():
            if self.api_keys[provider]:
                for model_name in models:
                    self.available_models.append(
                        {
                            "name": model_name,
                            "provider": provider,
                            "config": {
                                **self.default_configs[provider],
                                "api_key": self.api_keys[provider],
                                "endpoint": self.api_endpoints[provider],
                            },
                        }
                    )

    async def get_available_models(self) -> List[str]:
        """Gibt Liste der verfügbaren Modell-Namen zurück"""
        return [model["name"] for model in self.available_models]

    async def is_model_available(self, model_name: str) -> bool:
        """Prüft ob ein Modell verfügbar ist"""
        return model_name in await self.get_available_models()

    async def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Gibt Konfiguration für ein Modell zurück"""
        for model in self.available_models:
            if model["name"] == model_name:
                return model["config"]
        return {}

    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Gibt Informationen über ein Modell zurück"""
        for model in self.available_models:
            if model["name"] == model_name:
                return model
        return {}

    async def generate_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert eine Antwort mit einem API-Modell"""
        try:
            model_info = await self.get_model_info(model_name)
            if not model_info:
                raise ValueError(f"Modell {model_name} nicht gefunden")

            provider = model_info["provider"]

            if provider == "openai":
                return await self._generate_openai_response(model_name, prompt, **kwargs)
            elif provider == "anthropic":
                return await self._generate_anthropic_response(model_name, prompt, **kwargs)
            elif provider == "google":
                return await self._generate_google_response(model_name, prompt, **kwargs)
            else:
                raise ValueError(f"Unbekannter Provider: {provider}")

        except Exception as e:
            logger.error(f"Fehler bei der API-Antwort-Generierung: {e}")
            raise

    async def _generate_openai_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit OpenAI"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                "frequency_penalty": kwargs.get(
                    "frequency_penalty", config.get("frequency_penalty", 0.0)
                ),
                "presence_penalty": kwargs.get(
                    "presence_penalty", config.get("presence_penalty", 0.0)
                ),
            }

            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        raise Exception(f"OpenAI-Fehler {response.status}: {error_text}")

        except Exception as e:
            logger.error(f"Fehler bei OpenAI-Antwort: {e}")
            raise

    async def _generate_anthropic_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit Anthropic"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                "messages": [{"role": "user", "content": prompt}],
            }

            headers = {
                "x-api-key": config["api_key"],
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/messages", json=payload, headers=headers, timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["content"][0]["text"]
                    else:
                        error_text = await response.text()
                        raise Exception(f"Anthropic-Fehler {response.status}: {error_text}")

        except Exception as e:
            logger.error(f"Fehler bei Anthropic-Antwort: {e}")
            raise

    async def _generate_google_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit Google"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                    "maxOutputTokens": kwargs.get(
                        "max_tokens", config.get("max_output_tokens", 2048)
                    ),
                    "topP": kwargs.get("top_p", config.get("top_p", 0.9)),
                    "topK": kwargs.get("top_k", config.get("top_k", 40)),
                },
            }

            params = {"key": config["api_key"]}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/models/{model_name}:generateContent",
                    json=payload,
                    params=params,
                    timeout=60,
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        error_text = await response.text()
                        raise Exception(f"Google-Fehler {response.status}: {error_text}")

        except Exception as e:
            logger.error(f"Fehler bei Google-Antwort: {e}")
            raise

    async def generate_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert eine Streaming-Antwort"""
        try:
            model_info = await self.get_model_info(model_name)
            if not model_info:
                raise ValueError(f"Modell {model_name} nicht gefunden")

            provider = model_info["provider"]

            if provider == "openai":
                async for chunk in self._generate_openai_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            elif provider == "anthropic":
                async for chunk in self._generate_anthropic_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            elif provider == "google":
                async for chunk in self._generate_google_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            else:
                raise ValueError(f"Unbekannter Provider: {provider}")

        except Exception as e:
            logger.error(f"Fehler bei der API-Streaming-Antwort: {e}")
            raise

    async def _generate_openai_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit OpenAI"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                "stream": True,
            }

            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=60,
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                line_str = line.decode("utf-8")
                                if line_str.startswith("data: "):
                                    data_str = line_str[6:]
                                    if data_str.strip() == "[DONE]":
                                        break
                                    try:
                                        import json

                                        data = json.loads(data_str)
                                        if "choices" in data and len(data["choices"]) > 0:
                                            delta = data["choices"][0].get("delta", {})
                                            if "content" in delta:
                                                yield delta["content"]
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        error_text = await response.text()
                        raise Exception(f"OpenAI-Streaming-Fehler {response.status}: {error_text}")

        except Exception as e:
            logger.error(f"Fehler bei OpenAI-Streaming: {e}")
            raise

    async def _generate_anthropic_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit Anthropic"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                "messages": [{"role": "user", "content": prompt}],
                "stream": True,
            }

            headers = {
                "x-api-key": config["api_key"],
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/messages", json=payload, headers=headers, timeout=60
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                line_str = line.decode("utf-8")
                                if line_str.startswith("data: "):
                                    data_str = line_str[6:]
                                    if data_str.strip() == "[DONE]":
                                        break
                                    try:
                                        import json

                                        data = json.loads(data_str)
                                        if "type" in data and data["type"] == "content_block_delta":
                                            if "delta" in data and "text" in data["delta"]:
                                                yield data["delta"]["text"]
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        error_text = await response.text()
                        raise Exception(
                            f"Anthropic-Streaming-Fehler {response.status}: {error_text}"
                        )

        except Exception as e:
            logger.error(f"Fehler bei Anthropic-Streaming: {e}")
            raise

    async def _generate_google_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit Google"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                    "maxOutputTokens": kwargs.get(
                        "max_tokens", config.get("max_output_tokens", 2048)
                    ),
                    "topP": kwargs.get("top_p", config.get("top_p", 0.9)),
                    "topK": kwargs.get("top_k", config.get("top_k", 40)),
                },
            }

            params = {"key": config["api_key"]}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['endpoint']}/models/{model_name}:streamGenerateContent",
                    json=payload,
                    params=params,
                    timeout=60,
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                line_str = line.decode("utf-8")
                                if line_str.startswith("data: "):
                                    data_str = line_str[6:]
                                    try:
                                        import json

                                        data = json.loads(data_str)
                                        if "candidates" in data and len(data["candidates"]) > 0:
                                            candidate = data["candidates"][0]
                                            if (
                                                "content" in candidate
                                                and "parts" in candidate["content"]
                                            ):
                                                for part in candidate["content"]["parts"]:
                                                    if "text" in part:
                                                        yield part["text"]
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        error_text = await response.text()
                        raise Exception(f"Google-Streaming-Fehler {response.status}: {error_text}")

        except Exception as e:
            logger.error(f"Fehler bei Google-Streaming: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Führt einen Health-Check durch"""
        try:
            health_status = {
                "status": "healthy",
                "available_providers": [],
                "available_models": len(self.available_models),
                "errors": [],
            }

            # Prüfe API-Keys
            for provider, api_key in self.api_keys.items():
                if api_key and api_key != f"your_{provider}_api_key_here":
                    health_status["available_providers"].append(provider)
                else:
                    health_status["errors"].append(f"API-Key für {provider} nicht konfiguriert")

            if not health_status["available_providers"]:
                health_status["status"] = "unhealthy"
                health_status["errors"].append("Keine API-Keys konfiguriert")

            return health_status

        except Exception as e:
            logger.error(f"Fehler beim Health-Check: {e}")
            return {"status": "error", "error": str(e)}

    async def cleanup(self):
        """Bereinigt Ressourcen"""
        try:
            # Schließe offene Verbindungen
            logger.info("API Model Manager bereinigt")

        except Exception as e:
            logger.error(f"Fehler bei der Bereinigung: {e}")
