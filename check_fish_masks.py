from pathlib import Path
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import SimpleITK as sitk
import os
import time

import multiprocessing as mp


def make_mask_figure(im, mask, file_name):
    
    d = im.shape[0]
    w = im.shape[2]
    h = im.shape[1]

    fig = plt.figure(figsize= (14,9), layout="tight")

    gs = GridSpec(2, 1, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])


    ax1.imshow(im[:,:,int(w/2)].T, cmap='gray')
    ax1.imshow(mask[:,:,int(w/2)].T, alpha=0.5)

    ax2.imshow(im[:,int(h/2),:].T, cmap='gray')
    ax2.imshow(mask[:,int(h/2),:].T, alpha=0.5)

    for i, ax in enumerate(fig.axes):
            ax.set_xticks([])
            ax.set_yticks([])  
            
    fig.suptitle(f"{file_name}")
    
    plt.savefig(path_preview / f'{file_name}_mask_preview.png')
    
    
def process_dataset(d):
    
    sample = d
    
    print('Reading:', sample)

    sitk_image = sitk.ReadImage(path_data / f'{sample}.tif')
    im = sitk.GetArrayViewFromImage(sitk_image)

    sitk_mask= sitk.ReadImage(path_masks / f'{sample}.tif')
    mask= sitk.GetArrayViewFromImage(sitk_mask)
    
    make_mask_figure(im,mask, sample)
    
    print('Done:', sample)
    
    
path_data = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data")
path_masks = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data_masks")
path_preview = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data_masks_preview")

    
if __name__ == "__main__":
    start = time.time()

    print('Hi')
    
    files = os.listdir(str(path_masks))
    #datasets = [f.split('.')[0] for f in files]
    
    datasets= ["1170","1181","1185","1191","1192","1197","1216","1217","1222","1226","1227","1230","1232","1234","1248","1256","1257","1258","1264","1265","1269","1273","1274","1282","1284","1285","1291","1292","1293","1296","1297","1300","1305","1310","1320","1321","1323","1337","1338","1341","1346","1351","1353","1362","1363","1369","1370","1372","1376","1378","1380","1383","1384","1385","1389","1393","1394","1395","1396","1399","1400","1401","1404","1405","1406","1412","1413","1414","1417","1418","1423"]
    
    print('Datasets to process:', datasets)
    
    
    pool = mp.Pool(20)
    res = pool.map(process_dataset, datasets)
    
    elapsed = (time.time() - start) / 60
    
    print(f'Finished. Total computation time: {elapsed} min')
    
    
    
    