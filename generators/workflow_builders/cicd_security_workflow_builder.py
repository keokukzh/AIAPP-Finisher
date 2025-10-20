"""
CI/CD & Security Workflow Builder - Builds CI/CD and security workflows
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class CICDSecurityWorkflowBuilder:
    """Builds CI/CD and security workflow templates"""

    def get_cicd_template(self) -> str:
        """Returns the CI/CD workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter CI/CD-Workflow
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "ci_cd"
        self.ci_platforms = self._detect_ci_platforms()
    
    def _detect_ci_platforms(self) -> List[str]:
        """Erkennt verfügbare CI-Platforms"""
        platforms = []
        
        if (self.project_path / ".github/workflows").exists():
            platforms.append('github_actions')
        
        if (self.project_path / ".gitlab-ci.yml").exists():
            platforms.append('gitlab_ci')
        
        if (self.project_path / ".circleci").exists():
            platforms.append('circleci')
        
        return platforms
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den CI/CD-Workflow aus"""
        logger.info(f"🔄 Starting CI/CD workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "ci_cd",
            "ci_platforms_detected": self.ci_platforms,
            "workflows_generated": [],
            "execution_time": 0
        }}
        
        try:
            for platform in self.ci_platforms:
                config_results = await self._generate_ci_config(platform)
                results["workflows_generated"].extend(config_results)
            
            logger.info(f"✅ CI/CD workflow completed: {{len(results['workflows_generated'])}} configs generated")
            
        except Exception as e:
            logger.error(f"❌ Error in CI/CD workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _generate_ci_config(self, platform: str) -> List[str]:
        """Generiert CI-Config für eine spezifische Platform"""
        logger.info(f"🔧 Generating {{platform}} config...")
        
        generated_configs = []
        
        try:
            if platform == 'github_actions':
                config_path = await self._create_github_actions_workflow()
                if config_path:
                    generated_configs.append(config_path)
            
            elif platform == 'gitlab_ci':
                config_path = await self._create_gitlab_ci_config()
                if config_path:
                    generated_configs.append(config_path)
        
        except Exception as e:
            logger.error(f"❌ Error generating {{platform}} config: {{e}}")
        
        return generated_configs
    
    async def _create_github_actions_workflow(self) -> Optional[str]:
        """Erstellt GitHub Actions Workflow"""
        try:
            workflow_dir = self.project_path / ".github" / "workflows"
            workflow_dir.mkdir(parents=True, exist_ok=True)
            
            workflow_file = workflow_dir / "ci.yml"
            
            workflow_content = {{
                "name": "CI/CD Pipeline",
                "on": ["push", "pull_request"],
                "jobs": {{
                    "test": {{
                        "runs-on": "ubuntu-latest",
                        "steps": [
                            {{"uses": "actions/checkout@v3"}},
                            {{"name": "Set up Python", "uses": "actions/setup-python@v4", "with": {{"python-version": "3.11"}}}},
                            {{"name": "Install dependencies", "run": "pip install -r requirements.txt"}},
                            {{"name": "Run tests", "run": "pytest"}},
                            {{"name": "Build", "run": "python setup.py build"}}
                        ]
                    }}
                }}
            }}
            
            with open(workflow_file, 'w') as f:
                yaml.dump(workflow_content, f, default_flow_style=False)
            
            return str(workflow_file)
        
        except Exception as e:
            logger.error(f"❌ Error creating GitHub Actions workflow: {{e}}")
            return None
    
    async def _create_gitlab_ci_config(self) -> Optional[str]:
        """Erstellt GitLab CI Config"""
        try:
            config_file = self.project_path / ".gitlab-ci.yml"
            
            config_content = {{
                "stages": ["test", "build", "deploy"],
                "test": {{
                    "stage": "test",
                    "image": "python:3.11",
                    "script": [
                        "pip install -r requirements.txt",
                        "pytest"
                    ]
                }},
                "build": {{
                    "stage": "build",
                    "image": "python:3.11",
                    "script": [
                        "python setup.py build"
                    ]
                }}
            }}
            
            with open(config_file, 'w') as f:
                yaml.dump(config_content, f, default_flow_style=False)
            
            return str(config_file)
        
        except Exception as e:
            logger.error(f"❌ Error creating GitLab CI config: {{e}}")
            return None
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''

    def get_security_template(self) -> str:
        """Returns the security workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Security-Workflow
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "security"
        self.security_tools = self._detect_security_tools()
    
    def _detect_security_tools(self) -> List[str]:
        """Erkennt verfügbare Security-Tools"""
        tools = []
        
        # Python Security Tools
        if (self.project_path / "requirements.txt").exists():
            with open(self.project_path / "requirements.txt", 'r') as f:
                content = f.read()
                if 'safety' in content:
                    tools.append('safety')
                if 'bandit' in content:
                    tools.append('bandit')
        
        # Node.js Security Tools
        if (self.project_path / "package.json").exists():
            tools.append('npm_audit')
        
        return tools
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Security-Workflow aus"""
        logger.info(f"🔒 Starting security workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "security",
            "security_tools_detected": self.security_tools,
            "vulnerabilities_found": 0,
            "security_issues": [],
            "execution_time": 0
        }}
        
        try:
            for tool in self.security_tools:
                tool_results = await self._run_security_tool(tool)
                results.update(tool_results)
            
            logger.info(f"✅ Security workflow completed: {{results['vulnerabilities_found']}} vulnerabilities found")
            
        except Exception as e:
            logger.error(f"❌ Error in security workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _run_security_tool(self, tool: str) -> Dict[str, Any]:
        """Führt Security-Scan für ein spezifisches Tool aus"""
        logger.info(f"🔧 Running {{tool}} security scan...")
        
        results = {{"vulnerabilities_found": 0, "security_issues": []}}
        
        try:
            if tool == 'safety':
                result = subprocess.run(
                    ["safety", "check", "-r", "requirements.txt"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode != 0:
                    results["vulnerabilities_found"] += 1
                    results["security_issues"].append(f"Safety check failed: {{result.stdout}}")
            
            elif tool == 'npm_audit':
                result = subprocess.run(
                    ["npm", "audit"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if "found 0 vulnerabilities" not in result.stdout:
                    results["vulnerabilities_found"] += 1
                    results["security_issues"].append(f"NPM audit found issues: {{result.stdout}}")
        
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {{tool}} security scan timed out")
        except Exception as e:
            logger.error(f"❌ Error running {{tool}} security scan: {{e}}")
        
        return results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''
