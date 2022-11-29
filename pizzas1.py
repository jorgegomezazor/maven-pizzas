import pandas as pd
import numpy as np
def extract(): #importo los csv
    order_details = pd.read_csv('order_details.csv') #importo el csv de order_details
    orders = pd.read_csv('orders.csv') #importo el csv de orders
    pizza_types = pd.read_csv('pizza_types.csv',encoding='latin1') #importo el csv de pizza_types
    return  order_details, orders, pizza_types 
def analisis_nulls(order_details, orders, pizza_types): #analizo los nulls
    analisis_o_d = {} # Creo un diccionario vacío
    analisis_o_d['order_details'] = (order_details.isnull().sum(), order_details.dtypes) # Agrego al diccionario la cantidad de nulls de order_details
    analisis_o= {} # Creo un diccionario vacío
    analisis_o['orders'] = (orders.isnull().sum(),orders.dtypes) # Agrego al diccionario la cantidad de nulls de orders
    analisis_p_t = {} # Creo un diccionario vacío
    analisis_p_t['pizza_types'] = (pizza_types.isnull().sum(),pizza_types.dtypes) # Agrego al diccionario la cantidad de nulls de pizza_types
    dicc = [analisis_o_d, analisis_o, analisis_p_t] # Creo una lista con los diccionarios
    #creo csv con los nulls
    df = pd.DataFrame(dicc) #creo un dataframe con los diccionarios
    df = df.transpose() #transpongo el dataframe
    df.to_csv('analisis_nulls.csv')
    return
def transform(order_details, orders, pizza_types):
    pizza = {}
    fechas = []
    for i in range(len(pizza_types)):
        pizza[pizza_types['pizza_type_id'][i]] = pizza_types['ingredients'][i] #guardo los ingredientes en un diccionario
    for fecha in orders['date']:
        f = pd.to_datetime(fecha, errors='raise', dayfirst=True, yearfirst=False, utc=None, format='%d/%m/%Y', exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True) #convierto las fechas a datetime
        fechas.append(f) #guardo las fechas en una lista
    cant_pedidos = [[] for _ in range(53)] #creo una lista de listas para guardar la cantidad de pedidos por semana
    pedidos = [[] for _ in range(53)] #creo una lista de listas para guardar los pedidos por semana
    for pedido in range(len(fechas)):
        cant_pedidos[fechas[pedido].week-1].append(pedido+1) #guardo la cantidad de pedidos por semana
    for p in range(1,order_details['order_details_id'][len(order_details['order_details_id'])-1]-1): 
        for i in range(order_details['quantity'][p]):
            pedidos[fechas[order_details['order_id'][p]-1].week-1].append(order_details['pizza_id'][p]) #guardo los pedidos por semana teniendo en cuenta la cantidad de pizzas
    ingredientes_anuales = {}
    diccs = []
    for dic in range(53):
        diccs.append({}) #creo una lista de diccionarios para guardar los ingredientes por semana
    for i in range(len(pizza_types)):
        ingreds = pizza_types['ingredients'][i] #guardo los ingredientes en una variable
        ingreds = ingreds.split(', ') #separo los ingredientes
        for ingrediente in ingreds:
            ingredientes_anuales[ingrediente] = 0
            for i in range(len(diccs)):
                diccs[i][ingrediente] = 0 #guardo los ingredientes en los diccionarios
    for i in range(len(pedidos)):
        for p in pedidos[i]:
            ing = 0
            tamano = 0
            if p[-1] == 's': #guardo el tamaño de la pizza
                ing = 1 #si es s la pizza tiene 1 ingrediente de cada
                tamano = 2 
            elif p[-1] == 'm':
                ing = 2 #si es m la pizza tiene 2 ingredientes de cada
                tamano = 2
            elif p[-1] == 'l':
                if p[-2] == 'x':
                    if p[-3] == 'x':
                        ing = 5 #si es xxl la pizza tiene 5 ingredientes de cada
                        tamano = 4
                    else:
                        ing = 4 #si es xl la pizza tiene 4 ingredientes de cada
                        tamano = 3
                else:
                    ing = 3 #si es l la pizza tiene 3 ingredientes de cada
                    tamano = 2
            ings = pizza[p[:-tamano]].split(', ')
            for ingrediente in ings:
                ingredientes_anuales[ingrediente] += ing #guardo los ingredientes en el diccionario de ingredientes anuales
                diccs[i][ingrediente] += ing #guardo los ingredientes en los diccionarios de ingredientes por semana
    for i in range(len(diccs)):
        for j in diccs[i]:
            diccs[i][j] = int(np.ceil((diccs[i][j] + (ingredientes_anuales[j]/53))/2)) #aplico la predicción
    return diccs
def load(diccs):
    df = pd.DataFrame(diccs) #creo un dataframe con los diccionarios
    df = df.transpose() #transpongo el dataframe
    df.to_csv('prediccion_semanal.csv') #guardo el dataframe en un csv

if __name__ == '__main__':
    order_details, orders, pizza_types = extract()
    analisis_nulls(order_details,orders,pizza_types)
    diccs=transform( order_details, orders,pizza_types)
    load(diccs)
    '''
    La predicción se basa en que la cantidad de ingredientes semanales que se necesitarán en una semana serán 
    aproximadamente la media entre los ingredientes usados esa semana en el 2015 y los ingredientes usados en el 2015 entre las 53 semanas.
    '''