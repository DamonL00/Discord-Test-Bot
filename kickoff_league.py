import discord
from discord.ext import commands
import os
import sys
import traceback
import asyncio
from dotenv import load_dotenv
import random
import json
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with intents and better error handling
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class KickoffBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)
        self.initial_extensions = []
        self._cleanup_done = False
        self._reconnect_attempts = 0
        self.MAX_RECONNECT_ATTEMPTS = 5
        
    async def setup_hook(self):
        """Setup hook for bot initialization"""
        try:
            # Create data directory if it doesn't exist
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)
            
            # Load data at startup
            load_data()
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error in setup: {str(e)}")
            traceback.print_exc()
    
    async def close(self):
        """Cleanup when bot is shutting down"""
        if not self._cleanup_done:
            try:
                save_data()
                print("Data saved during shutdown")
                self._cleanup_done = True
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")
                traceback.print_exc()
        await super().close()

bot = KickoffBot()

# Global variables to store league data
teams_data = {}
fixtures_data = {}
matches_data = {}
time_slots = {}

# File paths for data persistence
DATA_DIR = "league_data"
TEAMS_FILE = os.path.join(DATA_DIR, "teams.json")
FIXTURES_FILE = os.path.join(DATA_DIR, "fixtures.json")
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")
TIME_SLOTS_FILE = os.path.join(DATA_DIR, "time_slots.json")

