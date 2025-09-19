import sys
from time import sleep
from tkinter import *
from tkinter import ttk

def exit():
    sys.exit()
def errorMessage(errMessage, errText):
    errorWindow = Tk()
    errorWindow.title("Stove")
    errorWindow.geometry("400x150")
    errorWindow.minsize(width=400, height=150)
    errorWindow.columnconfigure(0, weight=1)
    errorWindow.rowconfigure(0, weight=1)

    errorFrame = Frame(errorWindow)
    errorFrame.grid(column=0, row=0, sticky=(N, E, W, S))
    errorFrame.columnconfigure(0, weight=1)
    errorFrame.rowconfigure(0, weight=1)
    errorFrame.rowconfigure(1, weight=1)
    errorFrame.rowconfigure(2, weight=1)

    errorText = Label(errorFrame, text=errMessage)
    errorText.grid(column=0, row=0)

    errorTextBox = Label(errorFrame,text=errText)
    errorTextBox.grid(column=0, row=1)

    Button(errorFrame, text="Close", command=quit).grid(column=0, row=2)
    
    errorWindow.mainloop()

try:
    import clr
    import psutil as pu
    import sv_ttk
except ImportError as err:
    errorMessage("An import failed.", err.args)
except Exception as err:
    errorMessage("Unexpected error.", err.args)

try:
    clr.AddReference("LibreHardwareMonitorLib")
    from LibreHardwareMonitor import Hardware # type: ignore
except Exception as err:
    errorMessage("LibreHardwareMonitorLib.dll failed to import.", err.args)


try:
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
except Exception as err:
    errorMessage("LibreHardwareMonitor failed to initialize. Did you open as admin?", err.args)

array = {
    "cpu": {
        "temp": "No CPU",
        "loadPercentage": 0.0,
        "clock": "No CPU",
        "power": "No CPU"
    },
    "gpu": {
        "temp": "No GPU",
        "loadPercentage": 0.0,
        "clock": "No GPU",
        "power": "No GPU"
    },
    "memory": {
        "total": 0.0,
        "used": 0.0,
        "loadPercentage": 0.0
    },
    "disks": {}
}
noGPU = True

main = Tk()
main.title("Stove")
main.geometry("550x500")
main.minsize(width=375, height=200)
main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

frame = ttk.Frame(main)
frame.grid(column=0, row=0, sticky=(N, E, W, S))
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)

cpuFrame = ttk.Labelframe(frame, text="CPU")
cpuFrame.grid(column=0, row=0, sticky=(N, E, W, S))
cpuFrame.columnconfigure(0, weight=1)

cpuLoadFrame = ttk.Labelframe(cpuFrame, text="Load")
cpuLoadFrame.grid(column=0, row=0, sticky=(E, W))
cpuLoadFrame.columnconfigure(0, weight=1)
cpuLoadFrame.columnconfigure(1, weight=1)
cpuLoadPercentage = DoubleVar()
cpuLoadText = StringVar()
ttk.Progressbar(cpuLoadFrame, length=150, mode="determinate", variable=cpuLoadPercentage, orient="horizontal").grid(column=0, row=0)
ttk.Label(cpuLoadFrame, textvariable=cpuLoadText, font="TkDefaultFont 18 bold").grid(column=1, row=0)

cpuTempFrame = ttk.Labelframe(cpuFrame, text="Temperature")
cpuTempFrame.grid(column=0, row=1, sticky=(E, W))
cpuTemp = StringVar()
ttk.Label(cpuTempFrame, textvariable=cpuTemp, font="TkDefaultFont 18 bold").grid(column=0, row=0)

cpuClockFrame = ttk.Labelframe(cpuFrame, text="Clock")
cpuClockFrame.grid(column=0, row=2, sticky=(E, W))
cpuClock = StringVar()
ttk.Label(cpuClockFrame, textvariable=cpuClock, font="TkDefaultFont 18 bold").grid(column=0, row=0)

