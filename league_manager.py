import random
from typing import List, Dict, Any

class LeagueManager:
    def __init__(self):
        self.teams = {}  # team_name -> team_data
        self.matches = []  # list of played matches
        self.fixtures = {}  # matchday -> list of matches

    def register_team(self, team_name: str, manager_id: int) -> str:
        """Register a new team to the league"""
        if team_name in self.teams:
            return f"Team '{team_name}' is already registered!"
        
        self.teams[team_name] = {
            'name': team_name,
            'manager_id': manager_id,
            'played': 0,
            'won': 0,
            'drawn': 0,
            'lost': 0,
            'points': 0,
            'goals_for': 0,
            'goals_against': 0
        }
        return f"Team '{team_name}' has been registered!"

    def get_teams(self) -> List[Dict[str, Any]]:
        """Get list of all registered teams"""
        return list(self.teams.values())

    def get_league_table(self) -> List[Dict[str, Any]]:
        """Get the current league table sorted by points and goal difference"""
        teams = list(self.teams.values())
        teams.sort(key=lambda x: (x['points'], x['goals_for'] - x['goals_against']), reverse=True)
        return teams

    def generate_fixtures(self) -> Dict[int, List[Dict[str, str]]]:
        """Generate random fixtures for the league"""
        if len(self.teams) < 2:
            return {}

        team_list = list(self.teams.keys())
        random.shuffle(team_list)
        num_teams = len(team_list)
        num_matchdays = (num_teams - 1) * 2
        matches_per_day = num_teams // 2

        self.fixtures = {}
        for matchday in range(1, num_matchdays + 1):
            day_fixtures = []
            for i in range(matches_per_day):
                home = team_list[i]
                away = team_list[num_teams - 1 - i]
                day_fixtures.append({'home': home, 'away': away})
            self.fixtures[matchday] = day_fixtures
            # Rotate teams for next matchday
            team_list.insert(1, team_list.pop())

        return self.fixtures

    def record_match(self, home_team: str, away_team: str, home_score: int, away_score: int) -> str:
        """Record a match result and update team statistics"""
        if home_team not in self.teams or away_team not in self.teams:
            return "One or both teams are not registered!"

        # Update home team stats
        self.teams[home_team]['played'] += 1
        self.teams[home_team]['goals_for'] += home_score
        self.teams[home_team]['goals_against'] += away_score

        # Update away team stats
        self.teams[away_team]['played'] += 1
        self.teams[away_team]['goals_for'] += away_score
        self.teams[away_team]['goals_against'] += home_score

        # Update points and win/draw/loss records
        if home_score > away_score:
            self.teams[home_team]['won'] += 1
            self.teams[home_team]['points'] += 3
            self.teams[away_team]['lost'] += 1
        elif home_score < away_score:
            self.teams[away_team]['won'] += 1
            self.teams[away_team]['points'] += 3
            self.teams[home_team]['lost'] += 1
        else:
            self.teams[home_team]['drawn'] += 1
            self.teams[home_team]['points'] += 1
            self.teams[away_team]['drawn'] += 1
            self.teams[away_team]['points'] += 1

        return f"Match recorded: {home_team} {home_score} - {away_score} {away_team}" 