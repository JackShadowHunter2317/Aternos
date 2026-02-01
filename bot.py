import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import asyncio
import os
import time
from flask import Flask
from threading import Thread

# Flask app to keep Replit alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Aternos Bot is running!"

def run_flask():
    """Run Flask server in a separate thread"""
    app.run(host='0.0.0.0', port=8080)

# Start Flask in background
flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Configuration from environment variables
CONFIG = {
    'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
    'ATERNOS_USERNAME': os.getenv('ATERNOS_USERNAME'),
    'ATERNOS_PASSWORD': os.getenv('ATERNOS_PASSWORD'),
    'SERVER_NAME': os.getenv('SERVER_NAME'),
    'ALLOWED_ROLE': os.getenv('ALLOWED_ROLE', 'Admin'),
    'COMMAND_PREFIX': os.getenv('COMMAND_PREFIX', '!')
}

# Discord bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=CONFIG['COMMAND_PREFIX'], intents=intents)

def start_aternos_server(username, password, server_name):
    """
    Automate Aternos login and server startup using Selenium
    
    Args:
        username (str): Aternos username/email
        password (str): Aternos password
        server_name (str): Name of the server to start
        
    Returns:
        dict: Contains 'success' (bool) and 'message' (str)
    """
    driver = None
    
    try:
        print("Setting up Chrome driver...")
        
        # Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--window-size=1280,720')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        # Initialize Chrome driver
        # For Replit, you might need to specify the chromedriver path
        driver = webdriver.Chrome(options=chrome_options)
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        
        print("Navigating to Aternos...")
        driver.get('https://aternos.org/:it/')
        time.sleep(2)
        
        # Click login button
        print("Looking for login button...")
        wait = WebDriverWait(driver, 10)
        
        # Try multiple selectors for login button
        login_selectors = [
            (By.CSS_SELECTOR, 'a[href*="go/login"]'),
            (By.CLASS_NAME, 'login-button'),
            (By.ID, 'login')
        ]
        
        login_clicked = False
        for selector_type, selector_value in login_selectors:
            try:
                login_button = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                login_button.click()
                login_clicked = True
                print("Login button clicked!")
                break
            except:
                continue
        
        if not login_clicked:
            raise Exception("Could not find login button")
        
        time.sleep(2)
        
        # Fill in credentials
        print("Entering credentials...")
        
        # Find username field
        username_selectors = [
            (By.NAME, 'user'),
            (By.ID, 'user')
        ]
        
        for selector_type, selector_value in username_selectors:
            try:
                username_field = wait.until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                username_field.clear()
                username_field.send_keys(username)
                break
            except:
                continue
        
        # Find password field
        password_selectors = [
            (By.NAME, 'password'),
            (By.ID, 'password')
        ]
        
        for selector_type, selector_value in password_selectors:
            try:
                password_field = driver.find_element(selector_type, selector_value)
                password_field.clear()
                password_field.send_keys(password)
                break
            except:
                continue
        
        # Submit login form
        print("Logging in...")
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for page to load after login
        time.sleep(5)
        
        # Check if login was successful
        if "login" in driver.current_url.lower():
            raise Exception("Login failed - check your credentials")
        
        print("Login successful!")
        
        # Wait for server list to load
        print(f"Looking for server: {server_name}...")
        time.sleep(3)
        
        # Find all servers
        server_selectors = [
            (By.CLASS_NAME, 'server-body'),
            (By.CLASS_NAME, 'server-card')
        ]
        
        servers = []
        for selector_type, selector_value in server_selectors:
            try:
                servers = driver.find_elements(selector_type, selector_value)
                if servers:
                    break
            except:
                continue
        
        if not servers:
            raise Exception("No servers found in account")
        
        # Find the specific server by name
        server_found = False
        for server in servers:
            try:
                # Try to find server name element
                name_selectors = [
                    (By.CLASS_NAME, 'server-name'),
                    (By.CLASS_NAME, 'servername')
                ]
                
                for selector_type, selector_value in name_selectors:
                    try:
                        name_element = server.find_element(selector_type, selector_value)
                        name = name_element.text.strip()
                        
                        if name == server_name or server_name in name:
                            print(f"Found server: {name}")
                            server.click()
                            server_found = True
                            break
                    except:
                        continue
                
                if server_found:
                    break
            except:
                continue
        
        if not server_found:
            raise Exception(f"Server '{server_name}' not found in your account")
        
        time.sleep(3)
        
        # Click start button
        print("Looking for start button...")
        start_selectors = [
            (By.ID, 'start'),
            (By.CLASS_NAME, 'start-button'),
            (By.CSS_SELECTOR, 'button[data-action="start"]')
        ]
        
        start_clicked = False
        for selector_type, selector_value in start_selectors:
            try:
                start_button = wait.until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                start_button.click()
                start_clicked = True
                print("Start button clicked!")
                break
            except:
                continue
        
        if not start_clicked:
            raise Exception("Could not find or click start button")
        
        time.sleep(3)
        
        # Logout
        print("Logging out...")
        driver.get('https://aternos.org/go/logout/')
        time.sleep(2)
        
        print("Process completed successfully!")
        return {
            'success': True,
            'message': 'Server started successfully!'
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'success': False,
            'message': str(e)
        }
        
    finally:
        # Always close the driver
        if driver:
            driver.quit()
            print("Browser closed")

