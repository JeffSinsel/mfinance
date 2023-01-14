# mfinance
work in progress web scraper of marketwatch
basics:

Ticker(ticker) creates an object based on the ticker parameter with 3 different consturctors: 

---
`Ticker(ticker).financial(self,reports=list('income_statement','balance_statement','cash_flow'),ascending=False,format="float",quarterly=False)`

reports=list('income_statement','balance_statement','cash_flow')
this parameter by default has all 3 different financial statments, to only get one statement or any combination, simply pass a list that contains the reports that you would like

ascending=False
this parameter determines how the dataframe is sorted, by default the most recent is first, make this true to make the oldest year first

format='float'
this parameter determines how the numbers in the dataframe are formated, by default the numbers are cleaned into floats, make this = 'plain' to get the same data from the website

quarterly=False
this parameter determines if the data is given in yearly or quartely format, by default this is yearly, make it True for quarterly

Example:
```
>>> aapl = Ticker('AAPL')
>>> aapl_financial_df = aapl.financial()
>>> print(aapl_financial_df.head())
   year        Sales/Revenue Sales Growth Cost of Goods Sold (COGS) incl. D&A  ... Net Change in Cash      Free Cash Flow Free Cash Flow Growth Free Cash Flow Yield
0  2022       394330000000.0          NaN                      223550000000.0  ...     -10950000000.0      111440000000.0                   NaN                  NaN
1  2021       365820000000.0       0.3344                      212980000000.0  ...      -3860000000.0       92950000000.0                 0.267                 3.93
2  2020  274149999999.999969       0.0546                      170140000000.0  ...     -10440000000.0       73370000000.0                0.2457                  NaN
3  2019  259970000000.000031       -0.022                      162260000000.0  ...      24310000000.0       58900000000.0               -0.0815                  NaN
4  2018       265810000000.0      -0.3259                      163830000000.0  ...       5620000000.0  64120000000.000008               -0.4246                  NaN

[5 rows x 200 columns] 
```

---
`Ticker(ticker).profile(self,format="float")`

format='float'
this parameter determines how the numbers in the dataframe are formated, by default the numbers are cleaned into floats, make this = 'plain' to get the same data from the website

Example:
```
>>> aapl = Ticker('AAPL')
>>> aapl_profile_dict = aapl.profile(format='plain')
>>> print(aapl_profile_dict)
{'name': 'Apple Inc.', 'description': 'Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of related services. It operates through the following geographical segments: Americas, Europe, Greater China, Japan, and Rest of Asia Pacific. The Americas segment includes North and South America. The Europe segment consists of European countries, as well as India, the Middle East, and Africa. The Greater China segment comprises China, Hong Kong, and Taiwan. The Rest of Asia Pacific segment includes Australia and Asian countries. Its products and services include iPhone, Mac, iPad, AirPods, Apple TV, 
Apple Watch, Beats products, AppleCare, iCloud, digital content stores, streaming, and licensing services. The company was founded by Steven Paul Jobs, Ronald Gerald Wayne, and Stephen G. Wozniak in April 1976 and is headquartered in Cupertino, CA.', 'phone_number': '1 408 996-1010', 'address': 'One Apple Park Way Cupertino, California 95014-2083 ', 'industry': 'Computers/Consumer Electronics', 'sector': 'Technology', 'fiscal_year_end': '01/0002', 'revenue': '$394.33B', 'net_income': '$99.8B', '2022_sales_growth': 'N/A', 'employees': 'N/A', 'board_of_directors': {'Timothy Donald Cook MBA': 'Chief Executive Officer & Director', 'Alex Gorsky MBA': 'Director', 'Arthur D Levinson PhD': 'Independent Chairman', 'Monica Cecilia Lozano': 'Independent Director', 'Andrea Jung': 'Independent Non-Executive Director', 'Albert Arnold Gore Jr.': 'Independent Director', 'Ronald D Sugar PhD': 'Independent Director', 'Susan Lynne Wagner MBA': 'Independent Director', 'James A Bell': 'Independent Director'}, 'p/e_current': '21.82', 'p/e_ratio_(w/_extraordinary_items)': '21.55', 'p/e_ratio_(w/o_extraordinary_items)': '24.61', 'price_to_sales_ratio': '6.23', 'price_to_book_ratio': '47.33', 'price_to_cash_flow_ratio': '20.11', 'enterprise_value_to_ebitda': '16.90', 'enterprise_value_to_sales': '5.60', 'total_debt_to_enterprise_value': 'N/A', 'revenue/employee': 'N/A', 'income_per_employeee': 
'N/A', 'receivables_turnover': 'N/A', 'total_asset_turnover': '1.12', 'current_ratio': '0.88', 'quick_ratio': '0.85', 'cash_ratio': '0.31', 'gross_margin': '43.31%', 'operating_margin': '30.29%', 'pretax_margin': '30.20%', 'net_margin': '25.31%', 'return_on_assets': '28.36%', 'return_on_equity': '175.46%', 'return_on_total_capital': '62.41%', 'return_on_invested_capital': 'N/A', 'total_debt_to_total_equity': 'N/A', 'total_debt_to_total_capital': 'N/A', 'total_debt_to_total_assets': '37.56', 'long_term_debt_to_equity': 'N/A', 'long_term_debt_to_total_capital': 'N/A'}
```

---
`Ticker(ticker).historical_price(self,start_date=datetime.now()-timedelta(days=31),end_date=datetime.now(),ascending=False)`

start_date=datetime.now()-timedelta(days=31)
determines the start date of data pulled, input this in mm/dd/yyyy format, by default this is 31 days ago

end_date=datetime.now()
determines the end date of data pulled, input this in mm/dd/yyyy format, by default this is today

ascending=False
determines how the dataframe is sorted, by default the most recent is first, make this true to make the oldest year first

Example:
```
>>> aapl = Ticker('AAPL')
>>> aapl_price_df = aapl.historical_price()
>>> print(aapl_price_df.head())
        date    open    high     low   close      volume
0  2023-1-13  132.03  134.92  131.66  134.76  57809719.0
1  2023-1-12  133.88  134.26  131.44  133.41  71379648.0
2  2023-1-11  131.25  133.51  130.46  133.49  69458953.0
3  2023-1-10  130.26  131.26  128.12  130.73  63896160.0
4   2023-1-9  130.47  133.41  129.89  130.15  70790805.0
```