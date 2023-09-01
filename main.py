from fastapi import FastAPI
import pandas as pd

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

@app.get("/sentimentanalysis")
def sentiment_analysis(año : str):
    df = pd.read_csv('dataquery/sentiment_analysis.csv')
    if año in df['year_released']:
        return df[df['year_released'] == año]
    else:
        return 'Year not found'
        