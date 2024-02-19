import pandas as pd
from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2
from nba_api.stats.static import teams
import time, os, shutil

# print(teams.find_teams_by_full_name("Houston Rockets"))
# print(teams.find_team_name_by_id(1610612745))
# print(teamgamelog.TeamGameLog(team_id=1610612745, season='2023-24').get_data_frames()[0].iloc[0])

# # # Find the team ID for the LA Clippers
# # clippers_info = teams.find_team_by_abbreviation('LAC')
# # clippers_id = clippers_info['id']

# # # Retrieve the last game log for the LA Clippers
# # clippers_game_log = teamgamelog.TeamGameLog(team_id=clippers_id, season='2023-24').get_data_frames()[0]

# # # Get the most recent game details
# # last_game = clippers_game_log.iloc[0]

# # # Print the details of the last game
# # print(last_game)

# # yes = players.find_player_by_id(1628971)
# # print(yes)

# from nba_api.stats.endpoints import boxscoretraditionalv2

# Specify the GAME_ID for the game you're interested in
# game_id = '0022300732'  # Example GAME_ID, replace with your actual game_id

# # Fetch the traditional box score data for the game
# boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
# team_stats = boxscore.get_data_frames()[1]  # The team_stats data frame contains team-level statistics
# print("team stats",team_stats)

# # Extract points scored by both teams
# # Note: The data frame should have two rows, one for each team
# home_team_points = team_stats['PTS'].iloc[0]  # Assuming the first row is the home team
# away_team_points = team_stats['PTS'].iloc[1]  # Assuming the second row is the away team

# print(f"Home Team Points: {home_team_points}")
# print(f"Away Team Points: {away_team_points}")

# # Set pandas display options to show all rows and columns
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

# # Example GameID (replace with the actual GameID)
# game_id = '0022300662'

# # Retrieve the game summary
# game_summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
# game_info = game_summary.get_data_frames()[0]

# # Print the entire game information
# print(game_info)

#Change these first before daily run
yFile_m = 'matchupOutput_2_13_24.csv'

importedResultsCSV = pd.read_csv(yFile_m)

# Parse name from csv results.
# create a temporary array
# Run a for loop of the api in that array

# Function to extract the name from each line
def extract_first_team(line):
    if "vs" in line:
        return line.split(" vs")[0]
    else:
        return line

team_names = [extract_first_team(line) for line in importedResultsCSV['line']]
#print("THIS IS first teams...", team_names)

nice = []

for team in team_names:
    nice.append(teams.find_teams_by_full_name(team))
 
#print("THIS IS nice...", nice)

team_and_id = []

# Loop through each inner list in 'whoa'
for team_info in nice:
    # Check if the inner list is not empty
    if team_info:
        # Access the first (and only) dictionary in the inner list
        team = team_info[0]

        # Get the player's ID and other details
        team_id = team['id']
        team_name = team['full_name']
        team_and_id.append({'id': team_id, 'name': team_name})
    else:
        print(f"No team information found in this entry, {team_info}.")

#print("THIS IS team_and_id...", name_and_id)

request_count = 0
df = pd.read_csv(yFile_m)
df['win'] = 'No'
tFile_m = yFile_m+'_winResults.csv'
df.to_csv(tFile_m, index=False) 

