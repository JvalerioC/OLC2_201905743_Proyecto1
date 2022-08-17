from tokenize import String
from ts import TablaSimbolos
from instrucciones.instrucciones import Loop, If, If_Else
from expresiones.expresiones import *
from expresiones.aritmetica import *
from expresiones.logica import *
from expresiones.relacional import *


class Operacion():
    def __init__(self):
        '''clase para la operacion'''

    def ejecutar(self, expresion, data):

        if isinstance(expresion, ExpresionAritmetica):
            exp1 = self.ejecutar(expresion.expresion1, data)
            exp2 = self.ejecutar(expresion.expresion2, data)
            return aritmetica(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionLogica):
            exp1 = self.ejecutar(expresion.expresion1, data)
            exp2 = self.ejecutar(expresion.expresion2, data)
            return logica(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionRelacional):
            exp1 = self.ejecutar(expresion.expresion1, data)
            exp2 = self.ejecutar(expresion.expresion2, data)
            return relacional(exp1, exp2, expresion.operador, exp1.linea, exp1.columna, data)
        
        elif isinstance(expresion, ExpresionUnaria):
            exp1 = self.ejecutar(expresion.expresion, data)
            return unaria(exp1, expresion.operador, exp1.linea, exp1.columna, data)
        
        elif isinstance(expresion, ExpresionPotencia):
            exp1 = self.ejecutar(expresion.expresion1, data)
            exp2 = self.ejecutar(expresion.expresion2, data)
            return potencia(exp1, exp2, expresion.tipo, expresion.tipoP, exp1.linea, exp1.columna, data)

        elif isinstance(expresion, ExpresionInicial):
            resultado = Retorno()
            if expresion.expresion.type == "TRUE" or expresion.expresion.type == "FALSE":
                resultado.tipo = "BOOL"
                if expresion.expresion.value.upper() == "TRUE":
                    resultado.valor = True
                elif expresion.expresion.value.upper() == "FALSE":
                    resultado.valor = False
            elif expresion.expresion.type == "ID":
                simbol = data.ambito.obtenerSimbolo(expresion.expresion.value, data.ambito.longitud()-1)
                if simbol == 0:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                else:
                    resultado.tipo = simbol.tipoDato
                    resultado.valor = simbol.valor
            else:
                resultado.tipo = expresion.expresion.type
                resultado.valor = expresion.expresion.value
            resultado.linea = expresion.expresion.lineno
            resultado.columna = expresion.expresion.lexpos
            return resultado
        elif isinstance(expresion, ExpresionInstruccion):
            resultado = Retorno()
            if isinstance(expresion.instruccion, Loop):  resultado = expresion_loop(expresion.instruccion.instrucciones, data)
            elif isinstance(expresion.instruccion, If):  resultado = expresion_if(expresion.instruccion.condicion, expresion.instruccion.instrucciones, data)
            elif isinstance(expresion.instruccion, If_Else): resultado = expresion_elif(expresion.instruccion.condicion, expresion.instruccion.instrucciones, expresion.instruccion.ielse, data)
            else: print("la expresion instruccion a buscar no es valida")
            return resultado
        elif isinstance(expresion, ExpresionAcceso): 
            resultado = Retorno()
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                    resultado.tipo = "error"
                    resultado.valor = "error"
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    try:
                        temp1 = simbol.valor
                        for i in expresion.acceso:
                            temp1 = temp1[i]
                            
                        resultado.valor = temp1
                        resultado.tipo = simbol.tipoDato
                    except:
                        resultado.tipo = "error"
                        resultado.valor = "error"
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

def tipoDatoE(expresion):
    if isinstance(expresion, list): return "Arreglo"
    elif isinstance(expresion, int): return "ENTERO"
    elif isinstance(expresion, str): 
        if len(expresion) > 1:
            return "CADENA"
        else:
            return "CARACTER"
    elif isinstance(expresion, float): return "DECIMAL"
    elif isinstance(expresion, bool): return "BOOL"
    else:
        return "error"

def expresion_loop(instrucciones, data):
    from interprete import procesar_instrucciones
    resultado = Retorno()
    new_ts = TablaSimbolos()
    new_ts.nombre = "Loop"
    new_ts.isLoop = True
    data.ambito.ingresar(new_ts)
    while(True):
        procesar_instrucciones(instrucciones, data)
        if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
            resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
            break
        if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
            data.ambito.pila[data.ambito.longitud()-1].isContinue = False
    data.ambito.eliminar()
    return resultado

def expresion_if(condicion, instrucciones, data):
    op = Operacion()
    resultado = Retorno()
    dato =  op.ejecutar(condicion, data)
    if dato.valor == True:
        from interprete import procesar_instrucciones
        new_ts = TablaSimbolos()
        new_ts.nombre = "If"
        data.ambito.ingresar(new_ts)
        procesar_instrucciones(instrucciones, data)
        resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
        data.ambito.eliminar()
    return resultado

def expresion_elif(condicion, instrucciones, ielse, data):
    op = Operacion()
    resultado = Retorno()
    dato =  op.ejecutar(condicion, data)
    if dato.valor == True:
        from interprete import procesar_instrucciones
        new_ts = TablaSimbolos()
        new_ts.nombre = "If"
        data.ambito.ingresar(new_ts)
        procesar_instrucciones(instrucciones, data)
        resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
        data.ambito.eliminar()
        return resultado
    else:
        from instrucciones.instrucciones import If_Else, If
        if isinstance(ielse, If_Else) : resultado = expresion_elif(ielse.condicion, ielse.instrucciones, ielse.ielse, data)
        elif isinstance(ielse, If) : resultado = expresion_if(ielse.condicion, ielse.instrucciones, ielse.ielse, data)
        else:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = "Else"
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(ielse, data)
            resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
            data.ambito.eliminar()
        return resultado
