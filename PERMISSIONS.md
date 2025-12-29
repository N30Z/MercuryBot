# Discord Bot Permissions Guide

MercuryBot benötigt spezifische Discord-Berechtigungen, um alle Features korrekt zu nutzen.

## Erforderliche Berechtigungen

### 📋 Übersicht

| Berechtigung | Erforderlich | Zweck |
|--------------|--------------|-------|
| **View Channels** | ✅ Ja | Kanäle sehen und auf Nachrichten reagieren |
| **Send Messages** | ✅ Ja | Benachrichtigungen senden |
| **Embed Links** | ✅ Ja | Rich Embeds für formatierte Notifications |
| **Attach Files** | ✅ Ja | Bilder/GIFs von Spielen anhängen |
| **Add Reactions** | ✅ Ja | Reaktionen für Rollen-System hinzufügen |
| **Manage Roles** | ✅ Ja | Plattform-Rollen erstellen und zuweisen |
| **Read Message History** | ✅ Ja | Reaktions-Events verarbeiten |
| **Use Application Commands** | ✅ Ja | Slash-Commands (`/settings`, `/deals`, etc.) |

---

## Detaillierte Erklärung

### 🔹 View Channels (Kanäle ansehen)
**Berechtigung:** `VIEW_CHANNEL` (1024)

**Wofür:**
- Bot muss Kanäle sehen können
- Benachrichtigungskanal identifizieren
- Auf konfigurierte Kanäle zugreifen

**Ohne diese:**
- Bot kann keine Nachrichten senden
- `/settings` funktioniert nicht

---

### 🔹 Send Messages (Nachrichten senden)
**Berechtigung:** `SEND_MESSAGES` (2048)

**Wofür:**
- Spielbenachrichtigungen senden
- Test-Notifications (`/testnotify`)
- Fehlermeldungen anzeigen

**Ohne diese:**
- Hauptfunktion des Bots funktioniert nicht
- Keine Benachrichtigungen möglich

---

### 🔹 Embed Links (Einbettungen senden)
**Berechtigung:** `EMBED_LINKS` (16384)

**Wofür:**
- Rich Embeds für formatierte Benachrichtigungen
- Strukturierte Darstellung mit Feldern, Farben
- Bessere Lesbarkeit

**Ohne diese:**
- Nur Plain-Text Nachrichten möglich
- Keine schönen Game-Embeds

---

### 🔹 Attach Files (Dateien anhängen)
**Berechtigung:** `ATTACH_FILES` (32768)

**Wofür:**
- GIF/Bilder von Spielen anhängen
- Visuelle Darstellung der Free Games
- Image Attachments in Notifications

**Ohne diese:**
- Keine Bilder in Benachrichtigungen
- Nur Text-basierte Notifications

---

### 🔹 Add Reactions (Reaktionen hinzufügen)
**Berechtigung:** `ADD_REACTIONS` (64)

**Wofür:**
- Plattform-Emojis zu Notifications hinzufügen
- Reaktions-Rollen-System ermöglichen
- User können durch Reaktion Rollen bekommen

**Ohne diese:**
- Kein Reaktions-Rollen-System
- User müssen `/roles` verwenden

---

### 🔹 Manage Roles (Rollen verwalten)
**Berechtigung:** `MANAGE_ROLES` (268435456)

**Wofür:**
- Plattform-Rollen erstellen (z.B. "Epic Games Games")
- Rollen bei Reaktion zuweisen
- Rollen bei Reaktionsentfernung entziehen

**Ohne diese:**
- `/roles` Command funktioniert nicht
- Reaktions-Rollen-System nicht nutzbar
- Manuelles Rollen-Management nötig

---

### 🔹 Read Message History (Nachrichtenverlauf lesen)
**Berechtigung:** `READ_MESSAGE_HISTORY` (65536)

**Wofür:**
- Reaktions-Events auf älteren Nachrichten verarbeiten
- `on_raw_reaction_add/remove` Events
- Historische Reaktionen erkennen

**Ohne diese:**
- Reaktionen auf alte Nachrichten funktionieren nicht
- Nur Reaktionen auf neue Nachrichten erkannt

---

### 🔹 Use Application Commands (Slash-Commands)
**Berechtigung:** Automatisch mit Bot-Scope

**Wofür:**
- `/settings` - Bot konfigurieren
- `/roles` - Reaktions-Rollen einrichten
- `/testnotify` - Test-Benachrichtigungen
- `/deals` - Aktuelle Deals anzeigen
- `/feedback` - Feedback senden

**Ohne diese:**
- Keine Slash-Commands verfügbar
- Bot nicht konfigurierbar

---

## Permissions Integer

**Alle benötigten Berechtigungen:** `534723885120`

**Berechnung:**
```
1024        (VIEW_CHANNEL)
+ 2048      (SEND_MESSAGES)
+ 16384     (EMBED_LINKS)
+ 32768     (ATTACH_FILES)
+ 64        (ADD_REACTIONS)
+ 65536     (READ_MESSAGE_HISTORY)
+ 268435456 (MANAGE_ROLES)
+ 534240256 (weitere Standard-Berechtigungen)
= 534723885120
```

