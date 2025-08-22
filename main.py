from tkinter import *
from tkinter import ttk
from time import sleep

import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware

class UpdateVisitor(Hardware.IVisitor):
    __namespace__ = "Stove"
    def VisitComputer(self, computer):
        computer.Traverse(self)

    def VisitHardware(self, hardware):
        hardware.Update()
        for subHardware in hardware.SubHardware:
            subHardware.Update()

    def VisitParameter(self, parameter):
        pass

    def VisitSensor(self, sensor):
        pass

user = Hardware.Computer()
user.IsCpuEnabled = True
user.IsGpuEnabled = True
user.IsBatteryEnabled = True
user.IsMemoryEnabled = True
user.IsNetworkEnabled = True
user.IsStorageEnabled = True
user.Open()
user.Accept(UpdateVisitor())

array = {}
def getVal(sensor: any, decimalPlaces: int=0):
    return str(round(sensor.Value, decimalPlaces))

def updateArray() -> None:
    for hw in user.Hardware:
        hwType = str(hw.HardwareType).lower()
        if "gpu" in hwType: hwType ="gpu"
        array[hwType] = {"name": hw.Name}

        for sensor in hw.Sensors:
            sName = str(sensor.Name)
            sType = str(sensor.SensorType)

            #temp ----
            if (sName == "Core Average") or \
            (sName == "GPU Core" and sType == "Temperature"): 
                array[hwType]["temp"] = getVal(sensor, 1)

            #usagePercentage ----
            elif (sName == "CPU Total") or \
            (sName == "GPU Core" and sType == "Load") or \
                (sName == "Memory Total"):
                array[hwType]["usagePercentage"] = getVal(sensor, 1)

            #memoryPercentage ----
            elif (sName == "Gpu Core") or \
            (sName == "Memory" and sType == "Load"):
                array[hwType]["memoryPercentage"] = getVal(sensor, 1)
            
            #memorySpecific ----
            elif (sName == "Memory Used"):
                array[hwType]["memorySpecific"] = getVal(sensor, 1)
            
    #del array["gpu"]
    if "gpu" not in array:
        array["gpu"] = {
            "name": "No GPU",
            "temp": "N/A",
            "usage": "N/A"
        }

updateArray()

for hardware in user.Hardware:
    print(f"Hardware: {hardware.Name}")
    for sensor in hardware.Sensors:
        print(f"\tSensor: {sensor.Name}, value: {sensor.Value}, TYPE: {sensor.SensorType}")

main = Tk()
main.title("Stove")
main.geometry("400x150")

frame = ttk.Frame(main)
frame.grid(column=0, row=0)

cpuName = StringVar()
ttk.Label(frame, textvariable=cpuName).grid(column=1, row=0)
cpuName.set(array["cpu"]["usagePercentage"])

gpuName = StringVar()
ttk.Label(frame, textvariable=gpuName).grid(column=2, row=0)
gpuName.set(array["gpu"]["usagePercentage"])

for x in frame.winfo_children():
    x['padding'] = 10

def upd():
    print("a")
    updateArray()
    user.Open()
    user.Accept(UpdateVisitor())
    cpuName.set(array["cpu"]["usagePercentage"])
    gpuName.set(array["gpu"]["usagePercentage"])
    main.update()
    main.after(1000, upd)

main.after(1000, upd)
main.mainloop()