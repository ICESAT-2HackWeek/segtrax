# Reader function definition

import numpy as np
import h5py
import pandas as pd
import utils as ut

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
    
    freeboard=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_height'][:]

    freeboard_confidence=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_confidence'][:]
    freeboard_quality=f1[beam]['freeboard_beam_segment']['beam_freeboard']['beam_fb_quality_flag'][:]
    
    lons=f1[beam]['freeboard_beam_segment']['beam_freeboard']['longitude'][:]
    lats=f1[beam]['freeboard_beam_segment']['beam_freeboard']['latitude'][:]
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
    
    return lons, lats, dFtimepd, freeboard