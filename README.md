# 🤖 KI-Projektmanagement-System

Ein intelligentes, vollständig containerisiertes AI-Projektmanagement-System, das Projektordner automatisch analysiert, optimierte Agents/Workflows generiert und einen KI-Projektmanager mit lokalem/Cloud-Modell-Support bereitstellt.

## ✨ Features

### 🎯 Kern-Funktionen
- **📁 Automatische Projekt-Analyse** - Vollständige Code-Analyse mit AST-Parsing
- **🤖 KI-Projektmanager Agent** - Intelligenter Haupt-Agent mit Live-Chat
- **🛠️ Auto-Generierung** - Agents, Workflows und Skills basierend auf Projekt
- **💬 Natural Language Commands** - Chat-Interface für Änderungen während der Ausführung
- **📊 Optimierungs-Tool** - Kontinuierliche Verbesserungsvorschläge
- **🔄 Orchestrierte Multi-Agent-Architektur** - Spezifisch für das analysierte Projekt

### 🎨 Benutzeroberfläche
- **Streamlit Web-UI** - Moderne, responsive Benutzeroberfläche
- **📁 Drag & Drop** - Einfache Projektordner-Auswahl
- **📊 Live-Dashboard** - Echtzeit-Updates während der Analyse
- **💬 Chat-Interface** - Direkter Chat mit dem KI-Projektmanager
- **⚙️ Einstellungen** - Konfiguration für lokale und Cloud-Modelle

### 🧠 KI-Integration
- **Lokale Modelle**: Ollama, LM Studio, GPT4All
- **Cloud-APIs**: OpenAI, Anthropic, Google
- **Automatisches Fallback** - Wechsel zwischen Modellen
- **Streaming-Responses** - Echtzeit-Antworten

### 🔍 Projekt-Analyse
- **Sprach-Erkennung** - AST-basierte Code-Analyse
- **Framework-Erkennung** - Automatische Framework-Identifikation
- **Dependency-Analyse** - Vollständiger Dependency-Graph
- **API-Extraktion** - Automatische Endpoint-Erkennung
- **Security-Scan** - Vulnerability-Assessment
- **Test-Coverage** - Analyse der Test-Abdeckung

## 🚀 Quick Start

### 1. Setup

```bash
# Repository klonen
git clone <repository-url>
cd APP-Finisher

# .env erstellen
echo "PROJECT_PATH=/path/to/your/project" > .env
echo "OPENAI_API_KEY=your_key" >> .env
echo "ANTHROPIC_API_KEY=your_key" >> .env
echo "GOOGLE_API_KEY=your_key" >> .env
```

### 2. Starten

```bash
# Mit Docker Compose
docker-compose up -d

# Oder manuell
docker build -t ki-project-manager .
docker run -p 8501:8501 -p 8000:8000 -v /path/to/your/project:/workspace:ro ki-project-manager
```

### 3. Öffnen

- **Web-UI**: http://localhost:8501
- **API-Docs**: http://localhost:8000/docs
- **Status**: http://localhost:8000/status

## 📋 Verwendung

### 1. Projekt auswählen
- Öffne die Web-UI unter http://localhost:8501
- Wähle deinen Projektordner aus
- Klicke auf "Analyse starten"

### 2. Analyse abwarten
- Das System analysiert automatisch:
  - Code-Struktur und Sprachen
  - Frameworks und Dependencies
  - API-Endpoints
  - Security-Issues
  - Test-Coverage

### 3. Mit KI-Projektmanager chatten
- Nutze das Chat-Interface für:
  - "Analysiere mein Projekt"
  - "Optimiere die Performance"
  - "Erstelle Tests für die API"
  - "Finde Security-Probleme"

### 4. Optimierungen anwenden
- Sieh dir die vorgeschlagenen Optimierungen an
- Wende sie mit einem Klick an
- Verfolge den Fortschritt im Dashboard

## 🏗️ Architektur

