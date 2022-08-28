from instrucciones.instrucciones import TamanioTipo
from ts import TablaSimbolos
from expresiones.operacion import *

#funciones para el procesamiento de instrucciones
def procesar_imprimir(inst, data):
    op = Operacion()
    dato = op.ejecutar(inst, data)
    #print(dato)
    if dato.valor != "error":
        if dato.tipo == "CADENA":
            data.consola.concatenar("> ")
            data.consola.concatenar(str(dato.valor))
            data.consola.concatenar("\n")
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la expresion a imprimir no es de tipo cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    else:
        print("hubo error no se puede imprimir")
    #print(consola)
def procesar_imprimire(cadena, expresiones, data):
    op = Operacion()
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA":
        if "{:?}" in dato.valor:
            procesar_imprimirV(cadena, expresiones[0], data)
        else:
            temp = dato.valor.split("{}")
            if len(temp)-1 == len(expresiones):
                cadena_temp = "> "+temp[0]
                hubo_error = False
                for i in range(len(expresiones)):
                    exp_temp = op.ejecutar(expresiones[i], data)
                    if(exp_temp.valor == "error"):
                        hubo_error = True
                        break
                    cadena_temp += str(exp_temp.valor)+temp[i+1]
                cadena_temp += "\n"
                if hubo_error:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("la expresion a mostrar no es valida", temp_ambito, dato.linea, dato.columna, data.texto)
                else:
                    data.consola.concatenar(cadena_temp)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la cantidad de expresiones no es valida para imprimir en cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la expresion a imprimir no es de tipo cadena", temp_ambito, dato.linea, dato.columna, data.texto)
    
def procesar_imprimirV(cadena, expresion, data):
    op = Operacion()
    dato = op.ejecutar(cadena, data)
    if dato.tipo == "CADENA" and "{:?}" in dato.valor:
        temp = op.ejecutar(expresion, data)
        if isinstance(temp.valor, list):
            data.consola.concatenar("> ")
            data.consola.concatenar(str(temp.valor))
            data.consola.concatenar("\n")
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("se esperaba un vector, no se puede imprimir", temp_ambito, dato.linea, dato.columna, data.texto)
        
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la cadena no incluye la opcion de imprimir arreglo, o la expresion no es de tipo CADENA", temp_ambito, dato.linea, dato.columna, data.texto)

