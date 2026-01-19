# GitHub Repository Setup - Schritt für Schritt

Diese Anleitung führt dich durch den kompletten Prozess, um dieses Projekt auf GitHub hochzuladen.

## Schritt 1: Repository auf GitHub erstellen

1. Gehe zu [github.com](https://github.com) und logge dich ein
2. Klicke auf das **"+"** Symbol oben rechts → **"New repository"**
3. Fülle die Felder aus:
   - **Repository name**: `tcg-card-layer-generator` (oder einen Namen deiner Wahl)
   - **Description**: "Professional Python tool to generate print-ready layers for trading cards"
   - **Visibility**: Public oder Private (deine Wahl)
   - **WICHTIG**: Lasse "Initialize this repository with a README" **NICHT** angehakt!
   - **WICHTIG**: Lasse "Add .gitignore" und "Choose a license" auf "None"
4. Klicke auf **"Create repository"**

## Schritt 2: Repository-URL kopieren

Nach dem Erstellen zeigt GitHub dir eine URL an, z.B.:
- HTTPS: `https://github.com/DEIN-USERNAME/tcg-card-layer-generator.git`
- SSH: `git@github.com:DEIN-USERNAME/tcg-card-layer-generator.git`

**Kopiere diese URL** - du brauchst sie im nächsten Schritt!

## Schritt 3: Git im lokalen Projekt initialisieren

Öffne eine PowerShell oder Command Prompt in diesem Verzeichnis und führe aus:

```bash
# Git initialisieren
git init

# Alle Dateien zum Staging hinzufügen
git add .

# Ersten Commit erstellen
git commit -m "Initial commit: TCG Card Layer Generator"

# Branch auf 'main' umbenennen (falls nötig)
git branch -M main

# GitHub Repository als Remote hinzufügen
# ERSETZE 'DEIN-USERNAME' und 'tcg-card-layer-generator' mit deinen Werten!
git remote add origin https://github.com/DEIN-USERNAME/tcg-card-layer-generator.git

# Dateien hochladen
git push -u origin main
```

## Schritt 4: Authentifizierung

Bei `git push` wirst du möglicherweise nach deinem GitHub-Benutzernamen und Passwort gefragt:

- **Username**: Dein GitHub-Benutzername
- **Password**: Benutze ein **Personal Access Token** (kein normales Passwort!)
  - Siehe Schritt 5, wie du ein Token erstellst

## Schritt 5: Personal Access Token erstellen (falls nötig)

Falls du noch kein Token hast:

1. Gehe zu GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Klicke auf **"Generate new token"** → **"Generate new token (classic)"**
3. Gib dem Token einen Namen (z.B. "TCG Card Generator")
4. Wähle Scopes: **`repo`** (vollständiger Zugriff auf Repositories)
5. Klicke auf **"Generate token"**
6. **KOPIERE DEN TOKEN SOFORT** - er wird nur einmal angezeigt!
7. Verwende diesen Token als Passwort bei `git push`

## Alternative: GitHub CLI verwenden

Falls du die GitHub CLI installiert hast:

```bash
# Bei GitHub einloggen
gh auth login

# Repository erstellen und pushen (alles in einem!)
gh repo create tcg-card-layer-generator --public --source=. --remote=origin --push
```

## Troubleshooting

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/DEIN-USERNAME/tcg-card-layer-generator.git
```

### "Updates were rejected"
```bash
# Falls GitHub ein README erstellt hat, hole es zuerst:
git pull origin main --allow-unrelated-histories
# Dann merge die Änderungen und pushe erneut
git push -u origin main
```

### Passwort wird nicht akzeptiert
- Verwende ein **Personal Access Token** statt deinem GitHub-Passwort
- Oder nutze SSH-Keys (siehe GitHub-Dokumentation)

## Fertig! 🎉

Nach erfolgreichem `git push` ist dein Projekt auf GitHub verfügbar!

Du findest es unter: `https://github.com/DEIN-USERNAME/tcg-card-layer-generator`

## Zukünftige Updates

Wenn du Änderungen vorgenommen hast:

```bash
git add .
git commit -m "Beschreibung deiner Änderungen"
git push
```

