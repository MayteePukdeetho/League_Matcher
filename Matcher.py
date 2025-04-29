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


def favourite_champions(synergy_dataframe):
    '''
    Gets a persons favourite champions to play with (not necessarily play themselves by reformatting to dataframe from
    get_relevant_data, then creating a new summary one.) Filters for champions with 5 or more matches.
    :param synergy_dataframe:
    :return:
    '''
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
    summary = threshold_filterer(summary)
    if len(summary) <= 0:
        return None
    summary = summary.sort_values(by='win_rate', ascending=False).reset_index(drop=True)
    print(summary)
    return summary


def main_champions(synergy_dataframe):
    """
    Gets a persons favourite champions to play (reformatting to dataframe from
    get_relevant_data, then creating a new summary one.) Filters for champions with 5 or more matches.
    :param synergy_dataframe:
    :return:
    """
    reformatted_row = []

    for idx, row in synergy_dataframe.iterrows():
        played = row['Played']
        won = row['Won']
        reformatted_row.append({'Played' : played, 'Won': won})
    reformatted_dataframe = pd.DataFrame(reformatted_row)

    summary = reformatted_dataframe.groupby('Played').agg(
        games=('Won', 'count'),
        wins=('Won', 'sum'),
    ).reset_index()

    summary['win_rate'] = (summary['wins'] / summary['games']) * 100
    summary = threshold_filterer(summary)
    if len(summary) <= 0:
        return None
    summary = summary.sort_values(by='win_rate', ascending=False).reset_index(drop=True)
    print(summary)
    return summary


'''
Oh, I just realized I could probably have bans here as well. I'll add that later.
'''
def comparer(list_of_dataframes):
    everyone_champ_pool = []
    everyone_teammates_pool = []
    for dataframe in list_of_dataframes:
        if 'Teammates' in dataframe.columns:
            hashable_data_type = []
            for teammate in dataframe['Teammates']:
                hashable_data_type.extend(teammate)
            x_person_preferred = set(hashable_data_type)

            everyone_teammates_pool.append(x_person_preferred)

        if 'Played' in dataframe.columns:
            x_person_played = set(dataframe['Played'])
            everyone_champ_pool.append(x_person_played)


    shared_champ_pool = set.union(*everyone_champ_pool)
    shared_teammates_pool = set.union(*everyone_teammates_pool)

    return shared_champ_pool, shared_teammates_pool