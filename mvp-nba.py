from nba_api.stats.endpoints import playergamelog
import pandas as pd

# Dictionary to map player names to their NBA Player IDs
players = {
    "Joel Embiid": 203954,
    "Nikola Jokic": 203999,
    "Giannis Antetokounmpo": 203507,
    "Jayson Tatum": 1628369,
    "Shai Gilgeous-Alexander": 1628983,
    "Devin Booker": 1626164,
    "Luka Doncic": 1629029,
    "Stephen Curry": 201939,
    "Chris Paul": 101108,
    "LeBron James": 2544,
    "James Harden": 201935,
    "Kawhi Leonard": 202695,
    "Paul George": 202331,
    "Anthony Davis": 203076,
    "Damian Lillard": 203081,
    "Russell Westbrook": 201566,
    "Isaiah Thomas": 202738,
    "Kevin Durant": 201142,
    "Blake Griffin": 201933,
    "Joakim Noah": 201149,
    "Carmelo Anthony": 2546,
    "Kobe Bryant": 977,
    "Derrick Rose": 201565,
    "Dwight Howard": 2730,
    "Dwyane Wade": 2548,
    "Tony Parker": 2225
}

# List of top 5 MVPs for each season (year and player names)
mvp_candidates = {
    2023: ["Joel Embiid", "Nikola Jokic", "Giannis Antetokounmpo", "Jayson Tatum", "Shai Gilgeous-Alexander"],
    2022: ["Nikola Jokic", "Joel Embiid", "Giannis Antetokounmpo", "Devin Booker", "Luka Doncic"],
    2021: ["Nikola Jokic", "Joel Embiid", "Stephen Curry", "Giannis Antetokounmpo", "Chris Paul"],
    2020: ["Giannis Antetokounmpo", "LeBron James", "James Harden", "Luka Doncic", "Kawhi Leonard"],
    2019: ["Giannis Antetokounmpo", "James Harden", "Paul George", "Nikola Jokic", "Stephen Curry"],
    2018: ["James Harden", "LeBron James", "Anthony Davis", "Damian Lillard", "Russell Westbrook"],
    2017: ["Russell Westbrook", "James Harden", "Kawhi Leonard", "LeBron James", "Isaiah Thomas"],
    2016: ["Stephen Curry", "Kawhi Leonard", "LeBron James", "Russell Westbrook", "Kevin Durant"],
    2015: ["Stephen Curry", "James Harden", "LeBron James", "Russell Westbrook", "Anthony Davis"],
    2014: ["Kevin Durant", "LeBron James", "Blake Griffin", "Joakim Noah", "James Harden"],
    2013: ["LeBron James", "Kevin Durant", "Carmelo Anthony", "Chris Paul", "Kobe Bryant"],
    2012: ["LeBron James", "Kevin Durant", "Chris Paul", "Kobe Bryant", "Tony Parker"],
    2011: ["Derrick Rose", "Dwight Howard", "LeBron James", "Kobe Bryant", "Kevin Durant"],
    2010: ["LeBron James", "Kevin Durant", "Kobe Bryant", "Dwight Howard", "Dwyane Wade"]
}

# Initialize list to hold all players' data
all_season_summaries = []

# Loop through each year and players for that year
for year, top_5_players in mvp_candidates.items():
    for player_name in top_5_players:
        player_id = players.get(player_name)
        
        if player_id:
            # Fetch game log data for each player for the relevant season
            season_str = f"{year-1}-{str(year)[-2:]}"  # Format season string, e.g., "2022-23"
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season_str)
            gamelog_df = gamelog.get_data_frames()[0]
            
            # Calculate the season averages for each player
            summary = gamelog_df.mean(numeric_only=True).to_frame().T
            summary['Player'] = player_name  # Add player name column
            summary['Season'] = season_str  # Add season column
            
            # Append player summary to the list
            all_season_summaries.append(summary)
    
    # Add an empty row (separator) after each season
    all_season_summaries.append(pd.DataFrame([[""] * len(summary.columns)], columns=summary.columns))

# Combine all summaries into a single DataFrame
summary_stats_df = pd.concat(all_season_summaries, ignore_index=True)

# Save the data to CSV
summary_stats_df.to_csv('mvp_season_averages.csv', index=False)

# Print to verify
print(summary_stats_df)
