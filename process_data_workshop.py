import multiprocessing as mp

from scipy.spatial.transform import Rotation as R
import numpy as np
import math
import matplotlib.pyplot as plt 

import time
import os

import cv2
from PIL import Image

import SimpleITK as sitk
from torchio.transforms import Affine
from torchio import Image

from pathlib import Path

from bs4 import BeautifulSoup
import json

import pandas as pd

def read_crop_info(file_name):
    
    with open(file_name, "r") as fp:
        crop_info = json.load(fp)
        
    return crop_info

def read_rotation_info(file_name):
    
    with open(file_name, "r") as fp:
        rot = json.load(fp)
        
        
        #rotation_info = {'x_dir': {'x': x_dir.getX(), 'y': x_dir.getY(), 'z': z_dir.getZ()},
        #             'y_dir': {'x': y_dir.getX(), 'y': y_dir.getY(), 'z': y_dir.getZ()},
        #             'z_dir': {'x': z_dir.getX(), 'y': z_dir.getY(), 'z': z_dir.getZ()}
        #            }
        
    x = [rot['x_dir']['x'], rot['x_dir']['y'], rot['x_dir']['z']]
    y = [rot['y_dir']['x'], rot['y_dir']['y'], rot['y_dir']['z']]
    z = [rot['z_dir']['x'], rot['z_dir']['y'], rot['z_dir']['z']]
    
  
    return x,y,z
    

def read_dragonfly_transform(file_name):
    
    with open(str(file_name), 'r') as f:
        data = f.read()

#print(data[12:])

    xml_data = BeautifulSoup(data[12:], "xml")

    #print(xml_data)

    x_dir = xml_data.find('direction0')
    y_dir = xml_data.find('direction1')
    z_dir = xml_data.find('direction2')

    x2 = [float(x_dir.get('x')), float(x_dir.get('y')), float(x_dir.get('z'))]
    y2 = [float(y_dir.get('x')), float(y_dir.get('y')), float(y_dir.get('z'))]
    z2 = [float(z_dir.get('x')), float(z_dir.get('y')), float(z_dir.get('z'))]
    
    f.close()
    
    return x2,y2,z2

def read_mitk_landmarks(file_name, scale=1.0, mode='def'):
   
    if mode == 'lowercase':
        file_name = file_name.lower()
   
    with open(str(file_name) + '.mps', 'r') as f:
        data = f.read()
   
    xml_data = BeautifulSoup(data, "xml")
    points = xml_data.find_all('point')
   
    landmarks = []

    for p in points:
        if p.find('x').text == '0' and p.find('y').text == '0' and p.find('z').text == '0':
            continue

        x = float(p.find('x').text)*scale
        y = float(p.find('y').text)*scale
        z = float(p.find('z').text)*scale

        landmarks.append(np.asarray([x,y,z]))
       
    f.close()
       
    return landmarks

def save_np_as_multitiff_stack(volume, file_name):
    
    imlist = []
    for i in range(volume.shape[0]):
        imlist.append(Image.fromarray(volume[i]))

    imlist[0].save(file_name, save_all=True, append_images=imlist[1:])
    
    del imlist 
    
def vec_length(v):
    return np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def create_two_vector_sets(landmarks):
    
    tip = landmarks[0]
    up = landmarks[1]
    down = landmarks[2]
    left = landmarks[3]
    right = landmarks[4]
    end = landmarks[5]

    center = np.floor((up + down) / 2.0)

    vec_tip = tip - center
    vec_up = up - center
    vec_down = down - center
    vec_left = left - center
    vec_right = right - center 
    vec_end = end - center

    land_vectors = [vec_tip.tolist(), vec_up.tolist(), vec_down.tolist(), vec_left.tolist(), vec_right.tolist(), vec_end.tolist()]

    vec_tip0 = [0,0,vec_length(vec_tip)]
    vec_up0 = [0,-vec_length(vec_up),0]
    vec_down0 = [0,vec_length(vec_down),0]
    vec_left0 = [vec_length(vec_left),0,0]
    vec_right0 = [-vec_length(vec_right),0,0]
    vec_end0 = [0,0,-vec_length(vec_end)]

    norm_vectors = [vec_tip0, vec_up0, vec_down0, vec_left0, vec_right0, vec_end0]
    
    return norm_vectors, land_vectors

def get_center(landmarks):
    
    up = landmarks[1]
    down = landmarks[2]
    center = np.floor((up + down) / 2.0)
    
    return center

def distance(v1, v2):
    return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2) 
    
    
