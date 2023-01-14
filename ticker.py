from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
from datetime import datetime,timedelta

def get_soup(link):
    webpage_response = requests.get(link)
    html = webpage_response.content
    return BeautifulSoup(html, "html.parser")

def clean_number(value):
    value = value.replace(",","")
    value = value.replace("$","")
    value = value.replace('€',"")
    if "-" in value[1:]:
        value = value.replace("-","_") 
    if value[0] == "(" and value[-1] == ")":
        value = "-"+value[1:-1]
    if value[-1] == "K":
        value = float(value[:-1])*1000
    elif value[-1] == "M":
        value = float(value[:-1])*1000000
    elif value[-1] == "B":
        value = float(value[:-1])*1000000000
    elif value[-1] == "T":
        value = float(value[:-1])*1000000000000
    elif value[-1] == "%":
        value = float(value[:-1])/100
    if value == "-":
        value = np.nan
    if value == "N/A":
        value = np.nan
    return value

class Ticker:
    def __init__(self,ticker):
        self.ticker = ticker.upper()

    def financial(self,reports=['income_statement','balance_statement','cash_flow'],ascending=False,format="float",quarterly=False):
        link_is = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/financials/income/"
        link_bs = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/financials/balance-sheet/"
        link_cf = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/financials/cash-flow/"
        link_dict = {"income_statement":link_is,"balance_statement":link_bs,"cash_flow":link_cf}

        df_dict = {}
        label_lst = []
        for link in link_dict:
            if link in reports:
                if quarterly == True:
                    link_dict[link] += "quarter"
                webpage_response = requests.get(link_dict[link])
                html = webpage_response.content
                soup = BeautifulSoup(html, "html.parser")
                ticker_check = soup.find(class_="element element--message")

                if type(ticker_check) != type(None):
                    print("Ticker is not vaild")
                    return
                elements = soup(class_="cell__content")

                full_dict = {}

                for i,element in enumerate(elements):
                    value = element.get_text()
                    if format == 'float':
                        value = clean_number(value)

                    if i%8 == 0 or i%8 == 7:
                        pass
                    elif i<8:
                        if value == "Item":
                            value = "year"
                            label_lst.append(value)
                        else:
                            if quarterly == True:
                                value = datetime.strptime(value,"%d-%b-%Y").strftime("%Y-%m-%d")
                            label_lst.append(value)
                    elif i<16: 
                        full_dict[label_lst[(i-1)%8]]=[value]
                    else:
                        full_dict[label_lst[(i-1)%8]].append(value)

                df_dict[link] = pd.DataFrame(data=full_dict).T.sort_index(ascending=ascending)
                df_dict[link] = df_dict[link].rename(columns=df_dict[link].iloc[0]).reset_index()
                df_dict[link] = df_dict[link].drop(df_dict[link].index[0]).reset_index()
                df_dict[link] = df_dict[link].drop('level_0',axis=1).rename(columns={'index':"year"})
        
        if len(df_dict) <= 1:
            return list(df_dict.values())[0]
        full_df = pd.concat(df_dict.values(),axis=1)
        return full_df

    def profile(self,format="float"):
        link = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/company-profile"
        soup = get_soup(link)       
        profile_dict = {}
        profile_dict['name'] = soup(class_="heading")[0].get_text()
        profile_dict['description'] = soup(class_="description__text")[0].get_text()
        if format != 'float':
            profile_dict['phone_number'] = soup(class_="phone")[0].get_text().split("\n")[2]
        else:
            profile_dict['phone_number'] = soup(class_="phone")[0].get_text().split("\n")[2].replace(' ','').replace("-",'')
        profile_dict['address'] = soup(class_="address")[0].get_text().split("\n")[1]+" "+soup(class_="address")[0].get_text().split("\n")[2]
        elements = soup(class_="list list--kv list--col50")[0].get_text().split("\n")
        for i,value in enumerate(elements):
            if i%4 == 3:
                if format == 'float':
                    value = clean_number(value)
                profile_dict[elements[i-1].lower().replace(" ","_").replace("-","_")] = value
        directors_dict = {}
        elements = soup(class_="list list--kv")[0].get_text().split("\n")
        for i,value in enumerate(elements):
            if i%4 == 3:
                directors_dict[elements[i-1]] = value
        profile_dict['board_of_directors'] = directors_dict

        elements = soup(class_="table value-pairs no-heading")
        for value in elements:
            table_lst = value.get_text().split('\n')
            for i in range(len(table_lst)):
                if i%4 == 0 and i != 0:
                    if format == 'float':
                        profile_dict[table_lst[i-1].lower().replace(" ","_").replace("-","_")] = clean_number(table_lst[i])
                    else:
                        profile_dict[table_lst[i-1].lower().replace(" ","_").replace("-","_")] = table_lst[i]
        return profile_dict

    def historical_price(self,start_date=datetime.now()-timedelta(days=31),end_date=datetime.now(),ascending=False):
        if type(start_date) == type("s"):
            start_date = datetime.strptime(start_date,"%m/%d/%Y")
        if type(end_date) == type("s"):
            end_date = datetime.strptime(end_date,"%m/%d/%Y")
        df_dict = {}
        if end_date.year-start_date.year == 0:
            link = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/downloaddatapartial?startdate="+start_date.strftime("%#m/%#d/%Y")+"%2000:00:00&enddate="+end_date.strftime("%#m/%#d/%Y")+"%2023:59:59&daterange=d30&frequency=p1d&csvdownload=true&downloadpartial=false&newdates=false"
            soup = get_soup(link).get_text()[:-1].split("\n")[1:]
            date_lst = []
            open_lst = []
            high_lst = []
            low_lst = []
            close_lst = []
            volume_lst = []
            for values in soup:
                date_lst.append(datetime.strptime(values.replace("\"","").split(",")[0], "%m/%d/%Y"))
                open_lst.append(float(values.replace("\"","").split(",")[1]))
                high_lst.append(float(values.replace("\"","").split(",")[2]))
                low_lst.append(float(values.replace("\"","").split(",")[3]))
                close_lst.append(float(values.replace("\"","").split(",")[4]))
                volume_lst.append(float("".join(values.replace("\"","").split(",")[5:])))
            return pd.DataFrame(data={'date':date_lst,'open':open_lst,'high':high_lst,'low':low_lst,'close':close_lst,'volume':volume_lst}).set_index('date').reset_index()
        else:    
            for i in range(end_date.year-start_date.year):
                if i != end_date.year-start_date.year-1:
                    end_date =start_date+timedelta(days=365*(i+1))
                link = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/downloaddatapartial?startdate="+start_date.strftime("%#m/%#d/%Y")+"%2000:00:00&enddate="+end_date.strftime("%#m/%#d/%Y")+"%2023:59:59&daterange=d30&frequency=p1d&csvdownload=true&downloadpartial=false&newdates=false"
                soup = get_soup(link).get_text()[:-1].split("\n")[1:]
                date_lst = []
                open_lst = []
                high_lst = []
                low_lst = []
                close_lst = []
                volume_lst = []
                for values in soup:
                    date_lst.append(datetime.strptime(values.replace("\"","").split(",")[0], "%m/%d/%Y").strftime("%Y-%#m-%#d"))
                    open_lst.append(float(values.replace("\"","").split(",")[1]))
                    high_lst.append(float(values.replace("\"","").split(",")[2]))
                    low_lst.append(float(values.replace("\"","").split(",")[3]))
                    close_lst.append(float(values.replace("\"","").split(",")[4]))
                    volume_lst.append(float("".join(values.replace("\"","").split(",")[5:])))
                df_dict[i] = pd.DataFrame(data={'date':date_lst,'open':open_lst,'high':high_lst,'low':low_lst,'close':close_lst,'volume':volume_lst}).set_index('date')
            if len(df_dict) == 1:
                return list(df_dict.values())[0].reset_index()
            if len(df_dict) == 0 :
                return None
            full_df = pd.concat(df_dict.values(),join='inner').sort_values('date',ascending=ascending).reset_index()
            return full_df