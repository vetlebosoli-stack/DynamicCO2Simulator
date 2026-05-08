# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 08:33:23 2026

@author: vetle
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("plots", exist_ok=True)

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


#%% fig4 - SRD
kspice = [
    [0.467859, 3.94531],[0.521205, 3.7],[0.529487, 3.79712],
    [0.438132, 4.70594],[0.527418, 3.46859],[0.503249, 3.89628]
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
            label='K-Spice')
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
plt.savefig("plots/fig4.png", dpi=300)
plt.show()

#%% -------------------START OF CASE 1--------------------
df_case1 = pd.read_excel(readFromFile, "Case 1", header=None)
#%% fig5 - CO2 Input
pilotCO2Input = pd.read_csv("fig5_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Input_time = pilotCO2Input["time"]
pilotCO2Input_CO2 = pilotCO2Input["co2"]

kSpiceCO2Input_time, kSpiceCO2Input_CO2 = GetSensorData(df_case1, "GasToAbsorber:OutputCompositionVector[4]")
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
            label='K-Spice')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber Innløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 10)
plt.legend()
plt.savefig("plots/fig5.png", dpi=300)
plt.show()

#%% fig6 - CO2 Output
pilotCO2Output = pd.read_csv("fig6_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Output_time = pilotCO2Output["time"]
pilotCO2Output_CO2 = pilotCO2Output["co2"]

kSpiceCO2Output_time, kSpiceCO2Output_CO2 = GetSensorData(df_case1, "GasFromAbsorber:OutputCompositionVector[4]")
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
            label='K-Spice')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber utløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 6)
plt.legend()
plt.savefig("plots/fig6.png", dpi=300)
plt.show()

