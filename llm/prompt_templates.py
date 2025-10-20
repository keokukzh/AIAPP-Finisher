"""
Prompt-Templates für verschiedene Aufgaben
"""

import json
from typing import Any, Dict, List

# Direkte Prompt-Konstanten für Kompatibilität
AGENT_GENERATION_PROMPT = """
Basierend auf der folgenden Projektanalyse, generiere eine Python-Klasse für einen KI-Agenten.
Der Agent sollte eine spezifische Rolle im Projekt übernehmen und über definierte Fähigkeiten (Skills) verfügen.

Projektanalyse:
{analysis_results}

Anforderungen an den Agenten:
- Name: {agent_name}
- Rolle: {agent_role}
- Ziel: {agent_goal}
- Benötigte Skills: {required_skills} (Liste von Skill-Namen)

Generiere den Python-Code für die Klasse `{agent_name}Agent` in der Datei `agents/{agent_name.lower()}_agent.py`.
Die Klasse sollte von einer Basis-Agentenklasse erben (z.B. `BaseAgent`) und Methoden für die definierten Skills enthalten.
"""

SKILL_GENERATION_PROMPT = """
Basierend auf der folgenden Projektanalyse und der Beschreibung eines benötigten Skills, generiere eine Python-Funktion für diesen Skill.
Der Skill sollte eine spezifische Aufgabe im Kontext des Projekts ausführen können.

Projektanalyse:
{analysis_results}

Skill-Beschreibung:
- Name: {skill_name}
- Zweck: {skill_purpose}
- Eingaben: {skill_inputs}
- Ausgaben: {skill_outputs}
- Benötigte Abhängigkeiten/Tools: {skill_dependencies}

Generiere den Python-Code für die Funktion `{skill_name.lower()}_skill` in der Datei `skills/{skill_name.lower()}_skill.py`.
Die Funktion sollte die beschriebene Logik implementieren.
"""

CHAT_RESPONSE_PROMPT = """
Du bist der KI-Projektmanager. Deine Aufgabe ist es, auf Benutzeranfragen bezüglich des Projekts zu antworten,
Optimierungsvorschläge zu machen und bei der Steuerung der Agenten zu helfen.
Das aktuelle Projekt wurde wie folgt analysiert:
{analysis_results}

Bisheriger Chatverlauf:
{chat_history}

Benutzerfrage: {user_query}

Antworte präzise, hilfreich und im Kontext des Projekts. Schlage bei Bedarf nächste Schritte oder Aktionen vor.
"""

OPTIMIZATION_PROMPT = """
Basierend auf der folgenden detaillierten Projektanalyse, identifiziere Bereiche für Optimierungen in Bezug auf:
- Code-Qualität (Komplexität, Wartbarkeit, Best Practices)
- Performance (Engpässe, Effizienz)
- Sicherheit (Schwachstellen, veraltete Abhängigkeiten)
- Skalierbarkeit (Architektur, Infrastruktur)
- Kosten (Ressourcennutzung)

Projektanalyse:
{analysis_results}

Generiere eine Liste von konkreten, umsetzbaren Optimierungsvorschlägen.
Jeder Vorschlag sollte eine kurze Beschreibung, die betroffenen Bereiche und eine Empfehlung zur Umsetzung enthalten.
"""

WORKFLOW_GENERATION_PROMPT = """
Basierend auf der folgenden Projektanalyse, generiere einen Workflow für die Automatisierung von Projektaufgaben.
Der Workflow sollte projektspezifische Schritte und Prozesse definieren.

Projektanalyse:
{analysis_results}

Workflow-Anforderungen:
- Name: {workflow_name}
- Zweck: {workflow_purpose}
- Schritte: {workflow_steps}
- Trigger: {workflow_triggers}
- Ausgaben: {workflow_outputs}

Generiere den Python-Code für die Klasse `{workflow_name}Workflow` in der Datei `workflows/{workflow_name.lower()}_workflow.py`.
Der Workflow sollte eine execute() Methode haben, die die definierten Schritte ausführt.
"""


