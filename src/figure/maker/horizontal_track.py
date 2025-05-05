import os
from glob import glob
from typing import cast

import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from wrf import getvar, to_np

from config.configuration import (
    FORMER_PERIOD_HOUR,
    HEIGHT_KM,
    LATTER_PERIOD_HOUR,
    PARCEL_LAT_BOTTOM,
    PARCEL_LAT_TOP,
    PARCEL_LON_LEFT,
    PARCEL_LON_RIGHT,
    TRAJECTORY_RESULTS_DIR,
    TRAJECTORY_TYPE,
    VARIABLE,
    WRFOUT_PATH,
    plot_elevation_contour,
)
from config.constant import IMAGE_DPI, TITLE_SIZE, cbar_auto_ticks
from constant.analysis_type import TrajectoryAnalysisType
from constant.variables import VARIABLE_DICTIONARY
from figure.drawer.fig_axes import FigureAxesController
from figure.drawer.horizontal_track_drawer import HorizontalTrackDrawer
from figure.property.fig_property import FigureProperties
from loader.parcel_reader import TrajectoryResultReader
from util.path import generate_path


def make_horizontal_track_figure():
    # create instances for vizualization
    props = FigureProperties()
    drawer = HorizontalTrackDrawer(props=props)
    target_ax = FigureAxesController(ax=drawer.ax, props=props)

    # create an instance for reading trajectory data
    reader = TrajectoryResultReader(TrajectoryAnalysisType(TRAJECTORY_TYPE))

    # read each parcel track and plot
    result_files = sorted(glob(f"{TRAJECTORY_RESULTS_DIR}/*.asc"))
    for result_file in result_files:
        parcel_track = reader.get_parcel_track(
            result_filepath=result_file,
            variable=VARIABLE,
        )
        lons, lats, var_values = (
            parcel_track.lon,
            parcel_track.lat,
            parcel_track.var_value,
        )
        points = np.array([lons[:], lats[:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        target_ax.plot_trajectory_line(
            point_segments=segments, var_values=var_values
        )
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()

    # elevation contour plot
    if plot_elevation_contour:
        nc = netCDF4.Dataset(WRFOUT_PATH)
        elevation = cast(np.ndarray, to_np(getvar(nc, "HGT")))
        lat = cast(np.ndarray, getvar(nc, "XLAT"))
        lon = cast(np.ndarray, getvar(nc, "XLONG"))
        target_ax.plot_contour(
            lon=lon,
            lat=lat,
            data=elevation,
        )

    # trajectory period
    from_dt = (
        LATTER_PERIOD_HOUR
        if TRAJECTORY_TYPE == "backward"
        else FORMER_PERIOD_HOUR
    )
    to_dt = (
        FORMER_PERIOD_HOUR
        if TRAJECTORY_TYPE == "backward"
        else LATTER_PERIOD_HOUR
    )

    # title
    title = f"{TRAJECTORY_TYPE} trajectory:  {VARIABLE_DICTIONARY[VARIABLE.name]}   {from_dt} to {to_dt}\nparcels at {PARCEL_LAT_BOTTOM}°N-{PARCEL_LAT_TOP}°N, {PARCEL_LON_LEFT}°E-{PARCEL_LON_RIGHT}°E at {HEIGHT_KM}km"
    filename = f"{TRAJECTORY_TYPE}_trajectory_map_{VARIABLE.name}_at_{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}_{HEIGHT_KM}km.jpg"
    saving_rootdir = generate_path(f"/img/{os.path.basename(WRFOUT_PATH)}")
    saving_dir = f"{saving_rootdir}/{TRAJECTORY_TYPE}/{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}/{HEIGHT_KM}km/{VARIABLE.name}"
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
