from abc import ABC, abstractmethod

class GameFetcherStrategy(ABC):
    """Abstract base class for game fetching strategies."""

    def __init__(self,  schedule_url: str, team_name: str):
        self.team_name = team_name
        self.schedule_url = schedule_url

    @abstractmethod
    def fetch_next_game(self):
        """Fetch the next game details and return as JSON."""
        pass
