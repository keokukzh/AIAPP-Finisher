"""
Build & Deployment Workflow Builder - Builds build and deployment workflows
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class BuildDeploymentWorkflowBuilder:
    """Builds build and deployment workflow templates"""

    def get_build_template(self) -> str:
        """Returns the build workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Build-Workflow
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "build"
        self.build_tools = self._detect_build_tools()
    
    def _detect_build_tools(self) -> List[str]:
        """Erkennt verfügbare Build-Tools"""
        tools = []
        
        # Node.js Build-Tools
        if (self.project_path / "package.json").exists():
            with open(self.project_path / "package.json", 'r') as f:
                package_data = json.load(f)
                deps = package_data.get('dependencies', {{}}) | package_data.get('devDependencies', {{}})
                
                if 'webpack' in deps:
                    tools.append('webpack')
                if 'vite' in deps:
                    tools.append('vite')
                if 'rollup' in deps:
                    tools.append('rollup')
                if 'parcel' in deps:
                    tools.append('parcel')
        
        # Python Build-Tools
        if (self.project_path / "setup.py").exists():
            tools.append('setuptools')
        if (self.project_path / "pyproject.toml").exists():
            tools.append('poetry')
        
        return tools
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Build-Workflow aus"""
        logger.info(f"🔨 Starting build workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "build",
            "build_tools_detected": self.build_tools,
            "build_successful": False,
            "build_output": "",
            "bundle_size": 0,
            "execution_time": 0
        }}
        
        try:
            for tool in self.build_tools:
                tool_results = await self._run_build_tool(tool)
                results.update(tool_results)
            
            bundle_analysis = await self._analyze_bundle_size()
            results.update(bundle_analysis)
            
            logger.info(f"✅ Build workflow completed: {{'successful' if results['build_successful'] else 'failed'}}")
            
        except Exception as e:
            logger.error(f"❌ Error in build workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _run_build_tool(self, tool: str) -> Dict[str, Any]:
        """Führt Build für ein spezifisches Tool aus"""
        logger.info(f"🔧 Running {{tool}} build...")
        
        results = {{"build_successful": False, "build_output": ""}}
        
        try:
            if tool == 'webpack':
                result = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results["build_output"] = result.stdout + result.stderr
                results["build_successful"] = result.returncode == 0
                
            elif tool == 'vite':
                result = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results["build_output"] = result.stdout + result.stderr
                results["build_successful"] = result.returncode == 0
                
            elif tool == 'setuptools':
                result = subprocess.run(
                    ["python", "setup.py", "build"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results["build_output"] = result.stdout + result.stderr
                results["build_successful"] = result.returncode == 0
        
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {{tool}} build timed out")
            results["error"] = "Build timed out"
        except Exception as e:
            logger.error(f"❌ Error running {{tool}} build: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _analyze_bundle_size(self) -> Dict[str, Any]:
        """Analysiert Bundle-Größe"""
        logger.info("📦 Analyzing bundle size...")
        
        bundle_results = {{"bundle_size": 0, "bundle_files": []}}
        
        try:
            build_dirs = ['dist', 'build', 'out', 'public']
            
            for build_dir in build_dirs:
                build_path = self.project_path / build_dir
                if build_path.exists():
                    total_size = 0
                    files = []
                    
                    for file_path in build_path.rglob("*"):
                        if file_path.is_file():
                            file_size = file_path.stat().st_size
                            total_size += file_size
                            files.append({{
                                "name": str(file_path.relative_to(build_path)),
                                "size": file_size
                            }})
                    
                    bundle_results["bundle_size"] = total_size
                    bundle_results["bundle_files"] = files
                    break
        
        except Exception as e:
            logger.warning(f"⚠️ Could not analyze bundle size: {{e}}")
        
        return bundle_results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''

    def get_deployment_template(self) -> str:
        """Returns the deployment workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Deployment-Workflow
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "deployment"
        self.deployment_configs = self._detect_deployment_configs()
    
    def _detect_deployment_configs(self) -> List[str]:
        """Erkennt verfügbare Deployment-Configs"""
        configs = []
        
        if (self.project_path / "Dockerfile").exists():
            configs.append('docker')
        
        if (self.project_path / "docker-compose.yml").exists():
            configs.append('docker-compose')
        
        if any((self.project_path / "k8s").exists(), (self.project_path / "kubernetes").exists()):
            configs.append('kubernetes')
        
        return configs
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Deployment-Workflow aus"""
        logger.info(f"🚀 Starting deployment workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "deployment",
            "deployment_configs_detected": self.deployment_configs,
            "deployment_successful": False,
            "deployment_output": "",
            "deployment_url": "",
            "execution_time": 0
        }}
        
        try:
            for config in self.deployment_configs:
                config_results = await self._run_deployment_config(config)
                results.update(config_results)
            
            logger.info(f"✅ Deployment workflow completed: {{'successful' if results['deployment_successful'] else 'failed'}}")
            
        except Exception as e:
            logger.error(f"❌ Error in deployment workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _run_deployment_config(self, config: str) -> Dict[str, Any]:
        """Führt Deployment für eine spezifische Config aus"""
        logger.info(f"🔧 Running {{config}} deployment...")
        
        results = {{"deployment_successful": False, "deployment_output": ""}}
        
        try:
            if config == 'docker':
                build_result = subprocess.run(
                    ["docker", "build", "-t", f"{{self.project_name}}:latest", "."],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results["deployment_output"] = build_result.stdout + build_result.stderr
                results["deployment_successful"] = build_result.returncode == 0
                
            elif config == 'docker-compose':
                compose_result = subprocess.run(
                    ["docker-compose", "up", "-d"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results["deployment_output"] = compose_result.stdout + compose_result.stderr
                results["deployment_successful"] = compose_result.returncode == 0
        
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {{config}} deployment timed out")
            results["error"] = "Deployment timed out"
        except Exception as e:
            logger.error(f"❌ Error running {{config}} deployment: {{e}}")
            results["error"] = str(e)
        
        return results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''
