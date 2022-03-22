import pandas as pd
import os

DIR = os.path.abspath(__file__)
DIR = os.path.dirname(DIR)

df = pd.read_csv(DIR+'/duty_fp_10000.dat', sep=' ')

#  print(df.head())

print(df.loc[df['DV_y_m05_100_m00'] > 0.5])
print(df.loc[df['DV_z_m05_100_m00'] > 0.5])
