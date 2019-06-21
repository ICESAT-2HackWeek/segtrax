# Utilities for segtrax
import pyproj
import numpy as np
import scipy.interpolate as scinterp

def interp_uv(x, y, u, v, xi, yi):
    """Interpolates gridded (u, v) ice motion vectors to a set of points
    
    x - 1D or 2D array of x-coordinates
    y - 1D or 2D array of y-coordinates
    u - 2D array of u velocities
    v - 2D array of v velocities
    xi - 1D array-like of x-coords to interpolate to
    yi - 1D array-like of y-coords to interpolate to
    """
    # Set NaN to -99.99 in u and v arrays
    # - probably not the best approach but it will work for now
    um = np.where(~np.isnan(u), u, -99.9)
    vm = np.where(~np.isnan(v), v, -99.9)
    
    fu = scinterp.interp2d(x, y, um, kind='linear')
    fv = scinterp.interp2d(x, y, vm, kind='linear')
    
    ui = np.array([fu(x_i, y_i) for x_i, y_i in zip(xi, yi)])
    vi = np.array([fv(x_i, y_i) for x_i, y_i in zip(xi, yi)])
    
    return ui.flatten(), vi.flatten()
    
    
def transform_coord(from_epsg, to_epsg, x, y):
    """Transform coordinates from proj1 to proj2 (EPSG num).
    
    from_epsg - EPSG code for from_proj
    to_epsg - EPSG code for to_proj
    x - x-coordinate to convert
    y - y-coordinate to convert
    
    Useful EPSG:
    4326 - WGS84
    3408 - EASE North (https://spatialreference.org/ref/epsg/3408/)
    """
    
    # Set full EPSG projection strings
    from_proj = pyproj.Proj("+init=EPSG:"+str(from_epsg))
    to_proj = pyproj.Proj("+init=EPSG:"+str(to_epsg))
    
    # Convert coordinates
    return pyproj.transform(from_proj, to_proj, x, y)


def convert_julian(JD, ASTYPE=None, FORMAT='dict'):
    #-- convert to array if only a single value was imported
    # Written and provided by Tyler Sutterley
    
	if (np.ndim(JD) == 0):
		JD = np.array([JD])
		SINGLE_VALUE = True
	else:
		SINGLE_VALUE = False

	JDO = np.floor(JD + 0.5)
	C = np.zeros_like(JD)
	#-- calculate C for dates before and after the switch to Gregorian
	IGREG = 2299161.0
	ind1, = np.nonzero(JDO < IGREG)
	C[ind1] = JDO[ind1] + 1524.0
	ind2, = np.nonzero(JDO >= IGREG)
	B = np.floor((JDO[ind2] - 1867216.25)/36524.25)
	C[ind2] = JDO[ind2] + B - np.floor(B/4.0) + 1525.0
	#-- calculate coefficients for date conversion
	D = np.floor((C - 122.1)/365.25)
	E = np.floor((365.0 * D) + np.floor(D/4.0))
	F = np.floor((C - E)/30.6001)
	#-- calculate day, month, year and hour
	DAY = np.floor(C - E + 0.5) - np.floor(30.6001*F)
	MONTH = F - 1.0 - 12.0*np.floor(F/14.0)
	YEAR = D - 4715.0 - np.floor((7.0+MONTH)/10.0)
	HOUR = np.floor(24.0*(JD + 0.5 - JDO))
	#-- calculate minute and second
	G = (JD + 0.5 - JDO) - HOUR/24.0
	MINUTE = np.floor(G*1440.0)
	SECOND = (G - MINUTE/1440.0) * 86400.0

	#-- convert all variables to output type (from float)
	if ASTYPE is not None:
		YEAR = YEAR.astype(ASTYPE)
		MONTH = MONTH.astype(ASTYPE)
		DAY = DAY.astype(ASTYPE)
		HOUR = HOUR.astype(ASTYPE)
		MINUTE = MINUTE.astype(ASTYPE)
		SECOND = SECOND.astype(ASTYPE)

	#-- if only a single value was imported initially: remove singleton dims
	if SINGLE_VALUE:
		YEAR = YEAR.item(0)
		MONTH = MONTH.item(0)
		DAY = DAY.item(0)
		HOUR = HOUR.item(0)
		MINUTE = MINUTE.item(0)
		SECOND = SECOND.item(0)

	#-- return date variables in output format (default python dictionary)
	if (FORMAT == 'dict'):
		return dict(year=YEAR, month=MONTH, day=DAY,
			hour=HOUR, minute=MINUTE, second=SECOND)
	elif (FORMAT == 'tuple'):
		return (YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)
	elif (FORMAT == 'zip'):
		return zip(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND)


