try:
 import geopandas as gpd
except ImportError as error:
  print(error.__class__.__name__ + ': Missing package geopandas')

try:
 import shapely
except ImportError as error:
  print(error.__class__.__name__ + ': Missing package shapely')
  
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import mapping, shape
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt

name = 'Galapagos_Mapper'

