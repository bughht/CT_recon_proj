import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")

mean_red = np.load('mean_red.npy')
std_red = np.load('std_red.npy')
mean_green = np.load('mean_green.npy')
std_green = np.load('std_green.npy')

SNR_red = 10*np.log10(mean_red/std_red)
SNR_green = 10*np.log10(mean_green/std_green)

print(mean_red)
print(mean_green)

print("RED")
print(SNR_red)
print("GREEN")
print(SNR_green)

df = pd.DataFrame({'RED Light SNR/dB':SNR_red.flatten(),'GREEN Light SNR/dB':SNR_green.flatten(),'ROI color':np.concatenate([['RED' for _ in range(4)],['GREEN' for _ in range(4)],['BLACK' for _ in range(4)]]),'ROI layer':np.tile(['layer1','layer2','layer3','layer4'],3)})

df.to_csv("SNR.csv")


print(df)

plt.figure(figsize=(13,5))
plt.subplot(1,2,1)
sns.barplot(data=df,x='ROI layer',y='RED Light SNR/dB',hue='ROI color',palette=['r','g','k'])
plt.subplot(1,2,2)
sns.barplot(data=df,x='ROI layer',y='GREEN Light SNR/dB',hue='ROI color',palette=['r','g','k'])
plt.show()
