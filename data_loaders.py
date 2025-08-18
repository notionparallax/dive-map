"""Data loading utilities for the dive map project."""

import os
import warnings
from datetime import timedelta
from typing import List, Dict, Any, Optional, Union
import pandas as pd
import geopandas as gpd
import dateparser

try:
    import fitdecode
    import gpxpy
except ImportError:
    # These will be available when requirements are installed
    pass
from shapely.geometry import Point
from dateutil import tz
from config import CRS


class FitFileLoader:
    """Handles loading and processing of FIT files from dive computers."""

    @staticmethod
    def load_depth_data(file_path: str) -> List[Dict[str, Any]]:
        """Load depth data from a single FIT file."""
        depth_data = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with fitdecode.FitReader(file_path) as fit_file:
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

    @classmethod
    def create_depth_dataframe(cls, fit_files: List[str]) -> pd.DataFrame:
        """Create a consolidated depth dataframe from multiple FIT files."""
        depth_dataframes = []

        for fit_file in fit_files:
            raw_data = cls.load_depth_data(fit_file)
            df = pd.DataFrame(raw_data).set_index("dt")
            df["source_file"] = fit_file
            depth_dataframes.append(df)

        return pd.concat(depth_dataframes)


class GPXFileLoader:
    """Handles loading and processing of GPX files from GPS tracks."""

    @staticmethod
    def load_gps_track(
        file_path: str,
        description: str = "dive",
        crop: bool = False,
        end_time: Optional[str] = None,
        dive_end_time_delta: int = 70,
        dive_start_time_delta: int = 120,
    ) -> List[Dict[str, Any]]:
        """Load GPS track data from a GPX file with optional time cropping."""

        with open(file_path, "r", encoding="utf-8") as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        # Set up time filtering if cropping is enabled
        if crop and end_time:
            end_time_parsed = dateparser.parse(end_time)
            dive_end_time = end_time_parsed - timedelta(minutes=dive_end_time_delta)
            dive_start_time = end_time_parsed - timedelta(minutes=dive_start_time_delta)

        gps_data = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # Apply time filtering if enabled
                    if crop and end_time:
                        if not (dive_start_time < point.time < dive_end_time):
                            continue

                    gps_data.append(
                        {
                            "lon": point.longitude,
                            "lat": point.latitude,
                            "dt": point.time,
                            "description": description,
                        }
                    )

        return gps_data

    @classmethod
    def create_dive_dataframe(cls, gps_data: List[Dict[str, Any]]) -> gpd.GeoDataFrame:
        """Create a GeoDataFrame from GPS track data."""
        df = pd.DataFrame(gps_data).set_index("dt")
        df["geometry"] = df.apply(lambda row: Point(row.lon, row.lat), axis=1)
        return gpd.GeoDataFrame(df, crs=CRS)


class PhotoMetaLoader:
    """Handles loading and processing of photo metadata."""

    @staticmethod
    def process_photo_metadata(photo_meta_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Process photo metadata and standardize timestamps."""
        sydney_tz = tz.gettz("Australia/Sydney")

        for photo in photo_meta_data:
            naive_dt = photo["datetime"]
            sydney_dt = naive_dt.replace(tzinfo=sydney_tz)
            utc_dt = sydney_dt.astimezone(tz.tzutc())
            photo["dt"] = utc_dt

        return pd.DataFrame(photo_meta_data).set_index("dt")


class DiveDataProcessor:
    """Processes and combines all dive-related data sources."""

    def __init__(self):
        self.fit_loader = FitFileLoader()
        self.gpx_loader = GPXFileLoader()
        self.photo_loader = PhotoMetaLoader()

    def load_all_data(
        self,
        fit_files: List[str],
        gpx_configs: List[Dict[str, Any]],
        photo_metadata: List[Dict[str, Any]],
    ) -> tuple[pd.DataFrame, gpd.GeoDataFrame, pd.DataFrame]:
        """Load and return all data sources."""

        # Load depth data
        depth_df = self.fit_loader.create_depth_dataframe(fit_files)

        # Load GPS data
        all_gps_data = []
        for config in gpx_configs:
            gps_data = self.gpx_loader.load_gps_track(**config)
            all_gps_data.extend(gps_data)

        dives_gdf = self.gpx_loader.create_dive_dataframe(all_gps_data)

        # Load photo data
        photo_df = self.photo_loader.process_photo_metadata(photo_metadata)

        return depth_df, dives_gdf, photo_df
