"""
Skill Templates - Enthält alle Skill-Templates für die automatische Generierung
"""


def get_code_analysis_skill_template():
    """Template für Code-Analysis-Skill"""
    return '''"""
{skill_class} - Automatisch generierter Code-Analysis-Skill
"""

import ast
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class {skill_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.skill_type = "code_analysis"
    
    async def execute(self, file_path: str, analysis_options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Führt Code-Analyse aus"""
        logger.info(f"🔍 Starting code analysis for {{file_path}}")
        
        if analysis_options is None:
            analysis_options = {{}}
        
        results = {{
            "file_path": file_path,
            "analysis_type": "code_analysis",
            "complexity_metrics": {{}},
            "quality_issues": [],
            "suggestions": []
        }}
        
        try:
            file_path_obj = Path(file_path)
            
            if file_path_obj.suffix == '.py':
                results = await self._analyze_python_file(file_path_obj, analysis_options)
            elif file_path_obj.suffix in ['.js', '.ts']:
                results = await self._analyze_js_file(file_path_obj, analysis_options)
            else:
                results["error"] = f"Unsupported file type: {{file_path_obj.suffix}}"
            
            logger.info(f"✅ Code analysis completed for {{file_path}}")
            
        except Exception as e:
            logger.error(f"❌ Error in code analysis: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _analyze_python_file(self, file_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Analysiert eine Python-Datei"""
        results = {{
            "file_path": str(file_path),
            "analysis_type": "python_code_analysis",
            "complexity_metrics": {{}},
            "quality_issues": [],
            "suggestions": []
        }}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Analysiere Komplexität
            complexity = self._calculate_complexity(tree)
            results["complexity_metrics"] = complexity
            
            # Finde Quality-Issues
            issues = self._find_quality_issues(tree, content)
            results["quality_issues"] = issues
            
            # Generiere Vorschläge
            suggestions = self._generate_suggestions(tree, content, complexity)
            results["suggestions"] = suggestions
            
        except Exception as e:
            logger.error(f"❌ Error analyzing Python file {{file_path}}: {{e}}")
            results["error"] = str(e)
        
        return results
    
    def _calculate_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """Berechnet Komplexitäts-Metriken für Python"""
        complexity = {{
            "cyclomatic_complexity": 0,
            "function_count": 0,
            "class_count": 0,
            "line_count": 0
        }}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity["function_count"] += 1
                # Einfache Cyclomatic Complexity
                complexity["cyclomatic_complexity"] += len([n for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While, ast.ExceptHandler))])
            elif isinstance(node, ast.ClassDef):
                complexity["class_count"] += 1
            elif isinstance(node, ast.stmt):
                complexity["line_count"] += 1
        
        return complexity
    
    def _find_quality_issues(self, tree: ast.AST, content: str) -> List[Dict[str, str]]:
        """Findet Quality-Issues in Python-Code"""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Prüfe auf lange Funktionen
                if len(node.body) > 20:
                    issues.append({{
                        "type": "long_function",
                        "message": f"Function {{node.name}} is too long ({{len(node.body)}} statements)",
                        "severity": "warning"
                    }})
                
                # Prüfe auf viele Parameter
                if len(node.args.args) > 5:
                    issues.append({{
                        "type": "too_many_parameters",
                        "message": f"Function {{node.name}} has too many parameters ({{len(node.args.args)}})",
                        "severity": "warning"
                    }})
        
        # Prüfe auf Code-Smells
        if 'eval(' in content:
            issues.append({{
                "type": "code_smell",
                "message": "Use of eval() is dangerous",
                "severity": "error"
            }})
        
        return issues
    
    def _generate_suggestions(self, tree: ast.AST, content: str, complexity: Dict[str, int]) -> List[str]:
        """Generiert Verbesserungsvorschläge für Python-Code"""
        suggestions = []
        
        if complexity["cyclomatic_complexity"] > 10:
            suggestions.append("Consider breaking down complex functions into smaller ones")
        
        if complexity["function_count"] > 20:
            suggestions.append("Consider splitting this file into multiple modules")
        
        if 'import *' in content:
            suggestions.append("Avoid wildcard imports, use specific imports instead")
        
        return suggestions
    
    # Generierte Implementation vom LLM
    {generated_implementation}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {skill_class}")
'''


