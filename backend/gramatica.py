# ANALISIS LEXICO
reservadas={
    'i64': 'INT',         #
    'f64': 'FLOAT',       #
    'bool' : 'BOOL',      #
    'char' : 'CHAR',      #
    'let' : 'LET',        #
    'mut' : 'MUTABLE',    #
    'true' : 'TRUE',      #
    'false' : 'FALSE',    #
    'if' : 'IF',            #            
    'else' : 'ELSE',        #
    'while' : 'WHILE',      #
    'println' : 'PRINT',   #
    'break' : 'BREAK',      #
    'continue' : 'CONTINUE',#
    'return' : 'RETURN',
    'loop' : 'LOOP',        #
    'match' : 'MATCH',
    'fn'    : 'FUNCION',    #
    'struct': 'STRUCT',
    'mod'   : 'MOD',
    'abs'   : 'ABS' ,
    'sqrt'  : 'RAIZ' ,
    'to_string' : 'TOSTRING' ,
    'clone' : 'CLONE' ,
    'new': 'NEW' ,
    'len'   : 'LEN' ,
    'push'  : 'PUSH' ,
    'remove' : 'REMOVE' ,
    'contains': 'CONTAINS' ,
    'insert': 'INSERT' ,
    'capacity': 'CAPACITY' ,
    'with_capacity': 'WCAPACITY' ,
    'in' : 'IN',
    'vec' : 'VECTOR',
    'Vec' : 'VEC',
    'String': 'STRING'
}

tokens  = [
    #SIMBOLOS
    'PTCOMA',       #
    'COMA',         #
    'LLAVEIZQ',     #
    'LLAVEDER',     #
    'CORCHETEIZQ',   #
    'CORCHETEDER',   #
    'PARENTESISIZQ',#
    'PARENTESISDER',#
    'ASIGNACION',   #
    'POTENCIA',     # 
    'DOSPUNTOS',    #
    'PUNTO',
    #ESTOS SON OPERADORES
    'MAS',          #
    'MENOS',        #
    'POR',          #
    'DIVIDIDO',     #
    'MODULO',       #
    'MENORIGUAL',   #
    'MAYORIGUAL',   #
    'MENORQUE',     #
    'MAYORQUE',     #
    'IGUAL',        #
    'DIFERENTE',    #
    'OR',           #
    'AND',          #
    'NOT',          #
    #ESTOS SON DATOS O VALORES, SIMBOLOS
    'DECIMAL',      #
    'ENTERO',       #
    'CADENA',       #
    'CARACTER',     #
    'STR',
    'ID'    
] + list(reservadas.values())

#Tokens
t_PTCOMA        = r';'
t_COMA          = r','
t_LLAVEIZQ      = r'{'
t_LLAVEDER      = r'}'
t_CORCHETEIZQ   = r'\['
t_CORCHETEDER   = r'\]'
t_PARENTESISIZQ = r'\('
t_PARENTESISDER = r'\)'
t_IGUAL         = r'=='
t_ASIGNACION    = r'='
t_POTENCIA      = r'(::powf|::pow)'
t_DOSPUNTOS     = r':'
t_PUNTO         = r'\.'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIVIDIDO      = r'/'
t_MODULO        = r'%'
t_MENORIGUAL    = r'<='
t_MAYORIGUAL    = r'>='
t_MENORQUE      = r'<'
t_MAYORQUE      = r'>'
t_DIFERENTE     = r'!='
t_OR            = r'\|\|'
t_AND           = r'&&'
t_NOT           = r'!'
t_STR           = r'&str'

def t_DECIMAL(t):
    r'-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] 
    return t 

def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1] 
    return t 

def t_COMENTARIO(t):
    r'//.*\n'
    t.lexer.lineno += 1

def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    try:
        t.type = reservadas.get(t.value,'ID') # Verificar palabras reservadas
    except ValueError:
        print("el valor ingresado es una palabra reservada")
        t.value = "error"
    return t

