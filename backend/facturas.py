class Facturas():
    file = ""
    listafec = []
    listaref = []
    listanite = []
    listanitrec = []
    listavalor = []
    listaiva = []
    listatot = []
    listacom = [] #Si el valor es 1, fue aprobada, si es 0 la reprobé Hora 4:13 am
    contadorvalidos = 0
    ivaem = []
    ivarec = []
    contadorerrores = 0
    contadordefacturas = 0
    contadoremisores = []
    condaroreceptores = []
    erremisores = 0
    errreceptores = 0
    erriva = 0
    errref = 0
    errtotal = 0
    def __init__(self,fecha,ref,nitre,nitem,valor,iva,total,compro):
        self.fecha = fecha
        self.ref = ref
        self.nitre = nitre
        self.nitem = nitem
        self.valor = valor
        self.iva = iva
        self.total = total
        self.compro = compro

    def crear(self,fecha,ref,nitre,nitem,valor,iva,total,compro):
        print("matat")
        return "hola"
    
