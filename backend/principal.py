from modulosG import TablaModulos
from structsG import TablaStruct
from funcionesG import TablaF
import gramatica as g
from interprete import procesar_instrucciones, procesar_globales
from Errores import *
from ts import *
from tipoDato import *
from ambito import *

tErrores = TablaErrores()
ts = TablaSimbolos()
ts.nombre = "Global"
consola = Impresion()
ambito = AmbitoTS("Unico")
ambito.ingresar(ts)
tf = TablaF()
tstruct = TablaStruct()
tm = TablaModulos()

f = open("./entrada.txt", "r", encoding="utf-8")
input = f.read()
f.close()
#print(input)
raiz = g.parse(input)

data = Datos(consola, tErrores, ambito, tf, tstruct, tm, input)
#para encontrar todas las funciones, structs y modulos globales
procesar_globales(raiz, data)

for fn in data.funciones.funciones:
    if fn.nombre == "main":
        procesar_instrucciones(fn.instrucciones, data)

print("longitud ambito global......", len(data.ambito.pila[0].simbolos))
print("longitud tabla errores......",len(data.errores.errores))
print("tablas de simbolos en ambito",data.ambito.longitud())
print("funciones globales..........",len(data.funciones.funciones))
print("structs globales............",len(data.structs.structs))
print("modulos globales............", len(data.modulos.modulos))


print(data.consola.cadena)

#print (len(data.ambito.pila[1].simbolos))
#data.ambito.pila[2].generarHTML()
#data.ambito.pila[0].generarHTML()
data.errores.generarHTML()