def t_newline(t): # PARA SALTOS DE LINEA
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

t_ignore = " \t" #CARACTERES IGNORADOS

def t_error(t):
    print(t)
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador lexico
from structsG import Campo
from funcionesG import Parametro
from instrucciones.instrucciones import *
from expresiones.expresiones import *
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('nonassoc', 'IGUAL', 'DIFERENTE', 'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO', 'MODULO'),
    ('right','NOT'),
    ('right','UMENOS'),
    )

# ANALISIS SINTACTICO (GRAMATICA)

def p_inicio(t) :
    'inicio            : instrucciones'
    t[0] = t[1]

def p_lista_instrucciones(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]


def p_instruccion(t) :
    '''instruccion      : inst_imprimir PTCOMA
                        | inst_declaracion PTCOMA
                        | inst_asignacion PTCOMA
                        | inst_if
                        | inst_while
                        | inst_break PTCOMA
                        | inst_continue PTCOMA
                        | inst_loop 
                        | inst_funcion
                        | inst_struct
                        | inst_mod
                        | inst_declaracion_arreglo PTCOMA
                        | inst_declaracion_vector PTCOMA
                        | inst_modificar_arreglo PTCOMA
                        | inst_vector_op PTCOMA
                        | expresion '''
    t[0] = t[1]
    

def p_instruccion_imprimir_cadena(t) :
    'inst_imprimir      : PRINT NOT PARENTESISIZQ expresion PARENTESISDER'
    t[0] = Imprimir(t[4])

def p_instruccion_imprimir_expresion(t):
    'inst_imprimir      : PRINT NOT PARENTESISIZQ expresion COMA lista_expresiones PARENTESISDER'
    t[0] = Imprimire(t[4], t[6])

def p_lista_expresiones(t):
    'lista_expresiones  : lista_expresiones COMA expresion'
    t[1].append(t[3])
    t[0] = t[1]

def p_expresiones_expresion(t):
    'lista_expresiones   : expresion'
    t[0] = [t[1]]

def p_instruccion_declaracion_mutable(t) :
    '''inst_declaracion : LET MUTABLE ID DOSPUNTOS tipo_dato ASIGNACION expresion
                        | LET MUTABLE ID ASIGNACION expresion'''
    if(len(t) == 6):
        t[0] = DeclaracionMutable1(t.slice[3], t[5])
    else:
        t[0] = DeclaracionMutable2(t.slice[3], t[5], t[7])

def p_instruccion_declaracion_inmutable(t):
    '''inst_declaracion : LET ID DOSPUNTOS tipo_dato ASIGNACION expresion
                        | LET ID ASIGNACION expresion'''
    if(len(t) == 5):
        t[0] = Declaracion1(t.slice[2], t[4])
    else:
        t[0] = Declaracion2(t.slice[2], t[4], t[6])

def p_instruccion_declaracion_array1(t):
    '''inst_declaracion_arreglo : LET ID DOSPUNTOS tamanio_tipo ASIGNACION express 
                                | LET MUTABLE ID DOSPUNTOS tamanio_tipo  ASIGNACION express '''
    if(len(t) == 7):
        t[0] = DeclaracionArreglo(t.slice[2], t[4], t[6])
    else:
        t[0] = DeclaracionArregloM(t.slice[3], t[5], t[7])

def p_instruccion_declaracion_array2(t):
    '''inst_declaracion_arreglo : LET ID ASIGNACION express 
                                | LET MUTABLE ID ASIGNACION express '''
    if(len(t) == 5):
        t[0] = DeclaracionArregloST(t.slice[2], t[4])
    else:
        t[0] = DeclaracionArregloMST(t.slice[3], t[5])

def p_tamanio_tipo(t):
    'tamanio_tipo         : CORCHETEIZQ tamanio_tipo PTCOMA ENTERO CORCHETEDER'
    t[0] = TamanioTipo(t[2], t.slice[4])