def procesar_declaracion1(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
    if dato.tipo == 0 or dato.tipo == "error":
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el valor a asignar no es valido", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if temp == 0:
            if isinstance(dato.valor, list):
                tipe = "Arreglo"
            else:
                tipe = "Variable"
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(id.value, dato.valor, tipe, dato.tipo, temp_ambito, False, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_declaracion2(id, tipo, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    tipo = tipoD(tipo.value)
    if tipo == dato.tipo:
        temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
        if temp == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(id.value, dato.valor, "Variable", dato.tipo, temp_ambito, False, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_declaracionM1(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
    if dato.tipo == 0 or dato.tipo == "error":
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el valor a asignar no es valido", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if temp == 0:
            if isinstance(dato.valor, list):
                tipe = "Arreglo"
            else:
                tipe = "Variable"
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(id.value, dato.valor, tipe, dato.tipo, temp_ambito, True, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_declaracionM2(id, tipo, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    tipo = tipoD(tipo.value)
    if tipo == dato.tipo:
        temp = data.ambito.pila[data.ambito.longitud()-1].obtener(id.value)
        if temp == 0:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(id.value, dato.valor, "Variable", dato.tipo, temp_ambito, True, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_asignacion(id, expresion, data):
    op = Operacion()
    if  id.type == "ID":
        simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
        if(simbol == 0):
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("La variable no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            if simbol.mutable == True:
                dato = op.ejecutar(expresion, data)
                if(dato.tipo == simbol.tipoDato):
                    simbol.valor = dato.valor
                    data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("El tipo de la variable no coincide con el tipo de la expresion a asignar", temp_ambito, id.lineno, id.lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la variable no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def procesar_if(condicion, instrucciones, data):
    op = Operacion()
    dato =  op.ejecutar(condicion, data)
    if dato.valor == True:
        from interprete import procesar_instrucciones
        new_ts = TablaSimbolos()
        new_ts.nombre = "If"
        data.ambito.ingresar(new_ts)
        procesar_instrucciones(instrucciones, data)
        data.ambito.eliminar()

def procesar_if_else(condicion, instrucciones, ielse, data):
    op = Operacion()
    dato =  op.ejecutar(condicion, data)
    if dato.valor == True:
        from interprete import procesar_instrucciones
        new_ts = TablaSimbolos()
        new_ts.nombre = "If"
        data.ambito.ingresar(new_ts)
        procesar_instrucciones(instrucciones, data)
        data.ambito.eliminar()
    else:
        from instrucciones.instrucciones import If_Else
        from instrucciones.instrucciones import If
        if isinstance(ielse, If_Else) : procesar_if_else(ielse.condicion, ielse.instrucciones, ielse.ielse, data)
        elif isinstance(ielse, If) : procesar_if(ielse.condicion, ielse.instrucciones, data)
        else:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = "Else"
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(ielse, data)
            data.ambito.eliminar()

def procesar_for(variable, arreglo, inicio, fin, instrucciones, data):
    
    arreglo_temporal = 0
    #aqui manejo el arreglo para el for
    if arreglo == 0:
        temp_value = []
        op = Operacion()
        principio = op.ejecutar(inicio, data)
        final = 0
        if isinstance(fin, ExpresionInicial) or isinstance(fin, ExpresionAritmetica):
            final1 = op.ejecutar(fin, data)
            final = final1.valor
        else:
            simbol = data.ambito.obtenerSimbolo(fin.value, data.ambito.longitud()-1)
            final = len(simbol.valor)
        if principio.tipo == "ENTERO" and isinstance(final, int) :
            for i in range(principio.valor, final, 1):
                temp_value.append(i)
            arreglo_temporal = temp_value
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("no se puede recorrer el rango no es numerico ( entero) ", temp_ambito, variable.lineno, variable.lexpos, data.texto)
    else:
        if isinstance(arreglo, list):
            temp_value = []
            op = Operacion()
            for dato1  in arreglo:
                temp_dato = op.ejecutar(dato1, data)
                temp_value.append(temp_dato.valor)
            arreglo_temporal = temp_value
        elif isinstance(arreglo, ExpresionInicial):
            op = Operacion()
            temp_dato = op.ejecutar(arreglo, data)
            if temp_dato.tipo == "CADENA":
                arreglo_temporal = temp_dato.valor
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("no hay cadena para convertir a lista de caracteres", temp_ambito, variable.lineno, variable.lexpos, data.texto)
        elif arreglo.type == "ID":
            simbol = data.ambito.obtenerSimbolo(arreglo.value, data.ambito.longitud()-1)
            if isinstance(simbol.valor, list):
                arreglo_temporal = simbol.valor
            elif simbol.tipoDato == "CADENA":
                arreglo_temporal = simbol.valor
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion no es un arreglo", temp_ambito, arreglo.lineno, arreglo.lexpos, data.texto)
    
    if arreglo_temporal == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("no hay arreglo para recorrer", temp_ambito, variable.lineno, variable.lexpos, data.texto)
    else:
        from interprete import procesar_instrucciones
        for dato in arreglo_temporal:
            new_ts = TablaSimbolos()
            new_ts.nombre = "For"
            new_ts.isFor = True
            data.ambito.ingresar(new_ts)
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(variable.value, dato, "Variable", tipoDatoE(dato), temp_ambito, False, variable.lineno, variable.lexpos, data.texto)
            procesar_instrucciones(instrucciones, data)
            if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
                data.ambito.eliminar()
                break
            if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
                data.ambito.pila[data.ambito.longitud()-1].isContinue = False
            data.ambito.eliminar()

def procesar_while(condicion, instrucciones, data):
    op = Operacion()
    dato = op.ejecutar(condicion, data)
    from interprete import procesar_instrucciones
    new_ts = TablaSimbolos()
    new_ts.nombre = "While"
    new_ts.isWhile = True
    data.ambito.ingresar(new_ts)
    if dato.tipo == 0 or dato.tipo == "error":
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la expresion no cumple para el ciclo while", temp_ambito, dato.linea, dato.columna, data.texto)
    else:
        while(dato.valor):
            procesar_instrucciones(instrucciones, data)
            if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
                break
            if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
                data.ambito.pila[data.ambito.longitud()-1].isContinue = False
            dato = op.ejecutar(condicion, data)
            #print(dato.valor, dato.tipo)
        data.ambito.eliminar()

def procesar_break(expresion, data):
    temp_is_funcion = False
    if expresion == None:
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isWhile == True or data.ambito.pila[i].isFor == True or data.ambito.pila[i].isLoop == True:
                data.ambito.pila[i].isBreak = True
                break
            elif data.ambito.pila[i].isFuncion == True: 
                temp_is_funcion = True 
                break
        if temp_is_funcion == True:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion break no esta dentro de un ciclo", temp_ambito, 0, 0, data.texto)
    else:
        op = Operacion()
        resultado = op.ejecutar(expresion, data)
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isWhile == True or data.ambito.pila[i].isFor == True or data.ambito.pila[i].isLoop == True:
                data.ambito.pila[i].isBreak = True
                data.ambito.pila[i].retorno = resultado
                break
            elif data.ambito.pila[i].isFuncion == True: 
                temp_is_funcion = True 
                break
        if temp_is_funcion == True:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion break no esta dentro de un ciclo", temp_ambito, resultado.linea, resultado.columna, data.texto)
        
def procesar_continue(data):
    temp_is_funcion = False
    for i in range(data.ambito.longitud()-1, -1, -1):
        if data.ambito.pila[i].isWhile == True or data.ambito.pila[i].isFor == True: 
            data.ambito.pila[i].isContinue = True
            break
        elif data.ambito.pila[i].isFuncion == True: 
            temp_is_funcion = True 
            break
    if temp_is_funcion == True:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la instruccion continue no esta dentro de un ciclo", temp_ambito, 0, 0, data.texto)
    else:
        return

def procesar_loop(instrucciones, data):
    from interprete import procesar_instrucciones
    new_ts = TablaSimbolos()
    new_ts.nombre = "Loop"
    new_ts.isLoop = True
    data.ambito.ingresar(new_ts)
    while(True):
        procesar_instrucciones(instrucciones, data)
        if(data.ambito.pila[data.ambito.longitud()-1].isBreak == True):
            break
        if(data.ambito.pila[data.ambito.longitud()-1].isContinue == True):
            data.ambito.pila[data.ambito.longitud()-1].isContinue = False
    data.ambito.eliminar()

def procesar_match(expresion, data):
    print()

def procesar_expresion(expresion, data):
    op = Operacion()
    resultado = op.ejecutar(expresion, data)
    data.ambito.pila[data.ambito.longitud()-1].retorno = resultado

def procesar_funcion(nombre, tipo, parametros, instrucciones, data):
    print("soy una funcion")

def tipoD(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return 'CARACTER'
    if dato == "String": return "CADENA"
    if dato == "&str" : return "CADENA"

def procesar_declaracion_arreglo(nombre, tamanio, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        longitud = []
        tt = tamanio_tipo(longitud, tamanio)

        valor = calcular_array(tt[0], tt[1], expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt[1], temp_ambito, False, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_arreglo_mutable(nombre, tamanio, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        longitud = []
        tt = tamanio_tipo(longitud, tamanio)

        valor = calcular_array(tt[0], tt[1], expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt[1], temp_ambito, True, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_arreglo_mutable_st(nombre, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        tt = calcular_tipo_array(expresiones, data)
        valor = calcular_array(None, tt, expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt, temp_ambito, True, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_arreglo_st(nombre, expresiones, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        valor = []
        tt = calcular_tipo_array(expresiones, data)
        valor = calcular_array(None, tt, expresiones[0], data)
        if valor == "error":
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("Hubo un error en la declaracion de la variable", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.ambito.ingresarSimbolo(nombre.value, valor, "Arreglo", tt, temp_ambito, False, nombre.lineno, nombre.lexpos, data.texto)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def tamanio_tipo(longitud, tt):
    longitud.append(tt.tamanio.value)
    if isinstance(tt.tipo, TamanioTipo):
        return tamanio_tipo(longitud, tt.tipo)
    else:
        temp = []
        temp.append(longitud)
        temp.append(tipoD(tt.tipo.value))
        return temp

def calcular_tipo_array(expresiones, data):
    if isinstance(expresiones, ExpresionInicial):
        op = Operacion()
        dato = op.ejecutar(expresiones, data)
        return dato.tipo
    else:
        for i in expresiones:
            temp = calcular_tipo_array(i, data)
            
        return temp

def calcular_array(base, tipo, expresiones, data):
    array = []
    if isinstance(expresiones, ExpresionInicial):
        op = Operacion()
        dato = op.ejecutar(expresiones, data)
        if dato.tipo == tipo:
            return dato.valor
        else:
            return "error"
    elif expresiones == "error":
        return "error"
    else:
        for i in expresiones:
            temp = calcular_array(base, tipo, i, data)
            if temp == "error":
                array = "error"
                return "error"
            else:
                array.append(temp)
            
        return array

def procesar_declaracion_vector(nombre, tipo, valor, capacidad, mutable, data):
    is_vector = False
    op = Operacion()
    if tipo == None:
        if isinstance(valor[0], list):
            is_vector = True
        else:
            dato = op.ejecutar(valor[0], data)
            tipo1 = dato.tipo
    else:
        tipo1 = tipo
    
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    if temp == 0:
        if is_vector:
            hubo_error = False
            temp_valor = []
            for v in valor:
                dato = op.ejecutar(v[0], data)
                tipo1 = dato.tipo
                temp_valor1 = []
                for i in v:
                    dato2 = op.ejecutar(i, data)
                    if tipo1 == dato2.tipo:
                        temp_valor1.append(dato2.valor)
                    else:
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
                        hubo_error = True
                        break
                if not hubo_error:
                    temp_valor.append(temp_valor1)
                    
                else:
                    break
            if not hubo_error:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.ambito.ingresarSimboloV(nombre.value, temp_valor, "Vector", tipo1, temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad)
        else:
            temp_valor = []
            hubo_error = False
            for i in valor:
                dato1 = op.ejecutar(i, data)
                if tipo1 == dato1.tipo:
                    temp_valor.append(dato1.valor)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("el tipo de dato de la variable no coincide con el tipo de la expresion", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)
                    hubo_error = True
                    break
            if not hubo_error:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.ambito.ingresarSimboloV(nombre.value, temp_valor, "Vector", tipo1, temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_declaracion_vector2(nombre, tipo, mutable, capacidad, data):
    temp = data.ambito.pila[data.ambito.longitud()-1].obtener(nombre.value)
    valor = []
    if temp == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.ambito.ingresarSimboloV(nombre.value, valor, "Vector", tipoD(tipo.value), temp_ambito, mutable, nombre.lineno, nombre.lexpos, data.texto, capacidad)
    else:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("La variable ya existe, no se puede declarar", temp_ambito, nombre.lineno, nombre.lexpos, data.texto)

def procesar_modificar_arreglo(acceso, expresion, data):
    op = Operacion()
    id = acceso[0].value
    a = acceso[1]
    simbol = data.ambito.obtenerSimbolo(id, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("el vector o arreglo a modificar no existe no existe", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
    else:
        if simbol.mutable == True:
            if simbol.tipoSimbolo == "Arreglo":
                dato = op.ejecutar(expresion, data)
                if(dato.tipo == simbol.tipoDato):
                    temp = accesov(a, simbol.valor, dato.valor)
                    if temp == "error":
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("No es posible acceder a esta posicion del vector", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
                    else:
                        simbol.valor = temp
                        data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("El tipo de la variable no coincide con el tipo de la expresion a asignar", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("La variable no es de tipo Arreglo", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el vector o arreglo no se puede modificar, no es mutable", temp_ambito, acceso[0].lineno, acceso[0].lexpos, data.texto)

def accesov(acceso, arreglo, dato):
    vacio = []
    if len(acceso) >1:
        temp1 = arreglo[acceso[0]]
        for i in range(len(arreglo)):
            if i == acceso[0]:
                temp2 = accesov(acceso[1:], temp1, dato)
                if temp2 == "error":
                    vacio = "error"
                else:
                    vacio.append(temp2)
            else:
                vacio.append(arreglo[i])
        return vacio
    else:
        try:
            arreglo[acceso[0]] = dato
            return arreglo
        except:
            return "error"

def vector_push(id, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            if dato.tipo == simbol.tipoDato:
                temp = simbol.valor
                temp.append(dato.valor)
                simbol.valor = temp
                data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def vector_insert(id, posicion, expresion, data):
    op = Operacion()
    dato = op.ejecutar(expresion, data)
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            if dato.tipo == simbol.tipoDato:
                temp = simbol.valor
                temp.insert(posicion.value, dato.valor)
                simbol.valor = temp
                data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
            else:
                temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                data.errores.insertar("la expresion a ingresar no es del tipo de vector", temp_ambito, id.lineno, id.lexpos, data.texto)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def vector_remove(id, posicion, data):
    simbol = data.ambito.obtenerSimbolo(id.value, data.ambito.longitud()-1)
    if simbol == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("El vector no existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if simbol.mutable and simbol.tipoSimbolo == "Vector":
            temp = simbol.valor
            temp.pop(posicion.value)
            simbol.valor = temp
            data.ambito.modificarSimbolo(simbol, data.ambito.longitud()-1)
        else:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("el valor del id no es un vector o no se puede modificar, no es mutable", temp_ambito, id.lineno, id.lexpos, data.texto)

def llamada_funcion(id, parametros, data):
    buscar = data.funciones.obtener(id.value)
    if buscar == 0:
        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
        data.errores.insertar("la funcion no existe existe", temp_ambito, id.lineno, id.lexpos, data.texto)
    else:
        if parametros == None:
            from interprete import procesar_instrucciones
            new_ts = TablaSimbolos()
            new_ts.nombre = buscar.nombre
            data.ambito.ingresar(new_ts)
            procesar_instrucciones(buscar.instrucciones, data)
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
                    temp_ambito = buscar.nombre
                    data.ambito.ingresarSimbolo(buscar.parametros[i].id.value, param.valor, tipoS, param.tipoDato, temp_ambito, True, id.lineno, id.lexpos, data.texto)
                else:
                    temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                    data.errores.insertar("un parametro no coincide con el tipo de los parametros de la funcion", temp_ambito, id.lineno, id.lexpos, data.texto)
                    hubo_error = True
                    break
            if hubo_error:
                return
            else:
                procesar_instrucciones(buscar.instrucciones, data)
            data.ambito.eliminar()
            
def procesar_return(expresion, data):
    if expresion == None:
        temp = False
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isFuncion == True:
                data.ambito.pila[i].isReturn = True
                temp = True
                break
        if temp == False:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion return no esta dentro de una funcion", temp_ambito, 0, 0, data.texto)
    else:
        op = Operacion()
        temp = False
        resultado = op.ejecutar(expresion, data)
        for i in range(data.ambito.longitud()-1, -1, -1):
            if data.ambito.pila[i].isFuncion == True:
                data.ambito.pila[i].isReturn = True
                data.ambito.pila[i].retorno = resultado
                temp = True
                break
        if temp == False:
            temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
            data.errores.insertar("la instruccion return no esta dentro de una funcion", temp_ambito, resultado.linea, resultado.columna, data.texto)
    


# aqui empezare con las instrucciones globales (funciones, structs, modulos)
def procesar_funcion_global(nombre, tipo, parametros, instrucciones, data):
    if tipo == None:
        data.funciones.insertar(nombre.value, tipo, parametros, instrucciones, nombre.lineno, nombre.lexpos, data.texto)
    else:
        data.funciones.insertar(nombre.value, tipoDato(tipo.value), parametros, instrucciones, nombre.lineno, nombre.lexpos, data.texto)

def procesar_struct_global(nombre, campos, data):
    data.structs.insertar(nombre.value, campos, nombre.lineno, nombre.lexpos, data.texto)

def procesar_modulo_global(nombre, instrucciones, data):
    data.modulos.insertar(nombre.value, instrucciones, nombre.lineno, nombre.lexpos, data.texto)
    print(nombre, instrucciones)

def procesar_declaracion_struct(id, idStruct, campos, mutable, data):
    print(id, idStruct, campos, mutable)

def tipoDato(dato):
    if dato == "i64": return "ENTERO"
    if dato == "f64": return "DECIMAL"
    if dato == "bool": return "BOOL"
    if dato == "char": return "CARACTER"
    if (dato == "String" or dato == "&str"): return "CADENA"