cpuPowerFrame = ttk.Labelframe(cpuFrame, text="Power")
cpuPowerFrame.grid(column=0, row=3, sticky=(E, W))
cpuPower = StringVar()
ttk.Label(cpuPowerFrame, textvariable=cpuPower, font="TkDefaultFont 18 bold").grid(column=0, row=0)

gpuFrame = ttk.Labelframe(frame, text="GPU")
gpuFrame.grid(column=1, row=0, sticky=(N, E, W, S))
gpuFrame.columnconfigure(0, weight=1)

gpuLoadFrame = ttk.Labelframe(gpuFrame, text="Load")
gpuLoadFrame.grid(column=0, row=0, sticky=(E, W))
gpuLoadFrame.columnconfigure(0, weight=1)
gpuLoadFrame.columnconfigure(1, weight=1)
gpuLoadPercentage = DoubleVar()
gpuLoadText = StringVar()
ttk.Progressbar(gpuLoadFrame, length=100, mode="determinate", variable=gpuLoadPercentage, orient="horizontal").grid(column=0, row=0)
ttk.Label(gpuLoadFrame, textvariable=gpuLoadText, font="TkDefaultFont 18 bold").grid(column=1, row=0)

gpuTempFrame = ttk.Labelframe(gpuFrame, text="Temperature")
gpuTempFrame.grid(column=0, row=1, sticky=(E, W))
gpuTemp = StringVar()
ttk.Label(gpuTempFrame, textvariable=gpuTemp, font="TkDefaultFont 18 bold").grid(column=0, row=0)

gpuClockFrame = ttk.Labelframe(gpuFrame, text="Clock")
gpuClockFrame.grid(column=0, row=2, sticky=(E, W))
gpuClock = StringVar()
ttk.Label(gpuClockFrame, textvariable=gpuClock, font="TkDefaultFont 18 bold").grid(column=0, row=0)

gpuPowerFrame = ttk.Labelframe(gpuFrame, text="Power")
gpuPowerFrame.grid(column=0, row=3, sticky=(E, W))
gpuPower = StringVar()
ttk.Label(gpuPowerFrame, textvariable=gpuPower, font="TkDefaultFont 18 bold").grid(column=0, row=0)

memoryFrame = ttk.Labelframe(frame, text="Memory")
memoryFrame.grid(column=0, row=1, sticky=(N, E, W, S))
memoryFrame.columnconfigure(0, weight=1)

memoryLoadFrame = ttk.Labelframe(memoryFrame, text="Load")
memoryLoadFrame.grid(column=0, row=0, sticky=(E, W))
memoryLoadFrame.columnconfigure(0, weight=1)
memoryLoadFrame.columnconfigure(1, weight=1)
memoryHeader = StringVar()
ttk.Label(memoryLoadFrame, textvariable=memoryHeader, font="TkDefaultFont 24 bold").grid(column=0, row=0, columnspan=2)
memoryLoadPercentage = DoubleVar()
memoryLoadText = StringVar()
ttk.Progressbar(memoryLoadFrame, length=100, mode="determinate", variable=memoryLoadPercentage, orient="horizontal").grid(column=0, row=1)
ttk.Label(memoryLoadFrame, textvariable=memoryLoadText, font="TkDefaultFont 18 bold").grid(column=1, row=1)

diskFrame = ttk.Labelframe(frame, text="Disks")
diskFrame.grid(column=1, row=1, sticky=(N, E, W, S))
diskFrame.columnconfigure(0, weight=1)

diskEntries = []

