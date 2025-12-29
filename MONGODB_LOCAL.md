# Lokale MongoDB Installation & Setup

Diese Anleitung zeigt, wie du MongoDB lokal auf deinem System installierst und für MercuryBot konfigurierst - **keine Cloud-Dienste nötig!**

## Warum lokale MongoDB?

✅ **Kostenlos** - Keine Begrenzungen oder Kosten
✅ **Volle Kontrolle** - Daten bleiben auf deinem Server
✅ **Schneller** - Keine Netzwerk-Latenz
✅ **Offline-fähig** - Funktioniert ohne Internet

---

## Schnellstart

### Automatisches Setup (Linux/macOS):

```bash
chmod +x setup_mongodb.sh
./setup_mongodb.sh
```

Das interaktive Script führt dich durch die Installation!

---

## Manuelle Installation

### Linux (Ubuntu/Debian)

#### 1. MongoDB installieren

```bash
# System aktualisieren
sudo apt update

# MongoDB importieren
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Repository hinzufügen
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Installieren
sudo apt update
sudo apt install -y mongodb-org

# Starten und auto-start aktivieren
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### 2. Status überprüfen

```bash
sudo systemctl status mongod
```

Erwartete Ausgabe:
```
● mongod.service - MongoDB Database Server
   Loaded: loaded
   Active: active (running)
```

#### 3. Verbindung testen

```bash
mongosh
```

Du solltest die MongoDB Shell sehen:
```
Current Mongosh Log ID:	...
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true
Using MongoDB:		7.0.x
```

---

### macOS

#### Mit Homebrew:

```bash
# Homebrew installieren (falls nicht vorhanden)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# MongoDB installieren
brew tap mongodb/brew
brew install mongodb-community@7.0

# Starten
brew services start mongodb-community@7.0

# Status prüfen
brew services list | grep mongodb
```

#### Verbindung testen:

```bash
mongosh
```

---

### Windows

#### 1. Download & Installation:

1. Gehe zu [MongoDB Download Center](https://www.mongodb.com/try/download/community)
2. Wähle **Windows** und **MSI**
3. Lade herunter und führe den Installer aus
4. Wähle **Complete** Installation
5. Installiere **MongoDB Compass** (GUI) mit

#### 2. Als Service einrichten:

Im Installer:
- ✅ Install MongoDB as a Service
- ✅ Run service as Network Service user
- Data Directory: `C:\Program Files\MongoDB\Server\7.0\data`
- Log Directory: `C:\Program Files\MongoDB\Server\7.0\log`

#### 3. Testen:

```cmd
# CMD oder PowerShell öffnen
mongosh
```

---

## Datenbank & User erstellen

### 1. MongoDB Shell öffnen:

```bash
mongosh
```

### 2. Admin-Datenbank auswählen:

```javascript
use admin
```

### 3. Admin-User erstellen:

```javascript
db.createUser({
  user: "admin",
  pwd: "IhrSicheresPasswort123",  // ÄNDERN!
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})
```

Ausgabe:
```
{ ok: 1 }
```

### 4. MercuryBot-Datenbank erstellen:

```javascript
use mercurybot
```

### 5. Bot-User mit Zugriffsrechten erstellen:

```javascript
db.createUser({
  user: "mercurybot",
  pwd: "BotPasswort456",  // ÄNDERN!
  roles: [
    { role: "readWrite", db: "mercurybot" }
  ]
})
```

### 6. Shell beenden:

```javascript
exit
```

---

## Authentication aktivieren

### Linux/macOS:

#### 1. Konfigurationsdatei bearbeiten:

```bash
sudo nano /etc/mongod.conf
```

#### 2. Security-Abschnitt aktivieren:

Finde die Zeile `#security:` und ändere zu:

```yaml
security:
  authorization: enabled
```

#### 3. MongoDB neu starten:

```bash
sudo systemctl restart mongod
```

### Windows:

