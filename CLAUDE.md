# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KI-Projektmanagement-System** is an intelligent, containerized AI project management system that automatically analyzes project directories, generates optimized agents/workflows, and provides an AI project manager with local/cloud model support. The system is designed to analyze codebases and create specialized agents, skills, and workflows tailored to the detected project structure.

## Architecture

### Core Components

The system follows a modular, multi-layer architecture:

1. **Web Interface Layer** ([streamlit_app.py](streamlit_app.py))
   - Streamlit-based UI for project selection and interaction
   - Real-time dashboard showing analysis progress
   - Chat interface for AI project manager

2. **API Layer** ([app.py](app.py))
   - FastAPI backend serving REST endpoints
   - Handles project analysis requests, workflow execution, and agent management
   - Lazy loading of components to reduce startup time (components initialized on first use)
   - See "API Endpoints" section below for complete endpoint documentation

3. **Analysis Engine** ([analyzers/](analyzers/))
   - **ProjectAnalyzer**: Orchestrates all analysis phases
   - **LanguageDetector**: AST-based language detection
   - **FrameworkDetector**: Identifies frameworks from project structure
   - **DependencyAnalyzer**: Analyzes dependencies and creates dependency graphs
   - **APIAnalyzer**: Extracts API endpoints from code
   - **DatabaseAnalyzer**: Analyzes database schemas and migrations
   - **ASTAnalyzer**: Deep code analysis using AST parsing

4. **Agent System** ([agents/](agents/))
   - **ProjectManagerAgent**: Main AI intelligence coordinating the system
   - Dynamically generated agents based on project analysis
   - Agent orchestration via [orchestrator/agent_orchestrator.py](orchestrator/agent_orchestrator.py)

5. **Workflow System** ([workflows/](workflows/) & [orchestrator/](orchestrator/))
   - **WorkflowOrchestrator**: Manages workflow execution and state
   - **BaseWorkflow**: Base class for all workflows
   - **ProjectAnalysisWorkflow**: Complete project analysis pipeline
   - **SimpleAnalysisWorkflow**: Lightweight analysis workflow
   - Workflow registration and execution tracking

6. **Generator System** ([generators/](generators/))
   - **AgentGenerator**: Creates specialized agents based on analysis results
   - **SkillGenerator**: Generates skills for agent capabilities
   - **WorkflowGenerator**: Generates orchestrated workflows

7. **LLM Integration** ([llm/](llm/))
   - **ModelManager**: Manages multiple LLM providers (local and cloud)
   - **LocalModels**: Ollama, LM Studio, GPT4All integration
   - **APIModels**: OpenAI, Anthropic, Google integration
   - **PromptTemplates**: Centralized prompt management

8. **Output Generation** ([output/](output/))
   - **ReportGenerator**: Creates markdown analysis reports
   - **ArtifactGenerator**: Generates deployment guides, test plans, etc.

9. **Optimization System** ([optimization/](optimization/))
   - **OptimizationEngine**: Analyzes code and suggests improvements
   - Provides continuous optimization recommendations

10. **UI Components** ([ui/components/](ui/components/))
   - **ModernProjectSelector**: Enhanced project directory picker with drag-and-drop
   - **ProgressMonitor**: Real-time analysis progress tracking
   - **StatusWidget**: System status display with component health
   - **AnalysisDashboard**: Comprehensive analysis results visualization
   - **ChatInterface**: Chat UI for AI project manager interaction
   - **SettingsPanel**: LLM model and system configuration
   - **OptimizationView**: Display and apply optimization suggestions
   - **AgentMonitor**: Monitor generated agents and their status

### Key Design Patterns

- **Lazy Loading**: Components initialized on-demand to improve startup performance. On startup, only the ModelManager is initialized. ProjectManagerAgent and AgentOrchestrator are loaded when first needed.
- **Async/Await**: Extensive use of async for I/O-bound operations (file scanning, API calls, LLM requests)
- **Module Registry**: Dynamic loading of agents, skills, commands, hooks, plugins, and MCPs stored in the `loaded_modules` global dictionary
- **Workflow Pattern**: Complex operations broken into orchestrated workflows with progress tracking

