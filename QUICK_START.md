# MercuryBot - Quick Start Guide

Get MercuryBot up and running in minutes! 🚀

## Prerequisites

- **Python 3.10+** installed
- **MongoDB** database (free tier available at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))
- **Discord Bot Token** ([Create one here](https://discord.com/developers/applications))
- **Git** (to clone the repository)

---

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/MercuryBot.git
cd MercuryBot
```

---

## Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

---

## Step 3: Configure Environment

### Create `.env` file

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

### Minimal Required Configuration

Edit `.env` with these **required** settings:

```env
# Database (REQUIRED)
DB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/

# Discord Bot Token (REQUIRED)
DISCORD_TOKEN_LIVE=your_discord_bot_token_here

# Debug Mode (set to False for production)
DEBUG=False

# Admin Account (your Discord User ID for web interface access)
DISCORD_ADMIN_ACC=your_discord_user_id

# Web Interface (optional, defaults shown)
WEB_PORT=5000
WEB_HOST=0.0.0.0
FLASK_SECRET_KEY=change-this-to-random-secret-key
```

### Optional: Social Media Integration

If you want Twitter/X and Bluesky notifications:

```env
# Twitter/X (optional)
X_ACCESS_TOKEN=your_token
X_ACCESS_TOKEN_SECRET=your_secret
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret

# Bluesky (optional)
BSKY_USER="your_username"
BSKY_PASSWORD="your_password"
```

### Optional: Discord Emojis

Add custom emoji IDs for each platform:

```env
DISCORD_EPIC_EMOJI=emoji_id_here
DISCORD_STEAM_EMOJI=emoji_id_here
DISCORD_GOG_EMOJI=emoji_id_here
DISCORD_PSPLUS_EMOJI=emoji_id_here
DISCORD_PRIMEGAMING_EMOJI=emoji_id_here
```

**Note:** You can configure emojis later via the web interface!

---

## Step 4: Get Required Credentials

### 🔹 Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → Give it a name
3. Go to **Bot** tab → Click **Add Bot**
4. Under **Token**, click **Reset Token** → **Copy** the token
5. Paste into `.env` as `DISCORD_TOKEN_LIVE`

**Bot Permissions Needed:**
- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Add Reactions
- Manage Roles
- Use Slash Commands

**Invite URL:**
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=534723885120&scope=bot%20applications.commands
```
Replace `YOUR_CLIENT_ID` with your Application ID from the portal.

### 🔹 MongoDB Connection String

**Option 1: Cloud (MongoDB Atlas) - Einfach & Empfohlen**

1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a **Free Shared Cluster**
3. Click **Connect** → **Connect your application**
4. Copy the connection string
5. Replace `<username>` and `<password>` with your database credentials
6. Paste into `.env` as `DB_CONNECTION_STRING`

Example:
```
mongodb+srv://botuser:MySecureP@ss123@cluster0.abcde.mongodb.net/
```

**Option 2: Lokale MongoDB - Für Fortgeschrittene**

🚀 **Automatisches Setup (Empfohlen):**

```bash
# Linux/macOS:
./setup_mongodb.sh

# Alle Plattformen (Python):
python setup_mongodb.py
```

Die interaktiven Scripts führen dich durch die komplette lokale Installation!

📖 **Manuelle Installation:** Siehe [MONGODB_LOCAL.md](MONGODB_LOCAL.md)

### 🔹 Your Discord User ID

1. Enable **Developer Mode** in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username → **Copy ID**
3. Paste into `.env` as `DISCORD_ADMIN_ACC`

---

## Step 5: Run MercuryBot

```bash
python main.py
```

### Expected Output:

```
INFO - Modules: epic, steam, gog, psplus, primegaming
INFO - Starting web interface on 0.0.0.0:5000
INFO - Web server thread started
INFO - Discord client ready, connected to X servers
```

---

## Step 6: Configure Your Discord Server

### In Discord:

1. **Invite the bot** to your server using the invite URL
2. Run `/settings` command
3. Configure:
   - **Set channel:** Choose where notifications will be sent
   - **Set role:** (Optional) Choose a role to ping
   - **Set stores:** Select which platforms you want notifications for

### Test Setup:

```
/testnotify store:Epic Games
```

This sends a test notification to verify everything works!

---

## Step 7: Access Web Interface

Open your browser and go to:

```
http://localhost:5000
```

**Login:** Enter your Discord User ID (from `.env`)

### Web Interface Features:

- 🎨 **Configure Emojis** - Set emoji IDs for each platform
- 📊 **View Statistics** - See connected servers and active deals
- 📨 **Send Test Notifications** - Test notifications from the web
- 📝 **Template Documentation** - Learn how to customize messages

---

## Quick Command Reference

### Discord Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/settings` | Configure bot preferences | Manage Server |
| `/roles` | Set up reaction roles for platforms | Manage Server |
| `/testnotify` | Send test notification | Manage Server |
| `/deals` | View current free games | Everyone |
| `/feedback` | Submit feedback | Everyone |

### Bot Management

```bash
# Start bot
python main.py

# Stop bot
Ctrl + C

# View logs (if using systemd)
sudo journalctl -u mercurybot -f
```

---

## Troubleshooting

### Bot won't start

**Error:** `DISCORD_BOT_TOKEN is not set`
- **Solution:** Check that `.env` file exists and contains `DISCORD_TOKEN_LIVE`

**Error:** `Connection to MongoDB failed`
- **Solution:** Verify `DB_CONNECTION_STRING` is correct and IP is whitelisted in MongoDB Atlas

### Bot is online but commands don't work

- Wait 5-10 minutes for Discord to register slash commands
- Try kicking and re-inviting the bot
- Ensure bot has proper permissions

### Web interface won't start

**Error:** `Address already in use`
- **Solution:** Change `WEB_PORT` in `.env` to another port (e.g., 8080)

**Can't login to web interface**
- **Solution:** Verify `DISCORD_ADMIN_ACC` in `.env` matches your Discord User ID

### No notifications are sent

1. Run `/settings` and configure:
   - Notification channel
   - Stores to receive notifications for
2. Test with `/testnotify`
3. Check bot has permissions in the channel:
   - Send Messages
   - Embed Links
   - Attach Files
   - Add Reactions

---

## Production Deployment

For production use on a server:

### Using Systemd (Linux)

See [INSTALL_SERVICE.md](INSTALL_SERVICE.md) for detailed instructions.

Quick setup:
```bash
# Copy files to /opt/mercurybot
sudo cp -r . /opt/mercurybot/

# Install service
sudo cp mercurybot.service /etc/systemd/system/
sudo systemctl enable mercurybot
sudo systemctl start mercurybot

# Check status
sudo systemctl status mercurybot
```

### Using Docker (Coming Soon)

Docker support is planned for a future release.

---

## Next Steps

Now that MercuryBot is running:

1. ✅ **Customize Emojis** - Use web interface or `/roles` command
2. ✅ **Set up Reaction Roles** - Run `/roles` to let users self-assign platform roles
3. ✅ **Customize Templates** - Edit `clients/discord/messages.py` for custom notification designs
4. ✅ **Enable Social Media** - Configure Twitter/Bluesky in `.env` for multi-platform posting
5. ✅ **Monitor Performance** - Check web interface dashboard for statistics

---

## Getting Help

- 📚 **Full Documentation:** [README.md](README.md)
- 🔧 **Service Setup:** [INSTALL_SERVICE.md](INSTALL_SERVICE.md)
- 🌐 **Web Interface Guide:** [web/README.md](web/README.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/MercuryBot/issues)

---

## Configuration Examples

### Example 1: Discord Only (Minimal)

```env
DB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/
DISCORD_TOKEN_LIVE=your_token
DEBUG=False
DISCORD_ADMIN_ACC=123456789012345678
```

### Example 2: Full Setup with Social Media

```env
DB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/
DISCORD_TOKEN_LIVE=your_discord_token
DEBUG=False

DISCORD_ADMIN_ACC=123456789012345678
DISCORD_EPIC_EMOJI=987654321098765432
DISCORD_STEAM_EMOJI=987654321098765433
DISCORD_GOG_EMOJI=987654321098765434
DISCORD_PSPLUS_EMOJI=987654321098765435
DISCORD_PRIMEGAMING_EMOJI=987654321098765436

X_ACCESS_TOKEN=your_twitter_token
X_ACCESS_TOKEN_SECRET=your_twitter_secret
X_API_KEY=your_twitter_api_key
X_API_SECRET=your_twitter_api_secret

BSKY_USER="yourname.bsky.social"
BSKY_PASSWORD="your_bluesky_app_password"

WEB_PORT=5000
WEB_HOST=0.0.0.0
FLASK_SECRET_KEY=randomly_generated_secret_key_here
```

---

## Common Workflows

### Adding a New Server

1. Invite bot to server
2. Bot auto-configures with default channel
3. Admin runs `/settings` to customize
4. Users run `/roles` or react to messages to get platform roles

### Testing Notifications

**Via Discord:**
```
/testnotify store:Epic Games
```

**Via Web Interface:**
1. Go to `http://localhost:5000`
2. Login with Admin ID
3. Navigate to "Test Notifications"
4. Select server and store
5. Click "Send Test Notification"

### Updating Emojis

**Via Web Interface (Recommended):**
1. Dashboard → Emoji Configuration
2. Enter emoji IDs
3. Click "Save"
4. Restart bot

**Via .env File:**
1. Edit `.env`
2. Add/update `DISCORD_PLATFORM_EMOJI` values
3. Restart bot

---

## Success Checklist

- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with required values
- [ ] MongoDB connection string configured
- [ ] Discord bot token added
- [ ] Bot invited to Discord server
- [ ] Bot started successfully (`python main.py`)
- [ ] Web interface accessible
- [ ] `/settings` command run in Discord
- [ ] Test notification sent successfully
- [ ] Reaction roles working

---

**🎉 Congratulations!** MercuryBot is now running and ready to notify you about free games!

For advanced configuration and deployment options, see the full [README.md](README.md).
