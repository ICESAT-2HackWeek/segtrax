# Utilities for segtrax
import pyproj

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

