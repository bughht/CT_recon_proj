import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_style("whitegrid")

mean_red = np.load('mean_red.npy')
std_red = np.load('std_red.npy')
mean_green = np.load('mean_green.npy')
std_green = np.load('std_green.npy')

df_mean_green = pd.DataFrame(data=mean_green)
df_std_green = pd.DataFrame(data=std_green)
# df_mean_green.to_csv("mean_green.csv")
# df_std_green.to_csv("std_green.csv")

df_mean_red = pd.DataFrame(data=mean_red)
df_std_red = pd.DataFrame(data=std_red)
# df_mean_red.to_csv("mean_red.csv")
# df_std_red.to_csv("std_red.csv")


df = pd.DataFrame({'RED Light Signal Standard Deviation':std_red.flatten(),'GREEN Light Signal Standard Deviation':std_green.flatten(),'RED Light Signal Mean':mean_red.flatten(),'GREEN Light Signal Mean':mean_green.flatten(),'ROI color':np.concatenate([['RED' for _ in range(4)],['GREEN' for _ in range(4)],['BLACK' for _ in range(4)]]),'ROI layer':np.tile(['layer1','layer2','layer3','layer4'],3)})

plt.subplot(2,2,1)
sns.barplot(data=df,x='ROI layer',y='RED Light Signal Standard Deviation',hue='ROI color',palette=['r','g','k'])
plt.subplot(2,2,2)
sns.barplot(data=df,x='ROI layer',y='GREEN Light Signal Standard Deviation',hue='ROI color',palette=['r','g','k'])
plt.subplot(2,2,3)
sns.barplot(data=df,x='ROI layer',y='RED Light Signal Mean',hue='ROI color',palette=['r','g','k'])
plt.subplot(2,2,4)
sns.barplot(data=df,x='ROI layer',y='GREEN Light Signal Mean',hue='ROI color',palette=['r','g','k'])

plt.show()