'''
Class for the map element
'''
class GalapagosMap:
  import matplotlib.pyplot as plt
  global plt 
  
  import numpy as np
  global np
  
  import pandas as pd
  global pd
  
  import geopandas as gpd
  global gpd

  import os
  global os

  from shapely.geometry import mapping
  global mapping

  import csv
  global csv
  
  from math import radians, degrees, sin, cos, asin, acos, sqrt
  global radians, degrees, sin, cos, asin, acos, sqrt
  
  def __init__(self):

   #Create bounding boxes when ititiating the class
    bbox = {}

    module_directory = os.path.dirname(os.path.abspath(__file__))
    csv_path = module_directory +  '/bounding_box_geometry.csv'

    with open(csv_path, 'r') as geometry_csv:
      csv_reader = csv.reader(geometry_csv, delimiter=',')
      next(csv_reader, None)
      for row in csv_reader:
        bbox[row[0]] = np.array([float(row[1]), float(row[2]), float(row[3]), float(row[4])]) 

    self.bounding_boxes = bbox
    self.volcano_names = list(bbox.keys())

  #Add x_lim_island and y_lim_island here (remove Bounding_Box Class)
  #Define a method to create matplotlib compatible xlim
  def x_lim_island(self, zoom_factor=0.15):
    
    #Define the factor by which to zoom out x axis (this could be made into two zooms L & R)
    #z_factor = 0.15 means that 15% of the total boundign box will be added to both sides
    #This scales with the size of the island to add a border to all plots
    z_factor = zoom_factor

            
    xmin = self.bounding_boxes[self.island_to_plot][0]
    xmax = self.bounding_boxes[self.island_to_plot][2]

    zoom = (xmax - xmin) * z_factor

    return(xmin - zoom, xmax + zoom)

  #Copy of x_lim_island for the y axis
  def y_lim_island(self, zoom_factor=0.15):

    z_factor = zoom_factor

    ymin = self.bounding_boxes[self.island_to_plot][1]
    ymax = self.bounding_boxes[self.island_to_plot][3]

    zoom = (ymax - ymin) * z_factor

    return(ymin - zoom, ymax + zoom)
  
  #Plot a basemap with the correct axes, north arrow and scale bar
  def base_map(self, island_to_plot='Archipelago', arrow_length_fraction=20, arrow_text_fraction=15, arrow_buffer_fraction=40, 
               scale_buffer_fraction=10, manual_scale_x=None, manual_scale_y=None):
    
    #CALCULATE BUFFERS
    self.island_to_plot = island_to_plot
    
    x_diff = self.x_lim_island()[1] - self.x_lim_island()[0]
    y_diff = self.y_lim_island()[1] - self.y_lim_island()[0]
    diff_ratio = y_diff/x_diff

    self.arrow_x_buffer = x_diff / arrow_buffer_fraction
    self.arrow_y_buffer = self.arrow_x_buffer * diff_ratio
    
    #Remember: manual_scale_x MUST be used with manual_scale_y
    if manual_scale_x != None:
      scale_x_buffer = manual_scale_x
    else:
      scale_x_buffer = x_diff / scale_buffer_fraction
    
    if manual_scale_y != None:
      scale_y_buffer = manual_scale_y
    else:
      scale_y_buffer = scale_x_buffer * diff_ratio

    
    #NORTH ARROW CALCULATIONS
    x_diff = self.x_lim_island()[1] - self.x_lim_island()[0]
    arrow_x = self.x_lim_island()[1] - self.arrow_x_buffer
    y_diff = self.y_lim_island()[1] - self.y_lim_island()[0]
    arrow_y = self.y_lim_island()[1] - self.arrow_y_buffer    
    
    #SCALE BAR CACULATIONS
    def great_circle(lon1, lat1, lon2, lat2):
      lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  
      return 6371 * (acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2)))
  
    def dirty_inverse(kilometer_value):
      return((1.0/111.0)*(float(kilometer_value)))
    
    def scale_bar_coordinates():
      
      #List of possible labels for the scale bar
      scale_bar_labels = [0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]

      #Determine the location of the bottom corners (L & R) of the map
      left_map_point = [self.x_lim_island()[0], self.y_lim_island()[0]]
      right_map_point = [self.x_lim_island()[1], self.y_lim_island()[0]]

      #Determine the width of the map in kilometers
      map_width_km = great_circle(left_map_point[0], left_map_point[1],
                                right_map_point[0], right_map_point[1])

      #Determine the right x coordinate of the scale bar
      scale_R_coord = self.x_lim_island()[1] - scale_x_buffer

      #Make the scale bar approximately 1/5th of image by default
      scale_bar_image_fraction = 0.2

      #Compute distance of 1/5 of image in kilometers
      scale_relative_length = map_width_km * scale_bar_image_fraction

      #Find the value in scale_bar_labels closest to this value (scale_relative_length)
      closest_scale_bar_label = min(scale_bar_labels, key=lambda x:abs(x-scale_relative_length))

      #Do an inverse great circle distance computation (rather crude) to convert closest_scale_bar_label from degrees to km
      degree_shift = dirty_inverse(closest_scale_bar_label)

      #use degree_shift to compute the left x coordinate of the scale bar
      scale_L_coord = scale_R_coord - degree_shift

      #Determine the y coordinate for both the R and L corners of the scale bar
      scale_y_coord = self.y_lim_island()[0] + scale_y_buffer

      '''
      Add white lines to scale bar at 0.1 to 0.4, and 0.6 to 0.8
      '''

      #Find the x coordinate of 6 points along the scale bar line
      sextiles = np.linspace(scale_L_coord, scale_R_coord, 6)

      #Define the x coordinates for the two white patches on the line
      white1_x_coords = (sextiles[1], sextiles[2])
      white2_x_coords = (sextiles[3], (sextiles[4]))

      '''
      Add text to the scale bar
      '''

      #Define the height of the text (half of the distance between the scale bar and the plot frame)
      text_y_coordinate = scale_y_coord - (scale_y_buffer/2)

      return(
          {'scale_L_coord' : scale_L_coord,
           'scale_R_coord' : scale_R_coord,
           'scale_y_coord' : scale_y_coord,
           'white1_x_coords' : white1_x_coords,
           'white2_x_coords' : white2_x_coords,
           'text_y_coordinate' : text_y_coordinate,
           'closest_scale_bar_label' : closest_scale_bar_label
          }
      )
    
    #x_diff = self.x_lim_island()[1] - self.x_lim_island()[0]
        
    #item_buffer = x_diff * 0.1
         
    #Plot the base figure
    self.fig, self.ax = plt.subplots()
    
    #Plot North Arrow
    self.ax.annotate('', xy=(arrow_x, arrow_y), 
                     xytext=(arrow_x, (arrow_y-(y_diff/arrow_length_fraction))), 
                     arrowprops=dict(arrowstyle='simple', fc='k'), 
                     clip_on=True
                    )

    self.ax.text(x=arrow_x, 
                 y=(arrow_y-(y_diff/arrow_text_fraction)), 
                 s='N', 
                 horizontalalignment='center'
                )
    
    #Plot scale bar
    sb_coordinates = scale_bar_coordinates()
    
    scale_L_coord = sb_coordinates['scale_L_coord']
    scale_R_coord = sb_coordinates['scale_R_coord']
    scale_y_coord = sb_coordinates['scale_y_coord']
    white1_x_coords = sb_coordinates['white1_x_coords']
    white2_x_coords = sb_coordinates['white2_x_coords']
    text_y_coordinate = sb_coordinates['text_y_coordinate']
    closest_scale_bar_label = sb_coordinates['closest_scale_bar_label']
        
    self.ax.plot((scale_L_coord, scale_R_coord), (scale_y_coord, scale_y_coord), color='k', linestyle='-', linewidth=4),
    self.ax.plot(white1_x_coords, (scale_y_coord, scale_y_coord), color='w', linestyle='-', linewidth=2.5),
    self.ax.plot(white2_x_coords, (scale_y_coord, scale_y_coord), color='w', linestyle='-', linewidth=2.5),
    self.ax.text(scale_L_coord, text_y_coordinate, '0', ha='center'),
    self.ax.text(scale_R_coord, text_y_coordinate, str(closest_scale_bar_label) + ' km', ha='left')

    #Trying to place using pixel coordinates
    bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height

    width *= self.fig.dpi
    height *= self.fig.dpi

    #Zoom into desired island
    self.ax.set_xlim(self.x_lim_island())
    self.ax.set_ylim(self.y_lim_island())
    
    #Remove axis labels and ticks
    #self.ax.axes.get_xaxis().set_ticklabels([])
    #self.ax.axes.get_yaxis().set_ticklabels([])
    
    #self.ax.axis('on')
    self.ax.xaxis.set_major_locator(plt.NullLocator())
    self.ax.yaxis.set_major_locator(plt.NullLocator())


  #Accepts a rasterio raster and matplotlib **kwargs for plt.imshow()
  def add_raster_data(self, raster_data, raster_band=1, **kwargs):
    plt.imshow(raster_data.read(raster_band), 
                   extent=(raster_data.bounds[0], raster_data.bounds[2], raster_data.bounds[1], raster_data.bounds[3]),
                   **kwargs)
  
  #Accepts point data in lat_lon coordinates
  def add_xy_data(self, x_data, y_data, **kwargs):
    plt.scatter(x_data, y_data, **kwargs)
      
  #Accepts geospatial dataframe data
  def add_vector_data(self, vector_data, **kwargs):
    vector_data.geometry.plot(ax=self.ax, **kwargs)
  
  #Add an ocean color from a matplotlib compatible color string
  def add_ocean_color(self, color):
    self.ax.set_facecolor(color)
  
  #Add attribution text to the bottom left corner of the plot
  def add_attribution_text(self, attribution_text, **kwargs):
    
    self.ax.text(x=self.x_lim_island()[0] + self.arrow_x_buffer,
        y=self.y_lim_island()[0] + self.arrow_y_buffer,
        s=attribution_text, **kwargs)
  
  def add_grid(self, **kwargs):
    self.ax.grid(True, **kwargs)
