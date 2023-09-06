# Funciones usadas recurrentemente para transformar variables de los dataframes

import pandas as pd
import re
import ast

# Función para corregir el precio, en el que aparecen valores numéricos y en formato string
def fix_price(df):

    errors_list = []
    for i in df['price']:
        try:
            float(i)
        except:
            errors_list.append(i)

    errors = set(errors_list)
    #uniques_not_free = ['Starting at $499.00', 'Starting at $449.00']
    df['price_fixed'] = df['price'].apply(lambda x: 0 if x in errors 
                                                        else 499.0 if x=='Starting at $499.00'
                                                        else 449.0 if x=='Starting at $449.00'
                                                        else x)
    df['price_fixed'] = df['price_fixed'].astype(float)
    return df


# Función para convertir la columna fecha en dtype datetime
def safe_date_convert(df, date_column):
    def convert(x):
        try:
            return pd.to_datetime(x)
        except ValueError:
            # Try to find a year pattern in the string
            year_pattern = re.search(r'\b\d{4}\b', x)
            if year_pattern:
                # Convert the found year into a datetime format
                return pd.to_datetime(year_pattern.group(0), format='%Y')
            else:
                # If no year pattern is found, return NaT
                return pd.NaT

    df['date_fixed'] = df[date_column].astype(str).apply(convert)
    return df


# función para convertir a lista las columnas con múltiples elementos
def tolist(lst):
    text= ""
    if isinstance(lst, str) and len(lst) > 0 and '[' in lst:
        lst = lst.lower()
        lst = lst.replace("0's",'0s').replace(';','').replace('&','').replace("'em","em")
        try:
            lst =  ast.literal_eval(lst)
        except (SyntaxError, ValueError):
            return lst.lower()
        
    if isinstance(lst,list):
        for item in lst:
            while "  " in item:
                item = item.replace("  "," ")
            item = item.replace(" ", "-")
            text = text + " " + item 
            text = text.replace('"','')
        return text.strip().lower()

    return lst


# Función para crear las columnas binarias de los géneros
def create_genre_columns(dataframe):
    genres_list = set()

    # se crea el set con los valores DISTINCT de los géneros
    for genres in dataframe['genres']:
        if isinstance(genres, list):
            genres_list.update(genres)
    
    # crea una columna por cada genre en genre_list 
    # se recorre la columna genre imputando 1 cuando existe ese género 
    # en la fila analizada
    for genre in genres_list:
        dataframe[genre] = dataframe['genres'].apply(lambda x: 1 if genre in x else 0)
    
    return dataframe