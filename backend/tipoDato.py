def tipoDato(dato):
    if dato.valor == "i64": return 0
    if dato.valor == "f64": return 0.0
    if dato.valor == "bool": return False
    if dato.valor == "char": return '0'
    if (dato.valor == "String" or dato.valor == "&str"): return ""

class Retorno():
    def __init__(self):
        self.tipo = 0
        self.valor = 0
        self.linea = 0
        self.columna = 0
        self.tipoS = "Variable"
    
class Impresion():
    def __init__(self):
        self.cadena = ""
    
    def concatenar(self, texto):
        self.cadena += texto
    
    def imprimir(self):
        print(self.cadena)

#esta clase es para los datos que se manejaran en la aplicacion
class Datos():
    def __init__(self, consola, errores, ambito, funciones, structs, modulos, texto):
        self.consola = consola
        self.errores = errores
        self.ambito = ambito
        self.funciones = funciones
        self.structs = structs
        self.modulos = modulos
        self.texto = texto