def save_data():
    """Save all league data to JSON files"""
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        # Save teams data
        with open(TEAMS_FILE, 'w') as f:
            json.dump(teams_data, f, indent=4)
        
        # Save fixtures data
        with open(FIXTURES_FILE, 'w') as f:
            json.dump(fixtures_data, f, indent=4)
        
        # Save matches data
        with open(MATCHES_FILE, 'w') as f:
            json.dump(matches_data, f, indent=4)
        
        # Save time slots data
        with open(TIME_SLOTS_FILE, 'w') as f:
            json.dump(time_slots, f, indent=4)
            
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def load_data():
    """Load all league data from JSON files"""
    try:
        # Load teams data
        if os.path.exists(TEAMS_FILE):
            with open(TEAMS_FILE, 'r') as f:
                global teams_data
                teams_data = json.load(f)
        
        # Load fixtures data
        if os.path.exists(FIXTURES_FILE):
            with open(FIXTURES_FILE, 'r') as f:
                global fixtures_data
                fixtures_data = json.load(f)
        
        # Load matches data
        if os.path.exists(MATCHES_FILE):
            with open(MATCHES_FILE, 'r') as f:
                global matches_data
                matches_data = json.load(f)
        
        # Load time slots data
        if os.path.exists(TIME_SLOTS_FILE):
            with open(TIME_SLOTS_FILE, 'r') as f:
                global time_slots
                time_slots = json.load(f)
                
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {str(e)}")

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        """Send the help message with organized categories"""
        try:
            # Create embeds for different categories
            main_embed = discord.Embed(
                title="⚽ KICKOFF LEAGUE BOT ⚽",
                color=discord.Color.blue(),
                description="Use `!help [command]` for more details about a specific command!"
            )
            
            # Team Management
            team_embed = discord.Embed(
                title="🏢 TEAM MANAGEMENT",
                color=discord.Color.green()
            )
            team_embed.add_field(
                name="Commands",
                value="> `!register [team_name]` - Register a new team\n"
                    "> `!squad [team_name]` - View team roster\n"
                    "> `!my_squad` - View your team and teammates\n"
                    "> `!add_player [team_name] [@player]` - Add player to team\n"
                    "> `!remove_player [team_name] [@player]` - Remove player from team",
                inline=False
            )
            
            # Team Leadership
            leadership_embed = discord.Embed(
                title="👑 TEAM LEADERSHIP",
                color=discord.Color.gold()
            )
            leadership_embed.add_field(
                name="Commands",
                value="> `!captain [team_name]` - Show team captain\n"
                    "> `!transfer_captaincy [team_name] [@new_captain]` - Transfer captaincy\n"
                    "> `!add_co_captain [team_name] [@new_co_captain]` - Add co-captain\n"
                    "> `!remove_co_captain [team_name] [@co_captain]` - Remove co-captain",
                inline=False
            )
            
            # Match Scheduling
            match_embed = discord.Embed(
                title="📅 MATCH SCHEDULING",
                color=discord.Color.purple()
            )
            match_embed.add_field(
                name="Commands",
                value="> `!set_availability [day] [time] [timezone]` - Set team availability\n"
                    "> `!schedule_match [fixture_id] [DD-MM HH:MM]` - Schedule a match\n"
                    "> `!auto_schedule` - Toggle automatic scheduling\n"
                    "> `!fixtures` - Show upcoming matches\n"
                    "> `!my_fixtures` - Show your team's matches\n"
                    "> `!fixtures_page [page]` - Navigate through fixtures pages",
                inline=False
            )
            
            match_embed2 = discord.Embed(
                title="📅 MATCH MANAGEMENT",
                color=discord.Color.purple()
            )
            match_embed2.add_field(
                name="Commands",
                value="> `!start_match [fixture_id]` - Start a match\n"
                    "> `!record [fixture_id] [A_score]-[B_score]` - Record match result\n"
                    "> `!results` - Show recent results\n"
                    "> `!cancel_match [fixture_id]` - Cancel an active match",
                inline=False
            )
            
            # League Information
            league_embed = discord.Embed(
                title="📊 LEAGUE INFORMATION",
                color=discord.Color.dark_blue()
            )
            league_embed.add_field(
                name="Commands",
                value="> `!table` - Show league standings\n"
                    "> `!stats [team_name]` - View team statistics\n"
                    "> `!get_team_limit` - Show current team limit",
                inline=False
            )
            
            # Administration Commands (Only visible to admins/mods)
            if self.context.author.guild_permissions.administrator or self.context.author.guild_permissions.manage_guild:
                admin_embed = discord.Embed(
                    title="🔒 ADMINISTRATION",
                    color=discord.Color.red()
                )
                admin_embed.add_field(
                    name="Commands",
                    value="> `!new_season` - Reset all league data and start a new season\n"
                        "> `!set_team_limit [number]` - Set maximum number of teams\n"
                        "> `!set_reminder_channel [channel]` - Set channel for match reminders\n"
                        "> `!set_reminder_time [hours]` - Set match reminder time\n"
                        "> `!toggle_auto_schedule` - Enable/disable automatic scheduling",
                    inline=False
                )
                
                # Send all embeds
                await self.get_destination().send(embed=main_embed)
                await self.get_destination().send(embed=team_embed)
                await self.get_destination().send(embed=leadership_embed)
                await self.get_destination().send(embed=match_embed)
                await self.get_destination().send(embed=match_embed2)
                await self.get_destination().send(embed=league_embed)
                await self.get_destination().send(embed=admin_embed)
            else:
                # Send non-admin embeds
                await self.get_destination().send(embed=main_embed)
                await self.get_destination().send(embed=team_embed)
                await self.get_destination().send(embed=leadership_embed)
                await self.get_destination().send(embed=match_embed)
                await self.get_destination().send(embed=match_embed2)
                await self.get_destination().send(embed=league_embed)
                
            print(f"Help command executed by {self.context.author.name}")
        except Exception as e:
            print(f"Error in help command: {str(e)}")
            traceback.print_exc()  # This will print the full traceback
            await self.get_destination().send(f"Error showing help: {str(e)}")

    async def send_command_help(self, command):
        """Show help for a specific command"""
        try:
            embed = discord.Embed(
                title=f"Command: !{command.name}",
                color=discord.Color.blue(),
                description=command.help or "No description available"
            )
            
            if command.aliases:
                embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
                
            embed.add_field(name="Usage", value=f"!{command.name} {command.signature}", inline=False)
            
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(f"Error in command help: {str(e)}")
            traceback.print_exc()
            await self.get_destination().send(f"Error showing command help: {str(e)}")

    async def send_group_help(self, group):
        try:
            await self.send_command_help(group)
        except Exception as e:
            print(f"Error in group help: {str(e)}")
            traceback.print_exc()
            await self.get_destination().send(f"Error showing group help: {str(e)}")

    async def send_cog_help(self, cog):
        try:
            await self.send_bot_help(None)
        except Exception as e:
            print(f"Error in cog help: {str(e)}")
            traceback.print_exc()
            await self.get_destination().send(f"Error showing cog help: {str(e)}")
        
    async def send_error_message(self, error):
        try:
            embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
            await self.get_destination().send(embed=embed)
        except Exception as e:
            print(f"Error in error message: {str(e)}")
            traceback.print_exc()
            # Try a simple text message as fallback
            try:
                await self.get_destination().send(f"Error: {error}")
            except:
                print("Could not send error message at all")

# Set the custom help command
bot.help_command = CustomHelpCommand()

