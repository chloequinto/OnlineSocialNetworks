'''
Chloe Quinto 
CS 581 Online Social Networks 
HW 9 
I plege my honor that I have abided by the Stevens Honor System - Chloe Quinto 

!!! IMPORTANT: 
How to run 
1. cd into directory 
2. In terminal: run `python3 main.py`
3. Figures will pop up. Close out of window and you will see the next graph 
4. Keep doing so until the script have been finished. 

!!! MOST IMPORTANT: After finishing this script, please take a look at main.html. It's is an html version of this python script. It's a lot easier to read. 

!!! IMPORTANT: 
Dependencies: 
    - pandas 
    - matplotlib 
    - numpy 
    - statsmodels.api
    - seaborn
    - warnings 

Note: 
- This script was first made in a jupyter notebook and then converted to a python file. 
- It is much easier to see it on a jupyter notebook (please take a look at main.pdf)
- Plotting the graphs may take some time. 

'''


# Importing Libraries 
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Let's read in the file 
fb_data = pd.read_csv('FB_data.csv')

# Let's look at the top of the csv to get a better look 
fb_data.head()

# How big is the data set 
print(len(fb_data))


# Let's take a look at the current age dmographic 
plt.hist(fb_data['age'], color="green", ec="white", bins=100)
plt.title("Current Age Demographic")
plt.xlabel("Age")
plt.ylabel("Amount")
plt.savefig('output/0_AgeDemographic.png')
plt.show()

# we see that there's outliers where users are greater than 105, these are more likely fake ages 


# since there are "NA"s in gender, we need to drop rows where it includes it 
# Here we are going to look at the gender demographic 
fb_data.dropna(inplace=True)
plt.hist(fb_data["gender"])
plt.title("Current gender demographic")
plt.xlabel("Gender")
plt.ylabel("Amount")
plt.savefig('output/1_GenderDemographic.png')
plt.show()
print("Gender \n" + str(fb_data["gender"].value_counts()))


'''
Dunbar's Number

For this assignment, I want to focus on Dunbar's number. The theory goes that we can only really maintain about 150 connections at once. But does this still hold true for today's world of social media. 

I explore this topic with the facebook dataset and go over a few questions such as: 
1. Number of friends per user 
2. Friends count vs likes received 
'''


# Let's see the number of friends
plt.hist(fb_data["friend_count"], color="green", ec="white", bins=100)
plt.ylabel("Amount of Users")
plt.xlabel("Number of Friends")
plt.title("Friends Count")
plt.xlim(0,1100)
plt.savefig('output/2_numberOfFriends.png')
plt.show()

'''
For me personally, when I add friends on FB I don't necessarily interact with them so they really aren't "connections" per se. 
Let's see if there is any correlation to the number of friends that one has to the number of likes they receive.
We should expect to see a positive correlation between the number of friends one has with the number of likes a person gets. 
'''


plt.scatter(fb_data["friend_count"], fb_data["likes_received"])
plt.title("Friends Count vs Likes Received")
plt.xlim(0, 150)
plt.ylim(0,2000)
plt.xlabel("Friend Count")
plt.ylabel("Likes Received")
plt.savefig('output/3_friendsCountVsLikesReceived.png')
plt.show()

# Let's verify the results via stats - original linear regression 
results = sm.OLS(fb_data["likes_received"],sm.add_constant(fb_data["friend_count"])).fit()
print(results.summary())


# In[10]:


print("R2: ", results.rsquared)


# Looks like there is a weak positive correlation between  likes received and a user's friend count 

# Let's look at the linear regression line 
print("y="+str(results.params[1]) + "*x + " + str(results.params[0]))

# Let's plot the same thing as before but with a linear regression line 
plt.scatter(fb_data["friend_count"], fb_data["likes_received"])
plt.plot(fb_data["friend_count"], results.params[1]*fb_data["friend_count"]+results.params[0], color="red", linewidth=4)
plt.xlim(0, 150)
plt.ylim(0,2000)
plt.title("Friends Count vs Likes Received")
plt.xlabel("Friend Count")
plt.ylabel("Likes Received")
plt.savefig('output/4_friendsCountVsLikesReceived.png')
plt.show()

'''
We can't confidently say that the more friends you have the more likes you receive. 
This may be due to the nature of Facebook. Most users, including me, use it as a way of messaging 
communication rather than reading posts and liking them. As opposed to instagram, where the intention is to give and 
receive likes and comments. 

''' 

'''
Another question to look at it: 
    
If you're more likely to initiate friendships, are you more likely receive likes?
'''

sns.relplot(x="friendships_initiated", y="likes_received", data=fb_data, hue="gender")
plt.savefig('output/5_InitiateFriendsVsLikesOnFacebook.png')
plt.plot()

'''
That's interesting. The more friends you initiate, the less likes you get. 

Dunbar's theory says that you should have 500 acquaintances and 1500 people you can recognize. The numbers on the x-axis go all the way up to 4000 which is 
beyond the people you could possibly recognize. After 1500 friends, they are not a strong connection. 

Let's just verify the results with stats: 
'''



results = sm.OLS(fb_data["likes_received"],fb_data["friendships_initiated"]).fit()
print(results.summary())

print('R2: ', results.rsquared)
print('Parameters: ', results.params)


'''
Another question we could ask: 
Do females or males get more likes on facebook? 
'''


# In[16]:

plt.figure()
sns.boxplot(y='gender', x='likes_received', data=fb_data, hue='gender', orient='h').set_xlim([-20, 400])
plt.savefig('output/6_likesReceivedVsGender.png')
plt.show()

# In general, we see that females have a wider range of likes recieved than males. Another way you can look at it is:  

# In[17]:


sns.barplot(y="gender", x="likes_received", data=fb_data)
plt.savefig('output/7_LikeReceivedVsGender.png')
plt.show()



# So, this shows us overall, females receive more likes than males. Another view: 

# In[18]:


sns.relplot(x='friend_count', y='likes_received', data=fb_data, hue='gender')
plt.show()
plt.savefig("output/8_FriendCountVsLikesReceived.png")
