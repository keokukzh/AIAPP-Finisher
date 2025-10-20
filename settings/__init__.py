"""
Settings Module - Konfigurationssystem für das AI-Agent-System
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SettingsManager:
    """Zentraler Manager für alle Systemeinstellungen"""

    def __init__(self, config_dir: str = "settings"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

        self.settings = {}
        self.default_settings = {}
        self.environment_settings = {}

        self.logger = logging.getLogger("settings_manager")

        # Lade Standard-Einstellungen
        self._load_default_settings()

        # Lade Umgebungsvariablen
        self._load_environment_settings()

        # Lade Konfigurationsdateien
        self._load_config_files()

    def _load_default_settings(self):
        """Lädt Standard-Einstellungen"""
        self.default_settings = {
            "app": {
                "name": "AI Agent System",
                "version": "1.0.0",
                "debug": False,
                "log_level": "INFO",
                "host": "0.0.0.0",
                "port": 8000,
            },
            "database": {
                "url": "sqlite:///./agents.db",
                "pool_size": 10,
                "max_overflow": 20,
                "echo": False,
            },
            "api": {
                "rate_limit": {"enabled": True, "requests_per_minute": 100, "burst_limit": 10},
                "cors": {
                    "enabled": True,
                    "origins": ["*"],
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "headers": ["*"],
                },
            },
            "agents": {
                "max_concurrent": 10,
                "timeout": 30,
                "retry_attempts": 3,
                "auto_restart": True,
            },
            "skills": {"cache_enabled": True, "cache_ttl": 3600, "max_skill_execution_time": 60},
            "security": {
                "session_timeout": 3600,
                "max_login_attempts": 5,
                "password_min_length": 8,
                "require_2fa": False,
                "encryption_key": "default_key_change_in_production",
            },
            "monitoring": {
                "enabled": True,
                "metrics_interval": 60,
                "log_retention_days": 30,
                "alert_thresholds": {"cpu_usage": 80, "memory_usage": 85, "disk_usage": 90},
            },
            "ai_providers": {
                "openai": {
                    "enabled": False,
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000,
                    "temperature": 0.7,
                },
                "google": {
                    "enabled": False,
                    "model": "gemini-pro",
                    "max_tokens": 1000,
                    "temperature": 0.7,
                },
                "claude": {
                    "enabled": False,
                    "model": "claude-3-sonnet",
                    "max_tokens": 1000,
                    "temperature": 0.7,
                },
            },
        }

        self.settings = self.default_settings.copy()
        self.logger.info("Default settings loaded")

    def _load_environment_settings(self):
        """Lädt Einstellungen aus Umgebungsvariablen"""
        env_mappings = {
            "APP_NAME": ("app", "name"),
            "APP_VERSION": ("app", "version"),
            "DEBUG": ("app", "debug"),
            "LOG_LEVEL": ("app", "log_level"),
            "HOST": ("app", "host"),
            "PORT": ("app", "port"),
            "DATABASE_URL": ("database", "url"),
            "OPENAI_API_KEY": ("ai_providers", "openai", "api_key"),
            "GOOGLE_API_KEY": ("ai_providers", "google", "api_key"),
            "CLAUDE_API_KEY": ("ai_providers", "claude", "api_key"),
        }

        for env_var, setting_path in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._set_nested_value(self.environment_settings, setting_path, value)

        # Merge environment settings
        self._merge_settings(self.settings, self.environment_settings)
        self.logger.info("Environment settings loaded")

    def _load_config_files(self):
        """Lädt Konfigurationsdateien"""
        config_files = ["config.json", "settings.json", "app_config.json"]

        for config_file in config_files:
            config_path = self.config_dir / config_file
            if config_path.exists():
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        file_settings = json.load(f)
                    self._merge_settings(self.settings, file_settings)
                    self.logger.info(f"Loaded config file: {config_file}")
                except Exception as e:
                    self.logger.error(f"Error loading config file {config_file}: {e}")

    def _set_nested_value(self, dictionary: Dict, path: tuple, value: Any):
        """Setzt einen verschachtelten Wert in einem Dictionary"""
        current = dictionary
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value

    def _merge_settings(self, target: Dict, source: Dict):
        """Merge zwei Settings-Dictionaries"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_settings(target[key], value)
            else:
                target[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        """Holt einen Einstellungswert über einen Punkt-Notations-Pfad"""
        keys = key_path.split(".")
        current = self.settings

        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def set(self, key_path: str, value: Any):
        """Setzt einen Einstellungswert über einen Punkt-Notations-Pfad"""
        keys = key_path.split(".")
        current = self.settings

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        self.logger.info(f"Setting updated: {key_path} = {value}")

    def get_section(self, section: str) -> Dict[str, Any]:
        """Holt einen ganzen Einstellungsbereich"""
        return self.settings.get(section, {})

    def update_section(self, section: str, updates: Dict[str, Any]):
        """Aktualisiert einen ganzen Einstellungsbereich"""
        if section not in self.settings:
            self.settings[section] = {}

        self.settings[section].update(updates)
        self.logger.info(f"Section updated: {section}")

    async def save_config(self, filename: str = "settings.json"):
        """Speichert die aktuellen Einstellungen in eine Datei"""
        config_path = self.config_dir / filename

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Settings saved to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return False

    async def reload_config(self):
        """Lädt die Konfiguration neu"""
        self.settings = self.default_settings.copy()
        self._load_environment_settings()
        self._load_config_files()
        self.logger.info("Configuration reloaded")

    def get_all_settings(self) -> Dict[str, Any]:
        """Gibt alle Einstellungen zurück"""
        return self.settings.copy()

    def validate_settings(self) -> List[str]:
        """Validiert die aktuellen Einstellungen"""
        errors = []

        # Validiere App-Einstellungen
        app_settings = self.get_section("app")
        if not app_settings.get("name"):
            errors.append("App name is required")

        port = app_settings.get("port")
        if not isinstance(port, int) or port < 1 or port > 65535:
            errors.append("Port must be a valid integer between 1 and 65535")

        # Validiere AI-Provider-Einstellungen
        ai_providers = self.get_section("ai_providers")
        for provider, config in ai_providers.items():
            if config.get("enabled") and not config.get("api_key"):
                errors.append(f"API key required for enabled provider: {provider}")

        # Validiere Security-Einstellungen
        security = self.get_section("security")
        if security.get("encryption_key") == "default_key_change_in_production":
            errors.append("Default encryption key must be changed in production")

        return errors

    def get_api_keys(self) -> Dict[str, str]:
        """Gibt alle konfigurierten API-Schlüssel zurück"""
        api_keys = {}
        ai_providers = self.get_section("ai_providers")

        for provider, config in ai_providers.items():
            if config.get("enabled") and config.get("api_key"):
                api_keys[provider] = config["api_key"]

        return api_keys

    def is_provider_enabled(self, provider: str) -> bool:
        """Prüft ob ein AI-Provider aktiviert ist"""
        provider_config = self.get(f"ai_providers.{provider}")
        return provider_config.get("enabled", False) if provider_config else False

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Gibt die Konfiguration für einen AI-Provider zurück"""
        return self.get(f"ai_providers.{provider}", {})


class ConfigValidator:
    """Validiert Konfigurationseinstellungen"""

    @staticmethod
    def validate_app_config(config: Dict[str, Any]) -> List[str]:
        """Validiert App-Konfiguration"""
        errors = []

        required_fields = ["name", "version", "host", "port"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Required field missing: {field}")

        if "port" in config:
            port = config["port"]
            if not isinstance(port, int) or port < 1 or port > 65535:
                errors.append("Port must be a valid integer between 1 and 65535")

        if "debug" in config and not isinstance(config["debug"], bool):
            errors.append("Debug must be a boolean value")

        return errors

    @staticmethod
    def validate_database_config(config: Dict[str, Any]) -> List[str]:
        """Validiert Datenbank-Konfiguration"""
        errors = []

        if "url" not in config:
            errors.append("Database URL is required")

        if "pool_size" in config:
            pool_size = config["pool_size"]
            if not isinstance(pool_size, int) or pool_size < 1:
                errors.append("Pool size must be a positive integer")

        return errors

    @staticmethod
    def validate_security_config(config: Dict[str, Any]) -> List[str]:
        """Validiert Security-Konfiguration"""
        errors = []

        if "session_timeout" in config:
            timeout = config["session_timeout"]
            if not isinstance(timeout, int) or timeout < 60:
                errors.append("Session timeout must be at least 60 seconds")

        if "password_min_length" in config:
            min_length = config["password_min_length"]
            if not isinstance(min_length, int) or min_length < 6:
                errors.append("Password minimum length must be at least 6 characters")

        return errors


class EnvironmentConfig:
    """Behandelt Umgebungs-spezifische Konfigurationen"""

    def __init__(self, environment: str = None):
        self.environment = environment or os.getenv("ENVIRONMENT", "development")
        self.logger = logging.getLogger("environment_config")

    def get_environment_specific_config(self) -> Dict[str, Any]:
        """Gibt umgebungs-spezifische Konfigurationen zurück"""
        configs = {
            "development": {
                "app": {"debug": True, "log_level": "DEBUG"},
                "database": {"echo": True},
                "monitoring": {"enabled": False},
            },
            "testing": {
                "app": {"debug": True, "log_level": "INFO"},
                "database": {"url": "sqlite:///./test_agents.db", "echo": False},
                "monitoring": {"enabled": False},
            },
            "production": {
                "app": {"debug": False, "log_level": "WARNING"},
                "database": {"echo": False},
                "monitoring": {"enabled": True},
                "security": {"require_2fa": True},
            },
        }

        return configs.get(self.environment, configs["development"])

    def apply_environment_config(self, settings_manager: SettingsManager):
        """Wendet umgebungs-spezifische Konfigurationen an"""
        env_config = self.get_environment_specific_config()

        for section, config in env_config.items():
            settings_manager.update_section(section, config)

        self.logger.info(f"Applied {self.environment} environment configuration")


# Globale Settings-Instanz
settings_manager = SettingsManager()

# Alias für Kompatibilität
Settings = SettingsManager


# Initialisierungsfunktion
async def initialize():
    """Initialisiert das Settings-System"""
    print("Initializing settings system...")

    # Wende Umgebungs-Konfiguration an
    env_config = EnvironmentConfig()
    env_config.apply_environment_config(settings_manager)

    # Validiere Einstellungen
    errors = settings_manager.validate_settings()
    if errors:
        print(f"Configuration validation errors: {errors}")
    else:
        print("Configuration validation passed")

    # Speichere Standard-Konfiguration falls sie nicht existiert
    config_path = settings_manager.config_dir / "settings.json"
    if not config_path.exists():
        await settings_manager.save_config()
        print("Default configuration saved")

    print("Settings system initialized successfully!")
    return settings_manager
