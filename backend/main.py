from datetime import date, datetime
from flask import Flask,request,jsonify
from flask_cors import CORS
from manage import Manage
from xml.etree import ElementTree as ET
import re 
from datetime import datetime
from facturas import Facturas
from os import error,startfile

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
    try:

        for elemento in root:
            refe = True
            nitem = True
            nitrec = True
            ivaaa = True
            totaler = True
            print(elemento.text)
            for time in elemento.iter('TIEMPO'):
                match = re.search(r'(\d+/\d+/\d{4})',time.text)
                fecha = match.group(1)
                fecha = fecha.strip()
                Facturas.listafec.append(fecha)
                
            for ref in elemento.iter('REFERENCIA'):
                Facturas.listaref.append(ref.text) #revisar duplicada
            for nite in elemento.iter('NIT_EMISOR'):
                nitsin = nite.text.strip()
                Facturas.listanite.append(nite.text)
                if len(nitsin)>=2 and len(nitsin) <= 21 : 
                    print(nitsin)
                    listita = []
                    long = len(nitsin)
                    suma = 0
                    dig = long-1
                    contar = long
                    a = int(nitsin[dig])
                    print("aqui sigue")
                    a2 = dig
                    
                    for i in range(dig):
                        print(int(nitsin[i])*contar)
                        listita.append(int(nitsin[i])*contar)
                        a2 -=1
                        contar -=1
                    for x in range(dig):
                        suma += listita[x]
                        x +=1
                    mod = suma % 11
                    paso2 = 11-mod
                    mod2 = paso2 % 11
                    if mod2 < 10 and mod2 == a:
                        print("La factura fue validada")
                    else:
                        Facturas.contadoremisores +=1
                        nitem = False
                        
                        
            for nitre in elemento.iter('NIT_RECEPTOR'):
                nitsin = nitre.text.strip()
                Facturas.listanite.append(nitre.text)
                if len(nitsin)>=2 and len(nitsin) <= 21 : 
                    print(nitsin)
                    listita = []
                    long = len(nitsin)
                    suma = 0
                    dig = long-1
                    contar = long
                    a = int(nitsin[dig])
                    print("aqui sigue")
                    a2 = dig
                    
                    for i in range(dig):
                        print(int(nitsin[i])*contar)
                        listita.append(int(nitsin[i])*contar)
                        a2 -=1
                        contar -=1
                    for x in range(dig):
                        suma += listita[x]
                        x +=1
                    mod = suma % 11
                    paso2 = 11-mod
                    mod2 = paso2 % 11
                    if mod2 < 10 and mod2 == a:
                        print("La factura fue validada")
                    else:
                        Facturas.errreceptores +=1
                        nitrec = False
                        
                        
            for val in elemento.iter('VALOR'):
                valor = float(val.text)
                valor = round(valor,2)
                Facturas.listavalor.append(valor)
            for iva in elemento.iter('IVA'):
                IVA = round(valor*0.12,2)
                print(IVA)
                c = round(float(iva.text.strip()),2)
                print(c)
                if IVA == int(c):
                    print("yes")
                    Facturas.listaiva.append(c)
                else:
                    ivaaa = False
                    Facturas.listaiva.append(c)
                    Facturas.erriva +=1
            for tot in elemento.iter('TOTAL'):
                real = valor+IVA
                c = round(float(tot.text.strip()),2)
                Facturas.listatot.append(tot.text)
                if real == int(c):
                    print("yes")
                    Facturas.listatot.append(c)
                else:
                    totaler = False
                    Facturas.listatot.append(c)
                    Facturas.errtotal +=1
                Facturas.contadordefacturas += 1
                if nitem == False or nitrec == False or ivaaa == False or totaler == False or refe == False:
                    Facturas.contadorerrores +=1
                    Facturas.listacom.append(0)
                else :
                    Facturas.listacom.append(1)
    except:
        print()
    return jsonify({"msg":'Datos procesados y almacenados'})

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
    try:
        startfile(r'C:\Users\aleze\Desktop\USAC\Semestre 2 2021\IPC 2\Lab\Proyecto3\IPC2_Proyecto3_202004750\Documentación\Ayuda.png')
        startfile(r'C:\Users\aleze\Desktop\USAC\Semestre 2 2021\IPC 2\Lab\Proyecto3\IPC2_Proyecto3_202004750\Documentación\Reporte.pdf')
    except error:
        print(error)
    return "Abriendo menú"

@app.route('/enviar')
def enviar():
    pass

@app.route('/reset')
def reset():
    pass

@app.route('/salida')
def salida():
    a = Facturas.contadordefacturas
    b = Facturas.contadorerrores
    aprobadas = a-b
    f = open("autorizaciones.xml","w")
    f.write("""
    <LISTAAUTORIZACIONES>
 	    <AUTORIZACION>
 		    <FECHA> """+datetime.today().strftime('%d/%m/%Y')+""" </FECHA>
 		    <FACTURAS_RECIBIDAS> """+str(Facturas.contadordefacturas)+""" </FACTURAS_RECIBIDAS>
            <ERRORES>
 		        <NIT_EMISOR> """+str(Facturas.erremisores)+""" </NIT_EMISOR>
 		        <NIT_RECEPTOR> """+str(Facturas.errreceptores)+""" </NIT_RECEPTOR>
 		        <IVA> """+str(Facturas.erriva)+""" </IVA>
 		        <TOTAL> """+str(Facturas.errtotal)+""" </TOTAL>
 		        <REFERENCIA_DUPLICADA> """+str(Facturas.errref)+""" </REFERENCIA_DUPLICADA>
            </ERRORES>
 		    <FACTURAS_CORRECTAS> """+str(aprobadas)+""" </FACTURAS_CORRECTAS>
 		    <CANTIDAD_EMISORES> """+""+""" </CANTIDAD_EMISORES>
 		    <CANTIDAD_RECEPTORES> """+""+""" </CANTIDAD_RECEPTORES>
 		    <LISTADO_AUTORIZACIONES> 
                <APROBACION>
                    <NIT_EMISOR ref="""+"""> """+""+""" </NIT_EMISOR>
                    <CODIGO_APROBACION > """+""+""" </CODIGO_APROBACION>
                </APROBACION>
            <TOTAL_APROBACIONES> """+str(aprobadas)+""" </TOTAL_APROBACIONES>
        </AUTORIZACION>
    </LISTAAUTORIZACIONES >
    """)
    f.close
    return "Ola"


    

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True)