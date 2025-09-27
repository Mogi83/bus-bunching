import pandas as pd

def detect_bunching(event_log, threshold=3):
    # magic number (3) is representative of a bus being 3 minutes apart
    # in arrival time

    df = pd.DataFrame(event_log)

    arrived_df = df[df["event"] == "arrived"]
    bunching_events = []

    for stop in arrived_df["stop"].unique():
        stop_df = arrived_df[arrived_df["stop"] == stop]
        stop_df = stop_df.sort_values(by="time")

        for i in range(len(stop_df) - 1):
            bus_a = stop_df.iloc[i]
            bus_b = stop_df.iloc[i + 1]

            if bus_b["time"] - bus_a["time"] <= threshold:
                bunching_events.append({
                    "stop": stop,
                    "buses": [bus_a["bus_id"], bus_b["bus_id"]],
                    "delta_t": bus_b["time"] - bus_a["time"] 
                })
    
    print(pd.DataFrame(bunching_events))
