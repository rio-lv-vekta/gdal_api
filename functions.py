import subprocess
import os
import shutil

def generate_tiles(geotiff_filename, output_folder, default_srs='EPSG:4326', default_ullr=None):
    try:
        input_path = os.path.join('inputs', geotiff_filename)
        georef_path = os.path.join('inputs', 'georef_' + geotiff_filename)
        output_path = os.path.join('outputs', output_folder)

        if not os.path.exists(input_path):
            print(f"Error: File {input_path} not found.")
            return

        if default_ullr:
            # Georeference the image
            subprocess.run(['gdal2tiles.py', '-p', 'raster', input_path, output_path], check=True)

            input_path = georef_path  # Update input path to georeferenced image

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Generate tiles
        subprocess.run(['gdal2tiles.py', input_path, output_path], check=True)
        print("Tiles generated successfully.")
        
        # Example usage
        flatten_pyramid('outputs/test_tiles', 'flattened_tiles')
        
        return "Tiles generated successfully."

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)

# Example usage

def flatten_pyramid(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpeg'):  # Assuming tile image formats
                # Extract tile coordinates from path
                path_parts = root.split(os.sep)
                z, x = path_parts[-2], path_parts[-1]
                y = file.split('.')[0]

                new_filename = f"tile_{z}_{x}_{y}.png"  # Change the extension if necessary
                shutil.move(os.path.join(root, file), os.path.join(output_folder, new_filename))



def clear_output_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Loop through each item in the folder
    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)

        # Check if the item is a file or folder
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


