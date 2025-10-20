"""
Lokale LLM-Modelle (Ollama, LM Studio, GPT4All)
"""

import asyncio
import json
import logging
import os
from typing import Any, AsyncGenerator, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


class LocalModelManager:
    """Manager für lokale LLM-Modelle"""

    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.lmstudio_host = os.getenv("LMSTUDIO_HOST", "http://localhost:1234")
        self.gpt4all_path = os.getenv("GPT4ALL_PATH", os.path.expanduser("~/.cache/gpt4all/"))

        self.available_models = []
        self.model_configs = {}

        # Model-Konfigurationen
        self.default_configs = {
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
        }

    async def initialize(self):
        """Initialisiert den lokalen Model Manager"""
        try:
            # Prüfe verfügbare Services
            await self._check_services()

            # Lade verfügbare Modelle
            await self._load_available_models()

            logger.info(
                f"Lokaler Model Manager initialisiert: {len(self.available_models)} Modelle verfügbar"
            )

        except Exception as e:
            logger.error(f"Fehler bei der Initialisierung des lokalen Model Managers: {e}")

    async def _check_services(self):
        """Prüft verfügbare lokale Services"""
        self.services = {
            "ollama": await self._check_ollama(),
            "lmstudio": await self._check_lmstudio(),
            "gpt4all": await self._check_gpt4all(),
        }

        logger.info(f"Verfügbare Services: {[k for k, v in self.services.items() if v]}")

    async def _check_ollama(self) -> bool:
        """Prüft Ollama-Verfügbarkeit"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_host}/api/tags", timeout=5) as response:
                    return response.status == 200
        except Exception:
            return False

    async def _check_lmstudio(self) -> bool:
        """Prüft LM Studio-Verfügbarkeit"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.lmstudio_host}/v1/models", timeout=5) as response:
                    return response.status == 200
        except Exception:
            return False

    async def _check_gpt4all(self) -> bool:
        """Prüft GPT4All-Verfügbarkeit"""
        try:
            return os.path.exists(self.gpt4all_path) and len(os.listdir(self.gpt4all_path)) > 0
        except Exception:
            return False

    async def _load_available_models(self):
        """Lädt verfügbare lokale Modelle"""
        self.available_models = []

        # Ollama-Modelle
        if self.services["ollama"]:
            ollama_models = await self._get_ollama_models()
            self.available_models.extend(ollama_models)

        # LM Studio-Modelle
        if self.services["lmstudio"]:
            lmstudio_models = await self._get_lmstudio_models()
            self.available_models.extend(lmstudio_models)

        # GPT4All-Modelle
        if self.services["gpt4all"]:
            gpt4all_models = await self._get_gpt4all_models()
            self.available_models.extend(gpt4all_models)

    async def _get_ollama_models(self) -> List[Dict[str, Any]]:
        """Holt Ollama-Modelle"""
        models = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_host}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()

                        for model_info in data.get("models", []):
                            model_name = model_info["name"]
                            models.append(
                                {
                                    "name": model_name,
                                    "service": "ollama",
                                    "size": model_info.get("size", 0),
                                    "modified_at": model_info.get("modified_at", ""),
                                    "config": {**self.default_configs, "host": self.ollama_host},
                                }
                            )

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Ollama-Modelle: {e}")

        return models

    async def _get_lmstudio_models(self) -> List[Dict[str, Any]]:
        """Holt LM Studio-Modelle"""
        models = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.lmstudio_host}/v1/models") as response:
                    if response.status == 200:
                        data = await response.json()

                        for model_info in data.get("data", []):
                            model_name = model_info["id"]
                            models.append(
                                {
                                    "name": model_name,
                                    "service": "lmstudio",
                                    "config": {**self.default_configs, "host": self.lmstudio_host},
                                }
                            )

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der LM Studio-Modelle: {e}")

        return models

    async def _get_gpt4all_models(self) -> List[Dict[str, Any]]:
        """Holt GPT4All-Modelle"""
        models = []

        try:
            for file_name in os.listdir(self.gpt4all_path):
                if file_name.endswith(".bin") or file_name.endswith(".gguf"):
                    model_name = os.path.splitext(file_name)[0]
                    models.append(
                        {
                            "name": model_name,
                            "service": "gpt4all",
                            "file_path": os.path.join(self.gpt4all_path, file_name),
                            "config": {
                                **self.default_configs,
                                "model_path": os.path.join(self.gpt4all_path, file_name),
                            },
                        }
                    )

        except Exception as e:
            logger.error(f"Fehler beim Abrufen der GPT4All-Modelle: {e}")

        return models

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
        """Generiert eine Antwort mit einem lokalen Modell"""
        try:
            model_info = await self.get_model_info(model_name)
            if not model_info:
                raise ValueError(f"Modell {model_name} nicht gefunden")

            service = model_info["service"]

            if service == "ollama":
                return await self._generate_ollama_response(model_name, prompt, **kwargs)
            elif service == "lmstudio":
                return await self._generate_lmstudio_response(model_name, prompt, **kwargs)
            elif service == "gpt4all":
                return await self._generate_gpt4all_response(model_name, prompt, **kwargs)
            else:
                raise ValueError(f"Unbekannter Service: {service}")

        except Exception as e:
            logger.error(f"Fehler bei der Antwort-Generierung: {e}")
            raise

    async def _generate_ollama_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit Ollama"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                    "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                    "top_k": kwargs.get("top_k", config.get("top_k", 40)),
                    "repeat_penalty": kwargs.get(
                        "repeat_penalty", config.get("repeat_penalty", 1.1)
                    ),
                },
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['host']}/api/generate", json=payload, timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        raise Exception(f"Ollama-Fehler: {response.status}")

        except Exception as e:
            logger.error(f"Fehler bei Ollama-Antwort: {e}")
            raise

    async def _generate_lmstudio_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit LM Studio"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "stream": False,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['host']}/v1/chat/completions", json=payload, timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["choices"][0]["message"]["content"]
                    else:
                        raise Exception(f"LM Studio-Fehler: {response.status}")

        except Exception as e:
            logger.error(f"Fehler bei LM Studio-Antwort: {e}")
            raise

    async def _generate_gpt4all_response(self, model_name: str, prompt: str, **kwargs) -> str:
        """Generiert Antwort mit GPT4All"""
        try:
            # GPT4All-Integration würde hier implementiert werden
            # Für jetzt simulieren wir eine Antwort
            return f"GPT4All-Antwort für '{prompt[:50]}...' (Modell: {model_name})"

        except Exception as e:
            logger.error(f"Fehler bei GPT4All-Antwort: {e}")
            raise

    async def generate_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert eine Streaming-Antwort"""
        try:
            model_info = await self.get_model_info(model_name)
            if not model_info:
                raise ValueError(f"Modell {model_name} nicht gefunden")

            service = model_info["service"]

            if service == "ollama":
                async for chunk in self._generate_ollama_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            elif service == "lmstudio":
                async for chunk in self._generate_lmstudio_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            elif service == "gpt4all":
                async for chunk in self._generate_gpt4all_streaming_response(
                    model_name, prompt, **kwargs
                ):
                    yield chunk
            else:
                raise ValueError(f"Unbekannter Service: {service}")

        except Exception as e:
            logger.error(f"Fehler bei der Streaming-Antwort: {e}")
            raise

    async def _generate_ollama_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit Ollama"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                    "top_p": kwargs.get("top_p", config.get("top_p", 0.9)),
                    "top_k": kwargs.get("top_k", config.get("top_k", 40)),
                    "repeat_penalty": kwargs.get(
                        "repeat_penalty", config.get("repeat_penalty", 1.1)
                    ),
                },
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['host']}/api/generate", json=payload, timeout=60
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                try:
                                    data = json.loads(line.decode("utf-8"))
                                    if "response" in data:
                                        yield data["response"]
                                except json.JSONDecodeError:
                                    continue
                    else:
                        raise Exception(f"Ollama-Streaming-Fehler: {response.status}")

        except Exception as e:
            logger.error(f"Fehler bei Ollama-Streaming: {e}")
            raise

    async def _generate_lmstudio_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit LM Studio"""
        try:
            config = await self.get_model_config(model_name)

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", config.get("temperature", 0.7)),
                "max_tokens": kwargs.get("max_tokens", config.get("max_tokens", 2048)),
                "stream": True,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['host']}/v1/chat/completions", json=payload, timeout=60
                ) as response:
                    if response.status == 200:
                        async for line in response.content:
                            if line:
                                try:
                                    line_str = line.decode("utf-8")
                                    if line_str.startswith("data: "):
                                        data_str = line_str[6:]
                                        if data_str.strip() == "[DONE]":
                                            break
                                        data = json.loads(data_str)
                                        if "choices" in data and len(data["choices"]) > 0:
                                            delta = data["choices"][0].get("delta", {})
                                            if "content" in delta:
                                                yield delta["content"]
                                except json.JSONDecodeError:
                                    continue
                    else:
                        raise Exception(f"LM Studio-Streaming-Fehler: {response.status}")

        except Exception as e:
            logger.error(f"Fehler bei LM Studio-Streaming: {e}")
            raise

    async def _generate_gpt4all_streaming_response(
        self, model_name: str, prompt: str, **kwargs
    ) -> AsyncGenerator[str, None]:
        """Generiert Streaming-Antwort mit GPT4All"""
        try:
            # GPT4All-Streaming würde hier implementiert werden
            # Für jetzt simulieren wir eine Streaming-Antwort
            response = f"GPT4All-Streaming-Antwort für '{prompt[:50]}...' (Modell: {model_name})"
            for word in response.split():
                yield word + " "
                await asyncio.sleep(0.1)  # Simuliere Verzögerung

        except Exception as e:
            logger.error(f"Fehler bei GPT4All-Streaming: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Führt einen Health-Check durch"""
        try:
            health_status = {
                "status": "healthy",
                "services": self.services,
                "available_models": len(self.available_models),
                "errors": [],
            }

            # Prüfe Services erneut
            await self._check_services()

            if not any(self.services.values()):
                health_status["status"] = "unhealthy"
                health_status["errors"].append("Keine lokalen Services verfügbar")

            return health_status

        except Exception as e:
            logger.error(f"Fehler beim Health-Check: {e}")
            return {"status": "error", "error": str(e)}

    async def cleanup(self):
        """Bereinigt Ressourcen"""
        try:
            # Schließe offene Verbindungen
            logger.info("Lokaler Model Manager bereinigt")

        except Exception as e:
            logger.error(f"Fehler bei der Bereinigung: {e}")
