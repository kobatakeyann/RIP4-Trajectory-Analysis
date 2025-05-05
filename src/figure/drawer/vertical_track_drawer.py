import matplotlib.pyplot as plt
import numpy as np

from config.constant import cbar_auto_ticks
from figure.drawer.fig_axes import FigureAxesController
from figure.property.fig_property import FigureProperties


class VerticalTrackDrawer:
    def __init__(self, props: FigureProperties) -> None:
        self._props = props
        self.fig = plt.figure(figsize=(15, 10))
        self.ax = self.fig.add_axes((0.11, 0.1, 0.8, 0.8))

    def plot_trajectory_track(
        self,
        ax: FigureAxesController,
        parcel_point_segments: np.ndarray,
        parcel_levels: np.ndarray,
    ) -> None:
        ax.plot_trajectory_line(parcel_point_segments, parcel_levels)
        ax.plot_colorbar(is_auto_ticks=cbar_auto_ticks)
        ax.set_cbar_label()