### State Management

The system uses several global variables for state management in [app.py](app.py):

- **`current_project`**: Currently analyzed project path
- **`analysis_results`**: Latest analysis results (cached in memory)
- **`loaded_modules`**: Registry of dynamically loaded agents/skills/commands/hooks/plugins/MCPs
- **`_components_initialized`**: Lazy loading flag for system components

**Important**: State is stored in-memory only. Restarting the application clears all state.

## Development Commands

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit UI (primary interface)
streamlit run streamlit_app.py

# Run FastAPI backend separately
uvicorn app:app --reload

# Run both together (recommended for development)
python app.py  # Starts FastAPI on :8000
# In another terminal:
streamlit run streamlit_app.py  # Starts Streamlit on :8501
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analyzers.py

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test markers
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m "not slow"     # Skip slow tests
```

### Docker

```bash
# Build and run with Docker Compose (production)
docker-compose up -d

# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up -d

# Stop containers
docker-compose down

# Clean everything (including volumes)
docker-compose down -v --rmi all

# View logs
docker-compose logs -f ai-project-manager

# Check status
docker-compose ps
```

### Makefile Commands

```bash
# See all available commands
make help

# Development workflow
make install          # Install dependencies
make test            # Run tests
make run             # Run application locally
make lint            # Run linting
make format          # Format code with black and isort

# Docker workflow
make docker-build    # Build Docker image
make docker-run      # Run with Docker Compose
make docker-stop     # Stop containers
make docker-clean    # Clean Docker resources

# Setup
make setup           # Initial setup (creates dirs, copies config)
make clean           # Clean temporary files
```

## Configuration

### Environment Variables

The system uses environment variables defined in `config.env` and `.env`:

- **PROJECT_PATH**: Path to the project to analyze (set by user in UI)
- **OPENAI_API_KEY**, **ANTHROPIC_API_KEY**, **GOOGLE_API_KEY**: API keys for cloud LLMs
- **OLLAMA_HOST**, **LMSTUDIO_HOST**, **GPT4ALL_PATH**: Local LLM endpoints
- **MONGODB_URL**, **REDIS_URL**: Database connections

### Settings System

The [settings/](settings/) module provides centralized configuration management:

- Loads defaults, environment variables, and JSON config files
- Supports dot-notation access (e.g., `settings.get("ai_providers.openai.model")`)
- Environment-specific configs (development, testing, production)
- Config validation with error reporting

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with system info and available endpoints
- `GET /status` - System health and component status
- `GET /test` - Test endpoint for health checks

### Analysis Endpoints

- `POST /analyze-project` - Start project analysis (body: `{"project_path": "..."}`)
- `GET /analysis-results` - Get cached analysis results
- `GET /reports` - List generated analysis reports
- `GET /artifacts` - List generated artifacts

### Chat & Agent Endpoints

- `POST /chat` - Chat with AI project manager (params: `message`, `context`)
- `POST /generate-agents` - Generate agents from analysis results
- `GET /agent-status` - Get status of all generated agents
- `GET /optimizations` - Get optimization suggestions from agent

### Workflow Endpoints

- `POST /execute-workflow/{workflow_type}` - Execute specific workflow
- `POST /run-complete-workflow` - Run full analysis + generation workflow
- `GET /workflow-status` - Get all workflow statuses
- `GET /workflow-progress/{workflow_id}` - Get specific workflow progress with phases

### Optimization Endpoints

- `GET /optimization-suggestions` - Get detailed optimization analysis

### Model Management Endpoints

- `GET /models` - List available LLM models (local and cloud)
- `POST /set-model` - Set active LLM model (params: `model_name`, `model_type`)

## Project Workflow

### Analysis Workflow

When analyzing a project, the system executes this pipeline:

1. **File Scanning**: Recursively scans project directory
2. **Language Detection**: AST-based analysis to identify languages
3. **Framework Detection**: Identifies frameworks from file patterns and configs
4. **Dependency Analysis**: Parses package files and builds dependency graph
5. **API Extraction**: Analyzes code for API endpoints
6. **Database Analysis**: Detects schemas, migrations, and models
7. **Security Scan**: Identifies potential vulnerabilities
8. **Test Coverage**: Analyzes test files and coverage

Results stored in `analysis_results` global variable and available via `/analysis-results` endpoint.

### Agent Generation Workflow

After analysis, specialized agents can be auto-generated:

1. Analysis results examined to determine agent types needed
2. **AgentGenerator** creates agent definitions based on detected frameworks
3. **SkillGenerator** creates skills for each agent
4. **WorkflowGenerator** creates orchestrated workflows
5. Agents registered in `loaded_modules` registry
6. Available via `/agent-status` and `/execute-workflow/{type}` endpoints

### Workflow Execution Pattern

Workflows extend `BaseWorkflow` and implement `execute()` method:

```python
from workflows.base_workflow import BaseWorkflow

