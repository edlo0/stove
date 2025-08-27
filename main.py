from time import sleep
import psutil as pu
from tkinter import *
from tkinter import ttk
import sv_ttk
import clr

clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware # type: ignore
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
user.IsCpuEnabled = True
user.IsGpuEnabled = True
user.Open()
user.Accept(UpdateVisitor())

for hardware in user.Hardware:
    print(f"Hardware: {hardware.Name}")
    for sensor in hardware.Sensors:
        print(f"\tSensor: {sensor.Name}, value: {sensor.Value} TYPE: {sensor.SensorType}")
array = {
    "cpu": {},
    "gpu": {
        "temp": "Error",
        "loadPercentage": -1.0,
        "clock": "Error"
    },
    "memory": {}
}
noGPU = True

main = Tk()
main.title("Stove")
main.geometry("550x300")
main.minsize(width=375, height=200)
main.maxsize(width=550, height=300)
main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

frame = ttk.Frame(main)
frame.grid(column=0, row=0, sticky=(N, E, W, S))
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

cpuFrame = ttk.Labelframe(frame, text="CPU")
cpuFrame.grid(column=0, row=0, sticky=(N, E, W, S))
cpuFrame.columnconfigure(0, weight=1)

cpuLoadFrame = ttk.Labelframe(cpuFrame, text="Load")
cpuLoadFrame.grid(column=0, row=0, sticky=(E, W))
cpuLoadFrame.columnconfigure(1, weight=1)
cpuLoadPercentage = DoubleVar()
cpuLoadText = StringVar()
ttk.Progressbar(cpuLoadFrame, length=150, mode="determinate", variable=cpuLoadPercentage, orient="horizontal").grid(column=0, row=0)
ttk.Label(cpuLoadFrame, textvariable=cpuLoadPercentage, font="TkDefaultFont 18 bold").grid(column=1, row=0)

cpuTempFrame = ttk.Labelframe(cpuFrame, text="Temperature")
cpuTempFrame.grid(column=0, row=1, sticky=(E, W))
cpuTemp = StringVar()
ttk.Label(cpuTempFrame, textvariable=cpuTemp, font="TkDefaultFont 18 bold").grid(column=0, row=0)

cpuClockFrame = ttk.Labelframe(cpuFrame, text="Clock")
cpuClockFrame.grid(column=0, row=2, sticky=(E, W))
cpuClock = StringVar()
ttk.Label(cpuClockFrame, textvariable=cpuClock, font="TkDefaultFont 18 bold").grid(column=0, row=0)

gpuFrame = ttk.Labelframe(frame, text="GPU")
gpuFrame.grid(column=1, row=0, sticky=(N, E, W, S))
gpuFrame.columnconfigure(0, weight=1)

gpuLoadFrame = ttk.Labelframe(gpuFrame, text="Load")
gpuLoadFrame.grid(column=0, row=0, sticky=(E, W))
gpuLoadFrame.columnconfigure(1, weight=1)
gpuLoadPercentage = DoubleVar()
gpuLoadText = StringVar()
ttk.Progressbar(gpuLoadFrame, length=100, mode="determinate", variable=gpuLoadPercentage, orient="horizontal").grid(column=0, row=0)
ttk.Label(gpuLoadFrame, textvariable=gpuLoadPercentage, font="TkDefaultFont 18 bold").grid(column=1, row=0)

gpuTempFrame = ttk.Labelframe(gpuFrame, text="Temperature")
gpuTempFrame.grid(column=0, row=1, sticky=(E, W))
gpuTemp = StringVar()
ttk.Label(gpuTempFrame, textvariable=gpuTemp, font="TkDefaultFont 18 bold").grid(column=0, row=0)

gpuClockFrame = ttk.Labelframe(gpuFrame, text="Clock")
gpuClockFrame.grid(column=0, row=2, sticky=(E, W))
gpuClock = StringVar()
ttk.Label(gpuClockFrame, textvariable=gpuClock, font="TkDefaultFont 18 bold").grid(column=0, row=0)

for x in frame.winfo_children():
    x['padding'] = 10

def updateSensors():
    while True:
        user.Open()
        user.Accept(UpdateVisitor())
        sleep(1)

for i in user.Hardware:
    if "Gpu" in str(i.HardwareType):
        noGPU = False

def updateArray() -> None:
    #CPU ---------
    cpuHW = user.Hardware[0]
    array["cpu"]["loadPercentage"] = pu.cpu_percent(interval=None)
    cpuClocks = []
    for sensor in cpuHW.Sensors:
        sName = str(sensor.Name)
        sType = str(sensor.SensorType)
        if (sName == "Core Average" and sType == "Temperature"):
            array["cpu"]["temp"] = round(sensor.Value, 1)
        elif (sName == "CPU Total" and sType == "Load"):
            array["cpu"]["loadPercentage"] = round(sensor.Value, 1)
        elif ("CPU Core" in sName and sType == "Clock"):
            cpuClocks.append(sensor.Value)
    array["cpu"]["clock"] = round(sum(cpuClocks) / len(cpuClocks)) # average clocks

    #GPU ----------
    if noGPU == False:
        gpuHW = user.Hardware[1]
        for sensor in gpuHW.Sensors:
            sName = str(sensor.Name)
            sType = str(sensor.SensorType)
            if (sName == "GPU Core" and sType == "Temperature"):
                array["gpu"]["temp"] = round(sensor.Value, 1)
            elif (sName == "GPU Core" and sType == "Load"):
                array["gpu"]["loadPercentage"] = round(sensor.Value, 1)
            elif (sName == "GPU Core" and sType == "Clock"):
                array["gpu"]["clock"] = round(sensor.Value)

    #MEMORY ------------
    mem = pu.virtual_memory()
    array["memory"] = {
        "total": round(mem.total / (1024.0 ** 3.0)),
        "loadPercentage": mem.percent
    }

    #STORAGE ----------
    #for disk in pu.disk_partitions:
    print(array)
updateArray()

#def setStatic() -> None:
    #cpuName.set(array["cpu"]["name"])
    #gpuName.set(array["gpu"]["name"])
#setStatic()

def setInfo() -> None:
    cpuTemp.set(f"{array["cpu"]["temp"]} C") 
    gpuTemp.set(f"{array["gpu"]["temp"]} C")
    cpuLoadPercentage.set(array["cpu"]["loadPercentage"])
    gpuLoadPercentage.set(array["gpu"]["loadPercentage"])
    cpuLoadText.set(f"{array["cpu"]["loadPercentage"]}%")
    gpuLoadText.set(f"{array["gpu"]["loadPercentage"]}%")
    cpuClock.set(f"{array["cpu"]["clock"]} MHz")
    gpuClock.set(f"{array["gpu"]["clock"]} MHz")

def refresh() -> None:
    updateArray()
    user.Accept(UpdateVisitor())
    setInfo()
    main.update()
    main.after(1000, refresh)

main.after(1000, refresh)
sv_ttk.use_dark_theme()
main.mainloop()