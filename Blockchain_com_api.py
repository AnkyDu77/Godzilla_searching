import requests
import json
# Makeing timeline in unix time
limit_day = pd.to_datetime('2018-02-09')
datelist = pd.date_range(limit_day, periods=733).to_list()
date_series = pd.DataFrame(data=(datelist), columns=['Date'])
dt = pd.DatetimeIndex(date_series['Date']).astype(np.int64)//1000000
unix_mlseconds_lst = dt.to_list()

#Getting blocks hash list with timestamps
blocks_lst = []
for j in unix_mlseconds_lst:
    request = requests.get('https://blockchain.info/blocks/'+str(j)+'?format=json')
    parse_result = json.loads(request.content)
    blocks_lst.append(parse_result['blocks'])

#Parsing json content for the final dataset
blockID = []
hashID = []
timestamp = []
for d_list in blocks_lst:
    for dictionary in d_list:
        blockID.append(dictionary['height'])
        hashID.append(dictionary['hash'])
        timestamp.append(dictionary['time'])

#Makeing additional bh-dataset
additional_bh = pd.DataFrame(data=(blockID,hashID,timestamp)).T
additional_bh.columns=['blockID','hash','timestamp']
additional_bh['timestamp']=pd.to_datetime(additional_bh['timestamp'], unit='s')

#Getting info about additional outputs
dates_out_sums = {}
for indx in range(len(additional_bh)):
    request = requests.get('https://blockchain.info/rawblock/'+str(additional_bh['hash'][indx])) #Getting all info about block by it's hash
    parse_result = json.loads(request.content)
    block_outs_sum=[]
    for i in parse_result['tx']: #Running through all txs to sum up all outputs
        intermid_out_sum_values = []
        for j in i['out']:
            intermid_out_sum_values.append(j['value'])
        block_outs_sum.append(sum(intermid_out_sum_values))
    dates_out_sums[bh['timestamp'][indx]] = sum(block_outs_sum)

#Making dataframe of additional outputs
dates_out_sums_lst = dates_out_sums.items()
out_txs = pd.DataFrame(dates_out_sums_lst, columns=['Date', 'out_sums'])
out_txs['out_sums']=out_txs['out_sums'].apply(lambda x: x/100000000) #Making a series of bitcoins instead of satoshies
out_txs.to_csv('.../Data/additional_outs_dated(2018-02-09_2018-04-28).csv', index=False)