class MyWorkflow(BaseWorkflow):
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        return results
```

Register with `WorkflowOrchestrator.register_workflow(name, workflow_instance)`.

## Important Patterns

### Adding New Analyzers

1. Create analyzer in [analyzers/](analyzers/) extending base pattern
2. Add to `ProjectAnalyzer.__init__()` initialization
3. Call analyzer in `ProjectAnalyzer.analyze_project()` during appropriate phase
4. Update progress callback for UI feedback

### Adding New Workflows

1. Create workflow in [workflows/](workflows/) extending `BaseWorkflow`
2. Register in `WorkflowOrchestrator.__init__()`
3. Workflow IDs follow pattern: `{workflow_name}_{index}`
4. Track state in `running_workflows` and `workflow_history`

### API Endpoint Pattern

All FastAPI endpoints follow this pattern:
- Try-except with detailed logging
- HTTP exceptions with appropriate status codes
- Return structured JSON with status/message/data
- Background tasks for long-running operations using `BackgroundTasks`

### Progress Tracking

The UI expects real-time progress updates:
- Use `progress_callback` in analyzers for phase updates
- Workflows store state in `running_workflows` with `current_phase` and `overall_progress`
- `/workflow-progress/{workflow_id}` endpoint provides live status

## Testing Structure

Tests are organized in [tests/](tests/) with the following structure:

- **test_app.py**: FastAPI endpoint integration tests
- **test_agents.py**: Agent functionality and lifecycle tests
- **test_settings.py**: Settings system and configuration tests
- **test_skills.py**: Skill generation and execution tests
- **test_analyzers.py**: Analyzer module tests

### Test Markers

Run tests with markers defined in [pytest.ini](pytest.ini):

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (slower, with dependencies)
- `@pytest.mark.slow` - Slow-running tests (can be skipped with `-m "not slow"`)
- `@pytest.mark.asyncio` - Async tests

### Testing Strategy

- Unit tests: Individual analyzers, generators, models
- Integration tests: Full workflow execution, API endpoints
- Mock external services (OpenAI, Anthropic, etc.) in tests
- Test fixtures in [tests/fixtures/](tests/fixtures/) for sample projects

## Key Dependencies

### Core Framework

- **FastAPI** (0.104.1) - API backend
- **Streamlit** (1.29.0) - Web UI
- **Uvicorn** (0.24.0) - ASGI server

### LLM Integration

- **OpenAI** (1.3.7) - OpenAI API client
- **Anthropic** (0.7.8) - Claude API client
- **Ollama** (0.1.6) - Local model integration
- **Google API Python Client** (2.108.0) - Google AI integration

### Code Analysis

- **tree-sitter** (0.20.4) - AST parsing
- **esprima** (4.0.1) - JavaScript parsing
- **astroid** (3.0.1) - Python AST analysis
- **radon** (6.0.1) - Code metrics and complexity
- **lizard** (1.17.10) - Multi-language complexity analysis
- **safety** (2.3.5) - Security vulnerability scanning

### Infrastructure

- **MongoDB** (pymongo 4.6.0) - Metadata and results storage
- **Redis** (5.0.1) - Caching and task queue
- **Celery** (5.3.4) - Distributed task queue (for future use)

## Utility Scripts

The project includes standalone utility scripts for maintenance and debugging:

- **`monitor_analysis.py`**: Monitor running analysis workflows
- **`monitor_real_analysis.py`**: Advanced real-time analysis monitoring
- **`monitor_workflow.py`**: Workflow execution progress monitoring
- **`fix_security_issues.py`**: Automated security issue detection and remediation
- **`reduce_complexity.py`**: Code complexity reduction suggestions
- **`fix_hardcoded_secrets.py`**: Secret detection and remediation
- **`improve_error_handling.py`**: Error handling improvement suggestions

These scripts are standalone tools, not part of the main application. Run them directly with Python.

## Services and Ports

- **Streamlit UI**: <http://localhost:8501>
- **FastAPI Backend**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379
- **Prometheus**: <http://localhost:9090> (included by default)
- **Grafana**: <http://localhost:3000> (included by default, credentials: admin/admin)

## Logging

The system uses Python's logging module extensively:

- Emoji prefixes for visibility: 🚀 (startup), ✅ (success), ❌ (error), 🔄 (processing)
- Module-level loggers: `logger = logging.getLogger(__name__)`
- Log levels configurable via settings or LOG_LEVEL env var

## Known Limitations

1. **In-Memory State**: Analysis results and project state are stored in memory only. Server restart loses all state.
2. **Single Project**: Only one project can be analyzed at a time per application instance.
3. **No Persistence**: Generated agents/workflows are not persisted to database by default.
4. **Background Tasks**: Long-running workflows use FastAPI BackgroundTasks (not recommended for production at scale - consider using Celery for distributed task processing).
5. **Monitoring Setup**: Prometheus and Grafana are included in docker-compose.yml but may require manual configuration in the `monitoring/` directory.

## Troubleshooting

### Analysis Stuck at 0%

- Check logs: `docker-compose logs -f ai-project-manager`
- Verify project path is accessible and readable
- Ensure PROJECT_PATH environment variable is set correctly in `.env`
- Check file permissions on mounted volume

### Chat/Agent Not Responding

- Verify at least one LLM API key is configured in `.env`
- Check available models: `curl http://localhost:8000/models`
- Try setting model explicitly: `curl -X POST "http://localhost:8000/set-model?model_name=gpt-3.5-turbo&model_type=openai"`
- Review logs for LLM API errors

### Docker Build Fails

- Ensure all dependencies in requirements.txt are available
- Check Docker has sufficient memory (4GB+ recommended)
- Verify Python version compatibility (Python 3.9+ required)
- Clear Docker cache: `docker system prune -a`

### Tests Failing

- Run with verbose output: `pytest -v`
- Check if test fixtures exist in `tests/fixtures/`
- Ensure test database connections are configured
- Install test dependencies: `pip install -r requirements.txt`

### Port Already in Use

```bash
# Windows (using provided batch file)
view_logs.bat

# Linux/Mac - Find and kill process
lsof -ti:8501 | xargs kill -9  # For Streamlit
lsof -ti:8000 | xargs kill -9  # For FastAPI

# Or change ports in docker-compose.yml
```

### Workflow Progress Not Updating

- Check if workflow is registered: `curl http://localhost:8000/workflow-status`
- Verify workflow_id matches the returned ID from `/analyze-project`
- Check if workflow completed (check `workflow_history` in status)
- Review application logs for workflow errors

### LLM Model Not Available

- For local models (Ollama): Ensure Ollama service is running and accessible
- For cloud APIs: Verify API keys are set correctly
- Check model availability: `GET /models` endpoint
- Review ModelManager initialization in logs
