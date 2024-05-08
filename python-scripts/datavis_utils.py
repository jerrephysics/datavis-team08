import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
Ideas:
    - Price distribution
    - Total sales per region
    - Total Sales per acc manager
    - number of sales per acc manager
    - avg delivery time per region
    - product most sold
    - product per region
    - product per acc
'''

WAIT_TIME = 0.01

os.chdir(os.path.dirname(__file__))
print(os.getcwd())


with open('./DEAD/data/regions.csv') as f:
    regions = pd.read_csv(f)

with open('./DEAD/data/products.csv') as f:
    products = pd.read_csv(f)

with open('./DEAD/data/customers.csv') as f:
    customers = pd.read_csv(f)
    customers['Account Manager'] = customers['Account Manager'].astype(str)

with open('./DEAD/data/orders.csv') as f:
    orders = pd.read_csv(f)
    #print(orders.iloc[0,:])
    orders['DeliveryDate'] = pd.to_datetime(orders['DeliveryDate'])
    orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
    orders['DeliveryTime'] = orders['DeliveryDate'] - orders['OrderDate']
    orders.insert(2,"DeliveryTime", orders.pop('DeliveryTime'))
    orders['Products'] = orders['Products'].astype(str)
    orders['Products'] = orders.Products.map(lambda x : [s.strip() for s in x.split(';') if s.strip()])
    def remove_nan(x):
        if x == ['nan']:
            return []
        return x
    orders['Products'] = orders.Products.apply(remove_nan)
    orders['Quantities'] = orders['Quantities'].astype(str)
    orders['Quantities'] = orders.Quantities.map(lambda x: [int(i) for i in x.split(',') if i.strip()])
    orders['ProductPricesInCP'] = orders['ProductPricesInCP'].astype(str)
    orders['ProductPricesInCP'] = orders.ProductPricesInCP.map(lambda x: [float(i) for i in x.split(',') if i.strip()])
    orders['NbProds'] = orders.Products.apply(len)
    orders['NbQuant'] = orders.Quantities.apply(len)
    orders['NbPrices'] = orders.ProductPricesInCP.apply(len)
    orders['CorrectSplit'] = (orders.NbProds == orders.NbQuant) & (orders.NbProds == orders.NbPrices)
    print(np.all(orders['CorrectSplit']))


#print(orders.Products.iloc[44])
orders = orders[orders['CorrectSplit'] == True].reset_index()


if __name__ == '__main__':
    dataframes = dict(zip(["orders","regions","products","customers"],[orders,regions,products,customers]))
    features = []
    for df in dataframes.keys():
        curr_cols = list(dataframes[df].columns)
        features = features + curr_cols
        for c in curr_cols:
            print(f"{df} > {c}")
    print(len(features))
    del dataframes


    orders = orders.explode(['Products','Quantities'])
    prodquant = orders[['Products','Quantities']].groupby('Products').sum()

    prodquant.sort_values('Quantities',inplace=True,ascending=False)
    print(prodquant)


    prodquant.plot.bar()
    plt.show()

    merged = pd.merge(prodquant,products, left_on='Products',right_on='Product Name')
    print(merged)