# Discord bot events
@bot.event
async def on_ready():
    """Called when the bot is ready"""
    print(f'✅ Bot logged in as {bot.user.name}!')
    print(f'Bot ID: {bot.user.id}')
    print('------')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{CONFIG['COMMAND_PREFIX']}startserver"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    else:
        print(f"Error: {error}")
        await ctx.send("❌ An error occurred while processing the command.")

@bot.command(name='startserver')
async def start_server(ctx):
    """
    Start the Aternos Minecraft server
    
    Usage: !startserver
    """
    # Check if user has required role
    if not any(role.name == CONFIG['ALLOWED_ROLE'] for role in ctx.author.roles):
        await ctx.send(f"❌ You need the `{CONFIG['ALLOWED_ROLE']}` role to use this command!")
        return
    
    # Send initial status message
    status_message = await ctx.send("🔄 Starting Aternos server... This may take up to 1 minute...")
    
    try:
        # Run the automation in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            start_aternos_server,
            CONFIG['ATERNOS_USERNAME'],
            CONFIG['ATERNOS_PASSWORD'],
            CONFIG['SERVER_NAME']
        )
        
        if result['success']:
            await status_message.edit(
                content=f"✅ {result['message']}\n⏳ The server should be online in 2-3 minutes."
            )
        else:
            await status_message.edit(
                content=f"❌ Failed: {result['message']}"
            )
            
    except Exception as e:
        print(f"Command error: {e}")
        await status_message.edit(
            content="❌ An unexpected error occurred. Check console logs."
        )

@bot.command(name='help')
async def help_command(ctx):
    """
    Show help information
    
    Usage: !help
    """
    embed = discord.Embed(
        title="🎮 Aternos Server Bot",
        description="Automatically start your Aternos Minecraft server!",
        color=discord.Color.green()
    )
    
    prefix = CONFIG['COMMAND_PREFIX']
    
    embed.add_field(
        name=f"{prefix}startserver",
        value="▶️ Starts the Aternos server",
        inline=True
    )
    
    embed.add_field(
        name=f"{prefix}help",
        value="❓ Shows this help message",
        inline=True
    )
    
    embed.add_field(
        name=f"{prefix}status",
        value="📊 Shows bot status",
        inline=True
    )
    
    embed.set_footer(
        text=f"Only users with the {CONFIG['ALLOWED_ROLE']} role can start the server"
    )
    
    embed.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed)

@bot.command(name='status')
async def status_command(ctx):
    """
    Show bot status
    
    Usage: !status
    """
    # Calculate uptime
    uptime_seconds = time.time() - bot.start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    embed = discord.Embed(
        title="🤖 Bot Status",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🟢 Status",
        value="Online",
        inline=True
    )
    
    embed.add_field(
        name="⏱️ Uptime",
        value=f"{hours}h {minutes}m",
        inline=True
    )
    
    embed.add_field(
        name="🎯 Server",
        value=CONFIG['SERVER_NAME'],
        inline=True
    )
    
    embed.timestamp = discord.utils.utcnow()
    
    await ctx.send(embed=embed)

# Main execution
if __name__ == '__main__':
    # Store start time for uptime calculation
    bot.start_time = time.time()
    
    # Check if token is set
    if not CONFIG['DISCORD_TOKEN']:
        print("❌ Error: DISCORD_TOKEN not set in environment variables!")
        exit(1)
    
    print("Starting bot...")
    
    # Run the bot
    try:
        bot.run(CONFIG['DISCORD_TOKEN'])
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
