"""Fetch one round of live TomTom traffic-flow observations."""
import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from config import ROAD_POINTS
from storage import insert_observation, export_csv, initialize_database

API_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

def congestion_label(speed_ratio, road_closure):
    """Rule-based descriptive label, not a trained-model prediction."""
    if road_closure:
        return "Heavy"
    if speed_ratio is None:
        return "Unknown"
    if speed_ratio < 0.40:
        return "Heavy"
    if speed_ratio < 0.70:
        return "Moderate"
    return "Low"

def fetch_location(point, api_key, timeout=20):
    params = {
        "key": api_key,
        "point": f'{point["latitude"]},{point["longitude"]}',
        "unit": "KMPH",
    }
    response = requests.get(API_URL, params=params, timeout=timeout)
    if response.status_code == 401 or response.status_code == 403:
        raise RuntimeError("API key rejected or not authorized. Check your TomTom key and product access.")
    if response.status_code == 429:
        raise RuntimeError("API request limit reached. Check your provider quota and try later.")
    response.raise_for_status()
    payload = response.json()
    flow = payload.get("flowSegmentData")
    if not isinstance(flow, dict):
        raise RuntimeError("Unexpected API response: flowSegmentData is missing.")

    current_speed = flow.get("currentSpeed")
    free_flow_speed = flow.get("freeFlowSpeed")
    if current_speed is None or free_flow_speed is None:
        raise RuntimeError("API response does not contain currentSpeed/freeFlowSpeed.")

    current_speed = float(current_speed)
    free_flow_speed = float(free_flow_speed)
    speed_ratio = current_speed / free_flow_speed if free_flow_speed > 0 else None
    congestion_index = max(0.0, min(100.0, (1.0 - speed_ratio) * 100)) if speed_ratio is not None else None
    closure = bool(flow.get("roadClosure", False))
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return {
        "timestamp_utc": timestamp,
        "location_id": point["location_id"],
        "location_name": point["name"],
        "latitude": float(point["latitude"]),
        "longitude": float(point["longitude"]),
        "current_speed_kmph": current_speed,
        "free_flow_speed_kmph": free_flow_speed,
        "current_travel_time_sec": flow.get("currentTravelTime"),
        "free_flow_travel_time_sec": flow.get("freeFlowTravelTime"),
        "confidence": flow.get("confidence"),
        "road_closure": int(closure),
        "speed_ratio": speed_ratio,
        "congestion_index": congestion_index,
        "congestion_class": congestion_label(speed_ratio, closure),
        "functional_road_class": flow.get("frc"),
    }

def collect_once():
    load_dotenv()
    api_key = os.getenv("TOMTOM_API_KEY", "").strip()
    if not api_key or api_key == "put_your_api_key_here":
        raise RuntimeError("TOMTOM_API_KEY is missing. Copy .env.example to .env and add your API key.")
    initialize_database()
    outcomes = []
    for point in ROAD_POINTS:
        try:
            record = fetch_location(point, api_key)
            insert_observation(record)
            outcomes.append({"location": point["name"], "status": "success", "message": record["congestion_class"]})
        except Exception as exc:
            outcomes.append({"location": point["name"], "status": "error", "message": str(exc)})
    export_csv()
    return outcomes

if __name__ == "__main__":
    results = collect_once()
    for item in results:
        print(f'{item["location"]}: {item["status"]} - {item["message"]}')
    print("Collection round finished. Check data/traffic_history.csv.")
