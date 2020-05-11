'''
Chloe Quinto 

HW 7 - Using the Twitterr API to access Twitter Data 

Description: This python script is intended to use Twitter Data for data search/retrieval and processing/analysis. It utilizes Tweepy API 
To Run: type into the terminal `python3 main.py`

Dependencies: 
    - Install Tweepy 
    - Twitter Account 
    - Twitter Developer Account 

TODO 
[X] Prompt the user for a Twitter User Screen Name.  If the user enters STOP, end the program with an appropriate message and stop.
[X] Use the Twitter Screen Name to retrieve the following from the Twitter User Account and display them on the console with appropriate labels. 
[X] Print the text of the Twitter User Account's most recent tweet, with appropriate label.
[X] Print the screen names of thefirst 10followers of the Twitter User Account, with appropriate label. 
[X] Prompt the user for the next Twitter User Screen Name, unless they enter STOP.
'''


import tweepy 

# Authentication Keys
CONSUMER_KEY = ""
CONSUMER_KEY_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Authenticate 
authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Avoid going over Twitter's Rate limits 
API = tweepy.API(authenticate, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Global Variables 
screen_name = ""

# Rate Limit 
sleep_on_rate_limit = False

def getUser(user_screen_name): 
    '''
        Function gets information about a twitter user account information 
        Such as: User Name, User Screen Name, User ID, User Description, Number of Followers 
    '''

    global screen_name
    try: 
        twitter_user = API.get_user(user_screen_name)
        
        print("\n============================")
        # User Name 
        user_name = twitter_user.name

        # User Screen Name 
        screen_name = twitter_user.screen_name

        # User ID 
        user_id = twitter_user.id

        # User Description 
        user_description = twitter_user.description

        # Number of Followers
        num_followers =  twitter_user.followers_count

        print("User Name:", user_name)
        print("User Screen Name:", screen_name)
        print("User ID:", user_id)
        print("User Description:", user_description)
        print("Number of Followers:", num_followers)
        print("============================\n")

    except: 
        print("[ERROR] Could not get twitter user information")
    return None

def getMostRecentTweet():
    '''
        Function print the user's most recent tweet with appropriate label 
    '''
    global screen_name
    try: 
        print("============================")
        recent_tweet = API.get_user(screen_name = screen_name)
        print("Most Recent Tweet by " +  screen_name  + " \n" +  recent_tweet.status.text)
        print("============================\n")
    except: 
        print("[ERROR] Coult not get most recent twitter information")


def getFollowers(): 
    '''
        Function gets screen names of the first 10 followers of the Twitter User Account 
    '''
    global screen_name 
    print("============================")
    print("Screen Names of First 10 Followers of " + screen_name)
    try: 
        count = 0
        for users in tweepy.Cursor(API.followers, id = screen_name).items(): 
            if count == 10: 
                break 
            count += 1
            print("Follower " + str(count) + ": " + users.screen_name)
    except: 
        print("[ERROR] Could not get followers")

    print("============================\n")

    return None


if __name__ == "__main__":
    print("============================")
    user_screen_name = input("What Twitter User Account do you want to analyze? Type \"STOP\" to end program\n")

    while user_screen_name != "STOP": 
        getUser(user_screen_name)
        getMostRecentTweet()
        getFollowers()
        user_screen_name = input("What Twitter User Account do you want to analyze? Type \"STOP\" to end program\n")

    if user_screen_name == "STOP": 
        print("Sorry to see you go! Come back again!")
        exit()
    
    print("============================")