for index, row in df.iterrows():
    team1 = row['line'].split(" vs")[0]
    print("1. -----------------")
    print("2. This is team1: ", team1)
    team1_id = teams.find_teams_by_full_name(team1)[0]['id']
    print("3. This is team1 id: ", team1_id)
    game_info = teamgamelog.TeamGameLog(team_id=team1_id, season='2023-24').get_data_frames()[0].iloc[0]
    #print("3.999. This is game_info: ", game_info)
    print("4. This is game_info[ID]: ", game_info['Game_ID'])
    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_info['Game_ID'])
    team_stats = boxscore.get_data_frames()[1]
    print(team_stats)

    # Check if team1_id matches home_team_id or visitor_team_id to determine home/away status
    home_team_id = team_stats['TEAM_ID'].iloc[0]
    away_team_id = team_stats['TEAM_ID'].iloc[1]
    
    if team1_id == home_team_id:
        home_team_points = team_stats['PTS'].iloc[0]
        print("5. This is home team points: ", home_team_points)
        away_team_points = team_stats['PTS'].iloc[1]
        print("6. This is away team points: ", away_team_points)
    elif team1_id == away_team_id:
        home_team_points = team_stats['PTS'].iloc[1]
        print("5. This is home team points: ", home_team_points)
        away_team_points = team_stats['PTS'].iloc[0]
        print("6. This is away team points: ", away_team_points)
    else:
        # Handle unexpected case where team1_id does not match either home or away team IDs
        print(f"Unexpected case: team1_id ({team1_id}) does not match home_team_id ({home_team_id}) or away_team_id ({away_team_id})")
        continue  # Skip to the next iteration

    total = home_team_points + away_team_points
    spread = abs(home_team_points - away_team_points)

    if row['market'] == 'h2h' and game_info['WL'] == 'W' and team1 == row['side']:
        print("7. This is h2h.")
        df.at[index, 'win'] = 'Yes'
    elif row['market'] == 'h2h' and game_info['WL'] == 'L' and team1 != row['side']:
        print("7. This is h2h.")
        df.at[index, 'win'] = 'Yes'

    if row['market'] == 'totals':
        print("7. This is total.")
        parts = row['line'].split(", ")
        line = parts[-1].split(" ")[-1]
        line = float(line)
        #print(line)
        if (total > line and row['side'] == 'Over') or (total < line and row['side'] == 'Under'):
            df.at[index, 'win'] = 'Yes'
        else:
            df.at[index, 'win'] = 'No'
            
    if row['market'] == 'spreads':
        print("7. This is spreads.")
        spread_line_full = row['line'].split(", ")[-1]
        team_betting_on_parts = spread_line_full.split(" ")
        team_betting_on = " ".join(team_betting_on_parts[:-1])
        print("7a. This is team betting on: ", team_betting_on)
        spread_line = spread_line_full.split(" ")[-1]
        print("7b. this is spread_line: ", spread_line)
        spread_line_number = float(spread_line)

        # Determine if the team you're betting on is the home team or away team
        betting_on_home_team = team_betting_on == team1
    
        # Calculate the effective spread based on who you're betting on
        if betting_on_home_team:
            effective_spread = home_team_points - away_team_points + spread_line_number
        else:
            effective_spread = away_team_points - home_team_points + spread_line_number

        # Determine win or loss based on the effective spread
        if effective_spread > 0:
            df.at[index, 'win'] = 'Yes'
        else:
            df.at[index, 'win'] = 'No'
    
    # line_parts = row['line'].split(",")
    # player_name = line_parts[0].strip()
    side = row['side']
    line = row['line'].split()[-1]
    if row['market'] != "h2h":
        line = float(line)

    time.sleep(2)
    # Increment the request counter
    request_count += 1

    # Pause execution after every 23 requests
    if request_count % 23 == 0:
        print("Pausing to avoid rate limits...")
        time.sleep(33)  # Pause for 60 seconds (1 minute)

df.to_csv(tFile_m, index=False)

current_directory = '.'
archive_directory = './archive'

# List all files in the current directory
for filename in os.listdir(current_directory):
    # Construct full file path
    file_path = os.path.join(current_directory, filename)
    
    # Determine if the file should be moved
    should_move = not (
        '_player' in filename or 
        '_matchup' in filename or 
        filename in (yFile_m, tFile_m) or
        'player' in filename
    ) and os.path.isfile(file_path)

    # Move the file to the archive directory if it doesn't meet any of the keep conditions
    if should_move:
        archive_path = os.path.join(archive_directory, filename)
        shutil.move(file_path, archive_path)
        print(f"Moved {filename} to {archive_directory}")
