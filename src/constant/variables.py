from enum import Enum


class Variable(Enum):
    TIME = "Time(h)"
    LON = "Lon."
    LAT = "Lat."
    HGT = "Hgt.(m)"
    PRES = "Pres.(hPa)"
    W = "W(cm/s)"
    QV = "Qv(g/kg)"
    RH = "RH(%)"
    TH = "TH(K)"
    TC = "TC(C)"
    THV = "THV(K)"
    ETP = "ETP(K)"


VARIABLE_DICTIONARY = {
    "TIME": "time",
    "LON": "longitude",
    "LAT": "latitude",
    "HGT": "height",
    "PRES": "pressure",
    "W": "vertical velocity w",
    "QV": "mixing ratio",
    "RH": "relative humidity",
    "TH": "potential temperature",
    "TC": "temperature",
    "THV": "virtual potential temperature",
    "ETP": "equivalent potential temperature",
}
