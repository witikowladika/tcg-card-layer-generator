# Installation & Troubleshooting

## Problem: "no module named pil" oder "ModuleNotFoundError: No module named 'PIL'"

### Lösung 1: Dependencies installieren

Öffne PowerShell oder Command Prompt **im Projektverzeichnis** und führe aus:

```powershell
# Stelle sicher, dass du im richtigen Verzeichnis bist
cd "C:\Users\witik\OneDrive\Dokumente\Freizeit und Wünsche\TCG Cards\TCG Backside Generator"

# Installiere alle Dependencies
python -m pip install -r requirements.txt

# Oder einzeln installieren:
python -m pip install Pillow>=10.0.0
python -m pip install numpy>=1.24.0
```

### Lösung 2: Prüfe welche Python-Version du verwendest

```powershell
# Zeige Python-Pfad und Version
python --version
where python

# Prüfe ob Pillow installiert ist
python -m pip list | findstr Pillow
```

### Lösung 3: Virtuelle Umgebung verwenden (empfohlen)

```powershell
# Erstelle virtuelle Umgebung
python -m venv venv

# Aktiviere sie (PowerShell)
.\venv\Scripts\Activate.ps1

# Falls Fehler bei Activation: ExecutionPolicy setzen
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Installiere Dependencies
pip install -r requirements.txt

# Führe Skript aus
python src\main.py
```

### Lösung 4: Prüfe ob das Skript richtig ausgeführt wird

**Wichtig:** Das Skript muss aus dem Projekt-Root-Verzeichnis ausgeführt werden!

```powershell
# Im Projektverzeichnis
cd "C:\Users\witik\OneDrive\Dokumente\Freizeit und Wünsche\TCG Cards\TCG Backside Generator"

# Dann Skript ausführen
python src\main.py
```

Oder direkt mit vollständigem Pfad:

```powershell
python "C:\Users\witik\OneDrive\Dokumente\Freizeit und Wünsche\TCG Cards\TCG Backside Generator\src\main.py"
```

### Lösung 5: Wenn nichts hilft - Neuinstallation

```powershell
# Deinstalliere alte Version
python -m pip uninstall Pillow

# Installiere neu
python -m pip install --upgrade Pillow numpy
```

## Verwendung nach Installation

1. Lege dein Base-Artwork als `input/card_base.png` ab
2. Führe aus: `python src\main.py`
3. Oder mit Theme: `python src\main.py fire`

Die generierten Layer findest du in `output/layers/`

