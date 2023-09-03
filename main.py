from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import ast


app = FastAPI(title= 'Steam-API')

# ROOT DE LA WEB
@app.get("/")
def read_root():
    '''
    Root de la api donde debe regresar una pagina html
      Con la descripción de como usar los endpoints
    '''
    response = {"message": "Welcome to steam recommendations api!"}
    return JSONResponse(status_code=200,content=response)

# USERDATA: 
@app.get("/userdata/{user_id}",tags=['User'])
def userdata(user_id : str):
    '''
    Recibe un string con el **"User Id"** y devuelve un summary del user</br>
    
    Ejemplo:

        {
        "user_id": "--000--",
        "procentaje_recomendacion": 100,
        "cantidad_gastada": 402.77,
        "cantidad_items": 58
        }
    '''
    df_user = pd.read_csv('dataquery/user_data.csv')
    user_data = df_user[df_user['user_id'] == user_id]
    if len(user_data) == 0:
        return JSONResponse(status_code=404,content={'error': f"User with id '{user_id}' not found"})
    response = user_data.to_dict(orient='records')
    return JSONResponse(status_code=200,content={"results":response})

# Sentiment Analysis: recibe un str con el año que deseas evaluar
# Retorna el analisis
@app.get("/sentimentanalysis/{year}",tags=['Sentiment'])
def sentiment_analysis(year : str):
    '''
    **Sentiment Analysis:** recibe un str con el año que deseas evaluar y retorna la cantidad de reseñas</br>
    positivas, negativas y neutrales </br></br>

    Ejemplo: 2010</br>

        {
        "results": [
            {
            "year_released": "2010",
            "Negative": 265,
            "Neutral": 403,
            "Positive": 1341
            }]
        }
    '''
    year = year.strip()
    df = pd.read_csv('dataquery/sentiment_analysis.csv')
    df['year_released'] = df['year_released'].astype(str)
    if df['year_released'].str.contains(year).any():
        response = df[df['year_released'] == year].to_dict(orient='records')
        return JSONResponse(status_code=200,content={"results":response})
    else:
        return JSONResponse(status_code=404,content={"error":f"Year '{year}' not found"})
        

# Endpoint de la función Genero, se ingresa un genero en formato str
# Devuelve un objeto json con el genero cantidad de horas y rank
# en base de las horas jugadas totales de todos los géneros
@app.get("/genre/{genre}",tags=['Genre'])
def genre(genre : str):
    '''
    **Genre:** Recibe un string con el nombre del genero a evaluar</br>
    Devuelve el rank de las categorias con mas horas jugadas por los usuarios</br>
    y su total de horas jugadas.</br><br/>

    Ejemplo: RPG

        {
        "results": [
            {
            "Genre": "rpg",
            "Total_Hours": 1041022718,
            "Rank": 3
            }]
        }

    '''
    genre = genre.lower().strip()
    df_genre = pd.read_csv(r'./dataquery/gener_rank.csv')
    
    if df_genre['Genre'].str.contains(genre).any():
        genre_info = df_genre[df_genre['Genre']==genre]
        response = genre_info.to_dict(orient='records')
    else:
        return JSONResponse(status_code=404,content={'error':f"Genre '{genre}' not found"})
    return JSONResponse(status_code=200,content={"results":response})

# Endpoint que recibe un string para el genero y regresa el top5 de los usuarios con mas horas de juego
@app.get("/userforgenre/{genero}",tags=['Genre'])
def userforgenre( genero : str ):
    '''
    **User for genre:** Recibe un String con el genero que se desea evaluar
    Devuelve una lista ordenada de los usuarios ("User Id" y "User Url") con más horas jugadas según el ranking de cada género</br></br>

    Ejemplo: Indie

        {
        "results": [
            {
            "user_id": "wolop",
            "user_url": "http://steamcommunity.com/id/wolop"
            },
            {
            "user_id": "76561198039832932",
            "user_url": "http://steamcommunity.com/profiles/76561198039832932"
            },
            {
            "user_id": "tsunamitad",
            "user_url": "http://steamcommunity.com/id/tsunamitad"
            },
            {
            "user_id": "jimmynoe",
            "user_url": "http://steamcommunity.com/id/jimmynoe"
            },
            {
            "user_id": "lildoughnut",
            "user_url": "http://steamcommunity.com/id/lildoughnut"
            }
        ]
        }
    '''
    genero = genero.lower().strip()
    df1 = pd.read_csv(r'./dataquery/top5_users.csv')
    if genero not in df1.columns:
        return JSONResponse(status_code=404,content={'error':f"Genre '{genero}' not found"})
    
    top5 = df1.sort_values(by=genero,ascending=False).head(5).reset_index()
    response = top5[['user_id','user_url']].to_dict(orient='records')
    return JSONResponse(status_code=200,content={"results":response})

#Endpoint que recibe un desarrollador y devuelve la cantidad total de items 
# y el porcentaje de items gratis por cada año
@app.get("/developer/{developer}", tags=['Developer'])
def developer(developer : str):
    '''
    ** Developer:** Recibe un string con el nombre del desarrollador, 
    una lista de cada año donde el desarrollador publico juegos con su porcentaje de juegos free to play por año

    Ejemplo: Mortis Games

        {
        "results": [
            {
            "release_year": 2017,
            "item_count": 3,
            "porcentaje_free": 33.33
            }
        ]
        }
    '''
    df = pd.read_csv('dataquery/developer.csv')
    developer = developer.strip().lower()
    if df['developer'].str.contains(developer).any():
        data = df[df['developer'] == developer]
        response = data[['release_year','item_count','porcentaje_free']].to_dict(orient='records')
        return JSONResponse(status_code=200, content={"results":response})
    else:
        return JSONResponse(status_code=404, content={'error': f"Developer {developer} not found"})




# INGRESA EL ID DE UN JUEGO EN FORMATO INT
# DEVUELVE UNA LISTA CON LOS TOP5 RECOMENDACIONES
@app.get("/game_recommendations/{game_id}",tags=['Ml_model'])
def game_recommendations( game_id : int ):
    '''
    Ingresa el **Game id** de un juego en formato int y la función te regresa las 5 mejores recomendaciones basado en ese juego
    
    Ejemplo:</br>

        {
        "results": [
            {
            "game_id": 47730,
            "title": "Dragon Age™: Origins Awakening"
            },
            {
            "game_id": 17450,
            "title": "Dragon Age: Origins"
            },
            {
            "game_id": 17460,
            "title": "Mass Effect"
            },
            {
            "game_id": 7110,
            "title": "Jade Empire™: Special Edition"
            },
            {
            "game_id": 24980,
            "title": "Mass Effect 2"
            }
        ]
        }
    '''
    # carga de archivos
    df = pd.read_csv(r'./dataquery/model_item.csv')
    if game_id not in df['id'].values:
        return JSONResponse(status_code=404,content={'error':f"Game Id '{game_id}' not found"})

    # Obtiene la lista de recomendaciones
    result = df[df['id'] == game_id]['recommends'].iloc[0]

    # Conversion a lista
    try:
        result = ast.literal_eval(result)
    except (SyntaxError, ValueError):
        # retorno error
        return JSONResponse(status_code=404,content={'error':f"Game Id '{game_id}' not found"})

    response =[]
    for item_id in result:
        # Obtiene la información del juego recomendado
        item_info = df[df['id'] == item_id].iloc[0]  
        #append a la lista de salida
        response.append({'game_id': int(item_info['id']), 
                         'title': item_info['title']})

    return JSONResponse(status_code=200,content={"results":response})
