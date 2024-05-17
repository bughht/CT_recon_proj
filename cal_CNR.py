import numpy as np

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

CNR_green = CNR(mean_green,mean_bkgd_green,std_green,std_bkgd_green)
print(CNR_green)
