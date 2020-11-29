# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:57:45 2020

@author: User
"""

import pdftotext
import re
import pandas as pd

with open("09AllOrders.pdf",'rb') as f:
    pdf = pdftotext.PDF(f)

keywordList = ['pain','restrain','sedetion']
# Iterate over all the pages
count = 0
df_result = pd.DataFrame()
target = ''
box_str = ''
bool_target = False
bool_a = False
bool_q = False
for i,page in enumerate(pdf):
    #if i>5:
    #    break

    for row in page.split('\n'):
        if bool_target == True:
            if re.search('\[\d+\]',row):
                bool_q = False
                bool_a = False
                print(row)
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
                    df_result.loc[count,'OrderName'] = row.split(' [')[0].strip()
                    str_order = row.split(' [')[0].strip()
                    df_result.loc[count,'Code'] = row.split(' [')[1].replace(']','')
                    str_code = row.split(' [')[1].replace(']','')
                    count += 1
                    box_str = ''
                else:                    
                    pass
            elif re.search('Questionnaire',row):
                bool_q = True
            elif bool_q == True and re.search('Question',row):      
                #print(row)
                tmp = row.split()
                #print(tmp)
                #print(row)
                index_dict = {}
                for t in tmp:
                    #print(t, row.index(t))
                    index_dict[t]= row.index(t)
                #print(len(tmp))
                #print(tmp)
                #print(index_dict)
                bool_a = True
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif bool_a == True and re.search('Printed on',row)==None:
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
                #print(row)
                timeList = []
                for key in index_dict.keys():
                    timeList.append(key)
                #print(timeList)
                for k,time in enumerate(timeList):
                    #print(k, time)
                    if k == len(timeList)-1:
                        #print(timeList[k],index_dict[timeList[k]])
                        start_i = index_dict[timeList[k]]
                        end_i = len(row)
                        df_result.loc[count,'Answer'] = row[start_i:end_i]
                    else:
                        #print(timeList[k],index_dict[timeList[k]],timeList[k+1],index_dict[timeList[k+1]])
                        start_i = index_dict[timeList[k]]
                        end_i = index_dict[timeList[k+1]]
                        df_result.loc[count,'Question'] = row[start_i:end_i]
                    #print(row[start_i:end_i])
                    
                    #df_result.loc[count,'Date'] = str_date
                    #df_result.loc[count,'Title'] = str_title
                    #df_result.loc[count,'Time'] = timeList[k]
                    #df_result.loc[count,'T_Column'] = T_title
                    #df_result.loc[count,'T_Content'] = row[start_i:end_i].split('-')[0]
                    #try:
                    #    df_result.loc[count,'T_Person'] = row[start_i:end_i].split('-')[1]
                    #except:
                    #    df_result.loc[count,'T_Person'] = ''
                count += 1
            elif re.search('Printed on',row):
                pass
            elif re.search('Medication comments',row):
                df_result.loc[count_start,'Medication comments'] = row.split(':',1)[1]
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif re.search('PRN Comment',row):
                df_result.loc[count_start,'PRN Comment'] = row.split(':',1)[1]
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif re.search('Order comments',row):
                df_result.loc[count_start,'Order comments'] = row.split(':',1)[1]
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif re.search(':',row) and re.match('^    ',row)== None:

                print(len(re.findall(':', row)))
                
                if len(re.findall(':', row)) ==2:
                    print(row)
                    #print(row.rsplit(':',1)[0].rsplit('   ',1)[1])
                    SColname = row.rsplit(':',1)[0].rsplit('   ',1)[1].strip()
                    #print(row.rsplit(':',1)[1])
                    SColVal= row.rsplit(':',1)[1]
                    df_result.loc[count_start,SColname] = SColVal
                    #print(row.split('   ')[0])
                    FColname = row.split('   ')[0].split(':')[0].strip()
                    FColVal = row.split('   ')[0].split(':')[1]
                    df_result.loc[count_start,FColname] = FColVal
                    #print(row.split('Status: ')[1])
                elif len(re.findall(':', row)) ==1:
                    FColname = row.split(':')[0].strip()
                    FColVal = row.split(':')[1]
                    df_result.loc[count_start,FColname] = FColVal
                else:
                    print(row)
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')  
            else:
                
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
                #print(target)
            """
            if re.search('[\d+]',row):
                bool_time = False
                print(row)
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
            # need to identify last page
            
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
            elif re.search('Questionnaire',row):
                bool_q = True
            elif bool_q == True:
                tmp = row.split()
                #print(row)
                index_dict = {}
                for t in tmp:
                    #print(t, row.index(t))
                    index_dict[t]= row.index(t)
                #print(len(tmp))
                #print(tmp)
                #print(index_dict)
                bool_a = True
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            elif bool_a == True:
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
            """
            
        else:
            if re.search('All Orders',row.strip()):
                bool_target = True

#df_result = df_result.loc[:,['Date', 'Title','Content','pain', 'restrain', 'sedetion','Time', 'T_Column', 'T_Content', 'T_Person']]
df_result.to_excel('09AllOrders.xlsx')   