import pandas as pd

#Loading bh.dat
mit_data = pd.read_table('.../bh.dat', #Hear is the path to bh.dat file
                         header=None, names=['blockID', 'hash','block_timestamp', 'n_txs'])
mit_data['block_timestamp'] = pd.to_datetime(mit_data['block_timestamp'], unit='s')
#Loading info about output of transactions
out_txs_all = pd.read_table('.../txout.dat',header=None, #The path to txout.dat file
                           names=['txID', 'output_seq','addrID', 'sum'])
#Loading info transaction overview dataset
mapping_dataset = pd.read_table('.../tx.dat', #The path to the tx.dat file
                                header=None, names=['txID', 'blockID','n_inputs', 'n_outputs'])
#Dropping needless columns in outputs dataset and summing up outputs values groupping them by 'txID'
out_txs_all.drop('output_seq',axis=1,inplace=True)
out_txs_all.drop('addrID',axis=1,inplace=True)
out_txs_all = out_txs_all.groupby('txID').sum().reset_index()

#Dropping needless columns in transactions dataset and adding outputs values
mapping_dataset.drop('n_inputs', axis=1,inplace=True)
mapping_dataset.drop('n_outputs', axis=1,inplace=True)
mapping_dataset['sum_outs'] = out_txs_all['sum']

#Now we can dropp 'txID' column since it's useless now.
#Then we group mapping_df by blockID and addup all sums to get btc_sum per particular block
mapping_dataset.drop('txID', axis=1, inplace=True)
mapping_dataset=mapping_dataset.groupby('blockID').sum().reset_index()

#Prepare mit_data to the next manipulations
mit_data.drop('hash', axis=1,inplace=True)
mit_data.drop('n_txs', axis=1,inplace=True)

#Now we just can get dates from sliced block_timestemp dataset and concatinate it with mapping_df since they have equals sizes
#and contains similar blocks.
mapping_dataset['Date'] = mit_data['block_timestamp']
mapping_dataset['sum_outs'] = mapping_dataset['sum_outs'].apply(lambda x: x/100000000) #Getting amount of bitcoins instead of satoshies

#Finally we are making a csv file
mapping_dataset.to_csv('../filename.csv', #File path
                    index=False)
