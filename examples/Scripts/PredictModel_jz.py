import os
import glob
import sys
import numpy as np
from tqdm import tqdm
from tifffile import imread, imwrite
from vollseg import StarDist2D, UNET, VollSeg, MASKUNET, CARE
from pathlib import Path


image_dir = '/gpfsstore/rech/jsy/uzj81mi/Segmentation_Datasets/Drosophila_Segmentation/TimeLapse/'
model_dir = '/gpfsstore/rech/jsy/uzj81mi/Segmentation_Models/'
save_dir = image_dir + 'varun_skeletor/'

noise_model_name = 'CARE/denoising_generic_3D/' 
unet_model_name = 'Unet2D/Drosophila/'
star_model_name = 'StarDist2D/Drosophila/'
roi_model_name = None

if unet_model_name is not None:
  unet_model = UNET(config = None, name = unet_model_name, basedir = model_dir)
else:
    unet_model = None
if star_model_name is not None:
  star_model = StarDist2D(config = None, name = star_model_name, basedir = model_dir)
else:
    star_model = None
if noise_model_name is not None:
  noise_model = CARE(config=None, name= noise_model_name, basedir = model_dir)
else:
    noise_model = None
if roi_model_name is not None:
  roi_model = MASKUNET(config = None, name = roi_model_name, basedir = model_dir)
else:
    roi_model = None


Raw_path = os.path.join(image_dir, '*.tif')
filesRaw = glob.glob(Raw_path)
filesRaw.sort
#Minimum size in pixels for the cells to be segmented
min_size = 1
#Minimum size in pixels for the mask region, regions below this threshold would be removed
min_size_mask=10
#maximum size of the region, set this to veto regions above a certain size
max_size = 1000000
#Adjust the number of tiles depending on how good your GPU is, tiling ensures that your image tiles fit into the runtime
#memory 
n_tiles = (1,1,1)
#If your Unet model is weak we will use the denoising model to obtain the semantic segmentation map, set this to False if this
#is the case else set tit o TRUE if you are using Unet to obtain the semantic segmentation map.
dounet = True
#If you want to do seedpooling from unet and stardist set this to true else it will only take stardist seeds
seedpool = True
#Wether unet create labelling in 3D or slice by slice can be set by this parameter, if true it will merge neighbouring slices
slice_merge = False
#Use probability map for stardist to perform watershedding or use distance map
UseProbability = True
donormalize=True
lower_perc= 1
upper_perc=99.8
#For 2D images we have the option of segmenting RGB->Greyscale, if so set this to true else let it be False
RGB = False
#Set up the axes keyword depending on the type of image you have, if it is a time lapse movie of XYZ images 
#your axes would be TZYX, if it is a timelapse of 2D images the axes would be TYX, for a directory of XYZ images
#the axes is ZYX and for a directory of XY images the axes is YX
axes = 'TYX'
for fname in filesRaw:
     
     image = imread(fname)
     Name = os.path.basename(os.path.splitext(fname)[0])
     VollSeg( image, 
             unet_model = unet_model, 
             star_model = star_model, 
             roi_model= None,
             noise_model = noise_model, 
             seedpool = seedpool, 
             axes = axes, 
             min_size = min_size,  
             min_size_mask = min_size_mask,
             max_size = max_size,
             donormalize=donormalize,
             lower_perc= lower_perc,
             upper_perc=upper_perc,
             n_tiles = n_tiles, 
             slice_merge = slice_merge, 
             UseProbability = UseProbability, 
             save_dir = save_dir, 
             Name = Name, 
             dounet = dounet,
             RGB = RGB)    
