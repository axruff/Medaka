
from OrsHelpers.viewLogger import ViewLogger
from OrsPlugins.orsimageloader import OrsImageLoader
from OrsHelpers.managedhelper import ManagedHelper
from OrsHelpers.datasethelper import DatasetHelper
from OrsHelpers.layoutpropertieshelper import LayoutPropertiesHelper
from OrsPythonPlugins.OrsObjectPropertiesList.OrsObjectPropertiesList import OrsObjectPropertiesList
from OrsPythonPlugins.OrsDerivedDataset.OrsDerivedDataset import OrsDerivedDataset
from OrsHelpers.roihelper import ROIHelper
from OrsHelpers.structuredGridLogger import StructuredGridLogger
from OrsHelpers.structuredGridHelper import StructuredGridHelper
from OrsHelpers.reporthelper import ReportHelper
from OrsHelpers.displayROI import DisplayROI
from PIL import Image
import math
import json
import numpy as np

from OrsHelpers.multiroilabelhelper import MultiROILabelHelper
from OrsHelpers.datasethelper import DatasetHelper


PATH_INPUT_FOLDER        = "d:\\data\\medaka\\data\\"

SPACING = 0.001 # Pixel size in micrometers
ROI_COUNT = 9



def load_volume(volume_file_name = 'fA2p0_17_2_s_eig16_new_sagittal.tif'):
    
    print('Loading: ', volume_file_name)

    fileNamesListElement = PATH_INPUT_FOLDER + volume_file_name
    fileNames = [fileNamesListElement]

    vol_size = get_volume_size(PATH_INPUT_FOLDER + volume_file_name)

    #xSize = 1048
    #ySize = 1140
    #zSize = 1116

    xSize = vol_size[0]
    ySize = vol_size[1]
    zSize = vol_size[2]
    tSize = 1
    minX = 0
    maxX = xSize -1
    minY = 0
    maxY = ySize -1
    minZ = 0
    maxZ = zSize -1
    xSampling = 1
    ySampling = 1
    zSampling = 1
    tSampling = 1
    xSpacing = SPACING
    ySpacing = SPACING
    zSpacing = SPACING
    slope = 1.0
    offset = 0.0
    dataUnit = ''
    invertX = False
    invertY = False
    invertZ = False
    axesTransformation = 0
    datasetName = volume_file_name
    convertFrom32To16bits = False
    dataRangeMin = 0.0
    dataRangeMax = 0.0
    frameCount = 1

    additionalInfo = 'PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxJbWFnZUxvYWRlck1vZGVsIElzRGF0YVJHQj0iZmFsc2UiIFJHQk91dHB1dD0iMCIgSW52ZXJ0SW50ZW5zaXR5PSJmYWxzZSIgLz4K'


    output = OrsImageLoader.createDatasetFromFiles(fileNames=fileNames,
                                                xSize=xSize,
                                                ySize=ySize,
                                                zSize=zSize,
                                                tSize=tSize,
                                                minX=minX,
                                                maxX=maxX,
                                                minY=minY,
                                                maxY=maxY,
                                                minZ=minZ,
                                                maxZ=maxZ,
                                                xSampling=xSampling,
                                                ySampling=ySampling,
                                                zSampling=zSampling,
                                                tSampling=tSampling,
                                                xSpacing=xSpacing,
                                                ySpacing=ySpacing,
                                                zSpacing=zSpacing,
                                                slope=slope,
                                                offset=offset,
                                                dataUnit=dataUnit,
                                                invertX=invertX,
                                                invertY=invertY,
                                                invertZ=invertZ,
                                                axesTransformation=axesTransformation,
                                                datasetName=datasetName,
                                                convertFrom32To16bits=convertFrom32To16bits,
                                                dataRangeMin=dataRangeMin,
                                                dataRangeMax=dataRangeMax,
                                                frameCount=frameCount,
                                                additionalInfo=additionalInfo)

    volume_channel = output[0]
    ManagedHelper.publish(anObject=volume_channel)

    name = 'toplayout\\scene_0'
    isVisible = True
    
    DatasetHelper.setIsVisibleIn2DFromGenealogicalName(name=name,
                                                    dataset=volume_channel,
                                                    isVisible=isVisible)

  

    layoutFullName = 'toplayout\\scene_0'
    lutUUID = '7b00da82eefc11e68693448a5b87686a'
    aScalarValueTypeTag = ''
 
    LayoutPropertiesHelper.set3DLUTUUIDFromGenealogicalName(layoutFullName=layoutFullName,
                                                            anObject=volume_channel,
                                                            lutUUID=lutUUID,
                                                            aScalarValueTypeTag=aScalarValueTypeTag)


    return volume_channel



def get_volume_size(volume_path):

    im = Image.open(volume_path)
    return (im.size[0], im.size[1], im.n_frames)

def save_3d_array_as_tiff(array, output_path):
    """
    Save a 3D NumPy array as a multi-page TIFF file.

    Parameters:
    - array: 3D NumPy array (depth, height, width).
    - output_path: The output path for the multi-page TIFF file.
    """
    if array.ndim != 3:
        raise ValueError("The input array must be 3D")

    # Convert each 2D slice to a PIL Image
    images = [Image.fromarray(array[i]) for i in range(array.shape[0])]

    # Save as multi-page TIFF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        compression="tiff_deflate"
    )



def clean_all():
    global vol
    global label
    global multi_roi
    global dataset
    
    if vol != None:
        DatasetHelper.deleteDataset(aDataset=vol)
    if label != None:
        DatasetHelper.deleteDataset(aDataset=label)
    if multi_roi != None:    
        #DatasetHelper.deleteDataset(aDataset=multi_roi)
        DisplayROI.deleteMultiROI(aMultiROI=multi_roi)
    if dataset != None:    
        DatasetHelper.deleteDataset(aDataset=dataset)
        
    vol = None
    label = None
    multi_roi = None
    dataset = None 


##-------------------------------------------------
## Testing
##-------------------------------------------------

vol = load_volume('1099.tif')
label = load_volume('1099_brain.tif')

multi_roi = DatasetHelper.createMultiROIFromDataset(dataset=label, multiROI=None, IProgress=None)
multi_roi.publish(logging=True)



# def extract_all_roi_and_save(multi_roi, file_name):
#     return



# def extract_roi(multi_roi, label_index):
#     roi = MultiROILabelHelper.extractROIForLabel(multiroi=multi_roi, label=label_index)
#     roi.publish(logging=True)
#     return roi

# roi = extract_roi(multi_roi, 5)


dataset = DatasetHelper.createDatasetFromMultiROI(aMultiROI=multi_roi, IProgress=None)
dataset.publish(logging=True)

array = dataset.getNDArray()
save_3d_array_as_tiff(array, PATH_INPUT_FOLDER + '1099_labels.tif')




