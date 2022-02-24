#!/usr/bin/env python3
import serial


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            Str = ser.readline().decode('ascii').rstrip()
            Temp = float(Str[Str.find(":")+1:Str.find("Celsius")])
            Smoke = int(Str[Str.find("Smoke:") + 6:Str.find("PPM")])
            Flame = int(Str[Str.find("Flame:")+6:Str.find("Volt")])
            print(Str)
            print(Temp)
            print(Smoke)
            print(Flame)        
            
