##to combine many csvs into 1
import os
import glob
import pandas as pd
os.chdir("<<PATH>>")


extension = 'csv'
all_filenames = [i for i in glob.glob('*_conwy_uprn_*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "<<FILE>>", index=False, encoding='utf-8-sig')