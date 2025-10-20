"""
Package Parser - Parses package files (requirements.txt, package.json, etc.)
"""

import json
import logging
import re
from pathlib import Path
from typing import Any, Dict, List

import toml

logger = logging.getLogger(__name__)


class PackageParser:
    """Parses package dependency files"""

    async def parse_python_requirements(self, file_path: Path) -> List[str]:
        """Parse requirements.txt"""
        packages = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove version specifiers
                        package = re.split(r"[=<>!]", line)[0].strip()
                        if package:
                            packages.append(package)
        except Exception as e:
            logger.error(f"Error parsing requirements.txt: {e}")
        return packages

    async def parse_package_json(self, file_path: Path) -> Dict[str, List[str]]:
        """Parse package.json"""
        dependencies = {"dependencies": [], "devDependencies": []}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                dependencies["dependencies"] = list(data.get("dependencies", {}).keys())
                dependencies["devDependencies"] = list(data.get("devDependencies", {}).keys())
        except Exception as e:
            logger.error(f"Error parsing package.json: {e}")
        return dependencies

    async def parse_pipfile(self, file_path: Path) -> Dict[str, List[str]]:
        """Parse Pipfile"""
        dependencies = {"packages": [], "dev-packages": []}
        try:
            data = toml.load(file_path)
            dependencies["packages"] = list(data.get("packages", {}).keys())
            dependencies["dev-packages"] = list(data.get("dev-packages", {}).keys())
        except Exception as e:
            logger.error(f"Error parsing Pipfile: {e}")
        return dependencies

    async def parse_pyproject_toml(self, file_path: Path) -> List[str]:
        """Parse pyproject.toml"""
        packages = []
        try:
            data = toml.load(file_path)
            deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            packages = [k for k in deps.keys() if k != "python"]
        except Exception as e:
            logger.error(f"Error parsing pyproject.toml: {e}")
        return packages

    async def parse_composer_json(self, file_path: Path) -> List[str]:
        """Parse composer.json (PHP)"""
        packages = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                packages = list(data.get("require", {}).keys())
        except Exception as e:
            logger.error(f"Error parsing composer.json: {e}")
        return packages

    async def parse_gemfile(self, file_path: Path) -> List[str]:
        """Parse Gemfile (Ruby)"""
        packages = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r"\s*gem\s+['\"]([^'\"]+)['\"]", line)
                    if match:
                        packages.append(match.group(1))
        except Exception as e:
            logger.error(f"Error parsing Gemfile: {e}")
        return packages

    async def parse_go_mod(self, file_path: Path) -> List[str]:
        """Parse go.mod"""
        packages = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                in_require = False
                for line in f:
                    line = line.strip()
                    if line.startswith("require ("):
                        in_require = True
                    elif line == ")" and in_require:
                        in_require = False
                    elif in_require or line.startswith("require "):
                        match = re.match(r"require\s+([^\s]+)", line) or re.match(
                            r"([^\s]+)\s+v", line
                        )
                        if match:
                            packages.append(match.group(1))
        except Exception as e:
            logger.error(f"Error parsing go.mod: {e}")
        return packages
