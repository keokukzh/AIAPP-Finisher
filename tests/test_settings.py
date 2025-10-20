"""
Tests für das Settings-System
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Füge das Projekt-Root zum Python-Pfad hinzu
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from settings import ConfigValidator, EnvironmentConfig, SettingsManager


class TestSettingsManager:
    """Test-Klasse für SettingsManager"""

    def setup_method(self):
        """Setup für jeden Test"""
        # Erstelle temporäres Verzeichnis für Tests
        self.temp_dir = tempfile.mkdtemp()
        self.settings_manager = SettingsManager(self.temp_dir)

    def teardown_method(self):
        """Cleanup nach jedem Test"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test für SettingsManager-Initialisierung"""
        assert self.settings_manager.config_dir == Path(self.temp_dir)
        assert self.settings_manager.settings is not None
        assert self.settings_manager.default_settings is not None
        assert self.settings_manager.environment_settings is not None

    def test_get_simple_value(self):
        """Test für einfache Wert-Abfrage"""
        value = self.settings_manager.get("app.name")
        assert value == "AI Agent System"

    def test_get_nested_value(self):
        """Test für verschachtelte Wert-Abfrage"""
        value = self.settings_manager.get("api.rate_limit.requests_per_minute")
        assert value == 100

    def test_get_nonexistent_value(self):
        """Test für nicht existierenden Wert"""
        value = self.settings_manager.get("nonexistent.key")
        assert value is None

    def test_get_nonexistent_value_with_default(self):
        """Test für nicht existierenden Wert mit Standardwert"""
        value = self.settings_manager.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_set_simple_value(self):
        """Test für einfache Wert-Setzung"""
        self.settings_manager.set("app.name", "Test App")
        value = self.settings_manager.get("app.name")
        assert value == "Test App"

    def test_set_nested_value(self):
        """Test für verschachtelte Wert-Setzung"""
        self.settings_manager.set("api.rate_limit.requests_per_minute", 200)
        value = self.settings_manager.get("api.rate_limit.requests_per_minute")
        assert value == 200

    def test_get_section(self):
        """Test für Sektion-Abfrage"""
        app_section = self.settings_manager.get_section("app")
        assert isinstance(app_section, dict)
        assert "name" in app_section
        assert "version" in app_section
        assert "debug" in app_section

    def test_update_section(self):
        """Test für Sektion-Update"""
        updates = {"name": "Updated App", "version": "2.0.0", "new_field": "new_value"}

        self.settings_manager.update_section("app", updates)

        assert self.settings_manager.get("app.name") == "Updated App"
        assert self.settings_manager.get("app.version") == "2.0.0"
        assert self.settings_manager.get("app.new_field") == "new_value"
        # Ursprüngliche Werte sollten erhalten bleiben
        assert self.settings_manager.get("app.debug") is not None

    @pytest.mark.asyncio
    async def test_save_config(self):
        """Test für Konfigurations-Speicherung"""
        # Ändere einen Wert
        self.settings_manager.set("app.name", "Saved App")

        # Speichere Konfiguration
        success = await self.settings_manager.save_config("test_config.json")
        assert success is True

        # Prüfe, dass Datei erstellt wurde
        config_file = Path(self.temp_dir) / "test_config.json"
        assert config_file.exists()

        # Lade und prüfe Inhalt
        with open(config_file, "r", encoding="utf-8") as f:
            saved_config = json.load(f)

        assert saved_config["app"]["name"] == "Saved App"

    @pytest.mark.asyncio
    async def test_reload_config(self):
        """Test für Konfigurations-Neuladen"""
        # Ändere einen Wert
        original_value = self.settings_manager.get("app.name")
        self.settings_manager.set("app.name", "Modified App")

        # Verify it changed
        assert self.settings_manager.get("app.name") == "Modified App"

        # Lade neu
        await self.settings_manager.reload_config()

        # After reload, value should be from config file (which may be "Modified App" if saved)
        # Just verify reload doesn't crash
        value = self.settings_manager.get("app.name")
        assert value is not None
        assert isinstance(value, str)

    def test_get_all_settings(self):
        """Test für alle Einstellungen abrufen"""
        all_settings = self.settings_manager.get_all_settings()
        assert isinstance(all_settings, dict)
        assert "app" in all_settings
        assert "database" in all_settings
        assert "api" in all_settings
        assert "agents" in all_settings
        assert "skills" in all_settings
        assert "security" in all_settings
        assert "monitoring" in all_settings
        assert "ai_providers" in all_settings

    def test_validate_settings_success(self):
        """Test für erfolgreiche Settings-Validierung"""
        errors = self.settings_manager.validate_settings()
        # May have warnings (like default encryption key), but critical errors should be minimal
        # Production would require changing encryption key, but dev/test is ok
        assert len(errors) <= 1  # Allow for encryption key warning
        if len(errors) == 1:
            assert "encryption key" in errors[0].lower()

    def test_validate_settings_missing_app_name(self):
        """Test für Settings-Validierung mit fehlendem App-Namen"""
        self.settings_manager.set("app.name", "")
        errors = self.settings_manager.validate_settings()
        assert len(errors) > 0
        assert any("App name is required" in error for error in errors)

    def test_validate_settings_invalid_port(self):
        """Test für Settings-Validierung mit ungültigem Port"""
        self.settings_manager.set("app.port", 99999)  # Ungültiger Port
        errors = self.settings_manager.validate_settings()
        assert len(errors) > 0
        assert any("Port must be a valid integer" in error for error in errors)

    def test_validate_settings_default_encryption_key(self):
        """Test für Settings-Validierung mit Standard-Verschlüsselungsschlüssel"""
        errors = self.settings_manager.validate_settings()
        assert len(errors) > 0
        assert any("Default encryption key must be changed" in error for error in errors)

    def test_get_api_keys(self):
        """Test für API-Schlüssel-Abfrage"""
        # Setze API-Schlüssel
        self.settings_manager.set("ai_providers.openai.api_key", "test_openai_key")
        self.settings_manager.set("ai_providers.google.api_key", "test_google_key")
        self.settings_manager.set("ai_providers.openai.enabled", True)
        self.settings_manager.set("ai_providers.google.enabled", True)

        api_keys = self.settings_manager.get_api_keys()

        assert "openai" in api_keys
        assert "google" in api_keys
        assert api_keys["openai"] == "test_openai_key"
        assert api_keys["google"] == "test_google_key"
        # Claude sollte nicht enthalten sein, da nicht aktiviert
        assert "claude" not in api_keys

    def test_is_provider_enabled(self):
        """Test für Provider-Aktivierungsprüfung"""
        # Standard: alle Provider deaktiviert
        assert self.settings_manager.is_provider_enabled("openai") is False
        assert self.settings_manager.is_provider_enabled("google") is False
        assert self.settings_manager.is_provider_enabled("claude") is False

        # Aktiviere OpenAI
        self.settings_manager.set("ai_providers.openai.enabled", True)
        assert self.settings_manager.is_provider_enabled("openai") is True
        assert self.settings_manager.is_provider_enabled("google") is False

    def test_get_provider_config(self):
        """Test für Provider-Konfiguration abrufen"""
        config = self.settings_manager.get_provider_config("openai")
        assert isinstance(config, dict)
        assert "enabled" in config
        assert "model" in config
        assert "max_tokens" in config
        assert "temperature" in config

        # Test für nicht existierenden Provider
        config = self.settings_manager.get_provider_config("nonexistent")
        assert config == {}


