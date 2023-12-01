import requests
import sys
import boto3
import os
from botocore.config import Config
import time
def get_json_data(url):
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            json_data = response.json()
            
            # Now, you can work with the JSON data as a Python dictionary
            # print(json_data)
            return json_data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_from_s3(files):
    bucket_name = os.getenv('AWS_BUCKET', 'EODATA')
    
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    s3_service_url = os.getenv('AWS__ServiceURL')

    try:
        # Create an S3 client with explicit credentials and service URL
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            endpoint_url=s3_service_url,
            config=Config(retries={'max_attempts': 10, 'mode': 'standard'})
        )
        for file in files:
            directory_path = os.path.dirname(file)
            filename = os.path.basename(file)

            dir_array = directory_path.split('/')
            for i in range(len(dir_array) - 1, -1, -1):
                if dir_array[i].endswith('.SAFE'):
                    # Remove all previous occurrences of the value
                    del dir_array[:i+1]
                    break

            # Create local directories if they don't exist
            local_file = os.path.join(('/').join(dir_array), filename)
            if os.path.dirname(local_file):
                os.makedirs(os.path.dirname(local_file), exist_ok=True)
            print(f'Downloading {file} into {local_file}')
            try:
                s3.download_file(bucket_name, file.replace(f's3://{bucket_name}/', ''), local_file)
            except:
                try:
                    time.sleep(60)
                    s3.download_file(bucket_name, file.replace(f's3://{bucket_name}/', ''), local_file)
                except:
                    try:
                        time.sleep(300)
                        s3.download_file(bucket_name, file.replace(f's3://{bucket_name}/', ''), local_file)
                    except:
                        print(f'File {file} download failed after 3 tries')
        print(f"Files downloaded successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if a URL is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
    else:
        url = sys.argv[1]
        json = get_json_data(url)
        s3links = []
        for k, link in json['assets'].items():
            if link['href'].startswith('s3://'):
                s3links.append(link['href'])
        # print(s3links)
        print(f"Starting download")

        download_from_s3(s3links)