#************************************************ Code Number 5 ********************************************************
#==========================================Multi Bit Flip - TRANSIENT - lcAssertive==================================
import os
import sys
import optparse
import numpy
from sumolib import checkBinary # Check fore the binary in environ vars
import traci
import math
import random
from datetime import datetime, date, time
import struct

# we need to import some python modules from the $SUMO_HOME/tools directory=============================================
if 'SUMO_HOME' in os.environ:
    tools=os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable  'SUMO_HOME'")
#=====================================================Golden Run =======================================================
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


# ==================================Functions to choose random bits and check for repetablity===========================
def randomnumbers():  # 2 random number picker function
    numbers = random.sample(range(64), 2)
    return numbers
# ===========================Convert float to binary and reverse =======================================================
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
# Lists for record some data============================================================================================
lcModel = []
valueL = []
Number = []
jj = []
IDlist = []
sumo_retrieve = []
infinityNum=0
state_list = []
Flipped_list=[]
kkk = 0 # Number of experiment (ID)
for j in numpy.arange(11.0, 21.0, 0.5): # Loop for fault injection TIME interval =======================================
    jjj= round(j, 3)
    kk = 0
    randomList = []
    for i in range(0, 100, 1):  # in choosing number be careful bc the entire possibility is "(total - (repettive numbers like 11 22)) / 2
        XX = randomnumbers()
        if XX not in randomList:
            randomList.append(XX)
            randomList.append(XX[::-1])
        elif XX in randomList:
            # XX = randomnumbers()
            while XX in randomList:
                XX = randomnumbers()
            randomList.append(XX)
            randomList.append(XX[::-1])
        print("\n\n", "XX= ", XX)
        #===============
        jj.append(jjj)
        print("iteration Number = ", jjj, "_", i)
        kk += 1  #counts the step of experiment
        kkk += 1
        print("Experiment ID: ", kkk, "\n")
        Number.append(kk)
        IDlist.append(kkk)
        # ========================================================Bit flip =============================================
        vb= float(default_value[0])
        #print("default = ", vb)
        v = float2bin(vb)
        print("binary format of default= ", v)
        vv = list(v)
        Flipped_list.append(XX)
        for h in XX:
            if int(v[h]) == 1:
                vv[h] = '0'
            #print("I'm one")
            else:
                vv[h] = '1'
            #print("I'm zero")
        vvv = "".join(vv)
        print("binaryAfterBitFlip = ", vvv)
        value =bin2float(vvv)# original
        print("value= ", value)
        if abs(value) == math.inf or str(value) =='nan':   # if the value be infinity it consider as 99e+1000 since sumo not accept inf
            infinityNum+=1
            value=float(default_value[0])
            state_list.append("crash")
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

                if step == round(j, 3) * 10:
                     traci.vehicle.setParameter('5', "laneChangeModel.lcAssertive", str(value))
                if step == (round(j, 3) * 10) + 1:
                     traci.vehicle.setParameter('5', "laneChangeModel.lcAssertive", default_value[0])
                if step == (round(j, 3) * 10) + 3:
                    xc = traci.vehicle.getParameter('5', "laneChangeModel.lcAssertive")
                    sumo_retrieve.append(xc)
                    print("retrieved value = ", xc, type(xc), "\n=====================================================")
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
                         "--tripinfo-output","output/--ID ={: }  t ={:.2f} tripinfo.xml".format(kkk, jjj),
                         "--fcd-output", "output/--ID ={: }  t ={:.2f} fcd.xml".format(kkk, jjj),
                         "--netstate-dump", "output/--ID ={: }  t ={:.2f} Dump.xml".format(kkk, jjj),
                         "--full-output", "output/--ID ={: }  t ={:.2f} Full.xml".format(kkk, jjj),
                         "--amitran-output", "output/--D ={: }  t ={:.2f} Trajectory.xml".format(kkk, jjj),
                         "--lanechange-output", "output/--D ={: }  t ={:.2f} lanechange.xml".format(kkk, jjj),
                         "--error-log", "output/--D ={: }  t ={:.2f} Error.xml".format(kkk, jjj)
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
                'Flipped bits': Flipped_list,
                'state of execution': state_list
                }
        )
# Extracting the current Time ==========================================================================================
now = datetime.now()
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df.to_csv("Experiment_Info_{}.csv".format(current_time))



print("Current Time =", now)
print('infinityNum= ', infinityNum)

