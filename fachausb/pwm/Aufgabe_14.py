import flink
import time

# Beinhaltet Signal A und B (Für zwei Drehrichtungen)
ch = 0
fqd = flink.FlinkFQD()

while True:
    print("Position =", fqd.getCount(ch))
    time.sleep(1)