"""Project settings and editable road observation points.

The default point is an approximate central Nagpur coordinate, not a guarantee
that the nearest road is the road you want to monitor. Update/add points using
coordinates from a map and verify the road returned by the API.
"""
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
MODEL_DIR = PROJECT_DIR / "models"
DB_PATH = DATA_DIR / "traffic_history.db"
CSV_PATH = DATA_DIR / "traffic_history.csv"
MODEL_PATH = MODEL_DIR / "next_observation_model.joblib"

# Add more road points to monitor more locations. Coordinates are latitude, longitude.
# The API returns the road segment closest to each point.
ROAD_POINTS = [
    {
        "location_id": "nagpur_central_sample",
        "name": "Nagpur central sample point",
        "latitude": 21.1458,
        "longitude": 79.0882,
    },
]
