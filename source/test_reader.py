# Test reader function

from reader import getATL10

def main():
    file = '../data/ATL10_tracks/161185873/processed_ATL10-01_20181106165654_05970101_001_01.h5'

    segment_id, segment_length, date, lons, lats, freeboard = getATL10(file, beam='gt1l')

    print("lons size: {0}".format(len(lons)))
    print("lats size: {0}".format(len(lats)))
    print("time size: {0}".format(len(date)))
    print("freeboard size: {0}".format(len(freeboard)))

if __name__ == "__main__":
    main()