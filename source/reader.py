# Reader function definition

import numpy as np
import h5py
import pandas as pd
import utilities as ut
import xarray as xr

def getATL10(fileT, beam='gt1r'):
    """ ATL10 reader
    Adapted from code written by Alek Petty, June 2018 (alek.a.petty@nasa.gov)

    Args:
        fileT (str): File path of the ATL10 dataset
        beamStr (str): ICESat-2 beam (the number is the pair, r=strong, l=weak) - default is the gt1r beam

    returns:
        lists containing each quantity of interest

    """

    print('ATL10 file:', fileT)
    
    f1 = h5py.File(fileT, 'r')
    
    # Freeboard data
    freeboard=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_height'][:]

    freeboard_confidence=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_confidence'][:]
    freeboard_quality=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_quality_flag'][:]
    
    # Lat and lon data
    lons=f1[beam]['freeboard_beam_segment']['beam_freeboard']['longitude'][:]
    lats=f1[beam]['freeboard_beam_segment']['beam_freeboard']['latitude'][:]
    
    # Date and time data
    deltaTime=f1[beam]['freeboard_beam_segment']['beam_freeboard']['delta_time'][:]-f1[beam]['freeboard_beam_segment']['beam_freeboard']['delta_time'][0]
    
    # #Add this value to delta time parameters to compute full gps_seconds
    atlas_epoch=f1['/ancillary_data/atlas_sdp_gps_epoch'][:] 
    
    # Conversion of delta_time to a calendar date
    temp = ut.convert_GPS_time(atlas_epoch[0] + deltaTime, OFFSET=0.0)
    
    year = temp['year'][:].astype('int')
    month = temp['month'][:].astype('int')
    day = temp['day'][:].astype('int')
    hour = temp['hour'][:].astype('int')
    minute = temp['minute'][:].astype('int')
    second = temp['second'][:].astype('int')
    dFtime=pd.DataFrame({'year':year, 'month':month, 'day':day, 
                        'hour':hour, 'minute':minute, 'second':second})
    
    dF = pd.DataFrame({'freeboard':freeboard, 'lon':lons, 'lat':lats, 'delta_time':deltaTime,
                      'year':year, 'month':month, 'day':day})
    
    dFtimepd=pd.to_datetime(dFtime)

    # Segment ID
    segment_id = f1[beam]['freeboard_beam_segment']['beam_freeboard']['height_segment_id'][:]
    
    # Segment length
    segment_length = f1[beam]['freeboard_beam_segment']['beam_freeboard']['seg_dist_x'][:]
    
    return segment_id, segment_length, dFtimepd, lons, lats, freeboard

def getERAI(fname):
    """Function to read ERA-Interim 6-hourly T2M temperature
    
    Input: i, in form ['Year-Month'] for month that you want to read in
    Output: data, T2M for month i
    """
    data = xr.open_mfdataset(fname)
    return data

def daily_means(self):
    """Function to calculate daily means from 6 hourly data from ERA-I t2m data
    Needs to loop because the times are not consistent between months.

    Input: A single month of 6 hourly
    Output: Daily means
    """
    return self.groupby('time.day').mean('time')

def weekly_means(self):
    return self.resample(day='7D').sum('day')

def adjust(files):
    """Loops through ERA-Interim files, calculates, daily means, and concatenates them together
    
    Input: months list 'Year-Month'
    Output: Merged 3D xarray dataset with t2m
    """
    for f in files:
        month = getERAI(f)
        nmonth = len(month.time)
        data = month.isel(time=slice(0,nmonth-1))

        daily = daily_means(data)
        if f == files[0]:
            yrstrt,monstrt,hour = str(data.time.values[0]).split('-')
            print('starting year: ',yrstrt,', starting month: ',monstrt)
            merged = daily
        else:
            merged = xr.concat((merged,daily),'day')
        # problem here with the wrong file being selected if using different input files
        if f == files[2]:
            yrend,monend,hour = str(data.time.values[0]).split('-')
            print('ending year: ',yrend,', ending month: ',monend)

    end_new = str(int(monend)+1)        
    time = np.arange(np.datetime64(str(yrstrt)+'-'+str(monstrt)+'-01'),np.datetime64(str(yrend)+'-'+end_new.zfill(2)))
    merged = merged.assign_coords(day=time)
    
    return merged
