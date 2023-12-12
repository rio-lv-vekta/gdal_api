import os
import concurrent.futures
from google.cloud import storage
from threading import Lock

class ProgressTracker:
    def __init__(self, total_files):
        self.total_files = total_files
        self.uploaded_files = 0
        self.lock = Lock()

    def update(self, message):
        with self.lock:
            self.uploaded_files += 1
            print(f"{message} - {self.uploaded_files}/{self.total_files}")

def upload_file_to_gcs(bucket_name, source_folder, destination_folder, filename, progress_tracker):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    local_path = os.path.join(source_folder, filename)
    blob_path = os.path.join(destination_folder, filename)
    blob = bucket.blob(blob_path)

    blob.upload_from_filename(local_path)
    progress_tracker.update(f"{filename} uploaded to {blob_path}")

def upload_images_to_gcs(bucket_name, source_folder, destination_folder):
    print("=================Starting Parallel Upload=================")

    image_extensions = ['.tif', '.png', '.jpeg', '.jpg']
    image_files = [f for f in os.listdir(source_folder) if os.path.splitext(f)[1].lower() in image_extensions]

    progress_tracker = ProgressTracker(len(image_files))

    # Using ThreadPoolExecutor to upload files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(upload_file_to_gcs, bucket_name, source_folder, destination_folder, file, progress_tracker) for file in image_files]
        concurrent.futures.wait(futures)

# Usage
bucket_name = 'vekta_pyramids'
source_folder = 'flat_outputs'
destination_folder = 'marks_suggested_data_1'

upload_images_to_gcs(bucket_name, source_folder, destination_folder)
