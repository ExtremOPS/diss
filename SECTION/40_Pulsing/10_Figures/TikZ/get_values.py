import pandas as pd

df = pd.read_csv('./duty_fp_10000.dat', sep=' ')
print(df.head())

i_col = df.columns.get_loc('DV_y_m04_050_m00')


row = 64

out = '{'
while row < len(df):
    t = int(df.iloc[row, 0])
    val = df.iloc[row, i_col]
    out += f'{t}/{val:.3f},'
    row += 5

out = out[:-2]+'}'
print(out)