def convert_GPS_time(GPS_Time, OFFSET=0.0):
    """
    convert_GPS_time.py (10/2017)
    Return the calendar date and time for given GPS time.
    Written by Tyler Sutterley
    Based on Tiffany Summerscales's PHP conversion algorithm
        https://www.andrews.edu/~tzs/timeconv/timealgorithm.html
    INPUTS:
        GPS_Time: GPS time (standard = seconds since January 6, 1980 at 00:00)
    OUTPUTS:
        month: Number of the desired month (1 = January, ..., 12 = December).
        day: Number of day of the month.
        year: Number of the desired year.
        hour: hour of the day
        minute: minute of the hour
        second: second (and fractions of a second) of the minute.
    OPTIONS:
        OFFSET: number of seconds to offset each GPS time
    PYTHON DEPENDENCIES:
        numpy: Scientific Computing Tools For Python (http://www.numpy.org)
    PROGRAM DEPENDENCIES:
        convert_julian.py: convert Julian dates into calendar dates
    UPDATE HISTORY:
        Updated 10/2017: added leap second from midnight 2016-12-31
        Written 04/2016
    """

    #-- PURPOSE: convert from GPS time to calendar dates

    #-- convert from standard GPS time to UNIX time accounting for leap seconds
    #-- and adding the specified offset to GPS_Time
    UNIX_Time = convert_GPS_to_UNIX(np.array(GPS_Time) + OFFSET)
    #-- calculate Julian date from UNIX time and convert into calendar dates
    #-- UNIX time: seconds from 1970-01-01 00:00:00 UTC
    julian_date = (UNIX_Time/86400.0) + 2440587.500000
    cal_date = convert_julian(julian_date)
    #-- include UNIX times in output
    cal_date['UNIX'] = UNIX_Time
    #-- return the calendar dates and UNIX time

    return cal_date

def convert_GPS_to_UNIX(GPS_Time):
    # Taken from Alek Petty tutorial
    
    #-- PURPOSE: Convert GPS Time to UNIX Time
	#-- convert GPS_Time to UNIX without taking into account leap seconds
	#-- (UNIX epoch: Jan 1, 1970 00:00:00, GPS epoch: Jan 6, 1980 00:00:00)
	UNIX_Time = GPS_Time + 315964800
	#-- number of leap seconds prior to GPS_Time
	n_leaps = count_leaps(GPS_Time)
	UNIX_Time -= n_leaps
	#-- check if GPS Time is leap second
	Flag = is_leap(GPS_Time)
	if Flag.any():
		#-- for leap seconds: add a half second offset
		indices, = np.nonzero(Flag)
		UNIX_Time[indices] += 0.5
	return UNIX_Time

def get_leaps():
    #-- PURPOSE: Define GPS leap seconds
    # Written and provided by Tyler Sutterley
    
	leaps = [46828800, 78364801, 109900802, 173059203, 252028804, 315187205,
		346723206, 393984007, 425520008, 457056009, 504489610, 551750411,
		599184012, 820108813, 914803214, 1025136015, 1119744016, 1167264017]
	return leaps


def is_leap(GPS_Time):
    #-- PURPOSE: Test to see if any GPS seconds are leap seconds
    # Written and provided by Tyler Sutterley
    
	leaps = get_leaps()
	Flag = np.zeros_like(GPS_Time, dtype=np.bool)
	for leap in leaps:
		count = np.count_nonzero(np.floor(GPS_Time) == leap)
		if (count > 0):
			indices, = np.nonzero(np.floor(GPS_Time) == leap)
			Flag[indices] = True
	return Flag


def count_leaps(GPS_Time):
    #-- PURPOSE: Count number of leap seconds that have passed for each GPS time
    # Written and provided by Tyler Sutterley
	leaps = get_leaps()
	#-- number of leap seconds prior to GPS_Time
	n_leaps = np.zeros_like(GPS_Time, dtype=np.uint)
	for i,leap in enumerate(leaps):
		count = np.count_nonzero(GPS_Time >= leap)
		if (count > 0):
			indices, = np.nonzero(GPS_Time >= leap)
			# print(indices)
			# pdb.set_trace()
			n_leaps[indices] += 1
	return n_leaps