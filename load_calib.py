from bs4 import BeautifulSoup

class Calibration_data:
    def __init__(self, path) -> None:
        with open(path,encoding='utf-8') as f_calib:
            self.data_calib=BeautifulSoup(f_calib.read(), "xml")
        self.SourceToAxis=float(self.data_calib.find('SourceToAxis').text)
        self.AxisToDetector=float(self.data_calib.find('AxisToDetector').text)
        self.HorizLightSize=float(self.data_calib.find('HorizLightSize').text)
        self.VertLightSize=float(self.data_calib.find('VertLightSize').text)
        self.AxisOfRotationOffset=float(self.data_calib.find('AxisOfRotationOffset').text)
        self.EquatoralOffset=float(self.data_calib.find('EquatorialOffset').text)
        self.HorizPixelSize=float(self.data_calib.find('HorizPixelSize').text)
        self.VertPixelSize=float(self.data_calib.find('VertPixelSize').text)

if __name__ == "__main__":
    calib_green = Calibration_data('data/GREEN/calibration.xml')
    calib_red = Calibration_data('data/RED/calibration.xml')
    