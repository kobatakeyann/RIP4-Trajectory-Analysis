import numpy as np
import pandas as pd

from constant.analysis_type import TrajectoryAnalysisType
from constant.variables import Variable
from loader.type import TrackedParcel


class TrajectoryResultReader:
    def __init__(self, trajectory_type: TrajectoryAnalysisType) -> None:
        self._trajectory_type = trajectory_type

    def get_parcel_track(
        self, result_filepath: str, variable: Variable
    ) -> TrackedParcel:

        # set order toward trajectory time direction
        array_order = (
            1
            if self._trajectory_type == TrajectoryAnalysisType.FORWARD
            else -1
        )

        df = pd.read_csv(result_filepath, sep=r"\s+", header=0)
        lons = df[Variable.LON.value]

        # get first index of invalid data
        if "*********" in lons:
            lons = np.array(lons[::array_order])
            max_valid_index = np.where(lons == "*********")[0][0]
        else:
            max_valid_index = len(lons)
        df.replace("*********", np.nan, inplace=True)

        # extract valid data
        lons = np.array(
            df[Variable.LON.value][::array_order][:max_valid_index]
        ).astype(float)
        lats = np.array(
            df[Variable.LAT.value][::array_order][:max_valid_index]
        ).astype(float)
        var_values = np.array(
            df[variable.value][::array_order][:max_valid_index]
        ).astype(float)

        return TrackedParcel(
            lon=lons,
            lat=lats,
            var_value=var_values,
        )
