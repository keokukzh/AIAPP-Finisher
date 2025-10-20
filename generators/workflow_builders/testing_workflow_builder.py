"""
Testing Workflow Builder - Builds testing workflows
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class TestingWorkflowBuilder:
    """Builds testing workflow templates and logic"""

    def get_template(self) -> str:
        """Returns the testing workflow template"""
        return '''"""
{workflow_class} - Automatisch generierter Testing-Workflow
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
        self.workflow_type = "testing"
        self.test_frameworks = self._detect_test_frameworks()
    
    def _detect_test_frameworks(self) -> List[str]:
        """Erkennt verfügbare Test-Frameworks"""
        frameworks = []
        
        # Python
        if (self.project_path / "requirements.txt").exists():
            with open(self.project_path / "requirements.txt", 'r') as f:
                content = f.read()
                if 'pytest' in content:
                    frameworks.append('pytest')
                if 'unittest' in content:
                    frameworks.append('unittest')
        
        # Node.js
        if (self.project_path / "package.json").exists():
            with open(self.project_path / "package.json", 'r') as f:
                package_data = json.load(f)
                deps = package_data.get('dependencies', {{}}) | package_data.get('devDependencies', {{}})
                if 'jest' in deps:
                    frameworks.append('jest')
                if 'mocha' in deps:
                    frameworks.append('mocha')
                if 'vitest' in deps:
                    frameworks.append('vitest')
        
        return frameworks
    
    async def execute(self) -> Dict[str, Any]:
        """Führt den Testing-Workflow aus"""
        logger.info(f"🧪 Starting testing workflow for {{self.project_name}}")
        
        results = {{
            "workflow_type": "testing",
            "frameworks_detected": self.test_frameworks,
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "coverage_percentage": 0,
            "execution_time": 0
        }}
        
        try:
            # Führe Tests für jedes erkannte Framework aus
            for framework in self.test_frameworks:
                framework_results = await self._run_framework_tests(framework)
                results.update(framework_results)
            
            # Generiere Coverage-Report
            coverage_results = await self._generate_coverage_report()
            results.update(coverage_results)
            
            logger.info(f"✅ Testing workflow completed: {{results['tests_passed']}} passed, {{results['tests_failed']}} failed")
            
        except Exception as e:
            logger.error(f"❌ Error in testing workflow: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _run_framework_tests(self, framework: str) -> Dict[str, Any]:
        """Führt Tests für ein spezifisches Framework aus"""
        logger.info(f"🔧 Running {{framework}} tests...")
        
        results = {{"tests_run": 0, "tests_passed": 0, "tests_failed": 0}}
        
        try:
            if framework == 'pytest':
                result = subprocess.run(
                    ["python", "-m", "pytest", "-v", "--tb=short"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                results["tests_run"] = self._parse_pytest_output(result.stdout)
                results["tests_passed"] = result.returncode == 0
                
            elif framework == 'jest':
                result = subprocess.run(
                    ["npm", "test"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                results["tests_run"] = self._parse_jest_output(result.stdout)
                results["tests_passed"] = result.returncode == 0
                
            elif framework == 'mocha':
                result = subprocess.run(
                    ["npm", "test"],
                    cwd=self.project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                results["tests_run"] = self._parse_mocha_output(result.stdout)
                results["tests_passed"] = result.returncode == 0
        
        except subprocess.TimeoutExpired:
            logger.warning(f"⚠️ {{framework}} tests timed out")
            results["error"] = "Tests timed out"
        except Exception as e:
            logger.error(f"❌ Error running {{framework}} tests: {{e}}")
            results["error"] = str(e)
        
        return results
    
    def _parse_pytest_output(self, output: str) -> int:
        """Parst pytest Output"""
        lines = output.split('\\n')
        for line in lines:
            if 'passed' in line and 'failed' in line:
                import re
                match = re.search(r'(\\d+) passed', line)
                if match:
                    return int(match.group(1))
        return 0
    
    def _parse_jest_output(self, output: str) -> int:
        """Parst Jest Output"""
        lines = output.split('\\n')
        for line in lines:
            if 'Tests:' in line:
                import re
                match = re.search(r'(\\d+) passed', line)
                if match:
                    return int(match.group(1))
        return 0
    
    def _parse_mocha_output(self, output: str) -> int:
        """Parst Mocha Output"""
        lines = output.split('\\n')
        for line in lines:
            if 'passing' in line:
                import re
                match = re.search(r'(\\d+) passing', line)
                if match:
                    return int(match.group(1))
        return 0
    
    async def _generate_coverage_report(self) -> Dict[str, Any]:
        """Generiert Coverage-Report"""
        logger.info("📊 Generating coverage report...")
        
        coverage_results = {{"coverage_percentage": 0, "coverage_details": {{}}}}
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "--cov=.", "--cov-report=json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                coverage_file = self.project_path / "coverage.json"
                if coverage_file.exists():
                    with open(coverage_file, 'r') as f:
                        coverage_data = json.load(f)
                        coverage_results["coverage_percentage"] = coverage_data.get("totals", {{}}).get("percent_covered", 0)
        
        except Exception as e:
            logger.warning(f"⚠️ Could not generate coverage report: {{e}}")
        
        return coverage_results
    
    # Generierte Workflow-Schritte vom LLM
    {generated_steps}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {workflow_class}")
'''
