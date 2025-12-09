import os
from glob import glob
from typing import cast

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from config.configuration import (
    FILTERING_AREA_NAME,
    FORMER_DATETIME,
    LATTER_DATETIME,
    PARCEL_LAT_BOTTOM,
    PARCEL_LAT_TOP,
    PARCEL_LEVEL_KM,
    PARCEL_LON_LEFT,
    PARCEL_LON_RIGHT,
    REC_LAT_BOTTOM,
    REC_LAT_TOP,
    REC_LON_LEFT,
    REC_LON_RIGHT,
    TRAJECTORY_RESULTS_DIR,
    TRAJECTORY_TYPE,
    VARIABLE,
    filter_parcels_in_rectangle,
    plot_elevation_contour,
    plot_filtering_area,
    wrfout_path,
)
from config.constant import IMAGE_DPI, TITLE_SIZE, cbar_auto_ticks
from constant.analysis_type import TrajectoryAnalysisType
from constant.variables import VARIABLE_DICTIONARY
from figure.drawer.fig_axes import FigureAxesController
from figure.drawer.horizontal_track_drawer import HorizontalTrackDrawer
from figure.property.fig_property import FigureProperties
from loader.parcel_reader import TrajectoryResultReader
from util.path import generate_path
from wrf import getvar, to_np


def make_horizontal_track_figure():
    # create instances for vizualization
    props = FigureProperties()
    drawer = HorizontalTrackDrawer(props=props)
    target_ax = FigureAxesController(ax=drawer.ax, props=props)

    # create an instance for reading trajectory data
    reader = TrajectoryResultReader(TRAJECTORY_TYPE)
    traj_type = TRAJECTORY_TYPE.value

    # read each parcel track and plot
    result_files = sorted(glob(f"{TRAJECTORY_RESULTS_DIR}/*.asc"))
    if not result_files:
        raise FileNotFoundError(
            f"No trajectory result files found in {TRAJECTORY_RESULTS_DIR}"
        )
    for result_file in result_files:
        parcel_track = reader.get_parcel_track(
            result_filepath=result_file,
            variable=VARIABLE,
        )
        lons, lats, var_values = (
            parcel_track.lons,
            parcel_track.lats,
            parcel_track.var_values,
        )
        # skip parcels in the specified rectangle area
        if filter_parcels_in_rectangle:
            if not (
                (REC_LON_LEFT <= lons)
                & (lons <= REC_LON_RIGHT)
                & (REC_LAT_BOTTOM <= lats)
                & (lats <= REC_LAT_TOP)
            ).any():
                continue
        # plot each trajectory line
        points = np.array([lons[:], lats[:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        target_ax.plot_trajectory_line(
            point_segments=segments, var_values=var_values
        )
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()

    # elevation contour plot
    if plot_elevation_contour:
        nc = netCDF4.Dataset(wrfout_path)  # type: ignore
        elevation = cast(np.ndarray, to_np(getvar(nc, "HGT")))
        lat = cast(np.ndarray, getvar(nc, "XLAT"))
        lon = cast(np.ndarray, getvar(nc, "XLONG"))
        target_ax.plot_contour(
            lon=lon,
            lat=lat,
            data=elevation,
        )

    if plot_filtering_area:
        drawer.plot_rectangle_area(
            lon_left=REC_LON_LEFT,
            lon_right=REC_LON_RIGHT,
            lat_bottom=REC_LAT_BOTTOM,
            lat_top=REC_LAT_TOP,
        )

    # trajectory period
    from_dt = LATTER_DATETIME if traj_type == "backward" else FORMER_DATETIME
    to_dt = FORMER_DATETIME if traj_type == "backward" else LATTER_DATETIME

    # title
    title = f"{traj_type} trajectory:  {VARIABLE_DICTIONARY[VARIABLE.name]}   {from_dt} to {to_dt}\nparcels at {PARCEL_LAT_BOTTOM}°N-{PARCEL_LAT_TOP}°N, {PARCEL_LON_LEFT}°E-{PARCEL_LON_RIGHT}°E at {PARCEL_LEVEL_KM}km"
    filename = f"{traj_type}_trajectory_map_{VARIABLE.name}_at_{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}_{PARCEL_LEVEL_KM}km.jpg"
    saving_rootdir = generate_path(f"/img/{os.path.basename(wrfout_path)}")
    saving_dir = f"{saving_rootdir}/{traj_type}/{from_dt}-{to_dt}/{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}/{PARCEL_LEVEL_KM}km/{VARIABLE.name}"
    if filter_parcels_in_rectangle:
        saving_dir += f"/{FILTERING_AREA_NAME}"
    target_ax.set_title(title, fontsize=TITLE_SIZE)

    # save
    target_ax.save_figure(
        fig=drawer.fig,
        save_dir=saving_dir,
        filename=filename,
        dpi=IMAGE_DPI,
    )
    plt.cla()
    plt.close()
