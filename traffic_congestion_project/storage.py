"""SQLite persistence and CSV export for traffic observations."""
import sqlite3
from pathlib import Path
import pandas as pd

from config import DATA_DIR, DB_PATH, CSV_PATH

COLUMNS = [
    "timestamp_utc", "location_id", "location_name", "latitude", "longitude",
    "current_speed_kmph", "free_flow_speed_kmph", "current_travel_time_sec",
    "free_flow_travel_time_sec", "confidence", "road_closure",
    "speed_ratio", "congestion_index", "congestion_class", "functional_road_class"
]

def initialize_database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS traffic_observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                location_id TEXT NOT NULL,
                location_name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                current_speed_kmph REAL,
                free_flow_speed_kmph REAL,
                current_travel_time_sec REAL,
                free_flow_travel_time_sec REAL,
                confidence REAL,
                road_closure INTEGER,
                speed_ratio REAL,
                congestion_index REAL,
                congestion_class TEXT,
                functional_road_class TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_traffic_time_location
            ON traffic_observations(timestamp_utc, location_id)
        """)
        conn.commit()

def insert_observation(record):
    initialize_database()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO traffic_observations (
                timestamp_utc, location_id, location_name, latitude, longitude,
                current_speed_kmph, free_flow_speed_kmph, current_travel_time_sec,
                free_flow_travel_time_sec, confidence, road_closure,
                speed_ratio, congestion_index, congestion_class, functional_road_class
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(record.get(col) for col in COLUMNS))
        conn.commit()

def load_observations():
    initialize_database()
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT " + ", ".join(COLUMNS) + " FROM traffic_observations ORDER BY timestamp_utc",
            conn
        )
    if not df.empty:
        df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True, errors="coerce")
        df["road_closure"] = df["road_closure"].astype("boolean")
    return df

def export_csv():
    df = load_observations()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False)
    return CSV_PATH
