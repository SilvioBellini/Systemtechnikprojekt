import flink
import time

ch = 0      # Beinhaltet Signal A und B (Für zwei Drehrichtungen)
fqd = flink.FlinkFQD()

while True:
    print("Position =", fqd.getCount(ch))
    time.sleep(1)