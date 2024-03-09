# %%
from datetime import timedelta

import dateparser
import fitdecode
import folium
import geopandas as gp
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import pandas as pd
from dateutil import tz
from shapely.geometry import LineString, Point

from photo_meta import photo_meta

# %% depth data
depth_data = []
with fitdecode.FitReader("ScubaDiving_2024-03-08T09_29_45.fit") as fit_file:
    for frame in fit_file:
        if isinstance(frame, fitdecode.records.FitDataMessage):
            if frame.name == "record":
                depth_data.append(
                    {
                        # frame.name,
                        # [x.name for x in frame.fields],
                        "dt": frame.get_value("timestamp"),
                        "depth": -frame.get_value("depth"),
                    }
                )
depth_df = pd.DataFrame(depth_data).set_index("dt")
depth_df.plot(
    title="Depth of dive 1 around the gordon's chain",
    ylabel="Depth (m)",
    xlabel="Time (UTC)",
)
# %%
depth_df.head()

# %%
fp = "20240308-090746 - Gordons.gpx"
recorded_path = gp.read_file(fp, layer="tracks")
recorded_path.head()
# %%
recorded_path.plot()

# %% filter it down to just the dives, because this also has the bus trip back to the shop
with open(fp, "r", encoding="utf-8") as gpx_file:
    # gpx is a gpx object which contains lots of metadata as well
    gpx = gpxpy.parse(gpx_file)


# %%
end_time = dateparser.parse("2024-03-08T02:25:26Z")
dive_2_end_time = end_time - timedelta(minutes=70)
dive_2_start_time = end_time - timedelta(minutes=120)
dive_1_end_time = end_time - timedelta(minutes=180)
dive_1_start_time = end_time - timedelta(minutes=250)


dive_1_points = []
dive_2_points = []
dives_LLT = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if point.time < dive_1_end_time and point.time > dive_1_start_time:
                dive_1_points.append([point.longitude, point.latitude])
                dives_LLT.append(
                    {
                        "lon": point.longitude,
                        "lat": point.latitude,
                        "dt": point.time,
                        "description": "chain_loop",
                    }
                )
            elif point.time < dive_2_end_time and point.time > dive_2_start_time:
                dive_2_points.append([point.longitude, point.latitude])
                dives_LLT.append(
                    {
                        "lon": point.longitude,
                        "lat": point.latitude,
                        "dt": point.time,
                        "description": "boulder_garden",
                    }
                )

dive_data = [
    {
        "label": "dive_1",
        "geometry": LineString(dive_1_points),
        "colour": "red",
        "len": len(dive_1_points),
    },
    {
        "label": "dive_2",
        "geometry": LineString(dive_2_points),
        "colour": "green",
        "len": len(dive_2_points),
    },
]

# TODO: this is a filthy O(N²) loop, is there a more efficient way to do this?
# Create a timezone object for Sydney
sydney_tz = tz.gettz("Australia/Sydney")
for photo in photo_meta:
    naive_dt = photo["dt"]
    sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
    utc_dt = sydney_dt.astimezone(tz.tzutc())
    seg_start = utc_dt - timedelta(seconds=5)
    seg_end = utc_dt + timedelta(seconds=5)
    seg_points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.time < seg_end and point.time > seg_start:
                    seg_points.append([point.longitude, point.latitude])
    dive_data.append(
        {
            "label": photo["filename"].replace(".JPG", ""),
            "geometry": LineString(seg_points),
            "colour": "blue",
            "len": len(seg_points),
        },
    )

dives = gp.GeoDataFrame(dive_data)
dives.head()
# %%
dives.plot(color=dives.colour)
plt.tight_layout()
plt.savefig("docs/plain_graph.png")


# %%
def hack_the_coords_out(path):
    """Pull a list of [y, x] pairs.

    No idea if this is the easiest way to do this, I got a
    lot of NotImplementedYet errors for .coords and .xy
    """
    x = list(path.geometry[0].geoms[0].xy[0])
    y = list(path.geometry[0].geoms[0].xy[1])
    coords = list(zip(y, x))
    return coords


# %%
gordons_coords = [-33.91611178427029, 151.2636983190627]
f_map = folium.Map(
    location=gordons_coords,
    # tiles="CartoDB Positron",
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri Satellite",
    zoom_start=17,
)
# folium.PolyLine(
#     locations=hack_the_coords_out(recorded_path),
#     color="#FF0000",
#     weight=5,
#     tooltip="Walking around my office block",
# ).add_to(f_map)

folium.PolyLine(
    locations=zip(dives.iloc[0].geometry.xy[1], dives.iloc[0].geometry.xy[0]),
    color="red",
    weight=5,
    tooltip="dive 1, following the chain",
).add_to(f_map)
folium.PolyLine(
    locations=zip(dives.iloc[1].geometry.xy[1], dives.iloc[1].geometry.xy[0]),
    color="green",
    weight=5,
    tooltip="dive 2, outlining the rock garden",
).add_to(f_map)
f_map

# %%
dives_df = pd.DataFrame(dives_LLT).set_index("dt")
# %%
dives_df["geometry"] = dives_df.apply(lambda row: Point(row.lon, row.lat), axis=1)
dives_gdf = gp.GeoDataFrame(dives_df)
dives_gdf.plot()
# %%
dives_df.head()
# %%
depth_df.head()
# %%
sydney_tz = tz.gettz("Australia/Sydney")
for photo in photo_meta:
    naive_dt = photo["dt"]
    sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
    utc_dt = sydney_dt.astimezone(tz.tzutc())
    photo["dt"] = utc_dt

photo_df = pd.DataFrame(photo_meta).set_index("dt")
photo_df.head()

# %%
# Convert all timestamps to UTC
dives_df.index = dives_df.index.tz_convert("UTC")
depth_df.index = depth_df.index.tz_convert("UTC")
photo_df.index = photo_df.index.tz_convert("UTC")
# %%
print("dives_df:", repr(dives_df.iloc[0].name))
print("depth_df:", repr(depth_df.iloc[0].name))
print("photo_df:", repr(photo_df.iloc[0].name))
# %%
dives_df["source"] = "dives"
depth_df["source"] = "depth"
photo_df["source"] = "photo"
# %%
all_df = pd.concat([dives_df, depth_df, photo_df], sort=True)
all_df.sample(10)
# %%
all_df.head(20)
