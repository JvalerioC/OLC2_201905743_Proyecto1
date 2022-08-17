from importlib.util import module_from_spec


class Modulo():
    def __init__(self, nombre, instrucciones, fila, columna):
        self.nombre = nombre
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.mod = []
        self.fn = []


class TablaModulos():
    def __init__(self):
        self.modulos = []

    def insertar(self, nombre, instrucciones, fila, columna, texto):
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.modulos.append(Modulo(nombre, instrucciones, fila, columnaF))
        else:
            #aqui va el error semantico
            print("no se puede declarar modulo, ya existe")

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def limpiar(self):
        self.modulos = []

    def obtener(self, nombre):
        res = 0
        for modulo in self.modulos:
            if(modulo.nombre == nombre):
                res = modulo
                break
        return res

    def llamar(self, nombre, parametros):
        res = 0
        for modulo in self.modulos:
            if(modulo.nombre == nombre):
                if(len(parametros) == 0 and len(modulo.parametros) == 0):
                    res = modulo
                else:
                    if(len(parametros) == len(modulo.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == modulo.parametros[i].tipo):
                                res =  modulo
                            else:
                                res = 0
                                break
        return res