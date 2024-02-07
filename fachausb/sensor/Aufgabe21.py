import flink
import time
from typing import List

tcrt1000 = flink.FlinkReflectiveSensor()

while True:
    values: List[int] = []
    for i in range(4):
    print()
    values.append(tcrt1000.getValue(i))
    time.sleep(0.5)