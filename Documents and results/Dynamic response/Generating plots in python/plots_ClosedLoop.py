# -*- coding: utf-8 -*-
"""
Created on Tue May  5 00:07:15 2026

@author: vetle
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("plotsCL", exist_ok=True)

def GetSensorData(df, tag):
    for col in df.columns:
        if df.iloc[32, col] == tag:
            time = df.iloc[35:, 1]
            data = df.iloc[35:, col]
            return time, data
    return None, None

def GetOnlySensorData(df, tag):
    for col in df.columns:
        if df.iloc[32, col] == tag:
            return df.iloc[35:, col]
    return None

def GetSingleSensorData(df, tag, index):
    for col in df.columns:
        if df.iloc[32, col] == tag:
            return df.iloc[index, col]
    return None

readFromFile = "DynamicValidation.xlsx"

plt.rcParams.update({
    "font.size": 18,
    "axes.titlesize": 20,
    "axes.labelsize": 18,
    "legend.fontsize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16
})

#%% fig4CL - SRD
kspice = [
    [0.275371, 8.71632]
]

enaasen = [
    [0.322, 10.01],[0.408, 5.4],[0.418, 5.2],[0.420, 5.3],
    [0.442, 4.5],[0.454, 4.2],[0.490, 3.9],[0.494, 4.5]
]

pinto = [
    [0.250, 16.6],[0.252, 17.4],[0.311, 10.0],
    [0.329, 8.5],[0.388, 7.5],[0.479, 4.6],[0.541, 3.0]
]

tobiesen = [
    [0.26, 11.1],[0.29, 9.4],[0.31, 8.8],[0.31, 8.5],
    [0.31, 8.25],[0.31, 8.0],[0.32, 8.4],[0.32, 8.2],
    [0.33, 7.45],[0.34, 7.55],[0.35, 6.6],[0.37, 7.7],
    [0.39, 5.1],[0.40, 5.9],[0.41, 4.5],[0.43, 4.1],
    [0.45, 5.4],[0.45, 4.6],[0.45, 4.4],[0.46, 3.8]
]

xKspice = [point[0] for point in kspice]
yKspice = [point[1] for point in kspice]

xEnaasen = [point[0] for point in enaasen]
yEnaasen = [point[1] for point in enaasen]

xPinto = [point[0] for point in pinto]
yPinto = [point[1] for point in pinto]

xTobiesen = [point[0] for point in tobiesen]
yTobiesen = [point[1] for point in tobiesen]

plt.figure(figsize=(12, 7))
plt.scatter(xKspice, yKspice,
            marker='o',
            color='black',
            label='K-Spice - Lukket sløyfe')
plt.scatter(xEnaasen, yEnaasen,
            marker='o',
            facecolors='none',
            edgecolors='black',
            label='Enaasen Flø et al. (2015)')
plt.scatter(xPinto, yPinto,
            marker='D',
            facecolors='none',
            edgecolors='black',
            label='Pinto et al. (2014)')
plt.scatter(xTobiesen, yTobiesen,
            marker='s',
            facecolors='none',
            edgecolors='black',
            label='Tobiesen et al. (2007)')


plt.xlabel("CO₂-loading [mol CO₂/mol MEA]")
plt.ylabel("Spesifikk reboiler-arbeid [GJ/tonn CO2]")
plt.xlim(0.20, 0.55)
plt.ylim(0, 20)
plt.legend()
plt.savefig("plotsCL/fig4CL.png", dpi=300)
plt.show()

#%% -------------------START OF CASE 1 CLOSED LOOP--------------------
df_case1CL = pd.read_excel(readFromFile, "Case 1 CL", header=None)
#%% fig5CL - CO2 Input
pilotCO2Input = pd.read_csv("fig5_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Input_time = pilotCO2Input["time"]
pilotCO2Input_CO2 = pilotCO2Input["co2"]

kSpiceCO2Input_time, kSpiceCO2Input_CO2 = GetSensorData(df_case1CL, "GasToAbsorber:OutputCompositionVector[4]")
kSpiceCO2Input_CO2 = (kSpiceCO2Input_CO2/96.2)*100 #kompensasjon for 3.8% vann

plt.figure(figsize=(12, 7))
plt.plot(pilotCO2Input_time, pilotCO2Input_CO2,
            linestyle='--',
            linewidth=2,
            color='black',
            label='Pilot')

plt.plot(kSpiceCO2Input_time, kSpiceCO2Input_CO2,
            linestyle='-',
            linewidth=2,
            color='black',
            label='K-Spice - Lukket sløyfe')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber Innløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 10)
plt.legend()
plt.savefig("plotsCL/fig5CL.png", dpi=300)
plt.show()

#%% fig6CL - CO2 Output
pilotCO2Output = pd.read_csv("fig6_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Output_time = pilotCO2Output["time"]
pilotCO2Output_CO2 = pilotCO2Output["co2"]

kSpiceCO2Output_time, kSpiceCO2Output_CO2 = GetSensorData(df_case1CL, "GasFromAbsorber:OutputCompositionVector[4]")
kSpiceCO2Output_CO2 = (kSpiceCO2Output_CO2/96.2)*100 #kompensasjon for 3.8% vann


plt.figure(figsize=(12, 7))
plt.plot(pilotCO2Output_time, pilotCO2Output_CO2,
            linestyle='--',
            linewidth=2,
            color='black',
            label='Pilot')

plt.plot(kSpiceCO2Output_time, kSpiceCO2Output_CO2,
            linestyle='-',
            linewidth=2,
            color='black',
            label='K-Spice - Lukket sløyfe')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber utløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 4.5)
plt.legend()
plt.savefig("plotsCL/fig6CL.png", dpi=300)
plt.show()

#%% fig 7CL - Loading
#a) Lean Loading
pilotCO2AnalysisLean = pd.read_csv("fig7a_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2AnalysisLean_time = pilotCO2AnalysisLean["time"]
pilotCO2AnalysisLean_Loading = pilotCO2AnalysisLean["leanLoading"]

pilotCO2DensityA = pd.read_csv("fig7a_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2DensityA_time = pilotCO2DensityA["time"]
pilotCO2DensityA_Loading = pilotCO2DensityA["leanLoading"]

kSpiceLeanLoadingIn_time, kSpiceLeanLoadingIn_Loading = GetSensorData(df_case1CL, "LAL_IN:Output")

#b) Rich Loading
pilotCO2AnalysisRich = pd.read_csv("fig7b_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2AnalysisRich_time = pilotCO2AnalysisRich["time"]
pilotCO2AnalysisRich_Loading = pilotCO2AnalysisRich["richLoading"]

pilotCO2DensityB = pd.read_csv("fig7b_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2DensityB_time = pilotCO2DensityB["time"]
pilotCO2DensityB_Loading = pilotCO2DensityB["richLoading"]

kSpiceRichLoading_time, kSpiceRichLoading_Loading = GetSensorData(df_case1CL, "RAL:Output")

# Plot fig7
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig7a
axes[0].scatter(pilotCO2AnalysisLean_time, pilotCO2AnalysisLean_Loading,
                marker='o',
                facecolors="none",
                color='black',
                label='Pilot - Analyse')

axes[0].plot(pilotCO2DensityA_time, pilotCO2DensityA_Loading,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot - Tetthet')

axes[0].plot(kSpiceLeanLoadingIn_time, kSpiceLeanLoadingIn_Loading,
             linestyle='dotted',
             linewidth=2,
             color='black',
             label='K-Spice - Lukket sløyfe - Inn i absorber')

axes[0].set_xlabel("Tid [min]")
axes[0].set_ylabel("Lean loading [molCO2/molMEA]")
axes[0].set_xlim(0, 245)
axes[0].set_ylim(0, 0.4)
axes[0].legend()
axes[0].set_title("a)", loc="left")

# Plot fig7b
axes[1].scatter(pilotCO2AnalysisRich_time, pilotCO2AnalysisRich_Loading,
                marker='o',
                facecolors="none",
                color='black',
                label='Pilot - Analyse')

axes[1].plot(pilotCO2DensityB_time, pilotCO2DensityB_Loading,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot - Tetthet')

axes[1].plot(kSpiceRichLoading_time, kSpiceRichLoading_Loading,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice - Lukket sløyfe - Ut av absorber')

axes[1].set_xlabel("Tid [min]")
axes[1].set_ylabel("Rich loading [molCO2/molMEA]")
axes[1].set_xlim(0, 245)
axes[1].set_ylim(0, 0.55)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plotsCL/fig7CL.png", dpi=300, bbox_inches='tight')
plt.show()

#%% Fig 8CL - Absorbed and desorbed CO2
# a) Absorbed CO2
pilotAbsorbedCO2 = pd.read_csv("fig8a_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotAbsorbedCO2_time = pilotAbsorbedCO2["time"]
pilotAbsorbedCO2_CO2 = pilotAbsorbedCO2["co2"]

kSpiceAbsorbedCO2_time = GetOnlySensorData(df_case1CL, "AdjustedTime")
kSpiceAbsorbedCO2_molIn = GetOnlySensorData(df_case1CL, "GasToAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_CO2PercentIn = GetOnlySensorData(df_case1CL, "GasToAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_molOut = GetOnlySensorData(df_case1CL, "GasFromAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_CO2PercentOutL = GetOnlySensorData(df_case1CL, "GasFromAbsorber:OutputCompositionVector[2]")
kSpiceAbsorbedCO2_CO2PercentOutG = GetOnlySensorData(df_case1CL, "GasFromAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_CO2 = (kSpiceAbsorbedCO2_molIn*(kSpiceAbsorbedCO2_CO2PercentIn/100)-(kSpiceAbsorbedCO2_molOut*((kSpiceAbsorbedCO2_CO2PercentOutG + kSpiceAbsorbedCO2_CO2PercentOutL)/100)))/1000

# b) Desorbed CO2
pilotDesorbedCO2 = pd.read_csv("fig8b_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotDesorbedCO2_time = pilotDesorbedCO2["time"]
pilotDesorbedCO2_CO2 = pilotDesorbedCO2["co2"]

'''
kSpiceDesorbedCO2_time = GetOnlySensorData(df_case1CL, "AdjustedTime")
kSpiceDesorbedCO2_molIn = GetOnlySensorData(df_case1CL, "RichAmine:OutletStream.m")
kSpiceDesorbedCO2_CO2PercentInL = GetOnlySensorData(df_case1CL, "RichAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_CO2PercentInG = GetOnlySensorData(df_case1CL, "RichAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_molOut = GetOnlySensorData(df_case1CL, "LeanAmine:OutletStream.m")
kSpiceDesorbedCO2_CO2PercentOutG = GetOnlySensorData(df_case1CL, "LeanAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_CO2PercentOutL = GetOnlySensorData(df_case1CL, "LeanAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_CO2 = (kSpiceDesorbedCO2_molIn*((kSpiceDesorbedCO2_CO2PercentInL + kSpiceDesorbedCO2_CO2PercentInG)/100) - (kSpiceDesorbedCO2_molOut*(kSpiceDesorbedCO2_CO2PercentOutG + kSpiceDesorbedCO2_CO2PercentOutL)/100))/1000

'''
# Plot fig8
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig8a
axes[0].plot(pilotAbsorbedCO2_time, pilotAbsorbedCO2_CO2,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot')

axes[0].plot(kSpiceAbsorbedCO2_time, kSpiceAbsorbedCO2_CO2,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice')

axes[0].set_xlabel("Tid [min]")
axes[0].set_ylabel("Absorbert CO2 [kmol/h]")
axes[0].set_xlim(0, 245)
axes[0].set_ylim(0, 0.35)
axes[0].legend()
axes[0].set_title("a)", loc="left")
'''
# Plot fig8b
axes[1].plot(pilotDesorbedCO2_time, pilotDesorbedCO2_CO2,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot')

axes[1].plot(kSpiceDesorbedCO2_time, kSpiceDesorbedCO2_CO2,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice')

axes[1].set_xlabel("Tid [min]")
axes[1].set_ylabel("Desorbert CO2 [kmol/h]")
axes[1].set_xlim(0, 245)
axes[1].set_ylim(0, 0.30)
axes[1].legend()
axes[1].set_title("b)", loc="left")
'''
plt.tight_layout()
plt.savefig("plotsCL/fig8CL.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig9CL - Absorber Temperature
# a) Absorber Temperature at start
pilotAbsorberTempStart_Pilot = pd.read_csv("fig9a_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart_Pilot_height = pilotAbsorberTempStart_Pilot["height"]
pilotAbsorberTempStart_Pilot_temp = pilotAbsorberTempStart_Pilot["temp"]

pilotAbsorberTempStart_Pilot_Sump = pd.read_csv("fig9a_Pilot_Sump_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart_Pilot_Sump_height = pilotAbsorberTempStart_Pilot_Sump["height"]
pilotAbsorberTempStart_Pilot_Sump_temp = pilotAbsorberTempStart_Pilot_Sump["temp"]

pilotAbsorberTempStart_Pilot_Gas_Out = pd.read_csv("fig9a_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart_Pilot_Gas_Out_height = pilotAbsorberTempStart_Pilot_Gas_Out["height"]
pilotAbsorberTempStart_Pilot_Gas_Out_temp = pilotAbsorberTempStart_Pilot_Gas_Out["temp"]


kSpiceAbsorberTempStart = [
    [0.103371, GetSingleSensorData(df_case1CL, "00TA001:MeasuredValue", 35)],
    [0.458427, GetSingleSensorData(df_case1CL, "00TA002:MeasuredValue", 35)],
    [0.813483, GetSingleSensorData(df_case1CL, "00TA003:MeasuredValue", 35)],
    [1.16854, GetSingleSensorData(df_case1CL, "00TA004:MeasuredValue", 35)],
    [2.23371, GetSingleSensorData(df_case1CL, "00TA005:MeasuredValue", 35)],
    [3.30337, GetSingleSensorData(df_case1CL, "00TA006:MeasuredValue", 35)],
    [3.66292, GetSingleSensorData(df_case1CL, "00TA007:MeasuredValue", 35)],
    [4.02247, GetSingleSensorData(df_case1CL, "00TI015:MeasuredValue", 35)],
    ]
kSpiceAbsorberTempStart_height = [point[0] for point in kSpiceAbsorberTempStart]
kSpiceAbsorberTempStart_temp = [point[1] for point in kSpiceAbsorberTempStart]

kSpiceAbsorberTempStart_Sump = [[0.0, GetSingleSensorData(
    df_case1CL, "00TA000:MeasuredValue", 35)]]
kSpiceAbsorberTempStart_Sump_height = [point[0] for point in kSpiceAbsorberTempStart_Sump]
kSpiceAbsorberTempStart_Sump_temp = [point[1] for point in kSpiceAbsorberTempStart_Sump]

kSpiceAbsorberTempStart_Gas_Out = [[4.230, GetSingleSensorData(
    df_case1CL, "00TI003:MeasuredValue", 35)]]
kSpiceAbsorberTempStart_Gas_Out_height = [point[0] for point in kSpiceAbsorberTempStart_Gas_Out]
kSpiceAbsorberTempStart_Gas_Out_temp = [point[1] for point in kSpiceAbsorberTempStart_Gas_Out]



# b) Absorber Temperature at end
pilotAbsorberTempEnd_Pilot = pd.read_csv("fig9b_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd_Pilot_height = pilotAbsorberTempEnd_Pilot["height"]
pilotAbsorberTempEnd_Pilot_temp = pilotAbsorberTempEnd_Pilot["temp"]

pilotAbsorberTempEnd_Pilot_Sump = pd.read_csv("fig9b_Pilot_Sump_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd_Pilot_Sump_height = pilotAbsorberTempEnd_Pilot_Sump["height"]
pilotAbsorberTempEnd_Pilot_Sump_temp = pilotAbsorberTempEnd_Pilot_Sump["temp"]

pilotAbsorberTempEnd_Pilot_Gas_Out = pd.read_csv("fig9b_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd_Pilot_Gas_Out_height = pilotAbsorberTempEnd_Pilot_Gas_Out["height"]
pilotAbsorberTempEnd_Pilot_Gas_Out_temp = pilotAbsorberTempEnd_Pilot_Gas_Out["temp"]

kSpiceAbsorberTempEnd = [
    [0.103371, GetSingleSensorData(df_case1CL, "00TA001:MeasuredValue", -1)],
    [0.458427, GetSingleSensorData(df_case1CL, "00TA002:MeasuredValue", -1)],
    [0.813483, GetSingleSensorData(df_case1CL, "00TA003:MeasuredValue", -1)],
    [1.16854, GetSingleSensorData(df_case1CL, "00TA004:MeasuredValue", -1)],
    [2.23371, GetSingleSensorData(df_case1CL, "00TA005:MeasuredValue", -1)],
    [3.30337, GetSingleSensorData(df_case1CL, "00TA006:MeasuredValue", -1)],
    [3.66292, GetSingleSensorData(df_case1CL, "00TA007:MeasuredValue", -1)],
    [4.02247, GetSingleSensorData(df_case1CL, "00TI015:MeasuredValue", -1)],
    ]
kSpiceAbsorberTempEnd_height = [point[0] for point in kSpiceAbsorberTempEnd]
kSpiceAbsorberTempEnd_temp = [point[1] for point in kSpiceAbsorberTempEnd]

kSpiceAbsorberTempEnd_Sump = [[0.0, GetSingleSensorData(
    df_case1CL, "00TA000:MeasuredValue", -1)]]
kSpiceAbsorberTempEnd_Sump_height = [point[0] for point in kSpiceAbsorberTempEnd_Sump]
kSpiceAbsorberTempEnd_Sump_temp = [point[1] for point in kSpiceAbsorberTempEnd_Sump]

kSpiceAbsorberTempEnd_Gas_Out = [[4.230, GetSingleSensorData(
    df_case1CL, "00TI003:MeasuredValue", -1)]]
kSpiceAbsorberTempEnd_Gas_Out_height = [point[0] for point in kSpiceAbsorberTempEnd_Gas_Out]
kSpiceAbsorberTempEnd_Gas_Out_temp = [point[1] for point in kSpiceAbsorberTempEnd_Gas_Out]

# Plot fig9
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig9a
axes[0].scatter(pilotAbsorberTempStart_Pilot_height, pilotAbsorberTempStart_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[0].scatter(kSpiceAbsorberTempStart_height, kSpiceAbsorberTempStart_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice - Lukket sløyfe')

axes[0].scatter(pilotAbsorberTempStart_Pilot_Sump_height, pilotAbsorberTempStart_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[0].scatter(kSpiceAbsorberTempStart_Sump_height, kSpiceAbsorberTempStart_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump - Lukket sløyfe')

axes[0].scatter(pilotAbsorberTempStart_Pilot_Gas_Out_height, pilotAbsorberTempStart_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceAbsorberTempStart_Gas_Out_height, kSpiceAbsorberTempStart_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut - Lukket sløyfe')

axes[0].set_xlabel("Høyde [m]")
axes[0].set_ylabel("Temperatur i absorber [°C]")
axes[0].set_xlim(-0.02, 4.3)
axes[0].set_ylim(0, 70)
axes[0].legend()
axes[0].set_title("a)", loc="left")

# Plot fig9b
axes[1].scatter(pilotAbsorberTempEnd_Pilot_height, pilotAbsorberTempEnd_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[1].scatter(kSpiceAbsorberTempEnd_height, kSpiceAbsorberTempEnd_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice - Lukket sløyfe')

axes[1].scatter(pilotAbsorberTempEnd_Pilot_Sump_height, pilotAbsorberTempEnd_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[1].scatter(kSpiceAbsorberTempEnd_Sump_height, kSpiceAbsorberTempEnd_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump - Lukket sløyfe')

axes[1].scatter(pilotAbsorberTempEnd_Pilot_Gas_Out_height, pilotAbsorberTempEnd_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceAbsorberTempEnd_Gas_Out_height, kSpiceAbsorberTempEnd_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut - Lukket sløyfe')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i absorber [°C]")
axes[1].set_xlim(-0.02, 4.3)
axes[1].set_ylim(0, 70)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plotsCL/fig9CL.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig10CL - Desorber Temperature
#a) Desorber Temperature at start
pilotDesorberTempStart_Pilot = pd.read_csv("fig10a_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart_Pilot_height = pilotDesorberTempStart_Pilot["height"]
pilotDesorberTempStart_Pilot_temp = pilotDesorberTempStart_Pilot["temp"]

pilotDesorberTempStart_Pilot_Reboiler = pd.read_csv("fig10a_Pilot_Reboiler_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart_Pilot_Reboiler_height = pilotDesorberTempStart_Pilot_Reboiler["height"]
pilotDesorberTempStart_Pilot_Reboiler_temp = pilotDesorberTempStart_Pilot_Reboiler["temp"]

pilotDesorberTempStart_Pilot_Solvent_In = pd.read_csv("fig10a_Pilot_Solvent_In_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart_Pilot_Solvent_In_height = pilotDesorberTempStart_Pilot_Solvent_In["height"]
pilotDesorberTempStart_Pilot_Solvent_In_temp = pilotDesorberTempStart_Pilot_Solvent_In["temp"]

pilotDesorberTempStart_Pilot_Gas_Out = pd.read_csv("fig10a_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart_Pilot_Gas_Out_height = pilotDesorberTempStart_Pilot_Gas_Out["height"]
pilotDesorberTempStart_Pilot_Gas_Out_temp = pilotDesorberTempStart_Pilot_Gas_Out["temp"]

kSpiceDesorberTempStart = [
    [0.100425, GetSingleSensorData(df_case1CL, "01TS001:MeasuredValue", 35)],
    [1.04888, GetSingleSensorData(df_case1CL, "01TS002:MeasuredValue", 35)],
    [2.00106, GetSingleSensorData(df_case1CL, "01TS003:MeasuredValue", 35)],
    [2.9458, GetSingleSensorData(df_case1CL, "01TS004:MeasuredValue", 35)],
    [3.56695, GetSingleSensorData(df_case1CL, "01TS005:MeasuredValue", 35)]
    ]
kSpiceDesorberTempStart_height = [point[0] for point in kSpiceDesorberTempStart]
kSpiceDesorberTempStart_temp = [point[1] for point in kSpiceDesorberTempStart]

kSpiceDesorberTempStart_Reboiler = [[0.0, GetSingleSensorData(
    df_case1CL, "02TI010:MeasuredValue", 35)]]
kSpiceDesorberTempStart_Reboiler_height = [point[0] for point in kSpiceDesorberTempStart_Reboiler]
kSpiceDesorberTempStart_Reboiler_temp = [point[1] for point in kSpiceDesorberTempStart_Reboiler]

kSpiceDesorberTempStart_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case1CL, "01TI007:MeasuredValue", 35)]]
kSpiceDesorberTempStart_Solvent_In_height = [point[0] for point in kSpiceDesorberTempStart_Solvent_In]
kSpiceDesorberTempStart_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempStart_Solvent_In]

kSpiceDesorberTempStart_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case1CL, "GasFromDesorber:OutletStream.t", 35)]]
kSpiceDesorberTempStart_Gas_Out_height = [point[0] for point in kSpiceDesorberTempStart_Gas_Out]
kSpiceDesorberTempStart_Gas_Out_temp = [point[1] for point in kSpiceDesorberTempStart_Gas_Out]

# b) Desorber Temperature at end
pilotDesorberTempEnd_Pilot = pd.read_csv("fig10b_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd_Pilot_height = pilotDesorberTempEnd_Pilot["height"]
pilotDesorberTempEnd_Pilot_temp = pilotDesorberTempEnd_Pilot["temp"]

pilotDesorberTempEnd_Pilot_Reboiler = pd.read_csv("fig10b_Pilot_Reboiler_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd_Pilot_Reboiler_height = pilotDesorberTempEnd_Pilot_Reboiler["height"]
pilotDesorberTempEnd_Pilot_Reboiler_temp = pilotDesorberTempEnd_Pilot_Reboiler["temp"]

pilotDesorberTempEnd_Pilot_Solvent_In = pd.read_csv("fig10b_Pilot_Solvent_In_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd_Pilot_Solvent_In_height = pilotDesorberTempEnd_Pilot_Solvent_In["height"]
pilotDesorberTempEnd_Pilot_Solvent_In_temp = pilotDesorberTempEnd_Pilot_Solvent_In["temp"]

pilotDesorberTempEnd_Pilot_Gas_Out = pd.read_csv("fig10b_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd_Pilot_Gas_Out_height = pilotDesorberTempEnd_Pilot_Gas_Out["height"]
pilotDesorberTempEnd_Pilot_Gas_Out_temp = pilotDesorberTempEnd_Pilot_Gas_Out["temp"]

kSpiceDesorberTempEnd = [
    [0.100425, GetSingleSensorData(df_case1CL, "01TS001:MeasuredValue", -1)],
    [1.04888, GetSingleSensorData(df_case1CL, "01TS002:MeasuredValue", -1)],
    [2.00106, GetSingleSensorData(df_case1CL, "01TS003:MeasuredValue", -1)],
    [2.9458, GetSingleSensorData(df_case1CL, "01TS004:MeasuredValue", -1)],
    [3.56695, GetSingleSensorData(df_case1CL, "01TS005:MeasuredValue", -1)]
    ]
kSpiceDesorberTempEnd_height = [point[0] for point in kSpiceDesorberTempEnd]
kSpiceDesorberTempEnd_temp = [point[1] for point in kSpiceDesorberTempEnd]

kSpiceDesorberTempEnd_Reboiler = [[0.0, GetSingleSensorData(
    df_case1CL, "02TI010:MeasuredValue", -1)]]
kSpiceDesorberTempEnd_Reboiler_height = [point[0] for point in kSpiceDesorberTempEnd_Reboiler]
kSpiceDesorberTempEnd_Reboiler_temp = [point[1] for point in kSpiceDesorberTempEnd_Reboiler]

kSpiceDesorberTempEnd_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case1CL, "01TI007:MeasuredValue", -1)]]
kSpiceDesorberTempEnd_Solvent_In_height = [point[0] for point in kSpiceDesorberTempEnd_Solvent_In]
kSpiceDesorberTempEnd_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempEnd_Solvent_In]

kSpiceDesorberTempEnd_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case1CL, "GasFromDesorber:OutletStream.t", -1)]]
kSpiceDesorberTempEnd_Gas_Out_height = [point[0] for point in kSpiceDesorberTempEnd_Gas_Out]
kSpiceDesorberTempEnd_Gas_Out_temp = [point[1] for point in kSpiceDesorberTempEnd_Gas_Out]

#Plot fig10
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig10a
axes[0].scatter(pilotDesorberTempStart_Pilot_height, pilotDesorberTempStart_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[0].scatter(kSpiceDesorberTempStart_height, kSpiceDesorberTempStart_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice - Lukket sløyfe')

axes[0].scatter(pilotDesorberTempStart_Pilot_Reboiler_height, pilotDesorberTempStart_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[0].scatter(kSpiceDesorberTempStart_Reboiler_height, kSpiceDesorberTempStart_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler - Lukket sløyfe')

axes[0].scatter(pilotDesorberTempStart_Pilot_Solvent_In_height, pilotDesorberTempStart_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[0].scatter(kSpiceDesorberTempStart_Solvent_In_height, kSpiceDesorberTempStart_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in - Lukket sløyfe')

axes[0].scatter(pilotDesorberTempStart_Pilot_Gas_Out_height, pilotDesorberTempStart_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceDesorberTempStart_Gas_Out_height, kSpiceDesorberTempStart_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut - Lukket sløyfe')

axes[0].set_xlabel("Høyde [m]")
axes[0].set_ylabel("Temperatur i desorber [°C]")
axes[0].set_xlim(-0.02, 3.6)
axes[0].set_ylim(70, 125)
axes[0].legend()
axes[0].set_title("a)", loc="left")


# Plot fig10b
axes[1].scatter(pilotDesorberTempEnd_Pilot_height, pilotDesorberTempEnd_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[1].scatter(kSpiceDesorberTempEnd_height, kSpiceDesorberTempEnd_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice - Lukket sløyfe')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Reboiler_height, pilotDesorberTempEnd_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[1].scatter(kSpiceDesorberTempEnd_Reboiler_height, kSpiceDesorberTempEnd_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler - Lukket sløyfe')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Solvent_In_height, pilotDesorberTempEnd_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[1].scatter(kSpiceDesorberTempEnd_Solvent_In_height, kSpiceDesorberTempEnd_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in - Lukket sløyfe')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Gas_Out_height, pilotDesorberTempEnd_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceDesorberTempEnd_Gas_Out_height, kSpiceDesorberTempEnd_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut - Lukket sløyfe')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i desorber [°C]")
axes[1].set_xlim(-0.02, 3.6)
axes[1].set_ylim(70, 125)
axes[1].legend()
axes[1].set_title("b)", loc="left")


plt.tight_layout()
plt.savefig("plotsCL/fig10CL.png", dpi=300, bbox_inches='tight')
plt.show()

