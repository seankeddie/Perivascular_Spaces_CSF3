#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:38:02 2026

@author: seankeddie
"""

import os 
import sys
import numpy as np
import nibabel as nib

# Read source and destination directories from command-line arguments
src, dst = sys.argv[1], sys.argv[2]

#Required multiple for the spatial dimensions
M = 16

for subj in sorted(os.listdir(src)):
    
    #Find the T1w image for this subject
    f = os.path.join(src, subj, "t1w.nii.gz")
    if not os.path.isfile(f):
        continue
    #Load the MRI
    img = nib.load(f)
    data = img.get_fdata(dtype=np.float32)
    
    #Calculate padding for each spatial dimension 
    pad = [(0, 8 + (-s) % 8) for s in data.shape[:3]]
    pad += [(0, 0)] * (data.ndim - 3)
    padded = np.pad(data, pad, mode = 'constant', constant_values = 0)
    out = os.path.join(dst, subj)
    os.makedirs(out, exist_ok=True)
    nib.save(nib.Nifti1Image(padded, img.affine), os.path.join(out, "t1w.nii.gz"))
    print(subj, data.shape, "->", padded.shape)
    