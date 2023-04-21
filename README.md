# hsr ladder nash
Creates a CSV of matchups for decks with a significant number of games and find the popularity distribution for the nash equilibrium of ladder given the current deck matchup winrates.

Really just made for myself, but figured others could get some use out of this if they wanted. Instructions are kinda incomplete but wtv, you probably should actually read the code as well since there are a couple of useful values you can change.

The matchups json included in the repo is for the free bronze through gold stats, don't expect meaningful data about the meta out of it.

Finally, remember that stats are only a tool and can't capture many aspects of the game like how deck builds change in response to meta changes among other things, just because an unpopular deck is present at the top of the nash equalibrium doesn't mean it actually deserves to be the top deck in the game. 

## Usage
Get stats .json files from hsreplay.net by doing the following: 
- log in to your hsreplay account
- visit this [link](https://hsreplay.net/api/v1/archetypes/?hl=en) for the archetypes.json
- visit this [link](https://hsreplay.net/analytics/query/head_to_head_archetype_matchups_v2/?GameType=RANKED_STANDARD&LeagueRankRange=LEGEND&Region=ALL&TimeRange=CURRENT_PATCH) for matchups.json

The second link needs hsreplay premium, since it fetches legend stats for the current patch, you can get alternative stats by going to the website and looking in the browser debugger for the fetching http request with the stats filters you have selected. I wouldn't use anything below legend stats though. Top 1k is usually too sparse data leaving some decks unseen.