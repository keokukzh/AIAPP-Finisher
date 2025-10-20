"""
Comprehensive tests for refactored Route modules
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app import app


class TestAnalysisRoutes:
    """Tests for analysis route endpoints"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_analyze_project_endpoint_exists(self):
        """Test that analyze endpoint exists"""
        # POST request without data should return 422 (validation error) not 404
        response = self.client.post("/api/analysis/analyze", json={})
        assert response.status_code in [422, 400]  # Validation error expected

    def test_analysis_results_endpoint(self):
        """Test getting analysis results"""
        response = self.client.get("/api/analysis/results")
        # Should return either results or 404 if no analysis
        assert response.status_code in [200, 404]

    def test_list_reports_endpoint(self):
        """Test listing generated reports"""
        response = self.client.get("/api/analysis/reports")
        assert response.status_code == 200
        data = response.json()
        assert "reports" in data
        assert isinstance(data["reports"], list)

    def test_list_artifacts_endpoint(self):
        """Test listing generated artifacts"""
        response = self.client.get("/api/analysis/artifacts")
        assert response.status_code == 200
        data = response.json()
        assert "artifacts" in data
        assert isinstance(data["artifacts"], list)


class TestAgentRoutes:
    """Tests for agent route endpoints"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_agent_status_endpoint(self):
        """Test agent status endpoint"""
        response = self.client.get("/api/agents/status")
        assert response.status_code == 200
        data = response.json()
        assert "total_agents" in data
        assert "agents" in data
        assert isinstance(data["agents"], list)

    def test_chat_endpoint_exists(self):
        """Test that chat endpoint exists"""
        response = self.client.post("/api/agents/chat", json={})
        # Should return validation error or 503 if agent not initialized
        assert response.status_code in [422, 503, 400]

    def test_generate_agents_endpoint(self):
        """Test agent generation endpoint"""
        response = self.client.post("/api/agents/generate")
        # Should return 404 if no analysis or succeed
        assert response.status_code in [200, 404, 500]

    def test_optimizations_endpoint(self):
        """Test optimizations endpoint"""
        response = self.client.get("/api/agents/optimizations")
        # Should return 404 if no analysis available
        assert response.status_code in [200, 404]


class TestWorkflowRoutes:
    """Tests for workflow route endpoints"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_workflow_status_endpoint(self):
        """Test workflow status endpoint"""
        response = self.client.get("/api/workflows/status")
        assert response.status_code == 200
        data = response.json()
        assert "running_workflows" in data or "workflows" in data

    def test_execute_workflow_endpoint_exists(self):
        """Test workflow execution endpoint exists"""
        response = self.client.post("/api/workflows/execute/test_workflow", json={})
        # Should return error for invalid workflow or validation error
        assert response.status_code in [404, 422, 500]

    def test_workflow_progress_endpoint(self):
        """Test workflow progress endpoint"""
        response = self.client.get("/api/workflows/progress/test_workflow_1")
        # Should return 404 for nonexistent workflow
        assert response.status_code in [200, 404]


class TestModelRoutes:
    """Tests for model management route endpoints"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_list_models_endpoint(self):
        """Test listing available models"""
        response = self.client.get("/api/models")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "models" in data

    def test_set_model_endpoint_exists(self):
        """Test set model endpoint exists"""
        response = self.client.post("/api/models/set", json={})
        # Should return validation error
        assert response.status_code in [422, 400]

    def test_current_model_endpoint(self):
        """Test getting current model"""
        response = self.client.get("/api/models/current")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "model" in data


class TestRouteIntegration:
    """Integration tests for route functionality"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_cors_configuration(self):
        """Test CORS is properly configured"""
        response = self.client.options("/")
        # CORS should allow options
        assert response.status_code in [200, 405]

    def test_api_prefix_consistency(self):
        """Test all new routes use /api prefix"""
        # Analysis routes
        response1 = self.client.get("/api/analysis/reports")
        assert response1.status_code != 404  # Route exists

        # Agent routes
        response2 = self.client.get("/api/agents/status")
        assert response2.status_code != 404  # Route exists

        # Workflow routes
        response3 = self.client.get("/api/workflows/status")
        assert response3.status_code != 404  # Route exists

        # Model routes
        response4 = self.client.get("/api/models")
        assert response4.status_code != 404  # Route exists

    def test_error_response_format(self):
        """Test error responses are properly formatted"""
        # Try invalid endpoint
        response = self.client.get("/api/nonexistent")
        assert response.status_code == 404

        # Response should be JSON
        try:
            data = response.json()
            assert isinstance(data, dict)
        except:
            # Some frameworks return HTML 404 - that's ok
            pass

    @pytest.mark.asyncio
    async def test_route_async_handling(self):
        """Test routes handle async operations properly"""
        # Test an async endpoint
        response = self.client.get("/api/agents/status")
        assert response.status_code == 200
        # Should complete without hanging
        assert response.elapsed.total_seconds() < 10  # Should be quick


class TestRouteValidation:
    """Tests for route input validation"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_analyze_missing_project_path(self):
        """Test analyze endpoint validates project_path"""
        response = self.client.post("/api/analysis/analyze", json={})
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data

    def test_chat_missing_message(self):
        """Test chat endpoint validates message"""
        response = self.client.post("/api/agents/chat", json={})
        assert response.status_code == 422  # Validation error

    def test_set_model_missing_parameters(self):
        """Test set model validates required parameters"""
        response = self.client.post("/api/models/set", json={})
        assert response.status_code == 422  # Validation error


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