@bot.event
async def on_ready():
    """Called when the bot is ready"""
    try:
        print(f"Logged in as {bot.user.name}")
        print(f"Bot ID: {bot.user.id}")
        print("------")
        bot._reconnect_attempts = 0  # Reset reconnect attempts on successful connection
        
        # Set bot status
        await bot.change_presence(activity=discord.Game(name="!help for commands"), status=discord.Status.online)
    except Exception as e:
        print(f"Error in on_ready: {str(e)}")
        traceback.print_exc()

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors during event processing"""
    try:
        error = sys.exc_info()
        if error:
            error_type, error_value, error_traceback = error
            print(f"Error in {event}: {error_type.__name__}: {str(error_value)}")
            print("".join(traceback.format_tb(error_traceback)))
    except Exception as e:
        print(f"Error in error handler: {str(e)}")
        traceback.print_exc()

@bot.event
async def on_disconnect():
    """Handle disconnection"""
    try:
        print("Bot disconnected. Attempting to save data...")
        save_data()
        print("Data saved during disconnect")
        
        # Increment reconnect attempts
        bot._reconnect_attempts += 1
        if bot._reconnect_attempts <= bot.MAX_RECONNECT_ATTEMPTS:
            print(f"Reconnect attempt {bot._reconnect_attempts}/{bot.MAX_RECONNECT_ATTEMPTS}")
        else:
            print("Maximum reconnection attempts reached")
    except Exception as e:
        print(f"Error during disconnect: {str(e)}")
        traceback.print_exc()

@bot.event
async def on_connect():
    """Handle reconnection"""
    try:
        if bot._reconnect_attempts > 0:  # Only reload data if this is a reconnection
            print("Bot reconnected. Reloading data...")
            load_data()
            print("Data reloaded after reconnect")
            await bot.change_presence(activity=discord.Game(name="!help for commands"), status=discord.Status.online)
    except Exception as e:
        print(f"Error during reconnect: {str(e)}")
        traceback.print_exc()

@bot.event
async def on_command_error(ctx, error):
    """Handle errors during command execution"""
    try:
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ Command not found! Use `!help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name == 'register':
                await ctx.send("❌ Please provide a team name: `!register [team name]`")
            else:
                await ctx.send(f"❌ Missing required argument. Use `!help {ctx.command.name}` for correct usage.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Invalid argument: {str(error)}")
        elif isinstance(error, commands.CommandInvokeError):
            # Get the original error
            original = error.original
            print(f"Command '{ctx.command.name}' raised an error: {type(original).__name__}: {original}")
            traceback.print_exc()
            await ctx.send(f"❌ An error occurred while executing the command: {str(original)}")
        else:
            print(f"Command error in {ctx.command.name if ctx.command else 'unknown command'}:")
            print(f"{type(error).__name__}: {str(error)}")
            traceback.print_exc()
            await ctx.send(f"❌ An error occurred: {str(error)}")
    except Exception as e:
        # Catch any errors in the error handler itself
        print(f"Error in error handler: {str(e)}")
        traceback.print_exc()
        try:
            await ctx.send("❌ An unexpected error occurred while handling the command error.")
        except:
            pass  # If we can't send a message, there's not much we can do

@bot.command(name='register')
async def register_team(ctx, *, team_name: str):
    """Register a new team
    Usage: !register [team_name]"""
    try:
        # Check if team name already exists
        if team_name in teams_data:
            await ctx.send(f"❌ A team with the name '{team_name}' already exists!")
            return
        
        # Check team limit (default 12)
        team_limit = teams_data.get('_settings', {}).get('team_limit', 12)
        if len(teams_data) >= team_limit + 1:  # +1 because _settings is also counted
            await ctx.send(f"❌ Maximum team limit reached ({team_limit} teams)! Contact an admin to adjust the limit.")
            return
        
        # Create new team with proper initialization
        teams_data[team_name] = {
            'name': team_name,  # Add name field for table display
            'captain': ctx.author.id,
            'co_captains': [],  # Initialize empty co-captains list
            'players': [],      # Initialize empty players list
            'stats': {
                'matches_played': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0,
                'clean_sheets': 0
            }
        }
        
        # Save data
        save_data()
        
        # Create success embed
        embed = discord.Embed(
            title="✅ Team Registered Successfully",
            description=f"Team '{team_name}' has been created!",
            color=discord.Color.green()
        )
        embed.add_field(name="Captain", value=ctx.author.mention, inline=False)
        embed.add_field(name="Next Steps", 
                       value="1. Use `!add_player [team_name] [@player]` to add players\n"
                             "2. Use `!add_co_captain [team_name] [@player]` to add co-captains\n"
                             "3. Use `!squad [team_name]` to view your team roster",
                       inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error registering team: {str(e)}")

@bot.command(name='set_team_limit')
@commands.has_permissions(administrator=True)
async def set_team_limit(ctx, limit: int):
    """Set the maximum number of teams allowed (Admin only)
    Usage: !set_team_limit [number]"""
    try:
        if limit < 2:
            await ctx.send("❌ Team limit must be at least 2!")
            return
            
        # Initialize settings if not exists
        if '_settings' not in teams_data:
            teams_data['_settings'] = {}
        
        # Store old limit for message
        old_limit = teams_data['_settings'].get('team_limit', 12)
        
        # Update team limit
        teams_data['_settings']['team_limit'] = limit
        save_data()
        
        embed = discord.Embed(
            title="✅ Team Limit Updated",
            description=f"Maximum teams changed from {old_limit} to {limit}",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Current Status",
            value=f"Current Teams: {len(teams_data) - 1}\nNew Limit: {limit}",  # -1 to exclude _settings
            inline=False
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error setting team limit: {str(e)}")

@bot.command(name='get_team_limit')
async def get_team_limit(ctx):
    """Show current team limit and registration status"""
    try:
        team_limit = teams_data.get('_settings', {}).get('team_limit', 12)
        current_teams = len(teams_data) - 1 if '_settings' in teams_data else len(teams_data)  # -1 to exclude _settings
        
        embed = discord.Embed(
            title="📊 Team Registration Status",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Current Status",
            value=f"Teams Registered: {current_teams}/{team_limit}",
            inline=False
        )
        embed.add_field(
            name="Registration",
            value="Open ✅" if current_teams < team_limit else "Closed ❌",
            inline=False
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error getting team limit: {str(e)}")

@bot.command(name='generate_fixtures')
async def generate_fixtures(ctx):
    """Generate a complete fixture list where each team plays every other team twice"""
    try:
        # Check for exactly 12 teams
        if len(teams_data) < 12:
            await ctx.send(f"❌ Not enough teams registered! Current teams: {len(teams_data)}/12\nNeed exactly 12 teams to generate fixtures.")
            return
        elif len(teams_data) > 12:
            await ctx.send(f"❌ Too many teams registered! Current teams: {len(teams_data)}/12\nNeed exactly 12 teams to generate fixtures.")
            return
        
        # Clear existing fixtures
        fixtures_data.clear()
        
        # Get list of teams and shuffle them randomly
        teams = list(teams_data.keys())
        random.shuffle(teams)
        fixture_id = 1
        
        # Calculate total matchdays (22 matchdays for a balanced season - each team plays others home and away)
        total_matchdays = 22
        matches_per_matchday = 6  # 12 teams = 6 matches per matchday
        
        # Generate fixtures for the entire season
        for matchday in range(1, total_matchdays + 1):
            # Rotate teams for balanced scheduling
            if matchday > 1:
                teams = [teams[0]] + [teams[-1]] + teams[1:-1]
            
            # Create matches for this matchday
            for i in range(matches_per_matchday):
                home_team = teams[i]
                away_team = teams[11 - i]  # Match first with last, second with second-last, etc.
                
                # For second half of season, swap home/away
                if matchday > 11:
                    home_team, away_team = away_team, home_team
                
                # Create the fixture
                fixtures_data[fixture_id] = {
                    'home_team': home_team,
                    'away_team': away_team,
                    'matchday': matchday,
                    'status': 'pending',
                    'home_score': None,
                    'away_score': None,
                    'date': None,
                    'started_by': None,
                    'completed_by': None
                }
                fixture_id += 1
        
        # Save the fixtures
        save_data()
        
        # Create the fixtures message with matchday organization
        embed = discord.Embed(
            title="🏆 Season Fixtures Generated",
            description="Each team plays others home and away",
            color=discord.Color.green()
        )
        
        # Add summary field
        embed.add_field(
            name="📊 Season Summary",
            value=f"• Total Teams: 12\n• Total Matchdays: 22\n• Matches per Matchday: 6\n• Total Matches: {len(fixtures_data)}",
            inline=False
        )
        
        # Show first 5 matchdays as preview
        preview = "```\n"
        preview += "ID  Home            vs  Away             Matchday\n"
        preview += "─" * 55 + "\n"
        
        # Show first 10 fixtures as preview
        for fixture_id, fixture in list(fixtures_data.items())[:10]:
            preview += f"{fixture_id:<3} {fixture['home_team']:<15} vs {fixture['away_team']:<15} {fixture['matchday']}\n"
        
        preview += "\n... and more fixtures (use !fixtures to see all)\n"
        preview += "```"
        
        embed.add_field(name="🎮 Upcoming Fixtures (Preview)", value=preview, inline=False)
        embed.add_field(
            name="📝 Available Commands",
            value="• `!fixtures` - View all fixtures\n• `!start_match [fixture_id]` - Start a match\n• `!record [fixture_id] [A_score]-[B_score]` - Record result",
            inline=False
        )
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error generating fixtures: {str(e)}")
        traceback.print_exc()

@bot.command(name='start_match')
async def start_match(ctx, fixture_id: int):
    """Start a match, making it active for recording"""
    try:
        if fixture_id not in fixtures_data:
            await ctx.send(f"Fixture ID {fixture_id} not found!")
            return
        
        fixture = fixtures_data[fixture_id]
        
        # Check if match is already active or completed
        if fixture['status'] == 'active':
            await ctx.send(f"Match {fixture_id} is already in progress!")
            return
        elif fixture['status'] == 'completed':
            await ctx.send(f"Match {fixture_id} has already been completed!")
            return
        
        # Check if user is captain or co-captain of either team
        home_team = teams_data[fixture['home_team']]
        away_team = teams_data[fixture['away_team']]
        
        home_team_auth = (ctx.author.id == home_team['captain'] or 
                         ('co_captains' in home_team and ctx.author.id in home_team['co_captains']))
        away_team_auth = (ctx.author.id == away_team['captain'] or 
                         ('co_captains' in away_team and ctx.author.id in away_team['co_captains']))
        
        if not (home_team_auth or away_team_auth):
            await ctx.send("Only team captains or co-captains can start matches!")
            return
        
        # Start the match
        fixture['status'] = 'active'
        fixture['started_by'] = ctx.author.id
        fixture['date'] = ctx.message.created_at
        
        await ctx.send(f"Match {fixture_id} has been started!\n"
                      f"{fixture['home_team']} vs {fixture['away_team']}\n"
                      f"Use `!record {fixture_id} [A_score]-[B_score]` to record the result.")
    except Exception as e:
        await ctx.send(f"Error starting match: {str(e)}")

@bot.command(name='cancel_match')
async def cancel_match(ctx, fixture_id: int):
    """Cancel an active match"""
    try:
        if fixture_id not in fixtures_data:
            await ctx.send(f"Fixture ID {fixture_id} not found!")
            return
        
        fixture = fixtures_data[fixture_id]
        
        # Check if match is active
        if fixture['status'] != 'active':
            await ctx.send(f"Match {fixture_id} is not currently active!")
            return
        
        # Check if user started the match or is a captain
        home_team = teams_data[fixture['home_team']]
        away_team = teams_data[fixture['away_team']]
        
        if (ctx.author.id != fixture['started_by'] and 
            ctx.author.id not in [home_team['captain'], away_team['captain']]):
            await ctx.send("Only the match starter or team captains can cancel the match!")
            return
        
        # Cancel the match
        fixture['status'] = 'pending'
        fixture['started_by'] = None
        fixture['date'] = None
        
        await ctx.send(f"Match {fixture_id} has been cancelled and reset to pending status.")
    except Exception as e:
        await ctx.send(f"Error cancelling match: {str(e)}")

@bot.command(name='record')
async def record_match(ctx, fixture_id: str, score: str):
    """Record the result of a match"""
    try:
        # Check if fixture exists
        if fixture_id not in fixtures_data:
            await ctx.send(f"Fixture {fixture_id} not found!")
            return
        
        fixture = fixtures_data[fixture_id]
        
        # Check if match is active
        if fixture['status'] != 'active':
            await ctx.send(f"Match {fixture_id} is not active!")
            return
        
        # Parse score
        try:
            home_score, away_score = map(int, score.split('-'))
        except ValueError:
            await ctx.send("Invalid score format! Use A-B format (e.g., 2-1)")
            return
        
        # Update fixture status and scores
        fixture['status'] = 'completed'
        fixture['home_score'] = home_score
        fixture['away_score'] = away_score
        
        # Update team statistics
        home_team = teams_data[fixture['home_team']]
        away_team = teams_data[fixture['away_team']]
        
        # Update matches played
        home_team['stats']['matches_played'] += 1
        away_team['stats']['matches_played'] += 1
        
        # Update goals
        home_team['stats']['goals_for'] += home_score
        home_team['stats']['goals_against'] += away_score
        away_team['stats']['goals_for'] += away_score
        away_team['stats']['goals_against'] += home_score
        
        # Update goal difference
        home_team['stats']['goal_difference'] = home_team['stats']['goals_for'] - home_team['stats']['goals_against']
        away_team['stats']['goal_difference'] = away_team['stats']['goals_for'] - away_team['stats']['goals_against']
        
        # Update wins/losses and points
        if home_score > away_score:
            home_team['stats']['wins'] += 1
            away_team['stats']['losses'] += 1
            home_team['stats']['points'] += 3
        else:
            away_team['stats']['wins'] += 1
            home_team['stats']['losses'] += 1
            away_team['stats']['points'] += 3
        
        # Update clean sheets
        if away_score == 0:
            home_team['stats']['clean_sheets'] += 1
        if home_score == 0:
            away_team['stats']['clean_sheets'] += 1
        
        # Save data after recording match
        save_data()
        
        await ctx.send(f"Match {fixture_id} recorded: {fixture['home_team']} {home_score}-{away_score} {fixture['away_team']}")
    except Exception as e:
        await ctx.send(f"Error recording match: {str(e)}")

@bot.command(name='table')
async def show_table(ctx):
    """Display the current league table"""
    try:
        # Filter out settings from teams data
        actual_teams = {name: data for name, data in teams_data.items() if name != '_settings'}
        
        if not actual_teams:
            await ctx.send("No teams registered yet!")
            return
        
        # Create list of teams with their stats
        table_data = []
        for team_name, team in actual_teams.items():
            team_stats = team['stats']
            table_data.append({
                'name': team_name,
                'matches_played': team_stats['matches_played'],
                'wins': team_stats['wins'],
                'losses': team_stats['losses'],
                'draws': team_stats.get('draws', 0),  # Added draws
                'goals_for': team_stats['goals_for'],
                'goals_against': team_stats['goals_against'],
                'goal_difference': team_stats['goals_for'] - team_stats['goals_against'],
                'points': team_stats['points']
            })
        
        # Sort teams by points, goal difference, and goals scored
        table_data.sort(key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)
        
        # Create the table message
        table = "```\n"
        table += "Pos  Team            P   W   D   L   GF  GA  GD  Pts\n"
        table += "─" * 55 + "\n"
        
        for i, team in enumerate(table_data, 1):
            table += f"{i:<4} {team['name']:<15} {team['matches_played']:<3} {team['wins']:<3} {team['draws']:<3} "
            table += f"{team['losses']:<3} {team['goals_for']:<3} {team['goals_against']:<3} "
            table += f"{team['goal_difference']:<3} {team['points']:<3}\n"
        
        table += "\nP=Played  W=Won  D=Drawn  L=Lost  GF=Goals For  GA=Goals Against  GD=Goal Difference  Pts=Points"
        table += "```"
        
        embed = discord.Embed(
            title="📊 League Table",
            description=table,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error displaying table: {str(e)}")
        traceback.print_exc()  # This will help debug any issues

@bot.command(name='stats')
async def show_stats(ctx, team_name: str):
    """Show detailed statistics for a team"""
    try:
        team = teams_data.get(team_name)
        if not team:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        stats = f"**Statistics for {team_name}:**\n```\n"
        stats += f"Matches Played: {team['stats']['matches_played']}\n"
        stats += f"Wins: {team['stats']['wins']}\n"
        stats += f"Losses: {team['stats']['losses']}\n"
        stats += f"Goals For: {team['stats']['goals_for']}\n"
        stats += f"Goals Against: {team['stats']['goals_against']}\n"
        stats += f"Goal Difference: {team['stats']['goal_difference']}\n"
        stats += f"Points: {team['stats']['points']}\n"
        stats += f"Clean Sheets: {team['stats']['clean_sheets']}\n"
        stats += "```"
        
        await ctx.send(stats)
    except Exception as e:
        await ctx.send(f"Error showing stats: {str(e)}")

@bot.command(name='fixtures')
async def show_fixtures(ctx):
    """Show upcoming matches organized by matchday"""
    try:
        if not fixtures_data:
            await ctx.send("No fixtures have been generated yet! Use `!generate_fixtures` when 12 teams are registered.")
            return
        
        # Group fixtures by matchday
        fixtures_by_matchday = {}
        for fixture_id, fixture in fixtures_data.items():
            matchday = fixture.get('matchday', 0)
            if matchday not in fixtures_by_matchday:
                fixtures_by_matchday[matchday] = []
            fixtures_by_matchday[matchday].append((fixture_id, fixture))
        
        # Create embed
        embed = discord.Embed(
            title="⚽ League Fixtures",
            description="All scheduled matches for the season",
            color=discord.Color.blue()
        )
        
        # Add fixtures for each matchday
        for matchday in sorted(fixtures_by_matchday.keys()):
            fixtures_list = "```\n"
            fixtures_list += "ID  Home            vs  Away             Status\n"
            fixtures_list += "─" * 55 + "\n"
            
            for fixture_id, fixture in fixtures_by_matchday[matchday]:
                status = fixture['status'].capitalize()
                fixtures_list += f"{fixture_id:<3} {fixture['home_team']:<15} vs {fixture['away_team']:<15} {status}\n"
            
            fixtures_list += "```"
            
            embed.add_field(
                name=f"📅 Matchday {matchday}",
                value=fixtures_list,
                inline=False
            )
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error showing fixtures: {str(e)}")
        traceback.print_exc()

@bot.command(name='results')
async def show_results(ctx):
    """Show recent match results"""
    try:
        if not fixtures_data:
            await ctx.send("No matches have been played yet!")
            return
        
        # Create the results message
        results = "**Recent Results:**\n```\n"
        results += "ID  Home Team        Score    Away Team\n"
        results += "-" * 50 + "\n"
        
        for fixture_id, fixture in fixtures_data.items():
            if fixture['status'] == 'completed':
                results += f"{fixture_id:<3} {fixture['home_team']:<15} {fixture['home_score']}-{fixture['away_score']}  {fixture['away_team']}\n"
        
        results += "```"
        await ctx.send(results)
    except Exception as e:
        await ctx.send(f"Error showing results: {str(e)}")

@bot.command(name='captain')
async def show_captain(ctx, team_name: str):
    """Show who the captain of a team is
    Usage: !captain [team_name]"""
    try:
        if not team_name:
            await ctx.send("❌ Please provide a team name! Usage: `!captain [team_name]`")
            return
            
        team = teams_data.get(team_name)
        if not team:
            await ctx.send(f"❌ Team '{team_name}' not found!")
            return
        
        # Create embed
        embed = discord.Embed(
            title=f"👑 Team Leadership - {team_name}",
            color=discord.Color.gold()
        )
        
        # Add captain
        try:
            captain = await bot.fetch_user(team['captain'])
            embed.add_field(name="Captain", value=captain.mention, inline=False)
        except (KeyError, discord.NotFound):
            embed.add_field(name="Captain", value="No captain assigned", inline=False)
        
        # Add co-captains if they exist
        try:
            if team.get('co_captains'):
                co_captain_mentions = []
                for co_captain_id in team['co_captains']:
                    try:
                        co_captain = await bot.fetch_user(co_captain_id)
                        co_captain_mentions.append(co_captain.mention)
                    except discord.NotFound:
                        continue
                
                if co_captain_mentions:
                    embed.add_field(name="Co-Captains", value="\n".join(co_captain_mentions), inline=False)
                else:
                    embed.add_field(name="Co-Captains", value="No co-captains assigned", inline=False)
            else:
                embed.add_field(name="Co-Captains", value="No co-captains assigned", inline=False)
        except Exception:
            embed.add_field(name="Co-Captains", value="No co-captains assigned", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error showing captain: {str(e)}")

@bot.command(name='transfer_captaincy')
async def transfer_captaincy(ctx, team_name: str, new_captain: discord.Member):
    """Transfer captaincy to another user"""
    try:
        team = teams_data.get(team_name)
        if not team:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        # Check if current user is the captain
        if ctx.author.id != team['captain']:
            await ctx.send("Only the current captain can transfer captaincy!")
            return
        
        # Update captain
        team['captain'] = new_captain.id
        
        # Remove from co-captains if they were one
        if 'co_captains' in team and new_captain.id in team['co_captains']:
            team['co_captains'].remove(new_captain.id)
        
        await ctx.send(f"Captaincy of {team_name} has been transferred to {new_captain.name}!")
    except Exception as e:
        await ctx.send(f"Error transferring captaincy: {str(e)}")

@bot.command(name='add_co_captain')
async def add_co_captain(ctx, team_name: str, new_co_captain: discord.Member):
    """Add a co-captain to a team"""
    try:
        team = teams_data.get(team_name)
        if not team:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        # Check if current user is the captain
        if ctx.author.id != team['captain']:
            await ctx.send("Only the captain can add co-captains!")
            return
        
        # Initialize co-captain list if it doesn't exist
        if 'co_captains' not in team:
            team['co_captains'] = []
        
        # Check if user is already a co-captain
        if new_co_captain.id in team['co_captains']:
            await ctx.send(f"{new_co_captain.name} is already a co-captain!")
            return
        
        # Add co-captain
        team['co_captains'].append(new_co_captain.id)
        await ctx.send(f"{new_co_captain.name} has been added as a co-captain of {team_name}!")
    except Exception as e:
        await ctx.send(f"Error adding co-captain: {str(e)}")

@bot.command(name='remove_co_captain')
async def remove_co_captain(ctx, team_name: str, co_captain: discord.Member):
    """Remove a co-captain from a team"""
    try:
        team = teams_data.get(team_name)
        if not team:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        # Check if current user is the captain
        if ctx.author.id != team['captain']:
            await ctx.send("Only the captain can remove co-captains!")
            return
        
        # Check if co-captain exists
        if 'co_captains' not in team or co_captain.id not in team['co_captains']:
            await ctx.send(f"{co_captain.name} is not a co-captain of {team_name}!")
            return
        
        # Remove co-captain
        team['co_captains'].remove(co_captain.id)
        await ctx.send(f"{co_captain.name} has been removed as a co-captain of {team_name}!")
    except Exception as e:
        await ctx.send(f"Error removing co-captain: {str(e)}")

@bot.command(name='add_player')
async def add_player(ctx, team_name: str, player: discord.Member):
    """Add a player to a team"""
    try:
        # Check if team exists
        if team_name not in teams_data:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        # Check if player is already in a team
        for team in teams_data.values():
            if player.id in team['players']:
                await ctx.send(f"{player.mention} is already in a team!")
                return
        
        # Add player to team
        teams_data[team_name]['players'].append(player.id)
        
        # Save data after adding player
        save_data()
        
        await ctx.send(f"{player.mention} has been added to {team_name}!")
    except Exception as e:
        await ctx.send(f"Error adding player: {str(e)}")

@bot.command(name='remove_player')
async def remove_player(ctx, team_name: str, player: discord.Member):
    """Remove a player from a team"""
    try:
        if team_name not in teams_data:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        team = teams_data[team_name]
        
        # Check if user is captain or co-captain
        if (ctx.author.id != team['captain'] and 
            ('co_captains' not in team or ctx.author.id not in team['co_captains'])):
            await ctx.send("Only team captains or co-captains can remove players!")
            return
        
        # Check if player exists
        if player.id not in team['players']:
            await ctx.send(f"{player.name} is not a member of {team_name}!")
            return
        
        # Remove player
        team['players'].remove(player.id)
        await ctx.send(f"{player.name} has been removed from {team_name}!")
    except Exception as e:
        await ctx.send(f"Error removing player: {str(e)}")

@bot.command(name='squad')
async def show_squad(ctx, team_name: str):
    """Show the squad of a team"""
    try:
        if team_name not in teams_data:
            await ctx.send(f"Team '{team_name}' not found!")
            return
        
        team = teams_data[team_name]
        
        # Create the message
        message = f"**{team_name} Squad:**\n```\n"
        
        if team['players']:
            for player_id in team['players']:
                player = await bot.fetch_user(player_id)
                message += f"- {player.name}\n"
        else:
            message += "No players in the squad yet.\n"
        
        message += "```"
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Error showing squad: {str(e)}")

@bot.command(name='my_squad')
async def show_my_squad(ctx):
    """Show which team you're on and your teammates"""
    try:
        # Find which team the user is on
        user_team = None
        for team_name, team in teams_data.items():
            if ctx.author.id in team['players']:
                user_team = team_name
                break
        
        if not user_team:
            await ctx.send("You are not currently on any team!")
            return
        
        team = teams_data[user_team]
        
        # Get captain and co-captains
        captain = await bot.fetch_user(team['captain'])
        co_captains = []
        if 'co_captains' in team:
            for co_captain_id in team['co_captains']:
                co_captain = await bot.fetch_user(co_captain_id)
                co_captains.append(co_captain)
        
        # Create the message
        message = f"**Your Team: {user_team}**\n\n"
        message += f"**Captain:** {captain.name}\n"
        
        if co_captains:
            message += "\n**Co-Captains:**\n"
            for co_captain in co_captains:
                message += f"- {co_captain.name}\n"
        
        message += "\n**Teammates:**\n"
        for player_id in team['players']:
            if player_id != ctx.author.id:  # Don't show self in teammates list
                player = await bot.fetch_user(player_id)
                message += f"- {player.name}\n"
        
        await ctx.send(message)
    except Exception as e:
        await ctx.send(f"Error showing squad: {str(e)}")

