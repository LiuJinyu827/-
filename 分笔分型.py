# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:25:03 2019

@author: 15308
"""


import pandas as pd



def FenXing(k_data):
    after_fenxing = pd.DataFrame()
    temp_data = k_data[:1]
    zoushi = [3]
    for i in range(len(k_data)):
        case1_1 = (temp_data.high.iloc[-1] > k_data.high[i] and temp_data.low.iloc[-1] < k_data.low[i])# 第1根包含第2根
        case1_2 = temp_data.high.iloc[-1] > k_data.high[i] and temp_data.low.iloc[-1] == k_data.low[i]# 第1根包含第2根
        case1_3 = temp_data.high.iloc[-1] == k_data.high[i] and temp_data.low.iloc[-1] < k_data.low[i]# 第1根包含第2根
        case2_1 = temp_data.high.iloc[-1] < k_data.high[i] and temp_data.low.iloc[-1] > k_data.low[i] # 第2根包含第1根
        case2_2 = temp_data.high.iloc[-1] < k_data.high[i] and temp_data.low.iloc[-1] == k_data.low[i] # 第2根包含第1根
        case2_3 = temp_data.high.iloc[-1] == k_data.high[i] and temp_data.low.iloc[-1] > k_data.low[i] # 第2根包含第1根
        case3 = temp_data.high.iloc[-1] == k_data.high[i] and temp_data.low.iloc[-1] == k_data.low[i] # 第1根等于第2根
        case4 = temp_data.high.iloc[-1] > k_data.high[i] and temp_data.low.iloc[-1] > k_data.low[i] # 向下趋势
        case5 = temp_data.high.iloc[-1] < k_data.high[i] and temp_data.low.iloc[-1] < k_data.low[i] # 向上趋势
        if case1_1 or case1_2 or case1_3:
            if zoushi[-1] == 4:
                temp_data.high.iloc[-1] = k_data.high.iloc[i]
            else:
                temp_data.low.iloc[-1] = k_data.low.iloc[i]
            
        elif case2_1 or case2_2 or case2_3:
            temp_temp = temp_data.iloc[-1:]
            temp_data = k_data[i:i+1]
            if zoushi[-1] == 4:
                temp_data.high.iloc[-1] = temp_temp.high.iloc[0]
            else:
                temp_data.low.iloc[-1] = temp_temp.low.iloc[0]
                
        elif case3:
            zoushi.append(3)
            after_fenxing = pd.concat([after_fenxing,temp_data],axis = 0)
            temp_data = k_data[i:i+1]
            
        
        elif case4:
            zoushi.append(4)
            after_fenxing = pd.concat([after_fenxing,temp_data],axis = 0)
            temp_data = k_data[i:i+1]
            
        elif case5:
            zoushi.append(5)
            after_fenxing = pd.concat([after_fenxing,temp_data],axis = 0)
            temp_data = k_data[i:i+1]
    for i in range(len(after_fenxing)):
        if after_fenxing.open.iloc[i] > after_fenxing.close.iloc[i]:
            after_fenxing.open.iloc[i] = after_fenxing.high.iloc[i]
            after_fenxing.close.iloc[i] = after_fenxing.low.iloc[i]
        else:
            after_fenxing.open.iloc[i] = after_fenxing.low.iloc[i]
            after_fenxing.close.iloc[i] = after_fenxing.high.iloc[i]
    return k_data,after_fenxing,temp_data




def FenBi(k_data):
    temp_num = 0#上一个顶或底的位置
    temp_high = 0 #上一个顶的high值
    temp_low = 0 #上一个底的low值
    temp_type = 0 # 上一个记录位置的类型
    i = 3
    result = pd.DataFrame() # 分型点的DataFrame值
    while (i < len(k_data)-3):
        case1 = k_data.high.iloc[i-1]<k_data.high.iloc[i] and k_data.high.iloc[i]>k_data.high.iloc[i+1] and k_data.high.iloc[i-2]<k_data.high.iloc[i] and k_data.high.iloc[i]>k_data.high.iloc[i+2] and k_data.high.iloc[i-3]<k_data.high.iloc[i] and k_data.high.iloc[i]>k_data.high.iloc[i+3] #顶分型
        case2 = k_data.low.iloc[i-1]>k_data.low.iloc[i] and k_data.low.iloc[i]<k_data.low.iloc[i+1] and k_data.low.iloc[i-2]>k_data.low.iloc[i] and k_data.low.iloc[i]<k_data.low.iloc[i+2] and k_data.low.iloc[i-3]>k_data.low.iloc[i] and k_data.low.iloc[i]<k_data.low.iloc[i+3] #底分型
        if case1:
            if temp_type == 1: # 如果上一个分型为顶分型，则进行比较，选取高点更高的分型 
                if k_data.high.iloc[i] <= temp_high:
                    i += 1
                else:
                    temp_high = k_data.high.iloc[i]
                    temp_num = i
                    
                    temp_type = 1
                    i += 1
            elif temp_type == 2 : # 如果上一个分型为底分型，则记录上一个分型，用当前分型与后面的分型比较，选取同向更极端的分型
                if temp_low >= k_data.high.iloc[i]: # 如果上一个底分型的底比当前顶分型的顶高，则跳过当前顶分型。
                    i += 1
                elif i<temp_num+4:  #顶和底至少5k线
                    i+=1 
                else:
                    result = pd.concat([result,k_data.iloc[temp_num:temp_num+1]],axis = 0)
                    temp_high = k_data.high.iloc[i]
                    temp_num = i
                    temp_type = 1
                    i += 1
            else:
                temp_high = k_data.high.iloc[i]
                temp_num = i
                temp_type = 1
                i += 1
                
        elif case2:
            if temp_type == 2: # 如果上一个分型为底分型，则进行比较，选取低点更低的分型 
                if k_data.low.iloc[i] >= temp_low:
                    i += 1
                else:
                    temp_low = k_data.low.iloc[i]
                    temp_num = i
                    temp_type = 2
                    i += 1
            elif temp_type == 1 : # 如果上一个分型为顶分型，则记录上一个分型，用当前分型与后面的分型比较，选取同向更极端的分型
                if temp_high <= k_data.low.iloc[i]: # 如果上一个顶分型的底比当前底分型的底低，则跳过当前底分型。
                    i += 1
                elif i<temp_num+4:  #顶和底至少5k线
                    i+=1
                else:
                    result = pd.concat([result,k_data.iloc[temp_num:temp_num+1]],axis = 0)
                    temp_low = k_data.low.iloc[i]
                    temp_num = i
                    temp_type = 2
                    i += 1
            else:
                temp_low = k_data.low.iloc[i]
                temp_num = i
                temp_type = 2
                i += 1
        else:
            i += 1
    return result



def do_work():
    k_data = pd.read_excel(r'C:\Users\15308\Desktop\嘉沃资产\分笔分型\data.xlsx')
    k_data.columns = ['high','low','open','close']
    k_data['time'] = k_data.index
    k_data.index = range(len(k_data))
    result = FenBi(k_data)
    df = result
    time = list(df.time.values)
    k_data,after_fenxing,temp_data = FenXing(k_data)
    for i in range(len(after_fenxing)):
        if (after_fenxing.iloc[i]['time'] in time) and (after_fenxing.iloc[i+2]['time'] in time):
            df = df[~df['time'].isin([after_fenxing.iloc[i]['time'],after_fenxing.iloc[i+2]['time']])]
    return result

if __name__ == '__main__':
    result = do_work()
