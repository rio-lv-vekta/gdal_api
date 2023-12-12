# Start from the GDAL Alpine image
FROM osgeo/gdal:alpine-normal-3.6.3

# Install Python
RUN apk add --no-cache python3 py3-pip

# add GCP Credentials for local development only
# ENV GOOGLE_APPLICATION_CREDENTIALS=/credentials/service_account_credentials.json

# Set the working directory
WORKDIR /app

# Copy your Flask application code
COPY . /app

# # Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run your app
CMD ["python3", "app.py"]
