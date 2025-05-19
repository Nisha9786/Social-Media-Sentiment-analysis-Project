import streamlit as st
import pandas as pd
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


# Twitter API credentials
def twitter_api_setup():
    API_KEY = 'e3UlIx62BvQpUZepNvoruL3lE'
    API_SECRET = '0N4lIFUWFWGRdW8D38c9XrKkZ6exTDxKcrYsm4R8WLWf321HxI'
    ACCESS_TOKEN = '1462342882711379971-e5rC25IgjtoOeXOvcPmzoHIA6wkDtb'
    ACCESS_SECRET = 'OBxs2dFxXdi30llGLhKjXp4YI3BLDRv8YeoZBEhhKTkV9'

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

# Sentiment Analysis Function
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

# Function to fetch tweets
def fetch_tweets(api, query,count=500):
    tweets = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(count):
        tweets.append([tweet.full_text, analyze_sentiment(tweet.full_text)])
    df = pd.DataFrame(tweets, columns=['Tweet', 'Sentiment'])
    return df
# Streamlit App
def main():
    st.title("Social Media Sentiment Analysis")
    st.sidebar.title("Options")

    option = st.sidebar.selectbox("Select Mode:", ("Upload CSV", "Fetch Live Tweets"))

    if option == "Upload CSV":
        st.subheader("Upload CSV File")
        file = st.file_uploader("Choose a CSV file", type="csv")

        if file is not None:
            df = pd.read_csv(file)
            st.write("Uploaded Data:", df.head())

            if 'Tweet' in df.columns:
                df['Sentiment'] = df['Tweet'].apply(analyze_sentiment)
                st.write("Sentiment Analysis Completed!")
                st.write(df.head())

                # Visualizations
                st.subheader("Sentiment Distribution")
                sentiment_counts = df['Sentiment'].value_counts()
                fig, ax = plt.subplots()
                sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
                st.pyplot(fig)

                st.subheader("Word Cloud")
                all_words = ' '.join(df['Tweet'])
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.error("CSV file must contain a 'Tweet' column.")

    elif option == "Fetch Live Tweets":
        st.subheader("Fetch Tweets from Twitter")
        query = st.text_input("Enter Keyword or Hashtag:")
        count = st.slider("Number of Tweets to Fetch", 10, 200, 100)

        if st.button("Fetch Tweets"):
            api = twitter_api_setup()
            df = fetch_tweets(api, query, count)
            st.write("Fetched Tweets:", df.head())

            # Visualizations
            st.subheader("Sentiment Distribution")
            sentiment_counts = df['Sentiment'].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
            st.pyplot(fig)

            st.subheader("Word Cloud")
            all_words = ' '.join(df['Tweet'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot()

if __name__ == "__main__":
    main()
    st.markdown("---")
    st.markdown("Design By : Nisha Singh -2025")
