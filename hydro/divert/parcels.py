import json
import os

import shapefile
from django.conf import settings

SHAPEFILE_PATH = os.path.join(
    settings.BASE_DIR, "divert", "data", "parcels", "ca_tulare.shp", "ca_tulare.shp"
)
CACHE_PATH = os.path.join(
    settings.BASE_DIR, "divert", "data", "parcels", "ca_tulare_cache.geojson"
)

# Trimmed subset of the 129 Regrid fields - just enough to identify a parcel on click.
FIELDS = ["parcelnumb", "owner", "address", "city", "state2", "szip", "usedesc", "ll_gisacre"]

COORD_PRECISION = 6


def _round_coords(coords):
    if isinstance(coords[0], (int, float)):
        return [round(c, COORD_PRECISION) for c in coords]
    return [_round_coords(c) for c in coords]


def _build_tulare_geojson():
    reader = shapefile.Reader(SHAPEFILE_PATH)
    features = []

    for shape_record in reader.iterShapeRecords():
        record = shape_record.record.as_dict()
        geometry = shape_record.shape.__geo_interface__
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": geometry["type"],
                    "coordinates": _round_coords(geometry["coordinates"]),
                },
                "properties": {field: record.get(field) for field in FIELDS},
            }
        )

    geojson = {"type": "FeatureCollection", "features": features}

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(geojson, f)

    return geojson


def get_tulare_geojson_bytes():
    if not os.path.exists(CACHE_PATH):
        _build_tulare_geojson()

    with open(CACHE_PATH, "rb") as f:
        return f.read()
