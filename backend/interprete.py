from instrucciones.instrucciones import *
from instrucciones.procesarInstrucciones import *



def procesar_instrucciones(instrucciones, data) :
    ## lista de instrucciones recolectadas
    for inst in instrucciones :
        if data.ambito.pila[data.ambito.longitud()-1].isBreak == True or data.ambito.pila[data.ambito.longitud()-1].isContinue == True or data.ambito.pila[data.ambito.longitud()-1].isReturn == True: 
            return
        else:
            if isinstance(inst, Imprimir) : procesar_imprimir(inst.cadena, data)
            elif isinstance(inst, Imprimire) : procesar_imprimire(inst.cadena, inst.expresiones, data)
            elif isinstance(inst, Declaracion1) : procesar_declaracion1(inst.id, inst.expresion, data)
            elif isinstance(inst, Declaracion2) : procesar_declaracion2(inst.id, inst.tipoDato, inst.expresion, data)
            elif isinstance(inst, DeclaracionMutable1) : procesar_declaracionM1(inst.id, inst.expresion, data)
            elif isinstance(inst, DeclaracionMutable2) : procesar_declaracionM2(inst.id, inst.tipoDato, inst.expresion, data)
            elif isinstance(inst, Asignacion) : procesar_asignacion(inst.id, inst.expresion, data)
            elif isinstance(inst, If): procesar_if(inst.condicion, inst.instrucciones, data)
            elif isinstance(inst, If_Else): procesar_if_else(inst.condicion, inst.instrucciones, inst.ielse, data)
            elif isinstance(inst, While): procesar_while(inst.condicion, inst.instrucciones, data)
            elif isinstance(inst, For): procesar_for(inst.variable, inst.condicion, inst.paso, inst.instrucciones, data)
            elif isinstance(inst, Break): procesar_break(inst.expresion, data)
            elif isinstance(inst, Continue): procesar_continue(data)
            elif isinstance(inst, Loop) : procesar_loop(inst.instrucciones, data)
            elif isinstance(inst, Funcion): procesar_funcion(inst.nombre, inst.tipo, inst.parametros, inst.instrucciones, data)
            elif isinstance(inst, DeclaracionArreglo): procesar_declaracion_arreglo(inst.nombre, inst.tamanio, inst.expresiones, data)
            elif isinstance(inst, DeclaracionArregloM): procesar_declaracion_arreglo_mutable(inst.nombre, inst.tamanio, inst.expresiones, data)
            elif isinstance(inst, DeclaracionArregloMST): procesar_declaracion_arreglo_mutable_st(inst.nombre, inst.expresiones, data)
            elif isinstance(inst, DeclaracionArregloST): procesar_declaracion_arreglo_st(inst.nombre, inst.expresiones, data)
            elif isinstance(inst, DeclaracionVector): procesar_declaracion_vector(inst.nombre, inst.tipo, inst.valor, inst.capacidad, inst.mutable, data)
            elif isinstance(inst, DeclaracionVector2): procesar_declaracion_vector2(inst.nombre, inst.tipo, inst.mutable, inst.capacidad, data)
            elif isinstance(inst, ModificarArray): procesar_modificar_arreglo(inst.acceso, inst.expresion, data)
            elif isinstance(inst, Vinsert): vector_insert(inst.id, inst.posicion, inst.expresion, data)
            elif isinstance(inst, Vpush): vector_push(inst.id, inst.expresion, data)
            elif isinstance(inst, Vremove): vector_remove(inst.id, inst.posicion, data)
            else :
                if(isinstance(inst, ExpresionUnaria) or isinstance(inst, ExpresionRelacional) or
                isinstance(inst, ExpresionPotencia) or isinstance(inst, ExpresionAritmetica) or
                isinstance(inst, ExpresionLogica) or isinstance(inst, ExpresionInicial) or isinstance(inst, ExpresionInstruccion)): 
                    if data.ambito.pila[data.ambito.longitud()-1].nombre == "If" or data.ambito.pila[data.ambito.longitud()-1].nombre == "Else":
                        procesar_expresion(inst, data)
                    else:
                        temp_ambito = data.ambito.pila[len(data.ambito.pila)-1].nombre
                        data.errores.insertar("La instruccion de expresion no esta dentro de un if", temp_ambito, 0, 0, data.texto)
                        print("No esta dentro del if")
                else:
                    print('Error: instrucción no válida')
                

def procesar_globales(instrucciones, data):
    for inst in instrucciones:
        if isinstance(inst, Funcion) : procesar_funcion_global(inst.nombre, inst.tipo, inst.parametros, inst.instrucciones, data)
        elif isinstance(inst, Modulo) : procesar_modulo_global(inst.nombre, inst.instrucciones, data)
        elif isinstance(inst, Struct) : procesar_struct_global(inst.nombre, inst.campos, data)
        else:
            print("no se que paso, pero esto no debe estar aqui")
    


