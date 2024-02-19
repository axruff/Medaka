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

# GLOBALS

all_landmarks = [set_vert, set_fins, set_digest, set_heart, set_eyes, set_skull_front, set_skull_center, set_skull_end, set_brain]
landmarks_pointset_names = [x['file_name'] for x in all_landmarks]


def get_landmark_index(all_land, pointset_name, landmark_name):
    for p in all_land:
        if p['file_name'] == pointset_name:
            return p['landmarks'].index(landmark_name)
    return -1


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
    
    
def center_crop_with_padding(im, x, y, crop_w=400, crop_h=200):
   
    res = np.zeros((crop_h, crop_w))

    x1 = 0 if x < int(crop_w / 2) else x-int(crop_w / 2)
    y1 = 0 if y < int(crop_h / 2) else y-int(crop_h / 2)

    offset_x = 0 if x > int(crop_w / 2) else int(crop_w / 2) -x
    offset_y = 0 if y > int(crop_h / 2) else int(crop_h / 2) -y

    x2 = im.shape[1] if x > im.shape[1] - int(crop_w / 2) else x+int(crop_w / 2)
    y2 = im.shape[0] if y > im.shape[0] - int(crop_h / 2) else y+int(crop_h / 2)

    im_cr = im[y1:y2,x1:x2]

    res[offset_y:offset_y+im_cr.shape[0],offset_x:offset_x+im_cr.shape[1]] = im_cr
   
    return res