#### 1. Konfigurationsdatei öffnen:

```
C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg
```

#### 2. Security-Abschnitt hinzufügen/ändern:

```yaml
security:
  authorization: enabled
```

#### 3. MongoDB-Service neu starten:

**Dienste** (services.msc) → **MongoDB Server** → Rechtsklick → **Neu starten**

---

## Connection String erstellen

### Basis-Format:

```
mongodb://username:password@host:port/database
```

### Für MercuryBot:

```
mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot
```

### Mit allen Optionen:

```
mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot?authSource=mercurybot
```

---

## MercuryBot konfigurieren

### 1. `.env` bearbeiten:

```bash
nano .env
```

### 2. Connection String eintragen:

```env
DB_CONNECTION_STRING=mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot
```

**Wichtig:**
- Ersetze `mercurybot` und `BotPasswort456` mit deinen Credentials
- Ändere `localhost` zu deiner Server-IP falls remote

### 3. Bot starten und testen:

```bash
python main.py
```

Erwartete Ausgabe:
```
INFO - Connected to MongoDB successfully
INFO - Modules: epic, steam, gog, psplus, primegaming
```

---

## Verbindung testen

### Mit mongosh:

```bash
mongosh "mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot"
```

### Mit Python:

```python
from pymongo import MongoClient

# Verbinden
client = MongoClient('mongodb://mercurybot:BotPassword456@localhost:27017/mercurybot')

# Testen
db = client.mercurybot
print("Datenbanken:", client.list_database_names())
print("Collections:", db.list_collection_names())

# Verbindung schließen
client.close()
```

Ausgabe:
```
Datenbanken: ['admin', 'config', 'local', 'mercurybot']
Collections: []  # Leer beim ersten Start
```

---

## Firewall konfigurieren (Optional)

### Remote-Zugriff erlauben:

⚠️ **Nur wenn der Bot auf einem anderen Server läuft!**

#### Linux (UFW):

```bash
# Port für MongoDB öffnen
sudo ufw allow 27017/tcp

# Oder nur von spezifischer IP:
sudo ufw allow from YOUR_BOT_IP to any port 27017
```

#### Bind IP ändern:

```bash
sudo nano /etc/mongod.conf
```

Ändere:
```yaml
net:
  port: 27017
  bindIp: 0.0.0.0  # Alle IPs (VORSICHT!)
  # bindIp: 127.0.0.1,192.168.1.100  # Spezifische IPs
```

Neustart:
```bash
sudo systemctl restart mongod
```

---

## Backup & Restore

### Backup erstellen:

```bash
# Komplettes Backup
mongodump --uri="mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot" --out=/backup/mongo

# Spezifische Datenbank
mongodump --db=mercurybot --out=/backup/mongo
```

### Backup wiederherstellen:

```bash
mongorestore --uri="mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot" /backup/mongo
```

### Automatisches Backup (Cronjob):

```bash
# Cronjob erstellen
crontab -e

# Tägliches Backup um 3 Uhr morgens
0 3 * * * mongodump --db=mercurybot --out=/backup/mongo/$(date +\%Y\%m\%d)
```

---

## Monitoring & Verwaltung

### MongoDB Compass (GUI):

