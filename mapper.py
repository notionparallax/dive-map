# %%
import math
import os
from datetime import timedelta

import contextily as cx
import dateparser
import fitdecode
import folium
import geopandas as gp
import gpxpy
import gpxpy.gpx
import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
from dateutil import tz
from geopy.distance import geodesic
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely import centroid
from shapely.geometry import MultiPoint, Point, Polygon, box
from shapely.ops import voronoi_diagram

from photo_meta import photo_meta
from photo_meta_day_2 import photo_meta as photo_meta_day_2

photo_meta = photo_meta + photo_meta_day_2

plt.rcParams["svg.fonttype"] = "none"


# %% depth data
def get_depth_data_from_fit_file(file_name="ScubaDiving_2024-03-08T09_29_45.fit"):
    depth_data = []
    with fitdecode.FitReader(file_name) as fit_file:
        for frame in fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == "record":
                    depth_data.append(
                        {
                            "dt": frame.get_value("timestamp"),
                            "depth": -frame.get_value("depth"),
                        }
                    )
        return depth_data


def make_depth_df(fit_files: list[str]) -> pd.DataFrame:
    depth_dataframes = []
    for fit_file in fit_files:
        raw = get_depth_data_from_fit_file(file_name=fit_file)
        depth_df = pd.DataFrame(raw).set_index("dt")
        depth_df["source_file"] = fit_file
        depth_dataframes.append(depth_df)

    depth_dataframe = pd.concat(depth_dataframes)
    return depth_dataframe


depth_df_1 = make_depth_df(
    [
        os.path.join("fit", "ScubaDiving_2024-03-08T09_29_45.fit"),
        os.path.join("fit", "ScubaDiving_2024-03-08T11_26_21.fit"),
    ]
)
depth_df_1.plot(
    title="Depth of the dives\n 1 around the gordon's chain, 2 around the boulder garden",
    ylabel="Depth (m)",
    xlabel="Time (UTC)",
)
# %%
depth_df_2 = make_depth_df(
    [
        os.path.join("fit", "ScubaDiving_2024-03-23T08_51_29.fit"),
        os.path.join("fit", "ScubaDiving_2024-03-23T09_41_59.fit"),
        os.path.join("fit", "ScubaDiving_2024-03-23T11_06_51.fit"),
    ]
)
depth_df_2.plot(
    title="Depth of the dives\n 1 around bottom of the wall/desert interface,\n2 across to the other side",
    ylabel="Depth (m)",
    xlabel="Time (UTC)",
)

depth_df = pd.concat([depth_df_1, depth_df_2])
# depth_df.plot() #This is boring because there's 2 weeks of empty space between dive one and dive 2


# %%
def plot_gps_trace(fp: str = "20240308-090746 - Gordons.gpx"):
    recorded_path = gp.read_file(fp, layer="tracks")
    recorded_path.plot()
    plt.title(fp)
    return fp


first_dive_day = os.path.join("gps", "20240308-090746 - Gordons.gpx")
day_2_dive_1 = os.path.join("gps", "20240323-081550 - Map dive Saturday morning.gpx")
day_2_dive_2 = os.path.join("gps", "20240323-104518 - Dive 2.gpx")
plot_gps_trace(fp=first_dive_day)
plot_gps_trace(fp=day_2_dive_1)
plot_gps_trace(fp=day_2_dive_2)


# %%
def get_gps_data_single_dive(
    fp,
    description="a_nice_dive",
    crop=False,
    end_time="2024-03-08T02:25:26Z",
    dive_end_time_delta=70,
    dive_start_time_delta=120,
):
    with open(fp, "r", encoding="utf-8") as gpx_file:
        # gpx is a gpx object which contains lots of metadata as well
        gpx = gpxpy.parse(gpx_file)

    end_time = dateparser.parse(end_time)
    dive_end_time = end_time - timedelta(minutes=dive_end_time_delta)
    dive_start_time = end_time - timedelta(minutes=dive_start_time_delta)

    dives_lon_lat_time = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if (crop is False) or (
                    point.time < dive_end_time and point.time > dive_start_time
                ):
                    dives_lon_lat_time.append(
                        {
                            "lon": point.longitude,
                            "lat": point.latitude,
                            "dt": point.time,
                            "description": description,
                        }
                    )
                # else:
                #     pass  # this point is outside the crop range

    return dives_lon_lat_time


def make_dive_df(dives_lon_lat_time):
    dives_df = pd.DataFrame(dives_lon_lat_time).set_index("dt")
    dives_df["geometry"] = dives_df.apply(lambda row: Point(row.lon, row.lat), axis=1)
    dives_gdf = gp.GeoDataFrame(dives_df, crs="EPSG:4326")
    return dives_gdf


