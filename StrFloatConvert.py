import re
import pandas as pd

def strtofloatconvert(data):

    #Converting series to list
    price_lst = data['Price'].to_list()
    open_lst = data['Open'].to_list()
    high_lst = data['High'].to_list()
    low_lst = data['Low'].to_list()
    vol_lst = data['Vol.'].to_list()
    change_lst = data['Change %'].to_list()

    #Separating str by ',' sign exept Volume strings. It's got anoter
    #format, like '294.8K' or '12.9M'. Volume we convert lower
    sprt_prices = []
    sprt_open = []
    sprt_high = []
    sprt_low = []
    sprt_p = []
    sprt_o = []
    sprt_h = []
    sprt_l = []

    for price in price_lst:
        sprt_p = re.split(r',',price)
        sprt_prices.append(sprt_p)
    for open_p in open_lst:
        sprt_o = re.split(r',',open_p)
        sprt_open.append(sprt_o)
    for high in high_lst:
        sprt_h = re.split(r',',high)
        sprt_high.append(sprt_h)
    for low in low_lst:
        sprt_l = re.split(r',',low)
        sprt_low.append(sprt_l)

    #Adding splitted values together and converting them to float
    add_p = []
    add_o = []
    add_h = []
    add_l = []
    add_v = []
    add_ch = []

    for p in sprt_prices:
        if len(p) == 2:
            a = p[0]+p[1]
            a = float(a)
            add_p.append(a)
        else:
            a = p[0]
            a = float(a)
            add_p.append(a)
    for o in sprt_open:
        if len(o) == 2:
            a = o[0]+o[1]
            a = float(a)
            add_o.append(a)
        else:
            a = o[0]
            a = float(a)
            add_o.append(a)
    for h in sprt_high:
        if len(h) == 2:
            a = h[0]+h[1]
            a = float(a)
            add_h.append(a)
        else:
            a = h[0]
            a = float(a)
            add_h.append(a)
    for l in sprt_low:
        if len(l) == 2:
            a = l[0]+l[1]
            a = float(a)
            add_l.append(a)
        else:
            a = l[0]
            a = float(a)
            add_l.append(a)
#====================================
        #Working with zeroes in 'Vol.' in str_flt because it does not matter whether we put None or zero in empty space.
        #Pandas will convert None into NaN wich is kind of float 'number'. It will not respond to pandas 'isnull()' function.
    for v in vol_lst:
        if v == '-':
            add_v.append(0)
        else:
            exam = re.findall(r'K',v)
            if len(exam)>0:
                add = re.sub(r'K', '',v)
                add = float(add)
                add *= 1000
                add_v.append(add)
            else:
                add = re.sub(r'M', '',v)
                add = float(add)
                add *= 1000000
                add_v.append(add)
    for i in change_lst:
        add = re.sub(r'%', '',i)
        add = float(add)
        add_ch.append(add)

    #Putting all lists above to the DataFrame
    test_df = pd.DataFrame(data=(add_p, add_o, add_h, add_l,
                                        add_v,add_ch)).T
    test_df.columns = ['Price', 'Open', 'High', 'Low', 'Vol.', 'Change%']
    return test_df
