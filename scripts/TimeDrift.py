import uhd #should be installed when done through the C api thing
import time
import matplotlib.pyplot as plt

# the goal for this script is to get the current time on the connected B210 USRP devices
# and calculate the time drift from the reference synchronization signal/time on the Octoclock

# if current iter doesn't work try using the Kalman Filter (boo...)

# Initialize the USRP
usrp = uhd.usrp.MultiUSRP()

# Set up the reference and PPS sources
usrp.set_clock_source("external")  # Use the 10 MHz clock
usrp.set_time_source("external")   # Use the PPS signal

# Allow the system to lock
time.sleep(1)
if not usrp.get_mboard_sensor("ref_locked").to_bool():
    raise RuntimeError("External reference clock not locked!")

# Synchronize USRP time to PPS
usrp.set_time_next_pps(uhd.types.TimeSpec(0.0))
time.sleep(1)  # Wait for the next PPS edge

# Drift measurement
drift_data = []
last_pps_time = None

print("Recording drift data. Press Ctrl+C to stop.")
try:
    while True:
        # Get the current USRP time
        current_pps_time = usrp.get_time_now().get_real_secs()

        if last_pps_time is not None:
            # Calculate the time interval between PPS signals
            measured_interval = current_pps_time - last_pps_time
            # Expected interval is 1 second
            drift = measured_interval - 1.0
            drift_data.append((current_pps_time, drift))
            print(f"Time: {current_pps_time:.6f}, Drift: {drift:.6e} seconds")

        # Update last PPS time
        last_pps_time = current_pps_time
        time.sleep(1)  # Wait for the next PPS signal
except KeyboardInterrupt:
    print("Stopping drift recording...")

# Save the data to a file
with open("oscillator_drift.csv", "w") as f:
    f.write("USRP Time, Drift (s)\n")
    for t, d in drift_data:
        f.write(f"{t:.6f}, {d:.6e}\n")
    print("Drift data saved to 'oscillator_drift.csv'")

# Extract data for plotting
usrp_times = [t for t, d in drift_data]
drifts = [d for t, d in drift_data]

# Plot the oscillator drift
plt.figure(figsize=(10, 6))
plt.plot(usrp_times, drifts, marker="o", linestyle="-", color="b", label="Oscillator Drift")
plt.axhline(0, color="r", linestyle="--", label="Ideal PPS Interval")
plt.title("USRP B210 Oscillator Drift Over Time")
plt.xlabel("USRP Time (s)")
plt.ylabel("Drift from Expected Interval (seconds)")
plt.legend()
plt.grid()
plt.tight_layout()

# Show the plot
plt.show()