import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize


df = pd.read_csv('datapoints.dat', sep=',', index_col=False)
y = np.asarray(df['y'])
f = np.asarray(df['f'])


def fitFunc(x, a, b, c):
    return np.abs(c*np.sin(a*x+b))


params, params_covariance = optimize.curve_fit(
    fitFunc, y, f, p0=[3.3, 1.03, 230])

print(params)

plt.figure(figsize=(6, 4))
plt.scatter(y, f)

yMore = np.linspace(float(y[0]), float(y[-1]), 5e2)
plt.plot(yMore, fitFunc(yMore, *params), label='Fitted function')

plt.legend(loc='best')

plt.show()
