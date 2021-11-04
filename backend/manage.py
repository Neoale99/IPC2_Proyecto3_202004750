from facturas import Facturas
class Manage():
    def __init__(self):
        self.nit =  []

    def duplicadasref(ref):
        b = ref
        a = len(Facturas.listaref)
        for i in range(a):
            if b == Facturas.listaref[i]:
                Facturas.errref +=1
            i =+ 1
        
        return False
