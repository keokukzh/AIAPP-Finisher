"""Language detection module for project analysis.

This module provides the LanguageDetector class which identifies programming
languages used in a project by analyzing file extensions, special files,
project structure, and file content. Supports detection of 30+ languages
and frameworks.

Typical usage example:
    detector = LanguageDetector()
    languages = await detector.detect_languages(
        "/path/to/project",
        file_structure_data
    )
    print(f"Detected: {languages}")

Classes:
    LanguageDetector: Main class for language detection operations.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detects programming languages and frameworks in a project.

    Analyzes file extensions, special configuration files, directory structure,
    and file content to identify all programming languages and frameworks used
    in a project. Provides prioritized results based on file counts.
    """

    def __init__(self):
        # Sprach-zu-Extension-Mapping
        self.language_extensions = {
            "Python": {".py", ".pyw", ".pyc", ".pyo", ".pyd"},
            "JavaScript": {".js", ".mjs"},
            "TypeScript": {".ts", ".tsx"},
            "Java": {".java", ".class", ".jar"},
            "C++": {".cpp", ".cc", ".cxx", ".c++", ".hpp", ".hxx"},
            "C": {".c", ".h"},
            "C#": {".cs", ".csx"},
            "PHP": {".php", ".phtml", ".php3", ".php4", ".php5"},
            "Ruby": {".rb", ".rbw"},
            "Go": {".go"},
            "Rust": {".rs"},
            "Swift": {".swift"},
            "Kotlin": {".kt", ".kts"},
            "Scala": {".scala", ".sc"},
            "R": {".r", ".R"},
            "MATLAB": {".m", ".mat"},
            "Shell": {".sh", ".bash", ".zsh", ".fish"},
            "PowerShell": {".ps1", ".psm1", ".psd1"},
            "HTML": {".html", ".htm"},
            "CSS": {".css", ".scss", ".sass", ".less"},
            "SQL": {".sql", ".sqlite", ".db"},
            "JSON": {".json"},
            "XML": {".xml"},
            "YAML": {".yml", ".yaml"},
            "Markdown": {".md", ".markdown"},
            "Dockerfile": {"Dockerfile", "dockerfile"},
            "Makefile": {"Makefile", "makefile"},
            "CMake": {"CMakeLists.txt"},
            "Vue": {".vue"},
            "React": {".jsx"},
            "Angular": {".component.ts", ".service.ts", ".module.ts"},
        }

        # Spezielle Dateien
        self.special_files = {
            "package.json": "Node.js",
            "requirements.txt": "Python",
            "Pipfile": "Python",
            "pyproject.toml": "Python",
            "composer.json": "PHP",
            "Gemfile": "Ruby",
            "Cargo.toml": "Rust",
            "go.mod": "Go",
            "pom.xml": "Java",
            "build.gradle": "Java",
            "Dockerfile": "Docker",
            "docker-compose.yml": "Docker",
            "README.md": "Documentation",
            "LICENSE": "Documentation",
        }

    async def detect_languages(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[str]:
        """Detect all programming languages used in the project.

        Performs comprehensive language detection by analyzing file extensions,
        special configuration files, project structure patterns, and file content.
        Returns a prioritized list of detected languages.

        Args:
            project_path: Absolute path to the project root directory.
            file_structure: Dictionary containing project file structure with
                keys 'file_types', 'all_files', and 'directories'.

        Returns:
            List of detected language names, sorted by prevalence (most common first).
            Returns ["Unknown"] if detection fails. Maximum of 10 languages returned.

        Example:
            >>> detector = LanguageDetector()
            >>> langs = await detector.detect_languages(
            ...     "/path/to/project",
            ...     {"file_types": {".py": 50, ".js": 20}}
            ... )
            >>> print(langs)
            ['Python', 'JavaScript']
        """
        detected_languages = set()

        try:
            # Analysiere Dateierweiterungen
            file_types = file_structure.get("file_types", {})
            for extension, count in file_types.items():
                language = self._get_language_by_extension(extension)
                if language:
                    detected_languages.add(language)

            # Analysiere spezielle Dateien
            all_files = file_structure.get("all_files", [])
            for file_info in all_files:
                file_name = Path(file_info["path"]).name
                if file_name in self.special_files:
                    detected_languages.add(self.special_files[file_name])

            # Analysiere Projekt-Struktur
            structure_languages = await self._detect_by_structure(project_path, file_structure)
            detected_languages.update(structure_languages)

            # Analysiere Inhalt von Konfigurationsdateien
            content_languages = await self._detect_by_content(project_path, file_structure)
            detected_languages.update(content_languages)

            # Filtere und priorisiere
            filtered_languages = self._filter_and_prioritize(detected_languages, file_structure)

            logger.info(f"Erkannte Sprachen: {filtered_languages}")
            return filtered_languages

        except Exception as e:
            logger.error(f"Fehler bei der Sprach-Erkennung: {e}")
            return ["Unknown"]

    def _get_language_by_extension(self, extension: str) -> Optional[str]:
        """Get programming language by file extension.

        Args:
            extension: File extension including the dot (e.g., '.py').

        Returns:
            Language name if extension is recognized, None otherwise.
        """
        extension = extension.lower()

        for language, extensions in self.language_extensions.items():
            if extension in extensions:
                return language

        return None

    async def _detect_by_structure(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Set[str]:
        """Detect languages based on project directory structure.

        Identifies languages and frameworks by looking for characteristic
        directory names like node_modules, __pycache__, vendor, etc.

        Args:
            project_path: Absolute path to project root (currently unused,
                kept for API consistency).
            file_structure: Dictionary containing 'directories' key with
                list of directory paths.

        Returns:
            Set of detected language/framework names based on structure patterns.
        """
        detected = set()

        try:
            directories = file_structure.get("directories", [])

            # Typische Projekt-Strukturen
            if any("src" in dir_path for dir_path in directories):
                detected.add("Structured Project")

            if any("tests" in dir_path or "test" in dir_path for dir_path in directories):
                detected.add("Testing Framework")

            if any("node_modules" in dir_path for dir_path in directories):
                detected.add("Node.js")

            if any("__pycache__" in dir_path for dir_path in directories):
                detected.add("Python")

            if any("target" in dir_path for dir_path in directories):
                detected.add("Java")

            if any("vendor" in dir_path for dir_path in directories):
                detected.add("PHP")

            # Framework-spezifische Strukturen
            if any("components" in dir_path for dir_path in directories):
                detected.add("React/Vue/Angular")

            if any("templates" in dir_path for dir_path in directories):
                detected.add("Django/Flask")

            if any("app" in dir_path for dir_path in directories):
                detected.add("Mobile App")

        except Exception as e:
            logger.error(f"Fehler bei der Struktur-Analyse: {e}")

        return detected

    async def _detect_by_content(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Set[str]:
        """Detect languages and frameworks by analyzing file content.

        Reads and parses configuration files (package.json, requirements.txt,
        Dockerfile) to identify specific frameworks and tools.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing file structure (currently unused,
                kept for API consistency).

        Returns:
            Set of detected language/framework names from file content analysis.
        """
        detected = set()

        try:
            # Analysiere package.json
            package_json_path = Path(project_path) / "package.json"
            if package_json_path.exists():
                try:
                    with open(package_json_path, "r", encoding="utf-8") as f:
                        package_data = json.load(f)

                        # Erkenne Frameworks
                        dependencies = package_data.get("dependencies", {})
                        dev_dependencies = package_data.get("devDependencies", {})
                        all_deps = {**dependencies, **dev_dependencies}

                        if "react" in all_deps:
                            detected.add("React")
                        if "vue" in all_deps:
                            detected.add("Vue")
                        if "@angular/core" in all_deps:
                            detected.add("Angular")
                        if "express" in all_deps:
                            detected.add("Express.js")
                        if "next" in all_deps:
                            detected.add("Next.js")
                        if "nuxt" in all_deps:
                            detected.add("Nuxt.js")

                except Exception as e:
                    logger.debug(f"Fehler beim Lesen von package.json: {e}")

            # Analysiere requirements.txt
            requirements_path = Path(project_path) / "requirements.txt"
            if requirements_path.exists():
                try:
                    with open(requirements_path, "r", encoding="utf-8") as f:
                        content = f.read().lower()

                        if "django" in content:
                            detected.add("Django")
                        if "flask" in content:
                            detected.add("Flask")
                        if "fastapi" in content:
                            detected.add("FastAPI")
                        if "pytest" in content:
                            detected.add("pytest")

                except Exception as e:
                    logger.debug(f"Fehler beim Lesen von requirements.txt: {e}")

            # Analysiere Dockerfile
            dockerfile_path = Path(project_path) / "Dockerfile"
            if dockerfile_path.exists():
                try:
                    with open(dockerfile_path, "r", encoding="utf-8") as f:
                        content = f.read().lower()

                        if "python" in content:
                            detected.add("Python Docker")
                        if "node" in content:
                            detected.add("Node.js Docker")
                        if "java" in content:
                            detected.add("Java Docker")

                except Exception as e:
                    logger.debug(f"Fehler beim Lesen von Dockerfile: {e}")

        except Exception as e:
            logger.error(f"Fehler bei der Content-Analyse: {e}")

        return detected

    def _filter_and_prioritize(
        self, languages: Set[str], file_structure: Dict[str, Any]
    ) -> List[str]:
        """Filter and prioritize detected languages by file count.

        Removes generic/non-language entries and sorts remaining languages
        by the number of files of each language type.

        Args:
            languages: Set of detected language/framework names.
            file_structure: Dictionary containing 'file_types' with extension counts.

        Returns:
            Sorted list of up to 10 languages, most prevalent first.
        """
        # Entferne generische/irrelevante Sprachen
        filtered = set()

        for language in languages:
            if language not in ["Structured Project", "Testing Framework", "Documentation"]:
                filtered.add(language)

        # Priorisiere basierend auf Dateianzahl
        file_types = file_structure.get("file_types", {})
        language_scores = {}

        for language in filtered:
            score = 0
            if language in self.language_extensions:
                for ext in self.language_extensions[language]:
                    score += file_types.get(ext, 0)
            language_scores[language] = score

        # Sortiere nach Score
        sorted_languages = sorted(filtered, key=lambda x: language_scores.get(x, 0), reverse=True)

        return sorted_languages[:10]  # Top 10 Sprachen

    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get detailed information about a programming language.

        Args:
            language: Name of the programming language.

        Returns:
            Dictionary containing language metadata:
                - name: Language name
                - extensions: List of file extensions
                - type: Category (Frontend/Backend/Mobile/Data Science/General)
                - description: Brief language description
        """
        info = {
            "name": language,
            "extensions": list(self.language_extensions.get(language, set())),
            "type": self._get_language_type(language),
            "description": self._get_language_description(language),
        }

        return info

    def _get_language_type(self, language: str) -> str:
        """Determine the category type of a programming language.

        Args:
            language: Name of the programming language.

        Returns:
            Category string: 'Frontend', 'Backend', 'Mobile', 'Data Science', or 'General'.
        """
        web_languages = {"HTML", "CSS", "JavaScript", "TypeScript", "React", "Vue", "Angular"}
        backend_languages = {"Python", "Java", "C#", "PHP", "Ruby", "Go", "Rust", "Node.js"}
        mobile_languages = {"Swift", "Kotlin", "React Native", "Flutter"}
        data_languages = {"R", "MATLAB", "SQL"}

        if language in web_languages:
            return "Frontend"
        elif language in backend_languages:
            return "Backend"
        elif language in mobile_languages:
            return "Mobile"
        elif language in data_languages:
            return "Data Science"
        else:
            return "General"

    def _get_language_description(self, language: str) -> str:
        """Get a brief description of a programming language.

        Args:
            language: Name of the programming language.

        Returns:
            Brief description string. Returns generic message if language not in database.
        """
        descriptions = {
            "Python": "Interpretierte, objektorientierte Programmiersprache",
            "JavaScript": "Skriptsprache für Web-Entwicklung",
            "TypeScript": "Typisierte Erweiterung von JavaScript",
            "Java": "Objektorientierte Programmiersprache",
            "C++": "Erweiterte Version der Programmiersprache C",
            "C#": "Objektorientierte Programmiersprache von Microsoft",
            "PHP": "Skriptsprache für Web-Entwicklung",
            "Ruby": "Objektorientierte Skriptsprache",
            "Go": "Programmiersprache von Google",
            "Rust": "Systemprogrammiersprache",
            "React": "JavaScript-Bibliothek für UI-Entwicklung",
            "Vue": "Progressive JavaScript-Framework",
            "Angular": "TypeScript-basiertes Web-Framework",
        }

        return descriptions.get(language, "Programmiersprache oder Framework")
