# 🐍 Python Aternos Bot - Replit Setup Guide

Complete guide to run the Python version of the Aternos Discord bot on Replit.

---

## 📋 Files You Need

1. **bot.py** - Main bot code
2. **requirements.txt** - Python dependencies
3. **.replit** - Replit configuration
4. **replit.nix** - System dependencies (Chrome)

---

## 🚀 Step-by-Step Setup

### Step 1: Create a Replit Project

1. Go to [Replit.com](https://replit.com)
2. Click **"+ Create Repl"**
3. Choose **"Python"** template (NOT Node.js)
4. Name it: `aternos-discord-bot`
5. Click **"Create Repl"**

### Step 2: Upload Files

1. Delete the default `main.py` file
2. Upload these files to your Repl:
   - `bot.py`
   - `requirements.txt`
   - `.replit`
   - `replit.nix`

### Step 3: Get a Discord Bot Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name your bot: `Aternos Server Manager`
4. Go to **"Bot"** section → Click **"Add Bot"**
5. **IMPORTANT:** Enable these under "Privileged Gateway Intents":
   - ✅ **MESSAGE CONTENT INTENT**
   - ✅ Presence Intent (optional)
   - ✅ Server Members Intent (optional)
6. Click **"Reset Token"** → Copy the token (save it!)

### Step 4: Invite Bot to Discord Server

1. Go to **"OAuth2"** → **"URL Generator"**
2. Select scopes:
   - ✅ `bot`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Embed Links
   - ✅ Read Message History
4. Copy the generated URL
5. Paste in browser and select your server

### Step 5: Configure Replit Secrets

Click the **🔒 Lock icon** (Secrets) in the sidebar and add:

```
DISCORD_TOKEN = your_discord_bot_token_here
ATERNOS_USERNAME = your_aternos_email@example.com
ATERNOS_PASSWORD = your_aternos_password
SERVER_NAME = YourExactServerName
ALLOWED_ROLE = Admin
COMMAND_PREFIX = !
```

**⚠️ Critical Notes:**
- `SERVER_NAME` must match EXACTLY (case-sensitive!)
- Never share your secrets with anyone
- Token starts with something like `MTIzNDU2...`

### Step 6: Install Dependencies

In the Replit Shell (bottom panel), run:

```bash
pip install -r requirements.txt
```

This installs:
- discord.py (Discord bot library)
- selenium (Web automation)
- Flask (Keep-alive server)
- webdriver-manager (Chrome driver)

### Step 7: Run the Bot

1. Click the big green **"Run"** button
2. Wait for installation to complete
3. You should see:
   ```
   ✅ Bot logged in as YourBot#1234!
   ```

### Step 8: Test in Discord

Open your Discord server and type:

```
!help
```

You should see a help embed! Then try:

```
!startserver
```

The bot will:
1. Show a loading message
2. Log into Aternos
3. Find your server
4. Start it
5. Confirm success!

---

## 🎮 Available Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!startserver` | Start the Aternos server | Requires allowed role |
| `!help` | Show help message | Everyone |
| `!status` | Show bot uptime and status | Everyone |

---

## 📁 File Structure

```
aternos-discord-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── .replit            # Replit run configuration
├── replit.nix         # System packages (Chrome)
└── README.md          # This file
```

---

## 🔧 Configuration Files Explained

### `.replit`
```json
{
  "run": "python bot.py",
  "language": "python",
  "onBoot": "pip install -r requirements.txt"
}
```
- Tells Replit to run `python bot.py`
- Auto-installs dependencies on boot

### `replit.nix`
```nix
{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.chromium
    pkgs.chromedriver
  ];
}
```
- Installs system-level packages
- **Chromium** is needed for Selenium
- **Chromedriver** controls Chrome

### `requirements.txt`
```
discord.py==2.3.2
selenium==4.16.0
webdriver-manager==4.0.1
Flask==3.0.0
python-dotenv==1.0.0
```
- Python packages needed by the bot

---

## 🐛 Troubleshooting

### Bot Shows Offline in Discord

**Possible causes:**
1. Wrong Discord token
2. Bot not invited to server
3. Message Content Intent not enabled

**Solution:**
```bash
# Check if bot is running
# Look for: "✅ Bot logged in as..."

# If not, check secrets:
# - DISCORD_TOKEN should start with MTI, MTA, etc.
# - No spaces before/after token
```

### "You need the Admin role"

**Cause:** User doesn't have the required role

**Solution:**
1. In Discord, create a role named exactly as `ALLOWED_ROLE` (default: `Admin`)
2. Right-click user → Roles → Assign the role
3. Try command again

### "Server not found"

**Possible causes:**
1. `SERVER_NAME` doesn't match exactly
2. Server not in your Aternos account
3. Typo in server name

**Solution:**
```bash
# Check your Aternos dashboard
# Copy the EXACT server name (case matters!)
# Update SERVER_NAME secret in Replit
```

### Selenium/Chrome Errors

**Error:** `chromedriver not found`

**Solution:**
```bash
# In Replit Shell:
which chromium
which chromedriver

# If missing, check replit.nix file exists
# Then restart the Repl
```

**Error:** `Message: unknown error: Chrome failed to start`

**Solution:**
```bash
# Add to bot.py (already included):
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
```

### Bot Goes Offline After 1 Hour

**Cause:** Replit free tier puts inactive repls to sleep

**Solution - Use UptimeRobot:**

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up (free)
3. Click **"Add New Monitor"**
4. Settings:
   - Monitor Type: `HTTP(s)`
   - Friendly Name: `Aternos Bot`
   - URL: `https://your-repl-url.repl.co`
   - Monitoring Interval: `5 minutes`
5. Click **"Create Monitor"**

This pings your bot every 5 minutes, keeping it awake!

### Login Fails

**Possible causes:**
1. Wrong Aternos credentials
2. Aternos detected automation
3. Aternos website structure changed

**Solution:**
```bash
# Test credentials manually:
# 1. Visit aternos.org
# 2. Try logging in
# 3. If it works, check secrets in Replit

# If you're getting CAPTCHA:
# - Aternos might be blocking automated logins
# - Try from a different IP (use VPN)
# - Wait 30 minutes and try again
```

---

## 🔄 Keeping Bot Online 24/7

### Method 1: UptimeRobot (Free)

1. Create account at [uptimerobot.com](https://uptimerobot.com)
2. Add HTTP monitor
3. URL: Your Repl's URL
4. Interval: 5 minutes
5. Done! Bot stays awake

### Method 2: Replit Hacker Plan

- Upgrade to Replit Hacker
- Always-on Repls
- No need for keep-alive tricks
- Costs ~$7/month

### Method 3: Self-Host (Advanced)

Run on your own computer:

```bash
# Clone/download files
python3 bot.py

# Or use screen/tmux to run in background
screen -S aternos-bot
python3 bot.py
# Press Ctrl+A, then D to detach
```

---

## ⚙️ Customization

### Change Command Prefix

Update `COMMAND_PREFIX` secret:
- `!` → Commands: `!startserver`
- `$` → Commands: `$startserver`
- `/` → Commands: `/startserver`

### Change Required Role

Update `ALLOWED_ROLE` secret:
- `Admin` (default)
- `Moderator`
- `ServerOwner`
- Any role name in your Discord

### Add More Commands

Edit `bot.py`:

```python
@bot.command(name='stopserver')
async def stop_server(ctx):
    """Stop the server"""
    await ctx.send("This command isn't implemented yet!")
```

---

## 📊 Understanding the Code

### Main Components

1. **Flask Server** (lines 10-20)
   - Keeps Replit alive
   - Responds to HTTP pings
   - Runs in background thread

2. **Discord Bot Setup** (lines 30-50)
   - Creates bot instance
   - Sets up intents
   - Loads configuration

3. **Selenium Automation** (lines 52-200)
   - Opens Chrome browser
   - Logs into Aternos
   - Finds and starts server
   - Handles errors

4. **Discord Commands** (lines 202-300)
   - `@bot.command()` decorators
   - Command handlers
   - Embed creation

### How It Works Together

```
User types: !startserver
    ↓
Discord.py receives message
    ↓
Checks user has required role
    ↓
Runs Selenium automation (async)
    ↓
Selenium opens Chrome:
    • Goes to Aternos
    • Logs in
    • Finds server
    • Clicks start
    ↓
Returns result to Discord
    ↓
Bot sends success/error message
```

---

## 🔐 Security Best Practices

### DO:
- ✅ Use Replit Secrets (not hardcoded)
- ✅ Limit bot permissions in Discord
- ✅ Only give required role to trusted users
- ✅ Keep bot token private
- ✅ Use strong Aternos password

### DON'T:
- ❌ Share your bot token
- ❌ Commit secrets to GitHub
- ❌ Give bot admin permissions
- ❌ Use the same password everywhere
- ❌ Share your Repl publicly with secrets

---

## 📚 Learn More

### Python Resources
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Python Discord](https://pythondiscord.com/)

### Discord.py Resources
- [Official Documentation](https://discordpy.readthedocs.io/)
- [Discord.py Guide](https://guide.pycord.dev/)
- [Discord Developer Docs](https://discord.com/developers/docs)

### Selenium Resources
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Selenium Tutorial](https://www.selenium.dev/documentation/)

---

## ❓ FAQ

**Q: Can I use this with Dyno bot?**
A: Yes! This is your own custom bot. It works alongside Dyno or any other bots.

**Q: Is this against Aternos ToS?**
A: Automated access might be. Use at your own risk for personal/educational purposes.

**Q: How much does this cost?**
A: Free! Replit free tier + Discord bot + Aternos free = $0

**Q: Can I run multiple servers?**
A: Currently no, but you can modify the code to support it.

**Q: Does this work on mobile?**
A: The bot runs on Replit (cloud), so you just use Discord mobile normally!

**Q: Can I add more features?**
A: Yes! Edit `bot.py` and add new commands. Python is beginner-friendly.

---

## 🎉 Success Checklist

- [ ] Repl created and files uploaded
- [ ] Discord bot created and invited
- [ ] All secrets configured in Replit
- [ ] Dependencies installed
- [ ] Bot shows "logged in" message
- [ ] `!help` command works in Discord
- [ ] Required role created and assigned
- [ ] `!startserver` successfully starts server
- [ ] UptimeRobot configured (optional)

---

## 📞 Need Help?

If you're stuck:

1. Check the console for error messages
2. Verify all secrets are set correctly
3. Make sure Discord intents are enabled
4. Test Aternos credentials manually
5. Check Replit community forums

---

**Happy gaming! 🎮🐍**
