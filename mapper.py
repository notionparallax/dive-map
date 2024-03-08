# %%
import geopandas as gp
import folium

# %%

# fp = "20240221-154533 - Around The block.gpx"
fp = "20240308-090746 - Gordons.gpx"
walking_path = gp.read_file(fp, layer="tracks")
walking_path.head()
# %%
walking_path.plot()


# %%
def hack_the_coords_out(path):
    x = list(path.geometry[0].geoms[0].xy[0])
    y = list(path.geometry[0].geoms[0].xy[1])
    coords = list(zip(y, x))
    return coords


# %%
gordons_coords = [-33.91611178427029, 151.2636983190627]
BVN_coords = -33.87223918078827, 151.20757513528568
f_map = folium.Map(
    location=gordons_coords,
    tiles="CartoDB Positron",
    zoom_start=18,
)
folium.PolyLine(
    locations=hack_the_coords_out(walking_path),
    color="#FF0000",
    weight=5,
    tooltip="Walking around my office block",
).add_to(f_map)
f_map

# %%
