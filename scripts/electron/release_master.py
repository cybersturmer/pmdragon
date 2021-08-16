#!/usr/bin/env python3
import csv
import sys
import json

from pathlib import Path

if __name__ == '__main__':
    assert len(sys.argv) >= 2, 'Please provide required arguments (build_number and release_file)'

    build_number = sys.argv[1]
    releases_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    print(f'Got build number: {build_number}')
    print(f'Got releases file path: {releases_file_path}', end='\r\n\r\n')

    print('Checking if releases file exists...', end='')

    releases_file = Path(releases_file_path)
    if not releases_file.is_file():
        raise Exception('Releases file does not exist')

    print('ok')

    """ 
    Markers to determine platform
    So if we found win32 in version name - we consider version
    to be Windows platform oriented
    """
    markers = {
        'linux': ['linux'],
        'macos': ['darwin', 'mas'],
        'windows': ['win32']
    }

    envs = markers.keys()

    releases_dict = {
        'linux': [],
        'macos': [],
        'windows': []
    }

    # Parsing releases file to create json file with releases
    with open(releases_file_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            version, size, filename = row

            for env in envs:
                if not any([marker in version for marker in markers[env]]):
                    continue

                releases_dict[env].append({
                    'title': version,
                    'filename': filename,
                    'size': size
                })

    result = {
        'version': build_number,
        'releases': releases_dict
    }

    with open(output_file_path, 'w') as json_file_handler:
        json.dump(
            result,
            json_file_handler,
            sort_keys=True,
            indent=4
        )
