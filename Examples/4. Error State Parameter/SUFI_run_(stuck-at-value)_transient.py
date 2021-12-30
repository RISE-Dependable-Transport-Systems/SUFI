##############################################################################################
# **************         Error-state: Stuck-at-value - Transient                **************
##############################################################################################
import os, sys
import traci
from datetime import datetime, date, time
import pandas as pd
import numpy
import random
# Setting environment variable SUMO_HOME
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
##############################################################################################
# ****************          Function for Golden Run and Output Log                ************
##############################################################################################
def SUFI_golden_run():
    # sumoCmd: select run mode (sumo or sumo-gui), choose sumocfg file to be run, and define output files
    sumoCmd = ["sumo", "-c", "SumoRun.config.sumocfg",
               "--tripinfo-output", "outputG/--Golden Run_tripinfo.xml",
               "--fcd-output", "outputG/--Golden run_fcd.xml",
               "--netstate-dump", "outputG/--Golden Run_Dump.xml",
               "--full-output", "outputG/--Golden Run_Full.xml",
               "--amitran-output", "outputG/--Golden Run_Trajectory.xml",
               "--lanechange-output", "outputG/--Golden Run_lanechange.xml",
               "--error-log", "outputG/--Golden Run_Error.xml"
               ]
    print("SUFI Experiment Run is in Progress ...\n\n")
    traci.start(sumoCmd)
    time_step = 0
    # Run the simulation until all vehicles have arrived
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if time_step == 100:  # 100 refers to time 10s in the simulation
            default_value_Error_state = traci.vehicle.getParameter('5', 'device.driverstate.errorState')
        time_step += 1
    traci.close()
    return default_value_Error_state
##############################################################################################
# ****************       Function for Fault Injection Run and Output Log          ************
##############################################################################################
def SUFI_fault_injection_run(Initation_time, Target_vehicle, Target_parameter, Target_value):
    sumoCmd = ["sumo", "-c", "SumoRun.config.sumocfg",
             "--tripinfo-output","output/--Nr ={: }  t ={:.2f}  lc ={:.2f} tripinfo.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--fcd-output", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} fcd.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--netstate-dump", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} Dump.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--full-output", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} Full.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--amitran-output", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} Trajectory.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--lanechange-output", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} lanechange.xml".format(Ex_Nr, Injection_time, Injected_value),
             "--error-log", "output/--Nr ={: }  t ={:.2f}  lc ={:.2f} Error.xml".format(Ex_Nr, Injection_time, Injected_value)
               ]
    print("SUFI Experiment Run is in Progress ...\n\n")
    traci.start(sumoCmd)
    time_step = 0
    CarList = traci.vehicle.getIDList()
    # Run the simulation until all vehicles have arrived
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if time_step == Initation_time:
            traci.vehicle.setParameter(Target_vehicle, Target_parameter, Target_value)
        if time_step == Initation_time + 1: # this is for Transient faults (after one time_step backs to default)
            traci.vehicle.setParameter(Target_vehicle, Target_parameter, Default_value)
        time_step += 1
    traci.close()
##############################################################################################
# *************        Function for Fault Injection Campaign Data Log          ***************
##############################################################################################
def SUFI_compaign_data_log():
    # Record data in a csv file
    df = pd.DataFrame(
        {
            'Ex Number': LIST_Ex_Nr,
            'Injection_time': LIST_Injection_time,
            'Step_number': LIST_Step_number,
            'Injected_value': LIST_Injected_value,
            'Run_status': LIST_Run_status
        }
    )
    # Current Time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H.%M.%S")
    df.to_csv("Fault Injection Campaign Log _{}.csv".format(current_time))
    print("Current Time =", now)
##############################################################################################
# *************                 Fault Injection Campaign Setup                 ***************
##############################################################################################
# Lists for log fault injection campaign data
LIST_Ex_Nr = []
LIST_Injection_time = []
LIST_Injected_value = []
LIST_Step_number = []
LIST_Run_status = []
Ex_Nr = 0 # Number of experiment (Nr)
# run golden experiment:
Default_value = SUFI_golden_run()
# Value selection for fault injection and experiment run
for t in numpy.arange(11.0, 21.0, 0.5): # Loop for fault injection TIME interval
    Injection_time = round(t, 3)
    Step_number = 0 # Counts the step of the experiment
    Error_state = 0.0 # Reaction Time
    for i in range(100): # Loop to define how many times to select a random value for each Initiation_time
        LIST_Injection_time.append(Injection_time)
        print("\n\n", "Iteration Number:  Injection_time _ step = ", Injection_time, "_", i)
        Step_number += 1
        LIST_Step_number.append(Step_number)
        Ex_Nr += 1
        LIST_Ex_Nr.append(Ex_Nr)
        print("Ex Number = ", Ex_Nr)
        Error_state += 1 # Values for the OverTakeRight parameter
        value = round(Error_state, 3)
        LIST_Injected_value.append(value)
        print("Selected faulty value = ", value, "\n =====================================")
        Injected_value = value
        # run fault injection experiment:
        Initation_time = Injection_time * 10   # 10 is multiplied because of time_step (in sumoconfig we set it to 0.1)
        Target_vehicle = '5'
        Target_parameter = "device.driverstate.errorState"
        Target_value = str(Injected_value)
        try:
            SUFI_fault_injection_run(Initation_time, Target_vehicle, Target_parameter, Target_value)
            LIST_Run_status.append('Successful')
        except Exception as err:
            print("Something went wrong")
            traci.close(False)
            LIST_Run_status.append('Failed')

# Log the fault injection campaign data
SUFI_compaign_data_log()




