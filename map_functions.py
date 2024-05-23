# %%
import math
import os
import warnings
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
import scipy
from dateutil import tz
from geopy import Point as geopy_pt
from geopy.distance import geodesic, great_circle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely import centroid
from shapely.geometry import LineString, MultiPoint, Point, Polygon
from shapely.ops import voronoi_diagram

from photo_meta import photo_meta
from photo_meta_day_2 import photo_meta as photo_meta_day_2

photo_meta = photo_meta + photo_meta_day_2

plt.rcParams["svg.fonttype"] = "none"
TEXT_COLOUR = "white"
CRS = "EPSG:4326"
X_OFFSET = 0.0001
X_OFFSET_SMALL = 0.0002
Y_OFFSET = 0.000015


# %% depth data
def get_depth_data_from_fit_file(file_name="ScubaDiving_2024-03-08T09_29_45.fit"):
    depth_data = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
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
    depth_dataframes: list[pd.DataFrame] = []
    for fit_file in fit_files:
        raw = get_depth_data_from_fit_file(file_name=fit_file)
        this_depth_df = pd.DataFrame(raw).set_index("dt")
        this_depth_df["source_file"] = fit_file
        depth_dataframes.append(this_depth_df)

    depth_dataframe = pd.concat(depth_dataframes)
    return depth_dataframe


def plot_gps_trace(fp: str = "20240308-090746 - Gordons.gpx"):
    recorded_path = gp.read_file(fp, layer="tracks")
    recorded_path.plot()
    plt.title(fp)
    return fp


def move_pt(starting_point, meters: float, bearing: float):
    d = geodesic(meters=meters)
    new_point = d.destination(point=starting_point, bearing=bearing)
    return new_point


def draw_scale_bar(
    starting_point, scalebar_distances=[0, 5, 10, 15, 20, 50, 100], thickness=5
):
    scalebar_lines = []

    number_points = [starting_point]

    for i, distance in enumerate(
        scalebar_distances[1:], 1
    ):  # start from the second item
        start = scalebar_distances[i - 1]
        end = distance

        # Move east for the specified distance
        east_pt = move_pt(starting_point, end - start, 90)

        number_points.append(east_pt)
        # Create a line from the starting point to the east point
        # Note the reversal of coordinates for shapely
        line_east = LineString(
            [
                (starting_point.longitude, starting_point.latitude),
                (east_pt.longitude, east_pt.latitude),
            ]
        )
        scalebar_lines.append(line_east)

        # Move north or south for 2 meters
        ns_pt = move_pt(east_pt, thickness, 0 if i % 2 == 0 else 180)

        # Create a line from the east point to the north/south point
        # Note the reversal of coordinates for shapely
        line_ns = LineString(
            [(east_pt.longitude, east_pt.latitude), (ns_pt.longitude, ns_pt.latitude)]
        )
        scalebar_lines.append(line_ns)

        # The north/south point becomes the new starting point for the next iteration
        starting_point = ns_pt

        x_pos = move_pt(starting_point, thickness / 2, 0).latitude

    number_points = [Point(p.longitude, x_pos) for p in number_points]
    return {"scalebar_lines": scalebar_lines, "number_points": number_points}


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
    dives_gdf = gp.GeoDataFrame(dives_df, crs=CRS)
    return dives_gdf


def get_photo_data(photo_meta_data):
    sydney_tz = tz.gettz("Australia/Sydney")
    for photo in photo_meta_data:
        naive_dt = photo["datetime"]
        sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
        utc_dt = sydney_dt.astimezone(tz.tzutc())
        photo["dt"] = utc_dt

    photo_df = pd.DataFrame(photo_meta_data).set_index("dt")
    return photo_df


def naieve_ffill(df, column):
    """Written by copilot"""
    last_valid = None
    for idx, value in df[column].items():
        if pd.isna(value):
            df.loc[idx, column] = last_valid
        else:
            last_valid = value


# %%
def prep_for_contour(
    df, gridpoints_x: int = 100, gridpoints_y: int = 70, method: str = "cubic"
):
    """prep_for_contour _summary_

    Args:
        df (_type_): _description_
        gridpoints_x (int, optional): Number of points in the horizontal direction. Defaults to 100.
        gridpoints_y (int, optional): Number of points in the vertical direction. Defaults to 70.
        method (str, optional): one of ‘linear’, ‘nearest’, ‘cubic’. Defaults to "cubic".

    Returns:
        _type_: _description_
    """
    x = [p.x for p in df.geometry]
    y = [p.y for p in df.geometry]
    z = list(df.depth)

    # Create grid

    xi = np.linspace(min(x), max(x), gridpoints_x)
    yi = np.linspace(min(y), max(y), gridpoints_y)
    xi, yi = np.meshgrid(xi, yi)

    # Interpolate z values
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method=method)
    return xi, yi, zi


# %%
def make_marker_text(row):
    # filename = row.filename.replace(".JPG", "")
    if row.marker_type == "numbered":
        return (
            f"""{row.marker_number if row.marker_number else "-"}"""  # ({filename})"""
        )
    else:
        return ""


