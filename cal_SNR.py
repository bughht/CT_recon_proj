import numpy as np

mean_red = np.load('mean_red.npy')
std_red = np.load('std_red.npy')
mean_green = np.load('mean_green.npy')
std_green = np.load('std_green.npy')

SNR_red = 10*np.log10(mean_red/std_red)
SNR_green = 10*np.log10(mean_green/std_green)

print(mean_red)
print(mean_green)

print(SNR_red)
print(SNR_green)