from alpha_vantage.timeseries import TimeSeries
import json
import pandas
import sys
stock_list = ["GOOGL","AMZN","NVR","PCLN","MKL","WTM","ISRG","AZO","CABO","GHC"]
if len(sys.argv) > 1:
	stock_list = sys.argv[1:]
share_list = [1]*len(stock_list)
ts = TimeSeries(key='GYFRTBOLKR3X178N',output_format='pandas')
# Get json object with the intraday data and another with  the call's metadata

earnings = 0
total_price = 0
profit = 0
sales = 0
for i in range(len(stock_list)):
	stock = 0
	data, meta_data = ts.get_intraday(stock_list[i],interval='1min',outputsize='full')

	n_shares = share_list[i]
	trade_cost = 0.005
	share_price = data.iloc[1,2]
	total_price += n_shares*share_price
	for index, row in data.iterrows():
		if stock:
			earnings += n_shares*(close_cost - row["1. open"])
		if "16:00:00" in index:
			if stock:
				stock = 0
				sales += 1
				earnings += n_shares*(close_cost - open_cost)
		else:
			open_cost = row["1. open"]
			close_cost = row["4. close"]
			if open_cost > close_cost:
				if stock:
					stock = 0
					sales += 1
					earnings -= n_shares*(open_cost - close_cost)
					earnings -= n_shares*(trade_cost)
			if close_cost > open_cost:
				if stock == 0:
					stock = 1
					sales += 1
				else:
					earnings += n_shares*(close_cost - open_cost)
					earnings -= n_shares*(trade_cost)
print("Profit:", earnings/total_price)
print("Transactions:", sales)