def make_landmarks_comparison_figure_centered(im, file_name, land1, land2, landmark_name, name1, name2, color1 = 'red', color2 = 'blue'):

    marker_size = 5
    marker_alpha = 0.7
    line_width = 0.5

    x = math.floor(land1[0])
    y = math.floor(land1[1])
    z = math.floor(land1[2])

    x2 = math.floor(land2[0])
    y2 = math.floor(land2[1])
    z2 = math.floor(land2[2])
    
    zero_land1 = ' (ZERO)' if x == 0 and y == 0 and z == 0 else ''
    zero_land2 = ' (ZERO)' if x2 == 0 and y2 == 0 and z2 == 0 else ''
    
    diff = round(get_distance(land1, land2),1)

    fig = plt.figure(figsize= (14,6), layout="tight")

    gs = GridSpec(2, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[0, 1])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[0, 2])
    ax6 = fig.add_subplot(gs[1, 2])

    for i, ax in enumerate(fig.axes):
        ax.set_xticks([])
        ax.set_yticks([])  

    fig.suptitle(f"{landmark_name}    [{name1} and {name2}]    Diff = {diff} px", color='white')

    fig.patch.set_facecolor('black')

    #-------------------------
    # Front 1
    #-------------------------
    im_cr = center_crop_with_padding(im[z],x,y)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax5.imshow(im_cr, cmap='gray')
    # Markers
    ax5.plot(cx,cy,'ro', markersize=marker_size, alpha=marker_alpha)
    
    cx2,cy2 = cx +(x2-x),cy + (y2-y)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        #print('Fuck, out')
        ax5.plot(cx2,cy2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    #ax5.plot([0, im.shape[2]-1], [y, y], 'r', linestyle = 'dashed', linewidth=line_width)
    #ax5.plot([x, x], [0, im.shape[1]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax5.text(0.01, 0.95, name1 + zero_land1, horizontalalignment='left',
         verticalalignment='center', transform=ax5.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)

    #-------------------------
    # Front 2
    #-------------------------
    im_cr = center_crop_with_padding(im[z2],x2,y2)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax6.imshow(im_cr, cmap='gray')
    # Markers
    ax6.plot(cx,cy,'bo', markersize=marker_size, alpha=marker_alpha)
    
    cx2,cy2 = cx +(x-x2),cy + (y-y2)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        ax6.plot(cx2,cy2 ,'ro', markersize=marker_size, alpha=marker_alpha)

    # Lines
    #ax6.plot([0, im.shape[2]-1], [y2, y2], 'b', linestyle = 'dashed', linewidth=line_width)
    #ax6.plot([x2, x2], [0, im.shape[1]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax6.text(0.01, 0.95, name2+zero_land2, horizontalalignment='left',
         verticalalignment='center', transform=ax6.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color2, fontsize=12)
    #-------------------------
    # Top 1
    #-------------------------
    im_cr = center_crop_with_padding(im[:, y, :].T,z,x)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax1.imshow(im_cr, cmap='gray')
    ax1.plot(cx,cy,'ro', markersize=marker_size, alpha=marker_alpha)
    #ax1.plot(z2,x2,'bo', markersize=marker_size, alpha=marker_alpha) # Old
    cx2,cy2 = cx +(z2-z),cy + (x2-x)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        ax1.plot(cx2,cy2,'bo', markersize=marker_size, alpha=marker_alpha)
    
    # Lines
    #ax1.plot([0, im.shape[0]-1], [x, x], 'r', linestyle = 'dashed', linewidth=line_width)
    #ax1.plot([z, z], [0, im.shape[2]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax1.text(0.01, 0.95, name1+zero_land1, horizontalalignment='left',
         verticalalignment='center', transform=ax1.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)
    #-------------------------
    # Top 2
    #-------------------------
    im_cr = center_crop_with_padding(im[:, y2, :].T,z2,x2)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax2.imshow(im_cr, cmap='gray')
    cx2,cy2 = cx +(z-z2),cy + (x-x2)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        ax2.plot(cx2,cy2,'ro', markersize=marker_size, alpha=marker_alpha)
        
    ax2.plot(cx,cy,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    #ax2.plot([0, im.shape[0]-1], [x2, x2], 'b', linestyle = 'dashed', linewidth=line_width)
    #ax2.plot([z2, z2], [0, im.shape[2]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax2.text(0.01, 0.95, name2+zero_land2, horizontalalignment='left',
         verticalalignment='center', transform=ax2.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color2, fontsize=12)
    #-------------------------
    # Side 1
    #-------------------------
    im_cr = center_crop_with_padding(im[:, :, x].T,z,y)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax3.imshow(im_cr, cmap='gray')
    ax3.plot(cx,cy,'ro', markersize=marker_size, alpha=marker_alpha)
    cx2,cy2 = cx + (z2-z),cy + (y2-y)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        ax3.plot(cx2,cy2,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    #ax3.plot([0, im.shape[0]-1], [y, y], 'r', linestyle = 'dashed', linewidth=line_width)
    #ax3.plot([z, z], [0, im.shape[1]-1], 'r', linestyle = 'dashed', linewidth=line_width)

    ax3.text(0.01, 0.95, name1+zero_land1, horizontalalignment='left',
         verticalalignment='center', transform=ax3.transAxes, bbox=dict(facecolor='black', alpha=0.5), color=color1, fontsize=12)

    #-------------------------
    # Side 2
    #-------------------------
    im_cr = center_crop_with_padding(im[:, :, x2].T,z2,y2)
    cx,cy = int(im_cr.shape[1]/2), int(im_cr.shape[0]/2)
    ax4.imshow(im_cr, cmap='gray')
    cx2,cy2 = cx + (z-z2),cy+(y-y2)
    if not (cx2 > im_cr.shape[1] or cx2 < 0 or cy2 > im_cr.shape[0] or cy2 < 0):
        ax4.plot(cx2,cy2,'ro', markersize=marker_size, alpha=marker_alpha)
    ax4.plot(cx,cy,'bo', markersize=marker_size, alpha=marker_alpha)

    # Lines
    #ax4.plot([0, im.shape[0]-1], [y2, y2], 'b', linestyle = 'dashed', linewidth=line_width)
    #ax4.plot([z2, z2], [0, im.shape[1]-1], 'b', linestyle = 'dashed', linewidth=line_width)

    ax4.text(0.01, 0.95, name2+zero_land2, horizontalalignment='left',
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
    
    landmark_index = get_landmark_index(all_landmarks, pointset, landmark)

    make_landmarks_comparison_figure_centered(im, path_out / f'{str(pos).zfill(4)}_{sample}_{pointset}_{str(landmark_index).zfill(2)}_{landmark}_{name1}_{name2}', 
                                     [x,y,z], [x2,y2,z2], f'{pointset}: {landmark}', 
                                     participants_names[name1], participants_names[name2])
    
    
    
if __name__ == "__main__":
    
    path_eval = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/evaluation/")
    path_output = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/evaluation_vis/by_landmark_centered/")
    volumes_path = Path("/mnt/LSDF/tomo/ershov/medaka/workshop_landmarks/data/")
    
    #print(landmarks_pointset_names)
    
    # Top differences between 2 people
    TOP_COUNT = 200
    
    
    start = time.time()
    
    res_df = pd.read_excel(path_eval / 'results_landmarks.xlsx')
    
    for ps in landmarks_pointset_names:
    #for ps in ['pointset1_vert', 'pointset2_fins']:
    
        print('Processing pointset: ', ps)


        eval_df = pd.read_excel(path_eval / f'eval_{ps}.xlsx')
        
        landmarks_list = list(eval_df["landmark"].unique())
        
        for ld in landmarks_list:
            
            print(f'Processing landmark {ps}: {ld}')
            
            landmark_index = str(landmarks_list.index(ld)).zfill(2)
            
            ld_name = landmark_index + '_' +  ld
            
            path_out = path_output / ps / ld_name
            path_out.mkdir(parents=True, exist_ok=True)
            
            land_eval_df = eval_df[eval_df['landmark'] == ld]

            top_df = land_eval_df.sort_values(by='result', ascending=False).head(TOP_COUNT)
            top_df.to_excel(path_output / ps / f'{ld_name}.xlsx')
            #continue

            #print()
            #print(top_df)
            #print()

            proc_list = top_df.index.tolist()
            indexes = range(len(proc_list))

            #print(list(zip(indexes, proc_list)))

            pool = mp.Pool(30)
            res = pool.map(visualize_result, list(zip(indexes, proc_list)))

        
    elapsed = (time.time() - start) / 60  
    print(f'Finished. Total computation time: {elapsed} min')
