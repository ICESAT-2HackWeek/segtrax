# Test Trajectory class

import datetime as dt

from trajectory import Trajectory

def main():
    """Initialize a list of trajectory objects"""
    
    segments = [
        {'segID': 0,
         'length': 25.,
         'year': 2019, 
         'month': 6, 
         'day': 17, 
         'hour': 12, 
         'minutes': 1, 
         'seconds': 30, 
         'latitude': 40., 
         'longitude': -100., 
         'freeboard': 1.4,
         },
        {'segID': 1, 
         'length': 30., 
         'year': 2019, 
         'month': 6, 
         'day': 17, 
         'hour': 12, 
         'minutes': 2, 
         'seconds': 35, 
         'latitude': 40.5, 
         'longitude': -100.6, 
         'freeboard': 1.2,
         },
        {'segID': 2, 
         'length': 17., 
         'year': 2019, 
         'month': 6, 
         'day': 17, 
         'hour': 13, 
         'minutes': 2, 
         'seconds': 35, 
         'latitude': 45, 
         'longitude': -101, 
         'freeboard': 2.1,
         }
    ]
    
    trajectory_list = [Trajectory(seg['segID'],
                                  seg['length'],
                                  dt.datetime(seg['year'], seg['month'], seg['day'], seg['hour'], seg['minutes'], seg['seconds']),
                                  seg['latitude'],
                                  seg['longitude'],
                                  seg['freeboard']) for seg in segments]
    
    for t in trajectory_list:
        print (t)
        
        
if __name__ == "__main__":
    main()
    
                

