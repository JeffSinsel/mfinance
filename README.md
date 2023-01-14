# mfinance
 
work in progress web scraper of marketwatch
basics:
Ticker(ticker) creates an object based on the ticker parameter with 3 different consturctors: 

Ticker(ticker).financial(self,reports=list('income_statement','balance_statement','cash_flow'),ascending=False,format="float",quarterly=False)

reports=list('income_statement','balance_statement','cash_flow')
this parameter by default has all 3 different financial statments, to only get one statement or any combination, simply pass a list that contains the reports that you would like
ascending=False
this parameter determines how the dataframe is sorted, by default the most recent is first, make this true to make the oldest year first
format='float'
this parameter determines how the numbers in the dataframe are formated, by default the numbers are cleaned into floats, make this = 'plain' to get the same data from the website
quarterly=False
this parameter determines if the data is given in yearly or quartely format, by default this is yearly, make it True for quarterly

Ticker(ticker).profile(self,format="float")

format='float'
this parameter determines how the numbers in the dataframe are formated, by default the numbers are cleaned into floats, make this = 'plain' to get the same data from the website

Ticker(ticker).historical_price(self,start_date=datetime.now()-timedelta(days=31),end_date=datetime.now(),ascending=False):

start_date=datetime.now()-timedelta(days=31)
determines the start date of data pulled, input this in mm/dd/yyyy format, by default this is 31 days ago
end_date=datetime.now()
determines the end date of data pulled, input this in mm/dd/yyyy format, by default this is today
ascending=False
determines how the dataframe is sorted, by default the most recent is first, make this true to make the oldest year first