def p_tamanio_tipo2(t):
    'tamanio_tipo         : CORCHETEIZQ tipo_dato PTCOMA ENTERO CORCHETEDER'
    t[0] = TamanioTipo(t[2], t.slice[4])

def p_lista_express(t):
    'express        : express COMA express '
    temp1 = t[1]
    temp2 = t[3]
    array1 = []
    longitud = 0
    try:
        if(len(temp1)>0):
            longitud = len(temp1)
    except:
        longitud = 0
    if longitud > 0:
        for a in temp1:
            array1.append(a)
    else:
        array1.append(temp1)
    
    try:
        if(len(temp2)>0):
            longitud = len(temp2)
    except:
        longitud = 0
    if longitud > 0:
        for a in temp2:
            array1.append(a)
    else:
        array1.append(temp2)

    t[0] = array1

def p_express_express(t):
    'express        : CORCHETEIZQ express CORCHETEDER'
    t[0] = [t[2]]

def p_expres(t):
    'express     : CORCHETEIZQ lista_expresiones CORCHETEDER'
    t[0] = [t[2]]

def p_express2(t):
    'express        : CORCHETEIZQ expresion PTCOMA ENTERO CORCHETEDER'
    temp = []
    for i in range(t[4]):
        temp.append(t[2])
    
    t[0] = [temp]

def p_instruccion_asignacion(t) :
    'inst_asignacion    : ID ASIGNACION expresion'
    t[0] =Asignacion(t.slice[1], t[3])

def p_declaracion_vector(t):
    '''inst_declaracion_vector  : LET ID ASIGNACION VECTOR NOT formav
                                | LET MUTABLE ID ASIGNACION VECTOR NOT formav'''
    if len(t) == 7:
        t[0] = DeclaracionVector(t.slice[2], None, t[6], None, False)
    else:
        t[0] = DeclaracionVector(t.slice[3], None, t[7], None, True)

def p_declaracion_vector2(t):
    '''inst_declaracion_vector  : LET ID DOSPUNTOS VEC MENORQUE tipo_dato MAYORQUE ASIGNACION VEC DOSPUNTOS DOSPUNTOS NEW PARENTESISIZQ PARENTESISDER
                                | LET MUTABLE ID DOSPUNTOS VEC MENORQUE tipo_dato MAYORQUE ASIGNACION VEC DOSPUNTOS DOSPUNTOS NEW PARENTESISIZQ PARENTESISDER
                                | LET ID DOSPUNTOS VEC MENORQUE tipo_dato MAYORQUE ASIGNACION VEC DOSPUNTOS DOSPUNTOS WCAPACITY PARENTESISIZQ ENTERO PARENTESISDER
                                | LET MUTABLE ID DOSPUNTOS VEC MENORQUE tipo_dato MAYORQUE ASIGNACION VEC DOSPUNTOS DOSPUNTOS WCAPACITY PARENTESISIZQ ENTERO PARENTESISDER'''
    if len(t) == 15:
        t[0] = DeclaracionVector2(t.slice[2], t[6], False, None)
    elif len(t) == 16 and t[13] == "new":
        t[0] = DeclaracionVector2(t.slice[3], t[7], True, None)
    elif len(t) == 16 and t[12] == "with_capacity":
        t[0] = DeclaracionVector2(t.slice[2], t[6], False, t[14])
    elif len(t) == 17:
        t[0] = DeclaracionVector2(t.slice[3], t[7], True, t[15])

def p_formav(t):
    '''formav   : CORCHETEIZQ lista_expresiones CORCHETEDER
                | CORCHETEIZQ expresion PTCOMA ENTERO CORCHETEDER'''
    if len(t) == 4:
        t[0] = t[2]
    else:
        temp = []
        for i in range(t[4]):
            temp.append(t[2])
        
        t[0] = temp

def p_modificar_arreglo(t):
    'inst_modificar_arreglo : acceso_vector ASIGNACION expresion'
    t[0] = ModificarArray(t[1], t[3])