class PromptTemplates:
    """Sammlung von Prompt-Templates für verschiedene Aufgaben"""

    def __init__(self):
        self.templates = {
            "project_analysis": self._get_project_analysis_template(),
            "code_review": self._get_code_review_template(),
            "optimization_suggestions": self._get_optimization_template(),
            "test_generation": self._get_test_generation_template(),
            "documentation": self._get_documentation_template(),
            "security_analysis": self._get_security_analysis_template(),
            "deployment_plan": self._get_deployment_plan_template(),
            "chat_response": self._get_chat_response_template(),
        }

    def get_template(self, template_name: str, **kwargs) -> str:
        """Gibt einen Prompt-Template zurück"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' nicht gefunden")

        template = self.templates[template_name]
        return template.format(**kwargs)

    def _get_project_analysis_template(self) -> str:
        """Template für Projekt-Analyse"""
        return """
Du bist ein erfahrener Software-Architekt und Projekt-Analyst. Analysiere das folgende Projekt und erstelle eine umfassende Übersicht.

**Projekt-Informationen:**
- Name: {project_name}
- Pfad: {project_path}
- Dateien: {file_count}
- Zeilen Code: {lines_of_code}
- Dependencies: {dependency_count}

**Erkannte Technologien:**
{technologies}

**Erkannte Frameworks:**
{frameworks}

**API-Endpoints:**
{api_endpoints}

**Datenbank-Schema:**
{database_schema}

**Bitte erstelle eine Analyse mit folgenden Aspekten:**

1. **Projekt-Übersicht:**
   - Projekttyp und Hauptzweck
   - Architektur-Pattern
   - Technologie-Stack-Bewertung

2. **Code-Qualität:**
   - Stärken und Schwächen
   - Code-Organisation
   - Best Practices

3. **Performance-Bewertung:**
   - Potentielle Bottlenecks
   - Optimierungsmöglichkeiten
   - Skalierbarkeit

4. **Security-Analyse:**
   - Identifizierte Risiken
   - Sicherheitslücken
   - Empfohlene Maßnahmen

5. **Wartbarkeit:**
   - Code-Komplexität
   - Dokumentation
   - Test-Coverage

6. **Empfohlene Verbesserungen:**
   - Priorisierte Liste
   - Implementierungsaufwand
   - Erwarteter Nutzen

Antworte strukturiert und detailliert. Verwende Markdown-Formatierung für bessere Lesbarkeit.
"""

    def _get_code_review_template(self) -> str:
        """Template für Code-Review"""
        return """
Du bist ein Senior-Entwickler und führst ein Code-Review durch. Analysiere den folgenden Code und gib konstruktives Feedback.

**Code-Kontext:**
- Datei: {file_path}
- Funktion: {function_name}
- Framework: {framework}
- Sprache: {language}

**Code:**
```{language}
{code}
```

**Bitte bewerte folgende Aspekte:**

1. **Funktionalität:**
   - Korrektheit der Logik
   - Edge Cases
   - Fehlerbehandlung

2. **Code-Qualität:**
   - Lesbarkeit und Verständlichkeit
   - Namenskonventionen
   - Code-Duplikation

3. **Performance:**
   - Effizienz der Algorithmen
   - Speicherverbrauch
   - Optimierungsmöglichkeiten

4. **Best Practices:**
   - Framework-spezifische Konventionen
   - Design Patterns
   - SOLID-Prinzipien

5. **Security:**
   - Sicherheitslücken
   - Input-Validierung
   - Datenexposition

6. **Verbesserungsvorschläge:**
   - Konkrete Änderungen
   - Alternative Implementierungen
   - Refactoring-Empfehlungen

Gib spezifisches, konstruktives Feedback mit Code-Beispielen wo nötig.
"""

    def _get_optimization_template(self) -> str:
        """Template für Optimierungsvorschläge"""
        return """
Du bist ein Performance-Experte und Code-Optimierer. Analysiere das Projekt und erstelle konkrete Optimierungsvorschläge.

