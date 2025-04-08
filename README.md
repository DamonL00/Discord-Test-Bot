# Discord Kickoff League Bot

A Discord bot for managing soccer/football leagues, teams, and matches.

## Features

- Team registration and management
- Player roster management with captains and co-captains
- Match scheduling and fixtures generation
- Match result recording and statistics tracking
- League table generation
- Team and player statistics

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord token (see `.env.example`)
4. Run the bot:
   ```
   python kickoff_league.py
   ```

## Commands

Use `!help` in Discord to see all available commands.

### Main Commands

- `!register [team_name]` - Register a new team
- `!squad [team_name]` - View team roster
- `!my_squad` - View your team and teammates
- `!add_player [team_name] [@player]` - Add player to team
- `!fixtures` - Show upcoming matches
- `!start_match [fixture_id]` - Start a match
- `!record [fixture_id] [A_score]-[B_score]` - Record match result
- `!results` - Show recent results
- `!table` - Show league standings

## GitHub Integration

This repository includes scripts to simplify the GitHub deployment process:

### Using PowerShell (Recommended for Windows users)

1. Run `github_push.ps1` from PowerShell:
   ```
   .\github_push.ps1
   ```
2. Follow the prompts to enter your GitHub credentials if needed
3. The script will handle initialization, committing, and pushing

### Using Batch File (Alternative for Windows users)

1. Double-click `push_to_github.bat` in File Explorer or run it from Command Prompt:
   ```
   push_to_github.bat
   ```
2. Follow the prompts to complete the process

## License

This project is licensed under the CC0 1.0 Universal License - see the LICENSE file for details. 