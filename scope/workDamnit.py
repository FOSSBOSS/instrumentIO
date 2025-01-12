#!/usr/bin/env python3
import pyvisa
from time import sleep
def main():
    try:
        rm = pyvisa.ResourceManager('@py')  # Use @py for pyvisa-py backend
        #rm = pyvisa.ResourceManager('@ni')   #Error: 'IVIVisaLibrary' object has no attribute 'viParseRsrcEx'

        instruments = rm.list_resources()
        print(f"Available instruments: {instruments}")
        
        if instruments:
            scope = rm.open_resource(instruments[0])
            print(f"Connected to: {scope.query('*IDN?')}")
            sleep(10)
            # Example SCPI commands
            scope.write(':TIMEBASE:SCALE 0.0001')  # Set timebase to 1 ms
            scope.write(':TIMEBASE:SCALE 0.001')  # Set timebase scale to 1ms/div
            scope.write(':CHANNEL1:DISPLAY ON')   # Enable CH1 display
            scope.write(':CHANNEL2:DISPLAY ON')   # Enable CH2 display
            scope.write(':CHANNEL3:DISPLAY ON')   # Enable CH3 display
            scope.write(':CHANNEL4:DISPLAY ON')   # Enable CH4 display
                   
            scope.write(':CHANNEL1:SCALE 0.5')    # Set CH1 scale to 500mV/div
            scope.write(':TRIGGER:EDGE:SOURCE CHAN1')  # Set trigger source to CH1
            scope.write(':TRIGGER:EDGE:LEVEL 0.0')     # Set trigger level to 0V
            scope.write(':TRIGGER:EDGE:SLOPE POS')     # Set trigger slope to positive
            print(f"Timebase set: {scope.query(':TIMEBASE:SCALE?')}")
            #print(f" {}")
            sleep(5)
            scope.write(':CHANNEL1:DISPLAY OFF')   # Enable CH1 display
            scope.write(':CHANNEL2:DISPLAY OFF')   # Enable CH2 display
            scope.write(':CHANNEL3:DISPLAY OFF')   # Enable CH3 display
            scope.write(':CHANNEL4:DISPLAY OFF')   # Enable CH4 display

            sleep(5)
            scope.close()
        else:
            print("No instruments found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
