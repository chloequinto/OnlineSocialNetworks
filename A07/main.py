'''
Chloe Quinto 

To Run: type into the terminal `python3 main.py`


TODO 
[X] Prompt the user for a Twitter User Screen Name.  If the user enters STOP, end the program with an appropriate message and stop.
[] Use the Twitter Screen Name to retrieve the following from the Twitter User Account and display them on the console with appropriate labels. 
[] Print the text of the Twitter User Account's most recent tweet, with appropriate label.
[] Print the screen names of thefirst 10followers of the Twitter User Account, with appropriate label. 
[] Prompt the user for the next Twitter User Screen Name, unless they enter STOP.
'''


import tweepy 

# Authentication Keys
CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Authenticate 
authenticate = tweepy.OAUthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authentivate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Avoid going over Twitter's Rate limits 
API = tweepy.API(authenticate, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

def getUser(user_screen_name): 
    '''
        Function gets information about a twitter user account information 
        Such as: 
        - User Name 
        - User Screen Name 
        - User ID 
        - User Description 
        - Number of Followers 
    '''
    try: 
        twitter_user = api.get_user(user_screen_name)
    except: 
        print("[ERROR] Could not get twitter user information")

def getMostRecentTweet()


if __name__ == "__main__":
    user_screen_name = input("What Twitter User Account do you want to analyze? Type \"STOP\" to end program")
    if (user_screen_name == "STOP"): 
        return 
    getUser(user_screen_name)