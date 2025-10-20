"""
Hooks Module - Event-Handler für das System
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseHook(ABC):
    """Basisklasse für alle Hooks"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.events = []
        self.status = "initialized"
        self.logger = logging.getLogger(f"hook.{name}")
        self.callbacks = []

    @abstractmethod
    async def execute(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Führt den Hook aus"""
        pass

    def register_callback(self, callback: Callable):
        """Registriert einen Callback für den Hook"""
        self.callbacks.append(callback)
        self.logger.info(f"Registered callback for hook {self.name}")

    def get_info(self) -> Dict[str, Any]:
        """Gibt Informationen über den Hook zurück"""
        return {
            "name": self.name,
            "description": self.description,
            "events": self.events,
            "callbacks_count": len(self.callbacks),
            "status": self.status,
        }

    async def initialize(self):
        """Initialisiert den Hook"""
        self.status = "ready"
        self.logger.info(f"Hook {self.name} initialized")


class StartupHook(BaseHook):
    """Hook für System-Startup-Events"""

    def __init__(self):
        super().__init__(name="startup_hook", description="Behandelt System-Startup-Events")
        self.events = ["system_startup", "module_loaded", "agent_initialized"]

    async def execute(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Behandelt Startup-Events"""
        self.logger.info(f"Processing startup event: {event}")

        if event == "system_startup":
            result = {
                "event": event,
                "timestamp": datetime.now().isoformat(),
                "message": "System startup completed",
                "actions": ["load_modules", "initialize_agents", "start_services"],
            }

        elif event == "module_loaded":
            module_name = data.get("module_name", "unknown") if data else "unknown"
            result = {
                "event": event,
                "module_name": module_name,
                "timestamp": datetime.now().isoformat(),
                "message": f"Module {module_name} loaded successfully",
            }

        elif event == "agent_initialized":
            agent_name = data.get("agent_name", "unknown") if data else "unknown"
            result = {
                "event": event,
                "agent_name": agent_name,
                "timestamp": datetime.now().isoformat(),
                "message": f"Agent {agent_name} initialized successfully",
            }

        else:
            result = {
                "event": event,
                "timestamp": datetime.now().isoformat(),
                "message": f"Unknown startup event: {event}",
            }

        # Führe alle registrierten Callbacks aus
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event, data, result)
                else:
                    callback(event, data, result)
            except Exception as e:
                self.logger.error(f"Error in callback: {e}")

        return {"hook": self.name, "result": result, "status": "completed"}


