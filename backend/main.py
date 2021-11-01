from flask import Flask,request,jsonify
import flask
from flask_cors import CORS

app = flask(__name__)
app.confi["DEBUG"] = True

CORS(app)

@app.route('/')
def home():
    return "Si sirve"

@app.route('/cargararchivo')
def cargar():
    pass

@app.route('/peticiones')
def peticiones():
    pass

@app.route('/peticiones/consultar')
def consultar():
    pass

@app.route('/peticiones/resumeniva')
def resumeniva():
    pass

@app.route('/peticiones/resumenrango')
def resumenrango():
    pass

@app.route('/peticiones/grafica')
def grafica():
    pass

@app.route('/peticiones/reportes')
def reportes():
    pass

@app.route('/ayuda')
def ayuda():
    pass

@app.route('/enviar')
def enviar():
    pass

@app.route('/reset')
def reset():
    pass
print("Hola")