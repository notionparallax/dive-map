# %%
import math
from datetime import timedelta

import dateparser
import fitdecode
import folium
import geopandas as gp
import gpxpy
import gpxpy.gpx
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import pytz
from dateutil import tz
from geopandas import overlay
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely import centroid, offset_curve
from shapely.geometry import MultiPoint, Point, Polygon
from shapely.ops import voronoi_diagram

from photo_meta import photo_meta


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
    ["ScubaDiving_2024-03-08T09_29_45.fit", "ScubaDiving_2024-03-08T11_26_21.fit"]
)
depth_df_1.plot(
    title="Depth of the dives\n 1 around the gordon's chain, 2 around the boulder garden",
    ylabel="Depth (m)",
    xlabel="Time (UTC)",
)
# %%
depth_df_2 = make_depth_df(
    [
        "ScubaDiving_2024-03-23T08_51_29.fit",
        "ScubaDiving_2024-03-23T09_41_59.fit",
        "ScubaDiving_2024-03-23T11_06_51.fit",
    ]
)
depth_df_2.plot(
    title="Depth of the dives\n 1 around bottom of the wall/desert interface,\n2 across to the other side",
    ylabel="Depth (m)",
    xlabel="Time (UTC)",
)


# %%
def plot_gps_trace(fp: str = "20240308-090746 - Gordons.gpx"):
    recorded_path = gp.read_file(fp, layer="tracks")
    recorded_path.plot()
    plt.title(fp)
    return fp


first_dive_day = "20240308-090746 - Gordons.gpx"
day_2_dive_1 = "20240323-081550 - Map dive Saturday morning.gpx"
day_2_dive_2 = "20240323-104518 - Dive 2.gpx"
plot_gps_trace(fp=first_dive_day)
plot_gps_trace(fp=day_2_dive_1)
plot_gps_trace(fp=day_2_dive_2)


# %%
def get_gps_data(fp):
    with open(fp, "r", encoding="utf-8") as gpx_file:
        # gpx is a gpx object which contains lots of metadata as well
        gpx = gpxpy.parse(gpx_file)

    # filter it down to just the dives, because this also has the bus trip back to the shop
    end_time = dateparser.parse("2024-03-08T02:25:26Z")
    dive_2_end_time = end_time - timedelta(minutes=70)
    dive_2_start_time = end_time - timedelta(minutes=120)
    dive_1_end_time = end_time - timedelta(minutes=180)
    dive_1_start_time = end_time - timedelta(minutes=250)

    dives_LLT = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.time < dive_1_end_time and point.time > dive_1_start_time:
                    dives_LLT.append(
                        {
                            "lon": point.longitude,
                            "lat": point.latitude,
                            "dt": point.time,
                            "description": "chain_loop",
                        }
                    )
                elif point.time < dive_2_end_time and point.time > dive_2_start_time:
                    dives_LLT.append(
                        {
                            "lon": point.longitude,
                            "lat": point.latitude,
                            "dt": point.time,
                            "description": "boulder_garden",
                        }
                    )

    return dives_LLT


def make_dive_df(fp):
    dives_llt = get_gps_data(fp)
    dives_df = pd.DataFrame(dives_llt).set_index("dt")
    dives_df["geometry"] = dives_df.apply(lambda row: Point(row.lon, row.lat), axis=1)
    dives_gdf = gp.GeoDataFrame(dives_df)
    return dives_df, dives_gdf


# TODO: get rid of one of these two
dives_df, dives_gdf = make_dive_df(first_dive_day)
dives_gdf.plot()


# %%
def get_photo_data():
    sydney_tz = tz.gettz("Australia/Sydney")
    for photo in photo_meta:
        naive_dt = photo["dt"]
        sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
        utc_dt = sydney_dt.astimezone(tz.tzutc())
        photo["dt"] = utc_dt

    photo_df = pd.DataFrame(photo_meta).set_index("dt")
    return photo_df


photo_df = get_photo_data()


# %%
print("dives_df:", repr(dives_df.iloc[0].name))
print("depth_df:", repr(depth_df_1.iloc[0].name))
print("photo_df:", repr(photo_df.iloc[0].name))
# %%
# Convert all timestamps to UTC
dives_df.index = dives_df.index.tz_convert("UTC")
depth_df_1.index = depth_df_1.index.tz_convert("UTC")
photo_df.index = photo_df.index.tz_convert("UTC")
# %%
print("dives_df:", repr(dives_df.iloc[0].name))
print("depth_df:", repr(depth_df_1.iloc[0].name))
print("photo_df:", repr(photo_df.iloc[0].name))
# %%
dives_df["source"] = "dives"
depth_df_1["source"] = "depth"
photo_df["source"] = "photo"

# %%
reduced_dives = dives_df
# reduced_dives = reduced_dives.iloc[::60]  # pick one frame a minute
# reduced_dives = reduced_dives[
#     reduced_dives.index > depth_df.index[0]
# ]  # wait until there's depth data
all_df = pd.concat([reduced_dives, depth_df_1, photo_df])
all_df.sort_index(axis=0, inplace=True)
temp_df = all_df.copy(deep=True)
temp_df.index = temp_df.index.tz_localize(None)
# temp_df.to_csv("all_data.csv")
all_df.head(10)
# %%
all_df["depth"].ffill(inplace=True)
all_df["depth"].fillna(0, inplace=True)
all_df["filename"].ffill(inplace=True, limit=10)
all_df["geometry"].ffill(inplace=True)
all_df["description"].ffill(inplace=True)
all_df.drop(["lat", "lon"], axis=1, inplace=True, errors="ignore")
all_df.head()
# %%
all_gdf = gp.GeoDataFrame(all_df)


