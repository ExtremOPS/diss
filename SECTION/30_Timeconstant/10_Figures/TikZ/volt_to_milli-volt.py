import pandas as pd

df = pd.read_csv('averaged_yz_Voltages.dat', sep='\s')

print(df.head())

cols = df.columns.to_list()
cols.remove('dy')
print(cols)

for col in cols:
    df[col] = 1000*df[col]

print(df.head())

df.to_csv('averaged_yz_mVoltages.dat', sep=' ', float_format='%+4.2e',
          index=False)
