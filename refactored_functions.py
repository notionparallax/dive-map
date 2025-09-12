"""
Refactored map functions with improved organization and type hints.

This module contains utility functions that haven't been moved to dedicated classes yet.
Consider this a transition module while refactoring continues.
"""

import math
import warnings
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point, MultiPoint
from shapely import centroid
from geopy.distance import great_circle
from functools import partial

from config import TEXT_COLOUR, X_OFFSET, X_OFFSET_SMALL, Y_OFFSET


def naieve_ffill(df: pd.DataFrame, column: str) -> None:
    """
    Forward fill values in a DataFrame column.

    Args:
        df: DataFrame to modify
        column: Column name to forward fill
    """
    last_valid = None
    for idx, value in df[column].items():
        if pd.isna(value):
            df.loc[idx, column] = last_valid
        else:
            last_valid = value


def make_marker_text(row: pd.Series) -> str:
    """
    Generate marker text based on marker type and number.

    Args:
        row: DataFrame row containing marker information

    Returns:
        Formatted marker text string
    """
    if row.marker_type == "numbered":
        return f"{row.marker_number if row.marker_number else '-'}"
    return ""


def measure_line_string(line_string: LineString) -> float:
    """
    Calculate the length of a LineString in meters.

    Args:
        line_string: The LineString to measure

    Returns:
        Total distance in meters
    """
    total_length = 0

    for i in range(len(line_string.coords) - 1):
        # Reverse coordinates for great_circle (expects lat, lon)
        point1 = tuple(reversed(line_string.coords[i]))
        point2 = tuple(reversed(line_string.coords[i + 1]))
        distance = great_circle(point1, point2).meters
        total_length += distance

    return total_length


def filter_by_distance(
    gdf: gpd.GeoDataFrame, min_distance: float = 1.5
) -> gpd.GeoDataFrame:
    """
    Filter GeoDataFrame to keep only points separated by minimum distance.

    Args:
        gdf: GeoDataFrame with geometry column
        min_distance: Minimum distance in meters between points

    Returns:
        Filtered GeoDataFrame
    """
    from geopy.distance import geodesic

    filtered_data = []

    for i in range(len(gdf) - 1):
        # Convert to lat, lon format for geodesic
        point1 = (gdf.iloc[i].geometry.y, gdf.iloc[i].geometry.x)
        point2 = (gdf.iloc[i + 1].geometry.y, gdf.iloc[i + 1].geometry.x)

        distance = geodesic(point1, point2).meters

        if distance >= min_distance:
            filtered_data.append(gdf.iloc[i])

    # Always include the last point
    filtered_data.append(gdf.iloc[-1])

    return gpd.GeoDataFrame(pd.concat(filtered_data, axis=1).transpose())


def add_note_label(row: pd.Series, ax: plt.Axes) -> None:
    """Add a note annotation to the map."""
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


def add_intermediate_label(row: pd.Series, ax: plt.Axes) -> None:
    """Add filename marker for intermediate points."""
    filename_text = row.filename.replace(".JPG", "").replace("GOPR", "")

    ax.annotate(
        text=filename_text,
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


def unify_point_cluster(gdf: gpd.GeoDataFrame, marker_number: int) -> Point:
    a = gdf[gdf.canonical_marker_number == marker_number]
    if a.shape[0] == 1:
        p = a.geometry.iloc[0]
    elif a.shape[0] < 1:
        p = centroid(MultiPoint(a.geometry))
    else:
        raise ValueError(f"No marker found for {marker_number}")
    return p


def draw_shortcut_arrow(
    gdf: gpd.GeoDataFrame,
    ax: plt.Axes,
    from_marker_number: int = 3,
    to_marker_number: int = 14,
    text_colour: str = "red",
    arrow_colour: str = "blue",
    text_size: int = 7,
) -> None:
    """
    Draw compass bearing arrow between two markers.

    Args:
        gdf: GeoDataFrame containing marker data
        ax: Matplotlib axes to draw on
        from_marker_number: Starting marker number
        to_marker_number: Ending marker number
        text_colour: Color for bearing text
        arrow_colour: Color for arrow
        text_size: Font size for bearing text
    """
    # Get centroids of marker clusters
    point_a = unify_point_cluster(gdf, from_marker_number)
    point_b = unify_point_cluster(gdf, to_marker_number)

    # Calculate bearing angle
    dy = point_b.y - point_a.y
    dx = point_b.x - point_a.x
    angle = np.rad2deg(np.arctan2(dy, dx))

    # Calculate midpoint for text placement
    midpoint = Point((point_a.x + point_b.x) / 2, (point_a.y + point_b.y) / 2)

    # Add bearing text
    ax.text(
        midpoint.x,
        midpoint.y,
        f"{int((90 - angle) % 360)}º",
        ha="center",
        va="center",
        size=text_size,
        transform_rotates_text=True,
        rotation=angle,
        rotation_mode="anchor",
        color=text_colour,
        zorder=3,
    )

    # Add arrow
    ax.annotate(
        text="",
        xy=[point_b.x, point_b.y],
        xytext=[point_a.x, point_a.y],
        xycoords="data",
        size=text_size,
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


def apply_annotations(
    df: gpd.GeoDataFrame, ax: plt.Axes, annotation_func: callable
) -> None:
    """
    Apply annotation function to all rows in a GeoDataFrame.

    Args:
        df: GeoDataFrame to annotate
        ax: Matplotlib axes
        annotation_func: Function to apply for annotations
    """
    df.apply(partial(annotation_func, ax=ax), axis=1)


# Legacy functions kept for backward compatibility
# TODO: Move these to appropriate classes in future refactoring


def plot_gps_trace(fp: str = "20240308-090746 - Gordons.gpx") -> str:
    """Plot GPS trace from GPX file. Consider using GPXFileLoader instead."""
    recorded_path = gpd.read_file(fp, layer="tracks")
    recorded_path.plot()
    plt.title(fp)
    return fp


def depth_to_colour(depth: float, gdf: gpd.GeoDataFrame) -> str:
    """Convert depth to RGB color string for Folium maps."""
    import matplotlib as mpl

    min_depth = 0
    max_depth = gdf.depth.min()
    scaled_depth = depth / max_depth

    cmap = mpl.colormaps["rainbow_r"]
    c = cmap(scaled_depth)
    return f"rgb({c[0]*255} {c[1]*255} {c[2]*255})"
