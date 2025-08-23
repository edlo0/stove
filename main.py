from tkinter import *
from tkinter import ttk
from time import sleep
import threading

import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware # type: ignore

import psutil as pu

class UpdateVisitor(Hardware.IVisitor): # from repo pyhardwaremonitor's example code
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
user.IsGpuEnabled = True
user.Open()
user.Accept(UpdateVisitor())

print(pu.cpu_percent())

array = {}

df = "TkDefaultFont 18 bold"

main = Tk()
main.title("Stove")
main.option_add('*tearOff', FALSE)

frame = ttk.Frame(main)
frame.grid(column=0, row=0)

cpuFrame = ttk.Labelframe(frame, text="CPU")
cpuFrame.grid(column=0, row=0)
cpuName = StringVar()
ttk.Label(cpuFrame, textvariable=cpuName).grid(column=0, row=0)
cpuTempFrame = ttk.Labelframe(cpuFrame, text="Temperature")
cpuTempFrame.grid(column=0, row=1, sticky=(E, W))
cpuTemp = StringVar()
ttk.Label(cpuTempFrame, textvariable=cpuTemp, font=df).grid(column=0, row=0)
cpuLoadFrame = ttk.Labelframe(cpuFrame, text="Load")
cpuLoadFrame.grid(column=0, row=2, sticky=(E, W))
cpuLoad = StringVar()
ttk.Label(cpuLoadFrame, textvariable=cpuLoad, font=df).grid(column=0, row=0)

gpuFrame = ttk.Labelframe(frame, text="GPU")
gpuFrame.grid(column=1, row=0)
gpuName = StringVar()
ttk.Label(gpuFrame, textvariable=gpuName).grid(column=0, row=0)
gpuTempFrame = ttk.Labelframe(gpuFrame, text="Temperature")
gpuTempFrame.grid(column=0, row=1, sticky=(E, W))
gpuTemp = StringVar()
ttk.Label(gpuTempFrame, textvariable=gpuTemp, font=df).grid(column=0, row=0)
gpuLoadFrame = ttk.Labelframe(gpuFrame, text="Load")
gpuLoadFrame.grid(column=0, row=2, sticky=(E, W))
gpuLoad = StringVar()
ttk.Label(gpuLoadFrame, textvariable=gpuLoad, font=df).grid(column=0, row=0)

bottomBar = ttk.Frame()
bottomBar.grid(column=1, row=1, columnspan=2)
button1 = ttk.Button(text="asdasd")
button1.grid(column=0, row=0)

for x in frame.winfo_children():
    x['padding'] = 10
    

def updateSensors():
    while True:
        user.Open()
        user.Accept(UpdateVisitor())
        sleep(1)

"""
psutil:
-all cpu info
-all memory info
-all storage info
-all network info
librehardwaremonitorlib:
-all gpu info
"""

def rnd(num, places) -> str:
    return str(round(num, places))

def updateArray() -> None:
    card = user.Hardware[0]
    array["gpu"] = {}
    for sensor in card.Sensors:
        sName = str(sensor.Name)
        sType = str(sensor.SensorType)
        if ("core" in sName and sType == "Temperature"):
            array["gpu"]["temp"] = rnd(sensor.Value, 1)
            print(array["gpu"]["temp"])


    for hw in user.Hardware:
        hwType = str(hw.HardwareType).lower()
        if "gpu" in hwType: hwType ="gpu"
        array[hwType] = {"name": hw.Name}

        for sensor in hw.Sensors:
            

            #temp ----
            if (sName == "Core Average") or \
            (sName == "GPU Core" and sType == "Temperature"): 
                array[hwType]["temp"] = getVal(sensor, 1)

            #usagePercentage ----
            elif (sName == "CPU Total") or \
            (sName == "GPU Core" and sType == "Load") or \
            (sName == "Memory Total"):
                array[hwType]["usagePercentage"] = getVal(sensor, 1)
                print("percent: " + array[hwType]["usagePercentage"] + " | " + sType +sName)

            #memoryPercentage ----
            elif (sName == "Gpu Core") or \
            (sName == "Memory" and sType == "Load"):
                array[hwType]["memoryPercentage"] = getVal(sensor, 1)
            
            #memorySpecific ----
            elif (sName == "Memory Used"):
                array[hwType]["memorySpecific"] = getVal(sensor, 1)

            #
            
    #del array["gpu"]
    # if "gpu" not in array:
    #     array["gpu"] = {
    #         "name": "No GPU",
    #         "temp": "N/A",
    #         "usage": "N/A"
    #     }
    mem = pu.virtual_memory()

    array["cpu"] = {
        "loadPercentage": pu.cpu_percent(interval=None),
    }
    array["memory"] = {
        "total": round(mem.total / (1024.0 ** 3.0)),
        "loadPercentage": mem.percent
    }
updateArray()

def setStatic() -> None:
    gpuName.set(array["gpu"]["name"])
setStatic()

def setInfo() -> None:
    cpuTemp.set()
    gpuTemp.set(array["gpu"]["temp"])

def refresh() -> None:
    updateArray()
    user.Accept(UpdateVisitor())
    setInfo()
    main.update()
    main.after(1000, refresh)

main.after(1000, refresh)
main.mainloop()