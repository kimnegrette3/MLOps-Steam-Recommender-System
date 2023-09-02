from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import json

app = FastAPI(title= 'Steam-API')

@app.get("/")
def read_root():
    response = {"message": "Welcome to steam recommendations api!"}
    return JSONResponse(status_code=200,content=response)

@app.get("/userdata/{user_id}",tags=['user'])
def userdata(user_id : str):
    df_user = pd.read_csv('dataquery/user_data.csv')
    user_data = df_user[df_user['user_id'] == user_id]
    if len(user_data) == 0:
        return JSONResponse(status_code=404,content={'error': f"User with id '{user_id}' not found"})
    response = user_data.to_dict(orient='records')
    return JSONResponse(status_code=200,content={"results":response})

@app.get("/sentimentanalysis/{anio}")
def sentiment_analysis(anio : str):
    anio = anio.strip()
    df = pd.read_csv('dataquery/sentiment_analysis.csv')
    df['year_released'] = df['year_released'].astype(str)
    if df['year_released'].str.contains(anio).any():
        response = df[df['year_released'] == anio].to_dict(orient='records')
        return JSONResponse(status_code=200,content={"results":response})
    else:
        return JSONResponse(status_code=404,content={"error":f"Year '{anio}' is not found"})
        

# Enpoint de la función Genero, se ingresa un genero en formato str
# Devuelve un objeto json con el genero cantidad de horas y rank
# en base de las horas jugadas totales de todos los generos
@app.get("/genre/{genre}",tags=['genre'])
def genre(genre : str):
    genre = genre.lower().strip()
    df_genre = pd.read_csv(r'./dataquery/gener_rank.csv')
    
    if df_genre['Genre'].str.contains(genre).any():
        genre_info = df_genre[df_genre['Genre']==genre]
        response = genre_info.to_dict(orient='records')
    else:
        return JSONResponse(status_code=404,content={'error':f"Genre '{genre}' not found"})
    return JSONResponse(status_code=200,content={"results":response})

# Endpoint que recibe un string para el genero y regresa el top5 de los usuarios con mas horas de juego
@app.get("/userforgenre/{genero}",tags=['genre'])
def userforgenre( genero : str ):
    genero = genero.lower().strip()
    df1 = pd.read_csv(r'./dataquery/top5_users.csv')
    if genero not in df1.columns:
        return JSONResponse(status_code=404,content={'error':f"Genre '{genero}' not found"})
    
    top5 = df1.sort_values(by=genero,ascending=False).head(5).reset_index()
    response = top5[['user_id','user_url']].to_dict(orient='records')
    return JSONResponse(status_code=200,content={"results":response})
