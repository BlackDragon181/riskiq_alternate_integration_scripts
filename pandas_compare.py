from doctest import OutputChecker
import pandas as pd

df1 = pd.read_csv('q_kb.csv') #qualys know
df2 = pd.read_csv('bc.csv') #target
output_workbook = 'output.xlsx'

inner_join = pd.merge(df1, df2, on ='QID', how ='inner')
print(inner_join)
inner_join.to_excel(output_workbook,index=False)

print(dir(pd))
