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

def process_geotiff(file_path, output_path):
    print("============== COMMENCING GEOTIFF PROCESSING ==================")

    # Check for georeferencing
    if not check_georeferencing(file_path):
        print(f"The provided GeoTIFF {file_path} lacks proper georeferencing. Aborting.")
        return

    # Reproject GeoTIFF to Web Mercator (EPSG:3857)
    print(f"Reprojecting {file_path} to Web Mercator (EPSG:3857)")
    reprojected_path = file_path.replace('.tif', '_3857.tif')
    subprocess.run(['gdalwarp', '-t_srs', 'EPSG:3857', file_path, reprojected_path])

    # Convert the Image to 8-bit with Auto Scaling
    eight_bit_path = reprojected_path.replace('.tif', '_8bit.tif')
    subprocess.run(['gdal_translate', '-ot', 'Byte', '-scale', reprojected_path, eight_bit_path])

    # Update path for gdal2tiles.py
    gdal2tiles_command = f"gdal2tiles.py {eight_bit_path} {output_path}"

    # Run gdal2tiles.py
    print(f"Executing command: {gdal2tiles_command}")
    os.system(gdal2tiles_command)
    
def create_pyramid(input_folder,output_folder):
    # Process each GeoTIFF file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.tif'):
            file_path = os.path.join(input_folder, file_name)
            process_geotiff(file_path, output_folder)

# input_folder = "/app/inputs"
# output_folder = "/app/outputs"

# create_pyramid(input_folder,output_folder)