dives_lon_lat_time_day_1a = get_gps_data_single_dive(
    first_dive_day,
    description="chain_loop",
    crop=True,
    dive_end_time_delta=180,
    dive_start_time_delta=250,
    end_time="2024-03-08T02:25:26Z",
)
dives_gdf_1a = make_dive_df(dives_lon_lat_time_day_1a)
dives_gdf_1a.plot()

dives_lon_lat_time_day_1b = get_gps_data_single_dive(
    first_dive_day,
    description="boulder_garden",
    crop=True,
    end_time="2024-03-08T02:25:26Z",
    dive_end_time_delta=70,
    dive_start_time_delta=120,
)
dives_gdf_1b = make_dive_df(dives_lon_lat_time_day_1b)
dives_gdf_1b.plot()

dives_lon_lat_time_day_2a = get_gps_data_single_dive(
    day_2_dive_1,
    description="wall_to_desert",
    crop=True,
    end_time="2024-03-22 22:52:06+00:00",
    dive_end_time_delta=5,
    dive_start_time_delta=65,
)
# ((dives_gdf_2b.index.max()-dives_gdf_2b.index.min()).total_seconds() / 60)-15,
dives_gdf_2a = make_dive_df(dives_lon_lat_time_day_2a)
dives_gdf_2a.plot()

dives_lon_lat_time_day_2b = get_gps_data_single_dive(
    day_2_dive_2,
    description="far_side_desert",
    crop=True,
    end_time="2024-03-23 01:14:03.999000+00:00",
    dive_end_time_delta=10,
    dive_start_time_delta=68,
)
dives_gdf_2b = make_dive_df(dives_lon_lat_time_day_2b)
dives_gdf_2b.plot()
# %%
dives_gdf = gp.GeoDataFrame(
    pd.concat(
        [
            dives_gdf_1a,
            dives_gdf_1b,
            dives_gdf_2a,
            dives_gdf_2b,
        ]
    )
)
dives_gdf.plot(column="description")
plt.title(f"All dives so far ({', '.join( dives_gdf.description.unique())})")


# %%
def get_photo_data():
    sydney_tz = tz.gettz("Australia/Sydney")
    for photo in photo_meta:
        naive_dt = photo["datetime"]
        sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
        utc_dt = sydney_dt.astimezone(tz.tzutc())
        photo["dt"] = utc_dt

    photo_df = pd.DataFrame(photo_meta).set_index("dt")
    return photo_df


photo_df = get_photo_data()


# %%
print("dives_df:", repr(dives_gdf.iloc[0].name))
print("depth_df:", repr(depth_df.iloc[0].name))
print("photo_df:", repr(photo_df.iloc[0].name))
# %%
# Convert all timestamps to UTC
dives_gdf.index = dives_gdf.index.tz_convert("UTC")
depth_df_1.index = depth_df_1.index.tz_convert("UTC")
photo_df.index = photo_df.index.tz_convert("UTC")
# %%
print("dives_df:", repr(dives_gdf.iloc[0].name))
print("depth_df:", repr(depth_df.iloc[0].name))
print("photo_df:", repr(photo_df.iloc[0].name))
# %%
dives_gdf["source"] = "dives"
depth_df["source"] = "depth"
photo_df["source"] = "photo"

# %%
reduced_dives = dives_gdf
# reduced_dives = reduced_dives.iloc[::60]  # pick one frame a minute
# reduced_dives = reduced_dives[
#     reduced_dives.index > depth_df.index[0]
# ]  # wait until there's depth data
all_df = pd.concat([reduced_dives, depth_df, photo_df])
all_df.sort_index(axis=0, inplace=True)
# temp_df = all_df.copy(deep=True)
# temp_df.index = temp_df.index.tz_localize(None)
# temp_df.to_csv("all_data.csv")
all_df.head()


# %%
def naieve_ffill(df, column):
    """Written by copilot"""
    last_valid = None
    for idx, value in df[column].items():
        if pd.isna(value):
            df.loc[idx, column] = last_valid
        else:
            last_valid = value


all_df["depth"] = all_df["depth"].ffill()
all_df["depth"] = all_df["depth"].fillna(0)
all_df["filename"] = all_df["filename"].ffill(limit=10)
naieve_ffill(all_df, "geometry")
# all_df["geometry"] = all_df["geometry"].ffill()
all_df["description"] = all_df["description"].ffill()
all_df.drop(["lat", "lon"], axis=1, inplace=True, errors="ignore")
all_df.head()
# %%
all_gdf = gp.GeoDataFrame(all_df)


