# segtrax

## Team
- Andy Barrett,
- Walt Meier,
- Dave Babb,
- Ian Baxter,
- Sanggyun Lee,
- Brendan West

## The Problem
Sea ice is both in motion and evolves through time.  Ice floes sampled by ICESat-2, and therefore, freeboard segments will not be fixed in space.  #segtrax will develop a tool that generates trajectories of freeboard segments using ice motion data - initially from NSIDC but other motion data could be used.    An additional utility would be to evolve ice thickness using a simple freezing degree day ice growth model.

## Data
- ATL10 - sea ice freeboard product
- NSIDC sea ice motion vectors (https://nsidc.org/data/nsidc-0116)
- ERA-Interim daily 2 m air temperatures (https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era-interim)

## Methods and Tools
- h5py
- xarray

## Workflow

`import whiteboard`
![outline]IMG_9510.jpg
