try:
 import geopandas as gpd
except ImportError as error:
  print(error.__class__.__name__ + ': Please import geopandas package')

try:
 import shapely
except ImportError as error:
  print(error.__class__.__name__ + ': Please import shapely package')
  
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt

name = 'Galapagos_Mapper'

