import xml.etree.ElementTree as ET
import re
import glob
import csv
from datetime import datetime, date, time
import pandas as pd

file_list = glob.glob("output/*fcd.xml*") #Reads all the xml files with extension of fcd.xml and makes a list of their names
print(len(file_list))

# Lists to record vehicles deceleration separately =====================================================================
Decel_1 = []
Decel_2 = []
Decel_3 = []
Decel_4 = []
Decel_5 = []
Decel_6 = []
Decel_7 = []
Decel_8 = []
Decel_9 = []
Decel_10 = []
ID_list = [] # Experiment ID list
k = 0  # Experiment ID
for file in file_list:
    k += 1  # counts the Experiment ID
    ID_list.append(k)
    # ========================================== Reads the XML file ====================================================
    root = ET.parse(file).getroot()
    DecelList_1 = []
    DecelList_2 = []
    DecelList_3 = []
    DecelList_4 = []
    DecelList_5 = []
    DecelList_6 = []
    DecelList_7 = []
    DecelList_8 = []
    DecelList_9 = []
    DecelList_10 = []
    for X in root.findall('timestep'):#Inside xml file goes to (timestep-> vehicle); allows to pick up whatever I want from there
        timee = float(X.get("time"))
#        if timee>=11.00:
        for B in X.findall('vehicle'):
            id = B.get("id")
            if id == "1":
                value = B.get('acceleration')
                DecelList_1.append(float(value))
            elif id == "2":
                value = B.get('acceleration')
                DecelList_2.append(float(value))
            elif id == "3":
                value = B.get('acceleration')
                DecelList_3.append(float(value))
            elif id == "4":
                value = B.get('acceleration')
                DecelList_4.append(float(value))
            elif id == "5":
                value = B.get('acceleration')
                DecelList_5.append(float(value))
            elif id == "6":
                value = B.get('acceleration')
                DecelList_6.append(float(value))
            elif id == "7":
                value = B.get('acceleration')
                DecelList_7.append(float(value))
            elif id == "8":
                value = B.get('acceleration')
                DecelList_8.append(float(value))
            elif id == "9":
                value = B.get('acceleration')
                DecelList_9.append(float(value))
            elif id == "10":
                value = B.get('acceleration')
                DecelList_10.append(float(value))

    Decel_1.append(DecelList_1)
    Decel_2.append(DecelList_2)
    Decel_3.append(DecelList_3)
    Decel_4.append(DecelList_4)
    Decel_5.append(DecelList_5)
    Decel_6.append(DecelList_6)
    Decel_7.append(DecelList_7)
    Decel_8.append(DecelList_8)
    Decel_9.append(DecelList_9)
    Decel_10.append(DecelList_10)
    print("Decel List 5 = ", DecelList_5)
    print("Speed List 6 = ", DecelList_6)

# Read csv file to extract the fault injection time and the lc.Assertive value =========================================
f = open('table_2020-09-27 14.53.21.csv', 'r')
readCSV = csv.reader(f)
Time = []
value = []
next(readCSV)
for row in readCSV:
    Time.append(row[2])
    value.append(int(row[4]))

# ================================================Save in CSV file =====================================================
df_7 = pd.DataFrame(
        {
            'Ex ID' : ID_list,
            'Time': Time,
            'lc.Asertive': value,
            'Dcel_1': Decel_1,
            'Dcel_2': Decel_2,
            'Dcel_3': Decel_3,
            'Dcel_4': Decel_4,
            'Dcel_5': Decel_5,
            'Dcel_6': Decel_6,
            'Dcel_7': Decel_7,
            'Dcel_8': Decel_8,
            'Dcel_9': Decel_9,
            'Dcel_10': Decel_10
                }
        )

now = datetime.now() # Current time =========================================================================
current_time = now.strftime("%Y-%m-%d %H.%M.%S")
df_7.to_csv("Parsed Deceleration_All Vehicles_{}.csv".format(current_time))


