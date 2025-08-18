"""Visualization utilities for dive map generation."""

import math
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy import Point as geopy_pt
from geopy.distance import geodesic
import contextily as cx
from shapely.geometry import LineString, Point, MultiPoint
from shapely import centroid
import scipy.interpolate

from config import (
    TEXT_COLOUR,
    X_OFFSET,
    X_OFFSET_SMALL,
    Y_OFFSET,
    FIGURE_SIZE,
    WORST_CASE_CORD_ANGLE,
    BOTTOM_CONDITION_COLORS,
)


class MapRenderer:
    """Main class for rendering the dive map visualization."""

    def __init__(self, figure_size: Tuple[int, int] = FIGURE_SIZE):
        self.figure_size = figure_size
        self.ax = None
        self.fig = None

    def create_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create and return figure and axes."""
        self.fig, self.ax = plt.subplots(figsize=self.figure_size)
        return self.fig, self.ax

    def add_scalebar(self, starting_point: geopy_pt, distances: List[int]):
        """Add a scale bar to the map."""
        scalebar_helper = ScaleBarRenderer()
        scalebar_data = scalebar_helper.create_scalebar_geometry(
            starting_point, distances
        )

        # Plot the scalebar lines
        scale_gdf = gpd.GeoDataFrame(geometry=scalebar_data["scalebar_lines"])
        scale_gdf.plot(ax=self.ax, color=TEXT_COLOUR)

        # Add distance labels
        for i, point in enumerate(scalebar_data["number_points"]):
            self.ax.text(
                point.x,
                point.y,
                distances[i],
                ha="center",
                fontsize=5,
                color=TEXT_COLOUR,
            )

    def add_north_arrow(self, bottom_point: geopy_pt):
        """Add north arrow to the map."""
        arrow_renderer = CompassRenderer()
        arrow_renderer.draw_north_arrow(self.ax, bottom_point)

    def add_contours(self, contour_data: pd.DataFrame, levels: List[int]):
        """Add depth contours to the map."""
        contour_renderer = ContourRenderer()
        contour_renderer.plot_contours(self.ax, contour_data, levels)

    def add_basemap(self, gdf: gpd.GeoDataFrame):
        """Add satellite basemap."""
        cx.add_basemap(
            self.ax,
            crs=gdf.crs,
            source=cx.providers.Esri.WorldImagery,
        )

    def finalize_plot(self, bounds: Tuple[float, float, float, float], title: str):
        """Set bounds, title and finalize the plot."""
        self.ax.set_xlim([bounds[0], bounds[2]])
        self.ax.set_ylim([bounds[1], bounds[3]])
        self.ax.set_title(title)
        plt.tight_layout()


class ScaleBarRenderer:
    """Handles creation of scale bars."""

    @staticmethod
    def move_point(starting_point: geopy_pt, meters: float, bearing: float) -> geopy_pt:
        """Move a point by specified distance and bearing."""
        d = geodesic(meters=meters)
        return d.destination(point=starting_point, bearing=bearing)

    def create_scalebar_geometry(
        self, starting_point: geopy_pt, distances: List[int], thickness: int = 5
    ) -> Dict[str, List]:
        """Create geometry for scalebar lines and number points."""
        scalebar_lines = []
        number_points = [starting_point]

        for i, distance in enumerate(distances[1:], 1):
            start = distances[i - 1]
            end = distance

            # Move east for the specified distance
            east_pt = self.move_point(starting_point, end - start, 90)
            number_points.append(east_pt)

            # Create horizontal line
            line_east = LineString(
                [
                    (starting_point.longitude, starting_point.latitude),
                    (east_pt.longitude, east_pt.latitude),
                ]
            )
            scalebar_lines.append(line_east)

            # Create vertical tick mark
            ns_pt = self.move_point(east_pt, thickness, 0 if i % 2 == 0 else 180)
            line_ns = LineString(
                [
                    (east_pt.longitude, east_pt.latitude),
                    (ns_pt.longitude, ns_pt.latitude),
                ]
            )
            scalebar_lines.append(line_ns)

            starting_point = ns_pt

        # Convert to Points for labeling
        x_pos = self.move_point(starting_point, thickness / 2, 0).latitude
        number_points = [Point(p.longitude, x_pos) for p in number_points]

        return {"scalebar_lines": scalebar_lines, "number_points": number_points}


class CompassRenderer:
    """Handles rendering of compass/north arrow."""

    @staticmethod
    def move_point(starting_point: geopy_pt, meters: float, bearing: float) -> geopy_pt:
        """Move a point by specified distance and bearing."""
        d = geodesic(meters=meters)
        return d.destination(point=starting_point, bearing=bearing)

    def draw_north_arrow(self, ax: plt.Axes, bottom_point: geopy_pt):
        """Draw a north arrow on the map."""
        top_pt = self.move_point(bottom_point, 50, 0)
        south_pt = self.move_point(top_pt, 50, 180)
        mid_pt = self.move_point(bottom_point, 25, 0)
        east_pt = self.move_point(mid_pt, 20, 90)
        west_pt = self.move_point(mid_pt, 20, 270)

        arrow_props = {"arrowstyle": "<|-", "lw": 2, "ec": TEXT_COLOUR}

        # North arrow
        ax.annotate(
            "N",
            xy=(south_pt.longitude, south_pt.latitude),
            xytext=(top_pt.longitude, top_pt.latitude),
            va="center",
            arrowprops=arrow_props,
            color=TEXT_COLOUR,
        )

        # East arrow
        ax.annotate(
            "E",
            xy=(mid_pt.longitude, mid_pt.latitude),
            xytext=(east_pt.longitude, east_pt.latitude),
            va="center",
            arrowprops=arrow_props,
            color=TEXT_COLOUR,
        )

        # West arrow
        ax.annotate(
            "W",
            xy=(mid_pt.longitude, mid_pt.latitude),
            xytext=(west_pt.longitude, west_pt.latitude),
            va="center",
            arrowprops=arrow_props,
            color=TEXT_COLOUR,
        )


class ContourRenderer:
    """Handles depth contour rendering."""

    @staticmethod
    def prep_contour_data(
        df: pd.DataFrame,
        gridpoints_x: int = 100,
        gridpoints_y: int = 70,
        method: str = "linear",
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for contour plotting."""
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

    def plot_contours(
        self,
        ax: plt.Axes,
        contour_data: pd.DataFrame,
        levels: List[int],
        alpha: float = 0.5,
    ):
        """Plot depth contours on the given axes."""
        x, y, z = self.prep_contour_data(contour_data)

        norm = matplotlib.colors.Normalize(vmin=min(levels), vmax=max(levels))
        cmap = plt.get_cmap("rainbow")

        CS = ax.contour(
            x,
            y,
            z,
            levels=levels,
            colors=[cmap(norm(level)) for level in levels],
            alpha=alpha,
        )
        ax.clabel(CS, inline=1, fontsize=2)


