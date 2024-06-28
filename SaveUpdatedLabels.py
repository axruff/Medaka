
from OrsHelpers.viewLogger import ViewLogger
from OrsPlugins.orsimageloader import OrsImageLoader
from OrsHelpers.managedhelper import ManagedHelper
from OrsHelpers.datasethelper import DatasetHelper
from OrsHelpers.layoutpropertieshelper import LayoutPropertiesHelper
from OrsPythonPlugins.OrsObjectPropertiesList.OrsObjectPropertiesList import OrsObjectPropertiesList
from OrsPythonPlugins.OrsDerivedDataset.OrsDerivedDataset import OrsDerivedDataset
from OrsPythonPlugins.OrsDatasetProperties.OrsDatasetProperties import OrsDatasetProperties
from OrsHelpers.roihelper import ROIHelper
from OrsHelpers.structuredGridLogger import StructuredGridLogger
from OrsHelpers.structuredGridHelper import StructuredGridHelper
from OrsHelpers.reporthelper import ReportHelper
from OrsHelpers.displayROI import DisplayROI
#from ORSServiceClass.OrsPlugin.abstractContext import AbstractContext
from OrsLibraries.workingcontext import WorkingContext
from ORSModel.ors import Color
from PIL import Image
import math
import json
import numpy as np

from OrsHelpers.multiroilabelhelper import MultiROILabelHelper
from OrsHelpers.datasethelper import DatasetHelper


PATH_INPUT_FOLDER        = "d:\\data\\medaka\\segmentations_corrections\\"
PATH_OUTPUT_INFO_FOLDER  = "d:\\data\\medaka\\segmentations_corrections\\"

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

def copy_transform(vol, label):

    b = vol.getBox()
        
    x_dir = b.getDirection0()
    y_dir = b.getDirection1()
    z_dir = b.getDirection2()

    x_pos = b.getOrigin().getX()
    y_pos = b.getOrigin().getY()
    z_pos = b.getOrigin().getZ()

    OrsDatasetProperties.changeAdvancedStructuredGridProperties(structuredGrid=label,
                                                            xPosition=x_pos,
                                                            yPosition=y_pos,
                                                            zPosition=z_pos,
                                                            orientationAxis1X=x_dir.getX(),
                                                            orientationAxis1Y=x_dir.getY(),
                                                            orientationAxis1Z=x_dir.getZ(),
                                                            orientationAxis2X=y_dir.getX(),
                                                            orientationAxis2Y=y_dir.getY(),
                                                            orientationAxis2Z=y_dir.getZ(),
                                                            orientationAxis3X=z_dir.getX(),
                                                            orientationAxis3Y=z_dir.getY(),
                                                            orientationAxis3Z=z_dir.getZ())

    StructuredGridLogger.resetVisualBoxOfChannelFromLayoutGenealogicalName(aName='', channel=label)
    label.publish(logging=True)

def save_rotation_info(im, file_name):
    b = im.getBox()
    
    x_dir = b.getDirection0()
    y_dir = b.getDirection1()
    z_dir = b.getDirection2()
    
    rotation_info = {'x_dir': {'x': x_dir.getX(), 'y': x_dir.getY(), 'z': x_dir.getZ()},
                     'y_dir': {'x': y_dir.getX(), 'y': y_dir.getY(), 'z': y_dir.getZ()},
                     'z_dir': {'x': z_dir.getX(), 'y': z_dir.getY(), 'z': z_dir.getZ()}
                    }
    
    with open(PATH_OUTPUT_INFO_FOLDER + file_name + '_rot_info.txt', "w") as fp:
        json.dump(rotation_info, fp)  # encode dict into JSON 
        
    print(f'Dataset: {file_name}: Rotation info is saved')



def set_lut_for_labels(multi_roi):
    multi_roi.setLabelColor(1, Color(float(255/255),float(255/255),float(0/255)))
    multi_roi.setLabelColor(2, Color(float(0/255),float(174/255),float(255/255)))
    multi_roi.setLabelColor(3, Color(float(127/255),float(42/255),float(0/255)))
    multi_roi.setLabelColor(4, Color(float(255/255),float(0/255),float(255/255)))
    multi_roi.setLabelColor(5, Color(float(170/255),float(170/255),float(0/255)))
    multi_roi.setLabelColor(6, Color(float(20/255),float(122/255),float(255/255)))
    multi_roi.setLabelColor(7, Color(float(85/255),float(255/255),float(255/255)))
    multi_roi.setLabelColor(8, Color(float(0/255),float(255/255),float(0/255)))
    multi_roi.setLabelColor(9, Color(float(0/255),float(170/255),float(0/255)))

    multi_roi.setLabelName(1, 'optic nerves')
    multi_roi.setLabelName(2, 'optic tectum')
    multi_roi.setLabelName(3, 'forebrain')
    multi_roi.setLabelName(4, 'midbrain')
    multi_roi.setLabelName(5, 'hindbrain')
    multi_roi.setLabelName(6, 'cerebellum')
    multi_roi.setLabelName(7, 'epiphysis')
    multi_roi.setLabelName(8, 'hypophysis')
    multi_roi.setLabelName(9, 'torus')

##-------------------------------------------------
## Testing
##-------------------------------------------------

##-------------------------------------------------
## 1 Load volume
##-------------------------------------------------
i = 459
vol = load_volume(f'{i}_vol.tif')

##-------------------------------------------------
## 2 Manually align, Load labels, Apply transform, Save transfrom
##-------------------------------------------------

label = load_volume(f'{i}_brain.tif')
copy_transform(vol, label)
multi_roi = DatasetHelper.createMultiROIFromDataset(dataset=label, multiROI=None, IProgress=None)
set_lut_for_labels(multi_roi)
multi_roi.publish(logging=True)
save_rotation_info(vol, f'{i}')
WorkingContext.setCurrentGlobalState(None, 'OrsStateTrack')

##-------------------------------------------------
## 3 Manually correct, Save labels
##-------------------------------------------------

dataset = DatasetHelper.createDatasetFromMultiROI(aMultiROI=multi_roi, IProgress=None)
dataset.publish(logging=True)
array = dataset.getNDArray()
save_3d_array_as_tiff(array, PATH_INPUT_FOLDER + f'{i}_brain_corr.tif')
clean_all()

