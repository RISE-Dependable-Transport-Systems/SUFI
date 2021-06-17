#************************************************ Code Number 1 ********************************************************
#==========================================CHANGE OF VALUE - INTERMITTENT===============================================
import os
import sys
import optparse
import numpy
from sumolib import checkBinary # Check fore the binary in environ vars
import traci
import random
from datetime import datetime, date, time

# we need to import some python modules from the $SUMO_HOME/tools directory ============================================
'''
if 'SUMO_HOME' in os.environ:
    tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable  'SUMO_HOME'")
'''
# Lists for record some data============================================================================================
valueL = []
Number = []
jj = []
IDlist = []
kkk = 0 # Number of experiment (ID)
for j in numpy.arange(11.0, 21.0, 0.5): # Loop for fault injection TIME interval =======================================
    jjj= round(j, 3)
    kk = 0
    es = 0.0 # "ERROR  STATE" Note: The number zero not included in injection
    for i in range(100): # Loop to define how many times to inject fault for each time step ================================
        jj.append(jjj)
        print("\n\n", "Iteration Number = ", jjj, "_", i)
        kk += 1  #counts the step of experiment
        kkk += 1
        print("Ex ID = ", kkk)
        #errorr = [-10, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 40, 45, 50, 100]
        Number.append(kk)
        IDlist.append(kkk)
        def get_options():
            opt_parser = optparse.OptionParser()
            opt_parser.add_option("--nogui", action="store_true",
                                  default=False, help="run the commandline version of sumo ")
            options, args = opt_parser.parse_args()
            return options
        es += 1   # Value increase for target faulty parameter===================================
        value = round(es, 3)
        valueL.append(value)
        print("Error State = ", value, "\n ==========================================================================")
        k = value

        # contains TraCI control loop===================================================================================
        def run():
            step = 0
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                # print(step)

                CarList=traci.vehicle.getIDList()
                if step == (round(j, 3) * 10):
                    traci.vehicle.setParameter('5', 'device.driverstate.errorState', str(es))
                if step == (round(j, 3) * 10) +1:
                    traci.vehicle.setParameter('5', 'device.driverstate.errorState', str(0.0))
                if step >= ((round(j, 3) *10)-1)  and ('5' in CarList):
                    ES = traci.vehicle.getParameter('5', 'device.driverstate.errorState')
                    print("Time_step= ", step, "  Retrieved ES = ", ES)
                step += 1
            traci.close()
            sys.stdout.flush()

        # main entry point==============================================================================================
        if __name__ == "__main__":
            options = get_options()

            # check binary
            if options.nogui:
                sumoBinary = checkBinary('sumo')
            else:
                sumoBinary = checkBinary('sumo-gui')

            # traci starts sumo as aa subprocess and then this script connects and runs==AND OUTPUT DEFINITION =========
            traci.start(["sumo", "-c", "SumoRun.config.sumocfg",
                         "--fcd-output", "output/--ID ={: }  t ={:.2f}  es ={:.2f} fcd.xml".format(kkk, jjj, k),
                         "--error-log", "output/--D ={: }  t ={:.2f}  noise ={:.2f} Error.xml".format(kkk, jjj, k)
                         ])
            run()
# Record data in csv file===============================================================================================
import pandas as pd
df = pd.DataFrame(
        {
                'Ex ID' : IDlist,
                'time': jj,
                'Number': Number,
                'value (Error State)': valueL
                }
        )
# Extracting the current Time ==========================================================================================
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df.to_csv("table_{}.csv".format(current_time))



print("Current Time =", now)
#print(pwd)