#%% fig 7 - Loading
#a) Lean Loading
pilotCO2AnalysisLean = pd.read_csv("fig7a_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2AnalysisLean_time = pilotCO2AnalysisLean["time"]
pilotCO2AnalysisLean_Loading = pilotCO2AnalysisLean["leanLoading"]

pilotCO2DensityA = pd.read_csv("fig7a_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2DensityA_time = pilotCO2DensityA["time"]
pilotCO2DensityA_Loading = pilotCO2DensityA["leanLoading"]

kSpiceLeanLoading_time, kSpiceLeanLoading_Loading = GetSensorData(df_case1, "LAL:Output")

kSpiceLeanLoadingIn_time, kSpiceLeanLoadingIn_Loading = GetSensorData(df_case1, "LAL_IN:Output")

#b) Rich Loading
pilotCO2AnalysisRich = pd.read_csv("fig7b_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2AnalysisRich_time = pilotCO2AnalysisRich["time"]
pilotCO2AnalysisRich_Loading = pilotCO2AnalysisRich["richLoading"]

pilotCO2DensityB = pd.read_csv("fig7b_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2DensityB_time = pilotCO2DensityB["time"]
pilotCO2DensityB_Loading = pilotCO2DensityB["richLoading"]

kSpiceRichLoading_time, kSpiceRichLoading_Loading = GetSensorData(df_case1, "RAL:Output")

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

axes[0].plot(kSpiceLeanLoading_time, kSpiceLeanLoading_Loading,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice - Ut av desorber')

axes[0].plot(kSpiceLeanLoadingIn_time, kSpiceLeanLoadingIn_Loading,
             linestyle='dotted',
             linewidth=2,
             color='black',
             label='K-Spice - Inn i absorber')

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
             label='K-Spice - Ut av absorber')

axes[1].set_xlabel("Tid [min]")
axes[1].set_ylabel("Rich loading [molCO2/molMEA]")
axes[1].set_xlim(0, 245)
axes[1].set_ylim(0, 0.55)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plots/fig7.png", dpi=300, bbox_inches='tight')
plt.show()

#%% Fig 8 - Absorbed and desorbed CO2
# a) Absorbed CO2
pilotAbsorbedCO2 = pd.read_csv("fig8a_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotAbsorbedCO2_time = pilotAbsorbedCO2["time"]
pilotAbsorbedCO2_CO2 = pilotAbsorbedCO2["co2"]

kSpiceAbsorbedCO2_time = GetOnlySensorData(df_case1, "AdjustedTime")
kSpiceAbsorbedCO2_molIn = GetOnlySensorData(df_case1, "GasToAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_CO2PercentIn = GetOnlySensorData(df_case1, "GasToAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_molOut = GetOnlySensorData(df_case1, "GasFromAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_CO2PercentOutL = GetOnlySensorData(df_case1, "GasFromAbsorber:OutputCompositionVector[2]")
kSpiceAbsorbedCO2_CO2PercentOutG = GetOnlySensorData(df_case1, "GasFromAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_CO2 = (kSpiceAbsorbedCO2_molIn*(kSpiceAbsorbedCO2_CO2PercentIn/100)-(kSpiceAbsorbedCO2_molOut*((kSpiceAbsorbedCO2_CO2PercentOutG + kSpiceAbsorbedCO2_CO2PercentOutL)/100)))/1000

# b) Desorbed CO2
pilotDesorbedCO2 = pd.read_csv("fig8b_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotDesorbedCO2_time = pilotDesorbedCO2["time"]
pilotDesorbedCO2_CO2 = pilotDesorbedCO2["co2"]


kSpiceDesorbedCO2_time = GetOnlySensorData(df_case1, "AdjustedTime")
kSpiceDesorbedCO2_molIn = GetOnlySensorData(df_case1, "RichAmine:OutletStream.m")
kSpiceDesorbedCO2_CO2PercentInL = GetOnlySensorData(df_case1, "RichAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_CO2PercentInG = GetOnlySensorData(df_case1, "RichAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_molOut = GetOnlySensorData(df_case1, "LeanAmine:OutletStream.m")
kSpiceDesorbedCO2_CO2PercentOutG = GetOnlySensorData(df_case1, "LeanAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_CO2PercentOutL = GetOnlySensorData(df_case1, "LeanAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_CO2 = (kSpiceDesorbedCO2_molIn*((kSpiceDesorbedCO2_CO2PercentInL + kSpiceDesorbedCO2_CO2PercentInG)/100) - (kSpiceDesorbedCO2_molOut*(kSpiceDesorbedCO2_CO2PercentOutG + kSpiceDesorbedCO2_CO2PercentOutL)/100))/1000


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

plt.tight_layout()
plt.savefig("plots/fig8.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig9 - Absorber Temperature
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
    [0.103371, GetSingleSensorData(df_case1, "00TA001:MeasuredValue", 35)],
    [0.458427, GetSingleSensorData(df_case1, "00TA002:MeasuredValue", 35)],
    [0.813483, GetSingleSensorData(df_case1, "00TA003:MeasuredValue", 35)],
    [1.16854, GetSingleSensorData(df_case1, "00TA004:MeasuredValue", 35)],
    [2.23371, GetSingleSensorData(df_case1, "00TA005:MeasuredValue", 35)],
    [3.30337, GetSingleSensorData(df_case1, "00TA006:MeasuredValue", 35)],
    [3.66292, GetSingleSensorData(df_case1, "00TA007:MeasuredValue", 35)],
    [4.02247, GetSingleSensorData(df_case1, "00TI015:MeasuredValue", 35)],
    ]
kSpiceAbsorberTempStart_height = [point[0] for point in kSpiceAbsorberTempStart]
kSpiceAbsorberTempStart_temp = [point[1] for point in kSpiceAbsorberTempStart]

kSpiceAbsorberTempStart_Sump = [[0.0, GetSingleSensorData(
    df_case1, "00TA000:MeasuredValue", 35)]]
kSpiceAbsorberTempStart_Sump_height = [point[0] for point in kSpiceAbsorberTempStart_Sump]
kSpiceAbsorberTempStart_Sump_temp = [point[1] for point in kSpiceAbsorberTempStart_Sump]

kSpiceAbsorberTempStart_Gas_Out = [[4.230, GetSingleSensorData(
    df_case1, "00TI003:MeasuredValue", 35)]]
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
    [0.103371, GetSingleSensorData(df_case1, "00TA001:MeasuredValue", -1)],
    [0.458427, GetSingleSensorData(df_case1, "00TA002:MeasuredValue", -1)],
    [0.813483, GetSingleSensorData(df_case1, "00TA003:MeasuredValue", -1)],
    [1.16854, GetSingleSensorData(df_case1, "00TA004:MeasuredValue", -1)],
    [2.23371, GetSingleSensorData(df_case1, "00TA005:MeasuredValue", -1)],
    [3.30337, GetSingleSensorData(df_case1, "00TA006:MeasuredValue", -1)],
    [3.66292, GetSingleSensorData(df_case1, "00TA007:MeasuredValue", -1)],
    [4.02247, GetSingleSensorData(df_case1, "00TI015:MeasuredValue", -1)],
    ]
kSpiceAbsorberTempEnd_height = [point[0] for point in kSpiceAbsorberTempEnd]
kSpiceAbsorberTempEnd_temp = [point[1] for point in kSpiceAbsorberTempEnd]

kSpiceAbsorberTempEnd_Sump = [[0.0, GetSingleSensorData(
    df_case1, "00TA000:MeasuredValue", -1)]]
kSpiceAbsorberTempEnd_Sump_height = [point[0] for point in kSpiceAbsorberTempEnd_Sump]
kSpiceAbsorberTempEnd_Sump_temp = [point[1] for point in kSpiceAbsorberTempEnd_Sump]

kSpiceAbsorberTempEnd_Gas_Out = [[4.230, GetSingleSensorData(
    df_case1, "00TI003:MeasuredValue", -1)]]
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
                label='K-Spice')

axes[0].scatter(pilotAbsorberTempStart_Pilot_Sump_height, pilotAbsorberTempStart_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[0].scatter(kSpiceAbsorberTempStart_Sump_height, kSpiceAbsorberTempStart_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump')

axes[0].scatter(pilotAbsorberTempStart_Pilot_Gas_Out_height, pilotAbsorberTempStart_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceAbsorberTempStart_Gas_Out_height, kSpiceAbsorberTempStart_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

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
                label='K-Spice')

axes[1].scatter(pilotAbsorberTempEnd_Pilot_Sump_height, pilotAbsorberTempEnd_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[1].scatter(kSpiceAbsorberTempEnd_Sump_height, kSpiceAbsorberTempEnd_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump')

axes[1].scatter(pilotAbsorberTempEnd_Pilot_Gas_Out_height, pilotAbsorberTempEnd_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceAbsorberTempEnd_Gas_Out_height, kSpiceAbsorberTempEnd_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i absorber [°C]")
axes[1].set_xlim(-0.02, 4.3)
axes[1].set_ylim(0, 70)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plots/fig9.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig10 - Desorber Temperature
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
    [0.100425, GetSingleSensorData(df_case1, "01TS001:MeasuredValue", 35)],
    [1.04888, GetSingleSensorData(df_case1, "01TS002:MeasuredValue", 35)],
    [2.00106, GetSingleSensorData(df_case1, "01TS003:MeasuredValue", 35)],
    [2.9458, GetSingleSensorData(df_case1, "01TS004:MeasuredValue", 35)],
    [3.56695, GetSingleSensorData(df_case1, "01TS005:MeasuredValue", 35)]
    ]
kSpiceDesorberTempStart_height = [point[0] for point in kSpiceDesorberTempStart]
kSpiceDesorberTempStart_temp = [point[1] for point in kSpiceDesorberTempStart]

kSpiceDesorberTempStart_Reboiler = [[0.0, GetSingleSensorData(
    df_case1, "02TI010:MeasuredValue", 35)]]
kSpiceDesorberTempStart_Reboiler_height = [point[0] for point in kSpiceDesorberTempStart_Reboiler]
kSpiceDesorberTempStart_Reboiler_temp = [point[1] for point in kSpiceDesorberTempStart_Reboiler]

kSpiceDesorberTempStart_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case1, "01TI007:MeasuredValue", 35)]]
kSpiceDesorberTempStart_Solvent_In_height = [point[0] for point in kSpiceDesorberTempStart_Solvent_In]
kSpiceDesorberTempStart_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempStart_Solvent_In]

kSpiceDesorberTempStart_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case1, "GasFromDesorber:OutletStream.t", 35)]]
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
    [0.100425, GetSingleSensorData(df_case1, "01TS001:MeasuredValue", -1)],
    [1.04888, GetSingleSensorData(df_case1, "01TS002:MeasuredValue", -1)],
    [2.00106, GetSingleSensorData(df_case1, "01TS003:MeasuredValue", -1)],
    [2.9458, GetSingleSensorData(df_case1, "01TS004:MeasuredValue", -1)],
    [3.56695, GetSingleSensorData(df_case1, "01TS005:MeasuredValue", -1)]
    ]
kSpiceDesorberTempEnd_height = [point[0] for point in kSpiceDesorberTempEnd]
kSpiceDesorberTempEnd_temp = [point[1] for point in kSpiceDesorberTempEnd]

kSpiceDesorberTempEnd_Reboiler = [[0.0, GetSingleSensorData(
    df_case1, "02TI010:MeasuredValue", -1)]]
kSpiceDesorberTempEnd_Reboiler_height = [point[0] for point in kSpiceDesorberTempEnd_Reboiler]
kSpiceDesorberTempEnd_Reboiler_temp = [point[1] for point in kSpiceDesorberTempEnd_Reboiler]

kSpiceDesorberTempEnd_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case1, "01TI007:MeasuredValue", -1)]]
kSpiceDesorberTempEnd_Solvent_In_height = [point[0] for point in kSpiceDesorberTempEnd_Solvent_In]
kSpiceDesorberTempEnd_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempEnd_Solvent_In]

kSpiceDesorberTempEnd_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case1, "GasFromDesorber:OutletStream.t", -1)]]
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
                label='K-Spice')

