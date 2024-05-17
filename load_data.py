import numpy as np
import matplotlib.pyplot as plt
import os
from load_calib import Calibration_data
from scipy.ndimage import gaussian_filter, median_filter

class CT_data:
    def __init__(self,path,img_w=480,img_h=640,img_num=320) -> None:
        self.path_data = os.path.join(path,'ScanData')
        self.path_ref = os.path.join(path,'ScanRef')
        self.img_w, self.img_h, self.img_num = img_w, img_h, img_num
        self.scan_data = self.load_data(self.path_data)
        self.ref_data = self.load_data(self.path_ref)

        # Normalize
        self.data = np.log10(self.ref_data/self.scan_data)

        # filter
        kernel_size = [5,1,1]
        self.data = gaussian_filter(self.data, sigma=kernel_size )
        

        # Calibration
        self.Calibration = Calibration_data(os.path.join(path,'calibration.xml'))
        self.data = np.roll(self.data, -int(self.Calibration.AxisOfRotationOffset), axis=2)

        # Calc Param
        self.calculate_param()

    def load_data(self,path,offset=27):
        data = np.zeros((self.img_w, self.img_num, self.img_h))
        for slice_idx, data_name in enumerate(os.listdir(path)):
            with open(os.path.join(path,data_name), 'rb') as f:
                data[:,slice_idx,:] = np.fromfile(f, dtype=np.uint16)[offset:].reshape(self.img_w,self.img_h)
        return data

    def calculate_param(self):
        self.detector_pixel_size = self.Calibration.HorizPixelSize / self.img_h
        self.source_origin = self.Calibration.SourceToAxis/self.detector_pixel_size
        self.origin_det = self.Calibration.AxisToDetector/self.detector_pixel_size

if __name__ == "__main__":
    test_green = CT_data('data/GREEN')
