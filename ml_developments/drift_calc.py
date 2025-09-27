import numpy as np
import pandas as pd
import random

# -----------------------------
# Helper functions
# -----------------------------
def parse_log_file(filepath: str) -> pd.DataFrame:
    """Parse a .log file into a DataFrame with timestamp, value, status."""
    data = []
    with open(filepath, "r") as f:
        for line in f:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 3:
                continue
            try:
                ts, val, status = parts
                val = float(val)
                status = int(status.split(":")[1].strip())
                data.append((ts, val, status))
            except Exception:
                continue
    return pd.DataFrame(data, columns=["timestamp", "value", "status"])


def energy_distance_squared(x: np.ndarray, y: np.ndarray) -> float:
    """Compute squared energy distance between two 1D samples."""
    n, m = len(x), len(y)
    if n == 0 or m == 0:
        return np.nan
    cross = np.abs(x.reshape(-1, 1) - y.reshape(1, -1)).sum()
    xx = np.abs(x.reshape(-1, 1) - x.reshape(1, -1)).sum()
    yy = np.abs(y.reshape(-1, 1) - y.reshape(1, -1)).sum()
    return 2 * cross / (n * m) - xx / (n * n) - yy / (m * m)


def permutation_test(x: np.ndarray, y: np.ndarray, n_perms: int = 1000, seed: int = 42) -> float:
    """Permutation test for energy distance."""
    rng = random.Random(seed)
    combined = np.concatenate([x, y])
    n = len(x)
    observed = energy_distance_squared(x, y)
    count = 0
    for _ in range(n_perms):
        rng.shuffle(combined)
        a = combined[:n]
        b = combined[n:]
        stat = energy_distance_squared(a, b)
        if stat >= observed - 1e-12:
            count += 1
    return (count + 1) / (n_perms + 1)


def compute_drift(ref: np.ndarray, test: np.ndarray):
    """Compute energy distance, squared distance, and p-value."""
    d2 = energy_distance_squared(ref, test)
    d = np.sqrt(max(d2, 0.0))
    pval = permutation_test(ref, test)
    return d2, d, pval


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # Replace with your actual .log file path
    filepath_clean = "clean_response_times_500.log"
    filepath_mitm = "mitm_response_times_500.log"

    clean_df = parse_log_file(filepath_clean)
    mitm_df = parse_log_file(filepath_mitm)
    clean_values = clean_df["value"].to_numpy()
    mitm_values = mitm_df["value"].to_numpy()

    # Example: split into first half vs second half
    # mid = len(values) // 2
    # ref, test = values[:mid], values[mid:]
    ref = clean_values
    test = mitm_values

    d2, d, pval = compute_drift(ref, test)

    # print(f"Loaded {len(values)} log entries from {filepath}")
    print(f"Reference window size: {len(ref)}, Test window size: {len(test)}")
    print(f"Energy distance squared: {d2:.6f}")
    print(f"Energy distance (D): {d:.6f}")
    print(f"Permutation test p-value: {pval:.4f}")
