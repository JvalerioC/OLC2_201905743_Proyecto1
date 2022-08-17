class Nodo_AST():
    def __init__(self, etiqueta, valor, tipo, fila, columna):
        self.etiqueta = etiqueta
        self.valor = valor
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.hijos = []

    def agregarHijo(self, nodo):
        self.hijos.append(nodo)