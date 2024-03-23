# %%
import math
import os
import json
import geopandas as gp
import pandas as pd
import requests

# %%
gdf = gp.read_file(
    "Marine_NSWCoastalLidarCoverage_20190827/NSW_CoastalLiDAR_Coverage_20190827.shp"
)
gdf
# %%
gdf.plot()

# %%
for x in gdf.iloc[0]:
    print(x)

# %%
os.listdir("Marine_NSWCoastalLidarCoverage_20190827")

# %%
# Center coordinates
lat, lon = -33.9149, 151.2612

# Distance in degrees
km_dist = 10
d = km_dist / 111.11

# Bounding box coordinates
lat_min = lat - d
lat_max = lat + d
lon_min = lon - d * math.cos(math.radians(lat))
lon_max = lon + d * math.cos(math.radians(lat))

coords = ",".join([str(x) for x in [lat_min, lon_min, lat_max, lon_max]])
print(f"Bounding box coordinates: {coords}")

# Define the URL for the export endpoint
url = "https://mapprod2.environment.nsw.gov.au/arcgis/rest/services/Coastal_Marine/NSW_Marine_Lidar_Bathymetry_Data_2018/MapServer/export"

# Define the parameters for the request
params = {
    "bbox": coords,  # "xmin,ymin,xmax,ymax",  # Replace with the bounding box for Gordon's Bay
    "bboxSR": "",  # Replace with the spatial reference for the bounding box, if needed
    "layers": "0",  # Replace with the IDs of the layers you want to export
    "format": "tiff",  # We want to export in GeoTIFF format
    "f": "json",  # We want the response in JSON format
}

# Make the request
response = requests.get(url, params=params)

# The response should contain a URL for the exported GeoTIFF
print(json.dumps(response.json(), indent=2))
