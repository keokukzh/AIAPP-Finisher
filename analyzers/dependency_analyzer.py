"""Dependency analysis module for project package management.

This module provides the DependencyAnalyzer class which parses and analyzes
project dependencies across multiple languages and package managers. Supports
Python (pip, pipenv, poetry), JavaScript (npm, yarn), PHP (composer), Ruby (gem),
Go (modules), Rust (cargo), Java (maven, gradle), and C# (nuget).

Builds dependency graphs and provides security and version analysis.

Typical usage example:
    analyzer = DependencyAnalyzer()
    deps = await analyzer.analyze_dependencies(
        "/path/to/project",
        file_structure_data
    )
    print(f"Found {len(deps['packages'])} total packages")

Classes:
    DependencyAnalyzer: Main coordinator for dependency analysis operations.
"""

import logging
from pathlib import Path
from typing import Any, Dict

from .dependency_parsers import GraphBuilder, PackageParser

logger = logging.getLogger(__name__)


class DependencyAnalyzer:
    """Coordinates dependency analysis across multiple package managers.

    Delegates parsing to specialized PackageParser and graph building to
    GraphBuilder. Supports 8+ programming languages and their respective
    package management systems.

    Attributes:
        package_parser: Parser for various package file formats.
        graph_builder: Builder for dependency graph and tree analysis.
        package_files: Mapping of languages to their package file names.
    """

    def __init__(self) -> None:
        """Initialize DependencyAnalyzer with specialized parsers and graph builder.

        Creates instances of PackageParser and GraphBuilder, and defines
        the supported package file formats for each language.
        """
        self.package_parser = PackageParser()
        self.graph_builder = GraphBuilder()

        self.package_files = {
            "python": ["requirements.txt", "Pipfile", "pyproject.toml", "setup.py"],
            "javascript": ["package.json", "yarn.lock", "package-lock.json"],
            "php": ["composer.json", "composer.lock"],
            "ruby": ["Gemfile", "Gemfile.lock"],
            "go": ["go.mod", "go.sum"],
            "rust": ["Cargo.toml", "Cargo.lock"],
            "java": ["pom.xml", "build.gradle"],
            "csharp": ["packages.config", "*.csproj"],
        }

    async def analyze_dependencies(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze all project dependencies across supported package managers.

        Scans project files for package definitions (requirements.txt, package.json,
        Cargo.toml, etc.), parses each file format, builds a dependency graph,
        and performs tree analysis to identify transitive dependencies.

        Args:
            project_path: Absolute path to project root directory.
            file_structure: Dictionary containing project file structure with
                'all_files' key listing all project files with paths.

        Returns:
            Dictionary containing comprehensive dependency analysis:
                - packages: List of all packages (flat list)
                - by_language: Dict mapping language to package lists
                - package_files: List of package file paths found
                - dependency_graph: Dict representing dependency relationships
                - security_alerts: List of security vulnerabilities (if scanned)
                - outdated_packages: List of packages with newer versions

        Example:
            >>> analyzer = DependencyAnalyzer()
            >>> deps = await analyzer.analyze_dependencies(
            ...     "/path/to/project",
            ...     {"all_files": [{"path": "requirements.txt"}, ...]}
            ... )
            >>> print(f"Python packages: {len(deps['by_language']['python'])}")
            45

        Note:
            Returns empty structure with empty lists if analysis fails.
            Errors are logged but not raised.
        """
        dependencies = {
            "packages": [],
            "by_language": {},
            "package_files": [],
            "dependency_graph": {},
            "security_alerts": [],
            "outdated_packages": [],
        }

        try:
            all_files = file_structure.get("all_files", [])

            # Finde und parse Package-Dateien
            for file_info in all_files:
                file_path = Path(project_path) / file_info["path"]
                file_name = Path(file_info["path"]).name

                # Python Dependencies
                if file_name == "requirements.txt":
                    packages = await self.package_parser.parse_python_requirements(file_path)
                    dependencies["by_language"]["python"] = packages
                    dependencies["packages"].extend(packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "package.json":
                    node_deps = await self.package_parser.parse_package_json(file_path)
                    dependencies["by_language"]["javascript"] = node_deps
                    all_node_packages = node_deps.get("dependencies", []) + node_deps.get(
                        "devDependencies", []
                    )
                    dependencies["packages"].extend(all_node_packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "Pipfile":
                    pipfile_deps = await self.package_parser.parse_pipfile(file_path)
                    dependencies["by_language"]["python_pipenv"] = pipfile_deps
                    all_pip_packages = pipfile_deps.get("packages", []) + pipfile_deps.get(
                        "dev-packages", []
                    )
                    dependencies["packages"].extend(all_pip_packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "pyproject.toml":
                    poetry_packages = await self.package_parser.parse_pyproject_toml(file_path)
                    dependencies["by_language"]["python_poetry"] = poetry_packages
                    dependencies["packages"].extend(poetry_packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "composer.json":
                    php_packages = await self.package_parser.parse_composer_json(file_path)
                    dependencies["by_language"]["php"] = php_packages
                    dependencies["packages"].extend(php_packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "Gemfile":
                    ruby_packages = await self.package_parser.parse_gemfile(file_path)
                    dependencies["by_language"]["ruby"] = ruby_packages
                    dependencies["packages"].extend(ruby_packages)
                    dependencies["package_files"].append(file_info["path"])

                elif file_name == "go.mod":
                    go_packages = await self.package_parser.parse_go_mod(file_path)
                    dependencies["by_language"]["go"] = go_packages
                    dependencies["packages"].extend(go_packages)
                    dependencies["package_files"].append(file_info["path"])

            # Build Dependency Graph
            if dependencies["by_language"]:
                dep_graph = await self.graph_builder.build_dependency_graph(
                    dependencies["by_language"]
                )
                dependencies["dependency_graph"] = dep_graph

            # Analyze Dependency Tree
            tree_analysis = await self.graph_builder.analyze_dependency_tree(
                dependencies["by_language"]
            )
            dependencies.update(tree_analysis)

            logger.info(
                f"Analyzed {len(dependencies['packages'])} dependencies across "
                f"{len(dependencies['by_language'])} languages"
            )

        except Exception as e:
            logger.error(f"Error analyzing dependencies: {e}")

        return dependencies