class ErrorHook(BaseHook):
    """Hook für Error-Handling"""

    def __init__(self):
        super().__init__(name="error_hook", description="Behandelt System-Fehler und Exceptions")
        self.events = ["error_occurred", "exception_caught", "validation_failed"]
        self.error_count = 0

    async def execute(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Behandelt Error-Events"""
        self.error_count += 1
        self.logger.error(f"Processing error event: {event}")

        error_info = data.get("error_info", {}) if data else {}
        error_message = error_info.get("message", "Unknown error")
        error_type = error_info.get("type", "UnknownError")

        if event == "error_occurred":
            result = {
                "event": event,
                "error_type": error_type,
                "error_message": error_message,
                "timestamp": datetime.now().isoformat(),
                "error_count": self.error_count,
                "actions": ["log_error", "notify_admin", "attempt_recovery"],
            }

        elif event == "exception_caught":
            exception = error_info.get("exception", "UnknownException")
            result = {
                "event": event,
                "exception_type": str(type(exception).__name__),
                "exception_message": str(exception),
                "timestamp": datetime.now().isoformat(),
                "error_count": self.error_count,
                "actions": ["log_exception", "create_error_report"],
            }

        elif event == "validation_failed":
            validation_errors = error_info.get("validation_errors", [])
            result = {
                "event": event,
                "validation_errors": validation_errors,
                "timestamp": datetime.now().isoformat(),
                "error_count": self.error_count,
                "actions": ["log_validation_errors", "return_error_response"],
            }

        else:
            result = {
                "event": event,
                "timestamp": datetime.now().isoformat(),
                "error_count": self.error_count,
                "message": f"Unknown error event: {event}",
            }

        # Führe alle registrierten Callbacks aus
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event, data, result)
                else:
                    callback(event, data, result)
            except Exception as e:
                self.logger.error(f"Error in error hook callback: {e}")

        return {"hook": self.name, "result": result, "status": "completed"}


class PerformanceHook(BaseHook):
    """Hook für Performance-Monitoring"""

    def __init__(self):
        super().__init__(name="performance_hook", description="Überwacht System-Performance")
        self.events = ["performance_metric", "slow_operation", "resource_usage"]
        self.metrics = {"total_operations": 0, "slow_operations": 0, "average_response_time": 0.0}

    async def execute(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Behandelt Performance-Events"""
        self.logger.info(f"Processing performance event: {event}")

        if event == "performance_metric":
            metric_data = data.get("metric_data", {}) if data else {}
            operation_name = metric_data.get("operation", "unknown")
            response_time = metric_data.get("response_time", 0.0)

            self.metrics["total_operations"] += 1
            self.metrics["average_response_time"] = (
                self.metrics["average_response_time"] * (self.metrics["total_operations"] - 1)
                + response_time
            ) / self.metrics["total_operations"]

            result = {
                "event": event,
                "operation": operation_name,
                "response_time": response_time,
                "timestamp": datetime.now().isoformat(),
                "metrics": self.metrics.copy(),
            }

        elif event == "slow_operation":
            operation_data = data.get("operation_data", {}) if data else {}
            operation_name = operation_data.get("operation", "unknown")
            response_time = operation_data.get("response_time", 0.0)
            threshold = operation_data.get("threshold", 1.0)

            self.metrics["slow_operations"] += 1

            result = {
                "event": event,
                "operation": operation_name,
                "response_time": response_time,
                "threshold": threshold,
                "timestamp": datetime.now().isoformat(),
                "warning": f"Operation {operation_name} took {response_time:.2f}s (threshold: {threshold}s)",
            }

        elif event == "resource_usage":
            resource_data = data.get("resource_data", {}) if data else {}
            cpu_usage = resource_data.get("cpu_usage", 0.0)
            memory_usage = resource_data.get("memory_usage", 0.0)
            disk_usage = resource_data.get("disk_usage", 0.0)

            result = {
                "event": event,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
                "timestamp": datetime.now().isoformat(),
                "status": "normal" if cpu_usage < 80 and memory_usage < 80 else "warning",
            }

        else:
            result = {
                "event": event,
                "timestamp": datetime.now().isoformat(),
                "message": f"Unknown performance event: {event}",
            }

        # Führe alle registrierten Callbacks aus
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event, data, result)
                else:
                    callback(event, data, result)
            except Exception as e:
                self.logger.error(f"Error in performance hook callback: {e}")

        return {"hook": self.name, "result": result, "status": "completed"}


class SecurityHook(BaseHook):
    """Hook für Security-Events"""

    def __init__(self):
        super().__init__(
            name="security_hook", description="Behandelt Security-Events und -Warnungen"
        )
        self.events = ["authentication_failed", "unauthorized_access", "suspicious_activity"]
        self.security_events = []

    async def execute(self, event: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Behandelt Security-Events"""
        self.logger.warning(f"Processing security event: {event}")

        security_data = data.get("security_data", {}) if data else {}
        ip_address = security_data.get("ip_address", "unknown")
        user_agent = security_data.get("user_agent", "unknown")
        user_id = security_data.get("user_id", "anonymous")

        security_event = {
            "event": event,
            "timestamp": datetime.now().isoformat(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "user_id": user_id,
            "severity": (
                "high" if event in ["unauthorized_access", "suspicious_activity"] else "medium"
            ),
        }

        self.security_events.append(security_event)

        if event == "authentication_failed":
            result = {
                **security_event,
                "message": f"Authentication failed for user {user_id}",
                "actions": ["log_failed_attempt", "check_rate_limit", "notify_security"],
            }

        elif event == "unauthorized_access":
            result = {
                **security_event,
                "message": f"Unauthorized access attempt from {ip_address}",
                "actions": ["block_ip", "log_incident", "notify_admin", "create_security_report"],
            }

        elif event == "suspicious_activity":
            activity_type = security_data.get("activity_type", "unknown")
            result = {
                **security_event,
                "activity_type": activity_type,
                "message": f"Suspicious activity detected: {activity_type}",
                "actions": ["monitor_activity", "log_incident", "notify_security"],
            }

        else:
            result = {**security_event, "message": f"Unknown security event: {event}"}

        # Führe alle registrierten Callbacks aus
        for callback in self.callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event, data, result)
                else:
                    callback(event, data, result)
            except Exception as e:
                self.logger.error(f"Error in security hook callback: {e}")

        return {"hook": self.name, "result": result, "status": "completed"}


# Initialisierungsfunktion
async def initialize():
    """Initialisiert alle Hooks"""
    print("Initializing hooks...")

    hooks = {
        "startup_hook": StartupHook(),
        "error_hook": ErrorHook(),
        "performance_hook": PerformanceHook(),
        "security_hook": SecurityHook(),
    }

    for hook in hooks.values():
        await hook.initialize()

    print("Hooks initialized successfully!")
    return hooks
