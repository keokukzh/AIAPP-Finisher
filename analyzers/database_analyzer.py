"""Database schema analysis module for ORM and SQL extraction.

This module provides the DatabaseAnalyzer class which extracts database schemas,
models, relationships, migrations, and constraints from projects using various
ORM frameworks (SQLAlchemy, Django ORM, Prisma, Mongoose, Sequelize) and
direct SQL files.

Coordinates schema parsing and migration analysis to provide comprehensive
database structure information.

Typical usage example:
    analyzer = DatabaseAnalyzer()
    schema = await analyzer.extract_schema(
        "/path/to/project",
        file_structure_data
    )
    print(f"Found {len(schema['models'])} models")

Classes:
    DatabaseAnalyzer: Main coordinator for database schema analysis.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .database_parsers import MigrationParser, SchemaParser

logger = logging.getLogger(__name__)


class DatabaseAnalyzer:
    """Coordinates database schema extraction and analysis.

    Delegates parsing to specialized SchemaParser and MigrationParser instances.
    Detects ORM frameworks, extracts models and tables, analyzes relationships,
    and identifies database types.

    Attributes:
        schema_parser: Parser for ORM models and SQL schemas.
        migration_parser: Parser for database migration files.
        orm_frameworks: Mapping of ORM framework names to their import signatures.
    """

    def __init__(self) -> None:
        """Initialize DatabaseAnalyzer with specialized parsers.

        Creates instances of SchemaParser and MigrationParser, and defines
        the supported ORM frameworks with their characteristic import patterns.
        """
        self.schema_parser = SchemaParser()
        self.migration_parser = MigrationParser()

        self.orm_frameworks = {
            "SQLAlchemy": ["sqlalchemy", "from sqlalchemy"],
            "Django ORM": ["django.db.models", "from django.db import models"],
            "Prisma": ["prisma"],
            "Mongoose": ["mongoose", "from mongoose"],
            "Sequelize": ["sequelize", "from sequelize"],
        }

    async def extract_schema(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract complete database schema from project files.

        Performs comprehensive database analysis including ORM framework detection,
        model extraction, SQL schema parsing, migration analysis, relationship
        mapping, and database type identification.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing project file structure with
                'all_files' key listing all project files.

        Returns:
            Dictionary containing complete schema analysis:
                - tables: List of database tables with columns
                - models: List of ORM model definitions
                - relationships: List of foreign key and relationship definitions
                - orm_framework: Detected ORM framework name (or None)
                - database_type: Detected database type (PostgreSQL, MySQL, etc.)
                - migrations: List of migration files with operations
                - indexes: List of database indexes
                - constraints: List of constraints (unique, check, etc.)

        Example:
            >>> analyzer = DatabaseAnalyzer()
            >>> schema = await analyzer.extract_schema(
            ...     "/path/to/project",
            ...     {"all_files": [{"path": "models.py", "extension": ".py"}, ...]}
            ... )
            >>> print(f"ORM: {schema['orm_framework']}")
            'SQLAlchemy'

        Note:
            Returns schema structure with empty lists if extraction fails.
            Errors are logged but not raised.
        """
        schema = {
            "tables": [],
            "models": [],
            "relationships": [],
            "orm_framework": None,
            "database_type": None,
            "migrations": [],
            "indexes": [],
            "constraints": [],
        }

        try:
            # 1. Erkenne ORM-Framework
            orm_framework = await self._detect_orm_framework(project_path, file_structure)
            schema["orm_framework"] = orm_framework

            # 2. Extrahiere ORM-Models
            if orm_framework:
                models = await self.schema_parser.extract_orm_models(
                    project_path, file_structure, orm_framework
                )
                schema["models"] = models

            # 3. Extrahiere SQL-Schema
            sql_schema = await self.schema_parser.extract_sql_schema(project_path, file_structure)
            schema["tables"].extend(sql_schema.get("tables", []))
            schema["indexes"].extend(sql_schema.get("indexes", []))

            # 4. Extrahiere Migrations
            migrations = await self.migration_parser.extract_migrations(
                project_path, file_structure
            )
            schema["migrations"] = migrations

            # 5. Analysiere Relationships
            relationships = await self.schema_parser.analyze_relationships(
                schema["models"], schema["tables"]
            )
            schema["relationships"] = relationships

            # 6. Erkenne Database-Typ
            database_type = await self.migration_parser.detect_database_type(
                project_path, file_structure
            )
            schema["database_type"] = database_type

            logger.info(
                f"Extrahiert: {len(schema['models'])} Models, {len(schema['tables'])} Tables, "
                f"ORM: {orm_framework}, DB: {database_type}"
            )
            return schema

        except Exception as e:
            logger.error(f"Fehler bei der Schema-Extraktion: {e}")
            return schema

    async def _detect_orm_framework(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Optional[str]:
        """Detect the ORM framework used in the project.

        Searches for characteristic files (schema.prisma) and import patterns
        (sqlalchemy, django.db.models, etc.) to identify the ORM framework.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing 'all_files' with file metadata.

        Returns:
            Name of detected ORM framework ('SQLAlchemy', 'Django ORM', 'Prisma',
            'Mongoose', 'Sequelize'), or None if no ORM detected.

        Note:
            Returns None if detection fails or no ORM framework is found.
        """
        try:
            all_files = file_structure.get("all_files", [])

            # Prüfe auf Prisma-Schema-Datei
            for file_info in all_files:
                if "schema.prisma" in file_info["path"]:
                    return "Prisma"

            # Prüfe auf ORM-Imports in Code-Dateien
            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            for framework_name, imports in self.orm_frameworks.items():
                                if any(imp in content for imp in imports):
                                    return framework_name

                    except Exception:
                        continue

            return None

        except Exception as e:
            logger.error(f"Fehler bei der ORM-Framework-Erkennung: {e}")
            return None
