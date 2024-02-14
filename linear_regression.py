import random
import numpy as np
# import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
# from sklearn import datasets, linear_model
# from sklearn.linear_model import LinearRegression
from datetime import datetime
from nixtlats import TimeGPT
import pandas as pd

def random_plus_minus():
    return random.choice([1, -1])

# def get_signal(x,y):
#     return linear_regression_gradient(x,y)
#     return random_plus_minus()

def inplay(x, now_price):
    sum=0
    i=0
    for trade_index, trade_row in x.iterrows():
        if trade_row['open'] == 1:
            i=i+1
            sum=sum+trade_row['size']/trade_row['price']*now_price
            # print('trades open, ',i,'account ',account_balance)
    return sum

# def linear_regression_gradient(x,y):
#     timestamps = pd.to_datetime(x)
#     df = pd.DataFrame({'timestamp': timestamps, 'value': y})
#     timegpt_fcst_df = timegpt.forecast(df=df, h=7, freq='15T', time_col='timestamp', target_col='value')

#     # plt.plot(df['timestamp'], df['value'], marker='o', linestyle='-')
#     # plt.title('Price vs Timestamp')
#     # plt.xlabel('Timestamp')
#     # plt.ylabel('Price')
#     # plt.grid(True)
#     # plt.show()
    
#     # plt.plot(timegpt_fcst_df['timestamp'], timegpt_fcst_df['TimeGPT'], marker='o', linestyle='-')
#     # plt.title('Price vs TimeGPT')
#     # plt.xlabel('Timestamp')
#     # plt.ylabel('Price')
#     # plt.grid(True)
#     # plt.show()
    

#     print (timegpt_fcst_df)
    
#     timegpt_fcst_df['timestamp'] = pd.to_datetime(timegpt_fcst_df['timestamp'])
#     x = (timegpt_fcst_df['timestamp'].astype(np.int64) // 10**9).to_numpy()
#     y = timegpt_fcst_df['TimeGPT'].to_numpy()
    
#     print (timegpt_fcst_df)
#     print(x)
#     print(y)
#     x = x.reshape((-1, 1))
#     model = LinearRegression()
#     model.fit(x, y)
#     print(f"slope: {model.coef_}")
#     return model.coef_

file_path = 'prices.csv'
df_prices = pd.read_csv(file_path)
out_file='output.csv'


timegpt = TimeGPT(
    # defaults to os.environ.get("TIMEGPT_TOKEN")
    token = 'FGhvofD8JCo3kvfrY6XdCutbRnla7ZKiusXOu8mZBA6ZyPP9XvtxBb7ISNBrw3gJneb0scTwVBoCx0al0zdGucBWPOEmB0p3vObfH9iLieiGU5OmyTIpcs1ommKHxfWfdstmvf9rEI8ZfxI38DI96TK5z3ncflx9DfQydJTDzJ15xpkgOe1ET1pM5SocRvXeztO1VAl9WoKiTM00DTbmSJSnVVe5CSe4SuUt3wNXav27c6xAd82Akuhh52te7SNU'
)



account_balance=10000
percent_of_account_to_risk=0.01
commission=0.00
risk_reward=0.002

columns = [
    'longOrShort',
    'size',
    'price',
    'open',
    'signal',
    'multiplier',
    'balBeforeOpen',
    'balAfterOpen',
    'balBeforeClose',
    'balAfterClose',
    'sellPrice'
]
df_trades = pd.DataFrame(columns=columns)

for candle_index, candle in df_prices.iterrows():
    # print(f"day {candle_index}\tdate: {candle['date']}, price: {'{:.2f}'.format(candle['price'])}  \t Account Balance: {account_balance} \t in play: {inplay(df_trades, candle['price'])}")
    with open(out_file, "a") as file:
        file.write(f"day: {candle_index}, date: {candle['date']}, price: {candle['price']}, Account Balance: {account_balance}, in play: {inplay(df_trades, candle['price'])}, total: {inplay(df_trades, candle['price'])+account_balance}\n")
    
    # Close all the trades that need closing
    for trade_index, trade_row in df_trades.iterrows():
        # print(f"Index: {trade_index}, L/S: {trade_row['longOrShort']}, size: {trade_row['size']}, price: {trade_row['price']}, open: {trade_row['open']}")
        # print('trade_index',trade_index)
        if trade_row['open'] == 1:
            current_value = trade_row['size'] / trade_row['price'] * candle['price']
            profit_loss = (current_value - trade_row['size']) * trade_row['longOrShort']
            # print('should I close? ', trade_index, profit_loss, current_value, trade_row['size'])
