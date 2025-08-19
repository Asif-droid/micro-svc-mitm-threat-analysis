import pandas as pd
import numpy as np
from collections import Counter

# Load the data
# df = pd.read_csv("log.csv", names=["timestamp", "latency_sec", "status"], skiprows=0)


FILE_NAME = "clean_response_times.log"
df = pd.read_csv(FILE_NAME, 
                 header=None, 
                 names=['timestamp', 'latency_sec', 'status'],
                 sep=', ')
# Remove text like "Status: "
df['status'] = df['status'].astype(str).str.replace("Status:", "").str.strip()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

latencies = df['latency_sec'].astype(float).values
timestamps = df['timestamp'].values

print(f"Total requests: {len(latencies)}")
# print(latencies[:5])  # Show first 5 latencies for verification
print(FILE_NAME)
# 1. Percentiles
p50 = np.percentile(latencies, 50)
p90 = np.percentile(latencies, 90)
p99 = np.percentile(latencies, 99)

# 2. IQR & MAD
q75, q25 = np.percentile(latencies, [75, 25])
iqr = q75 - q25
mad = np.median(np.abs(latencies - np.median(latencies)))

# 3. Tail index (Hill estimator)
lat_sorted = np.sort(latencies)
k = max(5, int(0.1 * len(lat_sorted)))  # top 10%
tail = lat_sorted[-k:]
hill_est = np.mean(np.log(tail / tail[0]))

# 4. Burstiness (Fano factor)
inter_arrivals = np.diff(df['timestamp'].astype(np.int64) / 1e9)  # seconds
fano = np.var(inter_arrivals) / np.mean(inter_arrivals) if np.mean(inter_arrivals) > 0 else 0

# std
std_pop = np.std(latencies)

# Standard deviation (sample, n-1 denominator)
std_sample = np.std(latencies, ddof=1)

# 5. Status mix
status_counts = Counter(df['status'])
status_mix = {code: count / len(df) for code, count in status_counts.items()}

print({
    "p50": p50,
    "p90": p90,
    "p99": p99,
    "IQR": iqr,
    "MAD": mad,
    "TailIndex": hill_est,
    "Fano": fano,
    "Population std:": std_pop,
    "Sample std:": std_sample,
    "StatusMix": status_mix
})
