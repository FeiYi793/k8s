# -*- coding: utf-8 -*-
import os
import time

import pandas as pd

csv = pd.read_csv("./res.csv")

res = csv['0']

for i in range(0, len(res)):
    req = round(res[i]*2100)
    # locust -f locusttest.py -H http://172.20.110.29:30010 -u 2000 -r 20 --csv loadtest1 --csv-full-history
    os.system("locust -f locusttest.py -H http://192.168.221.100:30001 -u %s "
              "-r 20 --csv loadtest_%s --csv-full-history --headless -t 5m"
              % (req, i))
    time.sleep(30)

#locust -f locusttest.py --web-port=8089
