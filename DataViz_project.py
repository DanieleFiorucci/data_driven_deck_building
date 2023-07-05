#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing the libraries
import requests
import pandas as pd
import json 
import numpy as np



#########################################
#########################################
#########################################
############                 ############
############    TASK 3.1     ############
############                 ############
#########################################
#########################################
#########################################



# retrieving the dataset from the api
url='https://db.ygoprodeck.com/api/v7/cardinfo.php'
response= requests.request('GET', url)
print(response.text) # returns the data retrieved 
print(response.ok) #boolean value that say to you if th import went ok
print(response.status_code) 
# creating a json file in wrtie mode and then writing on it the retrieved data
response_file = open("dataset.json", 'w')
response_file.writelines(response.text)
response_file.close()
# opening in read mode the just created json file and successively loading it
# in the python environment as dictionary 
response_file_r = open("dataset.json", 'r')
j=json.load(response_file_r)
# transforming the json data corresponding to the key "response" into a DataFrame 
#df=pd.DataFrame.from_dict(j1["results"])

# Extract the 'data' field from the JSON data
results = j['data']

# Create a DataFrame from the 'data' field
df = pd.json_normalize(results)

# Print the DataFrame
print(df)

# understanding the dataset
df.shape
df.columns
df.dtypes
df.describe()
# checking for null
df.isnull().sum()

# our API is about yu-gi-oh cards. It has 12462 observations and 20 columns,
# 5 of them are floats columns while the others are categorical variable or
# populate dby ictionaries as usually happens when dealing with json files.
# As always happens in our dataframe not all columns are usefull for our visualization task.
# In the following lines of code we will clean the dataset, work on the dictionaries and 
# drop the less sefull columns.

#########################################
#########################################
#########################################
#########################################
# looking at the dataset can be noticed that there are some columns that are
# populated by dictionaries. In the following lines of code we worked in order
# to extract the informations from the dictionaries.

# the columns over which we worked on are 'card_prices' where there are the
# prices of the cards according to different websites and card image


cardmarket_price=[]
coolstuffinc_price=[]
tcgplayer_price=[]
ebay_price=[]
amazon_price=[]
for d in df['card_prices']:
    if d is not np.nan:
        cardmarket_price.append(d[0]['cardmarket_price'])
        coolstuffinc_price.append(d[0]['coolstuffinc_price'])
        tcgplayer_price.append(d[0]['tcgplayer_price'])
        ebay_price.append(d[0]['ebay_price'])
        amazon_price.append(d[0]['amazon_price'])
    else:
        cardmarket_price.append(np.nan)
        coolstuffinc_price.append(np.nan)
        tcgplayer_price.append(np.nan)
        ebay_price.append(np.nan)
        amazon_price.append(np.nan)
        
df['cardmarket_price']=cardmarket_price
df['coolstuffinc_price']=coolstuffinc_price
df['tcgplayer_price']=tcgplayer_price
df['ebay_price']=ebay_price
df['amazon_price']=amazon_price
df.drop('card_prices', axis=1, inplace=True)

# since all these 5 columns represent the same thing we decide to discard 4 of them.
# we only keep 'cardmarket_price' because it is the most reliable and used by
# card game players 

df.drop(['coolstuffinc_price', 'tcgplayer_price', 'ebay_price', 'amazon_price'],
        axis=1, inplace=True)

# going on with the datafarme cleaning we decided to drop other columns that
# we thought to be not relevant for our analysis 
df.columns

df.drop(['card_images','scale', 'linkval', 'linkmarkers'], axis=1, inplace=True)


# to handle the three columns about the banlist we thought that
# visualizing the null values in each column and the different categories that
# are in them
df.groupby('banlist_info.ban_ocg').size()
df.groupby('banlist_info.ban_goat').size()
df.groupby('banlist_info.ban_tcg').size()
df['banlist_info.ban_tcg'].isnull().sum()# this has the least number of Nulls
df['banlist_info.ban_ocg'].isnull().sum()
df['banlist_info.ban_goat'].isnull().sum() 

# we than decicded to keep only banlist_info.ban_tcg
df.drop(['banlist_info.ban_goat', 'banlist_info.ban_ocg'], axis=1, inplace=True)




# in dealing with the column 'card_sets' we undertook a different approach.
# we wanted to extract only the name of the deck so we created a function
# in order to extract the deck name and to assign it to a new column in the dataframe

# in the first step we created the function and than to create a new column
# in which for each card there is a list of all the decks in which that card is in
def extract_set_names(row):
    if isinstance(row['card_sets'], list) and len(row['card_sets']) > 0:
        set_info_list = row['card_sets']
        return [card_sets['set_name'] for card_sets in set_info_list]
    else:
        return np.nan

# apply the function to each row and create a new column with the extracted values
df['set_names'] = df.apply(extract_set_names, axis=1)


def extract_reraity(row):
    if isinstance(row['card_sets'], list) and len(row['card_sets']) > 0:
        set_info_list = row['card_sets']
        return [card_sets['set_rarity'] for card_sets in set_info_list]
    else:
        return np.nan

df['set_rarity'] = df.apply(extract_reraity, axis=1)


# this lines of code connect each card to its deck. Each card is repeated more times 
# according to the number of decks it is part of
df_exploded = df.explode(['set_names', 'set_rarity'])
df_exploded.reset_index(drop=True, inplace=True)
df.drop('card_sets', axis=1, inplace=True)
df_exploded.drop('card_sets', axis=1, inplace=True)
# this dataset will be used later on for visualization purposes



# last step to be performed once we dropped all the less usefull columns,
# is to check for NAs
df.isnull().sum()
df_exploded.isnull().sum()
# all the NAs that are in both dataframes can be accepted because there are
# some cards, like spell, trap and magic cards, don't have atk, def, level or
# archetype because these are features that usually belong to cards that are of
# the 'monster' type. So these are missing values that are there for because of
# how the yu-gi-oh game is built. The other NAs are in the column 'banlist_info.ban_tcg';
# this is due to the fact that only few cards of the game have been banned or restricted.
# The only missing values that can be taken off are the one in the set_names
# columns because it makes no sense that a cards doesn't belong to any set. 
df.dropna(subset=['set_names'], inplace=True)
df_exploded.dropna(subset=['set_names'], inplace=True)


# in order to import easly the dataframes created in this python file we
# finally exported all of them in the csv format


### Extracting the type of the cards and storing it in short
# Define a regex pattern to match the desired strings
pattern = r'(Monster|Pendulum|Synchro|Ritual)'
dff=df.copy()
# Extract the matching string into a new column
df['type_short'] = df['type'].str.extract(pattern)

# Remove the matched pattern from the original column
df['type'] = df['type'].str.replace(pattern, '')

df['type_short'] = df['type_short'].fillna(df['type'])

#df.to_csv('yu-gi-oh.csv', index=False)
#df_exploded.to_csv('df_exploded.csv', index=False)

df.to_csv('yu-gi-oh.csv', index=False)
df_exploded.to_csv('df_exploded.csv', index=False)


 
 
 
 
 
 
