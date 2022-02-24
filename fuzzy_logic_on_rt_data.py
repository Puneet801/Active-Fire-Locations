import numpy as np
import skfuzzy as fzy
from skfuzzy import control as ctrl
import time
import serial
import matplotlib as plt


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()

# sd - smoke density
sd = ctrl.Antecedent(np.arange(0,100,1),'sd')
sd['Low'] = fzy.trapmf(sd.universe, [0,0,30,40])
sd['Medium'] = fzy.trapmf(sd.universe, [30,40,60,70])
sd['High'] = fzy.trapmf(sd.universe, [60,75,100,100])

#sd.view()

# temp - temperature
temp = ctrl.Antecedent(np.arange(0,100,1),'temp')
temp['Cold'] = fzy.trapmf(temp.universe, [0,0,10,25])
temp['Normal'] = fzy.trapmf(temp.universe, [10,20,30,40])
temp['Hot'] = fzy.trapmf(temp.universe, [25,40,100,100])

#temp.view()

flame = ctrl.Antecedent(np.arange(0,1000,1),'flame')
flame['Far'] = fzy.trapmf(flame.universe, [0,0,300,400])
flame['Not far'] = fzy.trapmf(flame.universe,[300,400,600,700])
flame['Near'] = fzy.trapmf(flame.universe,[600,700,1000,1000])

#flame.view()

fire = ctrl.Consequent(np.arange(1,10,1),'fire')

fire.automf(3, names=['Low','Medium','High'])

#fire.view()

from skfuzzy.control import ControlSystem,ControlSystemSimulation,Rule

rule1 = Rule(sd['Low'] & temp['Cold'] & flame['Far'], fire['Low'])
rule2 = Rule(sd['Low'] & temp['Cold'] & flame['Not far'], fire['Low'])
rule3 = Rule(sd['Low'] & temp['Cold'] & flame['Near'], fire['Low'])
rule4 = Rule(sd['Low'] & temp['Normal'] & flame['Far'], fire['Low'])
rule5 = Rule(sd['Low'] & temp['Normal'] & flame['Not far'], fire['Low'])
rule6 = Rule(sd['Low'] & temp['Normal'] & flame['Near'], fire['Low'])
rule7 = Rule(sd['Low'] & temp['Hot'] & flame['Far'], fire['Low'])
rule8 = Rule(sd['Low'] & temp['Hot'] & flame['Not far'], fire['Low'])
rule9 = Rule(sd['Low'] & temp['Hot'] & flame['Near'], fire['Medium'])

rule10 = Rule(sd['Medium'] & temp['Cold'] & flame['Far'], fire['Low'])
rule11 = Rule(sd['Medium'] & temp['Cold'] & flame['Not far'], fire['Low'])
rule12 = Rule(sd['Medium'] & temp['Cold'] & flame['Near'], fire['Low'])
rule13 = Rule(sd['Medium'] & temp['Normal'] & flame['Far'], fire['Low'])
rule14 = Rule(sd['Medium'] & temp['Normal'] & flame['Not far'], fire['Low'])
rule15 = Rule(sd['Medium'] & temp['Normal'] & flame['Near'], fire['Low'])
rule16 = Rule(sd['Medium'] & temp['Hot'] & flame['Far'], fire['Medium'])
rule17 = Rule(sd['Medium'] & temp['Hot'] & flame['Not far'], fire['Medium'])
rule18 = Rule(sd['Medium'] & temp['Hot'] & flame['Near'], fire['High'])

rule19 = Rule(sd['High'] & temp['Cold'] & flame['Far'], fire['Medium'])
rule20 = Rule(sd['High'] & temp['Cold'] & flame['Not far'], fire['Medium'])
rule21 = Rule(sd['High'] & temp['Cold'] & flame['Near'], fire['High'])
rule22 = Rule(sd['High'] & temp['Normal'] & flame['Far'], fire['Medium'])
rule23 = Rule(sd['High'] & temp['Normal'] & flame['Not far'], fire['High'])
rule24 = Rule(sd['High'] & temp['Normal'] & flame['Near'], fire['High'])
rule25 = Rule(sd['High'] & temp['Hot'] & flame['Far'], fire['High'])
rule26 = Rule(sd['High'] & temp['Hot'] & flame['Not far'], fire['High'])
rule27 = Rule(sd['High'] & temp['Hot'] & flame['Near'], fire['High'])

rules_ctrl = ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,
                            rule10,rule11,rule12,rule13,rule14,rule15,rule16,rule17,rule18,
                            rule19,rule20,rule21,rule22,rule23,rule24,rule25,rule26,rule27])
fire_rslt = ControlSystemSimulation(rules_ctrl)

while True:
    if ser.in_waiting > 0:
        
        Str = ser.readline().decode('ascii').rstrip()
        Temp = float(Str[Str.find(":")+1:Str.find("Celsius")])
        Smoke = int(Str[Str.find("Smoke:") + 6:Str.find("PPM")])
        Flame = int(Str[Str.find("Flame:")+6:Str.find("Volt")])
        fire_rslt.input['sd'] = Smoke/100
        fire_rslt.input['temp'] = Temp
        fire_rslt.input['flame'] = Flame
        fire_rslt.compute()
        print('{:.1f}'.format(fire_rslt.output['fire']))
        time.sleep(3)
        

# plt.figure(figsize=(10,8))
# plt.plot(range(30),fire_output)
# plt.ylabel('Fire Output')

# fire_rslt.input['sd'] = 75
# fire_rslt.input['temp'] = 40
# fire_rslt.input['flame'] = 700

# fire_rslt.compute()

# print(fire_rslt.output['fire'])

