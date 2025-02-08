from matchday.game_fetcher_strategies import WebScraperGameFetcher

# Set team name and schedule link
TEAM_NAME = "Falcons Footy"
SCHEDULE_URL = "https://www.soccer7s.ca/league_fixtures.seam?divisionId=5557"

def main():
    fetcher = WebScraperGameFetcher(SCHEDULE_URL, TEAM_NAME)
    game_info = fetcher.fetch_next_game()

    if game_info:
        print("Next Game Details:")
        print("===================")
        print(game_info)
    else:
        print("Failed to retrieve game information.")

if __name__ == "__main__":
    main()