import os
import requests
import shutil
import json

def read_api_keys(file_path):
    with open(file_path, 'r') as file:
        api_keys = json.load(file)
    return api_keys['API_KEYS']

# Function to download and save the file
def download_file(url, filename, output_dir):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    else:
        print(f"Error {response.status_code}: Unable to download {filename}")

# Function to query the API and download all URLs
def download_all_files(application_id, api_key, output_dir):
    object_id = 'object_5'
    base_url = 'https://api.knack.com/v1/objects'
    endpoint = f'/{object_id}/records'

    headers = {
        'Content-Type': 'application/json',
        'X-Knack-Application-Id': application_id,
        'X-Knack-REST-API-Key': api_key
    }

    page = 1
    total_pages = 1

    while page <= total_pages:
        response = requests.get(f'{base_url}{endpoint}?page={page}&rows_per_page=1', headers=headers)

        if response.status_code == 200:
            data = response.json()
            total_pages = data['total_pages']

            for record in data['records']:
                for key, value in record.items():
                    if isinstance(value, dict) and 'url' in value:
                        url = value['url']
                        filename = value['filename']
                        download_file(url, filename, output_dir)

            page += 1
        else:
            print(f"Error {response.status_code}: Unable to fetch page {page}")
            break

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
keys_file = os.path.join(parent_dir, 'Knack API Keys.json')
api_keys = read_api_keys(keys_file)

for api_key_data in api_keys:
    app_name = api_key_data['appName']
    app_id = api_key_data['appId']
    api_key = api_key_data['apiKey']

    output_dir = os.path.join(parent_dir, app_name)
    os.makedirs(output_dir, exist_ok=True)
    download_all_files(app_id, api_key, output_dir)
