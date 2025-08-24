import psutil as pu

print(pu.disk_partitions())
print(pu.disk_usage('/'))