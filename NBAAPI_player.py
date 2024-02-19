import pandas as pd
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.static import players
import os, shutil, time

# yes = players.find_player_by_id(1630231)
# print(yes)

#Change these first before daily run
yFile_p = 'playerOutput_2_13_24.csv'

importedResultsCSV = pd.read_csv(yFile_p)

request_count = 0
df = pd.read_csv(yFile_p)
print("Hello")
for index, row in df.iterrows():
    line_parts = row['line'].split(",")  # Split the string at the comma
    player_name = line_parts[0].strip()  # Extract the player name

    # Update the player name if it matches a certain condition
    if player_name == "Cam Johnson":
        player_name = "Cameron Johnson"
    if player_name == "Lonnie Walker":
        player_name = "Lonnie Walker IV"
    if player_name == "Dereck Lively":
        player_name = "Dereck Lively II"
    if player_name == "T.J McConnell":
        player_name = "T.J. McConnell" #204456
    if player_name == "Bruce Brown Jr":
        player_name = "Bruce Brown" #1628971
    if player_name == "Jabari Smith":
        player_name = "Jabari Smith Jr."
    if player_name == "Kenyon Martin Jr.":
        player_name = "KJ Martin"     
    if player_name == "Danuel House":
        player_name = "Danuel House Jr."

    if row['side'] == 1:
        df.at[index, 'side'] = 'Over'
    elif row['side'] == 2:
        df.at[index, 'side'] = 'Under'

    # Reconstruct the 'line' string with the updated player name
    updated_line = f"{player_name},{','.join(line_parts[1:])}"
    df.at[index, 'line'] = updated_line

df['win'] = 'No'
tFile_p = yFile_p+'_winResults.csv'
df.to_csv(tFile_p, index=False)
df = pd.read_csv(tFile_p)

# Function to extract the name from each line
def extract_name(line):
    if " Over" in line:
        return line.split(", Over")[0]
    elif " Under" in line:
        return line.split(", Under")[0]
    else:
        return line

names = [extract_name(line) for line in df['line']]
#print("THIS IS names...", names)

whoa = []

for name in names:
    whoa.append(players.find_players_by_full_name(name))
 
#print("THIS IS whoa...", whoa)

name_and_id = []

# Loop through each inner list in 'whoa'
for player_info in whoa:
    # Check if the inner list is not empty
    if player_info:
        # Access the first (and only) dictionary in the inner list
        player = player_info[0]

        # Get the player's ID and other details
        player_id = player['id']
        full_name = player['full_name']
        name_and_id.append({'id': player_id, 'name': full_name})

    else:
        print(f"No player information found in this entry, {player_info}.")

#print("THIS IS name_and_id...", name_and_id)

for index, row in df.iterrows():
    line_parts = row['line'].split(",")
    player_name = line_parts[0].strip()
    side = row['side']
    line = row['line'].split()[-1]
    line = float(line)  

    # Find player ID from name_and_id
    player_id = None
    for player_info in name_and_id:
        if player_info['name'] == player_name:
            player_id = player_info['id']
            break

    # Retrieve game logs directly into a DataFrame
    player_last_game = playergamelogs.PlayerGameLogs(
        player_id_nullable=str(player_id),
        season_nullable='2023-24',
        last_n_games_nullable=0
    ).get_data_frames()[0]

    # Check if the DataFrame is not empty
    if not player_last_game.empty:
        last_game_pts = player_last_game["PTS"].values[0]
        #print(f"Type of last_game_pts!!!!!: {type(last_game_pts)}")

    # Determine if the bet was won
    if (side == 'Over' and last_game_pts > line) or \
        (side == 'Under' and last_game_pts < line):
        df.at[index, 'win'] = 'Yes'

    # Extract points (PTS) from the last game
    pts = player_last_game["PTS"].values[0] if not player_last_game.empty else "N/A"

    # Print the player's name and points
    print(player_name, pts, line, side)

    # Increment the request counter
    request_count += 1

    # Pause execution after every 23 requests
    if request_count % 23 == 0:
        print("Pausing to avoid rate limits...")
        time.sleep(33)  # Pause for 60 seconds (1 minute)

df.to_csv(tFile_p, index=False)

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
        filename in (yFile_p, tFile_p) or
        'matchup' in filename
    ) and os.path.isfile(file_path)

    # Move the file to the archive directory if it doesn't meet any of the keep conditions
    if should_move:
        archive_path = os.path.join(archive_directory, filename)
        shutil.move(file_path, archive_path)
        print(f"Moved {filename} to {archive_directory}")