#             print('trade_row[longorshort]', trade_row['longOrShort'])

            if abs(profit_loss) > risk_reward * trade_row['size']:
#             if ((profit_loss > 0 and profit_loss > risk_reward*trade_row['size']*2) or (profit_loss <0 and profit_loss < risk_reward*trade_row['size'])):
                df_trades.iloc[trade_index, 3] = 0 # open
                
                # TODO: DONT FORGET TO TAKE OFF COMMISSION THIS SIDE TOO!
                df_trades.iloc[trade_index, 8] = account_balance # balBeforeClose
                account_balance = account_balance + trade_row['size']
                account_balance = account_balance + profit_loss
                df_trades.iloc[trade_index, 9] = account_balance # balAfterClose
                df_trades.iloc[trade_index, 10] = candle['price'] # sellPrice
                
                print(
                    f"Closed: {trade_index}, "
                    f"balBeforeOpen: {trade_row['balBeforeOpen']}, "
                    f"bought: {trade_row['size']}, "
                    f"balAfterOpen: {trade_row['balAfterOpen']}, "
                    
                    f"sellingPrice: {current_value}, "
                    f"L/S: {trade_row['longOrShort']}, "
                    f"P/L: {profit_loss}, "
                    f"balBeforeClose: {trade_row['balBeforeClose']}, "
                    f"balAfterClose: {trade_row['balAfterClose']}, "
                    f"total: {inplay(df_trades, candle['price'])+account_balance}"
                )
                
    # Open a position randomly buy or sell for 1% of account_balance
    
    # Get Signal
    signal = random_plus_minus()
    # if candle_index > 9:

    #     date_format = "%Y-%m-%d %H:%M:%S"
     
    #     now_x = np.array([
    #         datetime.strptime(df_prices.iloc[candle_index-9,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-8,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-7,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-6,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-5,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-4,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-3,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-2,0], date_format).timestamp(),
    #         datetime.strptime(df_prices.iloc[candle_index-1,0], date_format).timestamp()
    #     ])
    #     now_y = np.array([
    #         df_prices.iloc[candle_index-9,1],
    #         df_prices.iloc[candle_index-8,1],
    #         df_prices.iloc[candle_index-7,1],
    #         df_prices.iloc[candle_index-6,1],
    #         df_prices.iloc[candle_index-5,1],
    #         df_prices.iloc[candle_index-4,1],
    #         df_prices.iloc[candle_index-3,1],
    #         df_prices.iloc[candle_index-2,1],
    #         df_prices.iloc[candle_index-1,1]
    #     ])

    signal = df_prices.iloc[candle_index]['slope']

    
    if (account_balance > 0 and candle_index > 9):
        
        multiplier = 0
        multiplier = signal/0.00001*0.2
        if multiplier < -0.005: multiplier = -0.005
        if multiplier > 0.005: multiplier = 0.005
        
        position_size = account_balance * (percent_of_account_to_risk + abs(multiplier))
        position_after_commission = position_size - (position_size * commission)
        position = {'balBeforeOpen': account_balance}
        account_balance = account_balance - position_size
        position['balAfterOpen'] = account_balance
        long_or_short = np.sign(signal)
        price = candle['price']

        position['longOrShort'] = long_or_short
        position['size'] = position_after_commission
        position['price'] = price
        position['open'] = 1
        position['signal'] = signal
        position['multiplier'] = multiplier
        
        position['balBeforeClose'] = 0
        position['balAfterClose'] = 0
        
        df_trades.loc[len(df_trades)] = position
        print(position)

df_trades.to_csv('trades.csv', index=False)





