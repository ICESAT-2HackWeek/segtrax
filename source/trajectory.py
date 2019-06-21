# Trajectory class definition

import numpy as np

fill_value = np.nan

class Trajectory:
    """Trajectory class to contain segment date, location, freeboard and other data
    
    Attributes
    ----------
    segment_id - unique identifier for segment
    segment_length - length of segment in m
    
    date - list of datetime objects
    latitude - list of latitudes for trajectory
    longitude - list of longitudes for trajectory
    hf - list of daily snow/ice freeboards  
    hice - lst of daily ice thicknesses
    temperature - list of daily 2 m reanalysis air temperatures
    fdd -list of freezing degree days
    hsnow - list of daily snow depths (may not be used - setting to zero)
    """
    
    def __init__(self, segment_id, segment_length, date, latitude, longitude, hf):

        self.segment_id = segment_id
        self.segment_length = segment_length

        self.date = [date]
        self.latitude = [latitude]
        self.longitude = [longitude]
        self.hf = [hf]
        self.hice = []
        self.temperature = []
        self.fdd = []
        self.hsnow = [] 
       

    def __repr__(self):
        return f'Trajectory for segment {self.segment_id} with length {self.segment_length}'

    
    def append(self, date, latitude, longitude, hf):
        """Initializes a trajectory with date, latitude and initial freeboard"""

        self.date.append(date)
        self.latitude.append(latitude)
        self.longitude.append(longitude)
        self.hf.append(hf)
        self.hice.append(fill_value)
        self.temperature.append(fill_value)
        self.fdd.append(fill_value)
        self.hsnow.append(fill_value)
        
    
    def get_coords(self):
        """Returns a tuple of coordinates"""
        return (self.date, self.longitude, self.latitude)
    
        

