import flink
import time
from typing import List

tcrt1000 = flink.FlinkReflectiveSensor()

while True:
    values: List[int] = []
    for i in range(4):
        values.append(tcrt1000.getValue(i))
    values.sort()
    print("Min.:" , values[0])
    print("Max.:" , values[-1])
    time.sleep(0.5)