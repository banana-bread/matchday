import requests
from bs4 import BeautifulSoup
from .base import GameFetcherStrategy
from squad_check.logger import logger
from squad_check.chatgpt_client import ChatGptClient
import re
from openai import OpenAIError

class WebScraperGameFetcher(GameFetcherStrategy):
    """Fetches game info by scraping the league schedule webpage using BeautifulSoup."""
    def fetch_next_game(self):
        """Fetches game info by scraping the league schedule webpage using BeautifulSoup."""
        try:
            html_content = self._fetch_schedule_html()
            return self._parse_game_info(html_content)
        except Exception:
            return None

    def _fetch_schedule_html(self):
        try:
            response = requests.get(self.schedule_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error("Failed to fetch schedule", extra={
                "error": str(e),
                "task_name": "WebScraperGameFetcher._fetch_schedule_html",
                "schedule_url": self.schedule_url,
                "team_name": self.team_name
            })
            raise RuntimeError(f"Schedule fetch failed: {str(e)}")
    
    def _parse_game_info(self, html):
        """Parses the HTML to find the next game for the specified team."""
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Find all game blocks
            games = soup.find_all("div", class_="fixtureColumns")
            
            for game in games:
                teams = game.find("div", class_="teams").find_all("td", class_="teamNames")
                team_names = [team.get_text(strip=True) for team in teams]

                # Check if our team is in this game
                if self.team_name not in team_names:
                    continue

                # Determine home/away
                home_team, away_team = team_names
                home_or_away = "Home" if home_team == self.team_name else "Away"
                opponent = away_team if home_team == self.team_name else home_team

                # Extract game time
                time_text = game.find("div", class_="locationAndTime").get_text(" ", strip=True)
                time_parts = time_text.split()
                time = next((part for part in time_parts if re.match(r"^\d{1,2}:\d{2}(?:am|pm)$", part, re.IGNORECASE)), "Unknown")

                # Extract location
                location_tag = game.find("a", class_="facilityLink")
                location = location_tag.get_text(strip=True) if location_tag else "Unknown"
                
                # Extract shirt colors
                shirts = game.find_all("span", class_="teamShirtNew")
                home_shirt_color = shirts[0]["style"].split("--shirt-colour-1: ")[1].split(";")[0] if shirts else "Unknown"
                away_shirt_color = shirts[1]["style"].split("--shirt-colour-1: ")[1].split(";")[0] if shirts else "Unknown"

                # Extract game date (Find the nearest previous header)
                date_tag = game.find_previous("th", class_="ui-state-default")
                date = date_tag.get_text(strip=True) if date_tag else "Unknown"

                # Determine team colours
                team_colour = home_shirt_color if home_or_away == "Home" else away_shirt_color
                opponoent_colour = away_shirt_color if home_or_away == "Home" else home_shirt_color

                return {
                    "next_game": {
                        "date": date,
                        "time": time,
                        "opponent": opponent,
                        "home_or_away": home_or_away,
                        "location": location,
                        "shirt_colours": {
                            "team": team_colour,
                            "opponent": opponoent_colour,
                            "conflict_exists": ChatGptClient().shirt_colour_conflict_exists(team_colour, opponoent_colour)
                        }
                    }
                }
            
            logger.warning("No upcoming games found", extra={
                "task_name": "WebScraperGameFetcher._parse_game_info",
                "schedule_url": self.schedule_url,
                "team_name": self.team_name
            })
            raise ValueError(f"No upcoming games found for team: {self.team_name}")

        except OpenAIError as e:
            logger.error("OpenAI API Error", extra={
                "task_name": "WebScraperGameFetcher._parse_game_info",
                "error": str(e)
            })
            return None
        except Exception as e:
            logger.error("HTML parsing failed", extra={
                "task_name": "WebScraperGameFetcher._parse_game_info",
                "error": str(e),
                "schedule_url": self.schedule_url,
                "team_name": self.team_name
            })
            raise RuntimeError(f"HTML parsing failed: {str(e)}")
        