---

## Bot-Einladungs-URL

### Option 1: Mit allen erforderlichen Berechtigungen

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=534723885120&scope=bot%20applications.commands
```

**Ersetze `YOUR_CLIENT_ID`** mit deiner Application ID aus dem [Discord Developer Portal](https://discord.com/developers/applications)

### Option 2: Administrator (Nicht empfohlen)

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

⚠️ **Warnung:** Administrator-Berechtigung gibt dem Bot volle Kontrolle. Nur für Testzwecke verwenden!

---

## Berechtigungen einrichten

### Beim Einladen:

1. Öffne die Einladungs-URL
2. Wähle deinen Server
3. Überprüfe die angeforderten Berechtigungen
4. Klicke auf "Autorisieren"

### Nach dem Einladen:

Berechtigungen können jederzeit angepasst werden:

1. **Server-Settings** → **Rollen**
2. Finde die **Bot-Rolle** (automatisch erstellt)
3. Aktiviere benötigte Berechtigungen
4. Speichern

### Kanal-spezifische Berechtigungen:

Für den Benachrichtigungskanal:

1. **Kanal-Settings** → **Berechtigungen**
2. Klicke auf **+** bei "Rollen/Mitglieder"
3. Wähle die **Bot-Rolle**
4. Aktiviere:
   - ✅ Kanäle ansehen
   - ✅ Nachrichten senden
   - ✅ Einbettungen senden
   - ✅ Dateien anhängen
   - ✅ Reaktionen hinzufügen
5. Speichern

---

## Fehlerbehebung

### Bot sendet keine Nachrichten

**Prüfe:**
1. Hat der Bot "Nachrichten senden" im Zielkanal?
2. Hat der Bot "Kanäle ansehen" im Zielkanal?
3. Ist der Kanal in `/settings` konfiguriert?

**Lösung:**
```
/settings → Set channel → Kanal auswählen
```

### Keine Bilder in Benachrichtigungen

**Prüfe:**
- "Dateien anhängen" Berechtigung
- "Einbettungen senden" Berechtigung

### Reaktions-Rollen funktionieren nicht

**Prüfe:**
1. "Reaktionen hinzufügen" Berechtigung
2. "Rollen verwalten" Berechtigung
3. **Wichtig:** Bot-Rolle muss **über** den zu vergebenden Rollen sein!

**Lösung:**
1. Server-Settings → Rollen
2. Ziehe die Bot-Rolle nach **oben**
3. Bot-Rolle muss höher sein als "Epic Games Games" etc.

### Commands nicht verfügbar

**Prüfe:**
1. Bot wurde mit `applications.commands` Scope eingeladen
2. Warte 5-10 Minuten nach Einladung
3. Kicke und lade Bot erneut ein

---

## Sicherheitshinweise

### ✅ Empfohlene Praxis:

- **Nur erforderliche Berechtigungen** erteilen
- **Keine Administrator-Rechte** geben
- Bot-Rolle **über Plattform-Rollen**, aber **unter Admin-Rollen**
- Berechtigungen regelmäßig überprüfen

### ⚠️ Zu vermeiden:

- ❌ Administrator-Berechtigung (außer zum Testen)
- ❌ Berechtigungen in allen Kanälen (nur wo nötig)
- ❌ Bot über Server-Owner-Rolle platzieren

---

## Überprüfung der Berechtigungen

### Via Discord:

1. Server-Settings → Rollen
2. Finde Bot-Rolle
3. Überprüfe aktivierte Berechtigungen

### Via Bot:

Der Bot prüft automatisch Berechtigungen beim `/settings` Command:

```
/settings → Set channel → Kanal auswählen
```

Bei fehlenden Berechtigungen zeigt der Bot eine Fehlermeldung mit Details.

---

## Minimale Berechtigungen

Für einen **Minimal-Setup** (nur Benachrichtigungen, keine Reaktions-Rollen):

**Erforderlich:**
- View Channels
- Send Messages
- Embed Links
- Attach Files
- Use Application Commands

**Permissions Integer:** `68672`

**Einladungs-URL:**
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=68672&scope=bot%20applications.commands
```

⚠️ **Hinweis:** Ohne "Add Reactions" und "Manage Roles" funktioniert das Reaktions-Rollen-System nicht!

---

## Zusammenfassung

**Standard-Setup (empfohlen):**
```
Permissions Integer: 534723885120
Scope: bot applications.commands
```

**Features:**
- ✅ Benachrichtigungen mit Bildern
- ✅ Reaktions-Rollen-System
- ✅ Alle Slash-Commands
- ✅ Automatische Rollenvergabe

**Einladungs-URL:**
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=534723885120&scope=bot%20applications.commands
```

Ersetze `YOUR_CLIENT_ID` mit deiner Bot Application ID!
