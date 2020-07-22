
import GetOldTweets3 as got
import pandas as pd
from datetime import date, timedelta
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class Sentiment:
    
    '''
    This class takes care of all task for Sentiment score calculation. The tasks includes scraping of tweets,
    then clean them and use them to get the sentiment score of the day.
    '''
    def __init__(self, mentions):
        '''
        Constructer function.
        '''
        self.username = ["@EconomicTimes","@NDTVProfit","@ETNOWlive","@BT_India","@BloombergQuint","@ETMarkets","@livemint","@bsindia"]
        self.date = str(date.today())
        self.mentions =mentions
   
    def get_clean_tweets(self,tweet):
        """
        This function takes raw text from tweets and cleans them by removing the hashtags, any twitter mentions
        and any hyperlink that present in the tweet and returns a cleaned text in string format.

        :rtype: string
        """ 
        cleaned_tweet = re.sub(r'#', '', tweet)
        cleaned_tweet = re.sub(r'@', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'htt(p|ps)\S*', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'RT', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'[^a-zA-Z ]','',cleaned_tweet)
        
        return cleaned_tweet


    def get_tweets(self):
        '''
        This function scrapes tweets from a given set of tweeter handles.
        The querry may contain hashtags or twitter mentions. It uses starting and ending date to 
        to scrape the tweets for a time frame.

        Input parameters :
        "username" : Stores the tweeter handles(in a list) to search from
        "date" : today's date
        "mentions" : all hashtags or tweeter mentions in a list

        rtype :
        It will return a pandas dataframe containing the columns, 'date','source','tweet'.
        '''
        try:
            tweets_list = []
            for mention in self.mentions:
                tweetCriteria = got.manager.TweetCriteria().setUsername(self.username)\
                                                        .setQuerySearch(mention)\
                                                        .setSince(self.date)
                tweets = got.manager.TweetManager.getTweets(tweetCriteria)
                tweets_list.append(tweets)

            #print("Tweets are fetched sucessfully...")
        
        except Exception as e:
            print("Runtime error in tweet extraction in Bank.get_tweets()")
            print(e)


        try:
            df = pd.DataFrame(columns = ['Text'])
            for tweets in tweets_list:
                temp_df = pd.DataFrame([[tweet.text] for tweet in tweets], columns = ['Text'])
                df = pd.concat([df, temp_df], ignore_index = True)

            df.drop_duplicates(keep = 'first', inplace = True)
            df['Text'] = df['Text'].apply(self.get_clean_tweets)
               
        except Exception as e:            
            print("Runtime error in DataFrame creation")
            print(e)
        
        return df
    
    
    def calculate_score(self,tweet):
        '''
        This function calculates the polarity score of a given tweet.
        
        Input parameters :
        "username" : raw tweet
        
        rtype :
        It will return the polarity score of the given tweet.
        '''
        sentiment = SentimentIntensityAnalyzer()
        return sentiment.polarity_scores(str(tweet))["compound"]

    def get_sentiment_score(self):

        tweets = self.get_tweets()
        tweets['score'] = tweets['Text'].apply(self.calculate_score)
        #print(tweets.head())
        score = tweets['score'].mean(axis = 0, skipna = True)
        
        if str(score) == 'nan':
            return 0
        else:
            return score



