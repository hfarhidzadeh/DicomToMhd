import os
import SimpleITK as sitk
import dicom as dc
import numpy as np

Folder_Path = "Folder of Dicom File"
fname = Folder_Path + "\\IndexNumer.txt"
with open(fname) as f:
    DICOM_LIST = f.readlines()
#To remove /n 
DICOM_LIST = [x.strip() for x in DICOM_LIST] 
##Sometimes image number and index are not the same
#To replace image index numebr with image number 
DICOM_LIST = [x[0:x.find(".dcm") + 4] for x in DICOM_LIST]

# To get first image as refenece image, supposed all images have same dimensions 
ReferenceImage = dc.read_file(DICOM_LIST[0])

# To get Dimensions
Dimension = (int(ReferenceImage.Rows), int(ReferenceImage.Columns), len(DICOM_LIST))

# To get 3D spacing
Spacing = (float(ReferenceImage.PixelSpacing[0]), float(ReferenceImage.PixelSpacing[1]), float(ReferenceImage.SliceThickness))

# To get image origin
Origin = ReferenceImage.ImagePositionPatient

# To make numpy array 
NpArrDc = np.zeros(Dimension, dtype=ReferenceImage.pixel_array.dtype)

# loop through all the DICOM files
for filename in DICOM_LIST:
    # To read the dicom file
    df = dc.read_file(filename)
    # store the raw image data
    NpArrDc[:, :, DICOM_LIST.index(filename)] = df.pixel_array  

NpArrDc = np.transpose(NpArrDc, (2, 0, 1))
sitk_img = sitk.GetImageFromArray(NpArrDc, isVector=False)
sitk_img.SetSpacing(Spacing)
sitk_img.SetOrigin(Origin)
sitk.WriteImage(sitk_img, os.path.join(Folder_Path, "sample" + ".mhd") )