**Projekt-Kontext:**
- Typ: {project_type}
- Framework: {framework}
- Größe: {project_size}
- Performance-Issues: {performance_issues}

**Aktuelle Metriken:**
- Bundle-Größe: {bundle_size}
- Ladezeit: {load_time}
- Memory-Usage: {memory_usage}
- CPU-Usage: {cpu_usage}

**Bitte erstelle Optimierungsvorschläge für:**

1. **Frontend-Optimierungen:**
   - Bundle-Size-Reduktion
   - Lazy Loading
   - Caching-Strategien
   - Image-Optimierung

2. **Backend-Optimierungen:**
   - Datenbankabfragen
   - API-Performance
   - Caching
   - Async-Processing

3. **Code-Optimierungen:**
   - Algorithmus-Verbesserungen
   - Memory-Management
   - Code-Splitting
   - Dead Code Elimination

4. **Infrastruktur-Optimierungen:**
   - CDN-Nutzung
   - Compression
   - HTTP/2
   - Service-Worker

5. **Monitoring & Profiling:**
   - Performance-Metriken
   - Bottleneck-Identifikation
   - Continuous Monitoring

Für jeden Vorschlag:
- Beschreibung des Problems
- Konkrete Lösung
- Implementierungsaufwand (1-5)
- Erwarteter Impact (1-5)
- Code-Beispiele

Priorisiere die Vorschläge nach Impact/Aufwand-Verhältnis.
"""

    def _get_test_generation_template(self) -> str:
        """Template für Test-Generierung"""
        return """
Du bist ein Test-Experte und generierst umfassende Tests für das Projekt.

**Projekt-Kontext:**
- Framework: {framework}
- Test-Framework: {test_framework}
- Sprache: {language}
- Test-Coverage: {current_coverage}%

**Zu testende Komponenten:**
{components}

**Bitte generiere Tests für:**

1. **Unit-Tests:**
   - Alle öffentlichen Funktionen
   - Edge Cases
   - Error-Handling
   - Mocking-Strategien

2. **Integration-Tests:**
   - API-Endpoints
   - Datenbank-Interaktionen
   - Service-Integration
   - External-Dependencies

3. **End-to-End-Tests:**
   - User-Journeys
   - Critical-Paths
   - Cross-Browser-Testing
   - Performance-Tests

4. **Test-Utilities:**
   - Test-Fixtures
   - Helper-Functions
   - Mock-Objects
   - Test-Data

**Für jeden Test:**
- Test-Name (deskriptiv)
- Test-Description
- Setup/Teardown
- Assertions
- Code-Implementation

**Test-Struktur:**
```{language}
// Test-Beispiel
describe('ComponentName', () => {{
    beforeEach(() => {{
        // Setup
    }});
    
    it('should handle valid input', () => {{
        // Arrange
        // Act
        // Assert
    }});
    
    it('should handle edge cases', () => {{
        // Test edge cases
    }});
}});
```

Fokussiere auf:
- Hohe Test-Coverage
- Lesbare Tests
- Wartbare Test-Struktur
- Performance-Tests
"""

    def _get_documentation_template(self) -> str:
        """Template für Dokumentation"""
        return """
Du bist ein Technical Writer und erstellst umfassende Dokumentation für das Projekt.

**Projekt-Informationen:**
- Name: {project_name}
- Typ: {project_type}
- Framework: {framework}
- Zielgruppe: {target_audience}

**Bitte erstelle Dokumentation für:**

1. **README.md:**
   - Projekt-Beschreibung
   - Installation & Setup
   - Quick Start Guide
   - Usage Examples
   - Contributing Guidelines

2. **API-Dokumentation:**
   - Endpoint-Übersicht
   - Request/Response-Formate
   - Authentication
   - Error-Codes
   - Code-Beispiele

3. **Architektur-Dokumentation:**
   - System-Übersicht
   - Komponenten-Diagramm
   - Datenfluss
   - Design-Decisions
   - Deployment-Architecture

