import os
from datetime import datetime

from cmap import Colormap
from constant.analysis_type import TrajectoryAnalysisType
from constant.variables import Variable

# < path configuration >
TRAJ_RESULT_ROOT_DIR = "data/traj_result"

# wrfout specification
WRFOUT_ROOT_DIR = "your/wrfout/holder/path"  # e.g., "/data/wrfout"
WRFOUT_NAME = "your_wrfout_name"

FORMER_DATETIME = datetime(2023, 8, 21, 3, 0)
LATTER_DATETIME = datetime(2023, 8, 21, 14, 30)
TIME_ZONE = "JST"


# RIP4 conversion specification
START_TIME_FOR_CONVERSION = 0  # [min]
END_TIME_FOR_CONVERSION = 1080  # [min]
RIP4_HISTORY_INTERVAL = 10  # [min]

# trajectory calculation period
# Set former period earlier than latter period regardless of whether backward or forward trajectory.
# 0 indicates the start time of wrf simulation.
TRAJECTORY_TYPE = TrajectoryAnalysisType.BACKWARD
FORMER_PERIOD_HOUR = 0
LATTER_PERIOD_HOUR = 11.5
TRAJECTORY_TIME_STEP = 1  # [min]

# parcel location
PARCEL_LAT_BOTTOM, PARCEL_LAT_TOP = 33.2, 33.7
PARCEL_LON_LEFT, PARCEL_LON_RIGHT = 130.2, 130.7
PARCEL_LEVEL_KM = 0.25  # [km]


# <figure properties>
### variable to be plotted
VARIABLE = Variable.TC


# < horizontal plot configuration >
UNIT_LABEL = "[℃]"

### color bar
COLORBAR_MAX = 35
COLORBAR_MIN = 20
COLOR_MAP_NAME = Colormap("jet").to_mpl()


### whether to plot elevation with contour
plot_elevation_contour = True
plot_contour_label = False

### figure range
LAT_BOTTOM, LAT_TOP = 32, 34.5
LON_LEFT, LON_RIGHT = 129.5, 132
is_deg_min_format = True
LAT_TICKS_INTERVAL = 0.5
LON_TICKS_INTERVAL = 0.5

### parcel filtering
filter_parcels_in_rectangle = False
plot_filtering_area = False
FILTERING_AREA_NAME = "hakata"
REC_LON_LEFT, REC_LON_RIGHT = 130.1, 130.9
REC_LAT_BOTTOM, REC_LAT_TOP = 33.72, 33.85
LAT_BOTTOM, LAT_TOP = 33, 34.5
LON_LEFT, LON_RIGHT = 130, 132

### median track
plot_median_track = True
MEDIAN_LINEWIDTH = 3
MEDIAN_LINE_COLOR = "black"
paint_25th_75th_percentile = True
SHADE_25TH_75TH_COLOR = "gray"
SHADE_25TH_75TH_ALPHA = 0.3

# < vertical plot configuration >
LEVEL_MAX = 4000
LEVEL_MIN = 0

TIME_TICKS_FORMAT = "%H:%M"  # %d / %Hh
TIME_TICKS_INTERVAL = 12


# directory containing .asc files of trajectory result
wrfout_path = os.path.join(WRFOUT_ROOT_DIR, WRFOUT_NAME)
TRAJECTORY_RESULTS_DIR = os.path.join(
    TRAJ_RESULT_ROOT_DIR,
    WRFOUT_NAME,
    f"rip_{START_TIME_FOR_CONVERSION}h_to_{END_TIME_FOR_CONVERSION/60:.1f}h_{RIP4_HISTORY_INTERVAL}min_interval",
    TRAJECTORY_TYPE.value,
    f"{FORMER_PERIOD_HOUR}h_to_{LATTER_PERIOD_HOUR}h_{TRAJECTORY_TIME_STEP}min_step",
    f"{PARCEL_LEVEL_KM}km_{PARCEL_LON_LEFT}-{PARCEL_LON_RIGHT}-{PARCEL_LAT_BOTTOM}-{PARCEL_LAT_TOP}",
    "trajectory_result",
)
