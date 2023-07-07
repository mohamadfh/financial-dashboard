
#%%
import time
import requests
import datetime
import pandas as pd

def Market_with_askbid():
    count = 0 
    while count<5:
        url = 'http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx?h=0&r=0'
        data = requests.get(url, timeout=12)
        content = data.content.decode('utf-8')
        parts = content.split('@')
        if data.status_code != 200 or len(content.split('@')[2])<400:
            count+=1
            time.sleep(1)
        if count ==5:
            raise Exception('ohoh')
        if data.status_code == 200 and len(content.split('@')[2]) > 400:
            break

    parts = content.split('@')
    inst_price = parts[2].split(';')
    market_me = {}

    for item in inst_price:
        item=item.split(',')
        market_me[item[0]]= dict(id=item[0],isin=item[1],symbol=item[2],
                              name=item[3],open_price=float(item[5]),close_price=float(item[6]),
                              last_trade=float(item[7]),count=item[8],volume=float(item[9]),
                              value=float(item[10]),low_price=float(item[11]),
                              high_price=float(item[12]),yesterday_price=int(item[13]),
                              table_id=item[17],group_id=item[18],max_allowed_price=float(item[19]),
                              min_allowed_price=float(item[20]),last_return=(float(item[7])-float(item[13]))/float(item[13]),
                              close_ret=(float(item[6])-float(item[13]))/float(item[13]),
                              number_of_shares=float(item[21]), market_cap=int(item[21])*int(item[6]))
    
    for item in parts[3].split(';'):
        try:
            item=item.split(',')
            if item[1] == '1':
                market_me[item[0]]['bid_price_1']=  float(item[4])
                market_me[item[0]]['bid_vol_1']=  float(item[6])
                
                market_me[item[0]]['ask_price_1']=  float(item[5])
                market_me[item[0]]['ask_vol_1']=  float(item[7])

            if item[1] == '2':
                market_me[item[0]]['bid_price_2']=  float(item[4])
                market_me[item[0]]['bid_vol_2']=  float(item[6])
                
                market_me[item[0]]['ask_price_2']=  float(item[5])
                market_me[item[0]]['ask_vol_2']=  float(item[7])

            if item[1] == '3':
                market_me[item[0]]['bid_price_3']=  float(item[4])
                market_me[item[0]]['bid_vol_3']=  float(item[6])
                
                market_me[item[0]]['ask_price_3']=  float(item[5])
                market_me[item[0]]['ask_vol_3']=  float(item[7])

            if item[1] == '4':
                market_me[item[0]]['bid_price_4']=  float(item[4])
                market_me[item[0]]['bid_vol_4']=  float(item[6])
                
                market_me[item[0]]['ask_price_4']=  float(item[5])
                market_me[item[0]]['ask_vol_4']=  float(item[7])

            if item[1] == '5':
                market_me[item[0]]['bid_price_5']=  float(item[4])
                market_me[item[0]]['bid_vol_5']=  float(item[6])
                
                market_me[item[0]]['ask_price_5']=  float(item[5])
                market_me[item[0]]['ask_vol_5']=  float(item[7])
        except:
            pass
    df = pd.DataFrame(market_me).T

    
    df['ask_price_1'] = df['ask_price_1'].fillna(0)
    df['ask_vol_1'] = df['ask_vol_1'].fillna(0)
    df['bid_price_1'] = df['bid_price_1'].fillna(0)
    df['bid_vol_1'] = df['bid_vol_1'].fillna(0)
    for i in range(1,6):
        df[f'ask_value_{i}'] = df[f'ask_vol_{i}'] * df[f'ask_price_{i}']
        df[f'bid_value_{i}'] = df[f'bid_vol_{i}'] * df[f'bid_price_{i}']
    
    df['timestamp'] = time.time()
    df['time'] = str(datetime.datetime.now())
    df['date'] = str(datetime.date.today())
    return df
# %%
