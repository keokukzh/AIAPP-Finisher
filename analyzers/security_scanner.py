"""
Security Scanner - Scans for security vulnerabilities
"""

import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SecurityScanner:
    """Scans project for security issues"""

    async def scan_security(
        self, project_path: str, dependencies: Dict[str, Any], file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Führt einen echten Security-Scan durch"""
        security_issues = []

        try:
            # 1. Echter Safety-Scan für Python Dependencies
            safety_issues = await self._run_safety_scan(project_path)
            security_issues.extend(safety_issues)

            # 2. Hardcoded Secrets Scan
            secret_issues = await self._scan_hardcoded_secrets(project_path, file_structure)
            security_issues.extend(secret_issues)

            # 3. Code Security Issues
            code_issues = await self._scan_code_security_issues(project_path, file_structure)
            security_issues.extend(code_issues)

        except Exception as e:
            logger.error(f"Fehler beim Security-Scan: {e}")

        return security_issues

    async def _run_safety_scan(self, project_path: str) -> List[Dict[str, Any]]:
        """Führt echten Safety-Scan durch"""
        safety_issues = []

        try:
            # Prüfe ob requirements.txt existiert
            requirements_path = Path(project_path) / "requirements.txt"
            if not requirements_path.exists():
                return safety_issues

            # Führe Safety-Scan aus
            result = subprocess.run(
                ["safety", "check", "--json", "--file", str(requirements_path)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode == 0:
                logger.info("Safety-Scan: Keine Vulnerabilities gefunden")
            else:
                # Parse Safety-Output
                try:
                    safety_data = json.loads(result.stdout)
                    if isinstance(safety_data, dict):
                        for package, vulns in safety_data.items():
                            if isinstance(vulns, list):
                                for vuln in vulns:
                                    safety_issues.append(
                                        {
                                            "type": "dependency_vulnerability",
                                            "severity": "high",
                                            "package": package,
                                            "version": vuln.get("analyzed_version", "unknown"),
                                            "message": vuln.get(
                                                "advisory", "Security vulnerability found"
                                            ),
                                            "cve": vuln.get("cve", "N/A"),
                                            "source": "safety",
                                        }
                                    )
                    elif isinstance(safety_data, list):
                        for vuln in safety_data:
                            safety_issues.append(
                                {
                                    "type": "dependency_vulnerability",
                                    "severity": "high",
                                    "package": vuln.get("package_name", "unknown"),
                                    "version": vuln.get("analyzed_version", "unknown"),
                                    "message": vuln.get("advisory", "Security vulnerability found"),
                                    "cve": vuln.get("cve", "N/A"),
                                    "source": "safety",
                                }
                            )
                except json.JSONDecodeError:
                    # Fallback: Parse Text-Output
                    lines = result.stdout.split("\n")
                    for line in lines:
                        if "vulnerability" in line.lower() or "cve" in line.lower():
                            safety_issues.append(
                                {
                                    "type": "dependency_vulnerability",
                                    "severity": "high",
                                    "package": "unknown",
                                    "message": line.strip(),
                                    "source": "safety",
                                }
                            )

        except subprocess.TimeoutExpired:
            logger.warning("Safety-Scan timeout")
        except FileNotFoundError:
            logger.warning("Safety tool not found - install with: pip install safety")
        except Exception as e:
            logger.error(f"Fehler beim Safety-Scan: {e}")

        return safety_issues

    async def _scan_hardcoded_secrets(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Scannt nach hardcoded Secrets"""
        secret_issues = []

        try:
            # Erweiterte Secret-Patterns
            secret_patterns = {
                "password": r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
                "api_key": r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
                "secret": r'(?i)(secret|secret_key)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
                "token": r'(?i)(token|access_token|bearer_token)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
                "private_key": r'(?i)(private[_-]?key|privkey)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
                "database_url": r'(?i)(database[_-]?url|db[_-]?url)\s*[=:]\s*["\']?[^"\'\s]+["\']?',
            }

            for file_info in file_structure.get("all_files", []):
                if file_info["extension"].lower() in {
                    ".py",
                    ".js",
                    ".ts",
                    ".env",
                    ".json",
                    ".yaml",
                    ".yml",
                }:
                    file_path = Path(project_path) / file_info["path"]
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            lines = content.split("\n")

                            for line_num, line in enumerate(lines, 1):
                                for pattern_name, pattern in secret_patterns.items():
                                    if re.search(pattern, line):
                                        secret_issues.append(
                                            {
                                                "type": "hardcoded_secret",
                                                "severity": "high",
                                                "file": file_info["path"],
                                                "line": line_num,
                                                "message": f"Potentieller hardcoded {pattern_name} gefunden",
                                                "pattern": pattern_name,
                                                "source": "regex_scan",
                                            }
                                        )
                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler beim Secret-Scan: {e}")

        return secret_issues

    async def _scan_code_security_issues(
        self, project_path: str, file_structure: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Scannt nach Code-Security-Issues"""
        code_issues = []

        try:
            # Gefährliche Funktionen und Patterns
            dangerous_patterns = {
                "eval": r"eval\s*\(",
                "exec": r"exec\s*\(",
                "subprocess": r"subprocess\.(call|run|Popen)",
                "os.system": r"os\.system\s*\(",
                "shell": r"shell\s*=\s*True",
                "pickle": r"pickle\.(loads?|dumps?)",
                "yaml.load": r"yaml\.load\s*\(",
                "sql_injection": r'execute\s*\(\s*["\'].*%s.*["\']',
                "xss": r"innerHTML\s*=",
                "crypto_weak": r"MD5|SHA1\s*\(",
            }

            for file_info in file_structure.get("all_files", []):
                if file_info["extension"].lower() in {".py", ".js", ".ts", ".php", ".java"}:
                    file_path = Path(project_path) / file_info["path"]
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            lines = content.split("\n")

                            for line_num, line in enumerate(lines, 1):
                                for issue_type, pattern in dangerous_patterns.items():
                                    if re.search(pattern, line, re.IGNORECASE):
                                        severity = (
                                            "high"
                                            if issue_type in ["eval", "exec", "pickle"]
                                            else "medium"
                                        )
                                        code_issues.append(
                                            {
                                                "type": "code_security_issue",
                                                "severity": severity,
                                                "file": file_info["path"],
                                                "line": line_num,
                                                "message": f"Potentielles Security-Risiko: {issue_type}",
                                                "issue_type": issue_type,
                                                "source": "code_scan",
                                            }
                                        )
                    except Exception:
                        continue

        except Exception as e:
            logger.error(f"Fehler beim Code-Security-Scan: {e}")

        return code_issues
