import numpy as np
import matplotlib.pyplot as plt
from drift_calc import parse_log_file

# --- Load latencies from log files -----------------------------------------
filepath_clean = "clean_response_times_burst_500.log"
filepath_mitm  = "mitm_response_times_burst_500.log"

clean_df = parse_log_file(filepath_clean)
mitm_df  = parse_log_file(filepath_mitm)

clean_lat = clean_df["value"].to_numpy()
mitm_lat  = mitm_df["value"].to_numpy()



# --- Baseline parameters from clean run ------------------------------------
mu0    = clean_lat.mean()
sigma0 = clean_lat.std(ddof=1)   # sample std with n-1 denominator

# --- CUSUM parameters ------------------------------------------------------
k = 0.5 * sigma0        # reference value (half of expected shift)
h = 18.5 * sigma0        # decision threshold (5-sigma rule of thumb)

# --- One–sided CUSUM (upward) ---------------------------------------------
S = np.zeros_like(mitm_lat)
for i in range(1, len(mitm_lat)):
    S[i] = max(0, S[i-1] + (mitm_lat[i] - mu0 - k))

# --- Two–sided CUSUM (downward) -------------------------------------------
S_minus = np.zeros_like(mitm_lat)
for i in range(1, len(mitm_lat)):
    S_minus[i] = max(0, S_minus[i-1] + (mu0 - mitm_lat[i] - k))

# --- Report all key values -------------------------------------------------
print("=== Baseline parameters from clean run ===")
print(f"Mean (μ0)             : {mu0:.6f} s")
print(f"Std  (σ0)             : {sigma0:.6f} s")
print("=== Chosen CUSUM parameters ===")
print(f"Reference value (k)   : {k:.6f} s")
print(f"Decision threshold (h): {h:.6f} s\n")

print("=== Detection statistics (MITM run) ===")
print(f"Max upward  CUSUM (S+) : {S.max():.6f} s")
print(f"Max downward CUSUM (S-): {S_minus.max():.6f} s")

# --- Plot the upward CUSUM with threshold ---------------------------------
plt.step(range(len(mitm_lat)), S, where='mid', label='CUSUM (upward)')
plt.axhline(h, color='red', linestyle='--', label='threshold h')
plt.xlabel("Observation index")
plt.ylabel("CUSUM statistic")
plt.title("CUSUM test: MITM latencies vs clean baseline")
plt.legend()
plt.tight_layout()
plt.show()

# --- Decision --------------------------------------------------------------
if S.max() > h:
    print("\nResult: Significant upward shift detected (possible MITM).")
else:
    print("\nResult: No significant upward shift detected.")
