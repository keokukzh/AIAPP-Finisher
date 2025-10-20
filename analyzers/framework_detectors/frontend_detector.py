"""Frontend Framework Detector"""

import logging
import re
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class FrontendDetector:
    """Detects frontend frameworks"""

    def __init__(self):
        self.frameworks = {
            "React": ["react", "react-dom", "jsx"],
            "Vue.js": ["vue", "vuex", "vue-router"],
            "Angular": ["@angular/core", "@angular/common"],
            "Svelte": ["svelte"],
            "Next.js": ["next"],
            "Nuxt.js": ["nuxt"],
            "Gatsby": ["gatsby"],
        }

    async def detect(self, project_path: str, file_structure: Dict) -> List[Dict]:
        """Detect frontend frameworks"""
        detected = []
        for file_info in file_structure.get("all_files", []):
            if file_info["path"] == "package.json":
                file_path = Path(project_path) / file_info["path"]
                try:
                    import json

                    with open(file_path, "r", encoding="utf-8") as f:
                        package_data = json.load(f)
                        deps = package_data.get("dependencies", {})
                        dev_deps = package_data.get("devDependencies", {})
                        all_deps = {**deps, **dev_deps}

                        for framework, keywords in self.frameworks.items():
                            if any(kw in all_deps for kw in keywords):
                                detected.append(
                                    {"name": framework, "type": "Frontend", "confidence": 0.9}
                                )
                except Exception as e:
                    logger.debug(f"Error detecting frontend: {e}")
        return detected
