break_detector - Monte Carlo simulation of Accelerated Life Testing (ALT)

break_detector is a simple command-line Python model of the life and death of a part undergoing ALT and an idea I had a while back on an easy way to detect failures.  For more background check the docs folder, but in a nutshell the idea is to mount simple resistors on several different parts undergoing ALT, wire them up in parallel, and monitor the resulting network's electrical resistance.  Choosing good initial resistors for each strand will result in a unique resistance measurement depending on which strands are broken and which are intact, which means that you can back out when each strand ultimately broke.

break_detector has been tested under Python 2.7 on Windows 7 x64 and on OS X Lion.  How fast or slow it runs depends on your computer of course but for comparison a five-sensor network with a 15 cycle mean time to failure takes around 2 minutes to complete 100,000 simulations on my recent vintage notebook; and about half that under PyPy 1.5.0a0.

Chris Coughlin
July 27 2011