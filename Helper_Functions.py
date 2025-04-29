import requests
import pandas as pd
import time

'''
READ!!!!!!!!!! VERY IMPORTANT!!!!!!!!!!
API KEY EXPIRES EVERY 24 HOURS, NEEDS MANUAL GENERATION.
TO GENERATE OWN API KEY: 
https://developer.riotgames.com/
MAKE AN ACCOUNT HERE, AND CLICK ON YOUR USERNAME ON THE TOP RIGHT, COPY AND PASTE IT INTO THE STRING BELOW
I WILL ALSO BE UPDATING THIS IN GITHUB DAILY UNTIL THE END OF THE SEMESTER:
GITHUB LINK:
https://github.com/MayteePukdeetho/League_Matcher
'''
'''
Essentially most of these functions are:
what type of data you are inputting ->
oh you need this link to get the data ->
request data using requester ->
get the data your looking for
'''


api_key = "RGAPI-0ba4d851-6947-4ac1-9737-cf14446e82be"
def requester(api_url):
    '''
    This calls the api for us using the url provided and checks if we're being rate limited or not.
    If we are, then it stops for 60 seconds and tries again.
    :param api_url:
    :return:
    '''
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            print("rate limited, Riot API gives us 200 calls for 2 minutes... Trying again in 1 minute.")
            time.sleep(60)
        else:
            return resp

def riot_ID_to_PUUID(region, game_name, tag_line, api_key ):
    """
    Calls the riot API to get a persons PUUID (needed for other API calls) from a username).
    :param region: '
    :param game_name: This is a username like 'john_852'
    :param tag_line:
    :param api_key:
    :return:
    """
    api_url = ("https://" + region + ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/" +
               game_name + "/" + tag_line +
               "?api_key=" + api_key)

    resp = requester(api_url)
    player_info = resp.json()
    print(player_info)
    puuid = player_info['puuid']
    return puuid

my_puuid = riot_ID_to_PUUID("americas", "I will trade", "NA1", api_key)

def PUUID_to_Matches(puuid, region, api_key, games = 75):
    """
    Given a puuid and a players region, return their 50 most recent matches (can go up to 100 before being
    rate limited)
    :param puuid:
    :param region:
    :param api_key:
    :param games:
    :return: a list of the 20 most recent matches as match ids.
    """

    api_url = ("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
              puuid +
               "/ids?start=0" +
               "&count=" +
               str(games) +
               "&api_key=" + api_key)
    resp = requester(api_url)
    matches = resp.json()
    return matches

print(PUUID_to_Matches(my_puuid, "americas", api_key))

matches_to_analyze = PUUID_to_Matches(my_puuid, "americas", api_key)


'''
A quick sidenote of RIOT API matchdata:
Essentially it's a really, really, big dictionary, made out of two, big dictionaries.
The first one is metadata, which basically shows the match_id and the participants using their puuid.
The second one is info, where, well, the info of the game is held. I'll be commenting on what each line does throughout.
Most keys are self-explanatory.
'''

def Matches_to_Match_Data(region, match_id, api_key):
    """
    gets data about a certain match.
    :param match_id:
    :param puuid:
    :return: a really, really, big dictionary.
    """
    api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/match/v5/matches/" +
            match_id +
            "?api_key=" +
            api_key
    )

    resp = requester(api_url)
    match_data = resp.json()
    return match_data

print(Matches_to_Match_Data("americas", matches_to_analyze[0], api_key))
match_data = Matches_to_Match_Data("americas", matches_to_analyze[0], api_key)

def Match_Data_To_Player_Data(match_data, puuid):
    """
    From someones match data, get a certain players data.
    :param match_data:
    :param puuid:
    :return: a slightly smaller dictionary.
    """

    #get everyones puuid
    participants = match_data['metadata']['participants']
    #match it with the one we provided
    player_index = participants.index(puuid)
    #get the data we want
    player_data = match_data['info']['participants'][player_index]

    return player_data

def Team_Comp_Finder(match_data, puuid):

    team_comp = []
    player_of_interest = None

    #for everyone....
    for participant in match_data['info']['participants']:
        if participant['puuid'] == puuid:
            player_of_interest = participant
            #this is what champion the target played.
            champion_played = participant['championName']
            break

    if player_of_interest is None:
        raise ValueError("puuid is incorrect")

    team_of_interest = player_of_interest['teamId']

    for participant in match_data['info']['participants']:
        if participant['teamId'] == team_of_interest and participant['puuid'] != puuid:
            team_comp.append(participant['championName'])


    #Did they win as a true or false.
    winner = player_of_interest['win']
    return team_comp, champion_played, winner



