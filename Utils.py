#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:58:48 2019

@author: hamishgibbs
"""

#For use mapping relatively flat islands (changing the cutoff of a color map)
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
  from matplotlib.colors import LinearSegmentedColormap
  global LinearSegmentedColormap

  import numpy as np
  global np
    
  new_cmap = LinearSegmentedColormap.from_list(
      'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
      cmap(np.linspace(minval, maxval, n)))
  return new_cmap
