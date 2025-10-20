"""Backend Framework Detector"""

import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class BackendDetector:
    """Detects backend frameworks"""

    def __init__(self):
        self.frameworks = {
            "FastAPI": ["fastapi"],
            "Django": ["django"],
            "Flask": ["flask"],
            "Express.js": ["express"],
            "NestJS": ["@nestjs/core"],
            "Spring Boot": ["spring-boot"],
            "Laravel": ["laravel/framework"],
        }

    async def detect(self, project_path: str, file_structure: Dict) -> List[Dict]:
        """Detect backend frameworks"""
        detected = []

        # Check Python requirements
        for file_info in file_structure.get("all_files", []):
            if file_info["path"] == "requirements.txt":
                file_path = Path(project_path) / file_info["path"]
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                        for framework, keywords in self.frameworks.items():
                            if any(kw in content for kw in keywords):
                                detected.append(
                                    {"name": framework, "type": "Backend", "confidence": 0.9}
                                )
                except Exception as e:
                    logger.debug(f"Error detecting backend: {e}")

            # Check package.json for Node backends
            if file_info["path"] == "package.json":
                file_path = Path(project_path) / file_info["path"]
                try:
                    import json

                    with open(file_path, "r", encoding="utf-8") as f:
                        package_data = json.load(f)
                        deps = package_data.get("dependencies", {})
                        for framework, keywords in self.frameworks.items():
                            if any(kw in deps for kw in keywords):
                                detected.append(
                                    {"name": framework, "type": "Backend", "confidence": 0.9}
                                )
                except Exception as e:
                    logger.debug(f"Error detecting backend: {e}")

        return detected
