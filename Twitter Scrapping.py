import pandas as pd
import snscrape.modules.twitter as sntwitter

import json
import streamlit as st






st.set_page_config(page_title='Twitter Scrapping tool by Deepak Prem')
st.header('Twitter Scrapping Tool ')

# Creating list to append tweet data to
attributes_container = []

text = st.text_input('Enter the keyword to be searched')

Nos = st.number_input('How many tweets do you want? (Nos)',step=1)

startdate=st.date_input('Search from which date? (Enter Start date)')

enddate=st.date_input('Search till which date?(Enter the end date)')

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{text} since:{startdate} until:{enddate}').get_items()):
    if i > Nos:
        break
    attributes_container.append([tweet.date,tweet.id,tweet.rawContent,tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang , tweet.sourceLabel, tweet.likeCount])

# Creating a dataframe to load the list
tweets_df = pd.DataFrame(attributes_container, columns=["date", "id", "tweet content", "user","reply count", "retweet count","language", "source", "like count"])

tweets_df.to_csv(r'Searchresults.csv')
df = pd.read_csv(r'Searchresults.csv')
st.write(df)

if st.button('Upload into data base'):
  st.write(tweets_df.to_csv(r'Database.csv', mode='a'))

  print("Uploaded")


ds=pd.read_csv(r'Database.csv')

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
   "Download CSV File",
   csv,
   "Searchresults.csv",
   key='download-csv'
)



csv = convert_df(ds)

st.download_button(
   "Download Database CSV File (You can download the current one after uploading)",
   csv,
   "Database.csv",
   key='down-csv'
)

import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'id' to
            # be the primary key
            key = rows['id']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = r'Searchresults.csv'
jsonFilePath = r'Searchresults.json'
# Call the make_json function
make_json(csvFilePath, jsonFilePath)

json_string = json.dumps(jsonFilePath)

st.json(json_string, expanded=True)

st.download_button(
    label="Download Current JSON File",
    file_name="Searchresults.json",
    mime=r'Searchresults.json',
    data=json_string,
)
