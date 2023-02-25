# This code uses the model established for the manuscript to plot the graph at different values of a given target variable from those listed below:
''' 
USER-DEFINED SECTION 
This block contains variables that the user is meant to manipulate.
'''

Digest = False

V = 280 # Reactor Volume per CM
N_supply = 0 # Starting N supply (does not alter results. Is a hypothetical starting point for N supplies)
N_Diet = 14 # Nitrogen Demand (g per CM per day)
'''
System Variables: Note that Position 1 of each list signifies the original value, while Position 2 is used in 
the actual calculation
'''
eff = 0.90
eff2 = 0.90
a = 1.65
r = [0.013, 0.013, "Rate of Nitrogen Fixation (r)"]
eta_H = [0.5, 0.5, "Harvesting Index / Efficiency ($\u03B7_{H}$)"]
eta_B = [0.8, 0.8, "Nitrogen Harvestable from Bioreactor ($\u03B7_{B}$)"]
eta_F = [1.00, eff, "Fertilization Efficiency ($\u03B7_{F}$)"]
eta_AE = [0.5, eff2, "Aerobic (AN) Digester Efficiency ($\u03B7_{AE}$)"]
eta_AN = [0.75, eff2, "Anaerobic (AN) Digester Efficiency ($\u03B7_{AN}$)"]
eta_U = [1.0, 1.0, "Urine Nitrogen Recycling Efficiency ($\u03B7_{U}$)"]
W_c = [0.80, 0.80, "Fraction of Inedible Crop to Aerobic\nDigestion ($W_{C}$)"]
W_w = [0.50, 0.50, "Fraction of Feces to \nAerobic Digestion ($W_{W}$)"]
W_f = [0.20, 0.20, "Fraction of Human Waste Nitrogen to\nFeces ($W_{F}$)"]
N_D = [14, N_Diet, 'Nitrogen Demand (g per CM per day)']


try:
    TargetVariable = eta_B # Selects which variable you want to be analyzed in the figure
except:
    print("Invalid TargetVariable Selected. Please list the exact variable name from the System Variables list.")
''' --- MAIN CODE --- '''
    

target = TV = TVariable = TargetVariable
import numpy as np
import random as ran
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math as m
from colour import Color
from labellines import labelLine, labelLines


def graphing(x, placeholder, names, n, TV, q):
    fig, ax1 = plt.subplots()
    Color1 = Color('Red')
    Color2 = Color('Black')
    holder_palette = list(Color1.range_to(Color2, len(names)))
    palate = []
    
    for current_color in holder_palette:
        palate.append(current_color.hex_l)
    
    for i in range(0, len(placeholder)):

        if i != n:
            ax1.plot(x, placeholder[i], color=palate[len(names) - 1 - i], label = names[i])
        else:
            ax1.plot(x, placeholder[i], color='b', label = 'names[i]')
            #print(placeholder[4][365])


    ax1.set_xlabel('Time (Years)', fontsize = 14)
    ax1.set_ylabel('\u0394N (kg)', color='k', fontsize = 14)
    ax1.set_ylim([-30, 50])
    ax1.set_xlim([-0.01, 1])
    ax1.legend(reversed(plt.legend().legendHandles), reversed(placeholderNames), prop={'size': 12}, loc=2)
    ax1.tick_params(labelsize=13)
    
    plt.title(label=TV, 
              fontweight=10, 
              fontsize=16,
              horizontalalignment='left',
              loc='left')


def eta_(X, eta_AE, eta_AN):
    return (eta_AE[1]*X + eta_AN[1]*(1-X))




variables = [r, eta_B, eta_F, eta_H, eta_AE, eta_AN, eta_U, W_c, W_w, W_f]
variables = [W_c, W_w, W_f]



if Digest == False:
    Z = 0
else:
    Z = 1

if target == r or target == a:
    isEta = False
else:
    isEta = True
if target == W_w or target == W_f or target == W_c:
    isW = True
else:
    isW = False


mission_duration = 1

crew = [10, 10]
plt.rcParams['figure.dpi'] = 1000
V_true = [V * crew[1], V * crew[1]]

m_d = [mission_duration * 365, mission_duration * 365]
N_s = [N_supply, N_supply]
dt = 1 # day
units = int(m_d[1]/dt) + 1

scale100 = np.eye(units, 2)
scale80 = np.eye(units, 2)
scale60 = np.eye(units, 2)
scale40 = np.eye(units, 2)
scale20 = np.eye(units, 2)
scale0 = np.eye(units, 2)
scaleNom = np.eye(units, 2)

scales = [scale0, scale20, scale40, scale60, scale80, scale100, scaleNom]

