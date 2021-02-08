import numpy as np
import matplotlib.pyplot as plt


coin = [0,1]

conv = np.convolve(coin, coin)
print(conv)
plt.plot(conv)
plt.show()

dice = [1,2,3,4,5,6]

conv = np.convolve(dice, dice, mode='valid')
print(conv)
plt.plot(conv)
plt.show()
