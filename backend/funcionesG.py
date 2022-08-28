class Funcion():
    def __init__(self, nombre, tipo, parametros, instrucciones, fila, columna):
        self.nombre = nombre
        self.tipo = tipo
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.isFuncion = False

class Parametro():
    def __init__(self, id, tipo):
        self.tipo = tipo
        self.id = id
        self.valor = 0
        self.isReferencia = False

class TablaF():
    def __init__(self):
        self.funciones = []

    def insertar(self, nombre, tipo, parametros, instrucciones, fila, columna, texto):
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.funciones.append(Funcion(nombre, tipo, parametros, instrucciones, fila, columnaF))
        else:
            #aqui va el error semantico
            print("no se puede declarar funcion, ya existe")

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def limpiar(self):
        self.funciones = []

    def obtener(self, nombre):
        res = 0
        for funcion in self.funciones:
            if(funcion.nombre == nombre):
                res = funcion
                break
        return res

    def llamar(self, nombre, parametros):
        res = 0
        for funcion in self.funciones:
            if(funcion.nombre == nombre):
                if(len(parametros) == 0 and len(funcion.parametros) == 0):
                    res = funcion
                else:
                    if(len(parametros) == len(funcion.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == funcion.parametros[i].tipo):
                                res =  funcion
                            else:
                                res = 0
                                break
        return res

    