from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to steam recommendations api!"}

# Agrega aquí tus rutas y funciones de FastAPI
# Por ejemplo:
@app.get("/data")
def get_data():
    # Aquí puedes cargar los datos procesados y devolverlos como respuesta JSON
    # Ejemplo: return {"data": "datos_procesados"}
    pass

@app.get("/userdata")
def userdata(user_id : str):
    df_user = pd.read_csv('dataquery/user_data.csv')
    user_data = df_user[df_user['user_id'] == user_id]
    
    return user_data.to_json(orient='records')

# Enpoint de la funcion Genero, se ingresa un genero en formato str y devuelve un objeto json con el genero cantidad de horas y rank
# en base de las horas jugadas totales
@app.get("/genre")
def genre(genre : str):
    genre = genre.lower()
    df_genre = pd.read_csv(r'./dataquery/gener_rank.csv')
    
    if df_genre['Genre'].str.contains(genre).any():
        genre_info = df_genre[df_genre['Genre']==genre]
    else:
        return 'No se encontro el genero'
    return genre_info.to_json(orient='records')