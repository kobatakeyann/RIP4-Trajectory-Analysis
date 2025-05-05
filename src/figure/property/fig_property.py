import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Colormap

from config.configuration import (
    COLOR_MAP_NAME,
    COLORBAR_MAX,
    COLORBAR_MIN,
    LAT_BOTTOM,
    LAT_TOP,
    LON_LEFT,
    LON_RIGHT,
)
from config.constant import (
    CONTOUR_LABEL_INTERVAL,
    ELEVATION_CONTOUR_INTERVAL,
    ELEVATION_MAX,
    ELEVATION_MIN,
    FIGURE_SIZE,
    TRAJECTORY_LINE_WIDTH,
)


class FigureProperties:
    def __init__(self) -> None:
        self.figsize = self._calculate_figsize()
        self.contour_levels = self._get_contour_levels()
        self.clabel_levels = self._get_clabel_levels()
        self.colormap = self._get_color_map()
        self.cbar_max = COLORBAR_MAX
        self.cbar_min = COLORBAR_MIN
        self.line_width = TRAJECTORY_LINE_WIDTH

    def _calculate_figsize(self) -> tuple:
        lat_dif = LAT_TOP - LAT_BOTTOM
        lon_dif = LON_RIGHT - LON_LEFT
        figsize = (
            FIGURE_SIZE,
            FIGURE_SIZE * float(float(lat_dif) / float(lon_dif)),
        )
        return figsize

    def _get_contour_levels(self) -> np.ndarray:
        return np.arange(
            float(ELEVATION_MIN),
            float(ELEVATION_MAX) + 0.000000000000001,
            float(ELEVATION_CONTOUR_INTERVAL),
        )

    def _get_clabel_levels(self) -> np.ndarray:
        return np.arange(
            float(ELEVATION_MIN),
            float(ELEVATION_MAX) + 0.000000000000001,
            float(CONTOUR_LABEL_INTERVAL),
        )

    def _get_color_map(self) -> Colormap:
        return plt.get_cmap(COLOR_MAP_NAME).copy()
