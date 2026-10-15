#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 17:02:21 2026

@author: seankeddie
"""

import glob
import os
import sys
import nibabel as nib

orig, padded = sys.argv[1], sys.argv[2]

for subj in sorted(os.listdir(padded)):
    ref_file = os.path.join(orig, subj, "t1w.nii.gz")
    if not os.path.isfile(ref_file):
        continue
    ref = nib.load(ref_file)
    nx, ny, nz = ref.shape[:3]
    for seg in glob.glob(os.path.join(padded, subj, "pvs_seg*.nii.gz")):
        img = nib.load(seg)
        data = img.get_fdata()[:nx, :ny, :nz]
        out = os.path.join(orig, subj, os.path.basename(seg))
        nib.save(nib.Nifti1Image(data.astype(img.get_data_dtype()), ref.affine), out)
        print("cropped", out, data.shape)