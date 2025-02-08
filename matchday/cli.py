import argparse
from matchday.game_fetcher_strategies import WebScraperGameFetcher
import json

def main():
    parser = argparse.ArgumentParser(description="Fetch next soccer game details.")
    parser.add_argument("--team", required=True, help="Team name to search for")
    parser.add_argument("--url", required=True, help="Schedule URL to scrape")

    args = parser.parse_args()

    fetcher = WebScraperGameFetcher(args.url, args.team)
    game_info = fetcher.fetch_next_game()

    if game_info:
        print(json.dumps(game_info, indent=4))
    else:
        print("❌ No game found.")

if __name__ == "__main__":
    main()