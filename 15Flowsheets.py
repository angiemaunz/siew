# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:39:02 2020

@author: User
"""

import pdftotext
import re
import pandas as pd

with open("15Flowsheets.pdf",'rb') as f:
    pdf = pdftotext.PDF(f)

keywordList = ['pain','restrain','sedetion']
# Iterate over all the pages
count = 0
df_result = pd.DataFrame()
target = ''
box_str = ''
bool_target = False
bool_time = False
for i,page in enumerate(pdf):
    if i>50:
        break

    for row in page.split('\n'):
        if bool_target == True:
            if re.search('\, (\d){4}',row):
                bool_time = False
                if re.search('(continued)',row)== None:

                    if box_str !='':
                        df_result.loc[count_start,'Content'] = box_str
                        for keyword in keywordList:
                            if re.search(keyword,box_str,re.IGNORECASE):
                                df_result.loc[count_start,keyword] = 'Yes'
                            else:
                                df_result.loc[count_start,keyword] = 'No'
                    count_start = count
                    print(row)
                    df_result.loc[count,'Date'] = row.split(' - ')[1].strip()
                    str_date = row.split(' - ')[1].strip()
                    df_result.loc[count,'Title'] = row.split(' - ')[0].strip()
                    str_title = row.split(' - ')[0].strip()
                    count += 1
                    box_str = ''
                else:                    
                    pass
            elif re.search('User Key',row):
                bool_time = False
                if box_str !='':
                    df_result.loc[count_start,'Content'] = box_str
                    for keyword in keywordList:
                        if re.search(keyword,box_str,re.IGNORECASE):
                            df_result.loc[count_start,keyword] = 'Yes'
                        else:
                            df_result.loc[count_start,keyword] = 'No'
                count_start = count
                print(row)
                df_result.loc[count,'Date'] = row.split(' - ')[1].strip()
                str_date = row.split(' - ')[1].strip()
                df_result.loc[count,'Title'] = row.split(' - ')[0].strip()
                str_title = row.split(' - ')[0].strip()
                count += 1
                box_str = ''
                bool_target = False
            elif re.search('Row Name',row):
                tmp = row.replace('Row Name','').split()
                #print(row)
                index_dict = {}
                for t in tmp:
                    #print(t, row.index(t))
                    index_dict[t]= row.index(t)
                #print(len(tmp))
                #print(tmp)
                #print(index_dict)
                bool_time = True
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif bool_time == True:
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
                print(row)
                timeList = []
                for key in index_dict.keys():
                    timeList.append(key)
                print(timeList)
                for k,time in enumerate(timeList):
                    print(k, time)
                    if k == 0:
                        T_title = row[0:index_dict[timeList[k]]]
                    if k == len(timeList)-1:
                        #print(timeList[k],index_dict[timeList[k]])
                        start_i = index_dict[timeList[k]]
                        end_i = len(row)
                    else:
                        #print(timeList[k],index_dict[timeList[k]],timeList[k+1],index_dict[timeList[k+1]])
                        start_i = index_dict[timeList[k]]
                        end_i = index_dict[timeList[k+1]]
                    print(row[start_i:end_i])
                    df_result.loc[count,'Date'] = str_date
                    df_result.loc[count,'Title'] = str_title
                    df_result.loc[count,'Time'] = timeList[k]
                    df_result.loc[count,'T_Column'] = T_title
                    df_result.loc[count,'T_Content'] = row[start_i:end_i].split('-')[0]
                    try:
                        df_result.loc[count,'T_Person'] = row[start_i:end_i].split('-')[1]
                    except:
                        df_result.loc[count,'T_Person'] = ''
                    count += 1
            else:
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
                #print(target)
        
            
        else:
            if re.search('Flowsheets',row):
                bool_target = True

df_result = df_result.loc[:,['Date', 'Title','Content','pain', 'restrain', 'sedetion','Time', 'T_Column', 'T_Content', 'T_Person']]
df_result.to_excel('15Flowsheets_50pages.xlsx.xlsx')   