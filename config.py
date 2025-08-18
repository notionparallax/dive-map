"""Configuration settings for the dive map project."""

# Coordinate reference system
from shapely import LineString, Point


CRS = "EPSG:4326"

# Plotting constants
TEXT_COLOUR = "white"
X_OFFSET = 0.0001
X_OFFSET_SMALL = 0.0002
Y_OFFSET = 0.000015

# Dive site coordinates
GORDONS_BAY_COORDS = [-33.9161117, 151.26369831]

# Contour settings
CONTOUR_SPACING = 1
DEPTH_RANGE = (-15, 0)

# Grid resolution for interpolation
DEFAULT_GRID_X = 170
DEFAULT_GRID_Y = 170

# Tolerance settings
WORST_CASE_CORD_ANGLE = 35  # degrees
DISTANCE_FILTER_THRESHOLD = 1.5  # meters

# Color mappings for bottom conditions
BOTTOM_CONDITION_COLORS = {
    "rocky": "gray",
    "sandy": "khaki",
    "kelp": "seagreen",
    "low and sandy": "darkkhaki",
    "sandy and kelp": "mediumseagreen",
    "sandy and rocky": "thistle",
    "low and rocky": "mediumaquamarine",
    "low": "lightgreen",
    "rocky low kelp": "darkseagreen",
    "shore_rocks": "dimgrey",
    "beach": "papayawhip",
    "protruding_bommie": "red",
    "made_up_bottom_1": "red",
    "made_up_bottom_2": "red",
    "made_up_bottom_3": "red",
}

# Depth mappings for shore features
SHORE_DEPTHS = {
    "shore_rocks": 0,
    "beach": 0,
    "protruding_bommie": -0.5,
    "made_up_bottom_1": -9,
    "made_up_bottom_2": -6,
    "made_up_bottom_3": -12,
}

SPEAR_FISHING_BOUNDARY_COORDS = [
    Point(151.262863, -33.917595),
    Point(151.263333, -33.918333),
    Point(151.271667, -33.915833),
]


# File paths
FIT_FILES_DIR = "fit"
GPS_FILES_DIR = "gps"
DOCS_DIR = "docs"

# Plot settings
FIGURE_SIZE = (30, 18)
PLOT_DPI = 300