# %%
def make_marker_text(row):
    filename = row.filename.replace(".JPG", "")
    if row.marker_type == "numbered":
        return f"""{row.marker_number if row.marker_number else "-"} ({filename})"""
    else:
        return ""


markers_df = all_gdf[(all_gdf.source == "photo") & (all_gdf.marker_type == "numbered")]
intermediate_df = all_gdf[
    (all_gdf.source == "photo") & (all_gdf.marker_type == "intermediate")
]
markers_df["marker_text"] = markers_df.apply(make_marker_text, axis=1)
# %%
uni_marker_df = markers_df.groupby("marker_number").apply(
    lambda grp: pd.Series(
        {
            "geometry": centroid(MultiPoint(list(grp.geometry))),
            "marker_text": grp.marker_text[0],
            "depth": grp.depth.mean(),
        }
    )
)


# %%
X_OFFSET = 0.0004
X_OFFSET_SMALL = 0.0002
Y_OFFSET = 0.00003


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


fig, ax = plt.subplots(figsize=(15, 9))


# plot the swum paths and add a colourbar
cax = all_gdf.plot(column="depth", cmap="rainbow", ax=ax, zorder=2)
divider = make_axes_locatable(ax)
cax_cb = divider.append_axes("right", size="2%", pad=0.05)
cbar = plt.colorbar(cax.collections[0], cax=cax_cb)
cbar.set_label("Depth")

# Plot the voronoi of bottom conditions
points = MultiPoint(list(intermediate_df.geometry))
regions = voronoi_diagram(points)
r = gp.GeoDataFrame(
    {
        "geometry": list(regions.geoms),
        "points": intermediate_df.geometry,
        "bottom_condition": intermediate_df.bottom_condition,
    }
)
colors = {"rocky": "gray", "sandy": "khaki", "kelp": "seagreen", "unspecified": "white"}
legend_handles = []
for condition, color in colors.items():
    patch = mpatches.Patch(color=color, label=condition)
    legend_handles.append(patch)

buffer_radius = 0.0005  # Set this to your desired radius
buffers = Polygon(r.points.convex_hull).buffer(buffer_radius)
buffer_gdf = gp.GeoDataFrame(geometry=[buffers])
clipped_gdf = overlay(r, buffer_gdf, how="intersection")
clipped_gdf["color"] = clipped_gdf["bottom_condition"].map(colors)
clipped_gdf.plot(
    ax=ax,
    edgecolor=None,
    column="bottom_condition",
    color=clipped_gdf["color"],
    zorder=1,
)
# end voronoi


# add the markers
intermediate_df.plot(ax=ax, marker="2", zorder=3)
uni_marker_df.plot(ax=ax, marker="$\circ$", zorder=3)
uni_marker_df.apply(add_numbered_marker_label, axis=1)
uni_marker_df.apply(add_tolerance_circle, axis=1)
intermediate_df.apply(add_intermediate_label, axis=1)

import matplotlib.lines as mlines

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
print(all_gdf[all_gdf.source == "photo"].shape[0], "photos")


# %%
# Your existing code
points = MultiPoint(list(intermediate_df.geometry))
regions = voronoi_diagram(points)
r = gp.GeoDataFrame(
    {
        "geometry": list(regions.geoms),
        "points": intermediate_df.geometry,
        "bottom_condition": intermediate_df.bottom_condition,
    }
)

buffer_radius = 0.0005  # Set this to your desired radius
buffers = Polygon(r.points.convex_hull).buffer(buffer_radius)
buffer_gdf = gp.GeoDataFrame(geometry=[buffers])
clipped_gdf = overlay(r, buffer_gdf, how="intersection")
clipped_gdf.plot(ax=ax, edgecolor=None, column="bottom_condition")
r.points.plot(ax=ax, marker=r"$\circ$", color="red")

# %%
gordons_coords = [-33.91611178427029, 151.2636983190627]


def depth_to_colour(depth):
    min_depth = 0
    max_depth = all_gdf.depth.min()
    scaled_depth = depth / max_depth

    cmap = mpl.colormaps["rainbow_r"]
    c = cmap(scaled_depth)
    return f"""rgb({c[0]*255} {c[1]*255} {c[2]*255})"""


# %%
f_map = folium.Map(
    location=gordons_coords,
    # tiles="CartoDB Positron",
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri Satellite",
    zoom_start=17,
)
chain_loop = folium.FeatureGroup(name="chain trail, depth and gps", show=True).add_to(
    f_map
)
boulder_garden = folium.FeatureGroup(
    name="boulder garden, depth and gps", show=False
).add_to(f_map)
markers = folium.FeatureGroup(name="markers", show=True).add_to(f_map)
intermediate_markers = folium.FeatureGroup(
    name="intermediate markers", show=True
).add_to(f_map)
trail = folium.FeatureGroup(name="the trail", show=True).add_to(f_map)

for index, row in all_gdf[all_gdf.description == "chain_loop"].iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=2,
        color=depth_to_colour(row.depth),
        stroke=False,
        fill=True,
        weight=3,
        fill_opacity=0.6,
        opacity=1,
        tooltip=row.name.astimezone(pytz.timezone("Australia/Sydney")).strftime(
            "%H:%M:%S"
        ),
    ).add_to(chain_loop)

for index, row in all_gdf[all_gdf.description == "boulder_garden"].iterrows():
    folium.CircleMarker(
        location=[row.geometry.y, row.geometry.x],
        radius=2,
        color=depth_to_colour(row.depth),
        stroke=False,
        fill=True,
        weight=3,
        fill_opacity=0.6,
        opacity=1,
        tooltip=row.name.astimezone(pytz.timezone("Australia/Sydney")).strftime(
            "%H:%M:%S"
        ),
    ).add_to(boulder_garden)

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
