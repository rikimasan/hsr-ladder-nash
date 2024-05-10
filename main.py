import json
import numpy
import csv

# load json data
with open('data/archetypes.json', 'r') as f:
    archetypes_array = json.load(f)
    archetypes = dict()
    for archetype in archetypes_array:
        archetypes[str(archetype["id"])] = archetype

with open('data/matchups.json', 'r') as f:
    matchups = json.load(f)["series"]

total_games = matchups["metadata"]["totals"]["total_games"]
# get a list of deck_ids with a significant number of games and ensure deck_ids are not negative or non-numeric
real_deck_ids = [deck_id 
                 for deck_id in matchups["metadata"] 
                 if deck_id.isdigit() 
                 and int(deck_id) >= 0 
                 and matchups["metadata"][deck_id]["total_games"] / total_games > 0.01]

#sort real_deck_ids by archetypes[deck_id]["player_class"]
real_deck_ids = sorted(real_deck_ids, key=lambda deck_id: archetypes[deck_id]["player_class"])

# create a matchup table of winrates such that matchup_table[deck1][deck2] = winrate of deck1 vs deck2
matchup_table = dict()
for p1_deck_id in real_deck_ids:
    matchup_table[p1_deck_id] = dict()  # Initialize the inner dictionary
    for p2_deck_id in real_deck_ids:
        matchup_table[p1_deck_id][p2_deck_id] = matchups["data"][p1_deck_id][p2_deck_id]["win_rate"]

# write matchup table to a csv
with open('matchup_table.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write header row
    header = [''] + [archetypes[deck_id]["name"] for deck_id in real_deck_ids]
    csvwriter.writerow(header)

    # Write data rows
    for p1_deck_id, row in matchup_table.items():
        row = [archetypes[p1_deck_id]["name"]] + [row[p2_deck_id] / 100 for p2_deck_id in real_deck_ids]
        csvwriter.writerow(row)

# filter classes from deck_ids
temp = list()
for deck_id in real_deck_ids:
    if archetypes[deck_id]["player_class_name"] not in []:
        temp.append(deck_id)
real_deck_ids = temp

# create the matchup table again but now with only the filtered classes
matchup_table = dict()
for p1_deck_id in real_deck_ids:
    matchup_table[p1_deck_id] = dict()  # Initialize the inner dictionary
    for p2_deck_id in real_deck_ids:
        matchup_table[p1_deck_id][p2_deck_id] = matchups["data"][p1_deck_id][p2_deck_id]["win_rate"]

# initialize popularity distribution of decks
popularity_distribution = dict()
for deck_id in real_deck_ids:
    popularity_distribution[deck_id] = 1

# iterate popularity distribution from estimated winrates
std_dev = 1
while std_dev > 0.0325:
    # calculate estimated winrates of decks with current probability distribution
    estimated_winrates = dict()
    for deck_id in real_deck_ids:
        estimated_wr = 0
        popularity_total = 0
        for matchup in matchup_table[deck_id]:
            estimated_wr += matchup_table[deck_id][matchup] * popularity_distribution[matchup]
            popularity_total += popularity_distribution[matchup]
        estimated_wr /= popularity_total
        estimated_winrates[deck_id] = estimated_wr

    played_estimated_winrates = list()
    for deck_id, popularity in popularity_distribution.items():
        if popularity > 0:
            played_estimated_winrates.append(estimated_winrates[deck_id])

    std_dev = numpy.std(played_estimated_winrates)
    mean = numpy.mean(played_estimated_winrates)

    for deck_id in real_deck_ids:
        if estimated_winrates[deck_id] > mean:
            popularity_distribution[deck_id] += 1
        if estimated_winrates[deck_id] < mean - std_dev and popularity_distribution[deck_id] > 0:
            popularity_distribution[deck_id] -= 1

sorted_decks = sorted(((deck_id, popularity, estimated_winrates[deck_id]) for deck_id, popularity in popularity_distribution.items()), key=lambda x: x[1], reverse=True)
for deck_id, popularity, ewr in sorted_decks:
    if popularity > 0:
        print(f"{archetypes[deck_id]['name']}: {popularity} (EWR: {ewr:.2f})")
