import pandas as pd
import numpy as np
def extract():
    order_details = pd.read_csv('order_details.csv')
    orders = pd.read_csv('orders.csv')
    pizza_types = pd.read_csv('pizza_types.csv',encoding='latin1')
    return  order_details, orders, pizza_types
def analisis_nulls(order_details, orders, pizza_types):
    analisis = [order_details, orders, pizza_types]
    df_num = 0
    analisis_str = ['order_details', 'orders', 'pizza_types']
    numero_nulls = {}
    for df in analisis:
        cols = df.columns 
        nuls = df[cols].isnull()
        missing = 0
        for nul in nuls:
            for i in range(len(nul)):
                if nul[i] == True:
                    missing += 1
        numero_nulls[analisis_str[df_num]] = missing
        df_num += 1
    print(numero_nulls)
    return
def transform(order_details, orders, pizza_types):
    pizza = {}
    fechas = []
    for i in range(len(pizza_types)):
        pizza[pizza_types['pizza_type_id'][i]] = pizza_types['ingredients'][i]
    for fecha in orders['date']:
        f = pd.to_datetime(fecha, errors='raise', dayfirst=True, yearfirst=False, utc=None, format='%d/%m/%Y', exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)
        fechas.append(f)
    cant_pedidos = [[] for _ in range(53)]
    pedidos = [[] for _ in range(53)]
    for pedido in range(len(fechas)):
        cant_pedidos[fechas[pedido].week-1].append(pedido+1)
    for p in range(1,order_details['order_details_id'][len(order_details['order_details_id'])-1]-1):
        for i in range(order_details['quantity'][p]):
            pedidos[fechas[order_details['order_id'][p]-1].week-1].append(order_details['pizza_id'][p])
    ingredientes_anuales = {}
    diccs = []
    for dic in range(53):
        diccs.append({})
    for i in range(len(pizza_types)):
        ingreds = pizza_types['ingredients'][i]
        ingreds = ingreds.split(', ')
        for ingrediente in ingreds:
            ingredientes_anuales[ingrediente] = 0
            for i in range(len(diccs)):
                diccs[i][ingrediente] = 0       
    for i in range(len(pedidos)):
        for p in pedidos[i]:
            ing = 0
            tamano = 0
            if p[-1] == 's':
                ing = 1
                tamano = 2
            elif p[-1] == 'm':
                ing = 2
                tamano = 2
            elif p[-1] == 'l':
                if p[-2] == 'x':
                    if p[-3] == 'x':
                        ing = 5
                        tamano = 4
                    else:
                        ing = 4
                        tamano = 3
                else:
                    ing = 3
                    tamano = 2
            ings = pizza[p[:-tamano]].split(', ')
            for ingrediente in ings:
                ingredientes_anuales[ingrediente] += ing
                diccs[i][ingrediente] += ing
    print(ingredientes_anuales)
    for i in range(len(diccs)):
        for j in diccs[i]:
            diccs[i][j] = int(np.ceil((diccs[i][j] + (ingredientes_anuales[j]/53))/2))
    return diccs
def load(diccs):
    df = pd.DataFrame(diccs)
    print(df)
    df.to_csv('prediccion_semanal.csv')

if __name__ == '__main__':
    order_details, orders, pizza_types = extract()
    analisis_nulls(order_details,orders,pizza_types)
    diccs=transform( order_details, orders,pizza_types)
    load(diccs)