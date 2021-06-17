#************************************************ Code Number 1 ********************************************************
#==========================================Bit Flip - TRANSIENT===============================================
import os
import sys
import optparse
import numpy
from sumolib import checkBinary # Check fore the binary in environ vars
import traci
import random
from datetime import datetime, date, time
import struct
import math

# we need to import some python modules from the $SUMO_HOME/tools directory ============================================
if 'SUMO_HOME' in os.environ:
    tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable  'SUMO_HOME'")
#=====================================================Golden Run========================================================
def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo ")
    options, args = opt_parser.parse_args()
    return options
# contains TraCI control loop
default_value = []
def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if step == 100:
            default = traci.vehicle.getParameter('5', "laneChangeModel.lcAssertive")
            default_value.append(default)
            print("parameter at 10 sec = ", default_value)
        step += 1

    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as aa subprocess and then this script connects and runs
    traci.start(["sumo", "-c", "SumoRun.config.sumocfg",
                 "--tripinfo-output", "outputG/--Golden Run_tripinfo.xml",
                 "--fcd-output", "outputG/--Golden run_fcd.xml",
                 "--netstate-dump", "outputG/--Golden Run_Dump.xml",
                 "--full-output", "outputG/--Golden Run_Full.xml",
                 "--amitran-output", "outputG/--Golden Run_Trajectory.xml",
                 "--lanechange-output", "outputG/--Golden Run_lanechange.xml",
                 "--error-log", "outputG/--Golden Run_Error.xml"
                 ])
    run()

# Lists for record some data============================================================================================
valueL = []
Number = []
jj = []
IDlist = []
sumo_retrieve = []
state_list = []
infinityNum = 0
kkk = 0 # Number of experiment (ID)
for j in numpy.arange(11.0, 21.00, 0.5): # Loop for fault injection TIME interval =======================================
    jjj= round(j, 3)
    kk = 0
    for i in range(0, 64, 1): # Loop to define how many times to do bit-flip ===========================================
        jj.append(jjj)
        print("\n\n", "Iteration Number = ", jjj, "_", i)
        kk += 1  #counts the step of experiment
        kkk += 1
        print("Ex ID = ", kkk)
        Number.append(kk)
        IDlist.append(kkk)
        #=================== Convert float to binary and reverse =======================================================
        def bin2float(b):
            ''' Convert binary string to a float.

            Attributes:
                :b: Binary string to transform.
            '''
            h = int(b, 2).to_bytes(8, byteorder="big")
            return struct.unpack('>d', h)[0]
        def float2bin(f):
            ''' Convert float to 64-bit binary string.

            Attributes:
                :f: Float number to transform.
            '''
            [d] = struct.unpack(">Q", struct.pack(">d", f))
            return f'{d:064b}'
        # ========================================================Bit flip =============================================
        print("Default value = ", default_value[0])
        vb= float(default_value[0])  # converts string default value to float
        #print("default = ", vb)
        v = float2bin(vb)    # converts float to Binary format
        #print("binary format of default= ", v)
        vv = list(v) # converts the Binary to a list of strings
        #print("random num = ", i)
        if int(v[i]) == 1:
            vv[i] = '0'
            #print("I'm one")
        else:
            vv[i] = '1'
            #print("I'm zero")
        vvv = "".join(vv) # makes a list
        value =bin2float(vvv)# original
        print("value= ", value)
        if value == math.inf:   # if the value be infinity it consider as "Default" since sumo not accept inf
            infinityNum+=1
            value=float(default_value[0])
            state_list.append("detected")
        else:
            state_list.append("done")
        valueL.append(value)
        print("value2= ", value)
        k = value
        #=======================================Start Simulation =======================================================
        def get_options():
            opt_parser = optparse.OptionParser()
            opt_parser.add_option("--nogui", action="store_true",
                                  default=False, help="run the commandline version of sumo ")
            options, args = opt_parser.parse_args()
            return options
        # contains TraCI control loop===================================================================================
        def run():
            step = 0
            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()
                # print(step)

                if step == round(j, 3) *10:
                    traci.vehicle.setParameter('5', "laneChangeModel.lcAssertive", str(value))
                if step == (round(j, 3) * 10) + 1:
                     traci.vehicle.setParameter('5', "laneChangeModel.lcAssertive", default_value[0])
                if step == (round(j, 3) * 10) + 3:
                    xc = traci.vehicle.getParameter('5', "laneChangeModel.lcAssertive")
                    sumo_retrieve.append(xc)
                    print("parameter = ", xc, type(xc), "\n===========================================================")
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
                         "--tripinfo-output","output/--ID ={: }  t ={:.2f}  lc ={:.2f} tripinfo.xml".format(kkk, jjj, k),
                         "--fcd-output", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} fcd.xml".format(kkk, jjj, k),
                         "--netstate-dump", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} Dump.xml".format(kkk, jjj, k),
                         "--full-output", "output/--ID ={: }  t ={:.2f}  lc ={:.2f} Full.xml".format(kkk, jjj, k),
                         "--amitran-output", "output/--D ={: }  t ={:.2f}  lc ={:.2f} Trajectory.xml".format(kkk, jjj, k),
                         "--lanechange-output", "output/--D ={: }  t ={:.2f}  lc ={:.2f} lanechange.xml".format(kkk, jjj, k),
                         "--error-log", "output/--D ={: }  t ={:.2f}  lc ={:.2f} Error.xml".format(kkk, jjj, k)
                         ])
            run()
# Record data in csv file===============================================================================================
import pandas as pd
df = pd.DataFrame(
        {
                'Ex ID' : IDlist,
                'time': jj,
                'Number': Number,
                'Bit-flip-value (lcAssertive)': valueL,
                'Sumo_retrieve': sumo_retrieve,
                'state of execution': state_list
                }
        )
# Extracting the current Time ==========================================================================================
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df.to_csv("Experiment_Info_{}.csv".format(current_time))



print("Current Time =", now)
#print(pwd)