from typing import cast

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.geoaxes import GeoAxes

from config.constant import cbar_auto_ticks
from figure.drawer.fig_axes import FigureAxesController
from figure.map.plot import make_blank_map
from figure.property.fig_property import FigureProperties


class HorizontalTrackDrawer:
    def __init__(self, props: FigureProperties) -> None:
        self._props = props
        self.fig = plt.figure(figsize=self._props.figsize)
        ax = cast(
            GeoAxes,
            self.fig.add_axes(
                (0.11, 0.1, 0.8, 0.8),
                projection=ccrs.PlateCarree(),
            ),
        )
        self.ax = make_blank_map(ax)

    def plot_trajectory_track(
        self,
        ax: FigureAxesController,
        parcel_point_segments: np.ndarray,
        parcel_levels: np.ndarray,
    ) -> None:
        ax.plot_trajectory_line(parcel_point_segments, parcel_levels)
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()

    def plot_contour(
        self,
        ax: FigureAxesController,
        x: np.ndarray,
        y: np.ndarray,
        array: np.ndarray,
    ) -> None:
        ax.plot_contour(x, y, array)
