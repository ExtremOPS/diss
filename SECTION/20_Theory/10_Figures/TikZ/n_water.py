import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('Segelstein1981.dat', sep='\t', index_col=False)
df.wl *= 1e3
wl = df.wl.to_numpy()*1e-9
k = df.k.to_numpy()

a = 4*np.pi/wl*k
df["a"] = a
print(df.head())
df.to_csv('Segelstein1981a.dat', sep=' ', float_format='%.5e', index=False)

#  fig, ax = plt.subplots(1, 1)

#  ax.semilogy(wl, k)

#  ax = ax.twinx()
#  ax.semilogy(wl, a)

#  plt.show()
