"""
Security Scan Manager - Coordinates security scanning
Implements Manager pattern for security analysis
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SecurityScanManager:
    """Manages and coordinates security scanning using composition"""

    def __init__(self, security_scanner):
        # Composition over inheritance - inject dependency
        self.security_scanner = security_scanner

        self.scan_cache = {}
        self.scan_history = []

    async def perform_full_scan(
        self,
        project_path: str,
        file_structure: Dict[str, Any],
        dependencies: Dict[str, Any],
        progress_callback=None,
    ) -> Dict[str, Any]:
        """Coordinate complete security scan"""
        results = {
            "vulnerabilities": [],
            "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "dependency_issues": [],
            "code_issues": [],
            "total_issues": 0,
            "security_score": 100,
        }

        try:
            if progress_callback:
                progress_callback("Performing security scan", 0.0)

            # Perform scan using scanner
            scan_results = await self.security_scanner.scan_project(
                project_path, file_structure, dependencies
            )

            results["vulnerabilities"] = scan_results.get("vulnerabilities", [])
            results["dependency_issues"] = scan_results.get("dependency_issues", [])
            results["code_issues"] = scan_results.get("code_issues", [])

            # Calculate severity breakdown
            for vuln in results["vulnerabilities"]:
                severity = vuln.get("severity", "low").lower()
                if severity in results["severity_breakdown"]:
                    results["severity_breakdown"][severity] += 1

            results["total_issues"] = len(results["vulnerabilities"])

            # Calculate security score (100 - (issues * weight))
            score = 100
            score -= results["severity_breakdown"]["critical"] * 20
            score -= results["severity_breakdown"]["high"] * 10
            score -= results["severity_breakdown"]["medium"] * 5
            score -= results["severity_breakdown"]["low"] * 2
            results["security_score"] = max(0, score)

            # Record in history
            self.scan_history.append(
                {
                    "project_path": project_path,
                    "total_issues": results["total_issues"],
                    "security_score": results["security_score"],
                }
            )

            if progress_callback:
                progress_callback("Security scan complete", 1.0)

            logger.info(
                f"Security scan complete: {results['total_issues']} issues found, "
                f"score: {results['security_score']}/100"
            )

        except Exception as e:
            logger.error(f"Error in security scan: {e}")
            raise

        return results

    def get_cached_scan(self, project_path: str) -> Dict[str, Any]:
        """Get cached scan results"""
        return self.scan_cache.get(project_path)

    def cache_scan(self, project_path: str, results: Dict[str, Any]):
        """Cache scan results"""
        self.scan_cache[project_path] = results

    def get_scan_history(self) -> List[Dict[str, Any]]:
        """Get scan history"""
        return self.scan_history
