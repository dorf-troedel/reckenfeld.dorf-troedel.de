#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 Paul Schaefer <paul@realcyber.de>
#
# Distributed under terms of the All rights reserved license.

"""

"""

import csv
import sys

import urllib.parse
import json

import tqdm

import requests

markers = []

def find_coordinates(street):
    city = '48268 Greven'
    url = 'https://nominatim.openstreetmap.org/search?street=' + urllib.parse.quote(street) + '&city=' + urllib.parse.quote(city) + '&format=json'

    response = requests.get(url).json()
    if response:
        thing = list(response).pop(0)
        return thing['lat'], thing['lon']
    else:
        return -1, -1

with open(sys.argv[1], encoding='utf-8') as f:
    data = csv.reader(f, delimiter=";")

    for row in tqdm.tqdm(iter(data)):
        street = '{} {}'.format(row[1].strip(), row[2].strip())
        lat, lon = find_coordinates(street)

        text = f'{row[4]}<br>{street}'
        if row[3]:
            text += f'<br>{row[3]}'

        markers.append({
            'coord': [lat, lon],
            'text': '{}<br>{}'.format(row[4], street),
            'address': row[1] + ' ' + row[2]
        })

print(json.dumps(markers))
