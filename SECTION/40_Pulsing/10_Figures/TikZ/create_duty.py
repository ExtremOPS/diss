import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def duty_sine(f, f_duty, duty, offset=0.):
    n = 500
    t = np.linspace(0, 2.1*f_duty, num=n)
    out = offset*np.ones_like(t)

    t_duty = 1/f_duty

    for i, val in enumerate(t):
        #  condition = (val-val//t_duty*t_duty)/t_duty
        condition = val % t_duty
        if condition < duty:
            out[i] = np.sin(condition*f/f_duty*2*np.pi) + offset
            #  out[i] = duty

    return t, out


t, sin_50 = duty_sine(10, 1, 0.5, 4)
_, sin_70 = duty_sine(10, 1, 0.7, 2)
_, sin_100 = duty_sine(10, 1, 1.5)

df = pd.DataFrame()

df['time'] = t
df['duty_50'] = sin_50
df['duty_70'] = sin_70
df['duty_100'] = sin_100

df.to_csv('duty_cycle.dat', float_format='%+.4e', index=False, sep=' ')


#  plt.plot(t, sin_100, color='orange')
#  plt.plot(t, sin_70, color='g')
#  plt.plot(t, sin_50, color='r')
#  plt.axis('off')
#  plt.savefig('sine.png', transparent=True, bbox_inches='tight')
#  plt.show()
