"""Optional long-running collector. Use responsibly and respect API quotas."""
import time
from traffic_collector import collect_once

INTERVAL_SECONDS = 300  # 5 minutes; adjust to your provider's terms/quota.

if __name__ == "__main__":
    print(f"Starting collection every {INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            for item in collect_once():
                print(item)
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("Collector stopped.")