def get_performance_optimization_skill_template():
    """Template für Performance-Optimization-Skill"""
    return '''"""
{skill_class} - Automatisch generierter Performance-Optimization-Skill
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import psutil

logger = logging.getLogger(__name__)


class {skill_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.skill_type = "performance_optimization"
    
    async def execute(self, code_files: List[str], performance_metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        """Führt Performance-Optimierung aus"""
        logger.info(f"⚡ Starting performance optimization for {{len(code_files)}} files")
        
        if performance_metrics is None:
            performance_metrics = {{}}
        
        results = {{
            "optimization_type": "performance",
            "files_optimized": 0,
            "performance_improvements": [],
            "optimized_code": {{}},
            "metrics_before": {{}},
            "metrics_after": {{}}
        }}
        
        try:
            # Messe Performance vor Optimierung
            results["metrics_before"] = await self._measure_performance()
            
            # Optimiere jede Datei
            for file_path in code_files:
                optimized_code = await self._optimize_file(file_path)
                if optimized_code:
                    results["optimized_code"][file_path] = optimized_code
                    results["files_optimized"] += 1
            
            # Messe Performance nach Optimierung
            results["metrics_after"] = await self._measure_performance()
            
            # Berechne Verbesserungen
            results["performance_improvements"] = self._calculate_improvements(
                results["metrics_before"], 
                results["metrics_after"]
            )
            
            logger.info(f"✅ Performance optimization completed: {{results['files_optimized']}} files optimized")
            
        except Exception as e:
            logger.error(f"❌ Error in performance optimization: {{e}}")
            results["error"] = str(e)
        
        return results
    
    async def _measure_performance(self) -> Dict[str, float]:
        """Misst aktuelle Performance-Metriken"""
        metrics = {{
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "timestamp": time.time()
        }}
        
        return metrics
    
    async def _optimize_file(self, file_path: str) -> Optional[str]:
        """Optimiert eine einzelne Datei"""
        try:
            file_path_obj = Path(file_path)
            
            if not file_path_obj.exists():
                logger.warning(f"⚠️ File not found: {{file_path}}")
                return None
            
            with open(file_path_obj, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Führe Optimierungen durch
            optimized_content = await self._apply_optimizations(content, file_path_obj.suffix)
            
            return optimized_content
            
        except Exception as e:
            logger.error(f"❌ Error optimizing file {{file_path}}: {{e}}")
            return None
    
    async def _apply_optimizations(self, content: str, file_extension: str) -> str:
        """Wendet Performance-Optimierungen an"""
        optimized_content = content
        
        if file_extension == '.py':
            optimized_content = await self._optimize_python_code(content)
        elif file_extension in ['.js', '.ts']:
            optimized_content = await self._optimize_js_code(content)
        
        return optimized_content
    
    async def _optimize_python_code(self, content: str) -> str:
        """Optimiert Python-Code"""
        optimized = content
        
        # Einfache Optimierungen
        if 'for i in range(len(' in optimized:
            optimized = optimized.replace('for i in range(len(', 'for i, _ in enumerate(')
        
        if 'list(' in optimized and 'map(' in optimized:
            # Ersetze list(map(...)) mit List Comprehension wo möglich
            pass
        
        return optimized
    
    async def _optimize_js_code(self, content: str) -> str:
        """Optimiert JavaScript-Code"""
        optimized = content
        
        # Einfache Optimierungen
        if 'var ' in optimized:
            optimized = optimized.replace('var ', 'let ')
        
        if 'function(' in optimized:
            # Ersetze function() mit Arrow Functions wo möglich
            pass
        
        return optimized
    
    def _calculate_improvements(self, before: Dict[str, float], after: Dict[str, float]) -> List[Dict[str, Any]]:
        """Berechnet Performance-Verbesserungen"""
        improvements = []
        
        for metric in ['cpu_usage', 'memory_usage', 'disk_usage']:
            if metric in before and metric in after:
                improvement = before[metric] - after[metric]
                improvements.append({{
                    "metric": metric,
                    "improvement": improvement,
                    "improvement_percentage": (improvement / before[metric]) * 100 if before[metric] > 0 else 0
                }})
        
        return improvements
    
    # Generierte Implementation vom LLM
    {generated_implementation}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {skill_class}")
'''


def get_generic_skill_template():
    """Template für generischen Skill"""
    return '''"""
{skill_class} - Automatisch generierter Skill
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class {skill_class}:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = "{project_name}"
        self.skill_type = "generic"
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Führt den Skill aus"""
        logger.info(f"🔧 Starting {{self.skill_type}} skill execution")
        
        results = {{
            "skill_type": self.skill_type,
            "execution_successful": True,
            "output": "Skill executed successfully"
        }}
        
        try:
            # Generische Skill-Logik
            logger.info("🔧 Executing skill logic...")
            
            # Simuliere Skill-Ausführung
            await asyncio.sleep(0.1)
            
            logger.info(f"✅ {{self.skill_type}} skill completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Error in {{self.skill_type}} skill: {{e}}")
            results["error"] = str(e)
            results["execution_successful"] = False
        
        return results
    
    # Generierte Implementation vom LLM
    {generated_implementation}
    
    async def cleanup(self):
        """Bereinigt Ressourcen"""
        logger.info(f"🧹 Cleaning up {skill_class}")
'''
