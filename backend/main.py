from datetime import date, datetime
from flask import Flask,request,jsonify
from flask_cors import CORS
from manage import Manage
from xml.etree import ElementTree as ET
import re 
from datetime import datetime
from facturas import Facturas
from os import error, remove,startfile

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/')
def home():
    return "Si sirve"

@app.route('/cargararchivo', methods=['post'])
def cargar():
    datos()
    xml = str(request.data.decode('utf-8'))
    print(xml)
    Facturas.file = xml
    crearbase(xml)
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
                Facturas.listaref.append(ref.text.strip()) #revisar duplicada
                b = ref
                a = len(Facturas.listaref)
                for i in range(a):
                    if b == Facturas.listaref[i]:
                        Facturas.errref +=1
                        i =+ 1
                        refe = False
            for nite in elemento.iter('NIT_EMISOR'):
                nitsin = nite.text.strip()
                Facturas.listanite.append(nite.text)
                comparador = nitsin
                longitud = len(Facturas.listanite)
                for i in range(longitud):
                    if comparador == Facturas.listanite[i]:
                        Facturas.contadoremisores +=1
                        i =+ 1
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
                        Facturas.erremisores +=1
                        nitem = False
                        
                        
            for nitre in elemento.iter('NIT_RECEPTOR'):
                nitsin = nitre.text.strip()
                Facturas.listanitrec.append(nitre.text)
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
                valor = float(val.text.strip())
                valor = round(valor,2)
                Facturas.listavalor.append(valor)
            for iva in elemento.iter('IVA'):
                IVA = round(valor*0.12,2)
                print(IVA)
                c = round(float(iva.text.strip()),2)
                Facturas.ivaem.append(c)
                Facturas.ivarec.append(c)
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
        print(error)
    return jsonify({"msg":'Datos procesados y almacenados'})

@app.route('/peticiones')
def peticiones():
    return("Las posibles peticiones son: consultar,resumeninva,resumenrango,grafica,reportes")

@app.route('/peticiones/consultar')
def consultar():
    f = open("autorizaciones.xml",'r', encoding="utf-8")
    c = f.read()
    
    return(c)

@app.route('/peticiones/resumeniva')
def resumeniva():
    fecha = request.data.decode("utf-8")
    regresar = ""
    print(str(Facturas.listafec[1]))
    for i in range(Facturas.contadordefacturas):
        if fecha == str(Facturas.listafec[i]):
            Facturas.ivaem[1] = int(Facturas.listaiva[i])
    return("Sisoy")
@app.route('/peticiones/resumenrango')
def resumenrango():
    pass

@app.route('/peticiones/grafica')
def grafica():
    try:
       
        startfile(r'IPC2_Proyecto3_202004750\Documentación\ACE.pdf')
    except error:
        print(error)
    return "Abriendo menú"
@app.route('/peticiones/reportes')
def reportes():
    try:
       
        startfile(r'IPC2_Proyecto3_202004750\Documentación\sheeesh.pdf')
    except error:
        print(error)
    return "Abriendo menú"

@app.route('/ayuda')
def ayuda():
    try:
        startfile(r'IPC2_Proyecto3_202004750\Documentación\Ayuda.png')
        startfile(r'IPC2_Proyecto3_202004750\Documentación\Reporte.pdf')
    except error:
        print(error)
    return "Abriendo menú"

@app.route('/enviar')
def enviar():
    pass

@app.route('/reset')
def reset():
    try:
        remove('base.xml')
    except:
        print(error)
    return "Base de datos borrada"

@app.route('/salida')
def salida():
    a = Facturas.contadordefacturas
    b = Facturas.contadorerrores
    listaaux1 = []
    listaaux2 = []
    for i in range(len(Facturas.listanite)):
        aux = Facturas.listanite[i]
        
        if aux not in listaaux2 and Facturas.listacom[i] == 1:
            print(aux)
            listaaux2.append(aux)
    for i in range(len(Facturas.listanitrec)):
        aux = Facturas.listanitrec[i]
        
        if aux not in listaaux1 and Facturas.listacom[i] == 1:
            print(aux)
            listaaux1.append(aux)
    cantemi = len(listaaux2)
    contre = len(listaaux1)
    aprobadas = a-b
    w = ""
    
    dia = datetime.today().strftime('%d/%m/%Y')
    dia = dia.replace("/","")
    cont = 0
    for i in range(len(Facturas.listacom)):
        if Facturas.listacom[i]==1:
            cont+=1
            w+= """
                <APROBACION>
                    <NIT_EMISOR ref="""+str(Facturas.listaref[i])+"""> """+str(Facturas.listanite[i])+""" </NIT_EMISOR>
                    <CODIGO_APROBACION > """+str(dia)+str(cont)+""" </CODIGO_APROBACION>
                </APROBACION>            
            """
        
        i+=1
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
 		    <CANTIDAD_EMISORES> """+str(cantemi)+""" </CANTIDAD_EMISORES>
 		    <CANTIDAD_RECEPTORES> """+str(contre)+""" </CANTIDAD_RECEPTORES>
 		    <LISTADO_AUTORIZACIONES> 
"""+w+"""
            <TOTAL_APROBACIONES> """+str(aprobadas)+""" </TOTAL_APROBACIONES>
        </AUTORIZACION>
    </LISTAAUTORIZACIONES >
    """)
    f.close
    return "Ola"

def datos():
    comprobante = False
    try:
        f = open('base.xml','r')
        print(f)
        comprobante = True
    except:
        comprobante = False
    if comprobante == True:
        print("")
    try:
        tree = ET.parse(f)
        root = tree.getroot
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
                Facturas.listaref.append(ref.text.strip()) #revisar duplicada
                b = ref
                a = len(Facturas.listaref)
                for i in range(a):
                    if b == Facturas.listaref[i]:
                        Facturas.errref +=1
                        i =+ 1
                        refe = False
            for nite in elemento.iter('NIT_EMISOR'):
                nitsin = nite.text.strip()
                Facturas.listanite.append(nite.text)
                comparador = nitsin
                longitud = len(Facturas.listanite)
                for i in range(longitud):
                    if comparador == Facturas.listanite[i]:
                        Facturas.contadoremisores +=1
                        i =+ 1
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
                        Facturas.erremisores +=1
                        nitem = False
                        
                        
            for nitre in elemento.iter('NIT_RECEPTOR'):
                nitsin = nitre.text.strip()
                Facturas.listanitrec.append(nitre.text)
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
                valor = float(val.text.strip())
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
        print(error)   
    else:
        return     
    
def crearbase(cadena):
    f = open('base.xml',"w")
    f.write(cadena)
    f.close
    return
if __name__ == '__main__':
    app.run(host = 'localhost', debug = True)