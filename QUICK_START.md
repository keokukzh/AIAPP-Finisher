# ⚡ Quick Start Guide - 5 Minuten zum ersten Ergebnis

## ✅ System Status Prüfen

### Backend Status:
```powershell
curl http://localhost:8000/status
```

**Erwartetes Ergebnis (Initial):**
```json
{
  "status": "running",
  "current_project": null,            ← Normal! Noch nichts analysiert
  "analysis_available": false         ← Normal! Noch keine Daten
}
```

---

## 🚀 Erste Analyse in 4 Schritten

### Schritt 1: Öffne Modern UI
```
http://localhost:8501
```

### Schritt 2: Navigation
- Klicke **"🧠 Project Analysis"** in der linken Sidebar

### Schritt 3: Projekt eingeben
Gib in das Textfeld ein:
```
.
```
(Punkt = aktuelles Verzeichnis)

ODER den vollen Pfad:
```
C:/Users/keoku/Desktop/APP-Finisher
```

### Schritt 4: Analyse starten
- Klicke **"🚀 Analyze"** Button
- Warte ~30-60 Sekunden
- Ergebnisse erscheinen automatisch!

---

## 🎯 Nach der Analyse

### Backend Status wird jetzt zeigen:
```powershell
curl http://localhost:8000/status
```

```json
{
  "status": "running",
  "current_project": "C:/Users/keoku/Desktop/APP-Finisher",  ← JETZT GESETZT!
  "analysis_available": true                                  ← JETZT TRUE!
}
```

### Dashboard zeigt:
- ✅ Anzahl der Dateien
- ✅ Erkannte Sprachen (Python, JavaScript, etc.)
- ✅ Frameworks (FastAPI, Streamlit, etc.)
- ✅ Dependencies
- ✅ Code Quality Score

---

## 🔍 Test-Befehle

### 1. Prüfe Backend:
```powershell
curl http://localhost:8000/status
```

### 2. Prüfe verfügbare Endpunkte:
```powershell
curl http://localhost:8000/ 
```

### 3. Prüfe Modelle:
```powershell
curl http://localhost:8000/models
```

### 4. Prüfe Claude-Flow:
```powershell
curl http://localhost:8000/api/claude-flow/health
```

### 5. Manuelle Analyse (über API):
```powershell
curl -X POST http://localhost:8000/api/analyze-project `
  -H "Content-Type: application/json" `
  -d '{"project_path": "."}'
```

---

## 📊 Erwartete Zeiten

| Aktion | Dauer |
|--------|-------|
| Backend Start | 5-10 Sekunden |
| UI Start | 3-5 Sekunden |
| Kleine Analyse (<100 Dateien) | 30-60 Sekunden |
| Mittlere Analyse (100-500 Dateien) | 1-2 Minuten |
| Große Analyse (>500 Dateien) | 2-5 Minuten |

---

## ❌ Troubleshooting

### "analysis_available: false"
✅ **Normal!** Das bedeutet nur, dass noch keine Analyse durchgeführt wurde.
- **Lösung**: Gehe zur UI und analysiere ein Projekt (siehe oben)

### "Backend not responding"
- **Check**: Ist ein Python-Fenster geöffnet mit "Uvicorn running"?
- **Lösung**: Führe aus: `start_production.bat`

### "UI lädt nicht"
- **Check**: Ist port 8501 frei?
- **Lösung**: Führe aus: `stop.bat` dann `start_production.bat`

### "Analysis failed"
- **Check**: Ist der Projekt-Pfad gültig?
- **Lösung**: Versuche `.` für das aktuelle Verzeichnis

---

## 🎉 Success Checklist

Nach erfolgreicher Analyse sollten Sie sehen:

- ✅ Backend Status: `"status": "running"`
- ✅ Current Project: `"current_project": "..."`
- ✅ Analysis Available: `"analysis_available": true`
- ✅ Dashboard zeigt Metriken
- ✅ Sprachen und Frameworks erkannt
- ✅ Code Quality Score angezeigt

---

## 🚀 Nächste Schritte

1. ✅ **Verschiedene Projekte analysieren**
   - Probiere verschiedene Pfade
   - Vergleiche Ergebnisse

2. ✅ **Settings erkunden**
   - Wähle verschiedene AI-Modelle
   - Konfiguriere Einstellungen

3. ✅ **Claude-Flow testen**
   - Besuche `/api/claude-flow/health`
   - Teste Swarm-Features

4. ✅ **Berichte exportieren**
   - Finde Berichte in `analysis_output/`
   - Teile mit deinem Team

---

## 💡 Pro-Tips

1. **Schnelle Analyse**: Benutze `.` für das aktuelle Verzeichnis
2. **Große Projekte**: Erste Analyse dauert länger
3. **Caching**: Zweite Analyse ist schneller
4. **Browser-Refresh**: `Ctrl+R` zum UI neu laden
5. **Logs ansehen**: Schaue in die Backend/UI Terminal-Fenster

---

## 📞 Need Help?

- **Features Guide**: `UI_FEATURES_GUIDE.md`
- **Production Guide**: `PRODUCTION_READY.md`
- **Architecture**: `CLAUDE.md`
- **Status**: Check `http://localhost:8000/docs`

---

**Los geht's! 🚀**
Öffne jetzt: **http://localhost:8501**

