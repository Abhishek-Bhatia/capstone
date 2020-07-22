from sentiment import Sentiment
from stock import StockPrice
from sklearn.ensemble import RandomForestRegressor
import pickle 
import pandas as pd



class Prediction:
    '''
    This class used data from Arima prediction and Sentiment score to predict the final prediction.
    This class unpickles the RandomForest Regressor model and uses to predict the final stock price
    It will accept the stock name and its hashtags in a list format
    '''

    def __init__(self, stock):
        '''
        Constructer function.
        
        '''
        self.stockName = stock[0]
        self.hashtags =  stock[1]

    def get_final_price(self,pred_data):
        filename = self.stockName+'.txt'
        filePath = 'data/'+ self.stockName +'/'+ filename
        file = open(filePath,'rb')
        model = pickle.load(file)

        final_price = model.predict(pred_data)

        return final_price




    def get_final_prediction(self):
        '''
        This method will create objects for sentiment and stock class to get the sentiment score 
        and prediction price and use them to predict the final 
        '''

        sc = Sentiment(self.hashtags)
        sentiment_score = sc.get_sentiment_score()
        #print(sentiment_score)

        sp = StockPrice(self.stockName)
        stock_price = sp.get_stock_price()
        #print(stock_price)

        #data = pd.DataFrame({'stock_price':[sentiment_score],'stock_price':[stock_price]})
        data = pd.DataFrame({'sentiment_score':[sentiment_score],'stock_price':[stock_price]})

        #print(self.get_final_price(data))
        return self.get_final_price(data)




