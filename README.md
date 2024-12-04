# Fingerprinting Timing of ORAN devices

- First, utilizing ettus research's octoclock (the not G model), start with the steps on [this page for the library installation](https://files.ettus.com/manual/page_install.html) then the ones outlined in ettus' "Enabling Ethernet Connectivity on Octoclock and Octoclock-G" page linked [here](https://kb.ettus.com/Enabling_Ethernet_Connectivity_on_Octoclock_and_Octoclock-G).
  - Note: One issue that occured for me when working through the above steps was receiving an output in avrdude saying something about the process failing and lfuses being changed (I have no idea what that means) but there is a line on the page that says "If all three LEDs in the left column on the front panel are lit, then the bootloader was successfully loaded onto the device" which comes from [this page](https://files.ettus.com/manual/page_octoclock.html). For me I ran the avrdude command a good bit of times and got scared when I got the "not successful" output and couldn't find a fix, after proceeding as though it did succeed -> it just worked, maybe this process had already been done on the device, maybe I have no idea what im doing? But it worked...
 - Next, after this is set up and connectivity is confirmed between the host PC and Octoclock, the octoclockScript.cpp can be used to confirm the UHD api is also working and connects accurately with the octoclock.
 - Currently, I'm looking at connecting the octoclock with what I believe will be USRP B210 devices to begin working on synchronization? I'm not entirely sure. Whatever steps are next most likely will rely on the usage of the GNURadio software, [here is a relevant page](https://wiki.gnuradio.org/index.php?title=B200-B205mini_FM_Receiver). I'm assuming right now that here is where I'll be connecting the relevant devices we want to collect timing fingerprints on and I'll need to set up a synchronized environment for accurate collection that can be recorded and observed through GNURadio.
 - After coming back the next week, we set up 2 USRP B210s on and Octoclock-G and used a 3rd B210, also connected to the octoclock, as a transmitter using wireless antenna
 - This data was then captured and saved using GNURadio


# Update 12/4/24
- After confirming device synchronization between 3 B210 USRPs through the Octoclock I moved forward with working on getting and fingerprinting the timing data
- Currently using TimeDrift.py to look at the difference in recorded time change vs actual
- Next I'm thinking to look at disconnectin the Octoclock Synchronization and running a get_cur_time() function on each USRP on loop to see how they drift apart from each other
- Current data showing the time difference is in the two csv files where one is Synchronized using the OctoClock and the other is running the same code but with the OctoClock disconneced
- Even here there are noticeable time differences between each USRP which varies in such a way that indicates it likely can be fingerprinted to uniquely identify each device
