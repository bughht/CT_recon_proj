import numpy as np
import matplotlib.pyplot as plt

recon_red = np.load("recon_red_FDK.npy")*200
recon_red_no = np.load("recon_red_FDK_noflat.npy")*200

plt.figure(figsize=(10,4.8),constrained_layout=True)
plt.subplot(1,2,1)
plt.imshow(recon_red[330],cmap='gray')
plt.xticks([])
plt.yticks([])
plt.clim(0,0.5)
plt.xlabel("a")
# plt.colorbar()
plt.subplot(1,2,2)
plt.imshow(recon_red_no[330],cmap='gray')
plt.xticks([])
plt.yticks([])
plt.clim(0,0.5)
plt.xlabel("b")
plt.colorbar()
plt.show()