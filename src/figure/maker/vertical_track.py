import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config.configuration import (
    FILTERING_AREA_NAME,
    FORMER_DATETIME,
    LATTER_DATETIME,
    LEVEL_MAX,
    LEVEL_MIN,
    MEDIAN_LINE_COLOR,
    MEDIAN_LINEWIDTH,
    PARCEL_LAT_BOTTOM,
    PARCEL_LAT_TOP,
    PARCEL_LEVEL_KM,
    PARCEL_LON_LEFT,
    PARCEL_LON_RIGHT,
    REC_LAT_BOTTOM,
    REC_LAT_TOP,
    REC_LON_LEFT,
    REC_LON_RIGHT,
    RIP4_HISTORY_INTERVAL,
    SHADE_25TH_75TH_ALPHA,
    SHADE_25TH_75TH_COLOR,
    TIME_TICKS_FORMAT,
    TIME_TICKS_INTERVAL,
    TIME_ZONE,
    TRAJECTORY_RESULTS_DIR,
    TRAJECTORY_TYPE,
    VARIABLE,
    filter_parcels_in_rectangle,
    paint_25th_75th_percentile,
    plot_median_track,
    wrfout_path,
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
    parcel_levels_to_plot = []
    parcel_times_to_plot = []
    result_files = sorted(glob(f"{TRAJECTORY_RESULTS_DIR}/*.asc"))
    for result_file in result_files:
        lons, lats, var_values = reader.get_parcel_track(
            result_filepath=result_file,
            variable=VARIABLE,
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
        # get height and time
        _, _, levels = reader.get_parcel_track(
            result_filepath=result_file,
            variable=Variable.HGT,
        )
        _, _, times = reader.get_parcel_track(
            result_filepath=result_file,
            variable=Variable.TIME,
        )
        # collect parcels to plot median track
        parcel_levels_to_plot.append(levels)
        parcel_times_to_plot.append(times)
        # plot each trajectory line
        points = np.array([times[:], levels[:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        target_ax.plot_trajectory_line(
            point_segments=segments, var_values=var_values
        )
        target_ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        target_ax.set_cbar_label()

    # plot median trajectory line
    if plot_median_track:
        levels_median = np.nanmedian(np.vstack(parcel_levels_to_plot), axis=0)
        times_median = np.nanmedian(np.vstack(parcel_times_to_plot), axis=0)
        points = np.array([times_median[:], levels_median[:]]).T.reshape(
            -1, 1, 2
        )
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        target_ax.plot_median_line(
            point_segments=segments,
            line_color=MEDIAN_LINE_COLOR,
            line_width=MEDIAN_LINEWIDTH,
        )
    # plot 25th-75th percentile shading
    if paint_25th_75th_percentile:
        levels_25th = np.nanpercentile(
            np.vstack(parcel_levels_to_plot), 25, axis=0
        )
        levels_75th = np.nanpercentile(
            np.vstack(parcel_levels_to_plot), 75, axis=0
        )
        times_median = np.nanmedian(np.vstack(parcel_times_to_plot), axis=0)
        target_ax.plot_shaded_area(
            x_values=times_median,
            y_values_bottom=levels_25th,
            y_values_top=levels_75th,
            color=SHADE_25TH_75TH_COLOR,
            alpha=SHADE_25TH_75TH_ALPHA,
        )

    # trajectory time
    former_time = times[-1] if TRAJECTORY_TYPE == "backward" else times[0]
    latter_time = times[0] if TRAJECTORY_TYPE == "backward" else times[-1]

    # axis
    target_ax.set_axis_labels(
        x_label=f"Time ({TIME_ZONE})", y_label="Height [m]"
    )
    target_ax.set_axis_range(
        x_min=former_time,
        x_max=latter_time,
        y_min=LEVEL_MIN,
        y_max=LEVEL_MAX,
    )

    # ticks
    time_labels = pd.date_range(
        start=FORMER_DATETIME,
        end=LATTER_DATETIME,
        freq=f"{RIP4_HISTORY_INTERVAL}min",
    )[::TIME_TICKS_INTERVAL]
    x_ticks = np.arange(
        former_time, latter_time + 0.0000001, RIP4_HISTORY_INTERVAL / 60.0
    )[::TIME_TICKS_INTERVAL]
    target_ax.set_x_ticks_label(
        x_ticks=x_ticks,
        x_labels=list(
            map(lambda x: x.strftime(TIME_TICKS_FORMAT), time_labels)
        ),
    )
    target_ax.ax.tick_params(axis="y", labelsize=13)

    # grid
    target_ax.draw_grid()

    # trajectory period
    from_dt = (
        LATTER_DATETIME if TRAJECTORY_TYPE == "backward" else FORMER_DATETIME
    )
    to_dt = (
        FORMER_DATETIME if TRAJECTORY_TYPE == "backward" else LATTER_DATETIME
    )

    # title
    title = f"{TRAJECTORY_TYPE} trajectory:  {VARIABLE_DICTIONARY[VARIABLE.name]}\nparcels at {PARCEL_LAT_BOTTOM}°N-{PARCEL_LAT_TOP}°N, {PARCEL_LON_LEFT}°E-{PARCEL_LON_RIGHT}°E at {PARCEL_LEVEL_KM}km"
    filename = f"{TRAJECTORY_TYPE}_{VARIABLE.name}_vertical_traj_at_{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}_{PARCEL_LEVEL_KM}km.jpg"
    saving_rootdir = generate_path(f"/img/{os.path.basename(wrfout_path)}")
    saving_dir = f"{saving_rootdir}/{TRAJECTORY_TYPE}/{from_dt}-{to_dt}/{PARCEL_LAT_BOTTOM}_{PARCEL_LAT_TOP}_{PARCEL_LON_LEFT}_{PARCEL_LON_RIGHT}/{PARCEL_LEVEL_KM}km/{VARIABLE.name}"
    if filter_parcels_in_rectangle:
        saving_dir += f"/{FILTERING_AREA_NAME}"
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
