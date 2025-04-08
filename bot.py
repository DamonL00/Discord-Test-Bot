import os
import discord
import logging
import sys
from discord.ext import commands
from dotenv import load_dotenv
from league_manager import LeagueManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("No token found. Make sure you have DISCORD_TOKEN in your .env file")

print(f"Token loaded: {TOKEN[:10]}...")  # Only print first 10 chars for security

# Bot setup with all necessary intents
intents = discord.Intents.all()  # Enable all intents for testing

bot = commands.Bot(command_prefix='!', intents=intents)
league_manager = LeagueManager()

@bot.event
async def on_ready():
    print('=' * 50)
    print(f'Successfully logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Bot is in {len(bot.guilds)} servers')
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')
    print('=' * 50)

@bot.event
async def on_connect():
    print("Bot has connected to Discord!")

@bot.event
async def on_disconnect():
    print("Bot has disconnected from Discord!")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f'An error occurred in {event}:')
    import traceback
    traceback.print_exc()

@bot.command(name='register')
async def register(ctx, team_name: str):
    """Register a team to the league"""
    result = league_manager.register_team(team_name, ctx.author.id)
    await ctx.send(result)

@bot.command(name='teams')
async def list_teams(ctx):
    """List all registered teams"""
    teams = league_manager.get_teams()
    if not teams:
        await ctx.send("No teams registered yet!")
        return
    
    embed = discord.Embed(title="League Teams", color=discord.Color.blue())
    for team in teams:
        embed.add_field(name=team['name'], value=f"Manager: <@{team['manager_id']}>", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='table')
async def show_table(ctx):
    """Display the current league table"""
    table = league_manager.get_league_table()
    if not table:
        await ctx.send("No teams in the league yet!")
        return
    
    embed = discord.Embed(title="League Table", color=discord.Color.green())
    for position, team in enumerate(table, 1):
        embed.add_field(
            name=f"{position}. {team['name']}",
            value=f"P: {team['played']} W: {team['won']} D: {team['drawn']} L: {team['lost']} Pts: {team['points']}",
            inline=False
        )
    await ctx.send(embed=embed)

@bot.command(name='fixtures')
async def generate_fixtures(ctx):
    """Generate random fixtures for the league"""
    fixtures = league_manager.generate_fixtures()
    if not fixtures:
        await ctx.send("Not enough teams to generate fixtures!")
        return
    
    embed = discord.Embed(title="League Fixtures", color=discord.Color.orange())
    for matchday, matches in fixtures.items():
        match_text = "\n".join([f"{match['home']} vs {match['away']}" for match in matches])
        embed.add_field(name=f"Matchday {matchday}", value=match_text, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='record')
async def record_result(ctx, home_team: str, home_score: int, away_team: str, away_score: int):
    """Record a match result"""
    result = league_manager.record_match(home_team, away_team, home_score, away_score)
    await ctx.send(result)

try:
    print("Attempting to start bot...")
    bot.run(TOKEN)
except discord.LoginFailure as e:
    print(f"Failed to login: {e}")
    print("Please check your token and make sure it's correct and hasn't been revoked.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print("Please check your internet connection and try again.") 