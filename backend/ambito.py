from ts import Simbolo


class AmbitoTS():

    def __init__(self, name, pila = []):
        self.pila = pila
        self.name = name
    
    def ingresar(self, ts):
        self.pila.append(ts)

    def eliminar(self):
        self.pila.pop()

    def obtener(self):
        return self.pila

    def longitud(self):
        return len(self.pila)

    def limpiar(self):
        self.pila = []
    
    def ingresarSimbolo(self, id, valor, tipoSimbolo, tipoDato, ambito, mutable, linea, columna, texto):
        columnaF = self.find_column(texto, columna)
        simbol = Simbolo(id, valor, tipoSimbolo, tipoDato, ambito, mutable, linea, columnaF)
        self.pila[len(self.pila)-1].ingresar(simbol)
    
    def ingresarSimboloV(self, id, valor, tipoSimbolo, tipoDato, ambito, mutable, linea, columna, texto, capacidad):
        columnaF = self.find_column(texto, columna)
        simbol = Simbolo(id, valor, tipoSimbolo, tipoDato, ambito, mutable, linea, columnaF)
        if capacidad == None:
            self.pila[len(self.pila)-1].ingresar(simbol)
        else:
            simbol.capacidad = capacidad
            self.pila[len(self.pila)-1].ingresar(simbol)
        

    def find_column(self, input, pos): 
        line_start = input.rfind('\n', 0, pos) + 1 
        return (pos - line_start) + 1

    def obtenerSimbolo(self, id, posicion):
        simbol = 0
        if(posicion > 0):
            if (self.pila[posicion].isFuncion or self.pila[posicion].isMetodo):
                simbol = self.pila[posicion].obtener(id)
                if(simbol != 0):
                    return simbol
                else:
                    simbol = self.pila[0].obtener(id)
                    if(simbol != 0):
                        return simbol
                    else:
                        return 0
            else:
                simbol = self.pila[posicion].obtener(id)
                if simbol == 0:
                    simbol = self.obtenerSimbolo(id, posicion-1)

                return simbol
        else:
            simbol = self.pila[0].obtener(id)
            return simbol
    
    def modificarSimbolo(self, simbolo, posicion):
        simbol = 0
        if(posicion > 0):
            if (self.pila[posicion].isFuncion or self.pila[posicion].isMetodo):
                simbol = self.pila[posicion].modificar(simbolo)
                if(simbol != 0):
                    return
                else:
                    simbol = self.pila[0].modificar(simbolo)
                    return 
            else:
                simbol = self.pila[posicion].modificar(simbolo)
                if simbol == 0:
                    simbol = self.modificarSimbolo(simbolo, posicion-1)
                    return
        else:
            simbol = self.pila[0].modificar(simbolo)
            return

