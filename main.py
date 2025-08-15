from tkinter import *
from tkinter import ttk

import clr
clr.AddReference("LibreHardwareMonitorLib")
from LibreHardwareMonitor import Hardware # pyright: ignore[reportMissingImports]

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

def getCpuName():
    for hw in user.Hardware:
        if hw.HardwareType.value__ == 2:
            return hw.Name
        
def getGpuName():
    for hw in user.Hardware:
        if hw.HardwareType.value__ == 4:
            return hw.Name

main = Tk()
main.title("Stove")

frame = ttk.Frame(main)
frame.grid(column=0, row=0)

cpuName = StringVar()
ttk.Label(frame, textvariable=cpuName).grid(column=1, row=0)
cpuName.set(getCpuName())

gpuName = StringVar()
ttk.Label(frame, textvariable=gpuName).grid(column=2, row=0)
gpuName.set(getGpuName())

for x in frame.winfo_children():
    x['padding'] = 10

main.mainloop()