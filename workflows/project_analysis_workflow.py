"""
Project Analysis Workflow
"""

import asyncio
from typing import Any, Dict

from analyzers.project_analyzer import ProjectAnalyzer
from generators.agent_generator import AgentGenerator
from generators.skill_generator import SkillGenerator
from generators.workflow_generator import WorkflowGenerator
from llm.model_manager import ModelManager

from .base_workflow import BaseWorkflow


class ProjectAnalysisWorkflow(BaseWorkflow):
    """Complete project analysis and agent generation workflow"""

    def __init__(self):
        super().__init__(
            name="ProjectAnalysisWorkflow",
            description="Complete project analysis, agent generation, and optimization workflow",
        )
        self.project_analyzer = ProjectAnalyzer()
        self.llm_manager = ModelManager()
        self.agent_generator = AgentGenerator(self.llm_manager)
        self.skill_generator = SkillGenerator(self.llm_manager)
        self.workflow_generator = WorkflowGenerator(self.llm_manager)

        # Define workflow steps
        self.add_step("analyze_project", self._analyze_project)
        self.add_step("generate_agents", self._generate_agents, ["analyze_project"])
        self.add_step("generate_skills", self._generate_skills, ["analyze_project"])
        self.add_step("generate_workflows", self._generate_workflows, ["analyze_project"])
        self.add_step(
            "create_optimization_plan",
            self._create_optimization_plan,
            ["generate_agents", "generate_skills"],
        )
        self.add_step(
            "generate_tests", self._generate_tests, ["generate_agents", "generate_skills"]
        )

    async def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the complete workflow"""
        if not context or "project_path" not in context:
            raise ValueError("Project path is required in context")

        self.status = "running"
        project_path = context["project_path"]

        try:
            # Step 1: Analyze project
            analysis_results = await self.run_step(
                "analyze_project", {"project_path": project_path}
            )

            # Step 2: Generate agents
            agents = await self.run_step("generate_agents", {"analysis": analysis_results})

            # Step 3: Generate skills
            skills = await self.run_step("generate_skills", {"analysis": analysis_results})

            # Step 4: Generate workflows
            workflows = await self.run_step("generate_workflows", {"analysis": analysis_results})

            # Step 5: Create optimization plan
            optimization_plan = await self.run_step(
                "create_optimization_plan",
                {"analysis": analysis_results, "agents": agents, "skills": skills},
            )

            # Step 6: Generate tests
            tests = await self.run_step(
                "generate_tests", {"analysis": analysis_results, "agents": agents, "skills": skills}
            )

            self.status = "completed"
            self.results = {
                "analysis": analysis_results,
                "agents": agents,
                "skills": skills,
                "workflows": workflows,
                "optimization_plan": optimization_plan,
                "tests": tests,
            }

            return self.results

        except Exception as e:
            self.status = "failed"
            raise

    async def _analyze_project(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the project structure and content"""
        project_path = context["project_path"]

        # Progress callback für Live-Updates
        async def progress_callback(message: str, percentage: int, details: Dict = None):
            self._update_phase_status("analyze_project", "running", percentage, details)

        return await self.project_analyzer.analyze_project(project_path, progress_callback)

    async def _generate_agents(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agents based on project analysis"""
        analysis = context["analysis"]
        return await self.agent_generator.generate_agents_for_project(analysis)

    async def _generate_skills(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate skills based on project analysis"""
        analysis = context["analysis"]
        return await self.skill_generator.generate_skills_for_project(analysis)

    async def _generate_workflows(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflows based on project analysis"""
        analysis = context["analysis"]
        return await self.workflow_generator.generate_workflows_for_project(analysis)

    async def _create_optimization_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create optimization plan based on analysis and generated components"""
        analysis = context["analysis"]
        agents = context["agents"]
        skills = context["skills"]

        # Use LLM to create optimization plan
        llm = self.llm_manager.get_model()

        prompt = f"""
        Based on the following project analysis and generated components, create a comprehensive optimization plan:
        
        Project Analysis: {analysis}
        Generated Agents: {agents}
        Generated Skills: {skills}
        
        Create an optimization plan that includes:
        1. Code quality improvements
        2. Performance optimizations
        3. Security enhancements
        4. Architecture improvements
        5. Testing strategies
        6. Deployment optimizations
        
        Return the plan as a structured JSON object.
        """

        response = llm.generate_response(prompt)
        return {"optimization_plan": response}

    async def _generate_tests(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tests for the project"""
        analysis = context["analysis"]
        agents = context["agents"]
        skills = context["skills"]

        # Use LLM to generate tests
        llm = self.llm_manager.get_model()

        prompt = f"""
        Based on the following project analysis and generated components, create comprehensive tests:
        
        Project Analysis: {analysis}
        Generated Agents: {agents}
        Generated Skills: {skills}
        
        Generate:
        1. Unit tests for key functions
        2. Integration tests for workflows
        3. API tests for endpoints
        4. Performance tests
        5. Security tests
        
        Return the tests as structured code examples.
        """

        response = llm.generate_response(prompt)
        return {"tests": response}
