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
    city = "48268 Greven"
    url = (
        "https://nominatim.openstreetmap.org/search?street="
        + urllib.parse.quote(street)
        + "&city="
        + urllib.parse.quote(city)
        + "&format=json"
    )

    response = requests.get(url).json()
    if response:
        thing = list(response).pop(0)
        return thing["lat"], thing["lon"]
    else:
        return -1, -1


with open(sys.argv[1], encoding="utf-8") as f:
    # data = csv.reader(f, delimiter=";")
    data = csv.DictReader(f, delimiter=",")

    for row in tqdm.tqdm(iter(data)):
        street = "{} {}".format(row["Strasse"].strip(), row["HausNR"].strip())
        lat, lon = find_coordinates(street)

        text = f"{street}<br>{row['welche Angebote '] or 'Trödel'}"

        markers.append(
            {
                "coord": [lat, lon],
                "text": text,
                "address": row["Strasse"].strip() + " " + row["HausNR"].strip(),
            }
        )

print(json.dumps(markers))
