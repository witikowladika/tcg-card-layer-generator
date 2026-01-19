# 🚀 Quick Start: Projekt auf GitHub hochladen

## Option 1: Mit GitHub CLI (einfachste Methode)

Falls du GitHub CLI installiert hast:

```bash
# 1. Bei GitHub einloggen (falls noch nicht geschehen)
gh auth login

# 2. Repository erstellen und pushen (alles automatisch!)
gh repo create tcg-card-layer-generator --public --source=. --remote=origin --push
```

Fertig! 🎉

---

## Option 2: Manuell (Schritt für Schritt)

### 1️⃣ Repository auf GitHub erstellen

1. Gehe zu https://github.com/new
2. **Repository name**: `tcg-card-layer-generator`
3. **WICHTIG**: Lasse alle Checkboxen **leer** (kein README, kein .gitignore, keine Lizenz)
4. Klicke auf **"Create repository"**
5. **Kopiere die URL** die GitHub anzeigt (z.B. `https://github.com/DEIN-USERNAME/tcg-card-layer-generator.git`)

### 2️⃣ Im Projektverzeichnis ausführen

Öffne PowerShell in diesem Ordner und führe aus:

```powershell
# Git initialisieren
git init

# Alle Projektdateien hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit: TCG Card Layer Generator"

# Branch auf 'main' umbenennen
git branch -M main

# GitHub Repository verbinden (ERSETZE die URL!)
git remote add origin https://github.com/DEIN-USERNAME/tcg-card-layer-generator.git

# Dateien hochladen
git push -u origin main
```

### 3️⃣ Bei Authentifizierung

Wenn nach Benutzername/Passwort gefragt wird:
- **Username**: Dein GitHub-Benutzername
- **Password**: **Personal Access Token** (nicht dein GitHub-Passwort!)

**Token erstellen:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → Name: `tcg-generator`
3. Scope: **`repo`** auswählen
4. "Generate token" → **Token sofort kopieren!**
5. Token als Passwort verwenden

---

## ✅ Fertig!

Dein Projekt ist jetzt auf GitHub verfügbar!

**Prüfen:** `https://github.com/DEIN-USERNAME/tcg-card-layer-generator`

---

## 📝 Zukünftige Updates

Wenn du Änderungen gemacht hast:

```bash
git add .
git commit -m "Beschreibung der Änderungen"
git push
```

