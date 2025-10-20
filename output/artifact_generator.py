"""
Artifact Generator
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ArtifactGenerator:
    """Generates project artifacts (code files, configs, etc.)"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.artifacts_dir = os.path.join(output_dir, "artifacts")
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def generate_agent_files(self, agents: Dict[str, Any]) -> List[str]:
        """Generate agent Python files"""
        generated_files = []

        for agent_name, agent_info in agents.items():
            if isinstance(agent_info, dict) and "code" in agent_info:
                file_path = os.path.join(self.artifacts_dir, f"{agent_name.lower()}_agent.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(agent_info["code"])

                generated_files.append(file_path)
                logger.info(f"Generated agent file: {file_path}")

        return generated_files

    def generate_skill_files(self, skills: Dict[str, Any]) -> List[str]:
        """Generate skill Python files"""
        generated_files = []

        for skill_name, skill_info in skills.items():
            if isinstance(skill_info, dict) and "code" in skill_info:
                file_path = os.path.join(self.artifacts_dir, f"{skill_name.lower()}_skill.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(skill_info["code"])

                generated_files.append(file_path)
                logger.info(f"Generated skill file: {file_path}")

        return generated_files

    def generate_workflow_files(self, workflows: Dict[str, Any]) -> List[str]:
        """Generate workflow Python files"""
        generated_files = []

        for workflow_name, workflow_info in workflows.items():
            if isinstance(workflow_info, dict) and "code" in workflow_info:
                file_path = os.path.join(self.artifacts_dir, f"{workflow_name.lower()}_workflow.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(workflow_info["code"])

                generated_files.append(file_path)
                logger.info(f"Generated workflow file: {file_path}")

        return generated_files

    def generate_test_files(self, tests: Dict[str, Any]) -> List[str]:
        """Generate test files"""
        generated_files = []

        for test_name, test_info in tests.items():
            if isinstance(test_info, dict) and "code" in test_info:
                file_path = os.path.join(self.artifacts_dir, f"test_{test_name.lower()}.py")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(test_info["code"])

                generated_files.append(file_path)
                logger.info(f"Generated test file: {file_path}")

        return generated_files

    def generate_docker_config(self, analysis_results: Dict[str, Any]) -> str:
        """Generate Docker configuration"""
        dockerfile_path = os.path.join(self.artifacts_dir, "Dockerfile.generated")

        # Determine base image based on detected languages
        languages = analysis_results.get("languages", {})
        if "Python" in languages:
            base_image = "python:3.11-slim"
        elif "Node.js" in languages or "JavaScript" in languages:
            base_image = "node:18-alpine"
        else:
            base_image = "python:3.11-slim"  # Default

        dockerfile_content = f"""# Generated Dockerfile for {analysis_results.get('project_name', 'project')}
FROM {base_image}

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
"""

        if "Python" in languages:
            dockerfile_content += """
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
"""

        if "Node.js" in languages or "JavaScript" in languages:
            dockerfile_content += """
COPY package*.json ./
RUN npm install
"""

        dockerfile_content += """
# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "app.py"]
"""

        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)

        logger.info(f"Generated Dockerfile: {dockerfile_path}")
        return dockerfile_path

    def generate_requirements_file(self, analysis_results: Dict[str, Any]) -> str:
        """Generate requirements.txt file"""
        requirements_path = os.path.join(self.artifacts_dir, "requirements.generated.txt")

        # Base requirements
        requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "python-dotenv==1.0.0",
            "pydantic==2.5.0",
            "httpx==0.25.2",
        ]

        # Add requirements based on detected frameworks
        frameworks = analysis_results.get("frameworks", {})
        if "FastAPI" in frameworks:
            requirements.append("fastapi==0.104.1")
        if "Streamlit" in frameworks:
            requirements.append("streamlit==1.29.0")
        if "Django" in frameworks:
            requirements.append("django==4.2.7")
        if "Flask" in frameworks:
            requirements.append("flask==3.0.0")

        # Add API requirements
        apis = analysis_results.get("apis", [])
        if "OpenAI API" in apis:
            requirements.append("openai==1.3.7")
        if "Google API" in apis:
            requirements.append("google-api-python-client==2.108.0")
        if "Claude API" in apis:
            requirements.append("anthropic==0.7.8")

        with open(requirements_path, "w", encoding="utf-8") as f:
            f.write("\n".join(requirements))

        logger.info(f"Generated requirements file: {requirements_path}")
        return requirements_path

    def generate_all_artifacts(
        self,
        analysis_results: Dict[str, Any],
        agents: Dict[str, Any] = None,
        skills: Dict[str, Any] = None,
        workflows: Dict[str, Any] = None,
        tests: Dict[str, Any] = None,
    ) -> Dict[str, List[str]]:
        """Generate all artifacts"""

        generated_files = {"agents": [], "skills": [], "workflows": [], "tests": [], "configs": []}

        if agents:
            generated_files["agents"] = self.generate_agent_files(agents)

        if skills:
            generated_files["skills"] = self.generate_skill_files(skills)

        if workflows:
            generated_files["workflows"] = self.generate_workflow_files(workflows)

        if tests:
            generated_files["tests"] = self.generate_test_files(tests)

        # Generate config files
        dockerfile = self.generate_docker_config(analysis_results)
        requirements = self.generate_requirements_file(analysis_results)
        generated_files["configs"] = [dockerfile, requirements]

        return generated_files
