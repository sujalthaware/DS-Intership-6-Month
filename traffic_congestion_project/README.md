# Traffic Congestion Monitoring & Prediction

**Author:** Sujal  
**Level:** Intermediate internship project  
**Stack:** Python, Requests, Pandas, SQLite, Scikit-learn, Plotly, Streamlit

## 1. Problem statement

Traffic conditions change by time and location. This project collects live traffic-flow measurements for selected road points, stores timestamped observations, visualizes current and historical conditions, and experiments with predicting the congestion class at the next collected observation.

It is an educational prototype, not a road-safety system or a guaranteed travel-time forecast.

## 2. Features

- Live traffic-flow requests through TomTom's Flow Segment Data endpoint.
- Configurable latitude/longitude road points in `config.py`.
- SQLite historical storage and CSV export.
- Speed ratio and a transparent 0–100 congestion indicator.
- Streamlit dashboard with latest observations and historical trends.
- Scikit-learn Random Forest classifier with chronological train/test evaluation.
- Accuracy, balanced accuracy, weighted F1, classification report, and confusion matrix.
- Honest guardrails: model training is withheld until enough sequential observations exist.

## 3. Data provider and cost

The default provider is TomTom Traffic Flow Segment Data:
https://docs.tomtom.com/traffic-api/documentation/tomtom-maps/v1/traffic-flow/flow-segment-data

The endpoint requires a valid TomTom API key. TomTom advertises a free monthly allowance for Traffic Flow API Segment Data; quotas, eligibility, terms, and pricing can change, so check the current pricing page before use:
https://docs.tomtom.com/pricing

No API key is bundled in this repository. The project will not fabricate live results if the key is absent or the API fails. If you cannot obtain a key, you can still inspect the code and build the dashboard after importing your own properly licensed traffic dataset, but the live collection button will not work without a provider.

## 4. Installation on Windows / PowerShell

Open PowerShell and move to this folder:

```powershell
cd "D:\sujal\programs\DS-Intership-6-Month\month_2_task_traffic"
```

Create and activate a virtual environment:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.14` is not available, use the Python launcher version installed on your PC. Streamlit currently documents support for recent Python versions; see https://docs.streamlit.io/get-started/installation/command-line.

If PowerShell blocks environment activation, you can skip activation and use the venv's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 5. Configure API key

Copy the example file:

```powershell
Copy-Item .env.example .env
notepad .env
```

Replace the placeholder with your own key:

```text
TOMTOM_API_KEY=your_real_key_here
```

Do not share `.env`, commit it to Git, or paste the key into public screenshots.

## 6. Configure road points

Edit `config.py` and add road points. Each point needs a unique `location_id`, a display `name`, `latitude`, and `longitude`.

The API returns the road segment closest to the selected coordinates. Verify that the selected coordinate maps to the road you intend to monitor. The included Nagpur coordinate is only an approximate sample point, not a verified road-specific sensor.

## 7. Run the dashboard

From the project folder:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`.

Click **Fetch live traffic now** to collect an observation. Repeat later to create historical data. The app stores data in `data/traffic_history.db` and exports `data/traffic_history.csv`.

## 8. Collect data repeatedly

For a manually controlled collection round:

```powershell
python traffic_collector.py
```

For optional automatic collection every five minutes:

```powershell
python collector_loop.py
```

Keep the terminal open while the loop runs. Press `Ctrl+C` to stop. Adjust the interval in `collector_loop.py` to stay within the API's current quotas and terms. Repeated requests consume API quota.

## 9. Train and evaluate

The dashboard's **Train / evaluate model** button runs the model. You can also run:

```powershell
python train_model.py
```

The model sorts records by timestamp, then uses the earliest 80% of transitions for training and the latest 20% for testing.

The target is the next collected congestion class for the same location. It is not a fixed 5-, 15-, or 60-minute forecast; the time between observations depends on how often data is collected.

The training code requires at least 30 sequential transitions and more than one target class. This is only a minimal technical threshold, not a claim that the model is statistically reliable. Prefer many days/weeks of observations across multiple road points and times of day before interpreting metrics.

Metrics:
- **Accuracy:** fraction of correct predictions.
- **Balanced accuracy:** average recall across classes, useful when class counts differ.
- **Weighted F1:** weighted summary of precision and recall.
- **Confusion matrix:** shows which congestion classes are confused.

## 10. How the congestion indicator is defined

`speed_ratio = current_speed / free_flow_speed`

`congestion_index = clip((1 - speed_ratio) * 100, 0, 100)`

Labels use simple thresholds:
- `Low`: speed ratio at least 0.70
- `Moderate`: ratio from 0.40 to below 0.70
- `Heavy`: ratio below 0.40 or a reported road closure

These thresholds are project-defined heuristics, not official classifications from TomTom or a transport authority.

## 11. Project structure

```text
traffic_congestion_project/
├── app.py
├── config.py
├── storage.py
├── traffic_collector.py
├── collector_loop.py
├── train_model.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── data/
└── models/
```

## 12. Limitations and responsible interpretation

- Live collection requires internet access and a valid provider API key.
- Free quota is limited and provider terms may change.
- A coordinate represents the closest available road segment, not necessarily a full road or intersection.
- A single point cannot represent city-wide congestion.
- Sparse history and class imbalance can make model metrics unstable.
- A time-based holdout is more realistic than a random split, but it does not eliminate every source of bias.
- The classifier predicts the next collected class; it is not a validated traffic forecasting service.
- Traffic speed and congestion labels may be noisy, delayed, or unavailable.
- Do not use this prototype for emergency routing, safety-critical decisions, or official traffic control.

## 13. Future improvements

- Add verified road points and more neighborhoods.
- Collect for several weeks and monitor data quality.
- Add lagged traffic features and fixed-horizon targets (for example, 15 minutes) once sampling is consistent.
- Compare a baseline model with Random Forest.
- Add a map view, incident data, and alerting.
- Add automated tests, structured logging, and deployment secrets management.

## Conclusion

This project demonstrates a practical end-to-end workflow: live API collection, data storage, cleaning and feature engineering, time-aware model evaluation, and an interactive dashboard. Its main learning value is the complete workflow and honest evaluation, not an assumed accuracy score.