yLabels = []
MRVs = []
for i in range(units):
    for j in range(2):
        if j == 0:
            for k in range(0, len(scales)):
                scales[k][i][j] = i/365
        elif j == 1 and i == 0:
            for k in range(0, len(scales)):
                scales[k][i][j] = N_s[1]
        elif j == 1 and i > 0:
            for scale in range(len(scales)):
                if scale == len(scales) - 1:
                    TVariable[1] = TVariable[0]
                else:
                    if isEta == True:
                        TVariable[1] = scale * 0.2
                    elif isEta == False:
                        
                        doNothing = True
                        
                        if scale == 0:
                            TVariable[1] = TVariable[0] * 0.25
                        elif scale == 1:
                            TVariable[1] = TVariable[0] * 0.5
                        elif scale == 2:
                            TVariable[1] = TVariable[0] * 1.5
                        elif scale == 3:
                            TVariable[1] = TVariable[0] * 2.0
                        elif scale == 4:
                            TVariable[1] = TVariable[0] * 2.5
                        elif scale == 5:
                            TVariable[1] = TVariable[0] * 3.0
                    
                            
                if eta_F[1] == 0:
                    eta_F[1] = 0.001
                if eta_H[1] == 0:
                    eta_H[1] = 0.001
                if eta_B[1] == 0:
                    eta_B[1] = 0.001
                #W_c[1] = 0.8
                #print(eta_(W_c[1], eta_AE, eta_AN))
                N_in = a * r[1] * V_true[1] * eta_B[1] * (eta_(W_c[1], eta_AE, eta_AN))**Z
                N_rec = N_D[1]*( eta_(W_c[1], eta_AE, eta_AN) * ( 1 / eta_H[1] - 1) + W_f[1] * (eta_(W_w[1], eta_AE, eta_AN)) + eta_U[1] * (1 - W_f[1]))
                N_out = N_D[1] / (eta_F[1] * eta_H[1]) + Z * (N_D[1]) * eta_U[1] * (1 - W_f[1]) * (1-eta_(0.8, eta_AE, eta_AN)) 
                
               
                MRV_COMNFR = -(N_rec - N_out)/ (a * r[1] * eta_B[1] * (eta_(W_c[1], eta_AE, eta_AN))**Z)
                if MRV_COMNFR not in MRVs:
                    MRVs.append(MRV_COMNFR)
                
                
                scales[scale][i][j] = round(scales[scale][i-1][j] + dt * (N_in + crew[1] * (N_rec - N_out)) / 1000, 3)
print("Selected Variable:\t"+TV[2])
if Z == 0:
    print("\t\t\t\t\tNo Digestion")
else:
    print("Digestion:")
print("Minimal MRV:\t\t"+str(round(min(MRVs),0)), "\nMaximal MRV:\t\t"+str(round(max(MRVs),0)))
#print(MRVs[1:4])
influence = round(max(MRVs) - min(MRVs),0)
print("Influence:\t\t\t"+str(influence))
#print(N_rec, N_out)
x = [scales[0][i][0] for i in range(units)]
scale0y = [scales[0][i][j] for i in range(units)]
scale20y = [scales[1][i][j] for i in range(units)]
scale40y = [scales[2][i][j] for i in range(units)]
scale60y = [scales[3][i][j] for i in range(units)]
scale80y = [scales[4][i][j] for i in range(units)]
scale100y = [scales[5][i][j] for i in range(units)]
scaleNomy = [scales[6][i][j] for i in range(units)]

#print(scaleNomy[365]+60)

p1, p2, p3, p4, p5, p6, p7 = 0, 0, 0, 0, 0, 0, 0
n1, n2, n3, n4, n5, n6, n7 = None, None, None, None, None, None, None

p1 = scale0y
scaleFixed = [scale0y, scale20y, scale40y, scale60y, scale80y, scale100y]
if isEta == True:
    scaleNames = ["0%", "20%", "40%", "60%", "80%", "100%"]
    nomName = str(int(round(TVariable[1] * 100, 0)))+'%'
else:
    scaleNames = ["0.25x", "0.50x", "1.5x", "2.0x", "2.5x", "3.0x"]
    nomName = str(int(round(TVariable[1] * 100, 0)))+'.0x'

placeholder = [p1, p2, p3, p4, p5, p6, p7]
placeholderNames = [n1, n2, n3, n4, n5, n6, n7]

n = 0

#print(scaleNomy[units - 1], scaleFixed[n+1][units - 1])

while scaleNomy[units - 1] >= scaleFixed[n+1][units - 1]:
    n += 1
    overlap = [False, n]
    if scaleNomy[units - 1] == scaleFixed[n][units - 1]:
        overlap = [True, n]
        break
if n == 0:
    overlap = [False, n]
for i in range(len(placeholder)):
    if i == n:
        placeholder[i] = scaleNomy
        placeholderNames[i] = nomName
    elif i < n:
        placeholder[i] = scaleFixed[i]
        placeholderNames[i] = scaleNames[i]
    elif i > n:
        placeholder[i] = scaleFixed[i-1]
        placeholderNames[i] = scaleNames[i - 1]

if TV == eta_AE or TV == eta_AN or TV == eta_F or TV == r:
    if TV == r:
        minus = 3
        upper = '1.0x'
        lower = '0.5x'
    else:
        upper = '95%'
        lower = '80%'
        minus = 0
    mid = placeholder[5 - minus]
    placeholder[5- minus] = placeholder[4 - minus] 
    placeholder[4- minus] = mid
    placeholderNames[5 - minus] = upper
    placeholderNames[4 - minus] = lower
    n += 1

if TV == eta_H:
    minus = 2
    mid = placeholder[5 - minus]
    placeholder[5- minus] = placeholder[4 - minus] 
    placeholder[4- minus] = mid
    placeholderNames[5 - minus] = '50%'
    placeholderNames[4 - minus] = '40%'
    n += 1


if overlap[0] == True:
    placeholder.pop(n)
    placeholderNames.pop(n)

graphing(x, placeholder, placeholderNames, n, TV[2], i)


#plt.legend(reversed(plt.legend().legendHandles), reversed(placeholderNames), prop={'size': 9}, loc=2)
plt.show()





