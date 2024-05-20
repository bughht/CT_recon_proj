import astra
from load_data import CT_data
import numpy as np

def CT_recon(data:CT_data):
    cone_geom = astra.create_proj_geom(
        'cone',
        1,
        1,
        data.data.shape[0],
        data.data.shape[2],
        np.linspace(0, 2*np.pi, 320, endpoint=False),
        data.source_origin,
        data.origin_det
    )
    sinogram_id = astra.data3d.create(datatype='-sino', data=data.data, geometry=cone_geom)

    vol_geom = astra.create_vol_geom(640,640,480)
    cfg = astra.astra_dict('FDK_CUDA')
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
    recon_red, sinogram_red = CT_recon(CT_data_red)
    recon_green, sinogram_green= CT_recon(CT_data_green)

    slice = np.array([100,180,260,340])+15

    plt.figure()
    for i in range(4):
        plt.subplot(2,4,i+1)
        plt.imshow(recon_red[slice[i]])
        plt.clim(0,0.008)
        plt.colorbar()
        plt.subplot(2,4,i+5)
        plt.imshow(recon_green[slice[i]])
        plt.clim(0,0.008)
        plt.colorbar()
    plt.show()

    np.save('recon_red.npy',recon_red)
    np.save('recon_green.npy',recon_green)