# %%
def make_marker_text(row):
    filename = row.filename.replace(".JPG", "")
    if row.marker_type == "numbered":
        return (
            f"""{row.marker_number if row.marker_number else "-"}"""  # ({filename})"""
        )
    else:
        return ""


markers_df = all_gdf[(all_gdf.source == "photo") & (all_gdf.marker_type == "numbered")]
intermediate_df = all_gdf[
    (all_gdf.source == "photo") & (all_gdf.marker_type == "intermediate")
]
markers_df["marker_text"] = markers_df.apply(make_marker_text, axis=1)
# %%
uni_marker_df = (
    markers_df.groupby("marker_number")
    .apply(
        lambda grp: pd.Series(
            {
                "geometry": centroid(MultiPoint(list(grp.geometry))),
                "marker_text": grp.marker_text[0],
                "depth": grp.depth.mean(),
            }
        )
    )
    .sort_index()
)


# %%
X_OFFSET = 0.0001
X_OFFSET_SMALL = 0.0002
Y_OFFSET = 0.000015


def add_numbered_marker_label(row):
    """Add a numbered marker to the map for the major points on the trail."""
    ax.annotate(
        text=row.marker_text,
        xy=[row.geometry.x, row.geometry.y],
        xytext=[row.geometry.x + X_OFFSET, row.geometry.y],
        xycoords="data",
        size="small",
        color="k",
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.05", color="k"),
        zorder=3,
    )


def add_note_label(row):
    """Add a note to th map for something notable."""
    ax.annotate(
        text=row.note,
        xy=[row.geometry.x, row.geometry.y],
        xytext=[row.geometry.x + X_OFFSET, row.geometry.y + X_OFFSET],
        xycoords="data",
        size="small",
        color="k",
        ha="center",
        va="center",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.05", color="k"),
        zorder=3,
    )


def add_tolerance_circle(row):
    """Add a circle to each numbered marker to indicate how much uncertainty there is for a given worst case angle."""
    worst_case_cord_angle = 35
    ax.add_patch(
        plt.Circle(
            (row.geometry.x, row.geometry.y),
            (90 / 10_000000)
            * (math.tan(math.radians(worst_case_cord_angle)) * abs(row.depth)),
            color="r",
            fill=False,
            alpha=0.4,
            linestyle="-.",
            zorder=4,
        )
    )


def add_intermediate_label(row):
    """Add filename marker to the map for the minor points on the trail."""

    ax.annotate(
        text=row.filename.replace(".JPG", "").replace("GOPR", ""),
        xy=[row.geometry.x, row.geometry.y],
        xytext=[row.geometry.x - X_OFFSET_SMALL, row.geometry.y - Y_OFFSET],
        xycoords="data",
        size=6,
        color="k",
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.05", color="k"),
        alpha=0.6,
        zorder=3,
    )


def draw_shortcut_arrow(all_gdf, ax, from_marker_number=3, to_marker_number=14):
    point_a = MultiPoint(
        all_gdf[all_gdf.marker_number == from_marker_number].geometry
    ).centroid
    point_b = MultiPoint(
        all_gdf[all_gdf.marker_number == to_marker_number].geometry
    ).centroid

    # compute angle in raw data coordinates (no manual transforms)
    dy = point_b.y - point_a.y
    dx = point_b.x - point_a.x
    angle = np.rad2deg(np.arctan2(dy, dx))
    midpoint = Point((point_a.x + point_b.x) / 2, (point_a.y + point_b.y) / 2)

    # annotate with transform_rotates_text to align text and line
    ax.text(
        midpoint.x,
        midpoint.y,
        f"{int(angle%360)}º",
        ha="center",
        va="center",
        size="small",
        transform_rotates_text=True,
        rotation=angle,
        rotation_mode="anchor",
    )

    ax.annotate(
        text="",
        xy=[point_b.x, point_b.y],
        xytext=[point_a.x, point_a.y],
        xycoords="data",
        size="small",
        color="k",
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3",
            linestyle=(0, (5, 5)),
            linewidth=0.8,
            shrinkA=10,
            shrinkB=10,
        ),
        zorder=3,
    )


# %%
fig, ax = plt.subplots(figsize=(15, 9))


# plot the swum paths and add a colourbar
cax = all_gdf.plot(
    column="depth", cmap="rainbow", ax=ax, zorder=2, gid="depth_gps_trace"
)
divider = make_axes_locatable(ax)
cax_cb = divider.append_axes("right", size="2%", pad=0.05)
cbar = plt.colorbar(cax.collections[0], cax=cax_cb)
cbar.set_label("Depth")

