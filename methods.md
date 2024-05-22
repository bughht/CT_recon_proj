# Methods

## Data Acquisition

The experimental procedure for this project involves using a Dual-Energy CT (DECT) to scan colored objects within a phantom, utilizing different wavelengths of light. The materials required include the DECT phantom, 2 liters of water, and the Desk CAT Multi-slice Optical CT Scanner. The steps are as follows:
1. Select either the Red LED lights or Green LED lights as the light source using the Wavelength Selection Switch.
2. Adjust the camera settings to 50% of maximum brightness to ensure evenly distributed noise.
3. Perform geometry calibration by selecting Auto-Cal under Calibration、Geometry Calibration, ensuring no phantom is loaded during this process.
4. Set the number of projections on the side panel to acquire data, and scan reference data without placing the phantom.
5. Load the DECT Phantom into the scanner, secure it with the Jar Clamp, and mount it onto the Rotary Stage. Initiate a Data Scan and wait for completion.
6. Select the Hamming Filter under Reconstruction → Reconstruction Options and initiate the reconstruction process using the Voxel Resolution option.
7. Switch the light source and repeat the above steps.

The raw data collected includes ScanData (projection data with the phantom) and ScanRef (projection data without the phantom), along with calibration and information files. 

## Data Preprocessing 

The scan and reference data for green and red LED light acquisition are saved as 320 BMP images of uint16 data type, loaded with numpy. The calibration parameter are stored in an XML file and loaded using BeautifulSoup. The preprocessing involves the following steps:

1. Flat field correction is done by taking the logarithm of the ratio of reference data to scan data. Conventional methods of flat field correction is given by equation below. 

$$I = \log(\frac{I_{ref}-I_{dark}}{I_{scan}-I_{dark}})$$

However, in this case, the dark field data $I_{dark}$ is not available, so here we applied a low pass filter to extract the dark field data $\hat{I}_{dark}$ with low frequency components. The flat field correction is then given by:

$$I = \log(\frac{I_{ref}-\hat{I}_{dark}}{I_{scan}-\hat{I}_{dark}})$$

Ring artifacts are significantly reduced by applying the flat field correction.

2. Geometry correction is performed by shifting the data by the offset of the axis of rotation. It's convincing that the offsets provided in the calibration file is not accurate, so we manually adjust the offset to align the sinogram.

3. Parameters for FBP reconstruction are calculated using the calibration data. The parameters include SourceToAxis, AxisToDetector, HorizLightSize, VertLightSize, AxisOfRotationOffset, EquatoralOffset, HorizPixelSize, and VertPixelSize.

## Data Reconstruction

Astra Toolbox is used for the reconstruction of the data, which is a high-performance GPU-accelerated reconstruction library. Astra provides a set of tools for 2D and 3D tomography, including BP and FDK reconstruction algorithms. For this project, we utilize the "BP3D_CUDA" algorithm for filtered back projection (FBP) and "FDK_CUDA" for the Feldkamp-Davis-Kress (FDK) reconstruction method.

For both methods, the following steps are taken:

1. Create the geometry of the scanner using the calibration data.

```python
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
```

2. Initialize the FBP algorithm and perform the reconstruction, then get the reconstructed volume of 640x640x640:

```python
vol_geom = astra.create_vol_geom(640,640,480)
cfg = astra.astra_dict('FDK_CUDA')
cfg['ReconstructionDataId'] = astra.data3d.create(datatype='-vol', geometry=vol_geom,data=0)
cfg['ProjectionDataId'] = sinogram_id
alg_id = astra.algorithm.create(cfg)

astra.algorithm.run(alg_id, 1)
recon = astra.data3d.get(cfg['ReconstructionDataId'])
sinogram = astra.data3d.get(cfg['ProjectionDataId'])
```

Filtering process is not included in the "BP3D_CUDA" algorithm. We applied a high-pass ramp filter to the sinogram before reconstruction to reduce the artifacts. The ramp filter is given by:

$$H(u) = |u|$$

The filtering process is performed in the frequency domain by multiplying the Fourier transform of the sinogram with the ramp filter, as is demonstrated in the code below:

```python
ramp_window = np.ones(data.data.shape[2])
print(ramp_window.shape)
ramp_window[:len(ramp_window)//2] = np.linspace(1,0,len(ramp_window)//2)
ramp_window[len(ramp_window)//2:] = np.linspace(0,1,len(ramp_window)-len(ramp_window)//2)
data_fourier = fftshift(fft(ifftshift(data.data,axes=2),axis=2),axes=2)
data_fourier = data_fourier*ramp_window[np.newaxis,np.newaxis,:]
data.data = (fftshift(ifft(ifftshift(data_fourier,axes=2),axis=2),axes=2))
```

## Data Postprocessing

The reconstructed data is saved as a 3D numpy array. ROI analysis is performed to extract the volume of the object in the phantom. Given that the DECT phantom is a cylinder with 3 different colored objects with 4 levels of visibility. ROI is generated by manually selecting the cylindrical region of interest in the reconstructed volume. The center of the cylinder of red, green, and black objects are [225, 370], [280, 210], and [420, 370], respectively. The radius of the cylinder is 55 pixels. The mask is generated and given in the following figure.

# Analysis

