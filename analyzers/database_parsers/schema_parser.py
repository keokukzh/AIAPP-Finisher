"""
Schema Parser - Parses ORM models and SQL schemas
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SchemaParser:
    """Parses database schemas from ORM models and SQL files"""

    def __init__(self):
        self.orm_patterns = {
            "SQLAlchemy": {
                "imports": ["sqlalchemy", "from sqlalchemy"],
                "patterns": [
                    r"class\s+(\w+)\(.*Base.*\):",
                    r'__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]',
                    r"(\w+)\s*=\s*Column\(",
                    r"relationship\(",
                    r"ForeignKey\(",
                ],
            },
            "Django ORM": {
                "imports": ["django.db.models", "from django.db import models"],
                "patterns": [
                    r"class\s+(\w+)\(models\.Model\):",
                    r"class\s+Meta:",
                    r'db_table\s*=\s*[\'"]([^\'"]+)[\'"]',
                    r"(\w+)\s*=\s*models\.(\w+)\(",
                    r"ForeignKey\(",
                    r"ManyToManyField\(",
                ],
            },
            "Prisma": {
                "files": ["schema.prisma"],
                "patterns": [
                    r"model\s+(\w+)\s*\{",
                    r"(\w+)\s+(\w+)\s+@",
                    r'@@map\("([^"]+)"\)',
                    r"@relation\(",
                ],
            },
            "Mongoose": {
                "imports": ["mongoose", "from mongoose"],
                "patterns": [
                    r"const\s+(\w+)Schema\s*=",
                    r"mongoose\.model\(",
                    r"(\w+):\s*\{",
                    r"type:\s*Schema\.Types\.(\w+)",
                    r'ref:\s*[\'"]([^\'"]+)[\'"]',
                ],
            },
            "Sequelize": {
                "imports": ["sequelize", "from sequelize"],
                "patterns": [
                    r"class\s+(\w+)\s+extends\s+Model",
                    r"(\w+):\s*\{",
                    r"type:\s*DataTypes\.(\w+)",
                    r"belongsTo\(",
                    r"hasMany\(",
                ],
            },
        }

        self.sql_patterns = {
            "CREATE_TABLE": r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s\(]+)",
            "ALTER_TABLE": r"ALTER\s+TABLE\s+([^\s]+)",
            "CREATE_INDEX": r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+([^\s]+)",
            "FOREIGN_KEY": r"FOREIGN\s+KEY\s+\(([^)]+)\)\s+REFERENCES\s+([^\s]+)",
            "PRIMARY_KEY": r"PRIMARY\s+KEY\s+\(([^)]+)\)",
            "COLUMN_DEFINITION": r"(\w+)\s+(\w+)(?:\s+([^,]+))?",
        }

    async def extract_orm_models(
        self, project_path: str, file_structure: Dict[str, Any], orm_framework: str
    ) -> List[Dict[str, Any]]:
        """Extrahiert ORM-Models basierend auf dem erkannten Framework"""
        models = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() in {".py", ".js", ".ts"}:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            # Prüfe ob ORM-Imports vorhanden sind
                            orm_info = self.orm_patterns.get(orm_framework, {})
                            if "imports" in orm_info:
                                has_imports = any(imp in content for imp in orm_info["imports"])
                                if not has_imports:
                                    continue

                            # Extrahiere Models basierend auf Framework
                            if orm_framework == "SQLAlchemy":
                                models.extend(
                                    await self._extract_sqlalchemy_models(
                                        content, file_info["path"]
                                    )
                                )
                            elif orm_framework == "Django ORM":
                                models.extend(
                                    await self._extract_django_models(content, file_info["path"])
                                )
                            elif orm_framework == "Mongoose":
                                models.extend(
                                    await self._extract_mongoose_models(content, file_info["path"])
                                )
                            elif orm_framework == "Sequelize":
                                models.extend(
                                    await self._extract_sequelize_models(content, file_info["path"])
                                )

                    except Exception as e:
                        logger.debug(f"Fehler beim Lesen von {file_path}: {e}")
                        continue

            # Prisma hat spezielle Schema-Dateien
            if orm_framework == "Prisma":
                prisma_models = await self._extract_prisma_models(project_path, file_structure)
                models.extend(prisma_models)

            return models

        except Exception as e:
            logger.error(f"Fehler bei der ORM-Model-Extraktion: {e}")
            return models

    async def _extract_sqlalchemy_models(
        self, content: str, file_path: str
    ) -> List[Dict[str, Any]]:
        """Extrahiert SQLAlchemy-Models"""
        models = []

        try:
            class_pattern = r"class\s+(\w+)\(.*Base.*\):"
            class_matches = re.finditer(class_pattern, content)

            for match in class_matches:
                model_name = match.group(1)

                # Finde tablename
                tablename_pattern = (
                    rf'class\s+{model_name}.*?__tablename__\s*=\s*[\'"]([^\'"]+)[\'"]'
                )
                tablename_match = re.search(tablename_pattern, content, re.DOTALL)
                table_name = tablename_match.group(1) if tablename_match else model_name.lower()

                # Finde Spalten
                columns = []
                column_pattern = r"(\w+)\s*=\s*Column\(([^)]+)\)"
                column_matches = re.finditer(column_pattern, content)

                for col_match in column_matches:
                    columns.append(
                        {
                            "name": col_match.group(1),
                            "type": (
                                col_match.group(2).split(",")[0].strip()
                                if "," in col_match.group(2)
                                else col_match.group(2).strip()
                            ),
                        }
                    )

                models.append(
                    {
                        "name": model_name,
                        "table_name": table_name,
                        "orm": "SQLAlchemy",
                        "file_path": file_path,
                        "columns": columns,
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei SQLAlchemy-Model-Extraktion: {e}")

        return models

    async def _extract_django_models(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Django-Models"""
        models = []

        try:
            class_pattern = r"class\s+(\w+)\(models\.Model\):"
            class_matches = re.finditer(class_pattern, content)

            for match in class_matches:
                model_name = match.group(1)

                # Finde db_table in Meta
                meta_pattern = (
                    rf'class\s+{model_name}.*?class\s+Meta:.*?db_table\s*=\s*[\'"]([^\'"]+)[\'"]'
                )
                meta_match = re.search(meta_pattern, content, re.DOTALL)
                table_name = meta_match.group(1) if meta_match else model_name.lower()

                # Finde Felder
                columns = []
                field_pattern = r"(\w+)\s*=\s*models\.(\w+)\("
                field_matches = re.finditer(field_pattern, content)

                for field_match in field_matches:
                    columns.append({"name": field_match.group(1), "type": field_match.group(2)})

                models.append(
                    {
                        "name": model_name,
                        "table_name": table_name,
                        "orm": "Django ORM",
                        "file_path": file_path,
                        "columns": columns,
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Django-Model-Extraktion: {e}")

        return models

    async def _extract_mongoose_models(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Mongoose-Models"""
        models = []

        try:
            model_pattern = r'const\s+(\w+)\s*=\s*mongoose\.model\([\'"]([^\'"]+)[\'"]'
            model_matches = re.finditer(model_pattern, content)

            for match in model_matches:
                model_name = match.group(1)
                collection_name = match.group(2)

                models.append(
                    {
                        "name": model_name,
                        "table_name": collection_name,
                        "orm": "Mongoose",
                        "file_path": file_path,
                        "columns": [],
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Mongoose-Model-Extraktion: {e}")

        return models

    async def _extract_sequelize_models(self, content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extrahiert Sequelize-Models"""
        models = []

        try:
            class_pattern = r"class\s+(\w+)\s+extends\s+Model"
            class_matches = re.finditer(class_pattern, content)

            for match in class_matches:
                model_name = match.group(1)

                models.append(
                    {
                        "name": model_name,
                        "table_name": model_name.lower(),
                        "orm": "Sequelize",
                        "file_path": file_path,
                        "columns": [],
                    }
                )

        except Exception as e:
            logger.error(f"Fehler bei Sequelize-Model-Extraktion: {e}")

        return models

    async def _extract_prisma_models(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extrahiert Prisma-Models aus schema.prisma"""
        models = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if "schema.prisma" in file_info["path"]:
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()

                            # Extrahiere Models
                            model_pattern = r"model\s+(\w+)\s*\{([^}]+)\}"
                            model_matches = re.finditer(model_pattern, content, re.DOTALL)

                            for match in model_matches:
                                model_name = match.group(1)
                                model_body = match.group(2)

                                # Extrahiere Felder
                                columns = []
                                field_pattern = r"(\w+)\s+(\w+)"
                                field_matches = re.finditer(field_pattern, model_body)

                                for field_match in field_matches:
                                    columns.append(
                                        {"name": field_match.group(1), "type": field_match.group(2)}
                                    )

                                models.append(
                                    {
                                        "name": model_name,
                                        "table_name": model_name.lower(),
                                        "orm": "Prisma",
                                        "file_path": file_info["path"],
                                        "columns": columns,
                                    }
                                )

                    except Exception as e:
                        logger.debug(f"Fehler beim Lesen von Prisma-Schema: {e}")

        except Exception as e:
            logger.error(f"Fehler bei Prisma-Model-Extraktion: {e}")

        return models

    async def extract_sql_schema(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extrahiert SQL-Schema aus .sql Dateien"""
        tables = []
        indexes = []

        try:
            all_files = file_structure.get("all_files", [])

            for file_info in all_files:
                if file_info["extension"].lower() == ".sql":
                    file_path = Path(project_path) / file_info["path"]

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()

                            # Extrahiere CREATE TABLE
                            create_table_matches = re.finditer(
                                self.sql_patterns["CREATE_TABLE"], content, re.IGNORECASE
                            )
                            for match in create_table_matches:
                                table_name = match.group(1).strip("`\"'")
                                tables.append(
                                    {
                                        "name": table_name,
                                        "source": "sql",
                                        "file_path": file_info["path"],
                                    }
                                )

                            # Extrahiere CREATE INDEX
                            index_matches = re.finditer(
                                self.sql_patterns["CREATE_INDEX"], content, re.IGNORECASE
                            )
                            for match in index_matches:
                                index_name = match.group(1).strip("`\"'")
                                indexes.append({"name": index_name, "file_path": file_info["path"]})

                    except Exception as e:
                        logger.debug(f"Fehler beim Lesen von SQL-Datei: {e}")

        except Exception as e:
            logger.error(f"Fehler bei SQL-Schema-Extraktion: {e}")

        return {"tables": tables, "indexes": indexes}

    async def analyze_relationships(
        self, models: List[Dict[str, Any]], tables: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analysiert Beziehungen zwischen Models/Tables"""
        relationships = []

        try:
            # Einfache Relationship-Erkennung basierend auf Foreign Keys
            for model in models:
                for column in model.get("columns", []):
                    if (
                        "foreign" in column.get("type", "").lower()
                        or "fk" in column.get("name", "").lower()
                    ):
                        relationships.append(
                            {
                                "from": model.get("name"),
                                "to": column.get("name").replace("_id", "").replace("_fk", ""),
                                "type": "foreign_key",
                                "column": column.get("name"),
                            }
                        )

        except Exception as e:
            logger.error(f"Fehler bei Relationship-Analyse: {e}")

        return relationships
