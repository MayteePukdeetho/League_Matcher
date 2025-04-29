import pandas as pd

from Helper_Functions import *
def get_relevant_data(puuid, region, api_key):
    '''
    Using some other functions to get relevant data to be used in the main algorithim
    :param puuid:
    :param region:
    :param api_key:
    :return:
    '''
    dict_to_be_conveted = {
        'Teammates' : [],
        'Played' : [],
        'Won' : [],

    }
    all_matches = PUUID_to_Matches(puuid, region, api_key, games = 75)
    for match in all_matches:
        match_data = Matches_to_Match_Data(region, match, api_key)
        teammates, played, won = Team_Comp_Finder(match_data, puuid)
        dict_to_be_conveted['Teammates'].append(teammates)
        dict_to_be_conveted['Played'].append(played)
        dict_to_be_conveted['Won'].append(won)

    synergy_dataframe = pd.DataFrame(dict_to_be_conveted)
    return synergy_dataframe


def favourite_champions(puuid, region, api_key):
    '''
    Gets a persons favourite champions to play with (not necessarily play themselves by reformatting to dataframe from
    get_relevant_data, then creating a new summary one.) Filters for champions with 5 or more matches.
    :param puuid:
    :param region:
    :param api_key:
    :return:
    '''
    synergy_dataframe = get_relevant_data(puuid, region, api_key)
    reformatted_row = []
    for idx, row in synergy_dataframe.iterrows():
        teammates = row['Teammates']
        won = row['Won']
        for teammate in teammates:
            reformatted_row.append({'Teammate' : teammate, 'Won': won})

    reformatted_dataframe = pd.DataFrame(reformatted_row)

    summary = reformatted_dataframe.groupby('Teammate').agg(
        games = ('Won', 'count'),
        wins = ('Won', 'sum'),
    ).reset_index()

    summary['win_rate'] = (summary['wins'] / summary['games']) * 100

    summary = summary[summary['games'] >= 5]

    return summary.sort_values(by='win_rate', ascending=False)

print(favourite_champions(my_puuid, 'americas', api_key))

