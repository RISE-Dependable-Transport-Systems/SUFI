#************************************************ Code Number 1 ********************************************************
#=======================Chain of Faults CHANGE OF VALUE - INTERMITTENT - lcAssertive+ReactionTime=======================
import os
import sys
import optparse
import numpy
from sumolib import checkBinary # Check fore the binary in environ vars
import traci
import random
from datetime import datetime, date, time

# we need to import some python modules from the $SUMO_HOME/tools directory ============================================
if 'SUMO_HOME' in os.environ:
    tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable  'SUMO_HOME'")

# Lists for record some data============================================================================================
valueL = []
value_RT = []
Number = []
Number2 =[]  # number of loop in Reaction Time
jj = []
IDlist = []
kkk = 0 # Number of experiment (ID)
for j in numpy.arange(11.0, 14.5, 0.5): # Loop for fault injection TIME interval =======================================
    jjj= round(j, 3)
    kk = 0
    for i in range(100): # Loop to define how many times to pick random value ==========================================
        value = random.randrange(2, 1001)  # Random number for target faulty parameter==================================
        hh = 0
        for h in numpy.arange(0.2, 5.1, 0.2): # Define interval for Reaction Time parameter
            RT = round(h, 3)
            value_RT.append(RT)
            jj.append(jjj)
            print("\n\n", "Iteration Number = ", jjj, "_", i, "RT= ", RT)
            kk += 1  #counts the step of experiment
            kkk += 1
            hh += 1
            print("Ex ID = ", kkk)
            Number.append(kk)
            IDlist.append(kkk)
            Number2.append(hh)
            valueL.append(value)
            print("LC-Assertive = ", value)
            k = value
            # =======================================SUMO Run ==========================================================
            def get_options():
                opt_parser = optparse.OptionParser()
                opt_parser.add_option("--nogui", action="store_true",
                                      default=False, help="run the commandline version of sumo ")
                options, args = opt_parser.parse_args()
                return options

            # contains TraCI control loop===============================================================================
            def run():
                step = 0
                while traci.simulation.getMinExpectedNumber() > 0:
                    traci.simulationStep()
                    # print(step)

                    if step == round(j, 3) *10:
                        traci.vehicle.setParameter('5', "laneChangeModel.lcAssertive", str(value))
                        traci.vehicle.setParameter('5', 'device.driverstate.maximalReactionTime', str(RT))
                    if step == (round(j, 3) * 10) + 1:
                        RTr = traci.vehicle.getParameter('5', 'device.driverstate.maximalReactionTime')
                        print("Retrieved RT = ", RTr, "\n =============================================================")
                    step += 1
                traci.close()
                sys.stdout.flush()

            # main entry point==========================================================================================
            if __name__ == "__main__":
                options = get_options()

                # check binary
                if options.nogui:
                    sumoBinary = checkBinary('sumo')
                else:
                    sumoBinary = checkBinary('sumo-gui')

                # traci starts sumo as aa subprocess and then this script connects and runs==AND OUTPUT DEFINITION =====
                traci.start(["sumo", "-c", "SumoRun.config.sumocfg",
                             "--tripinfo-output","output/--ID ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} tripinfo.xml".format(kkk, jjj, k, RT),
                             "--fcd-output", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} fcd.xml".format(kkk, jjj, k, RT),
                             "--netstate-dump", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} Dump.xml".format(kkk, jjj, k, RT),
                             "--full-output", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} Full.xml".format(kkk, jjj, k, RT),
                             "--amitran-output", "output/--D ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} Trajectory.xml".format(kkk, jjj, k, RT),
                             "--lanechange-output", "output/--D ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} lanechange.xml".format(kkk, jjj, k, RT),
                             "--error-log", "output/--D ={: }  t ={:.2f}  lc ={:.2f} RT ={:.2f} Error.xml".format(kkk, jjj, k, RT)
                             ])
                run()
# Record data in csv file===============================================================================================
import pandas as pd
df = pd.DataFrame(
        {
                'Ex ID' : IDlist,
                'Time': jj,
                'Number': Number,
                'Number2': Number2,
                'value (lcAssertive)': valueL,
                'value (Reaction Time)': value_RT
                }
        )
# Extracting the current Time ==========================================================================================
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df.to_csv("table_{}.csv".format(current_time))



print("Current Time =", now)
#print(pwd)