#!/usr/bin/env python

import os
import boto3
import time
from multiprocessing.pool import ThreadPool

BASE_PATH = '/var/lib/odoo/filestore'

BUCKET = 'odoo-stateless'
ENDPOINT = 'https://minio.voltrans.dev'
AWS_ACCESS_KEY = '90JpFO2mjk6dIY5G'
AWS_ACCESS_SECRET = 'vIjXntneXTQ5vi54wqQVGJUyND998iSA'
PROCESSES = 500


def get_filenames(local_directory):
    filenames = []
    # enumerate local files recursively
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            # construct the full local path
            local_path = os.path.join(root, filename)

            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join('', relative_path)

            filenames.append([filename, local_path, s3_path])
    return filenames


def sync_minIO(filenames):
    content_type = 'text/html'
    if filenames[0].endswith('.json'):
        content_type = 'application/json'

    # config files
    ExtraArgs = {
        'ACL': 'public-read',
        'ContentType': content_type,
    }
    client.upload_file(filenames[1], BUCKET, filenames[2], ExtraArgs=ExtraArgs)
    print(f"Upload {filenames[2]} successful!")


def main():
    filenames = get_filenames(BASE_PATH)
    pool = ThreadPool(processes=PROCESSES)
    pool.map(sync_minIO, filenames)


if __name__ == '__main__':
    session = boto3.Session()
    client = session.client(
        's3',
        endpoint_url=ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_ACCESS_SECRET,
    )
    t = time.time()
    main()
    print(f"Syncing finished in: ", time.time() - t)