class MarkerRenderer:
    """Handles rendering of dive markers and annotations."""

    @staticmethod
    def add_numbered_marker(ax: plt.Axes, row: pd.Series):
        """Add a numbered marker annotation."""
        if row.marker_text:
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

    @staticmethod
    def add_tolerance_circle(ax: plt.Axes, row: pd.Series):
        """Add tolerance circle around markers."""
        if row.marker_text:
            radius = (90 / 10_000000) * (
                math.tan(math.radians(WORST_CASE_CORD_ANGLE)) * abs(row.depth)
            )
            circle = plt.Circle(
                (row.geometry.x, row.geometry.y),
                radius,
                color="r",
                fill=False,
                alpha=0.4,
                linestyle="-.",
                zorder=4,
            )
            ax.add_patch(circle)

    @staticmethod
    def create_legend(ax: plt.Axes) -> List:
        """Create legend elements for the map."""
        legend_handles = []

        # Bottom condition colors
        for condition, color in BOTTOM_CONDITION_COLORS.items():
            patch = mpatches.Patch(color=color, label=condition)
            legend_handles.append(patch)

        # Marker types
        markers = [
            {"description": "numbered", "marker": "$\circ$", "colour": "orange"},
            {"description": "unnumbered", "marker": "2", "colour": "blue"},
        ]

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

        # Tolerance circle
        tol_circle = plt.Circle(
            [],
            [],
            color="r",
            fill=False,
            alpha=0.4,
            linestyle="-.",
            label="Tolerance area",
        )
        legend_handles.append(tol_circle)

        ax.legend(handles=legend_handles, loc="lower left")
        return legend_handles
