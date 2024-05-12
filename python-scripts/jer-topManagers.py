import numpy as np
import pandas as pd
import json

from datavis_utils import *

manager_type = 'Regional Manager'

orders = orders.merge(regions,on='Territory')
orders.pop('index')

print(np.max(orders['OrderDate']))

orders['ODYear'] = orders['OrderDate'].apply(lambda x: x.year)
orders['ODMonth'] = orders['OrderDate'].apply(lambda x: x.month)


print(orders)


orders = orders[['ODYear','ODMonth', manager_type, 'CartPriceInCP']]

grouped = pd.DataFrame(orders.groupby(['ODYear','ODMonth', manager_type],as_index=False).sum())

grouped.sort_values(['ODYear','ODMonth', 'CartPriceInCP'],inplace=True,ascending=False)



print(grouped)
print(grouped['ODYear'].unique())

years = grouped['ODYear'].unique()
months = grouped['ODMonth'].unique()


ret_dict = {}
for y in years:
    ret_dict[str(y)] = {}
    for m in months:
        ret_dict[str(y)][str(m)] = list(grouped.loc[ (grouped['ODYear'] == y) & (grouped['ODMonth'] == months[0])].nlargest(3,'CartPriceInCP')[manager_type])


with open('../my-app/static/top3.json','w') as f:
    json.dump(ret_dict,f,indent=2)


