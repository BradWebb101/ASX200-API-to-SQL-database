# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 12:45:52 2019

@author: Brad
"""

#Importing libraries
import sqlalchemy
import pandas as pd
import time
import datetime

#Loading login credentials into Python
credentials = pd.read_csv('credentials.csv')
SQL_user = credentials.loc[0,'SQL_user']
SQL_pass = credentials.loc[0,'SQL_pass']
API_key = credentials.loc[0,'API_key']

#Creating list of stocks in update index
stocks = pd.read_csv('ASX_API_stocks.csv',index_col=False)

#Creating engine and connecting to database
engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + str(SQL_user) + ':' + str(SQL_pass) + '@localhost:3306/ASX_API')
con = engine.connect()

#Setup basic variables
asx_200 = pd.read_csv('ASX_API_stocks.csv')
stock_updated = []
stock_fail = []
entries_updated = 0
stocks_failed = 0
date = datetime.date.today()

for i in range(len(stocks)):
    try:
        print('Requesting data for ' +str(stocks.loc[i,'0']))
        data = pd.read_json('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' +str(stocks.loc[i,'0']) + '.AX&outputsize=compact&apikey=' + str(API_key))
        print('Data pull sucessful')
        print('Parsing data')
        data = data[2:-3]
        data = data['Time Series (Daily)'].apply(pd.Series)
        data.index.names = ['Date']
        data.columns = ['Open','High','Low','Close','Volume']
        data[['Open','High','Low','Close']] = data[['Open','High','Low','Close']].astype(float)
        data['Volume'] = data['Volume'].astype(int)
        data = data[(data['Open'] != 0) & (data['High'] != 0) & (data['Low'] != 0) & (data['Close'] != 0) & (data['Volume'] != 0)]
        print('Data parse sucessful')
        print('Finding last entry in Database')
        limit = con.execute(('SELECT * FROM `{}` ORDER BY date DESC LIMIT 1').format(stocks.loc[i,'0']))
        limit = pd.DataFrame(list(limit))
        limit = limit.loc[0,0]
        data = data.loc[str(limit):,:]
        data = data.iloc[1:,:]
        print('Updating table data for ' + str(stocks.loc[i,'0']))
        data.to_sql(stocks.loc[i,'0'], con=engine, if_exists='append')
        stock_updated.append(stocks.loc[i,'0'])
        entries_updated += len(data)
        print('Table updated sucessfully')
        print('                         ')
        print('-------------------------')
        time.sleep(15)
        
    except:
        print('Error updating ' + str(stocks.loc[i,'0']))
        stock_fail.append(stocks.loc[i,'0'])
        stocks_failed += 1
        print('-------------------------')
        print('                         ')
        time.sleep(15)

#Updating stats on update    
con.execute(('INSERT INTO update_stats (Date, Stocks_Updated, Entries_Updated, Stocks_Failed) VALUES("{}","{}","{}","{}")').format(date, len(stock_updated), entries_updated, stocks_failed))
print(('On {} this code updated {} stocks with {} entries total with {} stock requests failed').format(date, len(stock_updated), entries_updated, stocks_failed))