@bot.command(name='new_season')
async def new_season(ctx):
    """Reset all league data and start a new season (Admin/Mod only)"""
    try:
        # Check if user has either administrator or manage_guild permissions
        if not (ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_guild):
            await ctx.send("❌ You don't have permission to start a new season! This command is for administrators and moderators only.")
            return
            
        # Confirm with the user
        confirm_message = await ctx.send(
            "⚠️ **WARNING: This will reset ALL league data!** ⚠️\n"
            "This includes:\n"
            "- All teams and their rosters\n"
            "- All fixtures and match results\n"
            "- All statistics and records\n\n"
            "Type `!confirm` to proceed or `!cancel` to abort."
        )
        
        # Wait for confirmation
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            if msg.content.lower() == '!confirm':
                # Reset all data
                global teams_data, fixtures_data, matches_data, time_slots
                teams_data = {}
                fixtures_data = {}
                matches_data = {}
                time_slots = {}
                
                # Save empty data
                save_data()
                
                await ctx.send("✅ **New season started!** All data has been reset.\n"
                             "You can now begin registering new teams with `!register [team_name]`")
            else:
                await ctx.send("New season creation cancelled.")
        except asyncio.TimeoutError:
            await ctx.send("New season creation timed out. Please try again.")
            
    except Exception as e:
        await ctx.send(f"Error starting new season: {str(e)}")

