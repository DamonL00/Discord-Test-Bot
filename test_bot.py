import discord
from discord.ext import commands
import os
import sys
import traceback
import asyncio
import time
from dotenv import load_dotenv

# Set the event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load the token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("Error: No token found in .env file!")
    sys.exit(1)

# Create bot instance with explicit intents
intents = discord.Intents(
    guilds=True,              # Required for guild-related features
    members=True,             # Required for member-related features
    messages=True,            # Required for message-related features
    message_content=True,     # Required for reading message content
    presences=True,           # Required for presence-related features
    voice_states=True,        # Required for voice-related features
    reactions=True,           # Required for reaction-related features
    typing=True              # Required for typing indicators
)

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection_attempts = 0

    async def setup_hook(self):
        print("Bot is setting up...")
        try:
            # Add any setup code here
            pass
        except Exception as e:
            print(f"Error in setup_hook: {e}")
            traceback.print_exc()

    async def on_error(self, event, *args, **kwargs):
        print(f'Error in {event}:')
        traceback.print_exc()

    async def on_connect(self):
        self.connection_attempts = 0
        print("Bot has connected to Discord!")

    async def on_disconnect(self):
        print("Bot has disconnected from Discord!")

    async def on_ready(self):
        print('=' * 50)
        print(f'Test bot is ready! Logged in as {self.user.name}')
        print(f'Bot ID: {self.user.id}')
        print(f'Connected to {len(self.guilds)} servers:')
        for guild in self.guilds:
            print(f'- {guild.name} (ID: {guild.id})')
        print('=' * 50)

bot = MyBot(command_prefix='!', intents=intents)

@bot.command()
async def ping(ctx):
    try:
        await ctx.send('Pong!')
        print(f"Responded to ping from {ctx.author} in {ctx.guild.name}")
    except Exception as e:
        print(f"Error responding to ping: {e}")
        traceback.print_exc()

async def main():
    async with bot:
        try:
            await bot.start(TOKEN)
        except discord.LoginFailure:
            print("Failed to login: Invalid token")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

# Run the bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot is shutting down...")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc() 