4. **Developer-Guide:**
   - Development-Setup
   - Code-Standards
   - Testing-Guide
   - Debugging-Tips
   - Performance-Best-Practices

5. **User-Guide:**
   - Feature-Übersicht
   - Step-by-Step-Anleitungen
   - Screenshots/Diagrams
   - FAQ
   - Troubleshooting

**Dokumentations-Standards:**
- Klare, präzise Sprache
- Code-Beispiele
- Screenshots wo nötig
- Aktuelle Informationen
- Suchbare Struktur

**Format:**
Verwende Markdown mit:
- Überschriften (H1-H6)
- Code-Blöcke mit Syntax-Highlighting
- Listen und Tabellen
- Links und Referenzen
- Emojis für bessere Lesbarkeit

Erstelle eine vollständige, professionelle Dokumentation.
"""

    def _get_security_analysis_template(self) -> str:
        """Template für Security-Analyse"""
        return """
Du bist ein Security-Experte und führst eine umfassende Sicherheitsanalyse durch.

**Projekt-Kontext:**
- Typ: {project_type}
- Framework: {framework}
- Dependencies: {dependency_count}
- API-Endpoints: {api_count}

**Identifizierte Vulnerabilities:**
{vulnerabilities}

**Bitte analysiere folgende Security-Aspekte:**

1. **Dependency-Security:**
   - Veraltete Packages
   - Bekannte Vulnerabilities
   - License-Compliance
   - Supply-Chain-Risiken

2. **Authentication & Authorization:**
   - Login-Mechanismen
   - Session-Management
   - Role-Based-Access
   - Password-Policies

3. **Input-Validation:**
   - SQL-Injection-Schutz
   - XSS-Prevention
   - CSRF-Protection
   - File-Upload-Security

4. **Data-Protection:**
   - Encryption-at-Rest
   - Encryption-in-Transit
   - PII-Handling
   - Data-Minimization

5. **API-Security:**
   - Rate-Limiting
   - Input-Sanitization
   - Error-Handling
   - CORS-Configuration

6. **Infrastructure-Security:**
   - HTTPS-Enforcement
   - Security-Headers
   - Container-Security
   - Network-Security

**Für jeden Bereich:**
- Aktuelle Sicherheitslage
- Identifizierte Risiken
- Konkrete Verbesserungen
- Implementierungs-Priorität
- Code-Beispiele

**Security-Score:**
Bewerte das Projekt auf einer Skala von 1-10 für:
- Overall Security
- Authentication
- Data Protection
- API Security
- Infrastructure

Erstelle einen detaillierten Security-Report mit konkreten Handlungsempfehlungen.
"""

    def _get_deployment_plan_template(self) -> str:
        """Template für Deployment-Plan"""
        return """
Du bist ein DevOps-Experte und erstellst einen umfassenden Deployment-Plan.

**Projekt-Kontext:**
- Typ: {project_type}
- Framework: {framework}
- Dependencies: {dependencies}
- Database: {database}
- Target-Environment: {environment}

**Bitte erstelle einen Deployment-Plan für:**

1. **Containerisierung:**
   - Dockerfile-Optimierung
   - Multi-Stage-Builds
   - Image-Size-Reduktion
   - Security-Best-Practices

2. **CI/CD-Pipeline:**
   - Build-Process
   - Testing-Integration
   - Code-Quality-Checks
   - Automated-Deployment

3. **Infrastructure-as-Code:**
   - Kubernetes-Manifests
   - Terraform-Scripts
   - Environment-Configuration
   - Resource-Management

4. **Monitoring & Logging:**
   - Application-Monitoring
   - Infrastructure-Monitoring
   - Log-Aggregation
   - Alerting-Setup

5. **Security & Compliance:**
   - Secrets-Management
   - Network-Security
   - Compliance-Checks
   - Security-Scanning

6. **Performance & Scalability:**
   - Load-Balancing
   - Auto-Scaling
   - Caching-Strategy
   - CDN-Configuration

