class Struct():
    def __init__(self, nombre, campos, fila, columna):
        self.nombre = nombre
        self.campos = campos
        self.fila = fila
        self.columna = columna

class Campo():
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = 0

class TablaStruct():
    def __init__(self, structs = []):
        self.structs = structs

    def insertar(self, nombre, campos, fila, columna, texto):
        st = self.obtener(nombre)
        if(st == 0):
            columnaF = self.find_column(texto, columna)
            self.structs.append(Struct(nombre, campos, fila, columnaF))
        else:
            #aqui va el error semantico
            print("no se puede declarar struct, ya existe")

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def limpiar(self):
        self.structs = []

    def obtener(self, nombre):
        res = 0
        for struct in self.structs:
            if(struct.nombre == nombre):
                res = struct
                break
        return res

    def llamar(self, nombre, parametros):
        res = 0
        for struct in self.structs:
            if(struct.nombre == nombre):
                if(len(parametros) == 0 and len(struct.parametros) == 0):
                    res = struct
                else:
                    if(len(parametros) == len(struct.parametros)):
                        for i in range(len(parametros)):
                            if(parametros[i].tipo == struct.parametros[i].tipo):
                                res =  struct
                            else:
                                res = 0
                                break
        return res