# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:25:03 2019

@author: 15308
"""


import pandas as pd


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
    return result

if __name__ == '__main__':
    result = do_work()