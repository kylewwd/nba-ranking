from nba_api.stats.endpoints import playergamelog
import pandas as pd

# Dictionary to map player names to their NBA Player IDs
players = {
    "Nikola Jokic": 203999,
    "Luka Doncic": 1629029,
    "Giannis Antetokounmpo": 203507,
    "Shai Gilgeous-Alexander": 1628983,
    "Joel Embiid": 203954,
    "Jayson Tatum": 1628369,
    "Stephen Curry": 201939,
    "Kevin Durant": 201142,
    "Anthony Davis": 203076
}

all_player_summary = []

for player_name, player_id in players.items():
    # Fetch game log data for each player for the 2023-2024 season
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season='2023-24')
    gamelog_df = gamelog.get_data_frames()[0]
    
    # Calculate the summary stats for each player
    summary = gamelog_df.mean(numeric_only=True).to_frame().T
    summary['Player'] = player_name  # Add player name column
    
    # Append to summary list
    all_player_summary.append(summary)

# Combine all players' summaries
summary_stats_df = pd.concat(all_player_summary, ignore_index=True)

# Save to CSV
summary_stats_df.to_csv('player_summary_2023_2024.csv', index=False)

# Print to verify
print(summary_stats_df)