def p_acceso_arreglo(t):
    'acceso_vector  : ID lista_acceso'
    t[0] = [t.slice[1], t[2]]

def p_lista_acceso(t):
    'lista_acceso  : lista_acceso CORCHETEIZQ ENTERO CORCHETEDER'
    t[1].append(t[3])
    t[0] = t[1]

def p_acceso_accesp(t):
    'lista_acceso  : CORCHETEIZQ ENTERO CORCHETEDER'
    t[0] = [t[2]]

def p_instruccion_if(t) :
    'inst_if            : IF expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = If(t[2], t[4])

def p_instruccion_if_else(t):
    'inst_if            : IF expresion LLAVEIZQ instrucciones LLAVEDER ELSE else'
    t[0] = If_Else(t[2], t[4], t[7])

def p_instruccion_else(t):
    '''else             : inst_if
                        | LLAVEIZQ instrucciones LLAVEDER'''
    if(len(t) == 2):
        t[0] = t[1]
    else:
        t[0] = t[2]

def p_instruccion_while(t):
    'inst_while           : WHILE expresion LLAVEIZQ instrucciones LLAVEDER'
    t[0] = While(t[2], t[4])

def p_instruccion_break(t):
    '''inst_break           : BREAK expresion
                            | BREAK'''
    if len(t) == 2:
        t[0] = Break(None)
    else:
        t[0] = Break(t[2])

def p_instruccion_continue(t):
    'inst_continue      : CONTINUE'
    t[0] = Continue()

def p_instruccion_loop(t):
    'inst_loop     : LOOP LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Loop(t[3])

def p_operacion_vector(t):
    '''inst_vector_op   : ID PUNTO INSERT PARENTESISIZQ ENTERO COMA expresion PARENTESISDER
                        | ID PUNTO PUSH PARENTESISIZQ expresion PARENTESISDER
                        | ID PUNTO REMOVE PARENTESISIZQ ENTERO PARENTESISDER'''
    if t[3] == "insert":
        t[0] = Vinsert(t.slice[1], t.slice[5], t[7])
    elif t[3] == "push":
        t[0] = Vpush(t.slice[1], t[5])
    elif t[3] == "remove":
        t[0] = Vremove(t.slice[1], t.slice[5])

#def p_instruccion_match(t):
#    'inst_match     : MATCH LLAVEIZQ instrucciones LLAVEDER'
#    print()
def p_instruccion_funcion(t):
    '''inst_funcion     : FUNCION ID PARENTESISIZQ lista_parametros PARENTESISDER LLAVEIZQ instrucciones LLAVEDER 
                        | FUNCION ID PARENTESISIZQ lista_parametros PARENTESISDER MENOS MAYORQUE tipo_dato LLAVEIZQ instrucciones LLAVEDER
                        | FUNCION ID PARENTESISIZQ PARENTESISDER LLAVEIZQ instrucciones LLAVEDER
                        | FUNCION ID PARENTESISIZQ PARENTESISDER MENOS MAYORQUE tipo_dato LLAVEIZQ instrucciones LLAVEDER'''
    if len(t) == 9:
        t[0] = Funcion(t.slice[2], None, t[4], t[7])
    elif len(t) == 8:
        t[0] = Funcion(t.slice[2], None, None, t[6])
    elif len(t) == 11:
        t[0] = Funcion(t.slice[2], t[7], None, t[9])
    else:
        t[0] = Funcion(t.slice[2], t[8], t[4], t[10])

def p_instruccion_struct(t):
    ' inst_struct   : STRUCT ID LLAVEIZQ campos LLAVEDER'
    t[0] = Struct(t.slice[2], t[4])

def p_instruccion_mod(t):
    ' inst_mod      : MOD ID LLAVEIZQ instrucciones LLAVEDER'
    t[0] = Modulo(t.slice[2], t[4])

def p_lista_campos(t):
    'campos  : campos COMA campo'
    t[1].append(t[3])
    t[0] = t[1]

