## Grib Inventory v.0.0.2

GribInventory is a tool that piggybacks off of the range headers supported by http://nomads.ncep.noaa.gov/.
This allows a user to quickly pull subsets grib2 files of global/regional/expiremental model data hosted by NOAA. 
  
Compatible with Python3 only atm.  

Currently supported models:  
gfs - (GFS 0.25 degree)  
nam - (NAM model 12km resolution)  
nam4km - (NAM model 4km resolution)  

* Currently defaults to pulling the latest model run.

### Setup

```bash
python setup.py install
gribinventory
```

Usage - CLI:
```bash
gribinventory 
  --model [model name]  
  --savepath [output file path]  
  --variables [Comma seperated list of desired grib2 variables - ie. LEVEL:VARIABLE,LEVEL:VARIABLE,...]  
  --fhours [Comma seperated list of forecast hours-steps to download]  
  -t [Option: enable Multi-threading.]  
```
See: http://www.nco.ncep.noaa.gov/pmb/products/ for available levels:variables for each model.

Example:
```bash
gribinventory  
  --model nam4km  
  --savepath gribdata/nam4km  
  --variables "DPT:850 mb,ABSV:500 mb"  
  --fhours 01,02,03,15,21   
  -t  
```

Usage - Module:
```bash
from gribinventory.base import GribInventory

grbs = GribInventory(model, vars, fhours, enableThreading=True)

grbs.download()


```
See: http://www.nco.ncep.noaa.gov/pmb/products/ for available levels:variables for each model.

Example:
```bash
from gribinventory.base import GribInventory

grbs = GribInventory('NAM4km', ['DPT:850 mb', 'ABSV:500 mb'], ['01','02','03','15','21'], enableThreading=True)

grbs.download()

```
