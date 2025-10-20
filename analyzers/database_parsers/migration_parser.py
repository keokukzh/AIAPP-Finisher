"""
Migration Parser - Parses database migrations
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MigrationParser:
    """Parses database migration files"""

    async def extract_migrations(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extrahiert Migration-Dateien"""
        migrations = []

        try:
            all_files = file_structure.get("all_files", [])

            # Suche nach Migration-Verzeichnissen und -Dateien
            migration_patterns = [
                "migrations",
                "migrate",
                "alembic/versions",
                "db/migrate",
                "database/migrations",
                "prisma/migrations",
            ]

            for file_info in all_files:
                file_path_lower = file_info["path"].lower()

                # Prüfe ob Datei in Migration-Verzeichnis liegt
                if any(pattern in file_path_lower for pattern in migration_patterns):
                    if file_info["extension"].lower() in {".py", ".sql", ".js", ".ts"}:
                        migrations.append(
                            {
                                "name": Path(file_info["path"]).name,
                                "path": file_info["path"],
                                "type": self._detect_migration_type(file_info["path"]),
                                "timestamp": self._extract_migration_timestamp(
                                    Path(file_info["path"]).name
                                ),
                            }
                        )

        except Exception as e:
            logger.error(f"Fehler bei Migration-Extraktion: {e}")

        return migrations

    def _detect_migration_type(self, file_path: str) -> str:
        """Erkennt den Typ der Migration"""
        file_path_lower = file_path.lower()

        if "alembic" in file_path_lower:
            return "Alembic"
        elif "django" in file_path_lower or "migrations" in file_path_lower:
            return "Django"
        elif "prisma" in file_path_lower:
            return "Prisma"
        elif "sequelize" in file_path_lower:
            return "Sequelize"
        elif "flyway" in file_path_lower:
            return "Flyway"
        elif "liquibase" in file_path_lower:
            return "Liquibase"
        else:
            return "Unknown"

    def _extract_migration_timestamp(self, filename: str) -> str:
        """Extrahiert Zeitstempel aus Migration-Dateinamen"""
        # Suche nach Zeitstempel-Mustern
        patterns = [
            r"(\d{14})",  # YYYYMMDDHHmmss
            r"(\d{10})",  # Unix timestamp
            r"(\d{8})",  # YYYYMMDD
        ]

        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return match.group(1)

        return "unknown"

    async def detect_database_type(self, project_path: str, file_structure: Dict[str, Any]) -> str:
        """Erkennt den Datenbank-Typ aus Konfigurationsdateien"""
        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                file_path = Path(project_path) / file_info["path"]

                # Prüfe auf Konfigurationsdateien
                if any(
                    config in file_info["path"].lower()
                    for config in ["config", "settings", ".env", "database"]
                ):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read().lower()

                            # Suche nach Datenbank-Keywords
                            if "postgresql" in content or "postgres" in content:
                                return "PostgreSQL"
                            elif "mysql" in content:
                                return "MySQL"
                            elif "mongodb" in content or "mongo" in content:
                                return "MongoDB"
                            elif "sqlite" in content:
                                return "SQLite"
                            elif "redis" in content:
                                return "Redis"
                            elif "mariadb" in content:
                                return "MariaDB"
                            elif "oracle" in content:
                                return "Oracle"
                            elif "mssql" in content or "sqlserver" in content:
                                return "SQL Server"

                    except Exception:
                        continue

            return "Unknown"

        except Exception as e:
            logger.error(f"Fehler bei Database-Type-Erkennung: {e}")
            return "Unknown"
