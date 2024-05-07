import pandas as pd
import numpy as np
import datetime
from datavis1 import *

import os

orders = orders.merge(regions, on='Territory')
group = 'Area'

orders = orders[[group, "CartPriceInCP", "DeliveryTime"]]

orders = orders.groupby(group).mean()

orders['Hours'] = orders['DeliveryTime'] / datetime.timedelta(hours=1)
orders['Hours'] = orders['Hours'].transform(lambda x: int(x))

print(orders)

for c in orders.columns:
    print(c)

print(type(orders['DeliveryTime'].iloc[0]))

orders.pop('DeliveryTime')

orders = orders.reset_index()

orders['Location'] = orders.pop(group)
orders['Time'] = orders.pop('Hours')

orders.to_csv("../my-app/static/jer-data.csv", header=True, index=False)

os.system(f"head ../my-app/static/jer-data.csv")

