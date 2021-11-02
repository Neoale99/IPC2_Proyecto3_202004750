from datetime import date, datetime
from flask import Flask,request,jsonify
from flask_cors import CORS
from manage import Manage
from xml.etree import ElementTree as ET
import re 
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/')
def home():
    return "Si sirve"

@app.route('/cargararchivo', methods=['post'])
def cargar():
    xml = str(request.data.decode('utf-8'))
    print(xml)
    root = ET.fromstring(xml)
    for elemento in root:
        print(elemento.text)
        for time in elemento.iter('TIEMPO'):
            match = re.search(r'(\d+/\d+/\d{4})',time.text)
            fecha = match.group(1)
            fecha = fecha.strip()
            try:
             date_format="%d/%m/%Y"
             datetime.strptime(fecha,date_format)
             print(fecha)
            except ValueError as err:
             print(err)
        for ref in elemento.iter('REFERENCIA'):
            print(ref.text)
        for nite in elemento.iter('NIT_EMISOR'):
            print(nite.text)
        for nitre in elemento.iter('NIT_RECEPTOR'):
            print(nitre.text)
        for val in elemento.iter('VALOR'):
            print(val.text)
        for iva in elemento.iter('IVA'):
            print(iva.text)
        for tot in elemento.iter('TOTAL'):
            print(tot.text)
    return jsonify({"msg":'si sale'})

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

@app.route('/ola')
def salida():
    f = open("autorizaciones.xml","w")
    f.write("""
    <SOLICITUD_AUTORIZACION>
 	    <DTE>
 		    <TIEMPO> """+""+""" </TIEMPO>
 		    <REFERENCIA> """+""+""" </REFERENCIA>
 		    <NIT_EMISOR> """+""+""" </NIT_EMISOR>
 		    <NIT_RECEPTOR> """+""+""" </NIT_RECEPTOR>
 		    <VALOR> """+""+""" </VALOR>
 		    <IVA> """+""+""" </IVA>
 		    <TOTAL> """+""+""" </TOTAL>
        </DTE>
    </SOLICITUD_AUTORIZACION >
    """)
    f.close
    return "Ola"
if __name__ == '__main__':
    app.run(host = 'localhost', debug = True)