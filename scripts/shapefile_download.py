# Downloading the data using modified code described in Python_PreReq_Notebook from the tutorial notebooks.
from urllib.request import urlretrieve
import os
import zipfile

# Mixed results with the following two lines, think its a linux vs windows thing
# output_relative_dir = '../../data/'
output_relative_dir = 'data/'

# check if it exists as it makedir will raise an error if it does exist
if not os.path.exists(output_relative_dir):
    os.makedirs(output_relative_dir)
    for sub_dir in ['landing', 'raw', 'curated', 'development']:
            if not os.path.exists(output_relative_dir  + sub_dir):
                os.makedirs(output_relative_dir + sub_dir)

# this is the URL template as of 09/2024
SHAPEFILE_URL = "https://data.gov.au/data/dataset/af33dd8c-0534-4e18-9245-fc64440f742e/resource/0a9f2827-49e9-4390-9ba4-89329736b16b/download/gda2020.zip"

# data output directory is `data/tlc_data/`
shapefile_output = output_relative_dir + 'landing/GDA2020.zip'

print(f"Downloading shapefile to {shapefile_output}")

urlretrieve(SHAPEFILE_URL, shapefile_output)

# Unzip the file

print(f"Unzipping {shapefile_output}")

with zipfile.ZipFile(shapefile_output, 'r') as zip_ref:
    zip_ref.extractall(output_relative_dir + 'landing/')

print(f"Deleting {shapefile_output}...")
os.remove(shapefile_output)

print(f"Download and zip completed at: {output_relative_dir + 'landing/GDA2020/'}")