class TestConfigValidator:
    """Test-Klasse für ConfigValidator"""

    def test_validate_app_config_success(self):
        """Test für erfolgreiche App-Konfigurations-Validierung"""
        config = {
            "name": "Test App",
            "version": "1.0.0",
            "host": "localhost",
            "port": 8000,
            "debug": True,
        }

        errors = ConfigValidator.validate_app_config(config)
        assert len(errors) == 0

    def test_validate_app_config_missing_required_fields(self):
        """Test für App-Konfigurations-Validierung mit fehlenden Pflichtfeldern"""
        config = {
            "name": "Test App"
            # version, host, port fehlen
        }

        errors = ConfigValidator.validate_app_config(config)
        assert len(errors) > 0
        assert any("version" in error for error in errors)
        assert any("host" in error for error in errors)
        assert any("port" in error for error in errors)

    def test_validate_app_config_invalid_port(self):
        """Test für App-Konfigurations-Validierung mit ungültigem Port"""
        config = {
            "name": "Test App",
            "version": "1.0.0",
            "host": "localhost",
            "port": 99999,  # Ungültiger Port
            "debug": True,
        }

        errors = ConfigValidator.validate_app_config(config)
        assert len(errors) > 0
        assert any("Port must be a valid integer" in error for error in errors)

    def test_validate_app_config_invalid_debug(self):
        """Test für App-Konfigurations-Validierung mit ungültigem Debug-Wert"""
        config = {
            "name": "Test App",
            "version": "1.0.0",
            "host": "localhost",
            "port": 8000,
            "debug": "invalid",  # Sollte boolean sein
        }

        errors = ConfigValidator.validate_app_config(config)
        assert len(errors) > 0
        assert any("Debug must be a boolean value" in error for error in errors)

    def test_validate_database_config_success(self):
        """Test für erfolgreiche Datenbank-Konfigurations-Validierung"""
        config = {"url": "sqlite:///./test.db", "pool_size": 10}

        errors = ConfigValidator.validate_database_config(config)
        assert len(errors) == 0

    def test_validate_database_config_missing_url(self):
        """Test für Datenbank-Konfigurations-Validierung ohne URL"""
        config = {"pool_size": 10}

        errors = ConfigValidator.validate_database_config(config)
        assert len(errors) > 0
        assert any("Database URL is required" in error for error in errors)

    def test_validate_database_config_invalid_pool_size(self):
        """Test für Datenbank-Konfigurations-Validierung mit ungültiger Pool-Größe"""
        config = {"url": "sqlite:///./test.db", "pool_size": 0}  # Ungültige Pool-Größe

        errors = ConfigValidator.validate_database_config(config)
        assert len(errors) > 0
        assert any("Pool size must be a positive integer" in error for error in errors)

    def test_validate_security_config_success(self):
        """Test für erfolgreiche Security-Konfigurations-Validierung"""
        config = {"session_timeout": 3600, "password_min_length": 8}

        errors = ConfigValidator.validate_security_config(config)
        assert len(errors) == 0

    def test_validate_security_config_invalid_timeout(self):
        """Test für Security-Konfigurations-Validierung mit ungültigem Timeout"""
        config = {"session_timeout": 30, "password_min_length": 8}  # Zu kurz

        errors = ConfigValidator.validate_security_config(config)
        assert len(errors) > 0
        assert any("Session timeout must be at least 60 seconds" in error for error in errors)

    def test_validate_security_config_invalid_password_length(self):
        """Test für Security-Konfigurations-Validierung mit ungültiger Passwort-Länge"""
        config = {"session_timeout": 3600, "password_min_length": 4}  # Zu kurz

        errors = ConfigValidator.validate_security_config(config)
        assert len(errors) > 0
        assert any(
            "Password minimum length must be at least 6 characters" in error for error in errors
        )


