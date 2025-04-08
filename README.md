# Discord Kickoff League Bot

A Discord bot for managing football/soccer leagues with features like team registration, fixture generation, match management, and statistics tracking.

## Features

- **Team Management**
  - Register teams with captains and co-captains
  - Add/remove players from teams
  - View team rosters and squads
  - Automatic 12-team league system

- **Match Management**
  - Generate balanced fixtures automatically
  - Start and record matches
  - Track scores and results
  - Cancel ongoing matches

- **Statistics & Tracking**
  - League table with points and goal difference
  - Team statistics (wins, losses, goals, etc.)
  - Match history and results
  - Clean sheets tracking

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/DamonL00/Discord-Test-Bot.git
cd Discord-Test-Bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create environment file**
Create a `.env` file in the project root and add your Discord bot token:
```
DISCORD_TOKEN=your_bot_token_here
```

4. **Run the bot**
```bash
python kickoff_league.py
```

## Commands

### Team Management
- `!register [team_name]` - Register a new team
- `!squad [team_name]` - View team roster
- `!my_squad` - View your team and teammates
- `!add_player [team_name] [@player]` - Add player to team
- `!remove_player [team_name] [@player]` - Remove player from team

### Match Management
- `!generate_fixtures` - Generate season fixtures (requires 12 teams)
- `!fixtures` - Show upcoming matches
- `!start_match [fixture_id]` - Start a match
- `!record [fixture_id] [A_score]-[B_score]` - Record match result
- `!cancel_match [fixture_id]` - Cancel an active match

### Statistics
- `!table` - Show league standings
- `!stats [team_name]` - View team statistics
- `!results` - Show recent results

### Team Leadership
- `!captain [team_name]` - Show team captain
- `!transfer_captaincy [team_name] [@new_captain]` - Transfer captaincy
- `!add_co_captain [team_name] [@new_co_captain]` - Add co-captain
- `!remove_co_captain [team_name] [@co_captain]` - Remove co-captain

### Admin Commands
- `!new_season` - Reset all league data (Admin only)
- `!set_team_limit [number]` - Change maximum team limit (Admin only)
- `!get_team_limit` - Check current team registration status

## Points System

- Win: 3 points
- Draw: 1 point
- Loss: 0 points

Teams are ranked by:
1. Total points
2. Goal difference
3. Goals scored

## License

This project is licensed under the CC0-1.0 License - see the [LICENSE](LICENSE) file for details. 