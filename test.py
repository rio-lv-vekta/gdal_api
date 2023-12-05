import os
import subprocess
from osgeo import gdal

def check_georeferencing(geotiff_path):
    dataset = gdal.Open(geotiff_path)
    if dataset is None:
        print(f"Failed to open file: {geotiff_path}")
        return False
    geotransform = dataset.GetGeoTransform()
    if geotransform is None or geotransform == (0,1,0,0,0,1):
        print("Geotransform is missing or incorrect.")
        return False
    return True

print("Commencing Test =============================================================")

geotiff_path = "/app/inputs/test.tif"
output_path = "/app/outputs"

# Check for georeferencing
if not check_georeferencing(geotiff_path):
    print("The provided GeoTIFF lacks proper georeferencing. Aborting.")
    exit()

# Reproject GeoTIFF to Web Mercator (EPSG:3857)
print("Reprojecting GeoTIFF to Web Mercator (EPSG:3857)")
reprojected_path = geotiff_path.replace('.tif', '_3857.tif')
subprocess.run(['gdalwarp', '-t_srs', 'EPSG:3857', geotiff_path, reprojected_path])
geotiff_path = reprojected_path

# Prepare gdal2tiles command
gdal2tiles_command = f"gdal2tiles.py {geotiff_path} {output_path}"

# Run gdal2tiles.py
print("Executing command:", gdal2tiles_command)
os.system(gdal2tiles_command)
