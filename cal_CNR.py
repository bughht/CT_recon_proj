import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

def CNR(mu1,mu2,sigma1,sigma2):
    return 10*np.log10(np.abs(mu1-mu2)/np.sqrt(sigma1**2+sigma2**2))

# RED
print("RED")
mean_red = np.load('mean_red.npy')
std_red = np.load('std_red.npy')
mean_bkgd_red = np.load('mean_bkgd_red.npy')
std_bkgd_red = np.load('std_bkgd_red.npy')

CNR_red = CNR(mean_red,mean_bkgd_red,std_red,std_bkgd_red)
print(CNR_red)

# GREEN
print("GREEN")
mean_green = np.load('mean_green.npy')
std_green = np.load('std_green.npy')
mean_bkgd_green = np.load('mean_bkgd_green.npy')
std_bkgd_green = np.load('std_bkgd_green.npy')

print("mean bkgd green",mean_bkgd_green)
print("std bkgd green",std_bkgd_green)
print("mean bkgd red",mean_bkgd_red)
print("std bkgd red",std_bkgd_red)

print(mean_green)
print(std_green)
print(mean_bkgd_green)
print(std_bkgd_green)

CNR_green = CNR(mean_green,mean_bkgd_green,std_green,std_bkgd_green)
print(CNR_green)

df = pd.DataFrame({'RED Light CNR/dB':CNR_red.flatten(),'GREEN Light CNR/dB':CNR_green.flatten(),'ROI color':np.concatenate([['RED' for _ in range(4)],['GREEN' for _ in range(4)],['BLACK' for _ in range(4)]]),'ROI layer':np.tile(['layer1','layer2','layer3','layer4'],3)})

df.to_csv("CNR.csv")

print(df)

plt.figure(figsize=(13,5))
plt.subplot(1,2,1)
sns.barplot(data=df,x='ROI layer',y='RED Light CNR/dB',hue='ROI color',palette=['r','g','k'])
plt.subplot(1,2,2)
sns.barplot(data=df,x='ROI layer',y='GREEN Light CNR/dB',hue='ROI color',palette=['r','g','k'])
plt.show()
