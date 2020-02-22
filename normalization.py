# Data Normalizing Function
#Be carefull! Normilization should goes only on train data!

import pandas as pd

def norm(train_data, data):
    #Getting overall statistics
    train_stats = train_data.describe()
    train_stats = train_stats.transpose()

    #Normalizing data
    normalized_data = (data - train_stats['mean']) / train_stats['std']

    return normalized_data
