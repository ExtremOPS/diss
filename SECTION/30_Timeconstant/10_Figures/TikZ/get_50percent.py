import pandas as pd
import numpy as np

df = pd.read_csv('evolution_yz_Voltages.dat', sep=' ')
print(df.head())

cols = df.columns.to_list()
cols.remove('dt')

for col in cols:
    index = np.where(df[col] > 0.5)
    index = index[0][0]
    print(f'{col} -> dt@0.5 = {df.iloc[index,0]}')
