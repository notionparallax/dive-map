"""Plot a map of the NSW Seabed Landforms data for Gordon's Bay.

This script fetches the NSW Seabed Landforms data from the Seed 
Portal and plots the marine landforms for Gordon's Bay.
It's acually doing the whole coast from BrokenBay to Cronulla, 
but it's zoomed in on the gordon's bay area.

It's got the bones of the batymetry data in there too, but it's 
not working yet because it's a geotiff, but the files in the 
zip are .adf files, that need to be opened with gdal or qgis, 
and I don't have either yet.
"""

from io import BytesIO
from matplotlib.patches import Rectangle
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import requests


def plot_marine_landforms(
    # URL to the NSW Seabed Landforms data
    data_url1: str = "https://datasets.seed.nsw.gov.au/dataset/3f00d173-aa85-4e58-8dda-97948d772700/resource/58b03d70-b793-4cb7-b11e-dda4b0f9de39/download/marine_landforms06_brokenbay_cronulla_marinelidar.zip",
    fn: str = "data1",
    shapefile_folder: str = "Landforms06_BrokenBay_Cronulla_MarineLidar",
    shapefile_name: str = "Landforms06_BrokenBay_Cronulla_MarineLidar.shp",
    minx: float = 151.25965,
    maxx: float = 151.26881,
    miny: float = -33.919090,
    maxy: float = -33.913145,
):

    # URL to the NSW Seabed Landforms data
    data_url1 = "https://datasets.seed.nsw.gov.au/dataset/3f00d173-aa85-4e58-8dda-97948d772700/resource/58b03d70-b793-4cb7-b11e-dda4b0f9de39/download/marine_landforms06_brokenbay_cronulla_marinelidar.zip"

    fn = "data1"

    landforms_shp = os.path.normpath(
        os.path.join(
            "SEED/",
            fn,
            shapefile_folder,
            shapefile_name,
        )
    ).replace("\\", "/")
    # Check if the shapefile exists
    if not os.path.exists(landforms_shp):
        # Fetch the data
        response = requests.get(data_url1)
        # Check if the response is a zip file
        if response.headers["Content-Type"] != "application/zip":
            raise ValueError("The URL did not return a zip file. Please check the URL.")
        with open(f"{fn}.zip", "wb") as file:
            file.write(response.content)
        zip_file = ZipFile(f"{fn}.zip")
        # Extract the shapefile
        zip_file.extractall(fn)

    # Load the shapefile into a GeoDataFrame
    gdf = gpd.read_file(landforms_shp)
    # Check the coordinate system of the GeoDataFrame
    print("GeoDataFrame CRS:", gdf.crs)

    # Transform the GeoDataFrame to WGS84 (latitude and longitude)
    gdf = gdf.to_crs(epsg=4326)
    gdf.head()

    # Filter the data for Gordon's Bay (replace with actual coordinates or bounding box)
    gordons_bay_bounds = {
        "minx": 151.259654,
        "miny": -33.91909070391122,
        "maxx": 151.26881457540935,
        "maxy": -33.913145,
    }
    gdf_gordons_bay = gdf.cx[
        gordons_bay_bounds["minx"] : gordons_bay_bounds["maxx"],
        gordons_bay_bounds["miny"] : gordons_bay_bounds["maxy"],
    ]

    # Load the world dataset
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Filter for Australia
    australia = world[world.name == "Australia"]
    # Plot the 1m contour lines
    fig, ax = plt.subplots(figsize=(10, 10))
    australia.boundary.plot(ax=ax, edgecolor="black")
    gdf_gordons_bay.plot(ax=ax, column="LANDFORM", cmap="terrain", legend=True)
    # gdf_gordons_bay.plot(ax=ax, cmap="terrain", legend=True)

    # Set the plot limits to the bounding box
    ax.set_xlim(gordons_bay_bounds["minx"], gordons_bay_bounds["maxx"])
    ax.set_ylim(gordons_bay_bounds["miny"], gordons_bay_bounds["maxy"])

    plt.title("Marine Landforms for Gordon's Bay")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("SEED/gordons_bay_landforms.png")
    plt.show()

    return ax


plot_marine_landforms()


#
data_url = "https://datasets.seed.nsw.gov.au/dataset/aa8f268e-a23d-4d27-b046-f60c45f8349b/resource/2ef6c816-04b1-4aa7-9f06-e727b9c0cdd9/download/bathymetrymosaic_marinelidar_mbes.zip"

# %%
bathymetry = gpd.read_file(
    "SEED/data2/BathymetryMosaic_MarineLidar_MBES/ml_mb_dem0.ovr"
)
# %%
from osgeo import gdal

# Path to the .adf file
input_file = "SEED/data2/BathymetryMosaic_MarineLidar_MBES/ml_mb_dem0/w001000.adf"
output_file = "SEED/data2/BathymetryMosaic_MarineLidar_MBES/ml_mb_dem0/w001000.tif"

# Convert to GeoTIFF
gdal.Translate(output_file, input_file)

# %%
