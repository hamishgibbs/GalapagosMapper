try:
 import geopandas as gpd
except ImportError:
  !pip install geopandas

try:
 import shapely
except ImportError:
  !pip install shapely
  
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import mapping, shape
import numpy as np
from math import radians, degrees, sin, cos, asin, acos, sqrt

name = 'Galapagos_Mapper'

