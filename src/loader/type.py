from typing import NamedTuple

import numpy as np


class TrackedParcels(NamedTuple):
    lons: np.ndarray
    lats: np.ndarray
    var_values: np.ndarray
