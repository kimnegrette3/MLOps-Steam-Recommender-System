from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import json

app = FastAPI(title= 'Steam-API')

@app.get("/")
def read_root():
    return {"message": "Welcome to steam recommendations api!"}

@app.get("/userdata/{user_id}",tags=['user'])
def userdata(user_id : str):
    df_user = pd.read_csv('dataquery/user_data.csv')
    user_data = df_user[df_user['user_id'] == user_id]
    
    return user_data.to_json(orient='records')

@app.get("/sentimentanalysis/{año}",tags=['sentiment'])
def sentiment_analysis(año : str):
    df = pd.read_csv('dataquery/sentiment_analysis.csv')
    if año in df['year_released']:
        return df[df['year_released'] == año]
    else:
        return 'Year not found'
        

# Enpoint de la función Genero, se ingresa un genero en formato str
# Devuelve un objeto json con el genero cantidad de horas y rank
# en base de las horas jugadas totales de todos los generos
@app.get("/genre/{genre}",tags=['genre'])
def genre(genre : str):
    genre = genre.lower().strip()
    df_genre = pd.read_csv(r'./dataquery/gener_rank.csv')
    
    if df_genre['Genre'].str.contains(genre).any():
        genre_info = df_genre[df_genre['Genre']==genre]
    else:
        return JSONResponse(status_code=404,content="Genre not found")
    return JSONResponse(status_code=200,content=genre_info.to_dict(orient='records'))

# Endpoint que recibe un string para el genero y regresa el top5 de los usuarios con mas horas de juego
@app.get("/userforgenre/{genero}",tags=['genre'])
def userforgenre( genero : str ):
    genero = genero.lower().strip()
    df1 = pd.read_csv(r'./dataquery/top5_users.csv')
    if genero not in df1.columns:
        return JSONResponse(status_code=404,content="Genre not found")
    
    top5 = df1.sort_values(by=genero,ascending=False).head(5).reset_index()
    response = top5[['user_id','user_url']].to_dict(orient='records')
    return JSONResponse(status_code=200,content=response)
