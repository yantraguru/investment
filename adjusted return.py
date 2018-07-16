# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:41:48 2017

@author: Adwait
"""

import numpy as np
import pandas as pd
import matplotlib
%matplotlib inline

infy_data = pd.read_csv('D:\\work3\\post\\WIPRO.csv', index_col = 0, parse_dates = True,
            usecols = ['Date','Close Price'],dtype= {'Close Price':np.float64})
infy_data = infy_data.sort_index()  
            
infy_stock_split_data = pd.read_csv('D:\\work3\\post\\WIPRO_split.csv',
                                   index_col = 4, parse_dates = True )
infy_stock_split_data['adjustment_factor'] = infy_stock_split_data['Old FV']/infy_stock_split_data['New FV']
infy_stock_split_data['adjustment_event']  = 'Split'

infy_stock_bonus_data = pd.read_csv('D:\\work3\\post\\WIPRO_bonus.csv',
                                    index_col = 4, parse_dates = True )
                                    
infy_stock_bonus_data['adjustment_factor'] = infy_stock_bonus_data['New Holding']/infy_stock_bonus_data['Old Holding']                                
infy_stock_bonus_data['adjustment_event']  = 'Bonus'

infy_dividend_data = pd.read_csv('D:\\work3\\post\\WIPRO_dividend.csv', index_col = 1,parse_dates = True)
infy_dividend_data = infy_dividend_data.merge(infy_data, left_index=True, right_index=True, how='left')
infy_dividend_data['adjustment_factor'] = (infy_dividend_data['Close Price'] +  infy_dividend_data['Dividend per share'])/infy_dividend_data['Close Price']
infy_dividend_data['adjustment_event']  = 'Dividend'

infy_div_rein_data = infy_dividend_data.loc[:,['Dividend per share','Close Price','adjustment_event']]
infy_div_rein_data['adjustment_factor'] = 1 + (infy_div_rein_data['Dividend per share']/infy_div_rein_data['Close Price'])

class Price_History:

    def __init__(self, price_data):
        self.price_data = price_data.copy()
        self.price_data['adjusted_price'] = self.price_data['Close Price']
        self.price_data['adjustment_event'] = ''        
        
    def get_price_history(self):
        return self.price_data
        
    def adjust_price(self,adjustment_data):
        adjustment_data = adjustment_data.sort_index()
        
        for event_date,adjustment_factor,adjustment_event in adjustment_data[['adjustment_factor','adjustment_event']].itertuples():
            if event_date in self.price_data.index:
                self.price_data.loc[self.price_data.index < event_date,'adjusted_price'] = self.price_data.loc[self.price_data.index < event_date,'adjusted_price']/adjustment_factor
                self.price_data.set_value(event_date,'adjustment_event',adjustment_event)
            else:
                print 'Event date %s not found' % str(event_date)
        
        return self.price_data
        
class Stock(object):

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.price_history = Price_History(pd.DataFrame(columns=['Close Price']))
    
    def set_Price_History(self,price_data):
        self.price_history = price_data.copy()
        
    def get_Price_History(self,price_data):  
        return self.price_history

infy_price_history = Price_History(infy_data)        
infy_price_history.adjust_price(infy_stock_split_data)
infy_price_history.adjust_price(infy_stock_bonus_data)                
infy_price_history.adjust_price(infy_dividend_data)
infy_adjusted_data = infy_price_history.adjust_price(infy_div_rein_data)

infy_adjusted_data['adjusted_price'].plot(figsize=(10,6))
        