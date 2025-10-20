# 🏗️ KI-Projektmanagement-System Architecture Documentation

**Version:** 2.0.0  
**Last Updated:** 2025-10-20  
**Status:** Production-Ready

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Diagram](#component-diagram)
4. [Data Flow](#data-flow)
5. [API Endpoints](#api-endpoints)
6. [Design Patterns](#design-patterns)
7. [Technology Stack](#technology-stack)
8. [Deployment Architecture](#deployment-architecture)

---

## 🎯 System Overview

The **KI-Projektmanagement-System** is an intelligent, containerized AI project management system that automatically analyzes project directories, generates optimized agents/workflows, and provides an AI project manager with local/cloud model support.

### Key Capabilities

- **Automated Project Analysis**: AST-based code analysis, framework detection, dependency graphing
- **AI Agent Generation**: Dynamic creation of specialized agents based on project structure
- **Workflow Orchestration**: Multi-phase analysis pipelines with progress tracking
- **Multi-Model Support**: OpenAI, Anthropic, Google, Ollama, LM Studio, GPT4All
- **Real-Time UI**: Streamlit-based interface with live updates
- **Microservices Architecture**: Modular, scalable, testable components

---

## 🏛️ Architecture Layers

### 1. **Presentation Layer** (Port: 8501)

**Components:**
- `streamlit_app.py` - Main UI application
- `ui/components/*` - Reusable UI widgets

**Responsibilities:**
- User interaction and visualization
- Real-time progress monitoring
- Chat interface for AI interaction
- Configuration management

**Technologies:**
- Streamlit 1.29.0
- HTML/CSS/JavaScript (inline)
- WebSocket (for real-time updates)

---

### 2. **API Layer** (Port: 8000)

**Components:**
- `app.py` - FastAPI initialization (384 lines)
- `routes/` - Endpoint handlers (4 modules)
  - `analysis_routes.py` - Project analysis endpoints
  - `agent_routes.py` - Agent/chat endpoints
  - `workflow_routes.py` - Workflow execution
  - `model_routes.py` - LLM model management

**Responsibilities:**
- REST API endpoints
- Request validation (Pydantic)
- CORS middleware
- Error handling
- Background task management

**Technologies:**
- FastAPI 0.104.1
- Uvicorn 0.24.0 (ASGI server)
- Pydantic for validation

---

### 3. **Business Logic Layer**

**Components:**
- `services/` - Business logic (2 modules)
  - `project_service.py` - Project operations
  - `agent_service.py` - Agent management

**Responsibilities:**
- Core business rules
- Data transformation
- Service orchestration
- State management

**Design Pattern:**
- Service Layer Pattern
- Dependency Injection
- Single Responsibility

---

### 4. **Analysis Engine**

**Components:**
- `analyzers/` - 7 specialized analyzers
  - `project_analyzer.py` - Orchestrator
  - `language_detector.py` - AST-based language detection
  - `framework_detector.py` - Framework identification
  - `dependency_analyzer.py` - Dependency graph
  - `api_analyzer.py` - API endpoint extraction
  - `database_analyzer.py` - Schema detection
  - `ast_analyzer.py` - Deep code analysis

**Responsibilities:**
- Multi-phase project analysis
- AST parsing and code metrics
- Pattern matching and detection
- Dependency graph construction

**Technologies:**
- tree-sitter 0.20.4
- esprima 4.0.1 (JavaScript)
- astroid 3.0.1 (Python)
- radon 6.0.1 (complexity)
- lizard 1.17.10 (multi-language)

---

### 5. **AI Agent System**

**Components:**
- `agents/` - AI agent implementations
  - `project_manager_agent.py` - Main coordinator
  - `example_agent.py` - Base templates
  - Dynamic agents (generated)

**Responsibilities:**
- Task execution
- Context management
- Skill orchestration
- Conversation handling

**Agent Types:**
- `BaseAgent` - Abstract base
- `TaskAgent` - Task execution
- `ConversationalAgent` - Dialogue
- `DataProcessingAgent` - Data operations

---

### 6. **Workflow System**

**Components:**
- `workflows/` - Workflow definitions
  - `base_workflow.py` - Abstract base
  - `project_analysis_workflow.py` - Full pipeline
  - `simple_analysis_workflow.py` - Lightweight
- `orchestrator/` - Orchestration
  - `workflow_orchestrator.py` - Workflow management
  - `agent_orchestrator.py` - Agent coordination

**Responsibilities:**
- Multi-step process execution
- Progress tracking
- State management
- Parallel execution

**Pattern:**
- Workflow Pattern
- State Machine
- Observer (for progress)

---

### 7. **Generator System**

**Components:**
- `generators/` - Dynamic generation
  - `agent_generator.py` - Agent creation
  - `skill_generator.py` - Skill generation
  - `workflow_generator.py` - Workflow creation

**Responsibilities:**
- Code generation from templates
- Agent specialization
- Workflow composition
- Skill synthesis

---

### 8. **LLM Integration Layer**

**Components:**
- `llm/` - Model management
  - `model_manager.py` - Provider abstraction
  - `api_models.py` - Cloud APIs (OpenAI, Anthropic, Google)
  - `local_models.py` - Local models (Ollama, LM Studio, GPT4All)
  - `prompt_templates.py` - Prompt management

**Responsibilities:**
- Multi-provider support
- Model switching
- API abstraction
- Error handling

**Supported Providers:**
- **Cloud**: OpenAI, Anthropic Claude, Google Gemini
- **Local**: Ollama, LM Studio, GPT4All

---

### 9. **Output Generation**

**Components:**
- `output/` - Report generation
  - `report_generator.py` - Markdown reports
  - `artifact_generator.py` - Deployment guides, test plans

**Responsibilities:**
- Report formatting
- Artifact creation
- Documentation generation

---

### 10. **Optimization System**

**Components:**
- `optimization/` - Code optimization
  - `optimization_engine.py` - Analysis and suggestions

**Responsibilities:**
- Code smell detection
- Performance recommendations
- Security suggestions
- Best practices enforcement

---

## 🔄 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Streamlit  │  │ UI Components│  │  WebSockets  │     │
│  │   Frontend   │  │   (Widgets)  │  │ (Real-time)  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                       API LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI (app.py)                                     │  │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────────┐ │  │
│  │  │ Analysis   │ │   Agent    │ │    Workflow      │ │  │
│  │  │  Routes    │ │   Routes   │ │     Routes       │ │  │
│  │  └────────────┘ └────────────┘ └──────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  ┌────────────────┐           ┌────────────────┐           │
│  │ Project Service│           │  Agent Service │           │
│  └────────────────┘           └────────────────┘           │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐  ┌────────────────┐  ┌───────────────┐
│   ANALYSIS    │  │   AI AGENTS    │  │   WORKFLOWS   │
│    ENGINE     │  │     SYSTEM     │  │  ORCHESTRATOR │
│               │  │                │  │               │
│ • Analyzers   │  │ • Task Agents  │  │ • Execution   │
│ • Detectors   │  │ • Chat Agents  │  │ • Tracking    │
│ • Parsers     │  │ • Data Agents  │  │ • State Mgmt  │
└───────────────┘  └────────────────┘  └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ↓
                    ┌──────────────┐
                    │   LLM LAYER  │
                    │              │
                    │ • OpenAI     │
                    │ • Anthropic  │
                    │ • Ollama     │
                    └──────────────┘
```

---

## 🔀 Data Flow

### Project Analysis Flow

```
User → UI → /api/analysis/analyze
              ↓
      WorkflowOrchestrator
              ↓
    ProjectAnalysisWorkflow
              ↓
      ┌──────────────────┐
      │ Phase 1: Scan    │  → File System
      └──────────────────┘
              ↓
      ┌──────────────────┐
      │ Phase 2: Detect  │  → LanguageDetector
      └──────────────────┘     FrameworkDetector
              ↓
      ┌──────────────────┐
      │ Phase 3: Analyze │  → DependencyAnalyzer
      └──────────────────┘     APIAnalyzer
              ↓                 DatabaseAnalyzer
      ┌──────────────────┐
      │ Phase 4: Report  │  → ReportGenerator
      └──────────────────┘
              ↓
         Results → User
```

### Agent Generation Flow

```
Analysis Results
      ↓
AgentGenerator
      ↓
  ┌────────────────────┐
  │ Determine Required │
  │   Agent Types      │
  └────────────────────┘
      ↓
  ┌────────────────────┐
  │ Generate Agent     │
  │   Definitions      │
  └────────────────────┘
      ↓
  ┌────────────────────┐
  │ Create Skills      │
  └────────────────────┘
      ↓
  ┌────────────────────┐
  │ Register Agents    │
  └────────────────────┘
      ↓
   Active Agents
```

---

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System info and available endpoints |
| GET | `/status` | System health and component status |
| GET | `/test` | Health check endpoint |

### Analysis Endpoints (`/api/analysis/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analysis/analyze` | Start project analysis |
| GET | `/api/analysis/results` | Get analysis results |
| GET | `/api/analysis/reports` | List generated reports |
| GET | `/api/analysis/artifacts` | List generated artifacts |

### Agent Endpoints (`/api/agents/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/agents/chat` | Chat with AI project manager |
| POST | `/api/agents/generate` | Generate agents from analysis |
| GET | `/api/agents/status` | Get agent status |
| GET | `/api/agents/optimizations` | Get optimization suggestions |

### Workflow Endpoints (`/api/workflows/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/workflows/execute/{type}` | Execute specific workflow |
| POST | `/api/workflows/run-complete` | Run full analysis + generation |
| GET | `/api/workflows/status` | Get all workflow statuses |
| GET | `/api/workflows/progress/{id}` | Get workflow progress |

### Model Endpoints (`/api/models/*`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/models` | List available LLM models |
| POST | `/api/models/set` | Set active LLM model |
| GET | `/api/models/current` | Get currently active model |

---

## 🎨 Design Patterns

### 1. **Lazy Loading**
Components initialized on-demand to improve startup performance.

```python
async def ensure_components_initialized():
    global _components_initialized
    if _components_initialized:
        return
    
    # Initialize only when needed
    project_manager_agent = ProjectManagerAgent(model_manager)
    agent_orchestrator = AgentOrchestrator(model_manager)
```

### 2. **Service Layer Pattern**
Business logic separated from API handlers.

```python
# Service handles business logic
class ProjectService:
    async def analyze_project(self, path: str) -> Dict:
        return self.project_analyzer.analyze(path)

# Route delegates to service
@router.post("/analyze")
async def analyze(request, service):
    return await service.analyze_project(request.project_path)
```

### 3. **Dependency Injection**
Components receive dependencies explicitly.

```python
def __init__(self, project_analyzer, model_manager):
    self.project_analyzer = project_analyzer
    self.model_manager = model_manager
```

### 4. **Workflow Pattern**
Complex operations broken into orchestrated workflows.

```python
class ProjectAnalysisWorkflow(BaseWorkflow):
    async def execute(self, context):
        # Phase 1: Scan
        # Phase 2: Detect
        # Phase 3: Analyze
        # Phase 4: Report
        return results
```

### 5. **Module Registry**
Dynamic loading and registration of components.

```python
loaded_modules = {
    'agents': {},
    'skills': {},
    'workflows': {}
}
```

---

## 💻 Technology Stack

### Backend
- **Python**: 3.11+
- **FastAPI**: 0.104.1 (async web framework)
- **Uvicorn**: 0.24.0 (ASGI server)
- **Pydantic**: 2.x (validation)

### Frontend
- **Streamlit**: 1.29.0 (UI framework)
- **HTML/CSS/JS**: Inline custom components

### AI/ML
- **OpenAI**: 1.3.7
- **Anthropic**: 0.7.8
- **Ollama**: 0.1.6
- **Google AI Python Client**: 2.108.0

### Code Analysis
- **tree-sitter**: 0.20.4 (AST parsing)
- **esprima**: 4.0.1 (JavaScript)
- **astroid**: 3.0.1 (Python)
- **radon**: 6.0.1 (complexity)
- **lizard**: 1.17.10 (multi-language)

### Infrastructure
- **Docker**: Containerization
- **MongoDB**: 4.6.0 (optional, metadata)
- **Redis**: 5.0.1 (optional, caching)
- **Prometheus** + **Grafana**: Monitoring

---

## 🚀 Deployment Architecture

### Development

```
┌──────────────────────────────────────┐
│         Developer Machine            │
│                                      │
│  ┌──────────┐      ┌──────────┐    │
│  │Streamlit │:8501 │ FastAPI  │:8000│
│  │   Dev    │◄────►│   Dev    │    │
│  └──────────┘      └──────────┘    │
│                         │            │
│                         ↓            │
│                  ┌──────────┐       │
│                  │ Ollama/  │       │
│                  │ LM Studio│       │
│                  └──────────┘       │
└──────────────────────────────────────┘
```

### Production (Docker)

```
┌───────────────────────────────────────────────┐
│             Docker Host                        │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │     Docker Compose Network              │ │
│  │                                         │ │
│  │  ┌──────────┐      ┌──────────┐       │ │
│  │  │Streamlit │:8501 │ FastAPI  │:8000  │ │
│  │  │Container │◄────►│Container │       │ │
│  │  └──────────┘      └──────────┘       │ │
│  │        │                 │             │ │
│  │        └────────┬────────┘             │ │
│  │                 ↓                      │ │
│  │          ┌─────────────┐               │ │
│  │          │   MongoDB   │:27017         │ │
│  │          │  Container  │               │ │
│  │          └─────────────┘               │ │
│  │                 │                      │ │
│  │          ┌─────────────┐               │ │
│  │          │    Redis    │:6379          │ │
│  │          │  Container  │               │ │
│  │          └─────────────┘               │ │
│  │                                         │ │
│  │  ┌──────────┐      ┌──────────┐       │ │
│  │  │Prometheus│:9090 │ Grafana  │:3000  │ │
│  │  │Container │◄────►│Container │       │ │
│  │  └──────────┘      └──────────┘       │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  Volume Mounts:                               │
│  • ./data → /data                            │
│  • ./logs → /logs                            │
│  • ./analysis_output → /analysis_output      │
└───────────────────────────────────────────────┘
```

---

## 📊 Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Components load on-demand
2. **Async I/O**: Non-blocking operations
3. **Caching**: Redis for analysis results
4. **Background Tasks**: Long-running analysis via FastAPI BackgroundTasks
5. **Database Indexing**: MongoDB indexes on frequently queried fields

### Scalability

- **Horizontal**: Multiple FastAPI instances behind load balancer
- **Vertical**: Increase container resources
- **Caching**: Redis for frequently accessed data
- **Queue**: Celery for distributed task processing (future)

---

## 🔒 Security

### Implemented

- **CORS**: Configurable origins
- **Input Validation**: Pydantic models
- **Environment Variables**: Secrets in `.env`
- **Dependency Scanning**: `safety` for vulnerabilities

### Planned

- **Authentication**: JWT tokens
- **Rate Limiting**: Per-endpoint throttling
- **API Keys**: Secure storage in env vars
- **HTTPS**: TLS certificates

---

## 📈 Monitoring

### Metrics (Prometheus)

- Request latency
- Error rates
- Active workflows
- Agent execution times
- LLM API calls

### Dashboards (Grafana)

- System health
- API performance
- Workflow progress
- Resource usage

---

## 🔧 Maintenance

### Logging

- **Level**: INFO (production), DEBUG (development)
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Location**: `logs/` directory + stdout

### Backup

- MongoDB: Daily backups
- Analysis results: Retained 90 days
- Generated artifacts: Version controlled

---

**For implementation details, see:**
- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Development Guide](../README.md)

