from datetime import datetime

from constant.variables import Variable

# < base result data >
### directory containing .asc files of trajectory result
TRAJECTORY_RESULTS_DIR = "path/to/trajectory/result/dir"
WRFOUT_PATH = "path/to/wrfout/file"


# <trajectory properties>
### backward or forward
TRAJECTORY_TYPE = "backward"

### trajectory period
### Set former period earlier than latter period regardless of whether backward or forward trajectory.
FORMER_PERIOD_HOUR = datetime(2023, 8, 21, 9, 0)
LATTER_PERIOD_HOUR = datetime(2023, 8, 21, 21, 0)

### parcel displayment
PARCEL_LAT_BOTTOM, PARCEL_LAT_TOP = 33.3, 33.8
PARCEL_LON_LEFT, PARCEL_LON_RIGHT = 130.0, 130.6
HEIGHT_KM = 0.5


# < plot configuration >
### variable to be plotted
VARIABLE = Variable.QV
UNIT_LABEL = "[g/kg]"

### color bar
COLORBAR_MAX = 20
COLORBAR_MIN = 0
COLOR_MAP_NAME = "jet"

### whether to plot elevation with contour
plot_elevation_contour = True
plot_contour_label = False

### figure range
LAT_BOTTOM, LAT_TOP = 32, 35
LON_LEFT, LON_RIGHT = 129, 132
is_deg_min_format = False
LAT_TICKS_INTERVAL = 1
LON_TICKS_INTERVAL = 1
