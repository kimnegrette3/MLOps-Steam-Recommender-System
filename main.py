from fastapi import FastAPI

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