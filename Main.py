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

To be honest, this is like 10% done, I'll be working on it throughout the night, you can find the latest version here:
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

print("Hello! Welcome to the League of Legends Matcher. \n")
print("To get started, I need some quick data about yourself, or, whoever your looking for. \n")
player_id = input("Whats your player ID? (that would be the string before the #.)\n")
tag_line = input("And whats your tagline? (the part after the #.)\n")
region = input("What is your region?\n"
               "Type in 1 for in the Americas, 2 for Europe, 3 for Asia, and 4 for SEA (and OCE regions). \n")
region = int(region)
if (region != 1) and (region != 2) and (region != 3) and (region != 4):
    print("Invalid input. Please try again.")
elif region == 1:
    region = "americas"
elif region == 2:
    region = "europe"
elif region == 3:
    region = "asia"
elif region == 4:
    region = "sea"
try:
    print("Okay, now lets see if we can find you in the database... \n")
    user_puuid = riot_ID_to_PUUID(region, player_id, tag_line, api_key)
except:
    print("Welp, something went wrong, back to the start we go!")

print("Alright.... Lets Calculate some data about ya....")
print("")

print(favourite_champions(user_puuid, region, api_key))