def process_dataset(d):
    
    start = time.time()
    
    dataset = d
    
    ind = int(dataset.split('_')[1])
    
    
    f = open(path_datasets_list / 'datasets_201905.txt', 'r')
    datasets_201905 = f.readlines()
    f.close()
    
    f = open(path_datasets_list / 'datasets_201912.txt', 'r')
    datasets_201912 = f.readlines()
    f.close()
    
    f = open(path_datasets_list / 'datasets_202012.txt', 'r')
    datasets_202012 = f.readlines()
    f.close()
    
    if ind in [int(x.split('_')[1]) for x in datasets_201905]:
        data_path = "201905_beamtime_medaka_stained"
        
    if ind in [int(x.split('_')[1]) for x in datasets_201912]:
        data_path = "201912_beamtime_medaka"
        
    if ind in [int(x.split('_')[1]) for x in datasets_202012]:
        data_path = "202012_beamtime_medaka"
        
    
    # OLD: Depricated
    #if ind>=800 and ind<=979:
    #    data_path = "201905_beamtime_medaka_stained"

    #elif ind>=1064 and ind<=1297:
    #    data_path = "201912_beamtime_medaka";
    
    #data_path = "201912_beamtime_medaka"
    
    
    path = Path("/mnt/HD-LSDF/Medaka/" + data_path + "/" + dataset +"/scaled_0.5_8bit_slices.tif")
    
    # Read data
    print(f'Reading image: {dataset}')
    sitk_image = sitk.ReadImage(path)

    image_data = sitk.GetArrayFromImage(sitk_image).astype('uint8')
    #print('Image shape', image_data.shape)

    d = image_data.shape[0]
    h = image_data.shape[1]
    w = image_data.shape[2]
    
    # Get landmarks info
    land = read_mitk_landmarks(path_landmarks / str(ind), scale=2.0)

    c = get_center(land)
    #print('Center (x,y,z):', c)
    #print('Data size (x,y,z):', w,h,d)
    #print('Data center (x,y,z):', w/2,h/2,d/2)

    vec_norm, vec_land = create_two_vector_sets(land)
    
    res_rot = R.align_vectors(vec_land, vec_norm)

    # Find rotations
    rotation_degrees = res_rot[0].as_euler('zyx', degrees=True)
    print('Calculated rotations:', rotation_degrees)
    degrees = rotation_degrees

    img_translation = Affine(scales=[1.0, 1.0, 1.0], degrees=[0,0,0], translation=[d/2-c[2],h/2-c[1],w/2-c[0]], center='image')
    img_rotation = Affine(scales=[1.0, 1.0, 1.0], degrees=degrees, translation=[0,0,0], center='image')

    print('Transforming...')
    
    #image_rotated = image_data # TEMP
    image_trans = img_translation(np.expand_dims(image_data, axis=0))
    image_rotated = img_rotation(image_trans)[0]
    print('OK')
    
    # Crop
    nose_tip_offset = 50

    up = land[1]
    down = land[2]
    ud_dist = distance(up, down)

    left = land[3]
    right = land[4]
    lr_dist = distance(left, right)

    #image_crop = image_rotated # TEMP
    #image_crop = image_rotated[:int(d-(c[2] - d/2))+nose_tip_offset,:,:]
    image_crop = image_rotated[:int(d-(c[2] - d/2))+nose_tip_offset,
                               int(h/2 - ud_dist):int(h/2 + ud_dist),
                               int(w/2 - lr_dist):int(w/2 + lr_dist)]
    
    #Flip z axis: Start from head
    image_crop = np.flip(image_crop, 0)
    
    
    # Save preview
    #tip = land[0]
    #tip_d = distance(tip, c)
#
    #fig = plt.figure()
    #fig.set_size_inches(12, 12, forward=True)
#
    #plt.imshow(image_rotated[int(d/2 + tip_d/2)], cmap='gray')
    #plt.title(dataset)
    #plt.axis('off')
    #fig.savefig(path_output / f'{dataset}.png')
    #
    
    fig, axs = plt.subplots(3)
    fig.set_size_inches(15, 15, forward=True)

    #plt.imshow(image_rotated[int(d/2 + tip_d/2)], cmap='gray')
    axs[0].imshow(image_crop[int(image_crop.shape[0]/2)], cmap='gray')
    axs[0].set_title(dataset)

    axs[1].imshow(np.fliplr(image_crop[:,:,int(image_crop.shape[2]/2)].T), cmap='gray')
    axs[2].imshow(np.fliplr(image_crop[:,int(image_crop.shape[1]/2),:].T), cmap='gray')

    fig.savefig(path_preview / f'{ind}.png')
    
    sitk_image = sitk.GetImageFromArray(image_crop.astype('uint8'))
    sitk.WriteImage(sitk_image, path_output / f'{ind}.tif')
    
    end = time.time()
    
    elapsed = (end - start) / 60
    
    print(f'Elapsed: {elapsed} min')
    
    #print('')
    
    #fig = plt.figure()
    #plt.imshow(sitk.GetArrayViewFromImage(sitk_image)[500], cmap= 'gray')
    #plt.axis('off');
    #print('OK')
    #fig.savefig(path_output / f'{dataset}_test.png')

path_datasets_list = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/")
path_landmarks = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/landmarks_mitk/")
path_output = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data/")
path_preview = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/preview/")
    
def main(): 
    
    start = time.time()

    
    print('Hi')
    
    # Manual
    #dataset_list = ['Medaka_1064_4-1', 'Medaka_1071_8-2', 'Medaka_1075_13-2']
    
    #df = pd.read_excel(open(path_datasets_list / 'evaluation_segmentation.xlsx', 'rb'), sheet_name='selected')
    #df['dataset'].tolist()
    
    # Make dataset list to process
    f = open(path_datasets_list / 'selected_datasets.txt', 'r')
    lines = f.readlines()
    print('Selected fish:', lines)
    f.close()
    
    aligned_datasets = [x.split('.')[0] for x in os.listdir(path_landmarks) if '.mps' in x]
    processed_datasets = [x.split('.')[0] for x in os.listdir(path_output) if '.tif' in x]
    
    print('Aligned', aligned_datasets)
    
    dataset_list = [x.strip() for x in lines if (x.split('_')[1] in aligned_datasets) and (x.split('_')[1] not in processed_datasets) ]
    
    print('Datasets to process:', dataset_list)
    
    
   
                             
    pool = mp.Pool(10)
    res = pool.map(process_dataset, dataset_list)
    
    elapsed = (time.time() - start) / 60
    
    print(f'Finished. Total computation time: {elapsed} min')
    
if __name__ == "__main__":
    main()