# Plot the voronoi of bottom conditions
bottom_gdf = all_gdf[
    (all_gdf.source == "photo") & (all_gdf.bottom_condition != "unspecified")
]

# Initialize an empty list to store the filtered data
filtered_data = []

# Iterate over the GeoDataFrame
for i in range(len(bottom_gdf) - 1):
    # Swap the coordinates in the Point objects
    point1 = (bottom_gdf.iloc[i].geometry.y, bottom_gdf.iloc[i].geometry.x)
    point2 = (bottom_gdf.iloc[i + 1].geometry.y, bottom_gdf.iloc[i + 1].geometry.x)

    # Calculate the distance between the current point and the next point
    distance = geodesic(point1, point2).meters

    # If the distance is greater than or equal to 0.5 meters (500mm), keep the current point
    if distance >= 1.5:
        filtered_data.append(bottom_gdf.iloc[i])

# Append the last point as it has no next point to compare with
filtered_data.append(bottom_gdf.iloc[-1])
# Convert the list to a GeoDataFrame
filtered_gdf = gp.GeoDataFrame(pd.concat(filtered_data, axis=1).transpose())

# Load in the click data
json_df = pd.read_json("click_conditions.json")
click_gdf = gp.GeoDataFrame(
    geometry=json_df.apply(lambda row: Point(row.lon, row.lat), axis=1)
)
click_gdf["bottom_condition"] = json_df.condition

# concat it to the bottom of the dived data
filtered_gdf = pd.concat([filtered_gdf, click_gdf])


# Convert the points in the GeoDataFrame to a MultiPoint object
points = MultiPoint(filtered_gdf.geometry.values)


# Generate the Voronoi diagram
voronoi_polygons = voronoi_diagram(points)

# Convert the Voronoi polygons to a GeoDataFrame
voronoi_gdf = gp.GeoDataFrame(
    filtered_gdf["bottom_condition"],
    geometry=list(voronoi_polygons.geoms),
    crs=bottom_gdf.crs,
)

colors = {
    "rocky": "gray",
    "sandy": "khaki",
    "kelp": "seagreen",
    "low and sandy": "darkkhaki",
    "sandy and kelp": "mediumseagreen",
    "sandy and rocky": "thistle",
    "low and rocky": "mediumaquamarine",
    "low": "lightgreen",
    "shore_rocks": "dimgrey",
    "beach": "papayawhip",
}
# temp until voronoi is sorted out
filtered_gdf["colour"] = filtered_gdf["bottom_condition"].map(colors)
filtered_gdf.plot(color=filtered_gdf.colour, ax=ax, gid="bottom_condition_markers")
# temp until voronoi is sorted out

voronoi_gdf["colour"] = voronoi_gdf["bottom_condition"].map(colors)

legend_handles = []
for condition, color in colors.items():
    patch = mpatches.Patch(color=color, label=condition)
    legend_handles.append(patch)

## I can't get this to work any more :(
buffer_radius = 0.0003  # Set this to your desired radius
# buffers = Polygon(MultiPoint(filtered_gdf.geometry.values).convex_hull).buffer(
#     buffer_radius
# )
# buffer_gdf = gp.GeoDataFrame(geometry=[buffers])
# clipped_gdf = overlay(filtered_gdf, voronoi_gdf, how="intersection")
# TODO: The indexing between the cells and the colours is off. This needs to be
# pulled back into line, and then the voronoi plot uncommented.
# voronoi_gdf.plot(
#     ax=ax,
#     edgecolor=None,
#     # column="bottom_condition",
#     color=voronoi_gdf["colour"],
#     zorder=1,
#     alpha=0.9,
# )
bounds = (
    Polygon(MultiPoint(filtered_gdf.geometry.values).envelope)
    .buffer(buffer_radius)
    .bounds
)
ax.set_xlim([bounds[0], bounds[2]])
ax.set_ylim([bounds[1], bounds[3]])

## end voronoi

# Add context image
cx.add_basemap(ax, crs=voronoi_gdf.crs, source=cx.providers.Esri.WorldImagery)


# add the markers
intermediate_df.plot(ax=ax, marker="2", zorder=3, gid="intermediate_markers")
uni_marker_df.plot(ax=ax, marker="$\circ$", zorder=3, gid="numbered_markers")
uni_marker_df.apply(add_numbered_marker_label, axis=1)
uni_marker_df.apply(add_tolerance_circle, axis=1)
intermediate_df.apply(add_intermediate_label, axis=1)
all_gdf[all_gdf.note.notnull()].apply(add_note_label, axis=1)