async def main():
    """Main function to run the bot"""
    retry_count = 0
    while retry_count < 5:  # Maximum 5 retries
        try:
            print("Starting bot...")
            print("Checking token...")
            if not TOKEN:
                print("Error: No token found!")
                return
                
            print("Token found, attempting to start bot...")
            await bot.start(TOKEN)
            return  # If we get here, the bot started successfully
                
        except discord.LoginFailure:
            print("Failed to login. Please check your token.")
            return
        except discord.ConnectionClosed:
            retry_count += 1
            if retry_count >= 5:
                print("Maximum reconnection attempts reached. Shutting down.")
                return
            print(f"Connection closed. Attempting to reconnect... ({retry_count}/5)")
            await asyncio.sleep(5)  # Wait before reconnecting
        except Exception as e:
            print(f"Error in main: {str(e)}")
            traceback.print_exc()
            retry_count += 1
            if retry_count >= 5:
                print("Maximum reconnection attempts reached. Shutting down.")
                return
            await asyncio.sleep(5)  # Wait before reconnecting
        finally:
            if not bot._cleanup_done:
                try:
                    save_data()
                    print("Data saved during shutdown")
                except Exception as e:
                    print(f"Error saving data: {str(e)}")
                    traceback.print_exc()

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nBot shutting down (KeyboardInterrupt)...")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
    finally:
        try:
            if not getattr(bot, '_cleanup_done', False):
                save_data()
                print("Data saved during error")
            
            # Clean up the event loop
            if loop and not loop.is_closed():
                loop.run_until_complete(bot.close())
                loop.close()
        except Exception as save_error:
            print(f"Error during final cleanup: {str(save_error)}")
            traceback.print_exc() 