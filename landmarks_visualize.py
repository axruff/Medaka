from pathlib import Path
from xml.dom import minidom
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import SimpleITK as sitk

from tqdm import tqdm

import multiprocessing as mp

import os
import shutil
import filecmp

import time

from bs4 import BeautifulSoup

from landmarks_info import *



def get_landmark_coords_from_table(df, sample, pointset, landmark, name):
    df_query = res_df[(df['sample'] == sample)]
    df_query = df_query[df_query['point_set'] == pointset]
    df_query = df_query[df_query['landmark'] == landmark]
    df_query = df_query[df_query['name'] == name]

    x = df_query.iloc[0].x
    y = df_query.iloc[0].y
    z = df_query.iloc[0].z

    return x,y,z

def make_landmarks_comparison_figure(im, file_name, land1, land2, landmark_name, name1, name2, color1 = 'red', color2 = 'blue'):

    marker_size = 5
    marker_alpha = 0.7
    line_width = 0.5

    x = math.floor(land1[0])
    y = math.floor(land1[1])
    z = math.floor(land1[2])
    
    x2 = math.floor(land2[0])
    y2 = math.floor(land2[1])
    z2 = math.floor(land2[2])
    
    diff = round(get_distance(land1, land2),1)

    fig = plt.figure(figsize= (13,11), layout="tight")

    gs = GridSpec(4, 2, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[2,0])
    ax4 = fig.add_subplot(gs[3, 0])
    ax5 = fig.add_subplot(gs[0:2, 1])
    ax6 = fig.add_subplot(gs[2:4, 1])

    for i, ax in enumerate(fig.axes):
        ax.set_xticks([])
        ax.set_yticks([])  

    fig.suptitle(f"{landmark_name}    [{name1} and {name2}]    Diff = {diff} px", color='white')

    fig.patch.set_facecolor('black')

    #-------------------------
    # Front 1
    #-------------------------

    ax5.imshow(im[z], cmap='gray')
    # Markers
    ax5.plot(x,y,'ro', markersize=marker_size, alpha=marker_alpha)
    ax5.plot(x2,y2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax5.plot([0, im.shape[2]-1], [y, y], 'r', linestyle = 'dashed', linewidth=line_width)
    ax5.plot([x, x], [0, im.shape[1]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax5.text(0.05, 0.95, name1, horizontalalignment='center',
         verticalalignment='center', transform=ax5.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)

    #-------------------------
    # Front 2
    #-------------------------

    ax6.imshow(im[z2], cmap='gray')
    # Markers
    ax6.plot(x,y,'ro', markersize=marker_size, alpha=marker_alpha)
    ax6.plot(x2,y2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax6.plot([0, im.shape[2]-1], [y2, y2], 'b', linestyle = 'dashed', linewidth=line_width)
    ax6.plot([x2, x2], [0, im.shape[1]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax6.text(0.05, 0.95, name2, horizontalalignment='center',
         verticalalignment='center', transform=ax6.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color2, fontsize=12)
    #-------------------------
    # Top 1
    #-------------------------
    ax1.imshow(im[:, y, :].T, cmap='gray')
    ax1.plot(z,x,'ro', markersize=marker_size, alpha=marker_alpha)
    ax1.plot(z2,x2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax1.plot([0, im.shape[0]-1], [x, x], 'r', linestyle = 'dashed', linewidth=line_width)
    ax1.plot([z, z], [0, im.shape[2]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax1.text(0.05, 0.95, name1, horizontalalignment='center',
         verticalalignment='center', transform=ax1.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)
    #-------------------------
    # Top 2
    #-------------------------
    ax2.imshow(im[:, y2, :].T, cmap='gray')
    ax2.plot(z,x,'ro', markersize=marker_size, alpha=marker_alpha)
    ax2.plot(z2,x2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax2.plot([0, im.shape[0]-1], [x2, x2], 'b', linestyle = 'dashed', linewidth=line_width)
    ax2.plot([z2, z2], [0, im.shape[2]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax2.text(0.05, 0.95, name2, horizontalalignment='center',
         verticalalignment='center', transform=ax2.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color2, fontsize=12)
    #-------------------------
    # Side 1
    #-------------------------
    ax3.imshow(im[:, :, x].T, cmap='gray')
    ax3.plot(z,y,'ro', markersize=marker_size, alpha=marker_alpha)
    ax3.plot(z2,y2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax3.plot([0, im.shape[0]-1], [y, y], 'r', linestyle = 'dashed', linewidth=line_width)
    ax3.plot([z, z], [0, im.shape[1]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax3.text(0.05, 0.95, name1, horizontalalignment='center',
         verticalalignment='center', transform=ax3.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)

    #-------------------------
    # Side 2
    #-------------------------
    ax4.imshow(im[:, :, x2].T, cmap='gray')
    ax4.plot(z,y,'ro', markersize=marker_size, alpha=marker_alpha)
    ax4.plot(z2,y2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    ax4.plot([0, im.shape[0]-1], [y2, y2], 'b', linestyle = 'dashed', linewidth=line_width)
    ax4.plot([z2, z2], [0, im.shape[1]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax4.text(0.05, 0.95, name2, horizontalalignment='center',
         verticalalignment='center', transform=ax4.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color2, fontsize=12)


    #plt.show()

    plt.savefig(f'{file_name}.png')
    

def visualize_result(index):

    pos = index[0]
    i = index[1]
    
    sample = top_df.loc[i]['sample']
    pointset = top_df.loc[i]['point_set']
    name1 = top_df.loc[i]['name1']
    name2 = top_df.loc[i]['name2']
    landmark = top_df.loc[i]['landmark']

    # Depricated
    #fname1 = f"{sample}_{pointset}_{name1}.mps"
    #fname2 = f"{sample}_{pointset}_{name2}.mps"
    #print(f"{df_pointset.loc[i]['sample']}_{df_pointset.loc[i]['point_set']}_{df_pointset.loc[i]['name']}.mps")
    #land1 = read_landmarks(path_landmarks / fname1)
    #land2 = read_landmarks(path_landmarks / fname2)

    x,y,z = get_landmark_coords_from_table(res_df, sample, pointset, landmark, name1)
    #print([x,y,z])

    x2,y2,z2 = get_landmark_coords_from_table(res_df, sample, pointset, landmark, name2)
    #print([x,y,z])

    # Read sample

    #print(f'Processing: {sample}')
    sitk_image = sitk.ReadImage(volumes_path / f'{sample}.tif')
    im = sitk.GetArrayViewFromImage(sitk_image)
    #print('OK')

    make_landmarks_comparison_figure(im, path_out / f'{str(pos).zfill(4)}_{sample}_{pointset}_{landmark}_{name1}_{name2}', 
                                     [x,y,z], [x2,y2,z2], f'{pointset}: {landmark}', 
                                     participants_names[name1], participants_names[name2])
    
    
    
if __name__ == "__main__":
    
    path_eval = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/evaluation/")
    path_output = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/evaluation_vis/")
    volumes_path = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data/")
    
    all_landmarks = [set_vert, set_fins, set_digest, set_heart, set_eyes, set_skull_front, set_skull_center, set_skull_end, set_brain]

    landmarks_pointset_names = [x['file_name'] for x in all_landmarks]
    #print(landmarks_pointset_names)
    
    # Top differences between 2 people
    TOP_COUNT = 100
    
    
    start = time.time()
    
    res_df = pd.read_excel(path_eval / 'results_landmarks.xlsx')
    
    for ps in landmarks_pointset_names:
    #for ps in ['pointset1_vert', 'pointset2_fins']:
    
        print('Processing: ', ps)

        path_out = path_output / ps
        path_out.mkdir(parents=True, exist_ok=True)

        eval_df = pd.read_excel(path_eval / f'eval_{ps}.xlsx')
        
        top_df = eval_df.sort_values(by='result', ascending=False).head(TOP_COUNT)
        
        #print()
        #print(top_df)
        #print()
        
        proc_list = top_df.index.tolist()
        indexes = range(len(proc_list))
        
        #print(list(zip(indexes, proc_list)))
        
        pool = mp.Pool(20)
        res = pool.map(visualize_result, list(zip(indexes, proc_list)))

        if False:
            # for the selected results
            for i in top_df.index:
                sample = top_df.loc[i]['sample']
                pointset = top_df.loc[i]['point_set']
                name1 = top_df.loc[i]['name1']
                name2 = top_df.loc[i]['name2']
                landmark = top_df.loc[i]['landmark']

                # Depricated
                #fname1 = f"{sample}_{pointset}_{name1}.mps"
                #fname2 = f"{sample}_{pointset}_{name2}.mps"
                #print(f"{df_pointset.loc[i]['sample']}_{df_pointset.loc[i]['point_set']}_{df_pointset.loc[i]['name']}.mps")
                #land1 = read_landmarks(path_landmarks / fname1)
                #land2 = read_landmarks(path_landmarks / fname2)

                x,y,z = get_landmark_coords_from_table(res_df, sample, pointset, landmark, name1)
                #print([x,y,z])

                x2,y2,z2 = get_landmark_coords_from_table(res_df, sample, pointset, landmark, name2)
                #print([x,y,z])

                # Read sample

                #print(f'Processing: {sample}')
                sitk_image = sitk.ReadImage(volumes_path / f'{sample}.tif')
                im = sitk.GetArrayViewFromImage(sitk_image)
                #print('OK')

                make_landmarks_comparison_figure(im, path_out / f'{sample}_{pointset}_{landmark}_{name1}_{name2}', 
                                                 [x,y,z], [x2,y2,z2], f'{pointset}: {landmark}', 
                                                 participants_names[name1], participants_names[name2])


        #print(sample)
        
    elapsed = (time.time() - start) / 60  
    print(f'Finished. Total computation time: {elapsed} min')
