import os

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

from config.configuration import UNIT_LABEL, plot_contour_label
from config.constant import (
    CBAR_LABEL_LOCATION,
    CBAR_LABEL_SIZE,
    CBAR_TICKS_BASE,
    CBAR_TICKS_INTERVAL,
    CONTOUR_COLOR,
    CONTOUR_LABEL_SIZE,
    CONTOUR_WIDTH,
)
from figure.property.fig_property import FigureProperties


class FigureAxesController:
    def __init__(self, ax: Axes | GeoAxes, props: FigureProperties) -> None:
        self.ax = ax
        self._props = props

    def plot_trajectory_line(
        self, point_segments: np.ndarray, var_values: np.ndarray
    ) -> None:
        lc = LineCollection(point_segments.tolist(), cmap=self._props.colormap)
        lc.set_array(var_values)
        lc.set_linewidth(self._props.line_width)
        lc.set_clim(vmin=self._props.cbar_min, vmax=self._props.cbar_max)
        self.line = self.ax.add_collection(lc)

    def plot_colorbar(self, is_auto_ticks=True) -> None:
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.2, axes_class=Axes)
        plt.gcf().add_axes(cax)
        if is_auto_ticks:
            self.cbar = plt.colorbar(
                self.line,
                cax=cax,
                orientation="vertical",
            )
        else:
            ticks = mticker.IndexLocator(
                base=CBAR_TICKS_BASE, offset=CBAR_TICKS_INTERVAL
            )
            self.cbar = plt.colorbar(
                self.line,
                cax=cax,
                ticks=ticks,
                orientation="vertical",
            )

    def set_cbar_label(self) -> None:
        self.cbar.set_label(
            UNIT_LABEL,
            labelpad=CBAR_LABEL_LOCATION,
            y=1.09,
            rotation=0,
            fontsize=CBAR_LABEL_SIZE,
        )

    def plot_contour(
        self, lon: np.ndarray, lat: np.ndarray, data: np.ndarray
    ) -> None:
        self.contour = self.ax.contour(
            lon,
            lat,
            data,
            transform=ccrs.PlateCarree(),
            levels=self._props.contour_levels,
            linewidths=CONTOUR_WIDTH,
            colors=CONTOUR_COLOR,
        )
        if plot_contour_label:
            self.ax.clabel(
                self.contour,
                levels=self._props.clabel_levels,
                fmt="%.{0[0]}f".format([0]),
                fontsize=CONTOUR_LABEL_SIZE,
            )

    def set_axis_labels(self, x_label: str, y_label: str) -> None:
        self.ax.set_xlabel(x_label, fontsize=16)
        self.ax.set_ylabel(y_label, fontsize=16)
        self.ax.tick_params(axis="both")

    def set_axis_range(
        self,
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
    ) -> None:
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

    def set_x_ticks_label(
        self, x_ticks: np.ndarray, x_labels: list[str]
    ) -> None:
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_labels, rotation=45)

    def draw_grid(self) -> None:
        self.ax.grid(which="major", linestyle="--", linewidth=0.4)

    def set_title(self, title_name: str, fontsize: float) -> None:
        self.ax.set_title(title_name, fontsize=fontsize)

    def save_figure(
        self, fig: Figure, save_dir: str, filename: str, dpi: int
    ) -> None:
        os.makedirs(save_dir, exist_ok=True)
        out_path = os.path.join(save_dir, filename)
        fig.savefig(out_path, dpi=dpi)
