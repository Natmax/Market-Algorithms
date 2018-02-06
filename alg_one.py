from alpha_vantage.timeseries import TimeSeries
import json
import pandas
import sys
import datetime

now = datetime.datetime.now()
date_string = str(now)[:4] + "-" + str(now)[5:7] + "-" + str(now)[8:10]
stock_list = ["GOOG","AMZN","NVR","PCLN","MKL","WTM","ISRG","AZO","CABO","GHC"]
if len(sys.argv) > 2:
	stock_list = sys.argv[2:]
Share_num = 50
share_list = [Share_num]*len(stock_list)
# Get json object with the intraday data and another with  the call's metadata
ts = TimeSeries(key='GYFRTBOLKR3X178N',output_format='pandas')

# Basic algorithm rules: Sell at the end of every day. Buy or Hold if stock goes up. Sell if stock goes down.
# Input 1 for last 2 weeks, anything else for 1 hour of data.
earnings = 0
total_price = 0
profit = 0
sales = 0
trade_cost = 0.005
fees = 0
for i in range(len(stock_list)):
	stock = 0
	if sys.argv[1] == "today":
		print("Data for today")
		data, meta_data = ts.get_intraday(stock_list[i],interval='1min',outputsize='full')
	elif sys.argv[1] == "1":
		print("Data for last two weeks")
		data, meta_data = ts.get_intraday(stock_list[i],interval='1min',outputsize='full')
	else:
		print("Data for last hour")
		data, meta_data = ts.get_intraday(stock_list[i],interval='1min')
	n_shares = share_list[i]
	share_price = data.iloc[1,2]
	total_price += n_shares*share_price
	for index, row in data.iterrows():
		if date_string not in index:
			continue
		if stock:
			earnings += n_shares*(close_cost - row["1. open"])
		if "16:00:00" in index:
			if stock:
				stock = 0
				sales += 1
				earnings += n_shares*(close_cost - open_cost)
				earnings -= max(n_shares*(trade_cost),1)
				fees += max(n_shares*(trade_cost),1)
		else:
			open_cost = row["1. open"]
			close_cost = row["4. close"]
			if open_cost > close_cost:
				if stock:
					stock = 0
					sales += 1
					earnings -= n_shares*(open_cost - close_cost)
					earnings -= max(n_shares*(trade_cost),1)
					fees += max(n_shares*(trade_cost),1)
			if close_cost > open_cost:
				if stock == 0:
					stock = 1
					sales += 1
					earnings -= max(n_shares*(trade_cost),1)
					fees += max(n_shares*(trade_cost),1)
				else:
					earnings += n_shares*(close_cost - open_cost)
print("Earnings without fee:", earnings + fees)
print("Profit without fee:", (earnings + fees)/total_price)
print("Profit with fee:", earnings/total_price)
print("Transactions:", Share_num*sales)