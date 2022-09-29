##to combine many X:1 csvs from https://www.spenergynetworks.co.uk/pages/priority_services_register.aspx into a single, ordered table with correct headings
from os import listdir
from os.path import isfile, join
import pandas as pd

mypath = '<<path to CSVs>>'
pattern = ['0']

final_df = pd.DataFrame()

for x in listdir(mypath):
    if x.startswith(tuple(pattern)):
        f = join(mypath, x)
        df = pd.read_csv (f)
        old_col = df.columns[2]
        new_col = df.columns[1]
        df.sort_values(new_col, inplace=True)
        #print(df.iloc[:, 1:3])
        df.rename( {new_col:''}, axis='columns', inplace=True )
        df.rename( {old_col:new_col}, axis='columns', inplace=True )
        df.drop(df.columns[[0]], axis=1 , inplace=True)
        df.reset_index(drop=True, inplace=True)
        print(df)
        df1_transposed = df.transpose()
        print(df1_transposed)
        final_df = final_df.append((df1_transposed.iloc[1:]))
        print(final_df)
final_df.to_csv("<<PATH>>combines.csv", header=True)
