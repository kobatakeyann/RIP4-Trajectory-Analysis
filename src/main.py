from figure.maker.horizontal_track import make_horizontal_track_figure
from figure.maker.vertival_track import make_vertical_track_figure


def main():
    # vizualize horizontal parcel track on the map.
    make_horizontal_track_figure()

    # vizualize vertical parcel track on the time-height diagram.
    make_vertical_track_figure()


if __name__ == "__main__":
    main()