**Deployment-Strategien:**
- Blue-Green-Deployment
- Rolling-Updates
- Canary-Releases
- Rollback-Strategien

**Für jeden Bereich:**
- Konkrete Implementierung
- Konfigurationsdateien
- Best-Practices
- Troubleshooting-Guide

**Timeline:**
Erstelle einen realistischen Deployment-Timeline mit:
- Vorbereitungsphase
- Testing-Phase
- Staging-Deployment
- Production-Deployment
- Post-Deployment-Monitoring

Erstelle einen production-ready Deployment-Plan mit allen notwendigen Komponenten.
"""

    def _get_chat_response_template(self) -> str:
        """Template für Chat-Antworten"""
        return """
Du bist ein KI-Projektmanager und hilfst bei der Projektentwicklung. Antworte hilfreich und konstruktiv.

**Projekt-Kontext:**
- Name: {project_name}
- Typ: {project_type}
- Framework: {framework}
- Aktueller Status: {project_status}

**User-Nachricht:**
{user_message}

**Verfügbare Informationen:**
- Analyse-Ergebnisse: {analysis_available}
- Test-Status: {test_status}
- Deployment-Status: {deployment_status}
- Optimierungen: {optimizations_available}

**Antworte als KI-Projektmanager:**
- Sei hilfreich und konstruktiv
- Gib konkrete, umsetzbare Ratschläge
- Verwende dein Wissen über das Projekt
- Stelle relevante Fragen wenn nötig
- Biete weitere Unterstützung an

**Antwort-Stil:**
- Professionell aber freundlich
- Strukturiert und übersichtlich
- Mit konkreten Beispielen
- Emojis für bessere Lesbarkeit
- Markdown-Formatierung

**Falls du nicht genug Informationen hast:**
- Frage nach mehr Details
- Erkläre was du brauchst
- Biete alternative Lösungsansätze

Antworte direkt und hilfreich auf die User-Nachricht.
"""

    def get_custom_template(self, task: str, context: Dict[str, Any]) -> str:
        """Erstellt einen benutzerdefinierten Template"""
        base_template = """
Du bist ein KI-Assistent für Software-Entwicklung. Führe die folgende Aufgabe aus:

**Aufgabe:** {task}

**Kontext:**
{context}

**Anforderungen:**
- Sei präzise und hilfreich
- Gib konkrete, umsetzbare Empfehlungen
- Verwende dein technisches Wissen
- Strukturiere deine Antwort übersichtlich
- Verwende Markdown-Formatierung

Antworte detailliert und professionell.
"""

        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])

        return base_template.format(task=task, context=context_str)

    def list_templates(self) -> List[str]:
        """Gibt alle verfügbaren Templates zurück"""
        return list(self.templates.keys())

    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Gibt Informationen über ein Template zurück"""
        if template_name not in self.templates:
            return {}

        template = self.templates[template_name]

        # Extrahiere Platzhalter
        import re

        placeholders = re.findall(r"\{(\w+)\}", template)

        return {
            "name": template_name,
            "description": self._get_template_description(template_name),
            "placeholders": placeholders,
            "length": len(template),
        }

    def _get_template_description(self, template_name: str) -> str:
        """Gibt eine Beschreibung des Templates zurück"""
        descriptions = {
            "project_analysis": "Umfassende Projekt-Analyse mit Architektur-Bewertung",
            "code_review": "Detailliertes Code-Review mit Verbesserungsvorschlägen",
            "optimization_suggestions": "Performance-Optimierungen und Best-Practices",
            "test_generation": "Generierung von Unit-, Integration- und E2E-Tests",
            "documentation": "Erstellung von technischer Dokumentation",
            "security_analysis": "Sicherheitsanalyse und Vulnerability-Assessment",
            "deployment_plan": "Deployment-Strategie und DevOps-Setup",
            "chat_response": "Kontextuelle Chat-Antworten als Projektmanager",
        }

        return descriptions.get(template_name, "Keine Beschreibung verfügbar")
