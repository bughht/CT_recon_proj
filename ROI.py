import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import disk

recon_red = np.load('recon_red.npy')
recon_green = np.load('recon_green.npy')

recon_red = (recon_red-recon_red.min())/(np.max(recon_red)-np.min(recon_red))
recon_green = (recon_green-recon_green.min())/(np.max(recon_green)-np.min(recon_green))

plt.figure()
plt.subplot(1,2,1)
plt.imshow(recon_red[80])
plt.subplot(1,2,2)
plt.imshow(recon_green[80])

plt.figure()
plt.imshow(recon_red.sum(axis=1))
plt.show()


layer = np.array([
    [70, 120],
    [155, 205],
    [240, 290],
    [325, 375]
])

r = 55

# center_red = np.array([
#     [210, 350],
#     [320, 200],
#     [405, 400]
# ])
center_green = np.array([
    [225, 370],
    [280, 210],
    [420, 370]
])
center_red = center_green

def msk_generate(recon, center, layer, r):
    rr, cc = disk((center[0], center[1]), r, shape = recon.shape[1:])
    msk = np.zeros_like(recon, dtype=bool)
    msk[layer[0]:layer[1], rr, cc] = 1
    return msk

ROI_red = []
ROI_green = []

for center_idx in range(3):
    for l in layer:
        ROI_red.append(msk_generate(recon_red, center_red[center_idx], l, r))
        ROI_green.append(msk_generate(recon_green, center_green[center_idx], l, r))


ROI_bkgd = np.zeros(recon_red.shape, dtype=bool)
ROI_bkgd[300:350,480:510,280:330] = 1
plt.imshow(ROI_bkgd.sum(axis=(0)),cmap='gray')
plt.show()

ROI_red = np.array(ROI_red).reshape(3,4, *recon_red.shape)
ROI_green = np.array(ROI_green).reshape(3,4, *recon_green.shape)
print(ROI_red.shape)
plt.subplot(1,3,1)
plt.imshow(ROI_red.sum(axis=(0,1,2)),cmap='gray')
plt.title("ROI Transverse")
plt.subplot(1,3,2)
plt.imshow(ROI_red.sum(axis=(0,1,3)),cmap='gray')
plt.title("ROI Axial")
plt.subplot(1,3,3)
plt.imshow(ROI_red.sum(axis=(0,1,4)),cmap='gray')
plt.title("ROI Coronal")
plt.show()

print("RED")
img_ROI_red = recon_red.copy()
img_ROI_red = np.ma.asarray(img_ROI_red)
std_red = np.zeros(ROI_red.shape[:2])
mean_red = np.zeros(ROI_red.shape[:2])
for i,j in np.ndindex(ROI_red.shape[:2]):
    img_ROI_red.mask = ~ROI_red[i,j]
    std_red[i,j] = img_ROI_red.std()
    mean_red[i,j] = img_ROI_red.mean()
    print(i,j,std_red[i,j],mean_red[i,j])
img_ROI_red.mask = ~ROI_bkgd
mean_bkgd_red = recon_red[ROI_bkgd].mean()
std_bkgd_red = recon_red[ROI_bkgd].std()
print("mean_bkgd_red:",mean_bkgd_red)
print("std_bkgd_red:",std_bkgd_red)

print("GREEN")
img_ROI_green = recon_green.copy()
img_ROI_green = np.ma.asarray(img_ROI_green)
std_green = np.zeros(ROI_green.shape[:2])
mean_green = np.zeros(ROI_green.shape[:2])
for i,j in np.ndindex(ROI_green.shape[:2]):
    img_ROI_green.mask = ~ROI_green[i,j]
    std_green[i,j] = img_ROI_green.std()
    mean_green[i,j] = img_ROI_green.mean()
    print(i,j,std_green[i,j],mean_green[i,j])
img_ROI_green.mask = ~ROI_bkgd
mean_bkgd_green= recon_green[ROI_bkgd].mean()
std_bkgd_green = recon_green[ROI_bkgd].std()
print("mean_bkgd_green:",mean_bkgd_green)
print("std_bkgd_green:",std_bkgd_green)

np.save('mean_red.npy',mean_red)
np.save('std_red.npy',std_red)
np.save('mean_bkgd_red.npy',mean_bkgd_red)
np.save('std_bkgd_red.npy',std_bkgd_red)
np.save('mean_green.npy',mean_green)
np.save('std_green.npy',std_green)
np.save('mean_bkgd_green.npy',mean_bkgd_green)
np.save('std_bkgd_green.npy',std_bkgd_green)

# img_ROI_red[ROI_red[0,0]] = recon_red[ROI_red[0,0]]

img_ROI_red = np.zeros_like(recon_red)
img_ROI_green = np.zeros_like(recon_green)
for i,j in np.ndindex(ROI_red.shape[:2]):
    img_ROI_red[ROI_red[i,j]] = recon_red[ROI_red[i,j]]
    img_ROI_green[ROI_green[i,j]] = recon_green[ROI_green[i,j]]

plt.subplot(2,3,1)
plt.imshow(img_ROI_red[layer[0,0]:layer[0,1]].sum(axis=0))
plt.subplot(2,3,2)
plt.imshow(img_ROI_red[layer[1,0]:layer[1,1]].sum(axis=0))
plt.subplot(2,3,3)
plt.imshow(img_ROI_red[layer[2,0]:layer[2,1]].sum(axis=0))

plt.subplot(2,3,4)
plt.imshow(img_ROI_green[layer[0,0]:layer[0,1]].sum(axis=0))
plt.subplot(2,3,5)
plt.imshow(img_ROI_green[layer[1,0]:layer[1,1]].sum(axis=0))
plt.subplot(2,3,6)
plt.imshow(img_ROI_green[layer[2,0]:layer[2,1]].sum(axis=0))

plt.show()