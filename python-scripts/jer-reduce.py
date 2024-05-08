import pandas as pd
import numpy as np
import datetime
from datavis_utils import *

import os

def pick_col(orders):
    cols = list(orders.columns)
    for i,c in enumerate(cols):
        print(f"{i}: {c}")
    choice = int(input("Choose a column: "))
    return cols[choice]

orders = orders.merge(regions, on='Territory')
group = 'Region'

group = pick_col(orders)

orders = orders[[group, "CartPriceInCP", "DeliveryTime"]]

orders = orders.groupby(group).agg({'CartPriceInCP': 'sum', 'DeliveryTime':'mean'})

orders['Hours'] = orders['DeliveryTime'] / datetime.timedelta(hours=1)
orders.pop('DeliveryTime')


minDT = int(np.min(orders['Hours']))
rangeDT = int(np.max(orders['Hours'])) - minDT

orders['Hours'] = orders['Hours'].transform(lambda x: int(100 * ((int(x) - minDT)/rangeDT)))


totCartPrice = np.sum(orders["CartPriceInCP"])
orders["CartPriceInCP"] = orders["CartPriceInCP"].transform(lambda x: int(100*(x/totCartPrice)))

print(orders)

for c in orders.columns:
    print(c)



orders = orders.reset_index()

orders['Location'] = orders.pop(group)
orders['Time'] = orders.pop('Hours')

orders.to_csv(f"../my-app/static/jer-data-{group.lower().replace(' ','' )}.csv", header=True, index=False)

os.system(f"head ../my-app/static/jer-data.csv")