# Add the shortcut arrows
# This should be 4 to 14, but I haven't found marker 4 yet
draw_shortcut_arrow(all_gdf, ax, from_marker_number=5, to_marker_number=14)
draw_shortcut_arrow(all_gdf, ax, from_marker_number=11, to_marker_number=16)
draw_shortcut_arrow(all_gdf, ax, from_marker_number=23, to_marker_number=5)


markers = [
    {"description": "numbered", "marker": "$\circ$", "colour": "orange"},
    {"description": "unnumbered", "marker": "2", "colour": "blue"},
]

# Create a Line2D object for each marker type and add it to the legend handles
for marker in markers:
    line = mlines.Line2D(
        [],
        [],
        color=marker["colour"],
        marker=marker["marker"],
        linestyle="None",
        markersize=10,
        label=marker["description"],
    )
    legend_handles.append(line)

tol_circle = plt.Circle(
    [], [], color="r", fill=False, alpha=0.4, linestyle="-.", label="Tolerance area"
)
legend_handles.append(tol_circle)
ax.legend(handles=legend_handles)
ax.set_title("Gordon's bay trail, coloured by depth")
plt.tight_layout()
plt.savefig("docs/marker_graph.png")
plt.savefig("docs/marker_graph.svg")
print(all_gdf[all_gdf.source == "photo"].shape[0], "photos")


# %% folium map time
gordons_coords = [-33.91611178427029, 151.2636983190627]


def depth_to_colour(depth):
    min_depth = 0
    max_depth = all_gdf.depth.min()
    scaled_depth = depth / max_depth

    cmap = mpl.colormaps["rainbow_r"]
    c = cmap(scaled_depth)
    return f"""rgb({c[0]*255} {c[1]*255} {c[2]*255})"""


f_map = folium.Map(
    location=gordons_coords,
    # tiles="CartoDB Positron",
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri Satellite",
    zoom_start=17,
)
dive_1 = folium.FeatureGroup(name="chain trail, depth and gps", show=False).add_to(
    f_map
)
dive_2 = folium.FeatureGroup(name="boulder garden, depth and gps", show=False).add_to(
    f_map
)
dive_3 = folium.FeatureGroup(
    name="along the bottom of the wall's rocks, depth and gps", show=False
).add_to(f_map)
dive_4 = folium.FeatureGroup(
    name="across to the other side and back, depth and gps", show=False
).add_to(f_map)

markers = folium.FeatureGroup(name="markers", show=True).add_to(f_map)
intermediate_markers = folium.FeatureGroup(
    name="intermediate markers", show=True
).add_to(f_map)
trail = folium.FeatureGroup(name="the trail", show=True).add_to(f_map)


def add_depth_trace_to_map(
    all_gdf, to_add_to, filter_name="chain_loop", depth_filter=-0.3, radius=2
):
    for index, row in all_gdf[
        (all_gdf.description == filter_name) & (all_gdf.depth < depth_filter)
    ].iterrows():
        time = row.name.astimezone(pytz.timezone("Australia/Sydney")).strftime(
            "%H:%M:%S"
        )
        tt = f"{time} {row.depth}"
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=radius,
            color=depth_to_colour(row.depth),
            stroke=False,
            fill=True,
            weight=3,
            fill_opacity=0.6,
            opacity=1,
            tooltip=tt,
        ).add_to(to_add_to)


add_depth_trace_to_map(all_gdf, dive_1, filter_name="chain_loop")
add_depth_trace_to_map(all_gdf, dive_2, filter_name="boulder_garden", radius=1)
add_depth_trace_to_map(all_gdf, dive_3, filter_name="wall_to_desert", radius=1)
add_depth_trace_to_map(all_gdf, dive_4, filter_name="far_side_desert", radius=1)

folium.PolyLine(
    locations=[[p.y, p.x] for p in uni_marker_df.geometry],
    color="white",
    weight=2,
    tooltip="The trail, as it stands now",
).add_to(trail)

for index, row in uni_marker_df.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=5,
        color="white",
        stroke=True,
        fill=True,
        weight=1,
        fill_opacity=0.1,
        opacity=1,
        tooltip=row.marker_text,
    ).add_to(markers)

for index, row in intermediate_df.iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=2,
        color="white",
        stroke=True,
        fill=True,
        weight=1,
        fill_opacity=0.1,
        opacity=1,
        # tooltip=row.marker_text,
    ).add_to(intermediate_markers)

folium.LayerControl().add_to(f_map)
f_map.save("docs/gordons_map.html")

f_map
# %%
