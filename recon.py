import astra
from load_data import CT_data
import numpy as np
from numpy.fft import *

def CT_recon(data:CT_data,init_angle=0,recon_algo="FDK_CUDA"):
    print(data.data.shape)
    if recon_algo == "BP3D_CUDA":
        ramp_window = np.ones(data.data.shape[2])
        print(ramp_window.shape)
        ramp_window[:len(ramp_window)//2] = np.linspace(1,0,len(ramp_window)//2)
        ramp_window[len(ramp_window)//2:] = np.linspace(0,1,len(ramp_window)-len(ramp_window)//2)
        data_fourier = fftshift(fft(ifftshift(data.data,axes=2),axis=2),axes=2)
        data_fourier = data_fourier*ramp_window[np.newaxis,np.newaxis,:]
        plt.subplot(1,2,1)
        plt.imshow(np.abs(data.data)[330],cmap='gray')
        plt.title("Raw Sinogram")
        # plt.colorbar()
        data.data = (fftshift(ifft(ifftshift(data_fourier,axes=2),axis=2),axes=2))
        plt.subplot(1,2,2)
        plt.imshow(np.abs(data.data)[330],cmap='gray')
        plt.clim(0,0.008)
        plt.title("Filtered Sinogram")
        # plt.colorbar()
        plt.show()
        
    cone_geom = astra.create_proj_geom(
        'cone',
        1,
        1,
        data.data.shape[0],
        data.data.shape[2],
        np.linspace(init_angle, 2*np.pi+init_angle, 320, endpoint=False),
        data.source_origin,
        data.origin_det
    )
    sinogram_id = astra.data3d.create(datatype='-sino', data=data.data, geometry=cone_geom)

    vol_geom = astra.create_vol_geom(640,640,480)
    cfg = astra.astra_dict(recon_algo)
    cfg['ReconstructionDataId'] = astra.data3d.create(datatype='-vol', geometry=vol_geom,data=0)
    cfg['ProjectionDataId'] = sinogram_id
    alg_id = astra.algorithm.create(cfg)

    astra.algorithm.run(alg_id, 1)
    recon = astra.data3d.get(cfg['ReconstructionDataId'])
    sinogram = astra.data3d.get(cfg['ProjectionDataId'])
    print(sinogram.shape,recon.shape)

    return recon,sinogram



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    CT_data_red = CT_data('data/RED')
    CT_data_green = CT_data('data/GREEN')
    # FBP
    recon_red, sinogram_red = CT_recon(CT_data_red,np.deg2rad(18),recon_algo="BP3D_CUDA")
    recon_green, sinogram_green= CT_recon(CT_data_green,recon_algo="BP3D_CUDA")

    # # FDK
    # recon_red, sinogram_red = CT_recon(CT_data_red,np.deg2rad(18),recon_algo="FDK_CUDA")
    # recon_green, sinogram_green= CT_recon(CT_data_green,recon_algo="FDK_CUDA")

    slice = np.array([100,180,260,340])+15

    plt.figure()
    for i in range(4):
        plt.subplot(2,4,i+1)
        plt.imshow(recon_red[slice[i]])
        # plt.clim(0,0.008)
        # plt.colorbar()
        plt.subplot(2,4,i+5)
        plt.imshow(recon_green[slice[i]])
        # plt.colorbar()
    plt.show()

    # np.save('recon_red_FBP.npy',recon_red)
    # np.save('recon_green_FBP.npy',recon_green)
    np.save('recon_red_FDK.npy',recon_red)
    np.save('recon_green_FDK.npy',recon_green)