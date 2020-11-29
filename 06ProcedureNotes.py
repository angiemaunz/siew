# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:20:30 2020

@author: User
"""

#%%
import pdftotext
import re
import pandas as pd

with open("06ProcedureNotes.pdf",'rb') as f:
    pdf = pdftotext.PDF(f)

keywordList = ['pain','restrain','sedation','assess']
# Iterate over all the pages
count = 0
df_result = pd.DataFrame()
target = ''
box_str = ''
bool_target = False
bool_a = False
bool_q = False
for i,page in enumerate(pdf):
    #if i>1:
    #    break
    pref = page.split('\n')[0].strip()
    for row in page.split('\n'):
        if bool_target == True:
            if re.search('^Procedures',row) or re.search('Page 60',row):
                bool_q = False
                bool_a = False
                #print(row)
                if re.search('(continued)',row)== None:

                    if box_str !='':
                        df_result.loc[count_start,'Content'] = box_str
                        for keyword in keywordList:
                            if re.search(keyword,box_str,re.IGNORECASE):
                                df_result.loc[count_start,keyword] = 'Yes'
                            else:
                                df_result.loc[count_start,keyword] = 'No'
                    if re.search('Page 60',row)==None:
                        count_start = count
                        print(row)
                        df_result.loc[count,'Date'] = row.split(' at ')[1].split(maxsplit=1)[0].strip()
                        df_result.loc[count,'Time'] = row.split(' at ')[1].split(maxsplit=1)[1].split('Version')[0].strip()
                        df_result.loc[count,'Version'] = row.split('Version')[1].strip()
                        df_result.loc[count,'Person'] = row.split(' at ')[0].replace('Procedures by','').strip()
                        df_result.loc[count,'PageRef'] = pref
                        #str_order = row.split(' [')[0].strip()
                        #df_result.loc[count,'Code'] = row.split(' [')[1].replace(']','')
                        #str_code = row.split(' [')[1].replace(']','')
                        count += 1
                        box_str = ''
                        bool_q =True
                else:                    
                    pass
            #elif re.search(':',row) and re.search(':$',row.strip())is None:
            #    print(row)
            elif bool_q == True and re.search(': ',row):  
                #print(row)
                #print(len(re.findall('\: ', row)))
                if len(re.findall('\: ', row)) ==3:
                    #print('ROW:',row)
                    #print(row.rsplit(': ',1)[0].rsplit('   ',1)[1])
                    TColname = row.rsplit(': ',1)[0].rsplit('   ',1)[1].strip()
                    #print(row.rsplit(': ',1)[1])
                    TColVal= row.rsplit(': ',1)[1]
                    df_result.loc[count_start,TColname] = TColVal
                    row = re.sub(TColname+'.*','',row)
                    #print(row.rsplit(': ',1)[0].rsplit('   ',1)[1])
                    SColname = row.rsplit(': ',1)[0].rsplit('   ',1)[1].strip()
                    #print(row.rsplit(': ',1)[1])
                    SColVal= row.rsplit(': ',1)[1]
                    df_result.loc[count_start,SColname] = SColVal
                    #print(row.split(': ')[0].strip())
                    FColname = row.split(': ')[0].strip()
                    #print(row.split(SColname)[0].split(':')[1].strip())
                    FColVal = row.split(SColname)[0].split(': ')[1].strip()
                    df_result.loc[count_start,FColname] = FColVal
                    
                elif len(re.findall('\: ', row)) ==2:
                    #print('ROW:',row)
                    #print(row.rsplit(': ',1)[0].rsplit('   ',1)[1])
                    SColname = row.rsplit(': ',1)[0].rsplit('   ',1)[1].strip()
                    #print(row.rsplit(': ',1)[1])
                    SColVal= row.rsplit(': ',1)[1]
                    df_result.loc[count_start,SColname] = SColVal
                    #print(row.split(': ')[0].strip())
                    FColname = row.split(': ')[0].strip()
                    #print(row.split(SColname)[0].split(':')[1].strip())
                    FColVal = row.split(SColname)[0].split(': ')[1].strip()
                    df_result.loc[count_start,FColname] = FColVal
                
                elif len(re.findall(': ', row)) ==1:
                    #print(row)
                    FColname = row.split(': ')[0].strip()
                    FColVal = row.split(': ')[1]
                    df_result.loc[count_start,FColname] = FColVal
                else:
                    print(row)
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n') 
                
            elif bool_q == True  and re.search(': ',row) == None:  
                #print(row)
                bool_q =False
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
            else:
                #print(row)
                target += str(row)
                target += str('\n')
                box_str += str(row)
                box_str += str('\n')
                #print(target)

        else:
            #print(row)
            if re.search('Procedure Notes',row.strip()):
                bool_target = True
    
#df_result = df_result.loc[:,['Date', 'Title','Content','pain', 'restrain', 'sedetion','Time', 'T_Column', 'T_Content', 'T_Person']]
df_result.to_excel('06ProcedureNotes.xlsx')   