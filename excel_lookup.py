import pandas as pd
import numpy as np
import openpyxl

initial_workbook = 'Qualys_KB.xlsx' #Qualys knowledge database
info_workbook = 'bc.xlsx' #target plugins
output_workbook = 'output.xlsx'

df_initial = pd.read_excel(initial_workbook)
df_info = pd.read_excel(info_workbook)

#print(df_initial.columns)
#print(df_info.columns)

df_3 = pd.merge(df_initial,df_info[['QID']], on='QID', how='left')
print(df_3)

df_3.to_excel(output_workbook,index=False)