axes[0].scatter(pilotDesorberTempStart_Pilot_Reboiler_height, pilotDesorberTempStart_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[0].scatter(kSpiceDesorberTempStart_Reboiler_height, kSpiceDesorberTempStart_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler')

axes[0].scatter(pilotDesorberTempStart_Pilot_Solvent_In_height, pilotDesorberTempStart_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[0].scatter(kSpiceDesorberTempStart_Solvent_In_height, kSpiceDesorberTempStart_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in')

axes[0].scatter(pilotDesorberTempStart_Pilot_Gas_Out_height, pilotDesorberTempStart_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceDesorberTempStart_Gas_Out_height, kSpiceDesorberTempStart_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[0].set_xlabel("Høyde [m]")
axes[0].set_ylabel("Temperatur i desorber [°C]")
axes[0].set_xlim(-0.02, 3.6)
axes[0].set_ylim(95, 125)
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
                label='K-Spice')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Reboiler_height, pilotDesorberTempEnd_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[1].scatter(kSpiceDesorberTempEnd_Reboiler_height, kSpiceDesorberTempEnd_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Solvent_In_height, pilotDesorberTempEnd_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[1].scatter(kSpiceDesorberTempEnd_Solvent_In_height, kSpiceDesorberTempEnd_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in')

axes[1].scatter(pilotDesorberTempEnd_Pilot_Gas_Out_height, pilotDesorberTempEnd_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceDesorberTempEnd_Gas_Out_height, kSpiceDesorberTempEnd_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i desorber [°C]")
axes[1].set_xlim(-0.02, 3.6)
axes[1].set_ylim(95, 125)
axes[1].legend()
axes[1].set_title("b)", loc="left")


plt.tight_layout()
plt.savefig("plots/fig10.png", dpi=300, bbox_inches='tight')
plt.show()

#%% ----------------------START OF CASE 2--------------------------
df_case2 = pd.read_excel(readFromFile, "Case 2", header=None)

#%% fig11 - CO2 Input
pilotCO2Input11 = pd.read_csv("fig11_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Input11_time = pilotCO2Input11["time"]
pilotCO2Input11_CO2 = pilotCO2Input11["co2"]

kSpiceCO2Input11_time, kSpiceCO2Input11_CO2 = GetSensorData(df_case2, "GasToAbsorber:OutputCompositionVector[4]")

kSpiceCO2Input11_CO2 = (kSpiceCO2Input11_CO2/96.2)*100 #kompensasjon for 3.8% vann
plt.figure(figsize=(12, 7))
plt.plot(pilotCO2Input11_time, pilotCO2Input11_CO2,
            linestyle='--',
            linewidth=2,
            color='black',
            label='Pilot')

plt.plot(kSpiceCO2Input11_time, kSpiceCO2Input11_CO2,
            linestyle='-',
            linewidth=2,
            color='black',
            label='K-Spice')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber Innløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 10)
plt.legend()
plt.savefig("plots/fig11.png", dpi=300)
plt.show()

#%% fig12 - Rich Solvent Flow Rate
pilotSolventFlowRate12 = pd.read_csv("fig12_Pilot_E.csv", sep=";", decimal=",", names=["time","flow"])

pilotSolventFlowRate12_time = pilotSolventFlowRate12["time"]
pilotSolventFlowRate12_Flow = pilotSolventFlowRate12["flow"]

kSpiceSolventFlowRate12_time, kSpiceSolventFlowRate12_Flow = GetSensorData(df_case2, "00FT101:MeasuredValue")

plt.figure(figsize=(12, 7))
plt.plot(pilotSolventFlowRate12_time, pilotSolventFlowRate12_Flow,
            linestyle='--',
            linewidth=2,
            color='black',
            label='Pilot')

plt.plot(kSpiceSolventFlowRate12_time, kSpiceSolventFlowRate12_Flow,
            linestyle='-',
            linewidth=2,
            color='black',
            label='K-Spice')

plt.xlabel("Tid [min]")
plt.ylabel("Rich Solvent strømningsrate [kg/h]")
plt.xlim(0, 201)
plt.ylim(100, 300)
plt.legend()
plt.savefig("plots/fig12.png", dpi=300)
plt.show()

#%% fig13 - CO2 Output
pilotCO2Output13 = pd.read_csv("fig13_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])

pilotCO2Output13_time = pilotCO2Output13["time"]
pilotCO2Output13_CO2 = pilotCO2Output13["co2"]

kSpiceCO2Output13_time, kSpiceCO2Output13_CO2 = GetSensorData(df_case2, "GasFromAbsorber:OutputCompositionVector[4]")
kSpiceCO2Output13_CO2 = (kSpiceCO2Output13_CO2/96.2)*100 #kompensasjon for 3.8% vann

plt.figure(figsize=(12, 7))
plt.plot(pilotCO2Output13_time, pilotCO2Output13_CO2,
            linestyle='--',
            linewidth=2,
            color='black',
            label='Pilot')

plt.plot(kSpiceCO2Output13_time, kSpiceCO2Output13_CO2,
            linestyle='-',
            linewidth=2,
            color='black',
            label='K-Spice')

plt.xlabel("Tid [min]")
plt.ylabel("Absorber utløp CO2 [dry vol%]")
plt.xlim(0, 245)
plt.ylim(0, 2)
plt.legend()
plt.savefig("plots/fig13.png", dpi=300)
plt.show()

#%% fig14- Loading
#a) Lean Loading
pilotCO2AnalysisLean14 = pd.read_csv("fig14a_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2AnalysisLean14_time = pilotCO2AnalysisLean14["time"]
pilotCO2AnalysisLean14_Loading = pilotCO2AnalysisLean14["leanLoading"]

pilotCO2Density14A = pd.read_csv("fig14a_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","leanLoading"])
pilotCO2Density14A_time = pilotCO2Density14A["time"]
pilotCO2Density14A_Loading = pilotCO2Density14A["leanLoading"]

kSpiceLeanLoading14_time, kSpiceLeanLoading14_Loading = GetSensorData(df_case2, "LAL:Output")

kSpiceLeanLoadingIn14_time, kSpiceLeanLoadingIn14_Loading = GetSensorData(df_case2, "LAL_IN:Output")

#b) Rich Loading
pilotCO2AnalysisRich14 = pd.read_csv("fig14b_Pilot_Analysis_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2AnalysisRich14_time = pilotCO2AnalysisRich14["time"]
pilotCO2AnalysisRich14_Loading = pilotCO2AnalysisRich14["richLoading"]

pilotCO2Density14B = pd.read_csv("fig14b_Pilot_Density_E.csv", sep=";", decimal=",", names=["time","richLoading"])
pilotCO2Density14B_time = pilotCO2Density14B["time"]
pilotCO2Density14B_Loading = pilotCO2Density14B["richLoading"]

kSpiceRichLoading14_time, kSpiceRichLoading14_Loading = GetSensorData(df_case2, "RAL:Output")

# Plot fig14
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig14a
axes[0].scatter(pilotCO2AnalysisLean14_time, pilotCO2AnalysisLean14_Loading,
                marker='o',
                facecolors="none",
                color='black',
                label='Pilot - Analyse')

axes[0].plot(pilotCO2Density14A_time, pilotCO2Density14A_Loading,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot - Tetthet')

axes[0].plot(kSpiceLeanLoading14_time, kSpiceLeanLoading14_Loading,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice - Ut av desorber')

axes[0].plot(kSpiceLeanLoadingIn14_time, kSpiceLeanLoadingIn14_Loading,
             linestyle='dotted',
             linewidth=2,
             color='black',
             label='K-Spice - Inn i absorber')

axes[0].set_xlabel("Tid [min]")
axes[0].set_ylabel("Lean loading [molCO2/molMEA]")
axes[0].set_xlim(0, 245)
axes[0].set_ylim(0, 0.4)
axes[0].legend()
axes[0].set_title("a)", loc="left")

# Plot fig14b
axes[1].scatter(pilotCO2AnalysisRich14_time, pilotCO2AnalysisRich14_Loading,
                marker='o',
                facecolors="none",
                color='black',
                label='Pilot - Analyse')

axes[1].plot(pilotCO2Density14B_time, pilotCO2Density14B_Loading,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot - Tetthet')

axes[1].plot(kSpiceRichLoading14_time, kSpiceRichLoading14_Loading,
             linestyle='-',
             linewidth=2,
             color='black',
             label='K-Spice - Ut av absorber')

axes[1].set_xlabel("Tid [min]")
axes[1].set_ylabel("Rich loading [molCO2/molMEA]")
axes[1].set_xlim(0, 245)
axes[1].set_ylim(0, 0.55)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plots/fig14.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig15 - Absorbed and desorbed CO2
# a) Absorbed CO2
pilotAbsorbedCO2_15 = pd.read_csv("fig15a_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotAbsorbedCO2_15_time = pilotAbsorbedCO2_15["time"]
pilotAbsorbedCO2_15_CO2 = pilotAbsorbedCO2_15["co2"]

kSpiceAbsorbedCO2_15_time = GetOnlySensorData(df_case2, "AdjustedTime")
kSpiceAbsorbedCO2_15_molIn = GetOnlySensorData(df_case2, "GasToAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_15_CO2PercentIn = GetOnlySensorData(df_case2, "GasToAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_15_molOut = GetOnlySensorData(df_case2, "GasFromAbsorber:OutletStream.m")
kSpiceAbsorbedCO2_15_CO2PercentOutL = GetOnlySensorData(df_case2, "GasFromAbsorber:OutputCompositionVector[2]")
kSpiceAbsorbedCO2_15_CO2PercentOutG = GetOnlySensorData(df_case2, "GasFromAbsorber:OutputCompositionVector[4]")

kSpiceAbsorbedCO2_15_CO2 = (kSpiceAbsorbedCO2_15_molIn*(kSpiceAbsorbedCO2_15_CO2PercentIn/100)-(kSpiceAbsorbedCO2_15_molOut*((kSpiceAbsorbedCO2_15_CO2PercentOutG+kSpiceAbsorbedCO2_15_CO2PercentOutL)/100)))/1000

# b) Desorbed CO2
pilotDesorbedCO2_15 = pd.read_csv("fig15b_Pilot_E.csv", sep=";", decimal=",", names=["time","co2"])
pilotDesorbedCO2_15_time = pilotDesorbedCO2_15["time"]
pilotDesorbedCO2_15_CO2 = pilotDesorbedCO2_15["co2"]

kSpiceDesorbedCO2_15_time = GetOnlySensorData(df_case2, "AdjustedTime")
kSpiceDesorbedCO2_15_molIn = GetOnlySensorData(df_case2, "RichAmine:OutletStream.m")
kSpiceDesorbedCO2_15_CO2PercentInL = GetOnlySensorData(df_case2, "RichAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_15_CO2PercentInG = GetOnlySensorData(df_case2, "RichAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_15_molOut = GetOnlySensorData(df_case2, "LeanAmine:OutletStream.m")
kSpiceDesorbedCO2_15_CO2PercentOutG = GetOnlySensorData(df_case2, "LeanAmine:OutputCompositionVector[2]")
kSpiceDesorbedCO2_15_CO2PercentOutL = GetOnlySensorData(df_case2, "LeanAmine:OutputCompositionVector[4]")
kSpiceDesorbedCO2_15_CO2 = (kSpiceDesorbedCO2_15_molIn*((kSpiceDesorbedCO2_15_CO2PercentInL + kSpiceDesorbedCO2_15_CO2PercentInG)/100) - (kSpiceDesorbedCO2_15_molOut*(kSpiceDesorbedCO2_15_CO2PercentOutG + kSpiceDesorbedCO2_15_CO2PercentOutL)/100))/1000

# Plot fig15
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig15a
axes[0].plot(pilotAbsorbedCO2_15_time, pilotAbsorbedCO2_15_CO2,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot')

axes[0].plot(kSpiceAbsorbedCO2_15_time, kSpiceAbsorbedCO2_15_CO2,
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

# Plot fig15b
axes[1].plot(pilotDesorbedCO2_15_time, pilotDesorbedCO2_15_CO2,
             linestyle='--',
             linewidth=2,
             color='black',
             label='Pilot')

axes[1].plot(kSpiceDesorbedCO2_15_time, kSpiceDesorbedCO2_15_CO2,
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

plt.tight_layout()
plt.savefig("plots/fig15.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig16 - Absorber Temperature
# a) Absorber Temperature at start
pilotAbsorberTempStart16_Pilot = pd.read_csv("fig16a_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart16_Pilot_height = pilotAbsorberTempStart16_Pilot["height"]
pilotAbsorberTempStart16_Pilot_temp = pilotAbsorberTempStart16_Pilot["temp"]

pilotAbsorberTempStart16_Pilot_Sump = pd.read_csv("fig16a_Pilot_Sump_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart16_Pilot_Sump_height = pilotAbsorberTempStart16_Pilot_Sump["height"]
pilotAbsorberTempStart16_Pilot_Sump_temp = pilotAbsorberTempStart16_Pilot_Sump["temp"]

pilotAbsorberTempStart16_Pilot_Gas_Out = pd.read_csv("fig16a_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempStart16_Pilot_Gas_Out_height = pilotAbsorberTempStart16_Pilot_Gas_Out["height"]
pilotAbsorberTempStart16_Pilot_Gas_Out_temp = pilotAbsorberTempStart16_Pilot_Gas_Out["temp"]


kSpiceAbsorberTempStart16 = [
    [0.103371, GetSingleSensorData(df_case2, "00TA001:MeasuredValue", 35)],
    [0.458427, GetSingleSensorData(df_case2, "00TA002:MeasuredValue", 35)],
    [0.813483, GetSingleSensorData(df_case2, "00TA003:MeasuredValue", 35)],
    [1.16854, GetSingleSensorData(df_case2, "00TA004:MeasuredValue", 35)],
    [2.23371, GetSingleSensorData(df_case2, "00TA005:MeasuredValue", 35)],
    [3.30337, GetSingleSensorData(df_case2, "00TA006:MeasuredValue", 35)],
    [3.66292, GetSingleSensorData(df_case2, "00TA007:MeasuredValue", 35)],
    [4.02247, GetSingleSensorData(df_case2, "00TI015:MeasuredValue", 35)],
    ]
kSpiceAbsorberTempStart16_height = [point[0] for point in kSpiceAbsorberTempStart16]
kSpiceAbsorberTempStart16_temp = [point[1] for point in kSpiceAbsorberTempStart16]

kSpiceAbsorberTempStart16_Sump = [[0.0, GetSingleSensorData(
    df_case2, "00TA000:MeasuredValue", 35)]]
kSpiceAbsorberTempStart16_Sump_height = [point[0] for point in kSpiceAbsorberTempStart16_Sump]
kSpiceAbsorberTempStart16_Sump_temp = [point[1] for point in kSpiceAbsorberTempStart16_Sump]

kSpiceAbsorberTempStart16_Gas_Out = [[4.230, GetSingleSensorData(
    df_case2, "00TI003:MeasuredValue", 35)]]
kSpiceAbsorberTempStart16_Gas_Out_height = [point[0] for point in kSpiceAbsorberTempStart16_Gas_Out]
kSpiceAbsorberTempStart16_Gas_Out_temp = [point[1] for point in kSpiceAbsorberTempStart16_Gas_Out]



# b) Absorber Temperature at end
pilotAbsorberTempEnd16_Pilot = pd.read_csv("fig16b_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd16_Pilot_height = pilotAbsorberTempEnd16_Pilot["height"]
pilotAbsorberTempEnd16_Pilot_temp = pilotAbsorberTempEnd16_Pilot["temp"]

pilotAbsorberTempEnd16_Pilot_Sump = pd.read_csv("fig16b_Pilot_Sump_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd16_Pilot_Sump_height = pilotAbsorberTempEnd16_Pilot_Sump["height"]
pilotAbsorberTempEnd16_Pilot_Sump_temp = pilotAbsorberTempEnd16_Pilot_Sump["temp"]

pilotAbsorberTempEnd16_Pilot_Gas_Out = pd.read_csv("fig16b_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotAbsorberTempEnd16_Pilot_Gas_Out_height = pilotAbsorberTempEnd16_Pilot_Gas_Out["height"]
pilotAbsorberTempEnd16_Pilot_Gas_Out_temp = pilotAbsorberTempEnd16_Pilot_Gas_Out["temp"]

kSpiceAbsorberTempEnd16 = [
    [0.103371, GetSingleSensorData(df_case2, "00TA001:MeasuredValue", -1)],
    [0.458427, GetSingleSensorData(df_case2, "00TA002:MeasuredValue", -1)],
    [0.813483, GetSingleSensorData(df_case2, "00TA003:MeasuredValue", -1)],
    [1.16854, GetSingleSensorData(df_case2, "00TA004:MeasuredValue", -1)],
    [2.23371, GetSingleSensorData(df_case2, "00TA005:MeasuredValue", -1)],
    [3.30337, GetSingleSensorData(df_case2, "00TA006:MeasuredValue", -1)],
    [3.66292, GetSingleSensorData(df_case2, "00TA007:MeasuredValue", -1)],
    [4.02247, GetSingleSensorData(df_case2, "00TI015:MeasuredValue", -1)],
    ]
kSpiceAbsorberTempEnd16_height = [point[0] for point in kSpiceAbsorberTempEnd16]
kSpiceAbsorberTempEnd16_temp = [point[1] for point in kSpiceAbsorberTempEnd16]

kSpiceAbsorberTempEnd16_Sump = [[0.0, GetSingleSensorData(
    df_case2, "00TA000:MeasuredValue", -1)]]
kSpiceAbsorberTempEnd16_Sump_height = [point[0] for point in kSpiceAbsorberTempEnd16_Sump]
kSpiceAbsorberTempEnd16_Sump_temp = [point[1] for point in kSpiceAbsorberTempEnd16_Sump]

kSpiceAbsorberTempEnd16_Gas_Out = [[4.230, GetSingleSensorData(
    df_case2, "00TI003:MeasuredValue", -1)]]
kSpiceAbsorberTempEnd16_Gas_Out_height = [point[0] for point in kSpiceAbsorberTempEnd16_Gas_Out]
kSpiceAbsorberTempEnd16_Gas_Out_temp = [point[1] for point in kSpiceAbsorberTempEnd16_Gas_Out]

# Plot fig16
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig16a
axes[0].scatter(pilotAbsorberTempStart16_Pilot_height, pilotAbsorberTempStart16_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[0].scatter(kSpiceAbsorberTempStart16_height, kSpiceAbsorberTempStart16_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice')

axes[0].scatter(pilotAbsorberTempStart16_Pilot_Sump_height, pilotAbsorberTempStart16_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[0].scatter(kSpiceAbsorberTempStart16_Sump_height, kSpiceAbsorberTempStart16_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump')

axes[0].scatter(pilotAbsorberTempStart16_Pilot_Gas_Out_height, pilotAbsorberTempStart16_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceAbsorberTempStart16_Gas_Out_height, kSpiceAbsorberTempStart16_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[0].set_xlabel("Høyde [m]")
axes[0].set_ylabel("Temperatur i absorber [°C]")
axes[0].set_xlim(-0.02, 4.3)
axes[0].set_ylim(0, 70)
axes[0].legend()
axes[0].set_title("a)", loc="left")

# Plot fig16b
axes[1].scatter(pilotAbsorberTempEnd16_Pilot_height, pilotAbsorberTempEnd16_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[1].scatter(kSpiceAbsorberTempEnd16_height, kSpiceAbsorberTempEnd16_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice')

axes[1].scatter(pilotAbsorberTempEnd16_Pilot_Sump_height, pilotAbsorberTempEnd16_Pilot_Sump_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot sump')

axes[1].scatter(kSpiceAbsorberTempEnd16_Sump_height, kSpiceAbsorberTempEnd16_Sump_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice sump')

axes[1].scatter(pilotAbsorberTempEnd16_Pilot_Gas_Out_height, pilotAbsorberTempEnd16_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceAbsorberTempEnd16_Gas_Out_height, kSpiceAbsorberTempEnd16_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i absorber [°C]")
axes[1].set_xlim(-0.02, 4.3)
axes[1].set_ylim(0, 70)
axes[1].legend()
axes[1].set_title("b)", loc="left")

plt.tight_layout()
plt.savefig("plots/fig16.png", dpi=300, bbox_inches='tight')
plt.show()

#%% fig17 - Desorber Temperature
#a) Desorber Temperature at start
pilotDesorberTempStart17_Pilot = pd.read_csv("fig17a_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart17_Pilot_height = pilotDesorberTempStart17_Pilot["height"]
pilotDesorberTempStart17_Pilot_temp = pilotDesorberTempStart17_Pilot["temp"]

pilotDesorberTempStart17_Pilot_Reboiler = pd.read_csv("fig17a_Pilot_Reboiler_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart17_Pilot_Reboiler_height = pilotDesorberTempStart17_Pilot_Reboiler["height"]
pilotDesorberTempStart17_Pilot_Reboiler_temp = pilotDesorberTempStart17_Pilot_Reboiler["temp"]

pilotDesorberTempStart17_Pilot_Solvent_In = pd.read_csv("fig17a_Pilot_Solvent_In_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart17_Pilot_Solvent_In_height = pilotDesorberTempStart17_Pilot_Solvent_In["height"]
pilotDesorberTempStart17_Pilot_Solvent_In_temp = pilotDesorberTempStart17_Pilot_Solvent_In["temp"]

pilotDesorberTempStart17_Pilot_Gas_Out = pd.read_csv("fig17a_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempStart17_Pilot_Gas_Out_height = pilotDesorberTempStart17_Pilot_Gas_Out["height"]
pilotDesorberTempStart17_Pilot_Gas_Out_temp = pilotDesorberTempStart17_Pilot_Gas_Out["temp"]

kSpiceDesorberTempStart17 = [
    [0.100425, GetSingleSensorData(df_case2, "01TS001:MeasuredValue", 35)],
    [1.04888, GetSingleSensorData(df_case2, "01TS002:MeasuredValue", 35)],
    [2.00106, GetSingleSensorData(df_case2, "01TS003:MeasuredValue", 35)],
    [2.9458, GetSingleSensorData(df_case2, "01TS004:MeasuredValue", 35)],
    [3.56695, GetSingleSensorData(df_case2, "01TS005:MeasuredValue", 35)]
    ]
kSpiceDesorberTempStart17_height = [point[0] for point in kSpiceDesorberTempStart17]
kSpiceDesorberTempStart17_temp = [point[1] for point in kSpiceDesorberTempStart17]

kSpiceDesorberTempStart17_Reboiler = [[0.0, GetSingleSensorData(
    df_case2, "02TI010:MeasuredValue", 35)]]
kSpiceDesorberTempStart17_Reboiler_height = [point[0] for point in kSpiceDesorberTempStart17_Reboiler]
kSpiceDesorberTempStart17_Reboiler_temp = [point[1] for point in kSpiceDesorberTempStart17_Reboiler]

kSpiceDesorberTempStart17_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case2, "01TI007:MeasuredValue", 35)]]
kSpiceDesorberTempStart17_Solvent_In_height = [point[0] for point in kSpiceDesorberTempStart17_Solvent_In]
kSpiceDesorberTempStart17_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempStart17_Solvent_In]

kSpiceDesorberTempStart17_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case2, "GasFromDesorber:OutletStream.t", 35)]]
kSpiceDesorberTempStart17_Gas_Out_height = [point[0] for point in kSpiceDesorberTempStart17_Gas_Out]
kSpiceDesorberTempStart17_Gas_Out_temp = [point[1] for point in kSpiceDesorberTempStart17_Gas_Out]

# b) Desorber Temperature at end
pilotDesorberTempEnd17_Pilot = pd.read_csv("fig17b_Pilot_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd17_Pilot_height = pilotDesorberTempEnd17_Pilot["height"]
pilotDesorberTempEnd17_Pilot_temp = pilotDesorberTempEnd17_Pilot["temp"]

pilotDesorberTempEnd17_Pilot_Reboiler = pd.read_csv("fig17b_Pilot_Reboiler_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd17_Pilot_Reboiler_height = pilotDesorberTempEnd17_Pilot_Reboiler["height"]
pilotDesorberTempEnd17_Pilot_Reboiler_temp = pilotDesorberTempEnd17_Pilot_Reboiler["temp"]

pilotDesorberTempEnd17_Pilot_Solvent_In = pd.read_csv("fig17b_Pilot_Solvent_In_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd17_Pilot_Solvent_In_height = pilotDesorberTempEnd17_Pilot_Solvent_In["height"]
pilotDesorberTempEnd17_Pilot_Solvent_In_temp = pilotDesorberTempEnd17_Pilot_Solvent_In["temp"]

pilotDesorberTempEnd17_Pilot_Gas_Out = pd.read_csv("fig17b_Pilot_Gas_Out_E.csv", sep=";", decimal=",", names=["height","temp"])
pilotDesorberTempEnd17_Pilot_Gas_Out_height = pilotDesorberTempEnd17_Pilot_Gas_Out["height"]
pilotDesorberTempEnd17_Pilot_Gas_Out_temp = pilotDesorberTempEnd17_Pilot_Gas_Out["temp"]

kSpiceDesorberTempEnd17 = [
    [0.100425, GetSingleSensorData(df_case2, "01TS001:MeasuredValue", -1)],
    [1.04888, GetSingleSensorData(df_case2, "01TS002:MeasuredValue", -1)],
    [2.00106, GetSingleSensorData(df_case2, "01TS003:MeasuredValue", -1)],
    [2.9458, GetSingleSensorData(df_case2, "01TS004:MeasuredValue", -1)],
    [3.56695, GetSingleSensorData(df_case2, "01TS005:MeasuredValue", -1)]
    ]
kSpiceDesorberTempEnd17_height = [point[0] for point in kSpiceDesorberTempEnd17]
kSpiceDesorberTempEnd17_temp = [point[1] for point in kSpiceDesorberTempEnd17]

kSpiceDesorberTempEnd17_Reboiler = [[0.0, GetSingleSensorData(
    df_case2, "02TI010:MeasuredValue", -1)]]
kSpiceDesorberTempEnd17_Reboiler_height = [point[0] for point in kSpiceDesorberTempEnd17_Reboiler]
kSpiceDesorberTempEnd17_Reboiler_temp = [point[1] for point in kSpiceDesorberTempEnd17_Reboiler]

kSpiceDesorberTempEnd17_Solvent_In = [[3.56695, GetSingleSensorData(
    df_case2, "01TI007:MeasuredValue", -1)]]
kSpiceDesorberTempEnd17_Solvent_In_height = [point[0] for point in kSpiceDesorberTempEnd17_Solvent_In]
kSpiceDesorberTempEnd17_Solvent_In_temp = [point[1] for point in kSpiceDesorberTempEnd17_Solvent_In]

kSpiceDesorberTempEnd17_Gas_Out = [[3.56695, GetSingleSensorData(
    df_case2, "GasFromDesorber:OutletStream.t", -1)]]
kSpiceDesorberTempEnd17_Gas_Out_height = [point[0] for point in kSpiceDesorberTempEnd17_Gas_Out]
kSpiceDesorberTempEnd17_Gas_Out_temp = [point[1] for point in kSpiceDesorberTempEnd17_Gas_Out]

#Plot fig17
fig, axes = plt.subplots(1, 2, figsize=(22, 7))

# Plot fig17a
axes[0].scatter(pilotDesorberTempStart17_Pilot_height, pilotDesorberTempStart17_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[0].scatter(kSpiceDesorberTempStart17_height, kSpiceDesorberTempStart17_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice')

axes[0].scatter(pilotDesorberTempStart17_Pilot_Reboiler_height, pilotDesorberTempStart17_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[0].scatter(kSpiceDesorberTempStart17_Reboiler_height, kSpiceDesorberTempStart17_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler')

axes[0].scatter(pilotDesorberTempStart17_Pilot_Solvent_In_height, pilotDesorberTempStart17_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[0].scatter(kSpiceDesorberTempStart17_Solvent_In_height, kSpiceDesorberTempStart17_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in')

axes[0].scatter(pilotDesorberTempStart17_Pilot_Gas_Out_height, pilotDesorberTempStart17_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[0].scatter(kSpiceDesorberTempStart17_Gas_Out_height, kSpiceDesorberTempStart17_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[0].set_xlabel("Høyde [m]")
axes[0].set_ylabel("Temperatur i desorber [°C]")
axes[0].set_xlim(-0.02, 3.6)
axes[0].set_ylim(80, 125)
axes[0].legend()
axes[0].set_title("a)", loc="left")


# Plot fig17b
axes[1].scatter(pilotDesorberTempEnd17_Pilot_height, pilotDesorberTempEnd17_Pilot_temp,
                marker='o',
                color='black',
                facecolors="none",
                label='Pilot')

axes[1].scatter(kSpiceDesorberTempEnd17_height, kSpiceDesorberTempEnd17_temp,
                marker='o',
                color='black',
                facecolors="black",
                label='K-Spice')

axes[1].scatter(pilotDesorberTempEnd17_Pilot_Reboiler_height, pilotDesorberTempEnd17_Pilot_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="none",
                label='Pilot reboiler')

axes[1].scatter(kSpiceDesorberTempEnd17_Reboiler_height, kSpiceDesorberTempEnd17_Reboiler_temp,
                marker='s',
                color='black',
                facecolors="black",
                label='K-Spice reboiler')

axes[1].scatter(pilotDesorberTempEnd17_Pilot_Solvent_In_height, pilotDesorberTempEnd17_Pilot_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="none",
                label='Pilot solvent in')

axes[1].scatter(kSpiceDesorberTempEnd17_Solvent_In_height, kSpiceDesorberTempEnd17_Solvent_In_temp,
                marker='d',
                color='black',
                facecolors="black",
                label='K-Spice solvent in')

axes[1].scatter(pilotDesorberTempEnd17_Pilot_Gas_Out_height, pilotDesorberTempEnd17_Pilot_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="none",
                label='Pilot gass ut')

axes[1].scatter(kSpiceDesorberTempEnd17_Gas_Out_height, kSpiceDesorberTempEnd17_Gas_Out_temp,
                marker='v',
                color='black',
                facecolors="black",
                label='K-Spice gass ut')

axes[1].set_xlabel("Høyde [m]")
axes[1].set_ylabel("Temperatur i desorber [°C]")
axes[1].set_xlim(-0.02, 3.6)
axes[1].set_ylim(80, 125)
axes[1].legend()
axes[1].set_title("b)", loc="left")


plt.tight_layout()
plt.savefig("plots/fig17.png", dpi=300, bbox_inches='tight')
plt.show()





