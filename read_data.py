#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 16:39:04 2021

@author: lolus
"""

#%%

#pip install yfinance
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import datetime


##
# 1. ha funktion som tar in och läser data från olika bolag och du specificera tid. 
#2. Den anandra funktionen transponerar data till mander. kanske kan köra ihop dessa alltså 2 och tre
#3. den tredje köre en logg diff på skiten
# 4. juste måste accounta för att det finns vissa stocks som handlas olika dagar 

#Att göra: lägg till optimala vikter




#%%Input
stocks_list = ['WMT', 'JPM', 'CAT']
start_date = '2012-01-01'
end_date ='2014-12-31'
resolution_time = 4

#%% Run programme
df_stocks = read_data_stocks(start_date, end_date, stocks_list)
df_stocks_mod = resolution(df_stocks, resolution_time)
df_with_log_returns = log_returns(df_stocks_mod)
#df_nan_filled1 = fillna_with_latest_val(df1)
plot_returns(df_with_log_returns)
#%%
def plot_returns(df):
    plt.plot(df.iloc[:,1])






#%% making all log returns calculations

def log_returns(df):
    df_reversed = df.iloc[::-1]
    for col in range(len(df.T)-1):
        
        df_reversed[df_reversed.columns[col+1] + '_log_return' ] = (
            np.log(df_reversed[df_reversed.columns[col+1]]) - np.log(df_reversed[df_reversed.columns[col+1]].shift(1))
            )
    df_reversed = df_reversed.iloc[::-1]
    return df_reversed



#%%Fixing resolution
def resolution(df, resolution_time):
    
    if resolution_time == 30:
        df_resolution = df.iloc[::30, :]
    elif resolution_time == 7:
        df_resolution = df.iloc[::7, :]
    else:
        df_resolution = df
    
    
    return df_resolution
 

#%%Automatic reading all stocks




def read_data_stocks(start_date, end_date, stocks_list):

    init_data = date_df_initial(start_date=start_date, end_date=end_date )
    
    list_of_stocks = stocks_list
    
    for stocks in range(len(list_of_stocks)):
        init = yf.Ticker(list_of_stocks[stocks])
        history_data_stock =pd.DataFrame(init.history(start=start_date, end=end_date)['Close'])
        history_data_stock.columns = [list_of_stocks[stocks]]
        history_data_stock['date'] = history_data_stock.index
    
        
        init_data = pd.merge(init_data,
                             history_data_stock,
                             how= 'left',
                             on='date')
        fill_na_df = init_data.fillna(method='ffill')#, inplace=True)
        
    for col in range(len(list_of_stocks)):
        
        if np.isnan(fill_na_df.iloc[0,col+1]):
            fill_na_df.iloc[0,col+1] = fill_na_df.iloc[1,col+1]
        else:
            fill_na_df.iloc[0,col+1] = fill_na_df.iloc[0,col+1]
                           
        
        
    return fill_na_df
    
    
    
#%%
#Ready for being functionalized :)

def date_df_initial(start_date, end_date):
    
    """ Returns a dataframe with dates between start_date and end_date """
    
    num_days_interval = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days

    date_list = [pd.to_datetime(end_date) - datetime.timedelta(days=x) for x in range(num_days_interval)] 
    
    date_list_df = pd.DataFrame(date_list) 
    date_list_df.columns = ['date']
    
    return date_list_df

#%%










   