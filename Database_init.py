# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:26:55 2019

@author: Brad
"""
#Importing libraries
import sqlalchemy
import pandas as pd
import time

#Loading login credentials into Python
credentials = pd.read_csv('credentials.csv')
SQL_user = credentials.loc[0,'SQL_user']
SQL_pass = credentials.loc[0,'SQL_pass']
API_key = credentials.loc[0,'API_key']

#Creating list of stocks for table
asx_200 = pd.read_html('https://en.wikipedia.org/wiki/S%26P/ASX_200')
asx_200 = asx_200[0][0]
asx_200 = asx_200[1:]
asx_200.columns = ['Symbol']
asx_200 = asx_200.str.lower()

#Setting up database
engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + str(SQL_user) + ':' + str(SQL_pass) + '@localhost:3306')
con = engine.connect()
con.execute('CREATE database ASX_API')
con.close()

#Creating connection with MySQL server for API upload
engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + str(SQL_user) + ':' + str(SQL_pass) + '@localhost:3306/ASX_API')

con = engine.connect()

#API pull data for stocks and creating tables for sucessful pulls
asx_stocks = []

for stock in asx_200:
    try:
        print('Requesting data for ' +str(stock))
        data = pd.read_json('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' +str(stock) + '.AX&outputsize=full&apikey=' + str(API_key))
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
        print('Creating table for ' + str(stock))
        con.execute(('CREATE TABLE `{}` (Date date NOT NULL PRIMARY KEY, Open float(50) NOT NULL, High float(50) NOT NULL, Low float(50) NOT NULL, Close float(50) NOT NULL, Volume INT (50) NOT NULL)').format(stock))
        data.to_sql(stock, con=engine, if_exists='append')
        asx_stocks.append(stock)
        print('Table created sucessfully')
        print('                         ')
        print('-------------------------')
        time.sleep(15)
        
    except:
        print('Request for ' + str(stock) + ' failed')
        print('-------------------------')
        print('                         ')
        time.sleep(15)

#Sending list of stocks sucessfully pulled to CSV for update script
stock_list = pd.DataFrame(asx_stocks)
stock_list.to_csv('ASX_API_stocks.csv',index=False)

con.execute('CREATE TABLE Update_stats (Id int NOT NULL AUTO_INCREMENT PRIMARY KEY, Date date NOT NULL , Stocks_Updated int(5), Entries_Updated int(5), Stocks_Failed int(5))')

con.close()   
