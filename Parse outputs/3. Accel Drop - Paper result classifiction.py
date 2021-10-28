import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
import re
import csv
import ast

f = open('Parsed Deceleration_All Vehicles_2020-09-27 23.25.17.csv', 'r')
readCSV = csv.reader(f)

# ========================================== Reads the XML file ====================================================
root = ET.parse('outputG/2020-09-27-16-18-32fcd-output.xml').getroot()  # Golden run file
DecelList = {} # Dictionary to create a lists
for j in range(1, 11, 1): # Creates 10 lists
    DecelList[j] = []
for X in root.findall('timestep'): #Inside xml file goes to (timestep-> vehicle); allows to pick up whatever I want from there
    timee = float(X.get("time"))
    if timee >= 11.00:
        for B in X.findall('vehicle'):
            id = B.get("id")
            for v in range(1, 11, 1):
                if id == str(v):
                    value = B.get('acceleration')
                    DecelList[v].append(float(value))

for f in range(1, 11, 1):
    print("Deceleration_%s"%f , DecelList[f])
print("\n======================================================\n")
for f in range(1, 11, 1):
    print("Max Deceleration_%s" % f, min(DecelList[f]))
#===============================================================================
k = 0
# ==========================================
nonEffective = []
Effective = []
ID = []
Time = []
value_list = []
DecelTotal = []
CarNumber = []
next(readCSV)
for row in readCSV:
# ===================Reads Deceleration data for all of vehicles in the faulty experiments ===============================
    nonEffectiveEx = [] # Non-effective in each experiment
    EffectiveEx = [] # Effective in each experiment
    DecelEx = []  # Deceleration in each experiment
    CarEx = []  # considered car number in each experiment
    for v in range (4, 14, 1): # V is number of vehicles (10 vehicles: from 4 to 14)
        list = row[v]
        list1 = ast.literal_eval(list)  # Converting string to list
        k += 1
        print('step =   ', k, '=======================================================')
        if list1 == DecelList[v-3]: # if the faulty-run be identical with the golden-run
            nonEffectiveEx.append(1)
        else:
            EffectiveEx.append(1)
            DecelEx.append(min(list1))
            CarEx.append(v - 3)  # Adds the car number in the experiment

    if len(nonEffectiveEx) == 10:
        nonEffective.append(1)
    else:
        Effective.append(1)
        DecelTotal.append(abs(min(DecelEx)))
        CarNumber.append(CarEx[DecelEx.index(min(DecelEx))])
        ID.append(row[1])  # Adds the number of experiment to the list
        Time.append(row[2])
        value_list.append(float(row[3]))


#=========================================
'''
#plt.plot(0, abs(decel_min_G), '*r', linewidth=5)  #Golden run
plt.plot(ID, DecelTotal, '.', linewidth=0.1)
#plt.legend(['Golden', 'Faulty'], prop={"size":15})
plt.xlabel('Experiment ID', fontsize='10')
plt.ylabel('Deceleration [$m/s^2$]', fontsize='10')
plt.title('Max Brake Deceleration ', fontsize='10')
plt.title('Change of Value - Intermittent - lcAssertive')
# plt.grid()
plt.show()
print("ExID = ", ID)
print("Length ExID = ", len(ID))
print("DecelTotal = ", DecelTotal)
print("car numbers: ", CarNumber)
'''
#===============================================================================================================
#  separating catastrophic and benign cases
catas_list=[]
benign_list=[]
negligible_list=[]
print("lenght list= ", len(DecelTotal))
for i in range (0, len(DecelTotal)):  # here the index (i) of them is recorded by separating to different groups
    if DecelTotal[i] <= 0.78:
        negligible_list.append(i)
    elif DecelTotal[i] <= 5.0 and DecelTotal[i] > 0.78:
        benign_list.append(i)
    elif DecelTotal[i] > 5.0:
        catas_list.append(i)
print("negligible", negligible_list)
print("benign", benign_list)
print("catas", catas_list)
print(len(negligible_list), len(benign_list), len(catas_list))

print("Negligible =", len(negligible_list), "   Benign = ",  len(benign_list), "   Catastrophic = ",  len(catas_list))
#=======================================================================================================================
time_neg =[]
value_neg =[]
car_neg =[]
for i in negligible_list:
    time_neg.append(Time[i])
    value_neg.append(value_list[i])
    car_neg.append(CarNumber[i])
print("\n\nNegligible:===========================================================================================")
print("ego-vehicle= ", car_neg.count(5), "\nfollower-vehicle= ", car_neg.count(6), "\nall-vehicles= ", len(car_neg))
time_benign =[]
value_benign =[]
car_benign =[]
for i in benign_list:
    time_benign.append(Time[i])
    value_benign.append(value_list[i])
    car_benign.append(CarNumber[i])
print("\n\nBenign:===========================================================================================")
print("ego-vehicle= ", car_benign.count(5), "\nfollower-vehicle= ", car_benign.count(6), "\nall-vehicles= ", len(car_benign))
time_catas =[]
value_catas =[]
car_catas =[]
for i in catas_list:
    time_catas.append(Time[i])
    value_catas.append(value_list[i])
    car_catas.append(CarNumber[i])
print("\n\nCatastrophic:===========================================================================================")
print("ego-vehicle= ", car_catas.count(5), "\nfollower-vehicle= ", car_catas.count(6), "\nall-vehicles= ", len(car_catas))

'''
plt.plot(time_neg, value_neg, '.g', linewidth=1)
plt.plot(time_benign, value_benign, '.b', linewidth=1)
plt.plot(time_catas, value_catas, '.r', linewidth=1)
plt.xlabel('Time (S)', fontsize='10')
plt.ylabel('LC-Assertive Value', fontsize='10')
plt.legend(['Negligible', 'Benign', 'Catastrophic', 'Non-effective', 'Detected'], loc='center left', bbox_to_anchor=(0.925, 0.5), prop={"size":10})
# plt.grid()
plt.gcf().autofmt_xdate()
#plt.xticks([11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 19.5, 20.0, 20.5])
plt.show()
'''
print("\n\nNon-Effective = ", len(nonEffective))
print("Effective = ", len(Effective))
