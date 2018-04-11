import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack

d = np.linspace(1.5,25.5,25)
fx = np.linspace(0.0, 1.0/(2.0*0.999/1000), 1000/2)

fy = np.zeros(1000)

m = np.zeros(25)
s = np.zeros(25)

for i in range(25):
	se = pd.read_csv('Sharp '+str(15 + 10*i)+'mm/anag2.csv', header=None, squeeze = True)
	m[i] = se.mean()
	s[i] = se.std()
	se.plot.kde()
	fy = fy + scipy.fftpack.fft(se.values)

fy = scipy.fftpack.fft(se.values)

#plt.plot(d, m, c='b', alpha = 1)
#plt.fill_between(d, m-s, m+s, facecolor='r', alpha = 0.3)
#plt.plot(fx, 2.0/1000 * np.abs(fy[:1000//2]), c='b', alpha = 1)
#se.plot.kde()
plt.show()
