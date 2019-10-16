try:
 import geopandas as gpd
except ImportError:
  print(error.__class__.__name__ + ': ' + error.message)

try:
 import shapely
except ImportError:
    print(error.__class__.__name__ + ': ' + error.message)
  
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import mapping, shape
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt

name = 'Galapagos_Mapper'

