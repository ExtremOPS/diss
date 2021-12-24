import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

a = np.linspace(0.01, 0.5, num=51)

beta = np.linspace(0, 72 / 180 * np.pi, num=50)

A, B = np.meshgrid(a, beta)


#  theta = np.arctan(A * np.sin(gamma) / (1 - A * np.cos(gamma))) / np.pi * 180
#  theta = B/np.pi*180 - gamma

theta = np.arcsin(A * np.sin(np.pi-B))/np.pi*180
gamma = 180 - (180-B/np.pi*180) - theta

print(theta.max())
print(gamma.min())
print(gamma.max())

plt.contourf(A, B/np.pi*180, gamma)
plt.colorbar()
plt.show()

#  print(theta.shape)

# export to dat file
data = []
for i, ia in enumerate(a):
    for j, b in enumerate(beta):
        data.append([ia, b/np.pi*180, gamma[j, i], theta[j, i]])


#  #  plt.contourf(A, B, theta)
#  #  plt.show()

columns = ['a', 'beta', 'gamma', 'theta']
#  print(columns)
df = pd.DataFrame(data=data, columns=columns)
df.head()
df.to_csv('angles_mat.dat', sep=' ', float_format='%+.3e', index=False)