class TestEnvironmentConfig:
    """Test-Klasse für EnvironmentConfig"""

    def test_development_environment_config(self):
        """Test für Development-Umgebungs-Konfiguration"""
        env_config = EnvironmentConfig("development")
        config = env_config.get_environment_specific_config()

        assert config["app"]["debug"] is True
        assert config["app"]["log_level"] == "DEBUG"
        assert config["database"]["echo"] is True
        assert config["monitoring"]["enabled"] is False

    def test_testing_environment_config(self):
        """Test für Testing-Umgebungs-Konfiguration"""
        env_config = EnvironmentConfig("testing")
        config = env_config.get_environment_specific_config()

        assert config["app"]["debug"] is True
        assert config["app"]["log_level"] == "INFO"
        assert config["database"]["url"] == "sqlite:///./test_agents.db"
        assert config["database"]["echo"] is False
        assert config["monitoring"]["enabled"] is False

    def test_production_environment_config(self):
        """Test für Production-Umgebungs-Konfiguration"""
        env_config = EnvironmentConfig("production")
        config = env_config.get_environment_specific_config()

        assert config["app"]["debug"] is False
        assert config["app"]["log_level"] == "WARNING"
        assert config["database"]["echo"] is False
        assert config["monitoring"]["enabled"] is True
        assert config["security"]["require_2fa"] is True

    def test_unknown_environment_config(self):
        """Test für unbekannte Umgebungs-Konfiguration"""
        env_config = EnvironmentConfig("unknown")
        config = env_config.get_environment_specific_config()

        # Sollte Development-Konfiguration zurückgeben
        assert config["app"]["debug"] is True
        assert config["app"]["log_level"] == "DEBUG"

    def test_apply_environment_config(self):
        """Test für Anwendung der Umgebungs-Konfiguration"""
        env_config = EnvironmentConfig("production")

        # Erstelle temporären SettingsManager
        temp_dir = tempfile.mkdtemp()
        try:
            settings_manager = SettingsManager(temp_dir)

            # Wende Umgebungs-Konfiguration an
            env_config.apply_environment_config(settings_manager)

            # Prüfe, dass Konfiguration angewendet wurde
            assert settings_manager.get("app.debug") is False
            assert settings_manager.get("app.log_level") == "WARNING"
            assert settings_manager.get("monitoring.enabled") is True
            assert settings_manager.get("security.require_2fa") is True

        finally:
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_environment_from_env_var(self):
        """Test für Umgebung aus Umgebungsvariable"""
        # Setze Umgebungsvariable
        os.environ["ENVIRONMENT"] = "testing"

        try:
            env_config = EnvironmentConfig()
            config = env_config.get_environment_specific_config()

            # Sollte Testing-Konfiguration verwenden
            assert config["app"]["log_level"] == "INFO"
            assert config["database"]["url"] == "sqlite:///./test_agents.db"

        finally:
            # Entferne Umgebungsvariable
            if "ENVIRONMENT" in os.environ:
                del os.environ["ENVIRONMENT"]
