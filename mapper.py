# %%
import geopandas as gp

# %%

fp = "20240221-154533 - Around The block.gpx"
walking_path = gp.read_file(fp, layer="tracks")
walking_path.head()
# %%
walking_path.plot()

# %%