def p_campo_campo(t):
    'campos   : campo'
    t[0] = [t[1]]

def p_campo(t):
    '''campo    : ID DOSPUNTOS tipo_dato
                | ID '''
    if len(t) == 2:
        t[0] = Campo(t.slice[1], None)
    else:
        t[0] = Campo(t.slice[1], t[3])

def p_lista_parametros(t):
    'lista_parametros  : lista_parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]

def p_parametro_parametro(t):
    'lista_parametros   : parametro'
    t[0] = [t[1]]

def p_parametro(t):
    'parametro  : ID DOSPUNTOS tipo_dato'
    t[0] = Parametro(t.slice[1], t[3])

def p_tipo_dato(t):
    '''tipo_dato        : INT
                        | FLOAT
                        | CHAR
                        | STRING
                        | BOOL
                        | STR'''
    t[0] = t.slice[1]

def p_expresion_agrupacion(t):
    'expresion : PARENTESISIZQ expresion PARENTESISDER'
    t[0] = t[2]

def p_expresion_aritmetica(t):
    '''expresion    : expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
                    | expresion MODULO expresion'''

    if t[2] == '+'   : t[0] = ExpresionAritmetica(t[1], t[3], OPERACION_ARITMETICA.MAS)
    elif t[2] == '-' : t[0] = ExpresionAritmetica(t[1], t[3], OPERACION_ARITMETICA.MENOS)
    elif t[2] == '*' : t[0] = ExpresionAritmetica(t[1], t[3], OPERACION_ARITMETICA.POR)
    elif t[2] == '/' : t[0] = ExpresionAritmetica(t[1], t[3], OPERACION_ARITMETICA.DIVIDIDO)
    elif t[2] == '%' : t[0] = ExpresionAritmetica(t[1], t[3], OPERACION_ARITMETICA.MODULO)

def p_expresion_relacional(t):
    '''expresion    : expresion IGUAL expresion
                    | expresion DIFERENTE expresion
                    | expresion MAYORQUE expresion
                    | expresion MENORQUE expresion
                    | expresion MAYORIGUAL expresion
                    | expresion MENORIGUAL expresion'''

    if t[2] == '==': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.IGUAL)
    elif t[2] == '!=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.DIFERENTE)
    elif t[2] == '>' : t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.MAYOR_QUE)
    elif t[2] == '<' : t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.MENOR_QUE)
    elif t[2] == '>=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.MAYOR_IGUAL)
    elif t[2] == '<=': t[0] = ExpresionRelacional(t[1], t[3], OPERACION_RELACIONAL.MENOR_IGUAL)

def p_expresion_logica(t):
    '''expresion    : expresion AND expresion
                    | expresion OR expresion'''
    if t[2] == '&&': t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.AND)
    elif t[2] == '||': t[0] = ExpresionLogica(t[1], t[3], OPERACION_LOGICA.OR)

def p_expresion_instruccion(t):
    '''expresion    : inst_loop 
                    | inst_if'''
    t[0] = ExpresionInstruccion(t[1])

def p_expresion_unaria(t):
    '''expresion    : NOT expresion
                    | MENOS expresion %prec UMENOS'''
    t[0] = ExpresionUnaria(t[1], t[2])

def p_expresion_potencia(t):
    'expresion  : tipo_dato POTENCIA PARENTESISIZQ expresion COMA expresion PARENTESISDER'
    t[0] = ExpresionPotencia(t[1], t.slice[2], t[4], t[6])

def p_expresion(t):
    '''expresion    : ENTERO
                    | DECIMAL
                    | TRUE
                    | FALSE
                    | CARACTER
                    | CADENA
                    | ID '''
    t[0] = ExpresionInicial(t.slice[1])

def p_expresion_acceso_arreglo(t):
    'expresion  : acceso_vector'
    t[0] = ExpresionAcceso(t[1])



def p_error(t):
    print(t)
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return( parser.parse(input))

