from typing import NamedTuple

import numpy as np


class TrackedParcel(NamedTuple):
    lon: np.ndarray
    lat: np.ndarray
    var_value: np.ndarray
