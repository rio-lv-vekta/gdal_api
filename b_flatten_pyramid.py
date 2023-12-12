import os
import shutil

def consolidate_tiles(input_dir, output_dir):
    print("Flattening Pyramid")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for z_dir in os.listdir(input_dir):
        z_path = os.path.join(input_dir, z_dir)
        if os.path.isdir(z_path):
            max_y = 2 ** int(z_dir) - 1  # Calculate max y value for this zoom level
            for x_dir in os.listdir(z_path):
                x_path = os.path.join(z_path, x_dir)
                if os.path.isdir(x_path):
                    for y_file in os.listdir(x_path):
                        old_tile_path = os.path.join(x_path, y_file)
                        # Extract y from the tile filename (assuming format 'y.png')
                        y, _ = os.path.splitext(y_file)
                        inverted_y = max_y - int(y)  # Invert y coordinate
                        new_tile_name = f"tile_{z_dir}_{x_dir}_{inverted_y}.png"
                        print(new_tile_name)
                        new_tile_path = os.path.join(output_dir, new_tile_name)
                        shutil.move(old_tile_path, new_tile_path)

# Specify your input and output directories
input_tiles_dir = "/app/outputs"  # Directory where gdal2tiles.py outputs the tiles
consolidated_tiles_dir = "/app/flat_outputs"  # Directory for the consolidated tiles

consolidate_tiles(input_tiles_dir, consolidated_tiles_dir)
