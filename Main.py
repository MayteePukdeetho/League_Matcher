from Helper_Functions import *
from Matcher import *

'''
If you want to try out some random accounts, here are some:
player_id = "Hide on bush"
tag_line = KR1
region = 3
Heres mine!
player_id = "NoPacksNeeded"
tag_line = "NA1"
region = 1




To be honest, this is like 12% done, I'll be working on it throughout the night, you can find the latest version here:
 https://github.com/MayteePukdeetho/League_Matcher

To summarize, the end goal of this is to:
Take 2 accounts
match them against eachother
see how well they would do if they hypothetically Duo-Queued up together

Right now, i only have stats to show "Hey, if your teammate plays this, then this is your winrate".
Theres more nuance including roles and stuff im not including.
The roadmap is basically is:
Store 75 games of data for both players - Done
Analyze the data to see what champions are most effective when played with them - Done
Cross reference that with the other players champion pool - Not Done
Compute score/hypothetical winrate - Not done
Not to mention UI and actual menu stuff.

'''
def intro():
    print("Hello! Welcome to the League of Legends Matcher. \n")
    print("To get started, I need some quick data about yourself, or, whoever your looking for. \n")
    player_id = input("Whats your player ID? (that would be the string before the #.)\n")
    tag_line = input("And whats your tagline? (the part after the #.)\n")
    region = region_finder()
    try:
        print("Okay, now lets see if we can find you in the database... \n")
        user_puuid = riot_ID_to_PUUID(region, player_id, tag_line, api_key)
    except Exception as e:
        print(f"Welp, something went wrong, back to the start we go! {e}")
        return intro()

    print("Valid User Found, making data... (This might take up to 2 minutes).")
    person_one_df = get_relevant_data(user_puuid, region, api_key)
    return person_one_df

def menu(person_one_df):
    while True:
        print("Okay, we got a bunch of data from your, or some other persons, account. Here is the implemented functionality so far: \n")
        print("0. Exit")
        print("1. Get winrate from recent games.")
        print("2. Get winrate from teammates champions.")
        print("3. Input someone elses account.")
        option = input("What would you like to know about your account?\n")

        if option == "3":
            data = intro()
            menu(data)
            break
        elif option == "2":
            person_one_teammates = favourite_champions(person_one_df)
            good_output = bug_catcher(person_one_teammates)
            if good_output == True:
                conclusion_maker(person_one_teammates, 2)
            else:
                pass
        elif option == "1":
            person_one_champions = main_champions(person_one_df)
            good_output = bug_catcher(person_one_champions)
            if good_output == True:
                conclusion_maker(person_one_champions, 1)
            else:
                pass
        elif option == "0":
            print("Thanks for using League of Legends matcher!")
            break

        else:
            print("Invalid input! Back from the top.")

data = intro()
menu(data)