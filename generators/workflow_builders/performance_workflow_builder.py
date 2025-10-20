"""
Performance & Generic Workflow Builder - Builds performance and generic workflows
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PerformanceWorkflowBuilder:
    """Builds performance and generic workflow templates"""

    def get_performance_template(self) -> str:
        """Returns the performance workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Performance-Workflow
"""

import asyncio
import logging
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "performance"
        self.performance_tools = self._detect_performance_tools()
    
    def _detect_performance_tools(self) -> List[str]:
        """Erkennt verfügbare Performance-Tools"""
        tools = []
        
        # Python Performance Tools
        if (self.project_path / "requirements.txt").exists():
            with open(self.project_path / "requirements.txt", 'r') as f:
                content = f.read()
                if 'pytest-benchmark' in content:
                    tools.append('pytest_benchmark')
                if 'memory_profiler' in content:
                    tools.append('memory_profiler')
        
        # Node.js Performance Tools
        if (self.project_path / "package.json").exists():
            tools.append('node_performance')
        
        return tools
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Performance-Workflow aus"""
        logger.info(f"⚡ Starting performance workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "performance",
            "performance_tools_detected": self.performance_tools,
            "performance_metrics": {{}},
            "bottlenecks_found": [],
            "execution_time": 0
        }}
        
        try:
            for tool in self.performance_tools:
                tool_results = await self._run_performance_tool(tool)
                results.update(tool_results)
            
            logger.info(f"✅ Performance workflow completed: {{len(results['bottlenecks_found'])}} bottlenecks found")
            
        except Exception as e:
            logger.error(f"❌ Error in performance workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _run_performance_tool(self, tool: str) -> Dict[str, Any]:
        """Führt Performance-Test für ein spezifisches Tool aus"""
        logger.info(f"🔧 Running {{tool}} performance test...")
        
        results = {{"performance_metrics": {{}}, "bottlenecks_found": []}}
        
        try:
            if tool == 'pytest_benchmark':
                result = subprocess.run(
                    ["python", "-m", "pytest", "--benchmark-only"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    results["performance_metrics"]["benchmark_results"] = result.stdout
            
            elif tool == 'node_performance':
                start_time = time.time()
                result = subprocess.run(
                    ["node", "--version"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                end_time = time.time()
                results["performance_metrics"]["node_startup_time"] = end_time - start_time
        
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {{tool}} performance test timed out")
        except Exception as e:
            logger.error(f"❌ Error running {{tool}} performance test: {{e}}")
        
        return results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''

    def get_generic_template(self) -> str:
        """Returns the generic workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Workflow
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class {workflow_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.workflow_type = "generic"
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Workflow aus"""
        logger.info(f"🔄 Starting generic workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "generic",
            "execution_successful": True,
            "execution_time": 0
        }}
        
        try:
            logger.info("🔧 Executing generic workflow steps...")
            
            await asyncio.sleep(1)
            
            logger.info(f"✅ Generic workflow completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error in generic workflow: {{e}}")
            results["error"] = str(e)
            results["execution_successful"] = False
        
        return results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''