# %%
def add_numbered_marker_label(row, ax):
    """Add a numbered marker to the map for the major points on the trail."""
    if row.marker_text != "":
        ax.annotate(
            text=row.marker_text,
            xy=[row.geometry.x, row.geometry.y],
            xytext=[row.geometry.x + X_OFFSET, row.geometry.y],
            xycoords="data",
            size="small",
            color=TEXT_COLOUR,
            ha="center",
            va="center",
            arrowprops=dict(
                arrowstyle="-", connectionstyle="arc3,rad=-0.05", color=TEXT_COLOUR
            ),
            zorder=3,
        )


def add_note_label(row, ax):
    """Add a note to the map for something notable."""
    ax.annotate(
        text=row.note,
        xy=[row.geometry.x, row.geometry.y],
        xytext=[
            row.geometry.x + X_OFFSET * 0.5,
            row.geometry.y + X_OFFSET * 0.5,
        ],
        xycoords="data",
        size="small",
        color=TEXT_COLOUR,
        ha="center",
        va="center",
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=-0.05", color=TEXT_COLOUR
        ),
        zorder=3,
    )


def measure_line_string(the_line_string: LineString) -> float:
    """measure_line_string Returns the length, in metres, of a line string.

    Args:
        the_line_string (LineString): The line string that you want to measure

    Returns:
        float: Total distance in metres
    """
    # Initialize a variable to hold the total length
    total_length = 0

    # Iterate over the points in the LineString
    for i in range(len(the_line_string.coords) - 1):
        # Calculate the distance between each pair of points
        point1 = tuple(reversed(the_line_string.coords[i]))
        point2 = tuple(reversed(the_line_string.coords[i + 1]))
        distance = great_circle(point1, point2).meters
        total_length += distance
    return total_length


def add_tolerance_circle(row, ax):
    """Add a circle to each numbered marker to indicate how much uncertainty there is for a given worst case angle."""
    if row.marker_text != "":
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


def add_intermediate_label(row, ax):
    """Add filename marker to the map for the minor points on the trail."""

    ax.annotate(
        text=row.filename.replace(".JPG", "").replace("GOPR", ""),
        xy=[row.geometry.x, row.geometry.y],
        xytext=[row.geometry.x - X_OFFSET_SMALL, row.geometry.y - Y_OFFSET],
        xycoords="data",
        size=6,
        color=TEXT_COLOUR,
        ha="left",
        va="center",
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=-0.05", color=TEXT_COLOUR
        ),
        alpha=0.6,
        zorder=3,
    )


def draw_shortcut_arrow(
    all_gdf,
    ax,
    from_marker_number=3,
    to_marker_number=14,
    text_colour="red",
    arrow_colour="blue",
):
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
        f"{int( (90 - angle) % 360)}º",
        ha="center",
        va="center",
        size="small",
        transform_rotates_text=True,
        rotation=angle,
        rotation_mode="anchor",
        color=text_colour,
        zorder=3,
    )

    ax.annotate(
        text="",
        xy=[point_b.x, point_b.y],
        xytext=[point_a.x, point_a.y],
        xycoords="data",
        size="small",
        color=text_colour,
        ha="center",
        va="bottom",
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3",
            linestyle=(0, (5, 5)),
            linewidth=0.8,
            shrinkA=10,
            shrinkB=10,
            color=arrow_colour,
        ),
        zorder=3,
    )


def draw_north_arrow(ax, n_bottom_pt):
    n_top_pt = move_pt(n_bottom_pt, 50, 0)
    s_pt = move_pt(n_top_pt, 50, 180)
    # This seems like it's shifting across by 4m, which is pretty strange
    n_mid_pt = move_pt(n_bottom_pt, 25, 0)
    e_pt = move_pt(n_mid_pt, 20, 90)
    w_pt = move_pt(n_mid_pt, 20, 270)
    n_arrowprops = {"arrowstyle": "<|-", "lw": 2, "ec": TEXT_COLOUR}

    # print(
    #     f"""drawing north arrow
    #       {n_bottom_pt}
    #       {n_top_pt}
    #       {s_pt}"""
    # )
    ax.annotate(
        "N",
        xy=(s_pt.longitude, s_pt.latitude),
        xytext=(n_top_pt.longitude, n_top_pt.latitude),
        va="center",
        arrowprops=n_arrowprops,
        color=TEXT_COLOUR,
    )
    ax.annotate(
        "E",
        xy=(n_mid_pt.longitude, n_mid_pt.latitude),
        xytext=(e_pt.longitude, e_pt.latitude),
        va="center",
        arrowprops=n_arrowprops,
        color=TEXT_COLOUR,
    )
    ax.annotate(
        "W",
        xy=(n_mid_pt.longitude, n_mid_pt.latitude),
        xytext=(w_pt.longitude, w_pt.latitude),
        va="center",
        arrowprops=n_arrowprops,
        color=TEXT_COLOUR,
    )


def depth_to_colour(depth, gdf):
    min_depth = 0
    max_depth = gdf.depth.min()
    scaled_depth = depth / max_depth

    cmap = mpl.colormaps["rainbow_r"]
    c = cmap(scaled_depth)
    return f"""rgb({c[0]*255} {c[1]*255} {c[2]*255})"""


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