def setupDisks():
    disks = pu.disk_partitions()
    for x in range(len(disks)):
        disk = disks[x]
        try:
            pu.disk_usage(disk.device)
        except Exception as e:
            continue
        diskDict = {
            "device": disk.device,
            "diskHeader": StringVar(),
            "diskUsagePercentage": DoubleVar(),
            "diskUsageText": StringVar()
        }

        diskFrame.rowconfigure(x, weight=1)
        diskEntry = ttk.Labelframe(diskFrame, text=diskDict["device"])
        diskEntry.grid(column=0, row=x, sticky=(N, E, W, S))
        diskEntry.columnconfigure(0, weight=1)
        diskEntry.columnconfigure(1, weight=1)
        ttk.Label(diskEntry, textvariable=diskDict["diskHeader"], font="TkDefaultFont 18 bold").grid(column=0, row=0, columnspan=2)
        ttk.Progressbar(diskEntry, length=100, mode="determinate", variable=diskDict["diskUsagePercentage"], orient="horizontal").grid(column=0, row=1)
        ttk.Label(diskEntry, textvariable=diskDict["diskUsageText"], font="TkDefaultFont 18 bold").grid(column=1, row=1)
        diskEntries.append(diskDict)
try:
    setupDisks()
except Exception as err:
    errorMessage("Failed to display disks.", err.args)

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
        if (sName == "CPU Total" and sType == "Load"):
            array["cpu"]["loadPercentage"] = round(sensor.Value, 1)
        elif (sName == "Core Average" and sType == "Temperature"):
            array["cpu"]["temp"] = round(sensor.Value, 1)
        elif ("CPU Core" in sName and sType == "Clock"):
            cpuClocks.append(sensor.Value)
        elif (sName == "CPU Cores" and sType == "Power"):
            array["cpu"]["power"] = round(sensor.Value, 1)
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
            elif (sName == "GPU Package" and sType == "Power"):
                array["gpu"]["power"] = round(sensor.Value, 1)

    #MEMORY ------------
    mem = pu.virtual_memory()
    array["memory"] = {
        "total": round(mem.total / (1024.0 ** 3.0), 1),
        "used": round((mem.total - mem.available) / (1024.0 ** 3.0), 1),
        "loadPercentage": mem.percent
    }
updateArray()

def convertFromBytes(bytes: int) -> str:
    if bytes > (1024.0 ** 4.0):
        return f"{round(bytes / (1024.0 ** 4.0), 2)}TB"
    elif bytes > (1024.0 ** 3.0):
        return f"{round(bytes / (1024.0 ** 3.0))}GB"
    elif bytes > (1024.0 ** 2.0):
        return f"{round(bytes / (1024.0 ** 2.0))}MB"
    elif bytes > 1024.0:
        return f"{round(bytes / 1024.0)}KB"
    else:
        return f"{bytes}B"

def setInfo() -> None:
    cpuTemp.set(f"{array["cpu"]["temp"]} °C") 
    cpuLoadPercentage.set(array["cpu"]["loadPercentage"])
    cpuLoadText.set(f"{array["cpu"]["loadPercentage"]}%")
    cpuClock.set(f"{array["cpu"]["clock"]} MHz")
    cpuPower.set(f"{array["cpu"]["power"]} W")

    gpuTemp.set(f"{array["gpu"]["temp"]} °C")
    gpuLoadPercentage.set(array["gpu"]["loadPercentage"])
    gpuLoadText.set(f"{array["gpu"]["loadPercentage"]}%")
    gpuClock.set(f"{array["gpu"]["clock"]} MHz")
    gpuPower.set(f"{array["gpu"]["power"]} W")

    memoryHeader.set(f"{array["memory"]["used"]}/{array["memory"]["total"]}GB")
    memoryLoadPercentage.set(array["memory"]["loadPercentage"])
    memoryLoadText.set(f"{array["memory"]["loadPercentage"]}%")
    for x in range(len(diskEntries)):
        usage = pu.disk_usage(diskEntries[x]["device"])
        diskEntries[x]["diskHeader"].set(f"{convertFromBytes(usage.used)}/{convertFromBytes(usage.total)}")
        diskEntries[x]["diskUsagePercentage"].set(f"{usage.percent}")
        diskEntries[x]["diskUsageText"].set(f"{usage.percent}%")

def refresh() -> None:
    updateArray()
    user.Accept(UpdateVisitor())
    setInfo()
    main.update()
    main.after(1000, refresh)

main.after(1000, refresh)
sv_ttk.use_dark_theme()
main.mainloop()