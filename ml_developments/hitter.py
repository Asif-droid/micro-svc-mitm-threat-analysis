import requests
import time
import random
from datetime import datetime

# Config
URL = "http://127.0.0.1/app2"  # Change this
OUTPUT_FILE = "clean_response_times_burst_500.log"
MIN_DELAY = 1    # seconds
MAX_DELAY = 3    # seconds
NUM_REQUESTS = 500  # How many requests to send

def log_response(response_time, status_code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp}, {response_time:.3f} sec, Status: {status_code}\n"
    with open(OUTPUT_FILE, "a") as f:
        f.write(log_line)
    print(log_line, end="")

def main():
    for i in range(NUM_REQUESTS):
        # delay = random.uniform(MIN_DELAY, MAX_DELAY)
        # print(f"Sleeping for {delay:.2f} seconds before request {i+1}...")
        # time.sleep(delay)

        start_time = time.time()
        try:
            r = requests.get(URL)
            elapsed = time.time() - start_time
            log_response(elapsed, r.status_code)
        except requests.RequestException as e:
            elapsed = time.time() - start_time
            log_response(elapsed, f"Error: {e}")

if __name__ == "__main__":
    main()
