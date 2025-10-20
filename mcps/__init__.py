"""
MCPs Module - Modulare Kontrollpunkte für das System
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class MCPStatus(Enum):
    """Status-Enum für MCPs"""

    INACTIVE = "inactive"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class BaseMCP(ABC):
    """Basisklasse für alle Modularen Kontrollpunkte (MCPs)"""

    def __init__(self, name: str, description: str = "", priority: int = 1):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = MCPStatus.INACTIVE
        self.logger = logging.getLogger(f"mcp.{name}")
        self.handlers = {}
        self.metrics = {
            "requests_processed": 0,
            "errors": 0,
            "last_activity": None,
            "average_response_time": 0.0,
        }
        self.config = {}

    @abstractmethod
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet eine Anfrage"""
        pass

    def register_handler(self, event_type: str, handler: Callable):
        """Registriert einen Event-Handler"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        self.logger.info(f"Registered handler for event type: {event_type}")

    async def trigger_event(self, event_type: str, data: Optional[Dict[str, Any]] = None):
        """Triggert ein Event und ruft alle registrierten Handler auf"""
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(data)
                    else:
                        handler(data)
                except Exception as e:
                    self.logger.error(f"Error in event handler: {e}")

    def get_info(self) -> Dict[str, Any]:
        """Gibt Informationen über den MCP zurück"""
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "status": self.status.value,
            "metrics": self.metrics.copy(),
            "handlers_count": sum(len(handlers) for handlers in self.handlers.values()),
            "config": self.config,
        }

    async def initialize(self):
        """Initialisiert den MCP"""
        self.status = MCPStatus.ACTIVE
        self.logger.info(f"MCP {self.name} initialized")

    async def shutdown(self):
        """Fährt den MCP herunter"""
        self.status = MCPStatus.INACTIVE
        self.logger.info(f"MCP {self.name} shutdown")


class AuthenticationMCP(BaseMCP):
    """MCP für Authentifizierung und Autorisierung"""

    def __init__(self):
        super().__init__(
            name="authentication_mcp",
            description="Behandelt Authentifizierung und Autorisierung",
            priority=10,  # Hohe Priorität
        )
        self.config = {
            "session_timeout": 3600,  # 1 hour
            "max_login_attempts": 5,
            "password_min_length": 8,
            "require_2fa": False,
        }
        self.active_sessions = {}
        self.login_attempts = {}

    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Authentifizierungsanfragen"""
        action = request.get("action")
        self.metrics["requests_processed"] += 1
        start_time = asyncio.get_event_loop().time()

        try:
            if action == "login":
                result = await self._handle_login(request)
            elif action == "logout":
                result = await self._handle_logout(request)
            elif action == "validate_token":
                result = await self._handle_validate_token(request)
            elif action == "refresh_token":
                result = await self._handle_refresh_token(request)
            elif action == "check_permissions":
                result = await self._handle_check_permissions(request)
            else:
                result = {"error": f"Unknown action: {action}", "status": "error"}

            # Update metrics
            response_time = asyncio.get_event_loop().time() - start_time
            self.metrics["average_response_time"] = (
                self.metrics["average_response_time"] * (self.metrics["requests_processed"] - 1)
                + response_time
            ) / self.metrics["requests_processed"]
            self.metrics["last_activity"] = datetime.now().isoformat()

            return {"mcp": self.name, "action": action, "result": result, "status": "completed"}

        except Exception as e:
            self.metrics["errors"] += 1
            self.logger.error(f"Error processing authentication request: {e}")
            return {"mcp": self.name, "action": action, "error": str(e), "status": "error"}

    async def _handle_login(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Behandelt Login-Anfragen"""
        username = request.get("username")
        password = request.get("password")

        if not username or not password:
            return {"error": "Username and password are required", "success": False}

        # Simuliere Authentifizierung
        await asyncio.sleep(0.1)

        # Einfache Validierung (in echter Implementierung würde hier echte Auth-Logik stehen)
        if username == "admin" and password == "admin123":
            session_token = f"token_{datetime.now().timestamp()}"
            self.active_sessions[session_token] = {
                "username": username,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now().timestamp() + self.config["session_timeout"]),
            }

            await self.trigger_event(
                "user_logged_in", {"username": username, "session_token": session_token}
            )

            return {
                "success": True,
                "session_token": session_token,
                "expires_in": self.config["session_timeout"],
                "user": {"username": username, "role": "admin"},
            }
        else:
            # Track failed login attempts
            if username not in self.login_attempts:
                self.login_attempts[username] = 0
            self.login_attempts[username] += 1

            await self.trigger_event(
                "login_failed", {"username": username, "attempts": self.login_attempts[username]}
            )

            return {
                "success": False,
                "error": "Invalid credentials",
                "attempts": self.login_attempts[username],
            }

    async def _handle_logout(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Behandelt Logout-Anfragen"""
        session_token = request.get("session_token")

        if not session_token:
            return {"error": "Session token is required", "success": False}

        if session_token in self.active_sessions:
            username = self.active_sessions[session_token]["username"]
            del self.active_sessions[session_token]

            await self.trigger_event(
                "user_logged_out", {"username": username, "session_token": session_token}
            )

            return {"success": True, "message": "Logged out successfully"}
        else:
            return {"success": False, "error": "Invalid session token"}

    async def _handle_validate_token(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Validiert einen Session-Token"""
        session_token = request.get("session_token")

        if not session_token:
            return {"valid": False, "error": "Session token is required"}

        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            if datetime.now().timestamp() < session["expires_at"]:
                return {
                    "valid": True,
                    "user": {"username": session["username"]},
                    "expires_at": session["expires_at"],
                }
            else:
                # Token expired
                del self.active_sessions[session_token]
                return {"valid": False, "error": "Session expired"}
        else:
            return {"valid": False, "error": "Invalid session token"}

    async def _handle_refresh_token(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Erneuert einen Session-Token"""
        session_token = request.get("session_token")

        if not session_token:
            return {"error": "Session token is required", "success": False}

        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            new_token = f"token_{datetime.now().timestamp()}"

            self.active_sessions[new_token] = {
                **session,
                "created_at": datetime.now().isoformat(),
                "expires_at": datetime.now().timestamp() + self.config["session_timeout"],
            }

            del self.active_sessions[session_token]

            return {
                "success": True,
                "new_session_token": new_token,
                "expires_in": self.config["session_timeout"],
            }
        else:
            return {"success": False, "error": "Invalid session token"}

    async def _handle_check_permissions(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Prüft Benutzerberechtigungen"""
        session_token = request.get("session_token")
        required_permission = request.get("permission")

        if not session_token or not required_permission:
            return {"error": "Session token and permission are required", "authorized": False}

        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            username = session["username"]

            # Einfache Berechtigungsprüfung (in echter Implementierung würde hier echte RBAC stehen)
            user_permissions = {
                "admin": ["read", "write", "delete", "admin"],
                "user": ["read", "write"],
                "guest": ["read"],
            }

            user_role = "admin" if username == "admin" else "user"
            permissions = user_permissions.get(user_role, [])

            authorized = required_permission in permissions

            return {
                "authorized": authorized,
                "user": {"username": username, "role": user_role},
                "permission": required_permission,
                "user_permissions": permissions,
            }
        else:
            return {"authorized": False, "error": "Invalid session token"}


class ValidationMCP(BaseMCP):
    """MCP für Datenvalidierung"""

    def __init__(self):
        super().__init__(
            name="validation_mcp", description="Validiert Eingabedaten und Anfragen", priority=5
        )
        self.config = {
            "max_string_length": 1000,
            "max_array_size": 100,
            "allowed_file_types": ["txt", "json", "csv", "xml"],
            "max_file_size": 10 * 1024 * 1024,  # 10MB
        }
        self.validation_rules = {}

    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Validierungsanfragen"""
        action = request.get("action")
        self.metrics["requests_processed"] += 1
        start_time = asyncio.get_event_loop().time()

        try:
            if action == "validate_data":
                result = await self._validate_data(request)
            elif action == "validate_schema":
                result = await self._validate_schema(request)
            elif action == "sanitize_input":
                result = await self._sanitize_input(request)
            elif action == "check_constraints":
                result = await self._check_constraints(request)
            else:
                result = {"error": f"Unknown action: {action}", "status": "error"}

            # Update metrics
            response_time = asyncio.get_event_loop().time() - start_time
            self.metrics["average_response_time"] = (
                self.metrics["average_response_time"] * (self.metrics["requests_processed"] - 1)
                + response_time
            ) / self.metrics["requests_processed"]
            self.metrics["last_activity"] = datetime.now().isoformat()

            return {"mcp": self.name, "action": action, "result": result, "status": "completed"}

        except Exception as e:
            self.metrics["errors"] += 1
            self.logger.error(f"Error processing validation request: {e}")
            return {"mcp": self.name, "action": action, "error": str(e), "status": "error"}

    async def _validate_data(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Validiert Daten basierend auf Typ und Regeln"""
        data = request.get("data")
        data_type = request.get("data_type", "string")
        rules = request.get("rules", {})

        if data is None:
            return {"valid": False, "errors": ["Data is required"]}

        errors = []

        # Typ-Validierung
        if data_type == "string":
            if not isinstance(data, str):
                errors.append("Data must be a string")
            elif len(data) > self.config["max_string_length"]:
                errors.append(f"String too long (max: {self.config['max_string_length']})")

        elif data_type == "email":
            if not isinstance(data, str):
                errors.append("Email must be a string")
            elif "@" not in data or "." not in data:
                errors.append("Invalid email format")

        elif data_type == "number":
            if not isinstance(data, (int, float)):
                errors.append("Data must be a number")
            else:
                min_val = rules.get("min")
                max_val = rules.get("max")
                if min_val is not None and data < min_val:
                    errors.append(f"Number too small (min: {min_val})")
                if max_val is not None and data > max_val:
                    errors.append(f"Number too large (max: {max_val})")

        elif data_type == "array":
            if not isinstance(data, (list, tuple)):
                errors.append("Data must be an array")
            elif len(data) > self.config["max_array_size"]:
                errors.append(f"Array too large (max: {self.config['max_array_size']})")

        # Zusätzliche Regeln
        if "required" in rules and rules["required"] and not data:
            errors.append("Field is required")

        if "pattern" in rules and isinstance(data, str):
            import re

            if not re.match(rules["pattern"], data):
                errors.append(f"Data does not match pattern: {rules['pattern']}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "data_type": data_type,
            "rules_applied": list(rules.keys()),
        }

    async def _validate_schema(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Validiert Daten gegen ein Schema"""
        data = request.get("data")
        schema = request.get("schema")

        if not schema:
            return {"valid": False, "errors": ["Schema is required"]}

        if not isinstance(data, dict):
            return {"valid": False, "errors": ["Data must be a dictionary"]}

        errors = []

        # Prüfe erforderliche Felder
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data:
                errors.append(f"Required field missing: {field}")

        # Prüfe Feldtypen
        properties = schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                field_schema = properties[field]
                field_type = field_schema.get("type")

                if field_type == "string" and not isinstance(value, str):
                    errors.append(f"Field '{field}' must be a string")
                elif field_type == "number" and not isinstance(value, (int, float)):
                    errors.append(f"Field '{field}' must be a number")
                elif field_type == "boolean" and not isinstance(value, bool):
                    errors.append(f"Field '{field}' must be a boolean")
                elif field_type == "array" and not isinstance(value, (list, tuple)):
                    errors.append(f"Field '{field}' must be an array")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "schema": schema,
            "fields_validated": len(properties),
        }

    async def _sanitize_input(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Bereinigt Eingabedaten"""
        data = request.get("data")
        sanitization_type = request.get("type", "html")

        if data is None:
            return {"sanitized_data": None, "changes_made": False}

        original_data = str(data)
        sanitized_data = original_data

        changes_made = False

        if sanitization_type == "html":
            # Einfache HTML-Sanitization
            import re

            # Entferne HTML-Tags
            sanitized_data = re.sub(r"<[^>]+>", "", sanitized_data)
            if sanitized_data != original_data:
                changes_made = True

        elif sanitization_type == "sql":
            # Einfache SQL-Injection-Prävention
            dangerous_patterns = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
            for pattern in dangerous_patterns:
                if pattern in sanitized_data:
                    sanitized_data = sanitized_data.replace(pattern, "")
                    changes_made = True

        elif sanitization_type == "xss":
            # Einfache XSS-Prävention
            dangerous_patterns = ["<script", "javascript:", "onload=", "onerror="]
            for pattern in dangerous_patterns:
                if pattern.lower() in sanitized_data.lower():
                    sanitized_data = sanitized_data.replace(pattern, "")
                    changes_made = True

        return {
            "original_data": original_data,
            "sanitized_data": sanitized_data,
            "changes_made": changes_made,
            "sanitization_type": sanitization_type,
        }

    async def _check_constraints(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Prüft Constraints auf Daten"""
        data = request.get("data")
        constraints = request.get("constraints", [])

        if not constraints:
            return {"valid": True, "violations": [], "message": "No constraints to check"}

        violations = []

        for constraint in constraints:
            constraint_type = constraint.get("type")
            field = constraint.get("field")
            value = constraint.get("value")

            if constraint_type == "unique" and field in data:
                # Simuliere Unique-Constraint-Prüfung
                violations.append(f"Field '{field}' must be unique")

            elif constraint_type == "foreign_key" and field in data:
                # Simuliere Foreign-Key-Constraint-Prüfung
                violations.append(f"Field '{field}' references non-existent record")

            elif constraint_type == "check" and field in data:
                # Simuliere Check-Constraint-Prüfung
                if data[field] < value:
                    violations.append(f"Field '{field}' violates check constraint")

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "constraints_checked": len(constraints),
        }


class RateLimitMCP(BaseMCP):
    """MCP für Rate Limiting"""

    def __init__(self):
        super().__init__(
            name="rate_limit_mcp",
            description="Implementiert Rate Limiting für API-Anfragen",
            priority=8,
        )
        self.config = {
            "default_limit": 100,  # requests per window
            "default_window": 3600,  # seconds
            "burst_limit": 10,  # requests per burst
            "burst_window": 60,  # seconds
        }
        self.request_counts = {}
        self.burst_counts = {}

    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Verarbeitet Rate-Limit-Anfragen"""
        action = request.get("action")
        self.metrics["requests_processed"] += 1
        start_time = asyncio.get_event_loop().time()

        try:
            if action == "check_limit":
                result = await self._check_rate_limit(request)
            elif action == "increment_counter":
                result = await self._increment_counter(request)
            elif action == "reset_limits":
                result = await self._reset_limits(request)
            elif action == "get_stats":
                result = await self._get_rate_limit_stats(request)
            else:
                result = {"error": f"Unknown action: {action}", "status": "error"}

            # Update metrics
            response_time = asyncio.get_event_loop().time() - start_time
            self.metrics["average_response_time"] = (
                self.metrics["average_response_time"] * (self.metrics["requests_processed"] - 1)
                + response_time
            ) / self.metrics["requests_processed"]
            self.metrics["last_activity"] = datetime.now().isoformat()

            return {"mcp": self.name, "action": action, "result": result, "status": "completed"}

        except Exception as e:
            self.metrics["errors"] += 1
            self.logger.error(f"Error processing rate limit request: {e}")
            return {"mcp": self.name, "action": action, "error": str(e), "status": "error"}

    async def _check_rate_limit(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Prüft ob ein Rate-Limit überschritten wurde"""
        identifier = request.get("identifier", "default")  # IP, User ID, etc.
        limit = request.get("limit", self.config["default_limit"])
        window = request.get("window", self.config["default_window"])

        current_time = datetime.now().timestamp()
        window_start = current_time - window

        # Hole aktuelle Request-Counts
        if identifier not in self.request_counts:
            self.request_counts[identifier] = []

        # Entferne alte Einträge
        self.request_counts[identifier] = [
            timestamp for timestamp in self.request_counts[identifier] if timestamp > window_start
        ]

        current_count = len(self.request_counts[identifier])
        allowed = current_count < limit

        # Prüfe auch Burst-Limit
        burst_allowed = True
        if identifier in self.burst_counts:
            burst_window_start = current_time - self.config["burst_window"]
            recent_bursts = [
                timestamp
                for timestamp in self.burst_counts[identifier]
                if timestamp > burst_window_start
            ]
            burst_allowed = len(recent_bursts) < self.config["burst_limit"]

        return {
            "allowed": allowed and burst_allowed,
            "current_count": current_count,
            "limit": limit,
            "window": window,
            "reset_time": window_start + window,
            "burst_allowed": burst_allowed,
            "identifier": identifier,
        }

    async def _increment_counter(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Erhöht den Request-Counter"""
        identifier = request.get("identifier", "default")
        current_time = datetime.now().timestamp()

        if identifier not in self.request_counts:
            self.request_counts[identifier] = []

        self.request_counts[identifier].append(current_time)

        # Auch Burst-Counter erhöhen
        if identifier not in self.burst_counts:
            self.burst_counts[identifier] = []
        self.burst_counts[identifier].append(current_time)

        return {
            "incremented": True,
            "identifier": identifier,
            "timestamp": current_time,
            "total_requests": len(self.request_counts[identifier]),
        }

    async def _reset_limits(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Setzt Rate-Limits zurück"""
        identifier = request.get("identifier")

        if identifier:
            if identifier in self.request_counts:
                del self.request_counts[identifier]
            if identifier in self.burst_counts:
                del self.burst_counts[identifier]
            return {"reset": True, "identifier": identifier}
        else:
            # Reset alle Limits
            self.request_counts.clear()
            self.burst_counts.clear()
            return {"reset": True, "all_identifiers": True}

    async def _get_rate_limit_stats(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Gibt Rate-Limit-Statistiken zurück"""
        identifier = request.get("identifier")

        if identifier and identifier in self.request_counts:
            current_count = len(self.request_counts[identifier])
            burst_count = len(self.burst_counts.get(identifier, []))

            return {
                "identifier": identifier,
                "current_requests": current_count,
                "burst_requests": burst_count,
                "limit": self.config["default_limit"],
                "burst_limit": self.config["burst_limit"],
            }
        else:
            return {
                "total_identifiers": len(self.request_counts),
                "config": self.config,
                "global_stats": {
                    "total_requests": sum(
                        len(requests) for requests in self.request_counts.values()
                    ),
                    "active_identifiers": len(self.request_counts),
                },
            }


# Initialisierungsfunktion
async def initialize():
    """Initialisiert alle MCPs"""
    print("Initializing MCPs...")

    mcps = {
        "authentication_mcp": AuthenticationMCP(),
        "validation_mcp": ValidationMCP(),
        "rate_limit_mcp": RateLimitMCP(),
    }

    for mcp in mcps.values():
        await mcp.initialize()

    print("MCPs initialized successfully!")
    return mcps
