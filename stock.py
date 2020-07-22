import pandas as pd
from datetime import datetime,date, timedelta


print(type(str(date)))


class StockPrice:

    '''
    This class takes care of getting next day stock price to be used with sentiment score for final prediction.

    '''
    def __init__(self, stockName):
        '''
        Constructer function.
        '''
        self.stockName = stockName
        self.date = datetime.today()
        self.date += timedelta(days=1)
        self.date = self.date.strftime('%d-%m-%Y')
        self.date = str(self.date)
    
    def get_stock_price(self):
        '''
        This function return the next dat stock price predicted from the ARIMA model
        Stock names = [AxisBank]
        '''

        
        filename = self.stockName+'.csv'
        filePath = 'data/'+self.stockName + '/' + filename
        df = pd.read_csv(filePath)
        df.set_index('date',inplace =True)
        stock_price = df.loc[self.date]['predicted_price']


        return stock_price


   