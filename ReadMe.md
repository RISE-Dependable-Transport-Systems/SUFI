# **SUFI (SUmo-based Fault Injector)**


SUFI is a sumo-based fault injector tool. The tool combines [SUMO](https://www.eclipse.org/sumo/) and [Python](https://www.python.org/). SUFI uses sumo for mobility simulation, where we define the traffic scenario and vehicle features there. Also, sumo allows us to select the car-following and lane-changing models to model the car behavior during the simulation run, thereby, evaluate these models through the fault and attack injection. Python, on the other hand, allows us to write scripts for different fault models, select fault locations and define fault durations. SUMO and Python are communicating via [TraCI](https://sumo.dlr.de/docs/TraCI.html) with each other when running the experiments.

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/SUFI/blob/master/Documentation/pictures/SUFI.PNG">
</p>
<br/> 
<br/> 


## Simulation Setup

* Install [SUMO 1.6.0](https://sourceforge.net/projects/sumo/files/sumo/version%201.6.0/) (we used this version of SUMO so please note that for the later versions the car behavior might change)
* Install Python 3.7 or later

#### Required Python libraries:
* sumolib
* traci
* pandas
* numpy
* matplotlib

## IMPORTANT NOTES!
1. Before running the experiment make sure that the ".net", ".rou", ".settings", and ".sumocfg" files are in the same directory with the Python run file. Also create two folders with names "output" and "outputG" so some of the output data will be stored in these folders.

2. In the abovementioned version (SUMO 1.6.0) the "perception errors" functionality was not active for the CACC and ACC models, therefore, in order to inject fault
into the "error state" parameter we added this functionality into the source code. But for the later versions we requested the SUMO team to add this funtionality so you might do not need to do that.