1. [Download MongoDB Compass](https://www.mongodb.com/try/download/compass)
2. Installieren und öffnen
3. Connection String eingeben:
   ```
   mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot
   ```
4. Verbinden → Datenbanken visuell verwalten

### Via Command Line:

```bash
# Verbinden
mongosh "mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot"

# Datenbanken anzeigen
show dbs

# Collections anzeigen
show collections

# Dokumente zählen
db.discord.countDocuments()

# Beispiel-Dokument anzeigen
db.discord.findOne()

# Alle Dokumente
db.discord.find()
```

---

## Performance-Optimierung

### 1. Indizes erstellen:

```javascript
// In mongosh
use mercurybot

// Index für schnellere Server-Suche
db.discord.createIndex({ "server": 1 })

// Index für Deals
db.epic.createIndex({ "title": 1 })
db.steam.createIndex({ "title": 1 })
```

### 2. Speicher optimieren:

```bash
sudo nano /etc/mongod.conf
```

```yaml
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1  # 1GB Cache (anpassen nach RAM)
```

---

## Troubleshooting

### MongoDB startet nicht:

```bash
# Logs überprüfen
sudo journalctl -u mongod -n 50

# Oder direkt:
sudo tail -f /var/log/mongodb/mongod.log
```

**Häufige Probleme:**

1. **Port bereits in Benutzung:**
   ```bash
   sudo lsof -i :27017
   sudo kill -9 PID
   ```

2. **Datei-Permissions:**
   ```bash
   sudo chown -R mongodb:mongodb /var/lib/mongodb
   sudo chown -R mongodb:mongodb /var/log/mongodb
   ```

3. **Lock-File:**
   ```bash
   sudo rm /var/lib/mongodb/mongod.lock
   sudo systemctl restart mongod
   ```

### Verbindung schlägt fehl:

**Check 1: MongoDB läuft?**
```bash
sudo systemctl status mongod
```

**Check 2: Port offen?**
```bash
sudo netstat -tulpn | grep 27017
```

**Check 3: Credentials korrekt?**
```bash
mongosh "mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot"
```

### Authentication-Fehler:

```bash
# In mongosh als Admin
use admin
db.auth("admin", "IhrAdminPasswort")

# User-Rechte prüfen
use mercurybot
db.getUsers()
```

---

## Migration von MongoDB Atlas

### 1. Daten exportieren (aus Atlas):

```bash
mongodump --uri="mongodb+srv://user:pass@cluster.mongodb.net/mercurybot" --out=/tmp/atlas-backup
```

### 2. In lokale DB importieren:

```bash
mongorestore --uri="mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot" /tmp/atlas-backup/mercurybot
```

### 3. Connection String in `.env` ändern:

**Alt (Atlas):**
```env
DB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/mercurybot
```

**Neu (Lokal):**
```env
DB_CONNECTION_STRING=mongodb://mercurybot:BotPasswort456@localhost:27017/mercurybot
```

### 4. Bot neu starten:

```bash
python main.py
```

---

## Sicherheitsempfehlungen

1. ✅ **Starke Passwörter** verwenden (min. 16 Zeichen)
2. ✅ **Firewall** aktivieren (nur notwendige Ports öffnen)
3. ✅ **Bind IP** einschränken (nicht 0.0.0.0 in Production)
4. ✅ **Regelmäßige Backups** erstellen
5. ✅ **Updates** installieren
6. ❌ **Keine Root-User** für den Bot
7. ❌ **Kein Default-Port** 27017 (ändern zu custom port)

---

## Zusammenfassung

### Quick Setup (TL;DR):

```bash
# 1. MongoDB installieren
sudo apt install -y mongodb-org

# 2. Starten
sudo systemctl start mongod

# 3. User erstellen
mongosh
use admin
db.createUser({user: "admin", pwd: "PASSWORT", roles: ["userAdminAnyDatabase"]})
use mercurybot
db.createUser({user: "mercurybot", pwd: "BOTPW", roles: [{role: "readWrite", db: "mercurybot"}]})
exit

# 4. Auth aktivieren
sudo nano /etc/mongod.conf  # security: authorization: enabled
sudo systemctl restart mongod

# 5. .env konfigurieren
DB_CONNECTION_STRING=mongodb://mercurybot:BOTPW@localhost:27017/mercurybot

# 6. Bot starten
python main.py
```

**Fertig!** 🎉

---

## Hilfreiche Links

- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [MongoDB University](https://university.mongodb.com/) (Kostenlose Kurse)
- [MongoDB Community Forum](https://www.mongodb.com/community/forums/)
- [Install MongoDB on Ubuntu](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
