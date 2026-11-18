from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

client = MongoClient(os.environ["MONGO_URI"])
db = client["ISIS2304E08202620"]    


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

#COMENTARIOS

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(db['comentarios'].find({'bar_id': bar_id}, {'_id': 0}))
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    db['comentarios'].insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.put('/bares/{bar_id}/comentarios/{usuario}')
def update_comentario(bar_id: int, usuario: str, datos: dict):
    datos['bar_id'] = bar_id
    datos['usuario'] = usuario
    datos['fecha'] = datetime.now().isoformat()
    db['comentarios'].replace_one({'bar_id': bar_id, 'usuario': usuario}, datos)
    return {'mensaje': 'Comentario actualizado correctamente'}

@app.patch('/bares/{bar_id}/comentarios/{usuario}')
def patch_comentario(bar_id: int, usuario: str, datos: dict):
    db['comentarios'].update_one({'bar_id': bar_id, 'usuario': usuario}, {'$set': datos})
    return {'mensaje': 'Campos del comentario actualizados correctamente'}

@app.delete('/bares/{bar_id}/comentarios/{usuario}')
def delete_comentario(bar_id: int, usuario: str):
    db['comentarios'].delete_one({'bar_id': bar_id, 'usuario': usuario})
    return {'mensaje': f'Comentario de {usuario} eliminado'}


#EVENTOS

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(db['eventos'].find({'bar_id': bar_id}, {'_id': 0}))
    return eventos

@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db['eventos'].insert_one(datos)
    return {'mensaje': 'Evento guardado'}

@app.put('/bares/{bar_id}/eventos/{nombre}')
def update_evento(bar_id: int, nombre: str, datos: dict):
    datos['bar_id'] = bar_id
    datos['nombre'] = nombre
    datos['fecha_creacion'] = datetime.now().isoformat()
    db['eventos'].replace_one({'bar_id': bar_id, 'nombre': nombre}, datos)
    return {'mensaje': 'Evento actualizado correctamente'}

@app.patch('/bares/{bar_id}/eventos/{nombre}')
def patch_evento(bar_id: int, nombre: str, datos: dict):
    db['eventos'].update_one({'bar_id': bar_id, 'nombre': nombre}, {'$set': datos})
    return {'mensaje': 'Campos del evento actualizados correctamente'}

@app.delete('/bares/{bar_id}/eventos/{nombre}')
def delete_evento(bar_id: int, nombre: str):
    db['eventos'].delete_one({'bar_id': bar_id, 'nombre': nombre})
    return {'mensaje': f'Evento {nombre} eliminado'}