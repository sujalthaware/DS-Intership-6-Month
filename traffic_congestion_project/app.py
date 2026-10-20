"""Streamlit dashboard for live traffic monitoring and congestion modeling."""
import os
import joblib
from datetime import timezone

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from config import ROAD_POINTS, CSV_PATH, MODEL_PATH
from storage import load_observations, export_csv
from traffic_collector import collect_once
from train_model import train_and_evaluate, predict_next

load_dotenv()
st.set_page_config(page_title="Traffic Congestion Lab", page_icon="🚦", layout="wide")

st.title("🚦 Traffic Congestion Monitoring & Prediction")
st.caption("Live traffic flow • Historical observations • Machine-learning experiment")

with st.sidebar:
    st.header("Controls")
    st.write("**Configured road points**")
    for point in ROAD_POINTS:
        st.caption(f'{point["name"]} ({point["latitude"]:.4f}, {point["longitude"]:.4f})')
    st.info("The API returns the road segment closest to each configured coordinate. Edit config.py to add or change points.")
    if st.button("Fetch live traffic now", type="primary", use_container_width=True):
        with st.spinner("Requesting live traffic data..."):
            try:
                outcomes = collect_once()
                for item in outcomes:
                    if item["status"] == "success":
                        st.success(f'{item["location"]}: {item["message"]}')
                    else:
                        st.error(f'{item["location"]}: {item["message"]}')
            except Exception as exc:
                st.error(str(exc))
    if st.button("Train / evaluate model", use_container_width=True):
        with st.spinner("Training on collected historical observations..."):
            result = train_and_evaluate()
        if result.get("trained"):
            st.success(result["message"])
        else:
            st.warning(result["message"])

    if st.button("Refresh dashboard", use_container_width=True):
        st.rerun()

df = load_observations()

if df.empty:
    st.warning("No observations collected yet. Add a valid API key to .env, then click **Fetch live traffic now**.")
    st.markdown("""
    **Quick start**
    1. Copy `.env.example` to `.env`.
    2. Add your own TomTom API key.
    3. Run the app with `python -m streamlit run app.py`.
    4. Click **Fetch live traffic now** to save your first observation.
    """)
    st.stop()

latest = df.sort_values("timestamp_utc").groupby("location_id").tail(1)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Road points", int(latest["location_id"].nunique()))
c2.metric("Observations stored", int(len(df)))
c3.metric("Latest mean speed", f'{latest["current_speed_kmph"].mean():.1f} km/h')
c4.metric("Mean congestion index", f'{latest["congestion_index"].mean():.1f}/100')

st.subheader("Latest observed traffic")
display_cols = [
    "timestamp_utc", "location_name", "current_speed_kmph",
    "free_flow_speed_kmph", "congestion_index", "congestion_class",
    "confidence", "road_closure"
]
st.dataframe(latest[display_cols].sort_values("location_name"), use_container_width=True, hide_index=True)

st.caption("Congestion index = 100 × (1 − current speed / free-flow speed), clipped to 0–100. This is a simple indicator, not an official traffic severity score.")

left, right = st.columns(2)
with left:
    st.subheader("Current speed vs free-flow speed")
    speed_long = latest.melt(
        id_vars=["location_name"],
        value_vars=["current_speed_kmph", "free_flow_speed_kmph"],
        var_name="speed_type", value_name="speed_kmph"
    )
    fig = px.bar(speed_long, x="location_name", y="speed_kmph", color="speed_type", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Congestion index by road point")
    fig = px.bar(latest, x="location_name", y="congestion_index", color="congestion_class",
                 hover_data=["current_speed_kmph", "free_flow_speed_kmph"])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Historical trend")
locations = sorted(df["location_name"].dropna().unique().tolist())
selected = st.multiselect("Choose road points", locations, default=locations)
trend = df[df["location_name"].isin(selected)].sort_values("timestamp_utc")
if not trend.empty:
    fig = px.line(trend, x="timestamp_utc", y="current_speed_kmph", color="location_name",
                  markers=True, labels={"timestamp_utc": "Timestamp (UTC)", "current_speed_kmph": "Speed (km/h)"})
    st.plotly_chart(fig, use_container_width=True)
    fig = px.line(trend, x="timestamp_utc", y="congestion_index", color="location_name", markers=True,
                  labels={"timestamp_utc": "Timestamp (UTC)", "congestion_index": "Congestion index"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Choose at least one road point to view trends.")

st.subheader("Machine-learning model")
if MODEL_PATH.exists():
    try:
        saved_bundle = joblib.load(MODEL_PATH)
        result = saved_bundle.get("metrics", {})
        if result:
            st.warning("These are the metrics saved during the last training run. They describe a chronological holdout, not a guarantee of future performance.")
            m1, m2, m3 = st.columns(3)
            m1.metric("Accuracy", f'{result["accuracy"]:.1%}')
            m2.metric("Balanced accuracy", f'{result["balanced_accuracy"]:.1%}')
            m3.metric("Weighted F1", f'{result["weighted_f1"]:.3f}')
            st.caption(result["evaluation"])
            st.write("Confusion matrix labels:", ", ".join(result["labels"]))
            st.dataframe(pd.DataFrame(result["confusion_matrix"], index=result["labels"], columns=result["labels"]),
                         use_container_width=True)
        else:
            st.info("Saved model has no evaluation metrics. Train it again.")
    except Exception as exc:
        st.warning(f"Could not load saved model metrics: {exc}")
else:
    st.info("The model has not been trained yet. Collect observations over time, then click **Train / evaluate model**. The project intentionally does not fabricate model metrics.")

predictions, prediction_error = predict_next(df)
if predictions is not None:
    st.subheader("Next-observation class estimate")
    st.caption("This estimates the class at the next collected observation for each location. It is not a fixed-horizon forecast.")
    st.dataframe(predictions, use_container_width=True, hide_index=True)
elif prediction_error:
    st.caption(prediction_error)

st.subheader("Raw historical data")
with st.expander("Show stored observations"):
    st.dataframe(df.sort_values("timestamp_utc", ascending=False), use_container_width=True, hide_index=True)

csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("Download historical CSV", data=csv_bytes, file_name="traffic_history.csv", mime="text/csv")

st.caption("Live data is fetched only when you press the collection button. For ongoing history, run the collector repeatedly at a reasonable interval and stay within your API quota.")
