# landsat-pystac
The purpose of the Landsat Pystac package is to easily search the Landsat archives using the SpatioTemporal Asset Catalog (STAC) API. The STAC browser is also available [here](https://landsatlook.usgs.gov/stac-browser).

# Usage

Sample usage below:
```py
from landsatpystac.stac import STACResult
from landsatpystac.search import Search

# Search using default parameters
s = Search(wrs_row='030', wrs_path='042', cloud_cover_max=50)
_, result = s.search()

# Parse search results by loading it into STACResult class
r = STACResult(result)
# Class can be indexed to access search results
# Access S3 download paths of the first item in the search result
r[0].s3_tiff_paths

# In addition we can loop through the class
for scene in r:
    # Loop through the class and print the scene ID of each scene
    print(scene.id)

```


