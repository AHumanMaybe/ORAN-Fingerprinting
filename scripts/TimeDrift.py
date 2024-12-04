import uhd #should be installed when done through the C api thing
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

# the goal for this script is to get the current time on the connected B210 USRP devices
# and calculate the time drift from the reference synchronization signal/time on the Octoclock

# if current iter doesn't work try using the Kalman Filter (boo...)


def get_data(iterations):
    # Initialize the USRP
    usrp = uhd.usrp.MultiUSRP("serial=327125E")
    usrp1 = uhd.usrp.MultiUSRP("serial=33559CF")
    usrp2 = uhd.usrp.MultiUSRP("serial=329089E")

    # Set up the reference and PPS sources
    # usrp.set_clock_source("external")  # Use the 10 MHz clock
    # usrp.set_time_source("external")   # Use the PPS signal
    # usrp1.set_clock_source("external") 
    # usrp1.set_time_source("external") 
    # usrp2.set_clock_source("external") 
    # usrp2.set_time_source("external")   

    last_real_time = None
    last_time = None
    last_time1 = None
    last_time2 = None



    with open('drift_data_NS.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Real_Difference' , 'Drift_327125E', 'Drift_33559CF', 'Drift_329089E']) 

        while iterations > 0:
            time_now = usrp.get_time_now()
            now_seconds = time_now.get_real_secs()

            time_now1 = usrp1.get_time_now()
            now_seconds1 = time_now1.get_real_secs()

            time_now2 = usrp2.get_time_now()
            now_seconds2 = time_now2.get_real_secs()

            if last_time is not None:
                time_diff = now_seconds - last_time
                time_diff1 = now_seconds1 - last_time1
                time_diff2 = now_seconds2 - last_time2

                found_diff = time_diff - 1 # expected change in time is 1 sec (Pulse Per SECOND)
                found_diff1 = time_diff1 - 1
                found_diff2 = time_diff2 - 1
                
                print(f"Current Drift (327125E): {str(found_diff)} Current Drift (33559CF): {str(found_diff1)} Current Drift (329089E): {str(found_diff2)}")

                writer.writerow([time.time(), time.time()-last_real_time, found_diff, found_diff1, found_diff2])
            else: 
                print("No Last time yet")

            last_real_time = time.time()
            last_time = now_seconds
            last_time1 = now_seconds1
            last_time2 = now_seconds2

            iterations -= 1

            time.sleep(1)


# Ideally for this function after synchronizing the clocks of the USRPs (can be confirmed through TX/RX or w/above)
# Disconnect the Octoclock (leaving the USRPs without a syncrhonization signal)
# Hopefully, this will show the unique changes in the internal oscillators (clocks) of each USRP since they no longer can rely on the OctoClock PPS
# run first tests at higher iterations (arbitrarily set to limit spamming data collection and collects once per second) since idk how long it will take for drift to occur
def get_drift(iterations):
    usrp = uhd.usrp.MultiUSRP("serial=327125E")
    usrp1 = uhd.usrp.MultiUSRP("serial=33559CF")
    usrp2 = uhd.usrp.MultiUSRP("serial=329089E")
    
    with open('RealDrift.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time' , 'Time_327125E', 'Time_33559CF', 'Time_329089E'])

        while iterations > 0:
            time_now = usrp.get_time_now()
            now_seconds = time_now.get_real_secs()

            time_now1 = usrp1.get_time_now()
            now_seconds1 = time_now1.get_real_secs()

            time_now2 = usrp2.get_time_now()
            now_seconds2 = time_now2.get_real_secs()
            print("Crunching numbers omnomnom\n")

            writer.writerow([time.time(), now_seconds, now_seconds1, now_seconds2])

            iterations -= 1
            time.sleep(1)



get_data(iterations=100) # run for 1000 seconds

# After the loop, read the drift data from the CSV file and plot it
data = pd.read_csv('drift_data_NS.csv')

# Clean up column names (strip any extra spaces)
data.columns = data.columns.str.strip()

# Check the column names
print("Columns in CSV:", data.columns)

# Plot the drift over time
plt.figure(figsize=(10, 6))
plt.plot(data['Time'].to_numpy(), data['Drift_327125E'].to_numpy(), label='Drift 327125E')
plt.plot(data['Time'].to_numpy(), data['Drift_33559CF'].to_numpy(), label='Drift 33559CF')
plt.plot(data['Time'].to_numpy(), data['Drift_329089E'].to_numpy(), label='Drift 329089E')
# plt.plot(data['Time'].to_numpy(), data['Real_Difference'].to_numpy(), label='Real Time Difference')

plt.xlabel('Time (s)')
plt.ylabel('Time Drift (s)')
plt.title('Time Drift of USRP Devices')
plt.legend()
plt.grid(True)
plt.show()