### Komponenten
```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web-UI                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Dashboard │ │ Chat-Interface│ │ Einstellungen│          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   API       │ │   Status    │ │   Health    │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                KI-Projektmanager Agent                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Chat      │ │   Analysis  │ │ Optimization│          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                Projekt-Analyse-Engine                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Language  │ │  Framework  │ │ Dependency  │          │
│  │   Detector  │ │   Detector  │ │  Analyzer   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    LLM-Integration                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │   Local     │ │    API      │ │   Prompt    │          │
│  │   Models    │ │   Models    │ │ Templates   │          │
│  └─────────────┘ └─────────────┘ └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Services
- **ai-project-manager**: Haupt-Container mit Streamlit + FastAPI
- **mongodb**: Projekt-Metadaten und Analyse-Ergebnisse
- **redis**: Task-Queue und Caching
- **ollama**: Lokale LLM-Runtime (optional)

## ⚙️ Konfiguration

### Umgebungsvariablen

```bash
# Projekt-Pfad (wird vom User gesetzt)
PROJECT_PATH=/path/to/your/project

# API-Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Lokale LLM-Services
OLLAMA_HOST=http://localhost:11434
LMSTUDIO_HOST=http://localhost:1234
GPT4ALL_PATH=/root/.cache/gpt4all/

# Datenbank
MONGODB_URL=mongodb://mongodb:27017
REDIS_URL=redis://redis:6379
```

### Lokale LLM-Setup

#### Ollama
```bash
# Installieren
curl -fsSL https://ollama.ai/install.sh | sh

# Modell herunterladen
ollama pull codellama:7b
ollama pull mistral:7b

# Starten
ollama serve
```

#### LM Studio
1. Download: https://lmstudio.ai/
2. Modell laden
3. Local Server starten

#### GPT4All
1. Download: https://gpt4all.io/
2. Modell herunterladen
3. Pfad in .env setzen

## 🔧 Entwicklung

### Lokale Entwicklung

```bash
# Dependencies installieren
pip install -r requirements.txt

# Streamlit UI starten
streamlit run streamlit_app.py

# FastAPI Backend starten
uvicorn app:app --reload
```

### Tests

```bash
# Alle Tests
pytest

# Spezifische Tests
pytest tests/test_analyzers.py
pytest tests/test_agents.py
```

### Linting

```bash
# Code-Formatierung
black .

# Linting
flake8 .

# Type-Checking
mypy .
```

## 📊 Monitoring

### Prometheus + Grafana
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### Health Checks
- **System**: http://localhost:8000/status
- **Models**: http://localhost:8000/models
- **Analysis**: http://localhost:8000/analysis-results

## 🛠️ Erweiterte Features

### Automatische Agent-Generierung
Das System generiert automatisch spezialisierte Agents basierend auf der Projekt-Analyse:

- **Backend-Agent**: Versteht das Backend-Framework, testet API-Endpoints
- **Frontend-Agent**: Versteht UI-Framework, führt Component-Tests aus
- **Database-Agent**: Versteht DB-Schema, generiert Migrations
- **Test-Agent**: Generiert und führt Tests aus
- **Security-Agent**: Führt Security-Scans durch

### Workflow-Orchestrierung
- **Testing-Workflow**: Automatische Test-Ausführung
- **Build-Workflow**: Optimierte Build-Prozesse
- **Deployment-Workflow**: Production-ready Deployment
- **CI/CD-Integration**: GitHub Actions / GitLab CI

### Output-Generierung
- **PROJECT_ANALYSIS.md**: Vollständige Projekt-Übersicht
- **OPTIMIZATION_REPORT.md**: Angewendete Optimierungen
- **TEST_REPORT.md**: Test-Ergebnisse und Coverage
- **DEPLOYMENT_GUIDE.md**: Deployment-Anleitung

## 🤝 Contributing

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Documentation**: [Wiki](https://github.com/your-repo/wiki)

## 🎯 Roadmap

- [ ] **Phase 5**: Agent-Generierung (Automatisierung)
- [ ] **Phase 7**: Testing-Integration (Reale Tests)
- [ ] **Phase 8**: Workflow-Orchestrierung (Vollautomatisch)
- [ ] **Phase 9**: Output-Generierung (Finale Artefakte)
- [ ] **Phase 10**: Optimierungs-Tools (Continous Improvement)

---

**Entwickelt mit ❤️ für die Zukunft der Software-Entwicklung**