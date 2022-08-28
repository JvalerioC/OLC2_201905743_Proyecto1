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
                print(expresion.expresion.type, expresion.expresion.value)
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
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    try:
                        temp1 = simbol.valor
                        for i in expresion.acceso:
                            dato = self.ejecutar(i, data)
                            if dato.tipo == "ENTERO":
                                temp1 = temp1[dato.valor]
                            
                        resultado.valor = temp1
                        resultado.tipo = simbol.tipoDato
                    except:
                        resultado.tipo = "error"
                        resultado.valor = "error"
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

        elif isinstance(expresion, ExpresionRemove):
            resultado = Retorno()
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Vector" and simbol.mutable:
                    temp = simbol.valor
                    resultado.tipo = simbol.tipoDato
                    resultado.valor = temp.pop(expresion.posicion.value)
                    simbol.valor = temp
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector o el vector no es mutable", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

        elif isinstance(expresion, ExpresionContains):
            resultado = Retorno()
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    dato = self.ejecutar(expresion.expresion, data)
                    if dato.tipo == simbol.tipoDato:
                        resultado.tipo = "BOOL"
                        resultado.valor = dato.valor in simbol.valor
                    else:
                        resultado.tipo = "error"
                        resultado.valor = "error"
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado
        
        elif isinstance(expresion, ExpresionAbsoluto):
            resultado = Retorno()
            
            dato = self.ejecutar(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == 0 or dato.tipo == "error":
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, dato.linea, dato.columna, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                    resultado.tipo = dato.tipo
                    resultado.valor = abs(dato.valor)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("no es posible calcular el valor absoluto, la expresion no es numerica", temp_ambito, dato.linea, dato.columna, data.texto)
                    resultado.tipo = "error"
                    resultado.valor = "error"
            return resultado

        elif isinstance(expresion, ExpresionClone):
            resultado = Retorno()
            resultado.linea = expresion.id.lineno
            resultado.columna = expresion.id.lexpos
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                resultado.tipo = simbol.tipoDato
                resultado.valor = simbol.valor
            return resultado

        elif isinstance(expresion, ExpresionRaiz):
            resultado = Retorno()
            dato = self.ejecutar(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == 0 or dato.tipo == "error":
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, dato.linea, dato.columna, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else: 
                if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                    resultado.tipo = "DECIMAL"
                    resultado.valor = pow(dato.valor, 0.5)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("no es posible calcular la raiz, la expresion no es numerica", temp_ambito, dato.linea, dato.columna, data.texto)
                    resultado.tipo = "error"
                    resultado.valor = "error"
            return resultado

        elif isinstance(expresion, ExpresionToString):
            resultado = Retorno()
            dato = self.ejecutar(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == 0 or dato.tipo == "error":
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expreson no es valida", temp_ambito, dato.linea, dato.columna, data.texto)
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                resultado.tipo = 'CADENA'
                resultado.valor = str(dato.valor)
            return resultado

        elif isinstance(expresion, ExpresionCapacity):
            resultado = Retorno()
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Vector":
                    resultado.tipo = "ENTERO"
                    if simbol.capacidad == None:
                        resultado.valor = len(simbol.valor)+1
                    else:
                        resultado.valor = encontrar_capacidad(simbol.valor, simbol.capacidad)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado

        elif isinstance(expresion, ExpresionLen):
            resultado = Retorno()
            simbol = data.ambito.obtenerSimbolo(expresion.id.value, data.ambito.longitud()-1)
            if simbol == 0:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el id al que se intenta accesar no existe", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            else:
                if simbol.tipoSimbolo == "Arreglo" or simbol.tipoSimbolo == "Vector":
                    resultado.tipo = "ENTERO"
                    resultado.valor = len(simbol.valor)
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor del id enviado no coincide con un arreglo o vector", temp_ambito, expresion.id.lineno, expresion.id.lexpos, data.texto)
            return resultado
        
        elif isinstance(expresion, ExpresionLlamada):
            resultado = expresion_llamada(expresion.id, expresion.parametros, data)
            return resultado
        
        elif isinstance(expresion, ExpresionCasteo):
            resultado = Retorno()
            dato = self.ejecutar(expresion.expresion, data)
            resultado.linea = dato.linea
            resultado.columna = dato.columna
            if dato.tipo == "ENTERO" or dato.tipo == "DECIMAL":
                if expresion.tipo.type == "FLOAT":
                    resultado.valor = float(dato.valor)
                    resultado.tipo = "DECIMAL"
                elif expresion.tipo.type == "INT":
                    resultado.valor = int(dato.valor)
                    resultado.tipo = "ENTERO"
                else:
                    resultado.tipo = "error"
                    resultado.valor = "error"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el valor no se puede castear a un tipo que no sea decimal o entero", temp_ambito, expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
            else:
                resultado.tipo = "error"
                resultado.valor = "error"
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("el valor a castear no es entero o decimal", temp_ambito, expresion.tipo.lineno, expresion.tipo.lexpos, data.texto)
            return resultado


def encontrar_capacidad(arreglo, capacidad):
    temp = ""
    if len(arreglo) > capacidad:
        temp = encontrar_capacidad(arreglo, capacidad*2)
    else:
        temp = capacidad
    return temp

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

def expresion_llamada(id, parametros, data):
    resultado = Retorno()
    resultado.linea = id.lineno
    buscar = data.funciones.obtener(id.value)
    if buscar == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la funcion no existe existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        resultado.tipo = "error"
        resultado.valor = "error"
    else:
        if parametros == None:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(buscar.instrucciones, data)
            if data.ambito.pila[data.ambito.longitud()-1].retorno == None:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la funcion no cuenta con un valor de retorno", temp_ambito, id.lineno, id.lexpos, data.texto)
                resultado.valor ="error"
                resultado.tipo = "error"
            else:
                resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
            data.ambito.eliminar()
        else:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            new_ts.isFuncion = True
            data.ambito.ingresar(new_ts)
            op = Operacion()
            hubo_error = False
            for i in range(len(parametros)):
                param = data.ambito.obtenerSimboloLlamada(parametros[i].expresion.value, data.ambito.longitud()-1)
                if (tipoDato(buscar.parametros[i].tipo.value)) == param.tipoDato:
                    if buscar.parametros[i].isReferencia == "V":
                        tipoS = "Vector"
                    elif buscar.parametros[i].isReferencia == "A":
                        tipoS = "Arreglo"
                    else:
                        tipoS = "Variable"
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.ambito.ingresarSimbolo(buscar.parametros[i].id.value, param.valor, tipoS, param.tipoDato, temp_ambito, True, id.lineno, id.lexpos, data.texto)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("un parametro no coincide con el tipo de los parametros de la funcion", temp_ambito, id.lineno, id.lexpos, data.texto)
                    hubo_error = True
                    break
            if hubo_error:
                resultado.tipo = "error"
                resultado.valor = "error"
            else:
                procesar_instrucciones(buscar.instrucciones, data)
                if data.ambito.pila[data.ambito.longitud()-1].retorno == None:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("la funcion no cuenta con un valor de retorno", temp_ambito, id.lineno, id.lexpos, data.texto)
                    resultado.valor ="error"
                    resultado.tipo = "error"
                else:
                    resultado = data.ambito.pila[data.ambito.longitud()-1].retorno
            data.ambito.eliminar()
    return resultado

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

def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"

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
