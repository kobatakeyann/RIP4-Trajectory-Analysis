import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config.configuration import (
    FORMER_PERIOD_HOUR,
    HEIGHT_KM,
    LATTER_PERIOD_HOUR,
    LEVEL_MAX,
    LEVEL_MIN,
    PARCEL_LAT_BOTTOM,
    PARCEL_LAT_TOP,
    PARCEL_LON_LEFT,
    PARCEL_LON_RIGHT,
    RIP4_TIME_INTERVAL,
    TIME_TICKS_FORMAT,
    TIME_TICKS_INTERVAL,
    TIME_ZONE,
    TRAJECTORY_RESULTS_DIR,
    TRAJECTORY_TYPE,
    VARIABLE,
    WRFOUT_PATH,
)
from config.constant import IMAGE_DPI, cbar_auto_ticks
from constant.analysis_type import TrajectoryAnalysisType
from constant.variables import VARIABLE_DICTIONARY, Variable
from figure.drawer.fig_axes import FigureAxesController
from figure.drawer.vertical_track_drawer import VerticalTrackDrawer
from figure.property.fig_property import FigureProperties
from loader.parcel_reader import TrajectoryResultReader
from util.path import generate_path


def make_vertical_track_figure():
    # create instances for vizualization
    props = FigureProperties()
    drawer = VerticalTrackDrawer(props=props)
    target_ax = FigureAxesController(ax=drawer.ax, props=props)

    # create an instance for reading trajectory data
    reader = TrajectoryResultReader(TrajectoryAnalysisType(TRAJECTORY_TYPE))

    # read each parcel track and plot
    result_files = sorted(glob(f"{TRAJECTORY_RESULTS_DIR}/*.asc"))
    for result_file in result_files:
        parcel_variable_track = reader.get_parcel_track(
            result_filepath=result_file,
            variable=VARIABLE,
        )
        _, _, var_values = (
            parcel_variable_track.lon,
            parcel_variable_track.lat,
            parcel_variable_track.var_value,
        )
        _, _, levels = reader.get_parcel_track(
            result_filepath=result_file,
            variable=Variable.HGT,
        )
        _, _, times = reader.get_parcel_track(
            result_filepath=result_file,
            variable=Variable.TIME,
        )
        points = np.array([times[:], levels[:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        target_ax.plot_trajectory_line(
            point_segments=segments, var_values=var_values
        )
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()

    # trajectory period
    traj_start_time_idx = 0
    traj_end_time_idx = len(times) - 1

    # axis
    target_ax.set_axis_labels(
        x_label=f"Time {TIME_ZONE}", y_label="Height [m]"
    )
    target_ax.set_axis_range(
        x_min=traj_start_time_idx,
        x_max=traj_end_time_idx,
        y_min=LEVEL_MIN,
        y_max=LEVEL_MAX,
    )

    # ticks
    time_labels = pd.date_range(
        start=FORMER_PERIOD_HOUR,
        end=LATTER_PERIOD_HOUR,
        freq=f"{RIP4_TIME_INTERVAL}min",
    )[::TIME_TICKS_INTERVAL]
    x_ticks = np.arange(traj_start_time_idx, traj_end_time_idx + 1, 1)[
        ::TIME_TICKS_INTERVAL
    ]
    target_ax.set_x_ticks_label(
        x_ticks=x_ticks,
        x_labels=list(
            map(lambda x: x.strftime(TIME_TICKS_FORMAT), time_labels)
        ),
    )
    target_ax.ax.tick_params(axis="y", labelsize=13)

    # grid
    target_ax.draw_grid()

    # title
    title = f"{TRAJECTORY_TYPE} trajectory:  {VARIABLE_DICTIONARY[VARIABLE.name]}\nparcels at {PARCEL_LAT_BOTTOM}°N-{PARCEL_LAT_TOP}°N, {PARCEL_LON_LEFT}°E-{PARCEL_LON_RIGHT}°E at {HEIGHT_KM}km"
    filename = f"{TRAJECTORY_TYPE}_{VARIABLE.name}_vertical_traj_at_{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}_{HEIGHT_KM}km.jpg"
    saving_rootdir = generate_path(f"/img/{os.path.basename(WRFOUT_PATH)}")
    saving_dir = f"{saving_rootdir}/{TRAJECTORY_TYPE}/{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}/{HEIGHT_KM}km/{VARIABLE.name}"
    target_ax.set_title(title, fontsize=16)

    # save
    target_ax.save_figure(
        fig=drawer.fig,
        save_dir=saving_dir,
        filename=filename,
        dpi=IMAGE_DPI,
    )
    plt.cla()
    plt.close()
